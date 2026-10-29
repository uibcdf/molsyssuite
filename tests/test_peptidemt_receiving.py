"""Keep actual optional client use distinct from package/runtime claims."""

import unittest
from pathlib import Path

import tomllib


class PeptideMTReceivingTests(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        self.data = tomllib.loads((root / "suite.toml").read_text())
        self.edges = [
            edge
            for edge in self.data["dependency-graph"]["edges"]
            if edge["consumer"] == "peptidemt"
        ]

    def test_optional_integrations_do_not_become_fictitious_runtime_extras(self):
        runtime = {
            edge["provider"]: edge for edge in self.edges if edge["kind"] == "runtime"
        }
        self.assertEqual(set(runtime), {"depdigest", "smonitor"})
        self.assertTrue(all(not edge["optional"] for edge in runtime.values()))
        tooling = {
            edge["provider"]: edge
            for edge in self.edges
            if edge["kind"] == "test-tooling"
        }
        for provider in (
            "ackredit",
            "molsysmt",
            "argdigest",
            "pyunitwizard",
            "molsysviewer",
        ):
            with self.subTest(provider=provider):
                edge = tooling[provider]
                self.assertFalse(edge["optional"])
                self.assertNotIn("extras", edge)
                self.assertTrue(
                    any(
                        ref.startswith(
                            "uibcdf/peptidemt@7e6116ca27ed5e4fdb37620099a35b008d763365:"
                        )
                        for ref in edge["evidence"]
                    )
                )

    def test_canonical_guide_and_receiving_limits_keep_their_owners(self):
        guide = next(
            row for row in self.data["guides"] if row["filename"] == "ACKREDIT_GUIDE.md"
        )
        self.assertEqual(guide["owner"], "uibcdf/ackredit")
        self.assertEqual(guide["source"], "standards/ACKREDIT_GUIDE.md")
        self.assertIn("uibcdf/peptidemt", guide["consumers"])
        review = next(
            row
            for row in self.data["python-ecosystem-reviews"]
            if row["repository"] == "uibcdf/peptidemt"
        )
        self.assertEqual(review["review-issue"], "uibcdf/peptidemt#6")
        self.assertIn(review["support-libraries"], {"partial", "adopted"})
        self.assertIn("0.9.0", review["support-libraries-evidence"])
        ci = next(
            row
            for row in self.data["python-ci-reviews"]
            if row["repository"] == "uibcdf/peptidemt"
        )
        self.assertEqual(ci["platform-claims"], [])
