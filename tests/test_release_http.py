"""A transient read failure cannot become missing or verified evidence."""

import io
import json
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError

from devtools.scripts import _release_http as http


def response(payload=b'{"state":"present"}'):
    return io.BytesIO(payload)


def failure(code, headers=None):
    return HTTPError(
        "https://example.invalid/private?secret=hidden",
        code,
        "secret=hidden",
        headers or {},
        io.BytesIO(),
    )


class EvidenceHttpTests(unittest.TestCase):
    def test_secondary_limit_and_primary_reset_cannot_trigger_early_retry(self):
        for headers in (
            {"Retry-After": "60"},
            {"X-RateLimit-Remaining": "0", "X-RateLimit-Reset": "1060"},
        ):
            with (
                self.subTest(headers=headers),
                patch.object(http, "time", return_value=1000),
                patch.object(
                    http, "urlopen", side_effect=failure(403, headers)
                ) as read,
                patch.object(http, "sleep") as sleep,
                self.assertRaises(http.EvidenceUnavailable),
            ):
                http.read_json("https://example.invalid")
            self.assertEqual(1, read.call_count)
            sleep.assert_not_called()

    def test_http_date_retry_after_and_total_backoff_budget(self):
        with (
            patch.object(http, "time", return_value=0),
            patch.object(
                http,
                "urlopen",
                side_effect=[
                    failure(503, {"Retry-After": "Thu, 01 Jan 1970 00:00:03 GMT"}),
                    response(),
                ],
            ),
            patch.object(http, "sleep") as sleep,
        ):
            self.assertEqual(
                {"state": "present"}, http.read_json("https://example.invalid")
            )
        sleep.assert_called_once_with(3)
        with (
            patch.object(
                http,
                "urlopen",
                side_effect=[
                    failure(503, {"Retry-After": "6"}),
                    failure(503, {"Retry-After": "6"}),
                ],
            ) as read,
            patch.object(http, "sleep") as sleep,
            self.assertRaises(http.EvidenceUnavailable),
        ):
            http.read_json("https://example.invalid")
        self.assertEqual(2, read.call_count)
        sleep.assert_called_once_with(6)

    def test_transient_reads_retry_then_return_real_json(self):
        with (
            patch.object(
                http, "urlopen", side_effect=[failure(502), failure(503), response()]
            ) as read,
            patch.object(http, "sleep", create=True) as sleep,
        ):
            self.assertEqual(
                {"state": "present"},
                http.read_json("https://example.invalid", "private-token"),
            )
        self.assertEqual(3, read.call_count)
        self.assertEqual([1, 2], [call.args[0] for call in sleep.call_args_list])
        for call in read.call_args_list:
            self.assertEqual("GET", call.args[0].get_method())
            self.assertEqual(20, call.kwargs["timeout"])

    def test_exhaustion_is_typed_and_does_not_leak_service_details(self):
        with (
            patch.object(
                http, "urlopen", side_effect=[failure(502) for _ in range(3)]
            ) as read,
            patch.object(http, "sleep", create=True),
            self.assertRaises(ValueError) as raised,
        ):
            http.read_json("https://example.invalid", "private-token")
        self.assertEqual(3, read.call_count)
        self.assertEqual("acquisition_unavailable", raised.exception.category)
        self.assertNotIn("hidden", str(raised.exception))
        self.assertNotIn("private-token", str(raised.exception))

    def test_nontransient_status_preserves_the_original_http_error(self):
        for code in (401, 403, 404, 422):
            error = failure(code)
            with (
                self.subTest(code=code),
                patch.object(http, "urlopen", side_effect=error) as read,
                patch.object(http, "sleep", create=True) as sleep,
                self.assertRaises(HTTPError) as raised,
            ):
                http.read_json("https://example.invalid")
            self.assertIs(error, raised.exception)
            self.assertEqual(1, read.call_count)
            sleep.assert_not_called()
            error.close()

    def test_server_retry_after_is_never_shortened_to_the_local_budget(self):
        for code in (429, 503):
            with (
                self.subTest(code=code),
                patch.object(
                    http, "urlopen", side_effect=failure(code, {"Retry-After": "60"})
                ) as read,
                patch.object(http, "sleep", create=True) as sleep,
                self.assertRaises(ValueError) as raised,
            ):
                http.read_json("https://example.invalid")
            self.assertEqual("acquisition_unavailable", raised.exception.category)
            self.assertEqual(1, read.call_count)
            sleep.assert_not_called()

    def test_retry_after_within_budget_is_honored(self):
        with (
            patch.object(
                http,
                "urlopen",
                side_effect=[failure(429, {"Retry-After": "3"}), response()],
            ),
            patch.object(http, "sleep", create=True) as sleep,
        ):
            self.assertEqual(
                {"state": "present"}, http.read_json("https://example.invalid")
            )
        sleep.assert_called_once_with(3)

    def test_network_timeout_is_bounded_but_payload_errors_are_not_retried(self):
        with (
            patch.object(
                http, "urlopen", side_effect=[URLError(TimeoutError()), response()]
            ),
            patch.object(http, "sleep", create=True) as sleep,
        ):
            self.assertEqual(
                {"state": "present"}, http.read_json("https://example.invalid")
            )
        sleep.assert_called_once_with(1)
        for payload in (
            b"not JSON",
            json.dumps([]).encode(),
            b"x" * (8 * 1024 * 1024 + 1),
        ):
            with (
                self.subTest(payload_bytes=len(payload)),
                patch.object(http, "urlopen", return_value=response(payload)) as read,
                patch.object(http, "sleep", create=True) as sleep,
                self.assertRaises(ValueError),
            ):
                http.read_json("https://example.invalid")
            self.assertEqual(1, read.call_count)
            sleep.assert_not_called()
