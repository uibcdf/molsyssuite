from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from devtools.scripts import ci_lane_inventory


class CILaneInventoryTests(unittest.TestCase):
    def _workflow(self, text: str) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        path = Path(temporary.name) / "ci.yaml"
        path.write_text(text, encoding="utf-8")
        return path

    def test_static_matrix_keeps_events_cells_and_gating_separate(self):
        path = self._workflow(
            """
on:
  push:
  schedule:
    - cron: "17 9 * * 1"
jobs:
  test:
    runs-on: ${{ matrix.os }}
    continue-on-error: ${{ matrix.experimental }}
    strategy:
      matrix:
        os: [ubuntu-latest]
        python: ["3.11", "3.12"]
        experimental: [false]
        exclude:
          - { os: ubuntu-latest, python: "3.12" }
        include:
          - { os: macos-latest, python: "3.13", experimental: true }
    steps:
      - uses: actions/setup-python@v6
        with:
          python-version: ${{ matrix.python }}
      - run: python -m pytest tests/
"""
        )

        lanes = ci_lane_inventory.inventory_workflow(path, "uibcdf/example")

        self.assertEqual(len(lanes), 4)
        self.assertEqual(
            {(lane["event"], lane["os"], lane["python"]) for lane in lanes},
            {
                ("push", "ubuntu-latest", "3.11"),
                ("push", "macos-latest", "3.13"),
                ("schedule", "ubuntu-latest", "3.11"),
                ("schedule", "macos-latest", "3.13"),
            },
        )
        self.assertTrue(all(lane["test_command_observed"] for lane in lanes))
        self.assertEqual(
            {lane["gating"] for lane in lanes if lane["os"] == "macos-latest"},
            {False},
        )

    def test_version_in_comment_or_non_test_job_is_not_test_evidence(self):
        path = self._workflow(
            """
# Python 3.14 is planned.
on: [push]
jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - run: echo 'pytest on Python 3.14 someday'
"""
        )

        lanes = ci_lane_inventory.inventory_workflow(path, "uibcdf/example")

        self.assertEqual(len(lanes), 1)
        self.assertEqual(lanes[0]["python"], "unknown")
        self.assertFalse(lanes[0]["test_command_observed"])

    def test_nested_matrix_and_condition_are_not_claimed_as_guaranteed(self):
        path = self._workflow(
            """
on:
  push:
    paths-ignore: ["docs/**"]
  pull_request:
jobs:
  smoke:
    if: github.event_name != 'schedule' && !contains(github.event.head_commit.message, '[skip ci]')
    runs-on: ${{ matrix.cfg.os }}
    strategy:
      matrix:
        cfg:
          - { os: ubuntu-latest, python-version: "3.13" }
    steps:
      - uses: actions/setup-python@v6
        with:
          python-version: ${{ matrix.cfg.python-version }}
      - run: pytest --receptor=ci
"""
        )

        lanes = ci_lane_inventory.inventory_workflow(path, "uibcdf/example")

        self.assertEqual(len(lanes), 2)
        self.assertEqual({lane["python"] for lane in lanes}, {"3.13"})
        self.assertTrue(all(lane["conditional"] for lane in lanes))
        self.assertTrue(
            next(lane for lane in lanes if lane["event"] == "push")["path_filtered"]
        )
        self.assertFalse(
            next(lane for lane in lanes if lane["event"] == "pull_request")[
                "path_filtered"
            ]
        )

    def test_unresolved_matrix_is_reported_without_inventing_a_lane(self):
        path = self._workflow(
            """
on: [workflow_dispatch]
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix: ${{ fromJSON(inputs.matrix) }}
    steps:
      - uses: actions/setup-python@v6
        with:
          python-version: ${{ matrix.python }}
      - run: pytest
"""
        )

        lanes = ci_lane_inventory.inventory_workflow(path, "uibcdf/example")

        self.assertEqual(len(lanes), 1)
        self.assertEqual(lanes[0]["os"], "unknown")
        self.assertEqual(lanes[0]["python"], "unknown")
        self.assertEqual(lanes[0]["matrix_status"], "unresolved")

    def test_include_after_excluding_first_cell_does_not_duplicate_second(self):
        path = self._workflow(
            """
on: [push]
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest]
        exclude:
          - { os: ubuntu-latest }
        include:
          - { os: macos-latest, experimental: false }
    steps:
      - run: pytest
"""
        )

        lanes = ci_lane_inventory.inventory_workflow(path, "uibcdf/example")

        self.assertEqual(len(lanes), 1)
        self.assertEqual(lanes[0]["os"], "macos-latest")

    def test_include_only_matrix_has_one_cell_per_entry(self):
        path = self._workflow(
            """
on: [workflow_dispatch]
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        include:
          - { os: ubuntu-latest, python: "3.13" }
          - { os: macos-latest, python: "3.14" }
    steps:
      - uses: actions/setup-python@v6
        with:
          python-version: ${{ matrix.python }}
      - run: pytest
"""
        )

        lanes = ci_lane_inventory.inventory_workflow(path, "uibcdf/example")

        self.assertEqual(
            {(lane["os"], lane["python"]) for lane in lanes},
            {("ubuntu-latest", "3.13"), ("macos-latest", "3.14")},
        )

    def test_tolerated_test_step_is_not_a_gating_lane(self):
        path = self._workflow(
            """
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/setup-python@v6
        with:
          python-version: "3.13"
      - run: pytest
        continue-on-error: true
"""
        )

        lanes = ci_lane_inventory.inventory_workflow(path, "uibcdf/example")

        self.assertEqual(len(lanes), 1)
        self.assertTrue(lanes[0]["test_command_observed"])
        self.assertFalse(lanes[0]["gating"])

    def test_conditional_test_step_is_not_a_guaranteed_lane(self):
        path = self._workflow(
            """
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/setup-python@v6
        with:
          python-version: "3.13"
      - run: pytest
        if: github.event_name == 'schedule'
"""
        )

        lanes = ci_lane_inventory.inventory_workflow(path, "uibcdf/example")

        self.assertEqual(len(lanes), 1)
        self.assertTrue(lanes[0]["test_command_observed"])
        self.assertFalse(lanes[0]["event_eligible"])
        self.assertFalse(lanes[0]["conditional"])

    def test_tag_only_push_is_not_unrestricted_branch_ci(self):
        path = self._workflow(
            """
on:
  push:
    tags: ["*"]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: pytest
"""
        )

        lanes = ci_lane_inventory.inventory_workflow(path, "uibcdf/example")

        self.assertEqual(len(lanes), 1)
        self.assertTrue(lanes[0]["ref_filtered"])
        self.assertTrue(lanes[0]["tag_only"])

    def test_event_routing_does_not_claim_scheduled_test_on_push(self):
        path = self._workflow(
            """
on: [push, pull_request, schedule]
jobs:
  full_matrix:
    if: ${{ github.event_name == 'schedule' }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/setup-python@v6
        with:
          python-version: "3.13"
      - run: pytest
"""
        )

        lanes = ci_lane_inventory.inventory_workflow(path, "uibcdf/example")

        self.assertEqual(
            {lane["event"]: lane["event_eligible"] for lane in lanes},
            {"push": False, "pull_request": False, "schedule": True},
        )
        self.assertFalse(any(lane["conditional"] for lane in lanes))

    def test_test_step_routing_and_tolerated_failure_are_event_specific(self):
        path = self._workflow(
            """
on: [push, schedule]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/setup-python@v6
        with:
          python-version: "3.13"
      - run: pytest tests/routine
        if: github.event_name == 'push'
        continue-on-error: true
      - run: pytest tests/full
        if: github.event_name == 'schedule'
"""
        )

        lanes = ci_lane_inventory.inventory_workflow(path, "uibcdf/example")

        self.assertEqual(
            {lane["event"]: lane["gating"] for lane in lanes},
            {"push": False, "schedule": True},
        )
        self.assertTrue(all(lane["event_eligible"] for lane in lanes))

    def test_unresolved_condition_remains_unknown_on_matching_event(self):
        path = self._workflow(
            """
on: [push, schedule]
jobs:
  test:
    if: github.event_name != 'schedule' && !contains(github.event.head_commit.message, '[skip ci]')
    runs-on: ubuntu-latest
    steps:
      - run: pytest
"""
        )

        lanes = ci_lane_inventory.inventory_workflow(path, "uibcdf/example")

        self.assertEqual(
            {lane["event"]: lane["event_eligible"] for lane in lanes},
            {"push": None, "schedule": False},
        )
        self.assertTrue(
            next(lane for lane in lanes if lane["event"] == "push")["conditional"]
        )

    def test_github_event_name_comparison_ignores_case(self):
        path = self._workflow(
            """
on: [push, schedule]
jobs:
  test:
    if: github.event_name == 'PUSH'
    runs-on: ubuntu-latest
    steps:
      - run: pytest
"""
        )

        lanes = ci_lane_inventory.inventory_workflow(path, "uibcdf/example")

        self.assertEqual(
            {lane["event"]: lane["event_eligible"] for lane in lanes},
            {"push": True, "schedule": False},
        )

    def test_unrecognized_bare_event_name_is_not_treated_as_github_context(self):
        path = self._workflow(
            """
on: [push]
jobs:
  test:
    if: event_name == 'push'
    runs-on: ubuntu-latest
    steps:
      - run: pytest
"""
        )

        lanes = ci_lane_inventory.inventory_workflow(path, "uibcdf/example")

        self.assertIsNone(lanes[0]["event_eligible"])

    def test_starter_workflow_routes_routine_and_full_jobs_to_their_events(self):
        path = (
            Path(__file__).resolve().parents[1]
            / "devtools/templates/python_component/.github/workflows/ci.yml"
        )

        lanes = ci_lane_inventory.inventory_workflow(path, "uibcdf/example")
        by_job_event = {(lane["job"], lane["event"]): lane for lane in lanes}

        for event in ("push", "pull_request"):
            self.assertTrue(by_job_event[("test", event)]["event_eligible"])
            self.assertFalse(by_job_event[("full_matrix", event)]["event_eligible"])
        for event in ("schedule", "workflow_dispatch"):
            self.assertFalse(by_job_event[("test", event)]["event_eligible"])
            self.assertTrue(by_job_event[("full_matrix", event)]["event_eligible"])


if __name__ == "__main__":
    unittest.main()
