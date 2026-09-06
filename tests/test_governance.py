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

    def test_python_support_policy_is_exact(self):
        data = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
        policy = data["policies"]["python"]
        self.assertEqual(policy["requires-python"], ">=3.11,<3.14")
        self.assertEqual(policy["development-version"], "3.13")
        self.assertEqual(policy["ci-versions"], ["3.11", "3.12", "3.13"])

    def test_python_quality_policy_keeps_a_small_common_core(self):
        data = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
        policy = data["policies"]["python-quality"]
        self.assertEqual(policy["formatter"], "ruff")
        self.assertEqual(policy["linter"], "ruff")
        self.assertEqual(policy["test-runner"], "pytest")
        self.assertEqual(policy["type-checker"], "repository-local")
        self.assertEqual(policy["required-lint-rules"], ["E4", "E7", "E9", "F", "I"])


if __name__ == "__main__":
    unittest.main()
