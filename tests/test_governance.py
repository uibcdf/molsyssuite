from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import tomllib

from devtools.scripts import check_repository

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


class RepositoryConformanceTests(unittest.TestCase):
    def _repository(self, root: Path, conforming: bool) -> None:
        (root / ".github/workflows").mkdir(parents=True)
        if conforming:
            pyproject = """\
[project]
name = "pyunitwizard"
requires-python = ">=3.11.0,<3.14.0"

[tool.ruff]
target-version = "py311"

[tool.ruff.lint]
select = ["E4", "E7", "E9", "F", "I"]
"""
            workflow = 'python-version: ["3.11", "3.12", "3.13"]\n'
            agents = "Suite-wide reporting belongs to uibcdf/molsyssuite.\n"
        else:
            pyproject = """\
[project]
name = "pyunitwizard"
requires-python = ">=3.10"

[tool.black]
line-length = 88
"""
            workflow = 'python-version: "3.10"\nrun: flake8 .\n'
            agents = "Only local instructions.\n"
        (root / "pyproject.toml").write_text(pyproject, encoding="utf-8")
        (root / ".github/workflows/tests.yaml").write_text(workflow, encoding="utf-8")
        (root / "AGENTS.md").write_text(agents, encoding="utf-8")

    def test_a_conforming_python_member_has_no_findings(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._repository(root, conforming=True)
            before = {
                path.relative_to(root): path.read_bytes()
                for path in root.rglob("*")
                if path.is_file()
            }
            findings = check_repository.check(root, "uibcdf/pyunitwizard")
            after = {
                path.relative_to(root): path.read_bytes()
                for path in root.rglob("*")
                if path.is_file()
            }
        self.assertEqual(findings, [])
        self.assertEqual(after, before)

    def test_an_audit_reports_all_independent_policy_failures(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._repository(root, conforming=False)
            findings = check_repository.check(root, "uibcdf/pyunitwizard")
        codes = {finding.code for finding in findings}
        self.assertEqual(
            codes,
            {
                "GOVERNANCE_POINTER",
                "PYTHON_RANGE",
                "PYTHON_CI",
                "RUFF_CONFIG",
                "LEGACY_TOOL",
            },
        )

    def test_an_unregistered_repository_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            findings = check_repository.check(Path(temporary), "uibcdf/not-a-member")
        self.assertEqual([finding.code for finding in findings], ["UNREGISTERED"])

    def test_reusable_workflow_only_checks_policy(self):
        workflow = (ROOT / ".github/workflows/check-python-repository.yaml").read_text(
            encoding="utf-8"
        )
        self.assertIn("workflow_call", workflow)
        self.assertIn("check_repository.py", workflow)
        self.assertNotIn("pip install", workflow)
        self.assertNotIn("pytest", workflow)


if __name__ == "__main__":
    unittest.main()
