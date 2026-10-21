"""Bounded JSON acquisition shared by read-only release evidence tools."""

import json
import math
from email.utils import parsedate_to_datetime
from time import sleep, time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class EvidenceError(ValueError):
    """Public service evidence is malformed or exceeds its bound."""


class EvidenceUnavailable(EvidenceError):
    """Acquisition failed; no conclusion about the underlying evidence is possible."""

    category = "acquisition_unavailable"


def error_category(error: Exception) -> str:
    """Keep acquisition and pending-metadata failures distinct in CLI receipts."""
    if isinstance(error, (HTTPError, URLError, TimeoutError, ConnectionError)):
        return "acquisition_unavailable"
    return getattr(error, "category", "invalid_evidence")


def _retry_delay(error: HTTPError, attempt: int) -> float | None:
    headers = {key.lower(): value for key, value in (error.headers or {}).items()}
    limited = (
        error.code == 429
        or headers.get("x-ratelimit-remaining") == "0"
        or (error.code == 403 and "retry-after" in headers)
    )
    if error.code not in {429, 500, 502, 503, 504} and not (
        error.code == 403 and limited
    ):
        return None
    if "retry-after" in headers:
        try:
            value = headers["retry-after"]
            delay = (
                float(value)
                if str(value).isdigit()
                else parsedate_to_datetime(value).timestamp() - time()
            )
            return max(0, math.ceil(delay)) if math.isfinite(delay) else 60
        except (ValueError, TypeError, OverflowError):
            return 60
    if limited:
        try:
            return max(0, math.ceil(float(headers["x-ratelimit-reset"]) - time()))
        except (KeyError, ValueError, TypeError, OverflowError):
            return 60
    return 2**attempt


def read_json(url: str, token: str | None = None) -> dict:
    """GET JSON with at most three requests and ten total seconds of backoff.

    Server-requested backoff is respected or refused, never truncated. Permanent
    HTTP errors retain their type (notably the caller's explicit 404 handling).
    Payload validation is performed once and is never retried.
    """
    headers = {
        "Accept": "application/json",
        "User-Agent": "molsyssuite-conda-preflight/1",
    }
    if token:
        headers["Authorization"] = "Bearer " + token
    waited = 0
    for attempt in range(3):
        try:
            with urlopen(
                Request(url, headers=headers, method="GET"), timeout=20
            ) as response:
                payload = response.read(8 * 1024 * 1024 + 1)
            break
        except HTTPError as error:
            delay = _retry_delay(error, attempt)
            if delay is None:
                raise
            status = error.code
            error.close()
            reason = f"HTTP {status}"
        except (TimeoutError, ConnectionError) as error:
            delay, reason = 2**attempt, type(error).__name__
        except URLError as error:
            if not isinstance(error.reason, (TimeoutError, ConnectionError)):
                raise
            delay, reason = 2**attempt, type(error.reason).__name__
        if attempt == 2 or waited + delay > 10:
            raise EvidenceUnavailable(
                f"read-only evidence acquisition unavailable after {attempt + 1} request(s): {reason}; retry later"
            ) from None
        sleep(delay)
        waited += delay
    if len(payload) > 8 * 1024 * 1024:
        raise EvidenceError("preflight response exceeds 8 MiB")
    result = json.loads(payload)
    if not isinstance(result, dict):
        raise EvidenceError("preflight service returned non-object metadata")
    return result
