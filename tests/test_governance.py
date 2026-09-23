from __future__ import annotations

import copy
import io
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

import tomllib

from devtools.scripts import (
    adoption_status,
    audit_zenodo,
    bootstrap_component,
    check_repository,
    check_vendored_guides,
    component_issue_labels,
    devguide_reports,
    repository_badges,
    suite_status,
    sync_vendored_guides,
)

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
            "lindelint",
            "ackredit",
            "dockingmt",
        }
        self.assertEqual(actual, expected)

    def test_platform_architecture_is_owned_by_moli_not_suite_registry(self):
        data = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
        self.assertNotIn("architecture", data)
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("devguide/architecture/", readme)

    def test_component_ambassador_routes_to_moli_architecture(self):
        guide = (ROOT / "MOLSYSSUITE_GUIDE.md").read_text(encoding="utf-8")
        normalized = " ".join(guide.split())
        self.assertIn("uibcdf/moli/blob/main/architecture_1.0/README.md", normalized)
        self.assertNotIn("devguide/architecture/", normalized)

    def test_registry_separates_identity_state_and_work_priority(self):
        data = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
        self.assertEqual(data["schema-version"], 2)
        classification = data["policies"]["member-classification"]
        self.assertEqual(
            classification["roles"],
            ["scientific-component", "support-library", "developer-tool"],
        )
        self.assertEqual(classification["memberships"], ["primary", "auxiliary"])
        self.assertEqual(
            classification["maturities"], ["incubating", "stabilizing", "stable"]
        )
        self.assertEqual(classification["development-modes"], ["active", "maintenance"])
        self.assertEqual(classification["capabilities"], ["python-package"])

        members = {member["name"]: member for member in data["members"]}
        for member in members.values():
            self.assertIn(member["role"], classification["roles"])
            self.assertIn(member["membership"], classification["memberships"])
            self.assertIn(member["maturity"], classification["maturities"])
            self.assertIn(
                member["development-mode"], classification["development-modes"]
            )
            self.assertTrue(
                set(member["capabilities"]) <= set(classification["capabilities"])
            )

        self.assertEqual(members["lindelint"]["membership"], "auxiliary")
        self.assertEqual(
            {
                name
                for name, member in members.items()
                if member["maturity"] == "incubating"
            },
            {"topomt", "pharmacophoremt", "elastnetmt", "ackredit", "dockingmt"},
        )
        self.assertEqual(
            {member["development-mode"] for member in members.values()}, {"active"}
        )

        stabilization = data["initiatives"]["stabilization"]
        self.assertEqual(stabilization["status"], "active")
        self.assertEqual(
            stabilization["priority-members"],
            [
                "smonitor",
                "argdigest",
                "depdigest",
                "pyunitwizard",
                "molsysmt",
                "molsysviewer",
            ],
        )

    def test_ackredit_is_registered_as_incubating_support_library(self):
        data = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
        member = next(
            member for member in data["members"] if member["name"] == "ackredit"
        )
        self.assertEqual(
            member,
            {
                "name": "ackredit",
                "repository": "uibcdf/ackredit",
                "role": "support-library",
                "membership": "primary",
                "maturity": "incubating",
                "development-mode": "active",
                "capabilities": ["python-package"],
                "zenodo-archival": "optional",
            },
        )
        guides = {guide["filename"]: guide for guide in data["guides"]}
        self.assertEqual(
            guides["ACKREDIT_GUIDE.md"],
            {
                "filename": "ACKREDIT_GUIDE.md",
                "owner": "uibcdf/ackredit",
                "source": "standards/ACKREDIT_GUIDE.md",
                "consumers": [
                    "uibcdf/molsysmt",
                    "uibcdf/molsysviewer",
                    "uibcdf/topomt",
                    "uibcdf/pharmacophoremt",
                    "uibcdf/elastnetmt",
                ],
            },
        )
        for filename in (
            "MOLSYSSUITE_GUIDE.md",
            "SMONITOR_GUIDE.md",
            "DEPDIGEST_GUIDE.md",
            "GH_RUN_RECEPTOR_GUIDE.md",
        ):
            self.assertIn("uibcdf/ackredit", guides[filename]["consumers"])
        self.assertNotIn(
            "ackredit", data["initiatives"]["stabilization"]["priority-members"]
        )
        self.assertNotIn(
            "ackredit",
            {
                component["name"]
                for component in data["policies"]["python"]["transition"]["components"]
            },
        )

    def test_pytest_receptor_guide_targets_measured_consumers(self):
        data = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
        guides = {guide["filename"]: guide for guide in data["guides"]}

        self.assertEqual(
            guides["PYTEST_RECEPTOR_GUIDE.md"],
            {
                "filename": "PYTEST_RECEPTOR_GUIDE.md",
                "owner": "uibcdf/pytest-receptor",
                "source": "standards/PYTEST_RECEPTOR_GUIDE.md",
                "consumers": [
                    "uibcdf/smonitor",
                    "uibcdf/argdigest",
                    "uibcdf/depdigest",
                    "uibcdf/pyunitwizard",
                    "uibcdf/molsysmt",
                    "uibcdf/molsysviewer",
                    "uibcdf/gh-run-receptor",
                    "uibcdf/dockingmt",
                    "uibcdf/ackredit",
                ],
            },
        )

    def test_dockingmt_is_registered_as_incubating_scientific_component(self):
        data = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
        member = next(
            member for member in data["members"] if member["name"] == "dockingmt"
        )
        self.assertEqual(
            member,
            {
                "name": "dockingmt",
                "repository": "uibcdf/dockingmt",
                "role": "scientific-component",
                "membership": "primary",
                "maturity": "incubating",
                "development-mode": "active",
                "capabilities": ["python-package"],
                "zenodo-archival": "optional",
            },
        )
        guides = {guide["filename"]: guide for guide in data["guides"]}
        for filename in (
            "MOLSYSSUITE_GUIDE.md",
            "SMONITOR_GUIDE.md",
            "DEPDIGEST_GUIDE.md",
            "ARGDIGEST_GUIDE.md",
            "PYUNITWIZARD_GUIDE.md",
            "GH_RUN_RECEPTOR_GUIDE.md",
        ):
            self.assertIn("uibcdf/dockingmt", guides[filename]["consumers"])
        self.assertNotIn(
            "dockingmt", data["initiatives"]["stabilization"]["priority-members"]
        )
        self.assertNotIn(
            "dockingmt",
            {
                component["name"]
                for component in data["policies"]["python"]["transition"]["components"]
            },
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

    def test_public_release_version_policy_is_exact_and_prospective(self):
        data = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
        policy = data["policies"]["release-version"]

        self.assertEqual(policy["issue"], "uibcdf/molsyssuite#32")
        self.assertEqual(policy["applies-to"], ["repository"])
        self.assertEqual(
            policy["pattern"],
            r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$",
        )
        self.assertEqual(
            policy["versioningit-pattern"],
            (
                r"^(?P<version>(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
                r"\.(0|[1-9][0-9]*))$"
            ),
        )
        self.assertTrue(policy["tag-equals-version"])
        self.assertFalse(policy["public-prereleases"])
        self.assertEqual(
            {entry["repository"] for entry in policy["legacy-tags"]},
            {"uibcdf/pyunitwizard", "uibcdf/molsysmt"},
        )

    def test_zenodo_policy_and_inventory_cover_every_member(self):
        data = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
        policy = data["policies"]["zenodo-archival"]
        inventory = tomllib.loads(
            (ROOT / policy["inventory"]).read_text(encoding="utf-8")
        )
        self.assertEqual(policy["issue"], "uibcdf/molsyssuite#24")
        self.assertEqual(policy["applies-to"], ["repository"])
        self.assertEqual(
            {item["repository"] for item in inventory["components"]},
            {member["repository"] for member in data["members"]},
        )
        self.assertEqual(audit_zenodo.validate_inventory(data, inventory), [])

    def test_verified_zenodo_entry_requires_exact_public_file_evidence(self):
        entry = {
            "repository": "uibcdf/example",
            "state": "verified",
            "verified-version": "1.2.3",
            "concept-doi": "10.5281/zenodo.100",
            "version-doi": "10.5281/zenodo.101",
            "record-id": 101,
            "files": [
                {
                    "name": "uibcdf/example-1.2.3.zip",
                    "size": 42,
                    "checksum": "md5:" + "a" * 32,
                }
            ],
        }
        payload = {
            "id": 101,
            "doi": "10.5281/zenodo.101",
            "conceptdoi": "10.5281/zenodo.100",
            "status": "published",
            "metadata": {
                "version": "1.2.3",
                "access_right": "open",
                "resource_type": {"type": "software"},
                "related_identifiers": [
                    {"identifier": "https://github.com/uibcdf/example"}
                ],
            },
            "files": [
                {
                    "key": "uibcdf/example-1.2.3.zip",
                    "size": 42,
                    "checksum": "md5:" + "a" * 32,
                }
            ],
        }
        self.assertEqual(audit_zenodo.verify_record(entry, payload), [])
        payload["files"][0]["size"] = 41
        self.assertIn(
            "public file inventory differs from the registered evidence",
            audit_zenodo.verify_record(entry, payload),
        )

    def test_zenodo_code_repository_metadata_proves_repository_identity(self):
        entry = {
            "repository": "uibcdf/example",
            "state": "verified",
            "verified-version": "1.2.3",
            "concept-doi": "10.5281/zenodo.100",
            "version-doi": "10.5281/zenodo.101",
            "record-id": 101,
            "files": [
                {
                    "name": "uibcdf/example-1.2.3.zip",
                    "size": 42,
                    "checksum": "md5:" + "a" * 32,
                }
            ],
        }
        payload = {
            "id": 101,
            "doi": "10.5281/zenodo.101",
            "conceptdoi": "10.5281/zenodo.100",
            "status": "published",
            "metadata": {
                "version": "1.2.3",
                "access_right": "open",
                "resource_type": {"type": "software"},
                "related_identifiers": [
                    {"identifier": "https://github.com/uibcdf/example/tree/1.2.3"}
                ],
                "custom": {"code:codeRepository": "https://github.com/uibcdf/example"},
            },
            "files": [
                {
                    "key": "uibcdf/example-1.2.3.zip",
                    "size": 42,
                    "checksum": "md5:" + "a" * 32,
                }
            ],
        }

        self.assertEqual(audit_zenodo.verify_record(entry, payload), [])

    def test_zenodo_audit_workflow_is_public_and_bounded(self):
        workflow = (ROOT / ".github/workflows/audit-zenodo.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("schedule:", workflow)
        self.assertIn("audit_zenodo.py --public", workflow)
        self.assertNotIn("secrets.", workflow)
        self.assertNotIn("Authorization", workflow)

    def test_malformed_public_zenodo_evidence_is_invalid_not_unavailable(self):
        inventory = {
            "components": [
                {
                    "repository": "uibcdf/example",
                    "state": "verified",
                    "record-id": 101,
                }
            ]
        }
        error_output = io.StringIO()
        with (
            mock.patch.object(
                audit_zenodo,
                "_fetch_record",
                side_effect=audit_zenodo.PublicEvidenceInvalid(
                    "public response is not a JSON object"
                ),
            ),
            mock.patch("sys.stderr", error_output),
        ):
            outcome = audit_zenodo.audit_public(inventory)

        self.assertEqual(outcome, 1)
        self.assertIn("INVALID uibcdf/example", error_output.getvalue())

    def test_public_audit_preserves_nonverified_evidence_state(self):
        output = io.StringIO()
        with redirect_stdout(output):
            outcome = audit_zenodo.audit_public(
                {
                    "components": [
                        {"repository": "uibcdf/absent", "state": "absent"},
                        {"repository": "uibcdf/unknown", "state": "unknown"},
                    ]
                }
            )

        self.assertEqual(outcome, 0)
        self.assertIn("ABSENT uibcdf/absent", output.getvalue())
        self.assertIn("UNKNOWN uibcdf/unknown", output.getvalue())

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

    def test_reporting_protocol_separates_guard_addressability_from_relevance(self):
        protocol = (ROOT / "devguide/reporting_protocol.md").read_text(encoding="utf-8")
        protocol = " ".join(protocol.replace("**", "").split())

        for requirement in (
            "addressability is mechanical",
            "relevance is reviewed",
            "tests/path/test_module.py::test_name",
            "does not accept globs",
            "Do not place shell commands in front matter",
            "resolved on or after 2026-09-20",
        ):
            self.assertIn(requirement, protocol)

    def test_report_dependencies_may_reference_upstream_github_issues(self):
        self.assertIsNotNone(
            devguide_reports.CROSS_REPOSITORY_ISSUE.fullmatch(
                "pytest-dev/pytest-xdist#1372"
            )
        )

    def test_python_guard_rejects_a_missing_target(self):
        with tempfile.TemporaryDirectory() as directory:
            errors = devguide_reports.validate_pytest_guard(
                Path(directory), "tests/test_missing.py"
            )

        self.assertIn("names a file that does not exist", errors[0])

    def test_python_guard_rejects_a_missing_node_in_an_existing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            test_file = root / "tests/test_example.py"
            test_file.parent.mkdir()
            test_file.write_text("def test_present():\n    pass\n", encoding="utf-8")

            errors = devguide_reports.validate_pytest_guard(
                root, "tests/test_example.py::test_absent"
            )

        self.assertIn("does not resolve to a collected test", errors[0])

    def test_python_guard_rejects_unsupported_selector_syntax(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            test_file = root / "tests/test_example.py"
            test_file.parent.mkdir()
            test_file.write_text("def test_present():\n    pass\n", encoding="utf-8")

            errors = devguide_reports.validate_pytest_guard(
                root, "tests/test_example.py::test_present[param]"
            )

        self.assertIn("parameterized selectors are not supported", errors[0])

    def test_python_guard_accepts_file_function_and_class_method_targets(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            test_file = root / "tests/test_example.py"
            test_file.parent.mkdir()
            test_file.write_text(
                "def test_function():\n"
                "    pass\n\n"
                "class TestGroup:\n"
                "    def test_method(self):\n"
                "        pass\n",
                encoding="utf-8",
            )

            selectors = (
                "tests/test_example.py",
                "tests/test_example.py::test_function",
                "tests/test_example.py::TestGroup::test_method",
            )
            errors = [
                error
                for selector in selectors
                for error in devguide_reports.validate_pytest_guard(root, selector)
            ]

        self.assertEqual(errors, [])

    def test_an_addressable_but_unrelated_guard_remains_a_review_question(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            test_file = root / "tests/test_example.py"
            test_file.parent.mkdir()
            test_file.write_text(
                "def test_unrelated_behavior():\n    pass\n", encoding="utf-8"
            )

            errors = devguide_reports.validate_pytest_guard(
                root, "tests/test_example.py::test_unrelated_behavior"
            )

        self.assertEqual(errors, [])

    def test_a_resolved_report_without_guard_or_normative_is_rejected(self):
        report = devguide_reports.Report(
            path=ROOT / "devguide/archive/example.md",
            fields={
                "summary": "Example defect.",
                "issue": "uibcdf/molsyssuite#999",
                "status": "resolved",
                "opened": "2026-09-20",
                "closed": "2026-09-20",
                "severity": "medium",
                "verification": "reproduced",
                "area": ["governance"],
                "guard": "",
                "normative": "",
                "blocked_by": [],
                "supersedes": [],
            },
            kind="bug",
            archived=True,
        )

        errors = devguide_reports.validate_report(report)

        self.assertIn(
            "devguide/archive/example.md: resolved requires guard or normative", errors
        )

    def test_historical_guard_syntax_is_not_retroactively_invalidated(self):
        report = devguide_reports.Report(
            path=ROOT / "devguide/archive/example.md",
            fields={
                "summary": "Historical defect.",
                "issue": "uibcdf/molsyssuite#999",
                "status": "resolved",
                "opened": "2026-09-01",
                "closed": "2026-09-19",
                "severity": "medium",
                "verification": "reproduced",
                "area": ["governance"],
                "guard": "legacy runner syntax",
                "normative": "",
                "blocked_by": [],
                "supersedes": [],
            },
            kind="bug",
            archived=True,
        )

        self.assertEqual(devguide_reports.validate_report(report), [])

    def test_cross_component_feedback_is_a_universal_policy(self):
        data = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
        policy = data["policies"]["cross-component-feedback"]
        self.assertEqual(policy["applies-to"], ["repository"])
        self.assertEqual(policy["issue"], "uibcdf/molsyssuite#15")
        self.assertEqual(policy["provider-report-required"], True)
        self.assertEqual(policy["consumer-cross-link-required"], True)
        self.assertEqual(policy["workaround-tracking-required"], True)

    def test_cross_component_issue_labels_are_registered(self):
        data = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
        policy = data["policies"]["cross-component-issue-labels"]
        self.assertEqual(policy["issue"], "uibcdf/molsyssuite#38")
        self.assertEqual(policy["prefix"], "component:")
        self.assertEqual(policy["color"], "1d76db")
        self.assertEqual(policy["creation"], "on-demand")
        self.assertEqual(
            policy["inventory"], "devtools/scripts/component_issue_labels.py"
        )
        self.assertEqual(policy["normative"], "devguide/reporting_protocol.md")

    def test_component_guide_is_a_universal_policy(self):
        data = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
        policy = data["policies"]["component-guide"]
        self.assertEqual(policy["applies-to"], ["repository"])
        self.assertEqual(policy["filename"], "MOLSYSSUITE_GUIDE.md")
        self.assertEqual(policy["agents-reference-required"], True)
        guide = (ROOT / policy["normative"]).read_text(encoding="utf-8")
        for section in (
            "Where suite governance lives",
            "Cross-repository working state",
            "Reporting bugs and proposals",
            "Shared stewardship across components",
            "Common development baseline",
        ):
            self.assertIn(section, guide)

    def test_new_python_components_have_a_registered_starter_policy(self):
        data = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
        policy = data["policies"]["component-starter-kit"]
        self.assertEqual(policy["issue"], "uibcdf/molsyssuite#17")
        self.assertEqual(policy["applies-to"], ["capability:python-package"])
        self.assertEqual(policy["adoption"], "new-repositories")

    def test_governance_registers_the_suite_status_command(self):
        data = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
        self.assertEqual(
            data["governance"]["workspace-status"],
            "devtools/scripts/suite_status.py",
        )

    def test_python_transition_is_explicit_and_issue_backed(self):
        data = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
        transition = data["policies"]["python"]["transition"]
        self.assertEqual(transition["issue"], "uibcdf/molsyssuite#29")
        self.assertEqual(transition["target-requires-python"], ">=3.11,<3.15")
        self.assertEqual(
            transition["target-ci-versions"], ["3.11", "3.12", "3.13", "3.14"]
        )
        self.assertEqual(
            transition["components"],
            [
                {
                    "name": "pytest-receptor",
                    "issue": "uibcdf/pytest-receptor#3",
                    "state": "admitted",
                },
                {
                    "name": "gh-run-receptor",
                    "issue": "uibcdf/gh-run-receptor#49",
                    "state": "admitted",
                },
                {
                    "name": "smonitor",
                    "issue": "uibcdf/smonitor#17",
                    "state": "admitted",
                },
                {
                    "name": "depdigest",
                    "issue": "uibcdf/depdigest#14",
                    "state": "admitted",
                },
                {
                    "name": "argdigest",
                    "issue": "uibcdf/argdigest#13",
                    "state": "admitted",
                },
                {
                    "name": "pyunitwizard",
                    "issue": "uibcdf/pyunitwizard#78",
                    "state": "admitted",
                },
            ],
        )

    def test_repository_badge_policy_is_registered_for_every_member(self):
        data = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
        policy = data["policies"]["repository-badges"]

        self.assertEqual(policy["issue"], "uibcdf/molsyssuite#23")
        self.assertEqual(policy["applies-to"], ["repository"])
        self.assertEqual(policy["normative"], "devguide/repository_badges.md")
        self.assertEqual(policy["validator"], "devtools/scripts/repository_badges.py")
        self.assertEqual(policy["adoption"], "enforced")

    def test_vendored_guides_have_a_registered_policy(self):
        data = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
        policy = data["policies"]["vendored-guides"]
        self.assertEqual(policy["issue"], "uibcdf/molsyssuite#12")
        self.assertEqual(policy["applies-to"], ["capability:python-package"])
        self.assertEqual(policy["format-owner"], "canonical-repository")
        self.assertEqual(policy["copy-mode"], "byte-identical")
        self.assertEqual(policy["ruff-exclusion"], "explicit-root-path")
        self.assertEqual(
            policy["synchronizer"],
            "devtools/scripts/sync_vendored_guides.py",
        )
        self.assertEqual(
            {guide["filename"] for guide in data["guides"]},
            {
                "ARGDIGEST_GUIDE.md",
                "ACKREDIT_GUIDE.md",
                "DEPDIGEST_GUIDE.md",
                "GH_RUN_RECEPTOR_GUIDE.md",
                "MOLSYSSUITE_GUIDE.md",
                "PYTEST_RECEPTOR_GUIDE.md",
                "PYUNITWIZARD_GUIDE.md",
                "SMONITOR_GUIDE.md",
            },
        )
        registered = {member["repository"] for member in data["members"]}
        for guide in data["guides"]:
            self.assertIn(guide["owner"], registered | {"uibcdf/molsyssuite"})
            self.assertTrue(set(guide["consumers"]).issubset(registered))
            self.assertNotIn(guide["owner"], guide["consumers"])

    def test_adoption_lifecycle_has_a_normative_inventory(self):
        data = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
        policy = data["policies"]["adoption-lifecycle"]
        self.assertEqual(policy["issue"], "uibcdf/molsyssuite#34")
        self.assertEqual(policy["applies-to"], ["repository"])
        self.assertEqual(policy["normative"], "devguide/adoption_lifecycle.md")
        self.assertEqual(policy["inventory"], "devtools/scripts/adoption_status.py")
        self.assertEqual(
            policy["states"], ["current", "stale", "missing", "excepted", "unavailable"]
        )


class AdoptionStatusTests(unittest.TestCase):
    def _policy(self) -> dict[str, object]:
        return {
            "governance": {"repository": "uibcdf/molsyssuite"},
            "policies": {
                "release-version": {
                    "required-policy-release": "policy-v9.0.0",
                }
            },
            "members": [
                {
                    "name": "consumer",
                    "repository": "uibcdf/consumer",
                    "capabilities": ["python-package"],
                }
            ],
            "guides": [
                {
                    "filename": "PROVIDER_GUIDE.md",
                    "owner": "uibcdf/provider",
                    "source": "standards/PROVIDER_GUIDE.md",
                    "consumers": ["uibcdf/consumer"],
                }
            ],
        }

    def _workspace(self, root: Path) -> Path:
        workspace = root / "workspace"
        source = workspace / "provider/standards/PROVIDER_GUIDE.md"
        source.parent.mkdir(parents=True)
        source.write_text("canonical guide\n", encoding="utf-8")
        consumer = workspace / "consumer"
        (consumer / ".github/workflows").mkdir(parents=True)
        (consumer / "PROVIDER_GUIDE.md").write_bytes(source.read_bytes())
        (consumer / ".github/workflows/policy.yml").write_text(
            "uses: uibcdf/molsyssuite/.github/workflows/"
            "check-python-repository.yaml@policy-v9.0.0\n",
            encoding="utf-8",
        )
        return workspace

    def test_guide_and_policy_adoption_are_independent_records(self):
        with tempfile.TemporaryDirectory() as temporary:
            workspace = self._workspace(Path(temporary))
            records = adoption_status.inventory(workspace, policy=self._policy())
            states = {(record.kind, record.item): record.state for record in records}
            self.assertEqual(states["guide", "PROVIDER_GUIDE.md"], "current")
            self.assertEqual(states["policy", "policy-caller"], "current")

            (workspace / "consumer/PROVIDER_GUIDE.md").write_text(
                "stale guide\n", encoding="utf-8"
            )
            records = adoption_status.inventory(workspace, policy=self._policy())
            states = {(record.kind, record.item): record.state for record in records}

        self.assertEqual(states["guide", "PROVIDER_GUIDE.md"], "stale")
        self.assertEqual(states["policy", "policy-caller"], "current")

    def test_stale_policy_caller_names_the_owner_and_next_action(self):
        with tempfile.TemporaryDirectory() as temporary:
            workspace = self._workspace(Path(temporary))
            workflow = workspace / "consumer/.github/workflows/policy.yml"
            workflow.write_text(
                workflow.read_text(encoding="utf-8").replace(
                    "policy-v9.0.0", "policy-v8.0.0"
                ),
                encoding="utf-8",
            )
            records = adoption_status.inventory(workspace, policy=self._policy())
            record = next(record for record in records if record.kind == "policy")

        self.assertEqual(record.state, "stale")
        self.assertEqual(record.owner, "uibcdf/consumer")
        self.assertEqual(record.expected, "policy-v9.0.0")
        self.assertIn("policy-v9.0.0", record.next_action)

    def test_expired_or_unregistered_exceptions_are_rejected(self):
        policy = self._policy()
        policy["adoption-exceptions"] = [
            {
                "kind": "guide",
                "repository": "uibcdf/unknown",
                "item": "PROVIDER_GUIDE.md",
                "issue": "uibcdf/unknown#1",
                "reason": "Temporary test exception.",
                "expires-on": "2020-01-01",
                "removal-condition": "Adopt the canonical guide.",
            }
        ]

        errors = adoption_status.validate_exceptions(policy)

        self.assertTrue(any("unknown repository" in error for error in errors))
        self.assertTrue(any("expired" in error for error in errors))


class ComponentIssueLabelTests(unittest.TestCase):
    def _policy(self) -> dict[str, object]:
        return {
            "governance": {"repository": "uibcdf/molsyssuite"},
            "policies": {
                "cross-component-issue-labels": {
                    "prefix": "component:",
                    "color": "1d76db",
                    "description-template": (
                        "Cross-component relationship with {repository}"
                    ),
                }
            },
            "members": [
                {"name": "molsysmt", "repository": "uibcdf/molsysmt"},
                {"name": "dockingmt", "repository": "uibcdf/dockingmt"},
                {"name": "ackredit", "repository": "uibcdf/ackredit"},
            ],
        }

    def test_catalog_is_derived_from_registered_members(self):
        catalog = component_issue_labels.catalog(self._policy())

        self.assertEqual(
            catalog["dockingmt"],
            component_issue_labels.LabelSpec(
                name="component:dockingmt",
                color="1d76db",
                description="Cross-component relationship with uibcdf/dockingmt",
            ),
        )
        self.assertNotIn("molsyssuite", catalog)

    def test_analysis_distinguishes_stale_unknown_self_and_missing_labels(self):
        labels = [
            {
                "name": "component:dockingmt",
                "color": "ffffff",
                "description": "Old description",
            },
            {
                "name": "component:unknown",
                "color": "1d76db",
                "description": "Unknown component",
            },
            {
                "name": "component:molsysmt",
                "color": "1d76db",
                "description": "Self relationship",
            },
            {
                "name": "argdigest",
                "color": "c5def5",
                "description": "Area: argdigest",
            },
        ]

        findings, actions = component_issue_labels.analyze(
            "uibcdf/molsysmt",
            labels,
            self._policy(),
            required_components=["dockingmt", "ackredit"],
        )

        self.assertEqual(
            {(finding.code, finding.label) for finding in findings},
            {
                ("STALE", "component:dockingmt"),
                ("UNKNOWN", "component:unknown"),
                ("SELF", "component:molsysmt"),
                ("MISSING", "component:ackredit"),
            },
        )
        self.assertEqual(
            {(action.operation, action.spec.name) for action in actions},
            {
                ("update", "component:dockingmt"),
                ("create", "component:ackredit"),
            },
        )

    def test_unknown_requested_component_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "unknown component"):
            component_issue_labels.analyze(
                "uibcdf/molsysmt",
                [],
                self._policy(),
                required_components=["not-registered"],
            )

    def test_hosted_audit_is_scheduled_and_read_only(self):
        workflow = (
            ROOT / ".github/workflows/audit-component-issue-labels.yaml"
        ).read_text(encoding="utf-8")

        self.assertIn("schedule:", workflow)
        self.assertIn("component_issue_labels.py", workflow)
        self.assertIn("issues: read", workflow)
        self.assertNotIn("--write", workflow)


class RepositoryBadgeTests(unittest.TestCase):
    def test_every_member_has_one_accepted_display_role(self):
        data = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
        roles = {member["name"]: member["role"] for member in data["members"]}

        self.assertEqual(
            roles,
            {
                "smonitor": "support-library",
                "argdigest": "support-library",
                "depdigest": "support-library",
                "pyunitwizard": "support-library",
                "pytest-receptor": "developer-tool",
                "gh-run-receptor": "developer-tool",
                "molsysmt": "scientific-component",
                "molsysviewer": "scientific-component",
                "topomt": "scientific-component",
                "pharmacophoremt": "scientific-component",
                "elastnetmt": "scientific-component",
                "lindelint": "developer-tool",
                "ackredit": "support-library",
                "dockingmt": "scientific-component",
            },
        )
        self.assertEqual(set(roles.values()), set(repository_badges.ROLE_LABELS))

    def test_role_badges_use_canonical_static_shields_urls(self):
        repositories = {
            "scientific-component": "uibcdf/molsysmt",
            "support-library": "uibcdf/pyunitwizard",
            "developer-tool": "uibcdf/gh-run-receptor",
        }
        self.assertEqual(
            repository_badges.ROLE_COLORS,
            {
                "scientific-component": "0b7285",
                "support-library": "2563eb",
                "developer-tool": "6f42c1",
            },
        )

        data = repository_badges.load_registry()
        for role, repository in repositories.items():
            label = repository_badges.ROLE_LABELS[role].replace(" ", "%20")
            snippet = repository_badges.render_snippet(data, repository)
            self.assertIn(
                f"https://img.shields.io/badge/MolSysSuite-{label}-"
                f"{repository_badges.ROLE_COLORS[role]}?labelColor=24292f",
                snippet,
            )
        self.assertEqual(list((ROOT / "assets" / "badges").glob("*.svg")), [])

    def test_canonical_snippet_is_generated_from_the_registry(self):
        data = repository_badges.load_registry()
        snippet = repository_badges.render_snippet(data, "uibcdf/pyunitwizard")

        self.assertIn(
            "img.shields.io/badge/MolSysSuite-support%20library-2563eb"
            "?labelColor=24292f",
            snippet,
        )
        self.assertIn(
            "uibcdf/pyunitwizard/actions/workflows/molsyssuite-policy.yml", snippet
        )
        self.assertIn("Python-3.11%20%7C%203.12%20%7C%203.13%20%7C%203.14", snippet)
        self.assertIn("img.shields.io/github/license/uibcdf/pyunitwizard", snippet)

    def test_python_badge_claims_transition_only_after_admission(self):
        data = copy.deepcopy(repository_badges.load_registry())
        transition = data["policies"]["python"]["transition"]
        pytest_receptor = next(
            component
            for component in transition["components"]
            if component["name"] == "pytest-receptor"
        )
        pytest_receptor["state"] = "admitted"

        admitted = repository_badges.render_snippet(data, "uibcdf/pytest-receptor")
        gh_run_receptor = next(
            component
            for component in transition["components"]
            if component["name"] == "gh-run-receptor"
        )
        gh_run_receptor["state"] = "authorized"
        authorized = repository_badges.render_snippet(data, "uibcdf/gh-run-receptor")

        self.assertIn("Python-3.11%20%7C%203.12%20%7C%203.13%20%7C%203.14", admitted)
        self.assertIn("Python 3.11 | 3.12 | 3.13 | 3.14", admitted)
        self.assertIn("Python-3.11%20%7C%203.12%20%7C%203.13", authorized)
        self.assertNotIn("%7C%203.14", authorized)

    def test_canonical_snippet_passes_the_offline_validator(self):
        data = repository_badges.load_registry()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text(
                "# Example\n\n"
                + repository_badges.render_snippet(data, "uibcdf/pyunitwizard"),
                encoding="utf-8",
            )
            findings = repository_badges.validate_readme(
                root, "uibcdf/pyunitwizard", data
            )

        self.assertEqual(findings, [])

    def test_missing_baseline_badges_are_independent_findings(self):
        data = repository_badges.load_registry()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("# Example\n", encoding="utf-8")
            findings = repository_badges.validate_readme(
                root, "uibcdf/pyunitwizard", data
            )

        self.assertEqual(
            {finding.code for finding in findings},
            {"IDENTITY_BADGE", "POLICY_BADGE", "PYTHON_BADGE", "LICENSE_BADGE"},
        )

    def test_badge_order_and_foreign_workflow_targets_are_rejected(self):
        data = repository_badges.load_registry()
        badges = repository_badges.canonical_badges(data, "uibcdf/pyunitwizard")
        wrong_order = [badges[1], badges[0], *badges[2:]]
        foreign = (
            "[![Foreign CI](https://github.com/uibcdf/molsysmt/actions/workflows/CI.yaml/"
            "badge.svg)](https://github.com/uibcdf/molsysmt/actions/workflows/CI.yaml)"
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text(
                "# Example\n\n"
                + "\n".join(badge.markdown for badge in wrong_order)
                + "\n"
                + foreign,
                encoding="utf-8",
            )
            findings = repository_badges.validate_readme(
                root, "uibcdf/pyunitwizard", data
            )

        self.assertEqual(
            {finding.code for finding in findings},
            {"BADGE_ORDER", "FOREIGN_WORKFLOW_BADGE"},
        )

    def test_badge_for_another_role_is_rejected(self):
        data = repository_badges.load_registry()
        snippet = repository_badges.render_snippet(data, "uibcdf/pyunitwizard")
        wrong = snippet.replace(
            "support%20library-2563eb", "scientific%20component-0b7285"
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text(wrong, encoding="utf-8")
            findings = repository_badges.validate_readme(
                root, "uibcdf/pyunitwizard", data
            )

        self.assertEqual(
            {finding.code for finding in findings},
            {"IDENTITY_BADGE", "WRONG_IDENTITY_BADGE"},
        )

    def test_badge_policy_records_truthful_capability_boundaries(self):
        policy = (ROOT / "devguide/repository_badges.md").read_text(encoding="utf-8")
        policy = " ".join(policy.split())

        for requirement in (
            "Identity is not health",
            "absence is better than an unsupported claim",
            "default branch",
            "networked audit",
            "incubating",
            "renderer, not the authority",
        ):
            self.assertIn(requirement, policy)


class StarterKitTests(unittest.TestCase):
    def test_generated_pip_lane_reports_a_new_required_suite_dependency(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "topomt"
            bootstrap_component.bootstrap(
                target, "uibcdf/topomt", "Topological molecular analysis"
            )
            pyproject = target / "pyproject.toml"
            pyproject.write_text(
                pyproject.read_text(encoding="utf-8").replace(
                    'dynamic = ["version"]',
                    'dynamic = ["version"]\ndependencies = ["smonitor>=0.16.0"]',
                ),
                encoding="utf-8",
            )

            findings = check_repository.check(target, "uibcdf/topomt")

        self.assertIn("SIBLING_CI_ROUTE", {finding.code for finding in findings})

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
            smoke_program = (
                "import sys; sys.path.insert(0, 'src'); import topomt; "
                "assert topomt.__doc__"
            )
            import_smoke = subprocess.run(
                [
                    sys.executable,
                    "-c",
                    smoke_program,
                ],
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
            pyproject = tomllib.loads(
                (target / "pyproject.toml").read_text(encoding="utf-8")
            )

        self.assertEqual(findings, [])
        self.assertEqual(index.returncode, 0, index.stdout + index.stderr)
        self.assertEqual(
            import_smoke.returncode,
            0,
            import_smoke.stdout + import_smoke.stderr,
        )
        self.assertNotIn("__COMPONENT_NAME__", texts)
        self.assertNotIn("__PACKAGE_NAME__", texts)
        self.assertNotIn("__REPOSITORY__", texts)
        self.assertIn("import topomt", texts)
        self.assertIn("version", pyproject["project"]["dynamic"])
        tag2version = pyproject["tool"]["versioningit"]["tag2version"]
        self.assertEqual(
            tag2version["regex"],
            (
                r"^(?P<version>(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
                r"\.(0|[1-9][0-9]*))$"
            ),
        )
        self.assertIs(tag2version["require-match"], True)
        self.assertNotIn("tag-filter", pyproject["tool"]["versioningit"]["vcs"])

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
    def _repository(
        self,
        root: Path,
        conforming: bool,
        repository: str = "uibcdf/pyunitwizard",
    ) -> None:
        (root / ".github/workflows").mkdir(parents=True)
        if conforming:
            pyproject = """\
[project]
name = "pyunitwizard"
version = "1.2.3"
requires-python = ">=3.11.0,<3.15.0"

[tool.ruff]
target-version = "py311"
extend-exclude = ["MOLSYSSUITE_GUIDE.md"]

[tool.ruff.lint]
select = ["E4", "E7", "E9", "F", "I"]
"""
            workflow = """\
python-version: ["3.11", "3.12", "3.13", "3.14"]
run: ruff check .
run: ruff format --check .
uses: uibcdf/molsyssuite/.github/workflows/check-python-repository.yaml@policy-v1.4.6
"""
            agents = "Suite-wide reporting belongs to uibcdf/molsyssuite.\n"
            agents += "Read MOLSYSSUITE_GUIDE.md for suite governance.\n"
        else:
            pyproject = """\
[project]
name = "pyunitwizard"
version = "v1.2.3"
requires-python = ">=3.10"

[tool.black]
line-length = 88
"""
            workflow = 'python-version: "3.10"\nrun: flake8 .\n'
            agents = "Only local instructions.\n"
        (root / "pyproject.toml").write_text(pyproject, encoding="utf-8")
        (root / ".github/workflows/tests.yaml").write_text(workflow, encoding="utf-8")
        (root / "AGENTS.md").write_text(agents, encoding="utf-8")
        (root / "README.md").write_text(
            "# PyUnitWizard\n\n"
            + repository_badges.render_snippet(
                repository_badges.load_registry(),
                repository,
            ),
            encoding="utf-8",
        )
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

    def test_required_sibling_dependency_rejects_the_pip_only_ci_lane(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._repository(root, conforming=True)
            pyproject = root / "pyproject.toml"
            pyproject.write_text(
                pyproject.read_text(encoding="utf-8").replace(
                    'version = "1.2.3"',
                    'version = "1.2.3"\ndependencies = ["SMonitor>=0.16.0"]',
                ),
                encoding="utf-8",
            )
            workflow = root / ".github/workflows/tests.yaml"
            workflow.write_text(
                workflow.read_text(encoding="utf-8")
                + "\nrun: python -m pip install -e '.[test]'\n",
                encoding="utf-8",
            )

            findings = check_repository.check(root, "uibcdf/pyunitwizard")

        self.assertEqual([finding.code for finding in findings], ["SIBLING_CI_ROUTE"])
        self.assertIn("smonitor", findings[0].message)

    def test_required_sibling_dependency_accepts_a_conda_ci_environment(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._repository(root, conforming=True)
            pyproject = root / "pyproject.toml"
            pyproject.write_text(
                pyproject.read_text(encoding="utf-8").replace(
                    'version = "1.2.3"',
                    'version = "1.2.3"\ndependencies = ["smonitor"]',
                ),
                encoding="utf-8",
            )
            environment = root / "devtools/conda-envs/test_env.yaml"
            environment.parent.mkdir(parents=True)
            environment.write_text(
                "channels:\n  - uibcdf\n  - conda-forge\n"
                "dependencies:\n  - python=3.13\n  - smonitor\n",
                encoding="utf-8",
            )
            workflow = root / ".github/workflows/tests.yaml"
            workflow.write_text(
                workflow.read_text(encoding="utf-8")
                + "\nuses: mamba-org/setup-micromamba@v3.2.1\n"
                + "environment-file: devtools/conda-envs/test_env.yaml\n",
                encoding="utf-8",
            )

            findings = check_repository.check(root, "uibcdf/pyunitwizard")

        self.assertNotIn("SIBLING_CI_ROUTE", {finding.code for finding in findings})

    def test_required_sibling_dependency_accepts_a_pinned_source_install(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._repository(root, conforming=True)
            pyproject = root / "pyproject.toml"
            pyproject.write_text(
                pyproject.read_text(encoding="utf-8").replace(
                    'version = "1.2.3"',
                    'version = "1.2.3"\ndependencies = ["smonitor"]',
                ),
                encoding="utf-8",
            )
            workflow = root / ".github/workflows/tests.yaml"
            workflow.write_text(
                workflow.read_text(encoding="utf-8")
                + "\nrun: python -m pip install "
                + "git+https://github.com/uibcdf/smonitor@"
                + "0123456789abcdef0123456789abcdef01234567\n",
                encoding="utf-8",
            )

            findings = check_repository.check(root, "uibcdf/pyunitwizard")

        self.assertNotIn("SIBLING_CI_ROUTE", {finding.code for finding in findings})

    def test_required_sibling_dependency_rejects_a_floating_source_install(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._repository(root, conforming=True)
            pyproject = root / "pyproject.toml"
            pyproject.write_text(
                pyproject.read_text(encoding="utf-8").replace(
                    'version = "1.2.3"',
                    'version = "1.2.3"\ndependencies = ["smonitor"]',
                ),
                encoding="utf-8",
            )
            workflow = root / ".github/workflows/tests.yaml"
            workflow.write_text(
                workflow.read_text(encoding="utf-8")
                + "\nrun: python -m pip install "
                + "git+https://github.com/uibcdf/smonitor@main\n",
                encoding="utf-8",
            )

            findings = check_repository.check(root, "uibcdf/pyunitwizard")

        self.assertIn("SIBLING_CI_ROUTE", {finding.code for finding in findings})

    def test_required_sibling_dependency_rejects_an_unexecuted_source_reference(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._repository(root, conforming=True)
            pyproject = root / "pyproject.toml"
            pyproject.write_text(
                pyproject.read_text(encoding="utf-8").replace(
                    'version = "1.2.3"',
                    'version = "1.2.3"\ndependencies = ["smonitor"]',
                ),
                encoding="utf-8",
            )
            workflow = root / ".github/workflows/tests.yaml"
            workflow.write_text(
                workflow.read_text(encoding="utf-8")
                + "\n# git+https://github.com/uibcdf/smonitor@"
                + "0123456789abcdef0123456789abcdef01234567\n",
                encoding="utf-8",
            )

            findings = check_repository.check(root, "uibcdf/pyunitwizard")

        self.assertIn("SIBLING_CI_ROUTE", {finding.code for finding in findings})

    def test_import_smoke_step_cannot_hide_failure_behind_trailing_logging(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._repository(root, conforming=True)
            workflow = root / ".github/workflows/tests.yaml"
            workflow.write_text(
                workflow.read_text(encoding="utf-8")
                + """

jobs:
  smoke:
    steps:
      - name: Test import module
        shell: bash -l {0}
        run: |
          echo "::group::Importing module from home directory"
          cd
          python -c 'raise RuntimeError("broken import")'
          echo "::endgroup::"
""",
                encoding="utf-8",
            )

            findings = check_repository.check(root, "uibcdf/pyunitwizard")

        self.assertIn("WORKFLOW_FAIL_FAST", {finding.code for finding in findings})

    def test_fail_fast_import_smoke_step_is_accepted(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._repository(root, conforming=True)
            workflow = root / ".github/workflows/tests.yaml"
            workflow.write_text(
                workflow.read_text(encoding="utf-8")
                + """

jobs:
  smoke:
    steps:
      - name: Test import module (installed wheel)
        shell: bash -l {0}
        run: |
          set -euo pipefail
          echo "::group::Importing module from home directory"
          trap 'echo "::endgroup::"' EXIT
          cd
          python -c 'import pyunitwizard'
""",
                encoding="utf-8",
            )

            findings = check_repository.check(root, "uibcdf/pyunitwizard")

        self.assertNotIn("WORKFLOW_FAIL_FAST", {finding.code for finding in findings})

    def test_fail_fast_guard_does_not_claim_to_parse_unrelated_shell_steps(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._repository(root, conforming=True)
            workflow = root / ".github/workflows/tests.yaml"
            workflow.write_text(
                workflow.read_text(encoding="utf-8")
                + """

jobs:
  docs:
    steps:
      - name: Build documentation
        run: |
          python -m sphinx docs build
          echo "documentation complete"
""",
                encoding="utf-8",
            )

            findings = check_repository.check(root, "uibcdf/pyunitwizard")

        self.assertNotIn("WORKFLOW_FAIL_FAST", {finding.code for finding in findings})

    def test_common_gate_enforces_the_repository_badge_baseline(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._repository(root, conforming=True)
            (root / "README.md").write_text("# PyUnitWizard\n", encoding="utf-8")
            findings = check_repository.check(root, "uibcdf/pyunitwizard")

        self.assertEqual(
            {finding.code for finding in findings},
            {"IDENTITY_BADGE", "POLICY_BADGE", "PYTHON_BADGE", "LICENSE_BADGE"},
        )

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
                "RELEASE_VERSION",
                "RELEASE_POLICY_GATE",
            },
        )

    def test_public_release_versions_reject_prefixes_and_suffixes(self):
        for version in ("v1.2.3", "1.2.3rc1", "1.2.3.dev1", "1.2.3+local"):
            with (
                self.subTest(version=version),
                tempfile.TemporaryDirectory() as temporary,
            ):
                root = Path(temporary)
                self._repository(root, conforming=True)
                pyproject = root / "pyproject.toml"
                pyproject.write_text(
                    pyproject.read_text(encoding="utf-8").replace(
                        'version = "1.2.3"', f'version = "{version}"'
                    ),
                    encoding="utf-8",
                )

                findings = check_repository.check(root, "uibcdf/pyunitwizard")

            self.assertIn("RELEASE_VERSION", {finding.code for finding in findings})

    def test_dynamic_versions_require_the_effective_exact_release_tag_parser(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._repository(root, conforming=True)
            pyproject = root / "pyproject.toml"
            pyproject.write_text(
                pyproject.read_text(encoding="utf-8").replace(
                    'version = "1.2.3"', 'dynamic = ["version"]'
                )
                + """

[tool.versioningit.tag2version]
regex = '^(?P<version>[0-9]+\\.[0-9]+\\.[0-9]+)'
require-match = false
""",
                encoding="utf-8",
            )

            findings = check_repository.check(root, "uibcdf/pyunitwizard")

        self.assertIn("RELEASE_TAG_FILTER", {finding.code for finding in findings})

    def test_prerelease_event_triggers_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._repository(root, conforming=True)
            workflow = root / ".github/workflows/release.yml"
            workflow.write_text(
                "on:\n  release:\n    types: [released, prereleased]\n",
                encoding="utf-8",
            )

            findings = check_repository.check(root, "uibcdf/pyunitwizard")

        self.assertIn("PUBLIC_PRERELEASE", {finding.code for finding in findings})

    def test_unregistered_noncanonical_git_tags_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._repository(root, conforming=True)
            commands = (
                ["git", "init", "-q"],
                ["git", "add", "."],
                [
                    "git",
                    "-c",
                    "user.name=MolSysSuite test",
                    "-c",
                    "user.email=test@example.invalid",
                    "commit",
                    "-qm",
                    "fixture",
                ],
                ["git", "tag", "v1.2.3"],
            )
            for command in commands:
                subprocess.run(command, cwd=root, check=True)

            findings = check_repository.check(root, "uibcdf/pyunitwizard")

        self.assertIn("RELEASE_TAG", {finding.code for finding in findings})

    def test_registered_historical_git_tag_remains_accepted(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._repository(root, conforming=True)
            commands = (
                ["git", "init", "-q"],
                ["git", "add", "."],
                [
                    "git",
                    "-c",
                    "user.name=MolSysSuite test",
                    "-c",
                    "user.email=test@example.invalid",
                    "commit",
                    "-qm",
                    "fixture",
                ],
                ["git", "tag", "0.3.1b"],
            )
            for command in commands:
                subprocess.run(command, cwd=root, check=True)

            findings = check_repository.check(root, "uibcdf/pyunitwizard")

        self.assertNotIn("RELEASE_TAG", {finding.code for finding in findings})

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

    def test_versioned_policy_can_delegate_guide_bytes_to_live_sync_guard(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._repository(root, conforming=True)
            guide = root / "MOLSYSSUITE_GUIDE.md"
            guide.write_text(guide.read_text(encoding="utf-8") + "\nnew guide text\n")
            findings = check_repository.check(
                root, "uibcdf/pyunitwizard", check_guide_content=False
            )
        self.assertEqual(findings, [])

    def test_versioned_policy_still_requires_a_component_guide(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._repository(root, conforming=True)
            (root / "MOLSYSSUITE_GUIDE.md").unlink()
            findings = check_repository.check(
                root, "uibcdf/pyunitwizard", check_guide_content=False
            )
        self.assertEqual([finding.code for finding in findings], ["GUIDE_MISSING"])

    def test_ruff_configuration_without_active_ci_gates_is_not_conforming(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._repository(root, conforming=True)
            workflow = root / ".github/workflows/tests.yaml"
            workflow.write_text(
                'python-version: ["3.11", "3.12", "3.13", "3.14"]\n',
                encoding="utf-8",
            )
            findings = check_repository.check(root, "uibcdf/pyunitwizard")
        self.assertEqual(
            [finding.code for finding in findings],
            ["RELEASE_POLICY_GATE", "RUFF_CI"],
        )

    def test_exact_shared_policy_release_counts_as_the_active_ruff_gate(self):
        release = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))[
            "governance"
        ]["policy-release"]
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._repository(root, conforming=True)
            workflow = root / ".github/workflows/tests.yaml"
            workflow.write_text(
                'python-version: ["3.11", "3.12", "3.13", "3.14"]\n'
                "uses: uibcdf/molsyssuite/.github/workflows/"
                f"check-python-repository.yaml@{release}\n",
                encoding="utf-8",
            )
            findings = check_repository.check(root, "uibcdf/pyunitwizard")
        self.assertEqual(findings, [])

    def test_previous_compatible_gate_does_not_satisfy_release_policy(self):
        compatible = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))[
            "governance"
        ]["compatible-policy-releases"][0]
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._repository(root, conforming=True)
            workflow = root / ".github/workflows/tests.yaml"
            workflow.write_text(
                'python-version: ["3.11", "3.12", "3.13", "3.14"]\n'
                "uses: uibcdf/molsyssuite/.github/workflows/"
                f"check-python-repository.yaml@{compatible}\n",
                encoding="utf-8",
            )
            findings = check_repository.check(root, "uibcdf/pyunitwizard")
        self.assertEqual(
            [finding.code for finding in findings],
            ["RELEASE_POLICY_GATE", "RUFF_CI"],
        )

    def test_authorized_transition_member_requires_target_contract_and_gate(self):
        policy = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
        current = policy["governance"]["policy-release"]
        compatible = policy["governance"]["compatible-policy-releases"][0]
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._repository(
                root,
                conforming=True,
                repository="uibcdf/pytest-receptor",
            )
            workflow = root / ".github/workflows/tests.yaml"
            workflow.write_text(
                'python-version: ["3.11", "3.12", "3.13", "3.14"]\n'
                "uses: uibcdf/molsyssuite/.github/workflows/"
                f"check-python-repository.yaml@{compatible}\n",
                encoding="utf-8",
            )
            findings = check_repository.check(root, "uibcdf/pytest-receptor")
            self.assertEqual(
                [finding.code for finding in findings],
                ["RELEASE_POLICY_GATE", "RUFF_CI"],
            )

            workflow.write_text(
                workflow.read_text(encoding="utf-8").replace(compatible, current),
                encoding="utf-8",
            )
            findings = check_repository.check(root, "uibcdf/pytest-receptor")
        self.assertEqual(findings, [])

    def test_old_shared_policy_release_does_not_claim_the_new_ruff_gate(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._repository(root, conforming=True)
            workflow = root / ".github/workflows/tests.yaml"
            workflow.write_text(
                'python-version: ["3.11", "3.12", "3.13", "3.14"]\n'
                "uses: uibcdf/molsyssuite/.github/workflows/"
                "check-python-repository.yaml@policy-v1.1.0\n",
                encoding="utf-8",
            )
            findings = check_repository.check(root, "uibcdf/pyunitwizard")
        self.assertEqual(
            [finding.code for finding in findings],
            ["RELEASE_POLICY_GATE", "RUFF_CI"],
        )

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

    def test_each_present_vendored_guide_requires_an_explicit_ruff_exclusion(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._repository(root, conforming=True)
            pyproject = root / "pyproject.toml"
            pyproject.write_text(
                pyproject.read_text(encoding="utf-8").replace(
                    'extend-exclude = ["MOLSYSSUITE_GUIDE.md"]\n', ""
                ),
                encoding="utf-8",
            )
            findings = check_repository.check(root, "uibcdf/pyunitwizard")
        self.assertEqual(
            [finding.code for finding in findings], ["VENDORED_GUIDE_RUFF"]
        )

    def test_canonical_guide_owned_by_the_repository_is_not_excluded(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._repository(root, conforming=True)
            (root / "standards").mkdir()
            (root / "standards/PYUNITWIZARD_GUIDE.md").write_text(
                "# Repository-owned canonical guide\n", encoding="utf-8"
            )
            findings = check_repository.check(root, "uibcdf/pyunitwizard")
        self.assertEqual(findings, [])

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
        self.assertIn("--skip-guide-content", workflow)

    def test_component_guide_sync_is_independent_of_python_conformance(self):
        workflow = (ROOT / ".github/workflows/check-component-guides.yaml").read_text(
            encoding="utf-8"
        )
        self.assertIn("check_component_guide.py", workflow)
        self.assertIn('m["repository"] for m in data["members"]', workflow)
        self.assertNotIn("check_repository.py component", workflow)
        self.assertIn("schedule:", workflow)

    def test_vendored_guide_workflow_runs_the_cross_repository_guard(self):
        workflow = (ROOT / ".github/workflows/check-vendored-guides.yaml").read_text(
            encoding="utf-8"
        )
        self.assertIn("check_vendored_guides.py", workflow)
        self.assertIn("--list-repositories", workflow)
        self.assertIn("adoption_status.py", workflow)
        self.assertIn("if: always()", workflow)
        self.assertIn("schedule:", workflow)


class VendoredGuideSynchronizationTests(unittest.TestCase):
    def _workspace(self, root: Path) -> Path:
        workspace = root / "workspace"
        source = workspace / "smonitor/standards/SMONITOR_GUIDE.md"
        source.parent.mkdir(parents=True)
        source.write_text(
            "<!--\n"
            "SYNCHRONIZED MOLSYSSUITE GUIDE — DO NOT EDIT COMPONENT COPIES.\n"
            "Canonical source: https://github.com/uibcdf/smonitor/blob/main/"
            "standards/SMONITOR_GUIDE.md\n"
            "-->\n\n# SMonitor guide\n",
            encoding="utf-8",
        )
        consumer = workspace / "pyunitwizard"
        consumer.mkdir(parents=True)
        (consumer / "SMONITOR_GUIDE.md").write_bytes(source.read_bytes())
        return workspace

    def test_byte_identical_copy_passes(self):
        with tempfile.TemporaryDirectory() as temporary:
            workspace = self._workspace(Path(temporary))
            findings = check_vendored_guides.check_one(
                workspace,
                owner="uibcdf/smonitor",
                source_path="standards/SMONITOR_GUIDE.md",
                consumer="uibcdf/pyunitwizard",
                filename="SMONITOR_GUIDE.md",
            )
        self.assertEqual(findings, [])

    def test_modified_copy_is_reported_as_drift(self):
        with tempfile.TemporaryDirectory() as temporary:
            workspace = self._workspace(Path(temporary))
            copy = workspace / "pyunitwizard/SMONITOR_GUIDE.md"
            copy.write_text(copy.read_text(encoding="utf-8") + "local edit\n")
            findings = check_vendored_guides.check_one(
                workspace,
                owner="uibcdf/smonitor",
                source_path="standards/SMONITOR_GUIDE.md",
                consumer="uibcdf/pyunitwizard",
                filename="SMONITOR_GUIDE.md",
            )
        self.assertEqual([finding.code for finding in findings], ["GUIDE_DRIFT"])

    def test_missing_declared_copy_is_reported(self):
        with tempfile.TemporaryDirectory() as temporary:
            workspace = self._workspace(Path(temporary))
            (workspace / "pyunitwizard/SMONITOR_GUIDE.md").unlink()
            findings = check_vendored_guides.check_one(
                workspace,
                owner="uibcdf/smonitor",
                source_path="standards/SMONITOR_GUIDE.md",
                consumer="uibcdf/pyunitwizard",
                filename="SMONITOR_GUIDE.md",
            )
        self.assertEqual([finding.code for finding in findings], ["GUIDE_MISSING"])

    def test_missing_read_only_marker_is_reported(self):
        with tempfile.TemporaryDirectory() as temporary:
            workspace = self._workspace(Path(temporary))
            source = workspace / "smonitor/standards/SMONITOR_GUIDE.md"
            source.write_text("# SMonitor guide\n", encoding="utf-8")
            (workspace / "pyunitwizard/SMONITOR_GUIDE.md").write_bytes(
                source.read_bytes()
            )
            findings = check_vendored_guides.check_one(
                workspace,
                owner="uibcdf/smonitor",
                source_path="standards/SMONITOR_GUIDE.md",
                consumer="uibcdf/pyunitwizard",
                filename="SMONITOR_GUIDE.md",
            )
        self.assertEqual([finding.code for finding in findings], ["GUIDE_MARKER"])

    def test_registered_guide_can_be_synchronized_byte_identically(self):
        with tempfile.TemporaryDirectory() as temporary:
            workspace = self._workspace(Path(temporary))
            target = workspace / "pyunitwizard/SMONITOR_GUIDE.md"
            target.write_text("local drift\n", encoding="utf-8")
            relation = sync_vendored_guides.Relationship(
                owner="uibcdf/smonitor",
                source_path="standards/SMONITOR_GUIDE.md",
                consumer="uibcdf/pyunitwizard",
                filename="SMONITOR_GUIDE.md",
            )

            errors = sync_vendored_guides.process(workspace, [relation], write=True)

            source = workspace / "smonitor/standards/SMONITOR_GUIDE.md"
            self.assertEqual(errors, [])
            self.assertEqual(target.read_bytes(), source.read_bytes())

    def test_sync_check_does_not_modify_a_drifted_copy(self):
        with tempfile.TemporaryDirectory() as temporary:
            workspace = self._workspace(Path(temporary))
            target = workspace / "pyunitwizard/SMONITOR_GUIDE.md"
            target.write_text("local drift\n", encoding="utf-8")
            relation = sync_vendored_guides.Relationship(
                owner="uibcdf/smonitor",
                source_path="standards/SMONITOR_GUIDE.md",
                consumer="uibcdf/pyunitwizard",
                filename="SMONITOR_GUIDE.md",
            )

            errors = sync_vendored_guides.process(workspace, [relation], write=False)

            self.assertEqual(len(errors), 1)
            self.assertIn("missing or different", errors[0])
            self.assertEqual(target.read_text(encoding="utf-8"), "local drift\n")

    def test_sync_preflight_prevents_partial_writes(self):
        with tempfile.TemporaryDirectory() as temporary:
            workspace = self._workspace(Path(temporary))
            target = workspace / "pyunitwizard/SMONITOR_GUIDE.md"
            target.write_text("local drift\n", encoding="utf-8")
            valid = sync_vendored_guides.Relationship(
                owner="uibcdf/smonitor",
                source_path="standards/SMONITOR_GUIDE.md",
                consumer="uibcdf/pyunitwizard",
                filename="SMONITOR_GUIDE.md",
            )
            invalid = sync_vendored_guides.Relationship(
                owner="uibcdf/depdigest",
                source_path="standards/DEPDIGEST_GUIDE.md",
                consumer="uibcdf/pyunitwizard",
                filename="DEPDIGEST_GUIDE.md",
            )

            errors = sync_vendored_guides.process(
                workspace, [valid, invalid], write=True
            )

            self.assertEqual(len(errors), 1)
            self.assertIn("canonical guide is missing", errors[0])
            self.assertEqual(target.read_text(encoding="utf-8"), "local drift\n")

    def test_registry_filters_reject_unknown_selectors(self):
        with self.assertRaisesRegex(ValueError, "unknown guide"):
            sync_vendored_guides.relationships(guides=["UNKNOWN_GUIDE.md"])
        with self.assertRaisesRegex(ValueError, "unknown repository"):
            sync_vendored_guides.relationships(repositories=["uibcdf/unknown"])

    def test_write_guard_rejects_a_stale_canonical_checkout(self):
        with tempfile.TemporaryDirectory() as temporary:
            workspace = self._workspace(Path(temporary))
            relation = sync_vendored_guides.Relationship(
                owner="uibcdf/smonitor",
                source_path="standards/SMONITOR_GUIDE.md",
                consumer="uibcdf/pyunitwizard",
                filename="SMONITOR_GUIDE.md",
            )
            outputs = ["", "local-head", "remote-head\trefs/heads/main"]
            with mock.patch.object(
                sync_vendored_guides, "_git_output", side_effect=outputs
            ):
                errors = sync_vendored_guides.verify_sources(workspace, [relation])

        self.assertEqual(len(errors), 1)
        self.assertIn("does not match remote main", errors[0])

    def test_write_guard_rejects_an_uncommitted_canonical_guide(self):
        with tempfile.TemporaryDirectory() as temporary:
            workspace = self._workspace(Path(temporary))
            relation = sync_vendored_guides.Relationship(
                owner="uibcdf/smonitor",
                source_path="standards/SMONITOR_GUIDE.md",
                consumer="uibcdf/pyunitwizard",
                filename="SMONITOR_GUIDE.md",
            )
            with mock.patch.object(
                sync_vendored_guides,
                "_git_output",
                return_value=" M standards/SMONITOR_GUIDE.md",
            ):
                errors = sync_vendored_guides.verify_sources(workspace, [relation])

        self.assertEqual(len(errors), 1)
        self.assertIn("uncommitted canonical guide changes", errors[0])

    def test_write_guard_does_not_overwrite_a_local_consumer_edit(self):
        with tempfile.TemporaryDirectory() as temporary:
            workspace = self._workspace(Path(temporary))
            target = workspace / "pyunitwizard/SMONITOR_GUIDE.md"
            target.write_text("local edit\n", encoding="utf-8")
            relation = sync_vendored_guides.Relationship(
                owner="uibcdf/smonitor",
                source_path="standards/SMONITOR_GUIDE.md",
                consumer="uibcdf/pyunitwizard",
                filename="SMONITOR_GUIDE.md",
            )
            with mock.patch.object(
                sync_vendored_guides,
                "_git_output",
                return_value=" M SMONITOR_GUIDE.md",
            ):
                errors = sync_vendored_guides.verify_destinations(workspace, [relation])
            content = target.read_text(encoding="utf-8")

        self.assertEqual(len(errors), 1)
        self.assertIn("locally modified consumer guide", errors[0])
        self.assertEqual(content, "local edit\n")


class SuiteStatusTests(unittest.TestCase):
    def test_clean_current_repository_is_healthy(self):
        outputs = ["", "", "origin/main", "0 0", "main", "abc123"]
        with (
            tempfile.TemporaryDirectory() as temporary,
            mock.patch.object(suite_status, "_git_output", side_effect=outputs),
        ):
            status = suite_status.inspect_repository(
                Path(temporary),
                repository="uibcdf/example",
                initiative="stabilization",
                fetch=True,
            )

        self.assertTrue(status.healthy)
        self.assertEqual(status.ahead, 0)
        self.assertEqual(status.behind, 0)
        self.assertEqual(status.worktree, ())

    def test_dirty_diverged_repository_requires_attention(self):
        outputs = [
            " M tracked.py\n?? untracked.txt",
            "origin/main",
            "2 3",
            "main",
            "abc123",
        ]
        with (
            tempfile.TemporaryDirectory() as temporary,
            mock.patch.object(suite_status, "_git_output", side_effect=outputs),
        ):
            status = suite_status.inspect_repository(
                Path(temporary),
                repository="uibcdf/example",
                initiative="stabilization",
                fetch=False,
            )

        self.assertFalse(status.healthy)
        self.assertEqual(status.ahead, 2)
        self.assertEqual(status.behind, 3)
        self.assertEqual(status.worktree, ("M tracked.py", "?? untracked.txt"))
        self.assertEqual(status.state, "attention")

    def test_fetch_failure_is_reported_without_inspecting_stale_refs(self):
        with (
            tempfile.TemporaryDirectory() as temporary,
            mock.patch.object(
                suite_status,
                "_git_output",
                side_effect=RuntimeError("fetch failed"),
            ) as git_output,
        ):
            status = suite_status.inspect_repository(
                Path(temporary),
                repository="uibcdf/example",
                initiative="stabilization",
                fetch=True,
            )

        self.assertFalse(status.healthy)
        self.assertEqual(status.error, "fetch failed")
        git_output.assert_called_once()

    def test_missing_repository_is_reported_without_running_git(self):
        with tempfile.TemporaryDirectory() as temporary:
            missing = Path(temporary) / "missing"
            with mock.patch.object(suite_status, "_git_output") as git_output:
                status = suite_status.inspect_repository(
                    missing,
                    repository="uibcdf/missing",
                    initiative="",
                    fetch=True,
                )

        self.assertEqual(status.state, "error")
        self.assertIn("missing", status.error)
        git_output.assert_not_called()

    def test_registry_targets_prioritizes_the_stabilization_initiative(self):
        targets = suite_status.registered_targets()
        names = [target.repository for target in targets]
        self.assertEqual(
            names[:6],
            [
                "uibcdf/smonitor",
                "uibcdf/argdigest",
                "uibcdf/depdigest",
                "uibcdf/pyunitwizard",
                "uibcdf/molsysmt",
                "uibcdf/molsysviewer",
            ],
        )
        self.assertEqual(len(names), len(set(names)))

    def test_json_output_contains_machine_readable_state(self):
        status = suite_status.RepositoryStatus(
            repository="uibcdf/example",
            initiative="stabilization",
            root="/workspace/example",
            branch="main",
            head="abc123",
        )

        payload = json.loads(suite_status.render_json([status]))

        self.assertEqual(payload[0]["repository"], "uibcdf/example")
        self.assertEqual(payload[0]["state"], "current")
        self.assertEqual(payload[0]["healthy"], True)


if __name__ == "__main__":
    unittest.main()
