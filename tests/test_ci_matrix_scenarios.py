"""Bounded source matrix resolution never establishes execution or full debt relief."""

from __future__ import annotations

import copy
import json
import unittest
from unittest.mock import patch

from devtools.scripts import ci_lane_inventory as inventory


class CIMatrixScenarioTests(unittest.TestCase):
    def expression(self, value):
        # Actions escapes single quotes by doubling them, not by backslashes.
        return "${{ fromJSON('" + json.dumps(value).replace("'", "''") + "') }}"

    def setUp(self):
        self.full = [
            {"os": "ubuntu-latest", "python-version": minor}
            for minor in ("3.11", "3.12", "3.13", "3.14")
        ] + [{"os": "macos-15", "python-version": "3.14"}]
        self.single = [self.full[2]]
        self.branch = (
            "${{ fromJSON(github.event_name == 'workflow_dispatch' && "
            "inputs.python_313_only == true && '"
            + json.dumps(self.single)
            + "' || '"
            + json.dumps(self.full)
            + "') }}"
        )
        self.matrix = {"cfg": self.branch}

    def test_scheduled_default_and_manual_single_minor_have_distinct_cells(self):
        for event, context, expected in (
            ("schedule", {}, self.full),
            ("workflow_dispatch", {"inputs.python_313_only": False}, self.full),
            ("workflow_dispatch", {"inputs.python_313_only": True}, self.single),
        ):
            with self.subTest(event=event, context=context):
                result = inventory.scenario_matrix(self.matrix, event, context)
                self.assertEqual(result["status"], "resolved")
                self.assertEqual(result["combinations"], [{"cfg": x} for x in expected])
        # Event-only inventory cannot select a manual branch.
        self.assertEqual(inventory._expand_matrix(self.matrix), ([{}], "unresolved"))
        self.assertEqual(
            inventory.scenario_matrix(self.matrix, "workflow_dispatch", {}),
            {"status": "unresolved", "combinations": []},
        )

    def test_operand_values_truthiness_grouping_and_escaped_literals(self):
        for payload, expected in (
            ("false && '[1]' || '[2]'", [2]),
            ("true && '' || '[2]'", [2]),
            ("(true && '[1]') || '[2]'", [1]),
            ("!'nonempty' && '[1]' || '[2]'", [2]),
            ("'it''s' == 'IT''S' && '[1]' || '[2]'", [1]),
            ("inputs.flag == true && '[1]' || '[2]'", [1]),
        ):
            with self.subTest(payload=payload):
                result = inventory.scenario_matrix(
                    {"axis": "${{ fromJSON(" + payload + ") }}"},
                    "workflow_dispatch",
                    {"inputs.flag": "1"},
                )
                self.assertEqual(
                    result["combinations"], [{"axis": v} for v in expected]
                )
        result = inventory.scenario_matrix(
            {"axis": self.expression(["it's literal && inputs.flag"])}, "schedule", {}
        )
        self.assertEqual(
            result["combinations"], [{"axis": "it's literal && inputs.flag"}]
        )

    def test_whole_matrix_axes_and_include_exclude_share_static_semantics(self):
        matrix = {
            "python": ["3.13", "3.14"],
            "os": ["ubuntu-latest"],
            "exclude": [{"python": "3.13"}],
            "include": [{"os": "macos-15", "python": "3.14"}],
        }
        expected, status = inventory._expand_matrix(matrix)
        original = copy.deepcopy(matrix)
        for source in (matrix, self.expression(matrix)):
            result = inventory.scenario_matrix(source, "schedule", {})
            self.assertEqual(result["combinations"], expected)
            self.assertEqual(
                result["status"], "static" if source is matrix else "resolved"
            )
        self.assertEqual(status, "static")
        self.assertEqual(matrix, original)
        self.assertEqual(
            inventory.scenario_matrix(
                "${{ fromJSON(inputs.matrix_json) }}",
                "workflow_dispatch",
                {"inputs.matrix_json": json.dumps({"include": matrix["include"]})},
            ),
            {"status": "resolved", "combinations": matrix["include"]},
        )
        self.assertEqual(
            inventory.scenario_matrix(None, "schedule", {}),
            {"status": "none", "combinations": [{}]},
        )

    def test_unknown_runtime_unsupported_code_and_invalid_json_stay_unresolved(self):
        expressions = (
            "inputs.missing && '[1]' || '[2]'",
            "needs.producer.outputs.matrix",
            "contains('a', 'a') && '[1]' || '[2]'",
            "__import__('os').system('false')",
            "'[1]' + '[2]'",
            "true and '[1]' or '[2]'",
            "True && '[1]' || '[2]'",
            "false && always(true) || '[1]'",
            "'[1]' ''",
            '"[1]"',
            "'broken JSON'",
            '\'{"a": 1, "a": 2}\'',
            "'[NaN]'",
            "'[1e9999]'",
            "'[\"${{ secrets.VALUE }}\"]'",
            " || ".join(["false"] * 600 + ["'[1]'"]),
        )
        with patch("builtins.eval", side_effect=AssertionError("no eval")):
            for expression in expressions:
                with self.subTest(expression=expression):
                    self.assertEqual(
                        inventory.scenario_matrix(
                            {"axis": "${{ fromJSON(" + expression + ") }}"},
                            "workflow_dispatch",
                            {},
                        ),
                        {"status": "unresolved", "combinations": []},
                    )

    def test_inspection_limits_and_invalid_shapes_do_not_expand(self):
        deep = "value"
        for _ in range(20):
            deep = [deep]
        for matrix in (
            {"a": list(range(257))},
            {"a": list(range(17)), "b": list(range(17))},
            {"a": [1], "include": [{}] * 256},
            {"a": [1], "exclude": [1]},
            {"a": []},
            {"a": "${{ fromJSON('" + "x" * 32768 + "') }}"},
            {"a": self.expression(deep)},
            {"a": list(range(4097))},
            {str(n): [1] for n in range(23)},
            self.expression([1]),
        ):
            with self.subTest(shape=str(matrix)[:90]):
                self.assertEqual(
                    inventory.scenario_matrix(matrix, "schedule", {}),
                    {"status": "unresolved", "combinations": []},
                )
        self.assertEqual(
            len(
                inventory.scenario_matrix({"a": list(range(256))}, "schedule", {})[
                    "combinations"
                ]
            ),
            256,
        )

    def test_routes_keep_predicate_dependency_and_execution_separate(self):
        document = {
            "on": {
                "schedule": [{"cron": "0 9 * * MON"}],
                "workflow_dispatch": {
                    "inputs": {
                        "python_313_only": {"type": "boolean", "default": False},
                        "probe_backlog": {"type": "boolean", "default": False},
                    }
                },
            },
            "jobs": {
                "test": {
                    "if": "always() && inputs.probe_backlog != true && needs.decision.outputs.run_full == 'true'",
                    "needs": "decision",
                    "strategy": {"matrix": self.matrix},
                    "steps": [{"run": "pytest tests"}],
                },
                "decision": {"steps": [{"run": "python decide.py"}]},
            },
        }
        original = copy.deepcopy(document)
        routes = {
            r["scenario"]: r for r in inventory.inspect_event_routes(document, "test")
        }
        for scenario, route in routes.items():
            self.assertEqual(route["execution_evidence"], "not_requested")
            self.assertEqual(route["dependency_status"], "not_evaluated")
            test = route["jobs"][0]
            probe = "probe_backlog=true" in scenario
            self.assertIs(test["condition_outcome"], False if probe else None)
            expected = self.single if "python_313_only=true" in scenario else self.full
            self.assertEqual(
                test["matrix"]["combinations"], [{"cfg": x} for x in expected]
            )
        self.assertEqual(document, original)
