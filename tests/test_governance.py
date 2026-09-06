from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

import tomllib

ROOT = Path(__file__).resolve().parents[1]


class GovernanceTests(unittest.TestCase):
    def test_offline_governance_guard(self):
        completed = subprocess.run(
            [sys.executable, "devtools/scripts/validate_governance.py"],
            cwd=ROOT,
            capture_output=True,
            check=False,
            text=True,
            timeout=60,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)

    def test_registry_contains_the_agreed_members(self):
        data = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
        actual = {member["name"] for member in data["members"]}
        expected = {
            "smonitor",
            "argdigest",
            "depdigest",
            "pyunitwizard",
            "pytest-receptor",
            "gh-run-receptor",
            "molsysmt",
            "molsysviewer",
            "topomt",
            "pharmacophoremt",
            "elastnetmt",
        }
        self.assertEqual(actual, expected)

    def test_report_template_cannot_impersonate_a_real_issue(self):
        template = (ROOT / "devguide/templates/report.md").read_text(encoding="utf-8")
        self.assertIn("issue: uibcdf/molsyssuite#000", template)


if __name__ == "__main__":
    unittest.main()
