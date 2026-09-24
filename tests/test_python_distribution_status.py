"""Guard the separate member distribution readiness and access inventory."""

from __future__ import annotations

import copy
import unittest
from pathlib import Path

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
        errors = python_distribution_status.validate(changed)
        self.assertTrue(any("lacks evidence" in error for error in errors))
        self.assertTrue(any("without CI/recipe readiness" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
