"""Explicit cancellation facts describe predicates, never executed CI."""

from __future__ import annotations

import copy
import unittest

from devtools.scripts import ci_lane_inventory as inventory


class CICancellationTests(unittest.TestCase):
    def test_explicit_boolean_is_independent_of_event_and_context_mode(self):
        for event in ("push", "pull_request", "workflow_dispatch", "schedule"):
            for context in (None, {}):
                for cancelled in (False, True):
                    with self.subTest(
                        event=event, context=context, cancelled=cancelled
                    ):
                        self.assertIs(
                            inventory.condition_outcome(
                                "cancelled()", event, context, cancelled=cancelled
                            ),
                            cancelled,
                        )
                        self.assertIs(
                            inventory.condition_outcome(
                                "${{ !cancelled() }}",
                                event,
                                context,
                                cancelled=cancelled,
                            ),
                            not cancelled,
                        )
                        self.assertTrue(
                            inventory.condition_outcome(
                                "always()", event, {}, cancelled=cancelled
                            )
                        )
                        self.assertTrue(
                            inventory.condition_outcome(
                                "always()", event, cancelled=cancelled
                            )
                        )

    def test_missing_fact_is_not_inferred_from_event_or_dependency_result(self):
        for event in ("push", "pull_request", "workflow_dispatch", "schedule"):
            for context in (None, {}, {"needs.backlog.result": "cancelled"}):
                for expression in ("cancelled()", "!cancelled()"):
                    with self.subTest(
                        event=event, context=context, expression=expression
                    ):
                        self.assertIsNone(
                            inventory.condition_outcome(expression, event, context)
                        )
        # Preserve the historical explicit-predicate/default-context contract.
        self.assertIsNone(inventory.condition_outcome("always()", "push"))
        self.assertTrue(inventory.condition_outcome("always()", "push", {}))

    def test_three_valued_predicates_preserve_known_short_circuits(self):
        cases = [
            ("cancelled() && inputs.missing", False, False),
            ("cancelled() && inputs.missing", True, None),
            ("!cancelled() || inputs.missing", False, True),
            ("!cancelled() || inputs.missing", True, None),
            ("cancelled() && false", None, False),
            ("!cancelled() || true", None, True),
            ("cancelled() == true", False, False),
            ("cancelled() == true", True, True),
        ]
        for expression, cancelled, expected in cases:
            with self.subTest(expression=expression, cancelled=cancelled):
                self.assertIs(
                    inventory.condition_outcome(
                        expression, "workflow_dispatch", {}, cancelled=cancelled
                    ),
                    expected,
                )
        condition = (
            "!cancelled() && (needs.backlog.result != 'success' || "
            "needs.backlog.outputs.run_full == 'true')"
        )
        for cancelled, context, expected in (
            (True, {}, False),
            (False, {}, None),
            (False, {"needs.backlog.result": "failure"}, True),
            (False, {"needs.backlog.result": "success"}, None),
            (
                False,
                {
                    "needs.backlog.result": "success",
                    "needs.backlog.outputs.run_full": "false",
                },
                False,
            ),
            (
                False,
                {
                    "needs.backlog.result": "success",
                    "needs.backlog.outputs.run_full": "true",
                },
                True,
            ),
        ):
            with self.subTest(cancelled=cancelled, context=context):
                self.assertIs(
                    inventory.condition_outcome(
                        condition, "schedule", context, cancelled=cancelled
                    ),
                    expected,
                )

    def test_malformed_calls_and_unsupported_status_functions_stay_unknown(self):
        for expression in (
            "cancelled(true)",
            "cancelled(flag=true)",
            "cancelled(*inputs.flags)",
            "github.cancelled()",
            "failure()",
            "success()",
            "__import__('os').system('false')",
        ):
            with self.subTest(expression=expression):
                self.assertIsNone(
                    inventory.condition_outcome(expression, "push", {}, cancelled=True)
                )

    def test_invalid_facts_are_refused_even_without_an_expression_or_route(self):
        for value in (0, 1, "true", "false", "", [], {}):
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, "cancelled"):
                    inventory.condition_outcome(None, "push", cancelled=value)
                with self.assertRaisesRegex(ValueError, "cancelled"):
                    inventory.scenario_matrix(None, "push", {}, cancelled=value)
                with self.assertRaisesRegex(ValueError, "cancelled"):
                    inventory.inspect_event_routes({}, "test", cancelled=value)

    def matrix(self):
        return {
            "python": '${{ fromJSON(!cancelled() && \'["3.13","3.14"]\' || \'["3.14"]\') }}'
        }

    def test_matrix_selection_keeps_unknown_operands_and_invalid_calls_unresolved(self):
        for cancelled, expected in (
            (False, [{"python": "3.13"}, {"python": "3.14"}]),
            (True, [{"python": "3.14"}]),
        ):
            with self.subTest(cancelled=cancelled):
                self.assertEqual(
                    inventory.scenario_matrix(
                        self.matrix(), "workflow_dispatch", {}, cancelled=cancelled
                    ),
                    {"status": "resolved", "combinations": expected},
                )
        self.assertEqual(
            inventory.scenario_matrix(self.matrix(), "workflow_dispatch", {}),
            {"status": "unresolved", "combinations": []},
        )
        self.assertEqual(
            inventory.scenario_matrix(
                {"axis": "${{ fromJSON(false && cancelled() || '[2]') }}"},
                "workflow_dispatch",
                {},
            ),
            {"status": "unresolved", "combinations": []},
        )
        for payload in (
            "cancelled(true) && '[1]' || '[2]'",
            "false && failure() || '[2]'",
            "cancelled() || '[2]'",
        ):
            with self.subTest(payload=payload):
                self.assertEqual(
                    inventory.scenario_matrix(
                        {"axis": "${{ fromJSON(" + payload + ") }}"},
                        "workflow_dispatch",
                        {},
                        cancelled=True,
                    ),
                    {"status": "unresolved", "combinations": []},
                )

    def test_routes_propagate_explicit_facts_without_upgrading_execution(self):
        document = {
            "on": {"schedule": [{"cron": "0 9 * * MON"}], "workflow_dispatch": {}},
            "jobs": {
                "backlog": {"if": "always()", "steps": []},
                "test": {
                    "if": "!cancelled()",
                    "needs": "backlog",
                    "strategy": {"matrix": self.matrix()},
                    "steps": [{"if": "!cancelled()", "run": "pytest tests"}],
                },
            },
        }
        before = copy.deepcopy(document)
        default = inventory.inspect_event_routes(document, "test")
        self.assertEqual(len(default), 2)
        for row in default:
            self.assertNotIn("cancelled", row)
            self.assertIsNone(row["jobs"][0]["condition_outcome"])
            self.assertEqual(row["jobs"][0]["matrix"]["status"], "unresolved")
        for cancelled in (False, True):
            for row in inventory.inspect_event_routes(
                document, "test", cancelled=cancelled
            ):
                self.assertIs(row["cancelled"], cancelled)
                self.assertEqual(row["execution_evidence"], "not_requested")
                self.assertEqual(row["dependency_status"], "not_evaluated")
                test, backlog = row["jobs"]
                self.assertIs(test["condition_outcome"], not cancelled)
                self.assertIs(test["test_steps"][0]["condition_outcome"], not cancelled)
                self.assertEqual(
                    len(test["matrix"]["combinations"]), 1 if cancelled else 2
                )
                self.assertIs(backlog["condition_outcome"], True)
        self.assertEqual(document, before)
