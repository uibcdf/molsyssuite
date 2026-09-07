from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import tomllib

from devtools.scripts import bootstrap_component, check_repository, devguide_reports

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

    def test_registry_prioritizes_the_first_stabilization_cohort(self):
        data = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
        stabilization = data["stabilization"]
        self.assertEqual(
            stabilization["wave-1"],
            [
                "smonitor",
                "argdigest",
                "depdigest",
                "pyunitwizard",
                "molsysmt",
                "molsysviewer",
            ],
        )
        self.assertEqual(
            stabilization["infrastructure"],
            ["pytest-receptor", "gh-run-receptor"],
        )
        self.assertEqual(
            stabilization["incubating"],
            ["topomt", "pharmacophoremt", "elastnetmt"],
        )

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
        self.assertEqual(policy["ruff-version"], "0.16.5")
        self.assertEqual(policy["test-runner"], "pytest")
        self.assertEqual(policy["type-checker"], "repository-local")
        self.assertEqual(policy["required-lint-rules"], ["E4", "E7", "E9", "F", "I"])

    def test_reporting_lifecycle_is_a_universal_policy(self):
        data = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
        policy = data["policies"]["reporting-lifecycle"]
        self.assertEqual(policy["applies-to"], ["repository"])
        self.assertEqual(policy["issue"], "uibcdf/molsyssuite#11")
        self.assertEqual(policy["pending-kinds"], ["bug", "proposal"])
        self.assertEqual(
            policy["open-statuses"], ["open", "active", "blocked", "partial"]
        )
        self.assertEqual(
            policy["closed-statuses"], ["resolved", "withdrawn", "superseded"]
        )
        self.assertEqual(policy["archive-mode"], "repository-local")

    def test_reporting_protocol_names_member_obligations(self):
        protocol = (
            (ROOT / "devguide/reporting_protocol.md")
            .read_text(encoding="utf-8")
            .lower()
        )
        for obligation in (
            "every member repository",
            "every queued document must have an issue",
            "archive, never delete",
            "offline validator",
            "generated index",
        ):
            self.assertIn(obligation, protocol)

    def test_report_dependencies_may_reference_upstream_github_issues(self):
        self.assertIsNotNone(
            devguide_reports.CROSS_REPOSITORY_ISSUE.fullmatch(
                "pytest-dev/pytest-xdist#1372"
            )
        )

    def test_cross_component_feedback_is_a_universal_policy(self):
        data = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
        policy = data["policies"]["cross-component-feedback"]
        self.assertEqual(policy["applies-to"], ["repository"])
        self.assertEqual(policy["issue"], "uibcdf/molsyssuite#15")
        self.assertEqual(policy["provider-report-required"], True)
        self.assertEqual(policy["consumer-cross-link-required"], True)
        self.assertEqual(policy["workaround-tracking-required"], True)

    def test_component_guide_is_a_universal_policy(self):
        data = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
        policy = data["policies"]["component-guide"]
        self.assertEqual(policy["applies-to"], ["repository"])
        self.assertEqual(policy["filename"], "MOLSYSSUITE_GUIDE.md")
        self.assertEqual(policy["agents-reference-required"], True)
        guide = (ROOT / policy["normative"]).read_text(encoding="utf-8")
        for section in (
            "Where suite governance lives",
            "Reporting bugs and proposals",
            "Shared stewardship across components",
            "Common development baseline",
        ):
            self.assertIn(section, guide)

    def test_new_python_components_have_a_registered_starter_policy(self):
        data = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
        policy = data["policies"]["component-starter-kit"]
        self.assertEqual(policy["issue"], "uibcdf/molsyssuite#17")
        self.assertEqual(policy["applies-to"], ["python-library"])
        self.assertEqual(policy["adoption"], "new-repositories")


