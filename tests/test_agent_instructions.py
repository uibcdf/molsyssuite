from __future__ import annotations

import copy
import subprocess
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest import mock

import tomllib

from devtools.scripts import (
    agent_instructions,
    bootstrap_component,
    check_component_guide,
)

ROOT = Path(__file__).resolve().parents[1]
ROOT_ROUTE = agent_instructions.render_entry()
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
            ROOT_ROUTE.replace(agent_instructions.ENTRY_HEADING, "## Background")
        )
        self.assertIn("INSTRUCTION_ROOT_ROUTE", self.codes())

    def test_required_reading_and_scoped_precedence_cannot_be_optional_or_negated(self):
        for original, replacement, code in (
            (
                agent_instructions.READ_REQUIREMENT,
                "Reading the guide is optional.",
                "INSTRUCTION_REQUIRED_GUIDE",
            ),
            (
                agent_instructions.READ_REQUIREMENT,
                "Do not " + agent_instructions.READ_REQUIREMENT,
                "INSTRUCTION_REQUIRED_GUIDE",
            ),
            ("take precedence over", "are subordinate to", "INSTRUCTION_PRECEDENCE"),
            ("Within their stated scope, ", "", "INSTRUCTION_PRECEDENCE"),
            (
                "require the documented policy exception process.",
                "require no exception.",
                "INSTRUCTION_PRECEDENCE",
            ),
        ):
            with self.subTest(replacement=replacement):
                (self.root / "AGENTS.md").write_text(
                    ROOT_ROUTE.replace(original, replacement)
                )
                self.assertIn(code, self.codes())

    def test_local_section_cannot_precede_the_mandatory_entry(self):
        (self.root / "AGENTS.md").write_text(
            "## Local defaults\n\nRead these first.\n\n" + ROOT_ROUTE
        )
        self.assertIn("INSTRUCTION_REQUIRED_GUIDE", self.codes())

    def test_reflowed_notice_preserves_its_contract(self):
        (self.root / "AGENTS.md").write_text(
            ROOT_ROUTE.replace("this file\nand any", "this file and\nany")
        )
        self.assertEqual(self.codes(), set())

    def test_common_guide_covers_each_accepted_policy_and_rejects_a_hidden_route(self):
        text = (ROOT / "MOLSYSSUITE_GUIDE.md").read_text()
        self.assertEqual(
            agent_instructions.common_policy_findings(self.policy, text), []
        )
        changed = copy.deepcopy(self.policy)
        changed["policies"]["new-boundary"] = {
            "status": "accepted",
            "normative": "devguide/new_boundary.md",
        }
        url = "https://github.com/uibcdf/molsyssuite/blob/main/devguide/new_boundary.md"
        for candidate in (
            text,
            text + f"\n<!-- {url} -->",
            text + f"\n```\n{url}\n```",
        ):
            self.assertIn(
                "COMMON_POLICY_ROUTE",
                {
                    f.code
                    for f in agent_instructions.common_policy_findings(
                        changed, candidate
                    )
                },
            )
        self.assertEqual(
            agent_instructions.common_policy_findings(changed, text + "\n" + url), []
        )

    def test_public_receipt_binds_committed_inputs_and_rejects_uncommitted_changes(
        self,
    ):
        for args in (
            ("init", "-q"),
            ("add", "."),
            (
                "-c",
                "user.name=Test",
                "-c",
                "user.email=test@example.org",
                "commit",
                "-qm",
                "Fixture",
            ),
        ):
            subprocess.run(
                ["git", "-C", str(self.root), *args], capture_output=True, check=True
            )
        result = check_component_guide.receipt(self.root, "uibcdf/topomt", [])
        self.assertEqual(result["state"], "verified")
        self.assertEqual(len(result["inputs"]), 3)
        self.assertEqual(len(result["source_commit"]), 40)
        self.assertNotIn(str(self.root), str(result))
        self.assertNotIn("Read and follow", str(result))
        (self.root / "AGENTS.md").write_text(ROOT_ROUTE + "\nPrivate local draft")
        failed = check_component_guide.receipt(self.root, "uibcdf/topomt", [])
        self.assertEqual(failed["state"], "failure")
        self.assertIn("UNCOMMITTED_INPUT", failed["finding_codes"])
        self.assertNotIn("Private local draft", str(failed))

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

    @mock.patch.object(
        bootstrap_component,
        "_published_policy",
        side_effect=lambda release: (
            bootstrap_component.suite_policy.load_effective_registry()
        ),
    )
    def test_generated_repository_and_audit_use_same_checker(self, _published_policy):
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
