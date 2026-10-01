"""Protect delayed archival states, original deadlines and complete discovery."""

import copy
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from devtools.scripts import verify_zenodo_releases as recovery

NOW = datetime(2026, 10, 1, tzinfo=timezone.utc)
REPOSITORY = "uibcdf/molsysmt"
CONCEPT = "10.5281/zenodo.100"


def release(age, tag="1.0.0"):
    return {
        "tag_name": tag,
        "draft": False,
        "published_at": (NOW - timedelta(hours=age)).isoformat(),
    }


def record():
    return {
        "id": 101,
        "doi": "10.5281/zenodo.101",
        "conceptdoi": CONCEPT,
        "status": "published",
        "metadata": {
            "version": "1.0.0",
            "access_right": "open",
            "resource_type": {"type": "software"},
            "related_identifiers": [{"identifier": "https://github.com/" + REPOSITORY}],
        },
        "files": [
            {
                "key": "uibcdf/molsysmt-1.0.0.zip",
                "size": 10,
                "checksum": "md5:" + "a" * 32,
            }
        ],
    }


class RecoveryTests(unittest.TestCase):
    def evaluate(self, age, records=None, unavailable=False):
        return recovery.evaluate_release(
            release(age),
            records or [],
            REPOSITORY,
            CONCEPT,
            NOW,
            unavailable=unavailable,
        )

    def test_empty_query_before_deadline_is_pending_not_failure(self):
        for age in (0, 0.25, 24, 71.999):
            result = self.evaluate(age)
            self.assertEqual(result["state"], "ingestion_pending")
            self.assertFalse(result["escalation_required"])
            self.assertEqual(recovery.exit_status([result]), 0)

    def test_exact_deadline_requires_conclusive_absence(self):
        result = self.evaluate(72)
        self.assertEqual(result["state"], "absent")
        self.assertTrue(result["escalation_required"])
        self.assertEqual(recovery.exit_status([result]), 1)

    def test_service_failure_after_deadline_is_never_absence(self):
        result = self.evaluate(96, unavailable=True)
        self.assertEqual(result["state"], "temporarily_unavailable")
        self.assertTrue(result["escalation_required"])
        self.assertEqual(recovery.exit_status([result]), 2)

    def test_unindexable_record_cannot_prove_exact_version_absent(self):
        candidate = record()
        candidate["metadata"].pop("version")
        result = self.evaluate(96, [candidate])
        self.assertEqual(result["state"], "temporarily_unavailable")
        self.assertTrue(result["escalation_required"])

    def test_retry_does_not_reset_original_publication_deadline(self):
        original = release(71)
        result = recovery.evaluate_release(
            original, [], REPOSITORY, CONCEPT, NOW + timedelta(hours=2)
        )
        self.assertEqual(result["state"], "absent")
        self.assertEqual(result["published_at"], original["published_at"])

    def test_late_record_recovers_with_exact_file_evidence(self):
        result = self.evaluate(120, [record()])
        self.assertEqual(result["state"], "verified")
        self.assertEqual(result["files"], record()["files"])
        self.assertEqual(result["version_doi"], "10.5281/zenodo.101")

    def test_invalid_identity_and_file_inventory_never_pass(self):
        for change in (
            {"conceptdoi": "10.5281/zenodo.200"},
            {"doi": CONCEPT},
            {"status": "draft"},
            {"files": []},
            {
                "files": [
                    {
                        "key": "foreign-1.0.0.zip",
                        "size": 1,
                        "checksum": "md5:" + "a" * 32,
                    }
                ]
            },
            {
                "files": [
                    {
                        "key": "uibcdf/molsysmt-1.0.0.zip",
                        "size": 1,
                        "checksum": "made-up",
                    }
                ]
            },
        ):
            candidate = record()
            candidate.update(change)
            self.assertEqual(self.evaluate(1, [candidate])["state"], "invalid")
        for field, value in (
            ("access_right", "closed"),
            ("resource_type", {"type": "publication"}),
            ("related_identifiers", []),
        ):
            candidate = record()
            candidate["metadata"][field] = value
            self.assertEqual(self.evaluate(1, [candidate])["state"], "invalid")

    def test_duplicate_version_records_are_ambiguous(self):
        self.assertEqual(
            self.evaluate(1, [record(), copy.deepcopy(record())])["state"], "invalid"
        )

    def test_rollout_cutoff_is_fixed_and_old_missing_release_stays_visible(self):
        releases = [release(24, "2.0.0"), release(120), release(240, "0.1.0")]
        covered = recovery.select_releases(releases, NOW - timedelta(hours=200), NOW)
        self.assertEqual([item["tag_name"] for item in covered], ["2.0.0", "1.0.0"])
        later = recovery.select_releases(
            releases, NOW - timedelta(hours=200), NOW + timedelta(days=100)
        )
        self.assertEqual(covered, later)

    def test_draft_is_excluded_but_public_prerelease_is_covered(self):
        draft = release(1)
        draft["draft"] = True
        public = release(1, "2.0.0rc1")
        public["prerelease"] = True
        self.assertEqual(
            recovery.select_releases([draft, public], NOW - timedelta(days=1), NOW),
            [public],
        )

    def test_future_timestamp_cannot_extend_deadline(self):
        with self.assertRaises(ValueError):
            recovery.select_releases([release(-1)], NOW - timedelta(days=1), NOW)

    def test_record_pagination_requests_all_versions(self):
        calls = []

        def fetch(url, **kwargs):
            calls.append(url)
            return {
                "hits": {
                    "total": 26,
                    "hits": [record()] * (25 if len(calls) == 1 else 1),
                }
            }

        with patch.object(recovery, "fetch_json", side_effect=fetch):
            self.assertEqual(len(recovery.fetch_records(CONCEPT)), 26)
        self.assertTrue(all("all_versions=true" in url for url in calls))
        self.assertIn("page=2", calls[-1])

    def test_incomplete_record_query_cannot_prove_absence(self):
        with (
            patch.object(
                recovery,
                "fetch_json",
                return_value={"hits": {"total": 100, "hits": []}},
            ),
            self.assertRaises(recovery.EvidenceUnavailable),
        ):
            recovery.fetch_records(CONCEPT)

    def test_release_pagination_bound_is_not_silent_truncation(self):
        with (
            patch.object(recovery, "fetch_json", return_value=[release(1)] * 100),
            self.assertRaises(recovery.EvidenceUnavailable),
        ):
            recovery.fetch_releases(REPOSITORY, max_pages=1)


if __name__ == "__main__":
    unittest.main()
