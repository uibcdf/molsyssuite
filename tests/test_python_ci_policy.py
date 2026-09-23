"""Guard the accepted CI target without claiming member rollout is complete."""

from __future__ import annotations

import unittest
from pathlib import Path

import tomllib
import yaml

ROOT = Path(__file__).resolve().parents[1]


class PythonCIPolicyTests(unittest.TestCase):
    def test_registry_points_to_the_accepted_python_ci_contract(self):
        registry = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
        policy = registry["policies"]["python-ci"]

        self.assertEqual(policy["status"], "accepted")
        self.assertEqual(policy["adoption"], "phased")
        self.assertEqual(policy["applies-to"], ["capability:python-package"])
        self.assertEqual(policy["routine-python"], "3.13")
        self.assertEqual(policy["routine-events"], ["push", "pull_request"])
        self.assertEqual(policy["routine-os"], "linux")
        self.assertEqual(policy["full-matrix-frequency"], "weekly")
        self.assertEqual(policy["full-matrix-os"], ["linux"])
        self.assertTrue((ROOT / policy["normative"]).is_file())

    def test_starter_workflow_has_routine_and_weekly_full_lanes(self):
        path = ROOT / "devtools/templates/python_component/.github/workflows/ci.yml"
        workflow = yaml.load(path.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
        self.assertEqual(
            set(workflow["on"]),
            {"push", "pull_request", "schedule", "workflow_dispatch"},
        )
        routine = workflow["jobs"]["test"]
        full = workflow["jobs"]["full_matrix"]
        self.assertEqual(routine["steps"][1]["with"]["python-version"], "3.13")
        self.assertIn("push", routine["if"])
        self.assertIn("pull_request", routine["if"])
        self.assertNotIn("continue-on-error", routine)
        self.assertEqual(
            full["strategy"]["matrix"]["python-version"],
            ["3.11", "3.12", "3.13"],
        )
        self.assertIn("schedule", full["if"])
        self.assertIn("workflow_dispatch", full["if"])
        self.assertNotIn("continue-on-error", full)
        self.assertTrue(workflow["on"]["schedule"])


if __name__ == "__main__":
    unittest.main()