class StarterKitTests(unittest.TestCase):
    def test_generated_repository_passes_the_common_offline_gates(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "topomt"
            bootstrap_component.bootstrap(
                target,
                "uibcdf/topomt",
                "Topological molecular analysis",
            )

            findings = check_repository.check(target, "uibcdf/topomt")
            index = subprocess.run(
                [sys.executable, "devtools/devguide_index.py", "--check"],
                cwd=target,
                capture_output=True,
                check=False,
                text=True,
                timeout=30,
            )
            tests = subprocess.run(
                [sys.executable, "-m", "pytest", "-q"],
                cwd=target,
                capture_output=True,
                check=False,
                text=True,
                timeout=30,
            )
            ruff_check = subprocess.run(
                [sys.executable, "-m", "ruff", "check", "."],
                cwd=target,
                capture_output=True,
                check=False,
                text=True,
                timeout=30,
            )
            ruff_format = subprocess.run(
                [sys.executable, "-m", "ruff", "format", "--check", "."],
                cwd=target,
                capture_output=True,
                check=False,
                text=True,
                timeout=30,
            )
            texts = "\n".join(
                path.read_text(encoding="utf-8")
                for path in target.rglob("*")
                if path.is_file()
                and path.suffix in {".md", ".py", ".toml", ".yml", ".yaml"}
            )

        self.assertEqual(findings, [])
        self.assertEqual(index.returncode, 0, index.stdout + index.stderr)
        self.assertEqual(tests.returncode, 0, tests.stdout + tests.stderr)
        self.assertEqual(
            ruff_check.returncode, 0, ruff_check.stdout + ruff_check.stderr
        )
        self.assertEqual(
            ruff_format.returncode, 0, ruff_format.stdout + ruff_format.stderr
        )
        self.assertNotIn("__COMPONENT_NAME__", texts)
        self.assertNotIn("__PACKAGE_NAME__", texts)
        self.assertNotIn("__REPOSITORY__", texts)
        self.assertIn("import topomt", texts)

    def test_generator_rejects_unregistered_and_nonempty_destinations(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with self.assertRaisesRegex(ValueError, "registered in suite.toml"):
                bootstrap_component.bootstrap(
                    root / "unknown", "uibcdf/unknown", "Unknown component"
                )
            occupied = root / "topomt"
            occupied.mkdir()
            (occupied / "human-work.txt").write_text("keep", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                bootstrap_component.bootstrap(
                    occupied, "uibcdf/topomt", "Topological molecular analysis"
                )
            self.assertEqual(
                (occupied / "human-work.txt").read_text(encoding="utf-8"), "keep"
            )


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
            workflow = """\
python-version: ["3.11", "3.12", "3.13"]
run: ruff check .
run: ruff format --check .
"""
            agents = "Suite-wide reporting belongs to uibcdf/molsyssuite.\n"
            agents += "Read MOLSYSSUITE_GUIDE.md for suite governance.\n"
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
        if conforming:
            (root / "MOLSYSSUITE_GUIDE.md").write_bytes(
                (ROOT / "MOLSYSSUITE_GUIDE.md").read_bytes()
            )

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
                "GUIDE_MISSING",
                "GUIDE_POINTER",
                "PYTHON_RANGE",
                "PYTHON_CI",
                "RUFF_CONFIG",
                "RUFF_CI",
                "LEGACY_TOOL",
            },
        )

    def test_an_unregistered_repository_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            findings = check_repository.check(Path(temporary), "uibcdf/not-a-member")
        self.assertEqual([finding.code for finding in findings], ["UNREGISTERED"])

    def test_a_modified_component_guide_is_reported_as_drift(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._repository(root, conforming=True)
            guide = root / "MOLSYSSUITE_GUIDE.md"
            guide.write_text(guide.read_text(encoding="utf-8") + "\nlocal edit\n")
            findings = check_repository.check(root, "uibcdf/pyunitwizard")
        self.assertEqual([finding.code for finding in findings], ["GUIDE_DRIFT"])

    def test_ruff_configuration_without_active_ci_gates_is_not_conforming(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._repository(root, conforming=True)
            workflow = root / ".github/workflows/tests.yaml"
            workflow.write_text(
                'python-version: ["3.11", "3.12", "3.13"]\n', encoding="utf-8"
            )
            findings = check_repository.check(root, "uibcdf/pyunitwizard")
        self.assertEqual([finding.code for finding in findings], ["RUFF_CI"])

    def test_exact_shared_policy_release_counts_as_the_active_ruff_gate(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._repository(root, conforming=True)
            workflow = root / ".github/workflows/tests.yaml"
            workflow.write_text(
                'python-version: ["3.11", "3.12", "3.13"]\n'
                "uses: uibcdf/molsyssuite/.github/workflows/"
                "check-python-repository.yaml@policy-v1.1.2\n",
                encoding="utf-8",
            )
            findings = check_repository.check(root, "uibcdf/pyunitwizard")
        self.assertEqual(findings, [])

    def test_old_shared_policy_release_does_not_claim_the_new_ruff_gate(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._repository(root, conforming=True)
            workflow = root / ".github/workflows/tests.yaml"
            workflow.write_text(
                'python-version: ["3.11", "3.12", "3.13"]\n'
                "uses: uibcdf/molsyssuite/.github/workflows/"
                "check-python-repository.yaml@policy-v1.1.0\n",
                encoding="utf-8",
            )
            findings = check_repository.check(root, "uibcdf/pyunitwizard")
        self.assertEqual([finding.code for finding in findings], ["RUFF_CI"])

    def test_ruff_isort_settings_are_not_legacy_isort_tooling(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._repository(root, conforming=True)
            pyproject = root / "pyproject.toml"
            pyproject.write_text(
                pyproject.read_text(encoding="utf-8")
                + '\n[tool.ruff.lint.isort]\nknown-first-party = ["pyunitwizard"]\n',
                encoding="utf-8",
            )
            findings = check_repository.check(root, "uibcdf/pyunitwizard")
        self.assertEqual(findings, [])

    def test_actual_isort_configuration_remains_legacy_tooling(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._repository(root, conforming=True)
            pyproject = root / "pyproject.toml"
            pyproject.write_text(
                pyproject.read_text(encoding="utf-8")
                + '\n[tool.isort]\nprofile = "black"\n',
                encoding="utf-8",
            )
            findings = check_repository.check(root, "uibcdf/pyunitwizard")
        self.assertEqual([finding.code for finding in findings], ["LEGACY_TOOL"])

    def test_reusable_workflow_owns_quality_but_not_member_tests(self):
        workflow = (ROOT / ".github/workflows/check-python-repository.yaml").read_text(
            encoding="utf-8"
        )
        self.assertIn("workflow_call", workflow)
        self.assertIn("check_repository.py", workflow)
        self.assertIn("ruff==0.16.5", workflow)
        self.assertIn("ruff check", workflow)
        self.assertIn("ruff format --check", workflow)
        self.assertNotIn("pip install -e", workflow)
        self.assertNotIn("pytest", workflow)

    def test_reusable_workflow_checks_out_its_declared_policy_release(self):
        policy = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
        release = policy["governance"]["policy-release"]
        workflow = (ROOT / ".github/workflows/check-python-repository.yaml").read_text(
            encoding="utf-8"
        )
        self.assertIn(f"ref: {release}", workflow)

    def test_component_guide_sync_is_independent_of_python_conformance(self):
        workflow = (ROOT / ".github/workflows/check-component-guides.yaml").read_text(
            encoding="utf-8"
        )
        self.assertIn("check_component_guide.py", workflow)
        self.assertIn('m["repository"] for m in data["members"]', workflow)
        self.assertNotIn("check_repository.py component", workflow)
        self.assertIn("schedule:", workflow)


if __name__ == "__main__":
    unittest.main()
