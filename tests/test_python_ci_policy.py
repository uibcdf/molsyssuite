"""Guard the accepted CI target without claiming member rollout is complete."""

from __future__ import annotations

import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

import yaml

from devtools.scripts import bootstrap_component, python_ci_status, suite_policy

ROOT = Path(__file__).resolve().parents[1]


class PythonCIPolicyTests(unittest.TestCase):
    def test_every_python_member_has_an_honest_review(self):
        registry = suite_policy.load_effective_registry()
        self.assertEqual(python_ci_status.validate(registry), [])
        reviews = registry["python-ci-reviews"]
        self.assertEqual(
            len(reviews),
            sum(
                "python-package" in member.get("capabilities", [])
                for member in registry["members"]
            ),
        )
        by_repository = {review["repository"]: review for review in reviews}
        self.assertEqual(by_repository["uibcdf/smonitor"]["state"], "partial")
        self.assertEqual(
            by_repository["uibcdf/smonitor"]["review-issue"],
            "uibcdf/smonitor#33",
        )
        self.assertEqual(by_repository["uibcdf/argdigest"]["state"], "partial")
        self.assertEqual(
            by_repository["uibcdf/argdigest"]["review-issue"],
            "uibcdf/argdigest#21",
        )
        self.assertEqual(by_repository["uibcdf/gh-run-receptor"]["state"], "adopted")
        self.assertEqual(by_repository["uibcdf/molsysmt"]["state"], "partial")
        self.assertEqual(
            by_repository["uibcdf/molsysmt"]["smoke-issue"],
            "uibcdf/molsysmt#185",
        )
        self.assertEqual(by_repository["uibcdf/molsysviewer"]["state"], "partial")
        self.assertEqual(
            by_repository["uibcdf/molsysviewer"]["review-issue"],
            "uibcdf/molsysviewer#116",
        )
        self.assertTrue(
            all(
                review["state"] == "pending"
                for repository, review in by_repository.items()
                if repository
                not in {
                    "uibcdf/smonitor",
                    "uibcdf/argdigest",
                    "uibcdf/gh-run-receptor",
                    "uibcdf/molsysmt",
                    "uibcdf/molsysviewer",
                }
            )
        )

    def test_review_guard_rejects_missing_and_false_adoption(self):
        registry = deepcopy(suite_policy.load_effective_registry())
        review = registry["python-ci-reviews"].pop()
        self.assertIn(
            f"python CI review: missing {review['repository']}",
            python_ci_status.validate(registry),
        )

        review = next(
            item for item in registry["python-ci-reviews"] if item["state"] == "pending"
        )
        review.update(state="adopted", **{"review-issue": "uibcdf/molsyssuite#39"})
        errors = python_ci_status.validate(registry)
        self.assertTrue(any("needs a member issue" in error for error in errors))
        self.assertTrue(any("adoption is unreviewed" in error for error in errors))
        self.assertTrue(
            any("lacks a member hosted run URL" in error for error in errors)
        )

    def test_smoke_and_exception_need_bounded_local_evidence(self):
        registry = deepcopy(suite_policy.load_effective_registry())
        review = registry["python-ci-reviews"][0]
        review.update(
            state="adopted",
            **{
                "review-issue": "uibcdf/smonitor#1",
                "routine-test-level": "smoke",
                "platform-claims-reviewed": True,
                "evidence": "Reviewed full lane at exact candidate",
                "hosted-evidence": "https://github.com/uibcdf/smonitor/actions/runs/1",
            },
        )
        self.assertTrue(
            any(
                "smoke needs a member issue" in error
                for error in python_ci_status.validate(registry)
            )
        )
        review["smoke-issue"] = "uibcdf/smonitor#2"
        self.assertEqual(python_ci_status.validate(registry), [])

        review.update(
            state="excepted",
            **{"expires-on": "2020-01-01", "reason": "bounded transition"},
        )
        self.assertTrue(
            any(
                "exception expired" in error
                for error in python_ci_status.validate(registry)
            )
        )

    def test_registry_points_to_the_accepted_python_ci_contract(self):
        registry = suite_policy.load_effective_registry()
        policy = registry["policies"]["python-ci"]

        self.assertEqual(policy["status"], "accepted")
        self.assertEqual(policy["adoption"], "phased")
        self.assertEqual(policy["review-table"], "python-ci-reviews")
        self.assertEqual(policy["applies-to"], ["capability:python-package"])
        self.assertEqual(policy["routine-python"], "3.13")
        self.assertEqual(policy["routine-events"], ["push", "pull_request"])
        self.assertEqual(policy["routine-os"], "linux")
        self.assertEqual(policy["pull-request-test-level"], "full")
        self.assertEqual(
            policy["skip-ci-recovery"], "daily-conditional-full-when-enabled"
        )
        self.assertEqual(policy["full-matrix-frequency"], "weekly")
        self.assertEqual(policy["full-matrix-os"], ["linux"])
        self.assertTrue((ROOT / policy["normative"]).is_file())

    def test_starter_workflow_has_routine_and_weekly_full_lanes(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = (
                bootstrap_component.bootstrap(
                    Path(temporary) / "topomt",
                    "uibcdf/topomt",
                    "Topological molecular analysis",
                )
                / ".github/workflows/ci.yml"
            )
            workflow = yaml.load(
                path.read_text(encoding="utf-8"), Loader=yaml.BaseLoader
            )
        policy = suite_policy.load_effective_registry()["policies"]
        self.assertEqual(
            set(workflow["on"]),
            {"push", "pull_request", "schedule", "workflow_dispatch"},
        )
        routine = workflow["jobs"]["test"]
        full = workflow["jobs"]["full_matrix"]
        self.assertEqual(
            routine["steps"][1]["with"]["create-args"],
            f"python={policy['python']['development-version']}",
        )
        self.assertEqual(
            routine["steps"][1]["with"]["environment-file"],
            "devtools/conda-envs/test_env.yaml",
        )
        self.assertIn(
            "mamba-org/setup-micromamba@",
            routine["steps"][1]["uses"],
        )
        self.assertIn("push", routine["if"])
        self.assertIn("pull_request", routine["if"])
        self.assertNotIn("continue-on-error", routine)
        self.assertEqual(
            full["strategy"]["matrix"]["python-version"],
            policy["python"]["ci-versions"],
        )
        self.assertIn("schedule", full["if"])
        self.assertIn("workflow_dispatch", full["if"])
        self.assertNotIn("continue-on-error", full)
        self.assertTrue(workflow["on"]["schedule"])


if __name__ == "__main__":
    unittest.main()
