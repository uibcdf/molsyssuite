"""Source predicate scenarios cannot become executed CI or recovery evidence."""

from __future__ import annotations

import unittest

from devtools.scripts import ci_lane_inventory


class CIEventRouteTests(unittest.TestCase):
    def setUp(self):
        self.daily = "47 0 * * *"
        self.weekly = "0 9 * * MON"
        self.condition = (
            "always() && inputs.probe_backlog != true && "
            "(github.event_name != 'schedule' || "
            f"github.event.schedule != '{self.daily}' || "
            "needs.nightly-decision.result != 'success' || "
            "needs.nightly-decision.outputs.run_full == 'true')"
        )
        self.document = {
            "on": {
                "schedule": [{"cron": self.weekly}, {"cron": self.daily}],
                "workflow_dispatch": {
                    "inputs": {"probe_backlog": {"type": "boolean", "default": "false"}}
                },
            },
            "jobs": {
                "nightly-decision": {
                    "if": (
                        "(github.event_name == 'schedule' && "
                        f"github.event.schedule == '{self.daily}') || "
                        "(github.event_name == 'workflow_dispatch' && "
                        "inputs.probe_backlog == true)"
                    ),
                    "steps": [{"run": "python devtools/ci_backlog.py"}],
                },
                "test": {
                    "needs": "nightly-decision",
                    "if": self.condition,
                    "steps": [{"run": "pytest tests"}],
                },
            },
        }

    def routes(self):
        return {
            row["scenario"]: row
            for row in ci_lane_inventory.inspect_event_routes(self.document, "test")
        }

    def outcomes(self, route):
        return {job["job"]: job["condition_outcome"] for job in route["jobs"]}

    def test_weekly_predicate_and_skipped_decision_are_separate_from_execution(self):
        weekly = self.routes()[f"schedule:{self.weekly}"]
        self.assertEqual(
            self.outcomes(weekly), {"test": True, "nightly-decision": False}
        )
        self.assertEqual(weekly["context"]["inputs.probe_backlog"], "")
        self.assertEqual(weekly["execution_evidence"], "not_requested")
        self.assertEqual(weekly["dependency_status"], "not_evaluated")
        self.assertNotIn("success", weekly)

    def test_daily_missing_detector_result_never_becomes_zero_debt(self):
        daily = self.routes()[f"schedule:{self.daily}"]
        self.assertEqual(self.outcomes(daily), {"test": None, "nightly-decision": True})
        self.assertNotIn("needs.nightly-decision.outputs.run_full", daily["context"])

    def test_manual_default_and_probe_boolean_have_opposite_test_predicates(self):
        routes = self.routes()
        self.assertEqual(
            self.outcomes(routes["workflow_dispatch:defaults"]),
            {"test": True, "nightly-decision": False},
        )
        probe = routes["workflow_dispatch:inputs.probe_backlog=true"]
        self.assertIs(probe["context"]["inputs.probe_backlog"], True)
        self.assertEqual(
            self.outcomes(probe), {"test": False, "nightly-decision": True}
        )
        self.document["on"]["workflow_dispatch"]["inputs"]["probe_backlog"][
            "default"
        ] = "true"
        changed = self.routes()
        self.assertEqual(
            self.outcomes(changed["workflow_dispatch:defaults"]),
            {"test": False, "nightly-decision": True},
        )
        self.assertEqual(
            self.outcomes(changed["workflow_dispatch:inputs.probe_backlog=false"]),
            {"test": True, "nightly-decision": False},
        )

    def test_detector_failure_is_fail_safe_and_successful_no_debt_skips_tests(self):
        context = {"github.event.schedule": self.daily, "inputs.probe_backlog": ""}
        for result, run_full, expected in (
            ("success", "false", False),
            ("success", "true", True),
            ("failure", "", True),
            ("cancelled", "", True),
        ):
            with self.subTest(result=result, run_full=run_full):
                supplied = {
                    **context,
                    "needs.nightly-decision.result": result,
                    "needs.nightly-decision.outputs.run_full": run_full,
                }
                self.assertIs(
                    ci_lane_inventory.condition_outcome(
                        self.condition, "schedule", supplied
                    ),
                    expected,
                )
        # An absent result does not mean failure; an absent output does not mean false.
        self.assertIsNone(
            ci_lane_inventory.condition_outcome(self.condition, "schedule", context)
        )
        self.assertIsNone(
            ci_lane_inventory.condition_outcome(
                self.condition,
                "schedule",
                {**context, "needs.nightly-decision.result": "success"},
            )
        )

    def test_action_equality_does_not_confuse_boolean_string_and_empty_property(self):
        for value, expected in (
            (True, True),
            (False, False),
            ("true", False),
            ("", False),
            ("1", True),
        ):
            with self.subTest(value=value):
                self.assertIs(
                    ci_lane_inventory.condition_outcome(
                        "inputs.probe_backlog == true",
                        "workflow_dispatch",
                        {"inputs.probe_backlog": value},
                    ),
                    expected,
                )
        self.assertTrue(
            ci_lane_inventory.condition_outcome(
                "needs.nightly-decision.outputs.run_full == 'TRUE'",
                "schedule",
                {"needs.nightly-decision.outputs.run_full": "true"},
            )
        )

    def test_literals_unknown_references_and_unsupported_calls_are_not_executed(self):
        self.assertFalse(
            ci_lane_inventory.condition_outcome(
                "'inputs.probe_backlog' == 'true'",
                "schedule",
                {"inputs.probe_backlog": True},
            )
        )
        for expression in (
            "inputs.missing != true",
            "failure()",
            "contains('a', 'a')",
            "__import__('os').system('false')",
            "inputs['probe_backlog']",
            "always(1)",
        ):
            with self.subTest(expression=expression):
                self.assertIsNone(
                    ci_lane_inventory.condition_outcome(expression, "schedule", {})
                )
        self.assertTrue(
            ci_lane_inventory.condition_outcome("'it''s' == 'IT''S'", "schedule", {})
        )
        with self.assertRaises(ValueError):
            ci_lane_inventory.condition_outcome("true", "schedule", {"env.secret": "a"})

    def test_event_only_inventory_keeps_schedule_input_and_status_context_unknown(self):
        self.assertIsNone(
            ci_lane_inventory.condition_outcome(self.condition, "schedule")
        )
        self.assertIsNone(ci_lane_inventory.condition_outcome("always()", "schedule"))
        self.assertTrue(
            ci_lane_inventory.condition_outcome(
                "github.event_name == 'SCHEDULE'", "schedule"
            )
        )

    def test_required_input_without_default_is_unknown_and_routes_are_not_exhaustive(
        self,
    ):
        definition = self.document["on"]["workflow_dispatch"]["inputs"]
        definition["probe_backlog"].pop("default")
        definition["other"] = {"type": "string", "required": "true"}
        routes = self.routes()
        self.assertNotIn(
            "inputs.probe_backlog", routes["workflow_dispatch:defaults"]["context"]
        )
        self.assertIsNone(self.outcomes(routes["workflow_dispatch:defaults"])["test"])
        self.assertNotIn(
            "inputs.other", routes["workflow_dispatch:defaults"]["context"]
        )
        self.assertIn("workflow_dispatch:inputs.probe_backlog=false", routes)
        self.assertIn("workflow_dispatch:inputs.probe_backlog=true", routes)
