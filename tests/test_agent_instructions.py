from __future__ import annotations

import copy
import tempfile
import unittest
from datetime import date
from pathlib import Path

import tomllib

from devtools.scripts import (
    agent_instructions,
    bootstrap_component,
    check_component_guide,
)

ROOT = Path(__file__).resolve().parents[1]
ROOT_ROUTE = """## Durable working instructions

Follow MOLSYSSUITE_GUIDE.md#durable-working-instructions.
Read devguide/AGENTS.md for that directory.
"""
NESTED_ROUTE = "Read ../AGENTS.md and reporting_protocol.md. Follow ../MOLSYSSUITE_GUIDE.md#durable-working-instructions.\n"


class AgentInstructionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.policy = tomllib.loads((ROOT / "suite.toml").read_text())
        (self.root / "devguide").mkdir()
        (self.root / "AGENTS.md").write_text(ROOT_ROUTE)
        (self.root / "devguide/AGENTS.md").write_text(NESTED_ROUTE)
        (self.root / "devguide/reporting_protocol.md").write_text("Local lifecycle")
        (self.root / "MOLSYSSUITE_GUIDE.md").write_bytes(
            (ROOT / "MOLSYSSUITE_GUIDE.md").read_bytes()
        )

    def codes(self):
        return {
            f.code
            for f in agent_instructions.check(self.root, self.policy, "uibcdf/topomt")
        }

    def test_active_routes_and_local_layout_pass(self):
        self.assertEqual(self.codes(), set())

    def test_root_and_nested_missing_files_fail(self):
        for target in ("AGENTS.md", "devguide/AGENTS.md"):
            with self.subTest(target=target):
                path = self.root / target
                saved = path.read_text()
                path.unlink()
                self.assertIn("INSTRUCTION_FILE", self.codes())
                path.write_text(saved)

    def test_routes_in_examples_comments_and_quotes_fail(self):
        for wrapper in (
            "<!--\n{}\n-->",
            "````markdown\n{}\n```\n````",
            "~~~markdown\n{}\n~~~",
            "> {}",
            "    {}",
        ):
            with self.subTest(wrapper=wrapper):
                (self.root / "AGENTS.md").write_text(wrapper.format(ROOT_ROUTE))
                self.assertIn("INSTRUCTION_ROOT_ROUTE", self.codes())

    def test_root_route_in_unrelated_section_is_rejected(self):
        (self.root / "AGENTS.md").write_text(
            ROOT_ROUTE.replace("Durable working instructions", "Background")
        )
        self.assertIn("INSTRUCTION_ROOT_ROUTE", self.codes())

    def test_missing_nested_route_and_real_target_fail(self):
        (self.root / "devguide/AGENTS.md").write_text(
            NESTED_ROUTE.replace("reporting_protocol.md", "other.md")
        )
        self.assertIn("INSTRUCTION_NESTED_ROUTE", self.codes())
        (self.root / "devguide/AGENTS.md").write_text(NESTED_ROUTE)
        (self.root / "devguide/reporting_protocol.md").unlink()
        self.assertIn("INSTRUCTION_TARGET", self.codes())

    def test_unknown_repository_cannot_claim_adoption(self):
        findings = agent_instructions.check(self.root, self.policy, "uibcdf/unknown")
        self.assertEqual([f.code for f in findings], ["UNREGISTERED"])

    def test_complete_exception_is_bounded_and_expired_exception_fails(self):
        entry = {
            "repository": "uibcdf/topomt",
            "issue": "uibcdf/topomt#56",
            "owner": "maintainers",
            "reason": "scoped migration",
            "removal-condition": "adopt routes",
            "expires-on": "2026-12-31",
        }
        policy = copy.deepcopy(self.policy)
        policy["working-instruction-exceptions"] = [entry]
        self.assertEqual(
            agent_instructions.validate_exceptions(policy, date(2026, 10, 1)), []
        )
        self.assertTrue(
            agent_instructions.validate_exceptions(policy, date(2027, 1, 1))
        )
        for key in ("owner", "reason", "removal-condition", "issue", "expires-on"):
            with self.subTest(key=key):
                altered = copy.deepcopy(policy)
                del altered["working-instruction-exceptions"][0][key]
                self.assertTrue(
                    agent_instructions.validate_exceptions(altered, date(2026, 10, 1))
                )

    def test_duplicate_unknown_and_foreign_owner_exceptions_fail(self):
        entry = {
            "repository": "uibcdf/topomt",
            "issue": "uibcdf/molsyssuite#66",
            "owner": "maintainers",
            "reason": "migration",
            "removal-condition": "adopt routes",
            "expires-on": "2026-12-31",
        }
        for entries in (
            [entry, entry],
            [dict(entry, repository="uibcdf/unknown")],
            [dict(entry, issue="uibcdf/molsysmt#195")],
        ):
            policy = dict(self.policy, **{"working-instruction-exceptions": entries})
            self.assertTrue(
                agent_instructions.validate_exceptions(policy, date(2026, 10, 1))
            )

    def test_generated_repository_and_audit_use_same_checker(self):
        target = self.root / "generated"
        bootstrap_component.bootstrap(target, "uibcdf/topomt", "Topography")
        self.assertEqual(check_component_guide.check(target, "uibcdf/topomt"), [])
        (target / "devguide/AGENTS.md").unlink()
        self.assertIn(
            "INSTRUCTION_FILE",
            {f.code for f in check_component_guide.check(target, "uibcdf/topomt")},
        )

    def test_policy_applicability_and_exception_mechanism_are_registered(self):
        rule = self.policy["policies"]["working-instructions"]
        self.assertEqual(rule["issue"], "uibcdf/molsyssuite#66")
        self.assertEqual(rule["applies-to"], ["repository"])
        text = (ROOT / rule["normative"]).read_text()
        self.assertIn("## Exceptions", text)
        self.assertIn("uibcdf/molsyssuite#65", text)


if __name__ == "__main__":
    unittest.main()
