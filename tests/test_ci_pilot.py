"""Adversarial coverage for informational CI profiles, never a compliance gate."""

from __future__ import annotations

import hashlib
import io
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

    def test_comment_version_cannot_supply_required_interpreter(self):
        report = self.report("# Python 3.14 planned\n" + self.source(version="3.13"))
        self.assertEqual(self.lane(report)["state"], "not_observed")

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
