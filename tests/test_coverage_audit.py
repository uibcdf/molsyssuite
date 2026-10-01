"""Guards for separating coverage evidence from cached badges and CI health."""

import unittest

from devtools.scripts import coverage_audit as audit
from devtools.scripts import repository_badges


class CoverageAuditTests(unittest.TestCase):
    def test_public_badge_generator_and_foreign_identity_guard(self):
        badge = repository_badges.coverage_badge("uibcdf/example", "release/main")
        self.assertIn("release%2Fmain", badge)
        self.assertEqual(
            repository_badges.coverage_findings(badge, "uibcdf/example"), []
        )
        foreign = repository_badges.coverage_findings(badge, "uibcdf/other")
        self.assertEqual(
            {x.code for x in foreign},
            {"COVERAGE_BADGE_IDENTITY", "COVERAGE_BADGE_LINK"},
        )
        unsafe = badge.replace("badge.svg)", "badge.svg?token=placeholder)")
        self.assertIn(
            "COVERAGE_BADGE_QUERY",
            {
                x.code
                for x in repository_badges.coverage_findings(unsafe, "uibcdf/example")
            },
        )
        static = "[![Coverage](https://img.shields.io/badge/coverage-80%25-green)](https://app.codecov.io/gh/uibcdf/example)"
        self.assertEqual(
            {
                x.code
                for x in repository_badges.coverage_findings(static, "uibcdf/example")
            },
            {"COVERAGE_BADGE_IMAGE"},
        )
        self.assertEqual(
            repository_badges.coverage_findings(
                "No coverage claim yet", "uibcdf/example"
            ),
            [],
        )

    def report(self, **overrides):
        return {
            "commitid": "a" * 40,
            "branch": "main",
            "state": "complete",
            "timestamp": "2026-10-01T12:00:00Z",
            "totals": {"coverage": 0.0},
            **overrides,
        }

    def test_skipped_cached_totals_and_other_branches_do_not_prove_a_report(self):
        self.assertIsNone(audit.complete_report(self.report(state="skipped"), "main"))
        self.assertIsNone(audit.complete_report(self.report(branch="feature"), "main"))
        result = audit.complete_report(self.report(), "main")
        self.assertEqual(result["coverage"], 0.0)
        self.assertIn("commit_timestamp", result)
        self.assertNotIn("upload_timestamp", result)

    def test_invalid_complete_records_fail_instead_of_becoming_no_report(self):
        for value in (True, float("nan"), 101, -1, None, "90"):
            with self.subTest(value=value), self.assertRaises(audit.EvidenceInvalid):
                audit.complete_report(self.report(totals={"coverage": value}), "main")
        for overrides in (
            {"commitid": "short"},
            {"timestamp": "2026-10-01T12:00:00"},
            {"timestamp": None},
        ):
            with (
                self.subTest(overrides=overrides),
                self.assertRaises(audit.EvidenceInvalid),
            ):
                audit.complete_report(self.report(**overrides), "main")

    def test_badge_requires_svg_rendered_percentage(self):
        svg = '<svg xmlns="http://www.w3.org/2000/svg"><text>0%</text><text>0%</text></svg>'
        self.assertEqual(audit.numeric_badge(svg), ["0%"])
        for bad in (
            "<html>80%</html>",
            '<svg xmlns="http://www.w3.org/2000/svg"><text>unknown</text></svg>',
            '<svg xmlns="http://www.w3.org/2000/svg"><text>101%</text></svg>',
        ):
            with self.subTest(bad=bad), self.assertRaises(audit.EvidenceInvalid):
                audit.numeric_badge(bad)

    def fake_service(self, *, missing=False):
        calls = []

        def fetch(url, *, svg=False):
            calls.append(url)
            if "api.github.com" in url:
                return {"default_branch": "release/main"}
            if svg:
                return '<svg xmlns="http://www.w3.org/2000/svg"><text>70%</text></svg>'
            if "/branches/" in url:
                return {
                    "name": "release/main",
                    "head_commit": self.report(branch="release/main", state="skipped"),
                }
            if missing:
                raise audit.EvidenceUnavailable("HTTP 404")
            page = "page=2" in url
            report = self.report(
                branch="release/main", state="complete" if page else "skipped"
            )
            return {
                "results": [report],
                "next": None if page else "https://untrusted.example/next",
            }

        return calls, fetch

    def test_default_branch_and_bounded_pagination_ignore_untrusted_next_url(self):
        calls, fetch = self.fake_service()
        result = audit.inspect_codecov("uibcdf/example", fetch=fetch, pages=2)
        self.assertEqual(result["state"], "complete-report-observed")
        self.assertEqual(result["default_branch"], "release/main")
        self.assertEqual(result["scanned_pages"], 2)
        self.assertEqual(result["branch_cache"]["state"], "skipped")
        self.assertTrue(any("release%2Fmain" in url for url in calls))
        self.assertFalse(any("untrusted" in url for url in calls))

    def test_no_report_and_unavailability_never_become_non_applicability_or_pass(self):
        _, fetch = self.fake_service()
        bounded = audit.inspect_codecov("uibcdf/example", fetch=fetch, pages=1)
        self.assertEqual(bounded["state"], "incomplete")
        self.assertNotIn("latest_complete_report", bounded)
        _, unavailable = self.fake_service(missing=True)
        absent = audit.inspect_codecov("uibcdf/example", fetch=unavailable)
        self.assertEqual(absent["state"], "unavailable-or-invalid")
        self.assertEqual(absent["errors"]["commits"], "HTTP 404")
        self.assertNotIn("not_applicable", absent.values())


if __name__ == "__main__":
    unittest.main()
