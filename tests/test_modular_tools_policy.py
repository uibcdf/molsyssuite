from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

import tomllib

from devtools.scripts import bootstrap_component, check_component_guide
from tests.test_agent_instructions import NESTED_ROUTE, ROOT_ROUTE

ROOT = Path(__file__).resolve().parents[1]
ROUTE = "MOLSYSSUITE_GUIDE.md#modular-reusable-tools"
INSTRUCTION = (
    "## Modular reusable tools\n\n"
    "Before adding a feature, inspect existing tools and identify their owner.\n"
    f"Follow [{ROUTE}]({ROUTE}) for the required reusable tool contract.\n"
)


class ModularToolsPolicyTests(unittest.TestCase):
    def findings(self, instruction: str, guide: bytes | None = None):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "AGENTS.md").write_text(
                instruction + "\n" + ROOT_ROUTE, encoding="utf-8"
            )
            (root / "devguide").mkdir()
            (root / "devguide/AGENTS.md").write_text(NESTED_ROUTE)
            (root / "devguide/reporting_protocol.md").write_text("Local lifecycle")
            (root / "MOLSYSSUITE_GUIDE.md").write_bytes(
                (ROOT / "MOLSYSSUITE_GUIDE.md").read_bytes() if guide is None else guide
            )
            return {
                finding.code
                for finding in check_component_guide.check(root, "uibcdf/topomt")
            }

    def test_missing_explicit_instruction_is_rejected(self):
        self.assertIn(
            "MODULAR_TOOLS_ROUTE",
            self.findings("Read MOLSYSSUITE_GUIDE.md before development.\n"),
        )

    def test_route_in_another_section_is_not_explicit_tool_instruction(self):
        text = f"## Links\n\n{ROUTE}\n\n## Modular reusable tools\n\nSee above.\n"
        self.assertIn("MODULAR_TOOLS_ROUTE", self.findings(text))

    def test_commented_out_instruction_is_rejected(self):
        self.assertIn("MODULAR_TOOLS_ROUTE", self.findings(f"<!--\n{INSTRUCTION}-->"))

    def test_code_example_is_not_an_active_instruction(self):
        self.assertIn(
            "MODULAR_TOOLS_ROUTE", self.findings(f"```markdown\n{INSTRUCTION}```\n")
        )

    def test_explicit_instruction_and_current_guide_pass(self):
        self.assertEqual(self.findings(INSTRUCTION), set())

    def test_stale_guide_still_fails_with_valid_instruction(self):
        self.assertIn("GUIDE_DRIFT", self.findings(INSTRUCTION, b"outdated guide\n"))

    def test_unregistered_repository_cannot_claim_instruction_adoption(self):
        findings = check_component_guide.check(ROOT, "uibcdf/unregistered")
        self.assertEqual([finding.code for finding in findings], ["UNREGISTERED"])

    @mock.patch.object(
        bootstrap_component,
        "_published_policy",
        side_effect=lambda release: (
            bootstrap_component.suite_policy.load_effective_registry()
        ),
    )
    def test_generated_component_has_instruction_without_runtime_dependencies(
        self, _published_policy
    ):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "topomt"
            bootstrap_component.bootstrap(
                target, "uibcdf/topomt", "Molecular topography"
            )
            findings = check_component_guide.check(target, "uibcdf/topomt")
            instructions = (target / "AGENTS.md").read_text(encoding="utf-8")
            project = tomllib.loads((target / "pyproject.toml").read_text())
        self.assertEqual(findings, [])
        self.assertIn("## Modular reusable tools", instructions)
        self.assertIn(ROUTE, instructions)
        self.assertEqual(project["project"].get("dependencies", []), [])

    def test_registered_policy_has_applicability_and_exception_contract(self):
        policy = tomllib.loads((ROOT / "suite.toml").read_text())["policies"]
        rule = policy["modular-reusable-tools"]
        self.assertEqual(rule["applies-to"], ["repository"])
        self.assertEqual(rule["issue"], "uibcdf/molsyssuite#61")
        text = (ROOT / rule["normative"]).read_text()
        self.assertIn("## Exceptions", text)
        self.assertIn("## Evidence and verification", text)


if __name__ == "__main__":
    unittest.main()
