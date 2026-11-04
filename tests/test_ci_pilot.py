"""Adversarial coverage for informational CI profiles, never a compliance gate."""

from __future__ import annotations

import hashlib
import io
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from devtools.scripts import ci_lane_inventory, python_ci_status


class CIPilotTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.workspace = Path(temporary.name)
        self.root = self.workspace / "example"
        (self.root / ".github/workflows").mkdir(parents=True)
        (self.root / "pyproject.toml").write_text(
            '[tool.pytest.ini_options]\ntestpaths = ["tests"]\n'
        )
        self.workflow = self.root / ".github/workflows/ci.yaml"
        self.registry = {
            "members": [{"repository": "uibcdf/example", "name": "example"}],
            "python-ci-reviews": [
                {
                    "repository": "uibcdf/example",
                    "review-issue": "uibcdf/example#1",
                    "state": "partial",
                    "routine-test-level": "full",
                    "hosted-evidence": "https://github.com/uibcdf/example/actions/runs/1",
                }
            ],
        }

    def report(self, source, *, level="full", smoke_issue=None):
        self.workflow.write_text(source)
        inputs = {
            path: hashlib.sha256((self.root / path).read_bytes()).hexdigest()
            for path in ("pyproject.toml", ".github/workflows/ci.yaml")
        }
        self.profiles = {
            "schema-version": 1,
            "mode": "informational",
            "profiles": [
                {
                    "repository": "uibcdf/example",
                    "review-issue": "uibcdf/example#1",
                    "reviewed-source": "a" * 40,
                    "inputs": inputs,
                    "lanes": [
                        {
                            "workflow": "ci.yaml",
                            "job": "test",
                            "test-level": level,
                            "smoke-issue": smoke_issue,
                            "events": {
                                "push": ["3.14"],
                                "pull_request": ["3.14"],
                                "schedule": ["3.11", "3.12", "3.13", "3.14"],
                                "workflow_dispatch": ["3.14"],
                            },
                        }
                    ],
                }
            ],
        }
        return python_ci_status.inspect_pilot(
            self.registry, self.workspace, self.profiles
        )

    def source(
        self,
        *,
        version="3.14",
        command="python -m pytest tests",
        job_if="",
        test_extra="",
        event_extra="",
    ):
        return f"""on:
  push:
  pull_request:{event_extra}
  schedule:
    - cron: "17 5 * * MON"
  workflow_dispatch:
jobs:
  test:
    runs-on: ubuntu-latest
{job_if}    steps:
      - uses: actions/setup-python@v6
        with:
          python-version: "{version}"
      - run: {command}
{test_extra}"""

    def lane(self, report, event="pull_request", version="3.14"):
        return next(
            row
            for row in report["members"][0]["lanes"]
            if row["event"] == event and row["python"] == version
        )

    def test_recognized_source_never_becomes_hosted_or_backlog_evidence(self):
        report = self.report(self.source())
        self.assertEqual(self.lane(report)["state"], "configured")
        self.assertTrue(self.lane(report)["reviewed_level_matches_target"])
        member = report["members"][0]
        self.assertEqual(member["execution_evidence"], "not_requested")
        self.assertEqual(member["backlog_clearance"], "not_evaluated")
        self.assertEqual(member["existing_adoption_state"], "partial")
        self.assertNotIn("compliant", report)
        routes = member["event_routes"]
        self.assertTrue(routes)
        self.assertTrue(all(route["profile_inputs_current"] for route in routes))
        self.assertTrue(
            all(route["execution_evidence"] == "not_requested" for route in routes)
        )

    def test_comment_version_cannot_supply_required_interpreter(self):
        report = self.report("# Python 3.14 planned\n" + self.source(version="3.13"))
        self.assertEqual(self.lane(report)["state"], "not_observed")

    def test_resolved_scenario_matrix_cannot_upgrade_aggregate_or_drift_review(self):
        source = """on:
  push:
  pull_request:
  schedule:
    - cron: '0 9 * * MON'
  workflow_dispatch:
    inputs:
      single:
        type: boolean
        default: false
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python: ${{ fromJSON(inputs.single == true && '["3.13"]' || '["3.11", "3.12", "3.13", "3.14"]') }}
    steps:
      - uses: actions/setup-python@v7
        with:
          python-version: ${{ matrix.python }}
      - run: pytest tests
"""
        report = self.report(source)
        member = report["members"][0]
        self.assertTrue(all(lane["state"] == "unknown" for lane in member["lanes"]))
        single = next(
            route
            for route in member["event_routes"]
            if route["scenario"] == "workflow_dispatch:inputs.single=true"
        )
        self.assertEqual(
            single["jobs"][0]["matrix"],
            {"status": "resolved", "combinations": [{"python": "3.13"}]},
        )
        self.assertEqual(member["execution_evidence"], "not_requested")
        self.assertEqual(member["backlog_clearance"], "not_evaluated")
        self.workflow.write_text(source.replace("default: false", "default: true"))
        drift = python_ci_status.inspect_pilot(
            self.registry, self.workspace, self.profiles
        )
        self.assertTrue(
            all(
                not route["profile_inputs_current"]
                for route in drift["members"][0]["event_routes"]
            )
        )
        self.assertTrue(
            all(lane["state"] == "unknown" for lane in drift["members"][0]["lanes"])
        )

    def test_excluded_matrix_minor_does_not_count_as_weekly_cell(self):
        source = """on: [schedule]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python: ["3.11", "3.12", "3.13", "3.14"]
        exclude:
          - python: "3.12"
    steps:
      - uses: actions/setup-python@v6
        with:
          python-version: ${{ matrix.python }}
      - run: pytest tests
"""
        report = self.report(source)
        self.assertEqual(self.lane(report, "schedule", "3.12")["state"], "not_observed")
        self.assertEqual(self.lane(report, "schedule", "3.14")["state"], "configured")

    def test_skipped_and_tolerated_tests_are_not_required_lanes(self):
        skipped = self.report(self.source(job_if="    if: false\n"))
        self.assertEqual(self.lane(skipped)["state"], "not_observed")
        tolerated = self.report(
            self.source(test_extra="        continue-on-error: true\n")
        )
        self.assertEqual(self.lane(tolerated)["state"], "non_gating")

    def test_filtered_pr_and_unknown_schedule_conditions_stay_visible(self):
        filtered = self.report(self.source(event_extra='\n    paths: ["src/**"]'))
        self.assertEqual(self.lane(filtered)["state"], "conditional")
        self.assertTrue(self.lane(filtered)["observations"][0]["path_filtered"])
        conditional = self.report(
            self.source(job_if="    if: inputs.probe_backlog != true\n")
        )
        self.assertEqual(self.lane(conditional, "schedule")["state"], "conditional")
        self.assertIsNone(
            self.lane(conditional, "schedule")["observations"][0]["event_eligible"]
        )

    def test_wrappers_reusable_calls_and_dynamic_matrices_are_unknown(self):
        wrapper = self.report(self.source(command="python devtools/run_suite.py"))
        self.assertEqual(self.lane(wrapper)["state"], "unknown")
        reusable = self.report(
            "on: [pull_request]\njobs:\n  test:\n    uses: uibcdf/example/.github/workflows/tests.yml@"
            + "b" * 40
            + "\n"
        )
        self.assertEqual(self.lane(reusable)["state"], "unknown")
        dynamic = self.report("""on: [pull_request]
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix: ${{ fromJSON(inputs.matrix) }}
    steps:
      - run: pytest
""")
        self.assertEqual(self.lane(dynamic)["state"], "unknown")

    def test_cancellation_predicate_needs_runtime_facts_but_probe_still_excludes(self):
        source = self.source(
            job_if="    if: >-\n      !cancelled() && inputs.probe_backlog != true\n"
        ).replace(
            "  workflow_dispatch:\n",
            "  workflow_dispatch:\n"
            "    inputs:\n"
            "      probe_backlog:\n"
            "        type: boolean\n"
            "        default: false\n",
        )
        member = self.report(source)["members"][0]
        self.assertTrue(member["profile_inputs_current"])
        routes = {route["scenario"]: route for route in member["event_routes"]}
        default = routes["workflow_dispatch:defaults"]
        self.assertIsNone(default["jobs"][0]["condition_outcome"])
        probe = routes["workflow_dispatch:inputs.probe_backlog=true"]
        self.assertIs(probe["jobs"][0]["condition_outcome"], False)
        for route in (default, probe):
            self.assertEqual(route["execution_evidence"], "not_requested")
            self.assertEqual(route["dependency_status"], "not_evaluated")

    def test_selection_input_drift_invalidates_full_suite_review(self):
        self.report(self.source())
        (self.root / "pyproject.toml").write_text(
            '[tool.pytest.ini_options]\naddopts = "-k smoke"\n'
        )
        report = python_ci_status.inspect_pilot(
            self.registry, self.workspace, self.profiles
        )
        self.assertFalse(report["members"][0]["profile_inputs_current"])
        self.assertEqual(self.lane(report)["reviewed_test_level"], "unknown")
        self.assertFalse(self.lane(report)["reviewed_level_matches_target"])
        self.assertTrue(
            all(
                not route["profile_inputs_current"]
                for route in report["members"][0]["event_routes"]
            )
        )

    def test_unbound_root_pytest_configs_invalidate_selection_review(self):
        self.report(self.source())
        configurations = {
            "pytest.toml": '[pytest]\naddopts = ["-k", "only_this_subset"]\n',
            ".pytest.toml": '[pytest]\naddopts = ["-k", "only_this_subset"]\n',
            "pytest.ini": "[pytest]\naddopts = -k only_this_subset\n",
            ".pytest.ini": "[pytest]\naddopts = -k only_this_subset\n",
            "tox.ini": "[pytest]\naddopts = -k only_this_subset\n",
            "setup.cfg": "[tool:pytest]\naddopts = -k only_this_subset\n",
        }
        for name, content in configurations.items():
            with self.subTest(name=name):
                path = self.root / name
                path.write_text(content)
                try:
                    report = python_ci_status.inspect_pilot(
                        self.registry, self.workspace, self.profiles
                    )
                    member = report["members"][0]
                    self.assertFalse(member["profile_inputs_current"])
                    self.assertTrue(
                        all(row["state"] == "unknown" for row in member["lanes"])
                    )
                    self.assertTrue(
                        all(
                            not row["reviewed_level_matches_target"]
                            for row in member["lanes"]
                        )
                    )
                    self.assertTrue(
                        all(
                            not route["profile_inputs_current"]
                            for route in member["event_routes"]
                        )
                    )
                    finding = next(
                        row for row in member["inputs"] if row["path"] == name
                    )
                    self.assertFalse(finding["matches"])
                    self.assertIsNone(finding["expected_sha256"])
                    self.assertIn("not bound", finding["reason"])
                    self.assertEqual(member["execution_evidence"], "not_requested")
                    self.assertEqual(member["backlog_clearance"], "not_evaluated")
                finally:
                    path.unlink()

    def test_opt_in_collection_roots_detect_new_ancestor_and_nested_hooks(self):
        self.report(self.source())
        self.profiles["schema-version"] = 2
        (self.root / "tests/unit").mkdir(parents=True)
        self.profiles["profiles"][0]["collection-roots"] = ["tests/unit"]
        baseline = python_ci_status.inspect_pilot(
            self.registry, self.workspace, self.profiles
        )
        self.assertTrue(baseline["members"][0]["profile_inputs_current"])
        for relative in (
            "conftest.py",
            "tests/conftest.py",
            "tests/unit/conftest.py",
            "tests/unit/nested/conftest.py",
        ):
            with self.subTest(relative=relative):
                hook = self.root / relative
                hook.parent.mkdir(parents=True, exist_ok=True)
                hook.write_text("raise RuntimeError('must never import this hook')\n")
                try:
                    report = python_ci_status.inspect_pilot(
                        self.registry, self.workspace, self.profiles
                    )
                    member = report["members"][0]
                    self.assertFalse(member["profile_inputs_current"])
                    self.assertEqual(self.lane(report)["state"], "unknown")
                    self.assertFalse(self.lane(report)["reviewed_level_matches_target"])
                    finding = next(r for r in member["inputs"] if r["path"] == relative)
                    self.assertIn("not bound", finding["reason"])
                    self.assertEqual(member["execution_evidence"], "not_requested")
                    self.assertEqual(member["backlog_clearance"], "not_evaluated")
                finally:
                    hook.unlink()

    def test_bound_collection_hooks_keep_review_until_changed_or_missing(self):
        self.report(self.source())
        self.profiles["schema-version"] = 2
        tests = self.root / "tests"
        tests.mkdir()
        hook = tests / "conftest.py"
        hook.write_text("raise RuntimeError('inspection must never import hooks')\n")
        profile = self.profiles["profiles"][0]
        profile["collection-roots"] = ["tests"]
        profile["inputs"]["tests/conftest.py"] = hashlib.sha256(
            hook.read_bytes()
        ).hexdigest()
        current = python_ci_status.inspect_pilot(
            self.registry, self.workspace, self.profiles
        )
        self.assertTrue(current["members"][0]["profile_inputs_current"])
        for changed in ("raise RuntimeError('changed hook')\n", None):
            with self.subTest(changed=changed):
                if changed is None:
                    hook.unlink()
                else:
                    hook.write_text(changed)
                report = python_ci_status.inspect_pilot(
                    self.registry, self.workspace, self.profiles
                )
                self.assertEqual(self.lane(report)["state"], "unknown")
                self.assertFalse(report["members"][0]["profile_inputs_current"])

    def test_collection_roots_reject_invalid_profiles_and_report_missing_tree(self):
        self.report(self.source())
        self.profiles["schema-version"] = 2
        profile = self.profiles["profiles"][0]
        for roots in (
            [],
            "tests",
            ["."],
            ["../tests"],
            ["/tmp"],
            ["C:/tests"],
            ["tests\x00"],
            ["tests\\unit"],
            ["tests//unit"],
            ["tests", "tests"],
            ["tests", "tests/unit"],
            [None],
        ):
            with self.subTest(roots=roots):
                profile["collection-roots"] = roots
                with self.assertRaises(ValueError):
                    python_ci_status.inspect_pilot(
                        self.registry, self.workspace, self.profiles
                    )
        profile["collection-roots"] = ["missing-tests"]
        report = python_ci_status.inspect_pilot(
            self.registry, self.workspace, self.profiles
        )
        self.assertEqual(self.lane(report)["state"], "unknown")
        self.assertIn("missing", report["members"][0]["inputs"][-1]["reason"])

    def test_linked_collection_trees_and_hooks_are_unknown(self):
        self.report(self.source())
        self.profiles["schema-version"] = 2
        tests = self.root / "tests"
        tests.mkdir()
        outside = self.workspace / "outside"
        (outside / "unit").mkdir(parents=True)
        (outside / "conftest.py").write_text("raise RuntimeError('do not import')\n")
        profile = self.profiles["profiles"][0]
        profile["collection-roots"] = ["tests"]
        for relative in ("tests/linked", "tests/conftest.py", "tests"):
            with self.subTest(relative=relative):
                link = self.root / relative
                if relative == "tests":
                    tests.rmdir()
                    profile["collection-roots"] = ["tests/unit"]
                try:
                    link.symlink_to(outside / "conftest.py" if link.suffix else outside)
                except (OSError, NotImplementedError) as error:
                    self.skipTest(
                        f"symlink fixture unavailable: {type(error).__name__}"
                    )
                try:
                    report = python_ci_status.inspect_pilot(
                        self.registry, self.workspace, self.profiles
                    )
                    self.assertEqual(self.lane(report)["state"], "unknown")
                    self.assertTrue(
                        any(
                            "symlink" in r.get("reason", "")
                            for r in report["members"][0]["inputs"]
                        )
                    )
                finally:
                    link.unlink()

    def test_collection_inspection_limits_and_read_errors_are_unknown(self):
        self.report(self.source())
        self.profiles["schema-version"] = 2
        tests = self.root / "tests"
        tests.mkdir()
        (tests / "test_one.py").write_text("def test_one(): pass\n")
        self.profiles["profiles"][0]["collection-roots"] = ["tests"]
        for control in (
            patch.object(python_ci_status, "MAX_COLLECTION_ENTRIES", 1),
            patch.object(python_ci_status.os, "walk", side_effect=PermissionError),
        ):
            with control:
                report = python_ci_status.inspect_pilot(
                    self.registry, self.workspace, self.profiles
                )
                self.assertEqual(self.lane(report)["state"], "unknown")
                self.assertFalse(report["members"][0]["profile_inputs_current"])

    def test_collection_discovery_is_opt_in_and_stays_inside_declared_scope(self):
        baseline = self.report(self.source())
        (self.root / "tests").mkdir()
        (self.root / "tests/conftest.py").write_text(
            "raise RuntimeError('unreviewed')\n"
        )
        with patch.object(python_ci_status.os, "walk", side_effect=AssertionError):
            legacy = python_ci_status.inspect_pilot(
                self.registry, self.workspace, self.profiles
            )
        self.assertEqual(legacy, baseline)
        (self.root / "tests/conftest.py").unlink()
        (self.root / "docs").mkdir()
        (self.root / "docs/conftest.py").write_text(
            "raise RuntimeError('outside scope')\n"
        )
        self.profiles["schema-version"] = 2
        self.profiles["profiles"][0]["collection-roots"] = ["tests"]
        current = python_ci_status.inspect_pilot(
            self.registry, self.workspace, self.profiles
        )
        self.assertTrue(current["members"][0]["profile_inputs_current"])
        self.assertEqual(
            current["members"][0]["collection_hook_scope"]["roots"], ["tests"]
        )

    def test_collection_scope_requires_v2_and_legacy_reports_remain_equal(self):
        original = self.report(self.source())
        self.profiles["schema-version"] = 2
        upgraded = python_ci_status.inspect_pilot(
            self.registry, self.workspace, self.profiles
        )
        self.assertEqual(original, upgraded)
        self.profiles["schema-version"] = 1
        self.profiles["profiles"][0]["collection-roots"] = ["tests"]
        with self.assertRaisesRegex(ValueError, "requires schema-version 2"):
            python_ci_status.inspect_pilot(self.registry, self.workspace, self.profiles)
        for invalid in (0, 3, True, "2", None):
            with self.subTest(invalid=invalid):
                self.profiles["schema-version"] = invalid
                with self.assertRaisesRegex(ValueError, "schema-version 1 or 2"):
                    python_ci_status.inspect_pilot(
                        self.registry, self.workspace, self.profiles
                    )

    def test_reviewed_root_config_keeps_level_and_later_hash_drift_explicit(self):
        self.report(self.source())
        path = self.root / "pytest.ini"
        path.write_text("[pytest]\naddopts = -k only_this_subset\n")
        profile = self.profiles["profiles"][0]
        profile["inputs"]["pytest.ini"] = hashlib.sha256(path.read_bytes()).hexdigest()
        profile["lanes"][0].update(
            {"test-level": "smoke", "smoke-issue": "uibcdf/example#2"}
        )
        self.registry["python-ci-reviews"][0]["routine-test-level"] = "smoke"
        reviewed = python_ci_status.inspect_pilot(
            self.registry, self.workspace, self.profiles
        )
        self.assertTrue(reviewed["members"][0]["profile_inputs_current"])
        self.assertTrue(self.lane(reviewed, "push")["reviewed_level_matches_target"])
        self.assertFalse(self.lane(reviewed)["reviewed_level_matches_target"])
        for changed in ("[pytest]\naddopts = -k another_subset\n", None):
            with self.subTest(changed=changed):
                if changed is None:
                    path.unlink()
                else:
                    path.write_text(changed)
                report = python_ci_status.inspect_pilot(
                    self.registry, self.workspace, self.profiles
                )
                self.assertFalse(report["members"][0]["profile_inputs_current"])
                self.assertEqual(self.lane(report)["state"], "unknown")
                self.assertFalse(self.lane(report)["reviewed_level_matches_target"])

    def test_real_pytest_new_root_config_can_narrow_a_reviewed_suite(self):
        self.report(self.source())
        tests = self.root / "tests"
        tests.mkdir()
        (tests / "test_selection.py").write_text(
            "def test_kept():\n    assert True\n\ndef test_other():\n    assert True\n"
        )
        env = os.environ.copy()
        for key in ("PYTEST_ADDOPTS", "PYTEST_PLUGINS", "PYTHONPATH"):
            env.pop(key, None)
        env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"

        def run():
            result = subprocess.run(
                [sys.executable, "-m", "pytest", "-q"],
                cwd=self.root,
                env=env,
                capture_output=True,
                text=True,
                check=False,
                timeout=30,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            return result.stdout

        self.assertIn("2 passed", run())
        (self.root / "pytest.ini").write_text("[pytest]\naddopts = -k kept\n")
        self.assertIn("1 passed, 1 deselected", run())
        report = python_ci_status.inspect_pilot(
            self.registry, self.workspace, self.profiles
        )
        self.assertFalse(report["members"][0]["profile_inputs_current"])
        self.assertEqual(self.lane(report)["state"], "unknown")
        self.assertFalse(self.lane(report)["reviewed_level_matches_target"])

    def test_scoped_selection_is_not_a_full_target_or_a_smoke_exception(self):
        self.report(self.source(command='python -m pytest tests -m "not qt_runtime"'))
        self.profiles["schema-version"] = 2
        lane = self.profiles["profiles"][0]["lanes"][0]
        lane.update(
            {
                "test-level": "scoped",
                "selection-context": "Configured core selection excludes experimental qt_runtime.",
                "scope-issue": "uibcdf/example#1",
            }
        )
        report = python_ci_status.inspect_pilot(
            self.registry, self.workspace, self.profiles
        )
        observed = self.lane(report)
        self.assertEqual(report["schema"], "molsyssuite.ci-pilot@2")
        self.assertEqual(observed["state"], "configured")
        self.assertEqual(observed["reviewed_test_level"], "scoped")
        self.assertEqual(observed["target_test_level"], "full")
        self.assertFalse(observed["reviewed_level_matches_target"])
        self.assertEqual(observed["scope_issue"], "uibcdf/example#1")
        self.assertIsNone(observed["smoke_issue"])
        self.assertEqual(report["members"][0]["execution_evidence"], "not_requested")

    def test_scoped_metadata_needs_v2_context_and_owning_issue(self):
        self.report(self.source())
        profile = self.profiles["profiles"][0]
        lane = profile["lanes"][0]
        lane.update(
            {
                "test-level": "scoped",
                "selection-context": "Explicit subset",
                "scope-issue": "uibcdf/example#1",
            }
        )
        with self.assertRaisesRegex(ValueError, "schema-version 2"):
            python_ci_status.inspect_pilot(self.registry, self.workspace, self.profiles)
        self.profiles["schema-version"] = 2
        for context, issue in [
            (None, "uibcdf/example#1"),
            ("", "uibcdf/example#1"),
            (" ", "uibcdf/example#1"),
            ("valid", "uibcdf/other#1"),
            ("valid", ""),
            ([], "uibcdf/example#1"),
            ("x" * 2001, "uibcdf/example#1"),
        ]:
            with self.subTest(context=context, issue=issue):
                lane.update({"selection-context": context, "scope-issue": issue})
                with self.assertRaises(ValueError):
                    python_ci_status.inspect_pilot(
                        self.registry, self.workspace, self.profiles
                    )
        lane.update(
            {
                "selection-context": "valid",
                "scope-issue": "uibcdf/example#1",
                "test-level": "full",
            }
        )
        with self.assertRaisesRegex(ValueError, "scope-issue requires"):
            python_ci_status.inspect_pilot(self.registry, self.workspace, self.profiles)

    def test_scoped_context_stays_visible_when_input_drift_is_unknown(self):
        self.report(self.source())
        self.profiles["schema-version"] = 2
        self.profiles["profiles"][0]["lanes"][0].update(
            {
                "test-level": "scoped",
                "selection-context": "Reviewed core without experimental marker",
                "scope-issue": "uibcdf/example#1",
            }
        )
        self.workflow.write_text(self.source(command="python devtools/run_suite.py"))
        report = python_ci_status.inspect_pilot(
            self.registry, self.workspace, self.profiles
        )
        self.assertEqual(self.lane(report)["state"], "unknown")
        self.assertEqual(self.lane(report)["reviewed_test_level"], "unknown")
        self.assertFalse(self.lane(report)["reviewed_level_matches_target"])
        self.assertEqual(self.lane(report)["scope_issue"], "uibcdf/example#1")
        self.assertIn("Reviewed core", self.lane(report)["selection_context"])

    def test_smoke_push_does_not_satisfy_full_pr_target(self):
        self.registry["python-ci-reviews"][0]["routine-test-level"] = "smoke"
        report = self.report(
            self.source(command="pytest tests/smoke"),
            level="smoke",
            smoke_issue="uibcdf/example#2",
        )
        self.assertTrue(self.lane(report, "push")["reviewed_level_matches_target"])
        self.assertFalse(self.lane(report)["reviewed_level_matches_target"])
        with self.assertRaisesRegex(ValueError, "smoke profile needs"):
            self.report(self.source(), level="smoke")

    def test_coverage_module_is_recognized_without_inventing_shell_execution(self):
        command = (
            "python -m coverage run --branch --source=example -m pytest --receptor=ci"
        )
        self.assertIsNone(ci_lane_inventory.PYTEST_COMMAND.match(command))
        self.assertEqual(ci_lane_inventory.pytest_commands(command), [command])
        self.assertEqual(
            ci_lane_inventory.pytest_commands("python -m coverage run -m pytest"),
            ["python -m coverage run -m pytest"],
        )
        for invalid in (
            "echo 'python -m coverage run -m pytest'",
            "python -m coverage run script.py -m pytest",
            "python -m coverage run -m other --arg '-m pytest'",
            "python -m coverage run 'unterminated",
        ):
            self.assertEqual(ci_lane_inventory.pytest_commands(invalid), [])
        report = self.report(self.source(command=command))
        self.assertEqual(self.lane(report)["state"], "configured")

    def test_cli_is_informational_and_refuses_enforcement_combination(self):
        self.report(self.source())
        with (
            patch.object(
                python_ci_status, "PILOT_PROFILES", self.workspace / "unused.toml"
            ),
            patch.object(
                python_ci_status, "inspect_pilot", return_value={"members": []}
            ),
            patch.object(
                python_ci_status.tomllib,
                "loads",
                side_effect=[self.registry, self.profiles],
            ),
            patch.object(Path, "read_text", return_value="placeholder"),
            redirect_stdout(io.StringIO()) as output,
        ):
            self.assertEqual(python_ci_status.main(["--pilot", str(self.workspace)]), 0)
        self.assertIn("INFORMATIONAL PILOT", output.getvalue())
        with (
            redirect_stdout(io.StringIO()),
            redirect_stderr(io.StringIO()),
            patch.object(python_ci_status.tomllib, "loads", return_value=self.registry),
            patch.object(Path, "read_text", return_value="placeholder"),
            self.assertRaises(SystemExit),
        ):
            python_ci_status.main(["--pilot", str(self.workspace), "--require-adopted"])


if __name__ == "__main__":
    unittest.main()
