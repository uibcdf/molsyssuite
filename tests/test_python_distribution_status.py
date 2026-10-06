"""Guard the separate member distribution readiness and access inventory."""

from __future__ import annotations

import copy
import unittest
from pathlib import Path
from unittest.mock import patch

import tomllib

from devtools.scripts import python_distribution_status

ROOT = Path(__file__).resolve().parents[1]


class PythonDistributionStatusTests(unittest.TestCase):
    def test_every_python_member_has_an_honest_review(self):
        data = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
        self.assertEqual(python_distribution_status.validate(data), [])
        self.assertEqual(
            len(data["python-distribution-reviews"]),
            sum(
                "python-package" in member.get("capabilities", [])
                for member in data["members"]
            ),
        )

    def test_adoption_cannot_hide_missing_evidence_or_unreviewed_recipe(self):
        data = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
        changed = copy.deepcopy(data)
        review = changed["python-distribution-reviews"][0]
        review["state"] = "adopted"
        review["review-issue"] = f"{review['repository']}#1"
        # Construct the invalid case independently of the member's actual progress.
        review.pop("evidence", None)
        review["ci-recipe"] = "pending"
        errors = python_distribution_status.validate(changed)
        self.assertTrue(any("lacks evidence" in error for error in errors))
        self.assertTrue(any("without CI/recipe readiness" in error for error in errors))

    def test_publisher_inventory_requires_all_members_and_truthful_calls(self):
        data = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
        inventory = python_distribution_status.publisher_inventory(data)
        self.assertEqual(
            python_distribution_status.validate_publishers(data, inventory), []
        )
        changed = copy.deepcopy(inventory)
        removed = changed["rows"].pop()
        self.assertIn(
            f"publisher inventory: missing {removed['repository']}",
            python_distribution_status.validate_publishers(data, changed),
        )
        changed = copy.deepcopy(inventory)
        row = next(row for row in changed["rows"] if row["kind"] == "shared-noarch")
        row["calls"][0]["uses"] = python_distribution_status.SHARED_PUBLISHER + "main"
        self.assertTrue(
            any(
                "mutable shared source" in error
                for error in python_distribution_status.validate_publishers(
                    data, changed
                )
            )
        )
        row["kind"] = "no-conda-publisher-observed"
        self.assertTrue(
            any(
                "kind contradicts calls" in error
                for error in python_distribution_status.validate_publishers(
                    data, changed
                )
            )
        )

    def test_observation_excludes_backups_and_upload_free_provider_tests(self):
        data = {"governance": {"repository": "uibcdf/example"}, "members": []}
        shared = python_distribution_status.SHARED_PUBLISHER + "a" * 40
        fixture = f"""jobs:
  publish:
    uses: {shared}
  qualification:
    steps:
      - uses: {python_distribution_status.BUILD_PROVIDER}b{"b" * 39}
        with:
          upload: false
"""

        def git_result(arguments, **kwargs):
            if arguments[1] == "rev-parse":
                return "a" * 40
            if arguments[1] == "ls-tree":
                return ".github/workflows/publish.yaml\n.github/workflows/backups/old.yaml\n"
            self.assertEqual(
                arguments[-1], "origin/main:.github/workflows/publish.yaml"
            )
            return fixture

        with patch.object(
            python_distribution_status.subprocess,
            "check_output",
            side_effect=git_result,
        ):
            inventory = python_distribution_status.observe_publishers(
                data, Path("/tmp/workspace")
            )
        row = inventory["rows"][0]
        self.assertEqual(row["kind"], "shared-noarch")
        self.assertEqual(
            row["calls"],
            [
                {
                    "workflow": ".github/workflows/publish.yaml",
                    "job": "publish",
                    "uses": shared,
                }
            ],
        )


if __name__ == "__main__":
    unittest.main()
