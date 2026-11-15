"""Causal guards for latest adoption, actual callers and frozen compatibility."""

from __future__ import annotations

import copy
import io
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from devtools.scripts import (
    adoption_status,
    bootstrap_component,
    check_repository,
    suite_policy,
)


class LatestPolicyAdoptionTests(unittest.TestCase):
    def test_starter_rejects_newer_remote_target_before_generation(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "not-created"
            with (
                patch.object(
                    sys,
                    "argv",
                    [
                        "bootstrap",
                        str(destination),
                        "--repository",
                        "uibcdf/consumer",
                        "--description",
                        "Fixture",
                    ],
                ),
                patch.object(
                    suite_policy, "load_effective_registry", return_value=self.policy()
                ),
                patch.object(
                    suite_policy,
                    "published_policy_target",
                    return_value={"release": "policy-v9.2.0"},
                ),
                patch.object(bootstrap_component, "bootstrap") as generate,
                redirect_stdout(io.StringIO()),
            ):
                self.assertEqual(bootstrap_component.main(), 2)
                generate.assert_not_called()
                self.assertFalse(destination.exists())

    def test_live_audit_rejects_target_mismatch_instead_of_observing_an_old_target(
        self,
    ):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.workspace(Path(temporary), self.caller("policy-v9.1.0"))
            receipt = root / "evidence.json"
            with (
                patch.object(
                    sys,
                    "argv",
                    [
                        "audit",
                        str(root),
                        "--kind",
                        "policy",
                        "--check",
                        "--verify-published-policy",
                        "--receipt",
                        str(receipt),
                    ],
                ),
                patch.object(
                    adoption_status, "_load_policy", return_value=self.policy()
                ),
                patch.object(
                    suite_policy,
                    "published_policy_target",
                    return_value={"release": "policy-v9.2.0"},
                ),
                patch.object(adoption_status, "inventory") as observe,
                redirect_stdout(io.StringIO()),
            ):
                self.assertEqual(adoption_status.main(), 2)
                observe.assert_not_called()
                evidence = json.loads(receipt.read_text())
                self.assertEqual(evidence["status"], "target-unavailable")
                self.assertEqual(evidence["records"], [])
                self.assertEqual(
                    evidence["published_target"]["release"], "policy-v9.2.0"
                )

    def test_live_adoption_gate_is_independent_of_policy_definition_qualification(self):
        import yaml

        workflows = suite_policy.ROOT / ".github/workflows"
        audit = yaml.load(
            (workflows / "audit-policy-adoption.yaml").read_text(),
            Loader=yaml.BaseLoader,
        )
        checks = [s for s in audit["jobs"]["adoption"]["steps"] if "run" in s]
        gate = next(s for s in checks if "adoption_status.py" in s["run"])
        self.assertIn("--verify-published-policy --check", gate["run"])
        self.assertNotIn("continue-on-error", gate)
        self.assertIn("--receipt", gate["run"])
        # A policy snapshot can be qualified before its consumers migrate to it.
        definition = (workflows / "check-vendored-guides.yaml").read_text()
        self.assertNotIn("--verify-published-policy", definition)
        self.assertNotIn("adoption_status.py\n          workspace --check", definition)

    def policy(self):
        return {
            "governance": {
                "repository": "uibcdf/molsyssuite",
                "policy-release": "policy-v9.1.0",
                "compatible-policy-releases": ["policy-v9.0.0"],
            },
            "policies": {
                "adoption-lifecycle": {
                    "require-latest-policy": True,
                    "include-central": True,
                },
                "release-version": {"required-policy-release": "policy-v9.0.0"},
                "python": {"transition": {"components": []}},
            },
            "members": [
                {
                    "name": "consumer",
                    "repository": "uibcdf/consumer",
                    "capabilities": ["python-package"],
                }
            ],
            "guides": [],
        }

    def caller(self, release):
        return f"jobs:\n  policy:\n    uses: {suite_policy.POLICY_CALLER_PREFIX}{release}\n"

    def workspace(self, root, text):
        consumer = root / "consumer" / ".github" / "workflows"
        consumer.mkdir(parents=True)
        (consumer / "policy.yml").write_text(text)
        central = root / "molsyssuite"
        central.mkdir()
        (central / "suite.toml").write_text(
            '[governance]\npolicy-release="policy-v9.1.0"\n'
            "[policies.adoption-lifecycle]\nrequire-latest-policy=true\n"
        )
        return root

    def cli(self, root, policy):
        with (
            patch.object(adoption_status, "_load_policy", return_value=policy),
            patch.object(
                sys,
                "argv",
                [
                    "adoption_status",
                    str(root),
                    "--kind",
                    "policy",
                    "--repository",
                    "consumer",
                    "--check",
                ],
            ),
            redirect_stdout(io.StringIO()),
        ):
            return adoption_status.main()

    def test_compatible_caller_is_not_latest_adoption_but_frozen_mode_remains(self):
        policy = self.policy()
        with tempfile.TemporaryDirectory() as temporary:
            root = self.workspace(Path(temporary), self.caller("policy-v9.0.0"))
            self.assertEqual(self.cli(root, policy), 1)
            record = next(
                r
                for r in adoption_status.inventory(root, policy=policy)
                if r.repository == "uibcdf/consumer"
            )
            self.assertEqual(record.state, "compatible")
            self.assertIn("policy-v9.1.0", record.next_action)
            frozen = copy.deepcopy(policy)
            frozen["policies"].pop("adoption-lifecycle")
            self.assertEqual(self.cli(root, frozen), 0)

    def test_comment_latest_and_mixed_calls_cannot_manufacture_current_adoption(self):
        policy = self.policy()
        old = self.caller("policy-v9.0.0")
        examples = [
            old + "# " + suite_policy.POLICY_CALLER_PREFIX + "policy-v9.1.0\n",
            old
            + "  another:\n    uses: "
            + suite_policy.POLICY_CALLER_PREFIX
            + "policy-v9.1.0\n",
            "# " + suite_policy.POLICY_CALLER_PREFIX + "policy-v9.1.0\n",
        ]
        for text in examples:
            with self.subTest(text=text), tempfile.TemporaryDirectory() as temporary:
                root = self.workspace(Path(temporary), text)
                self.assertEqual(self.cli(root, policy), 1)
        with tempfile.TemporaryDirectory() as temporary:
            root = self.workspace(Path(temporary), self.caller("policy-v9.1.0"))
            self.assertEqual(self.cli(root, policy), 0)

    def test_non_python_member_and_central_are_both_inventoried(self):
        policy = self.policy()
        policy["members"][0]["capabilities"] = []
        with tempfile.TemporaryDirectory() as temporary:
            root = self.workspace(Path(temporary), self.caller("policy-v9.1.0"))
            rows = [
                r
                for r in adoption_status.inventory(root, policy=policy)
                if r.kind == "policy"
            ]
            self.assertEqual(
                {r.repository for r in rows}, {"uibcdf/consumer", "uibcdf/molsyssuite"}
            )
            self.assertTrue(all(r.state == "current" for r in rows))
            (root / "molsyssuite/suite.toml").write_text(
                '[governance]\npolicy-release="policy-v9.0.0"\n'
            )
            central = next(
                r
                for r in adoption_status.inventory(root, policy=policy)
                if r.repository == "uibcdf/molsyssuite"
            )
            self.assertEqual(central.state, "stale")

    def test_complete_unexpired_exception_is_explicit_and_expired_one_fails(self):
        policy = self.policy()
        exception = {
            "kind": "policy",
            "repository": "uibcdf/consumer",
            "item": "policy-caller",
            "issue": "uibcdf/consumer#2",
            "reason": "Selected route migration pending.",
            "expires-on": "2099-01-01",
            "removal-condition": "Publish the current caller and receive its gate.",
        }
        with tempfile.TemporaryDirectory() as temporary:
            root = self.workspace(Path(temporary), self.caller("policy-v9.0.0"))
            policy["adoption-exceptions"] = [exception]
            self.assertEqual(self.cli(root, policy), 0)
            record = next(
                r
                for r in adoption_status.inventory(root, policy=policy)
                if r.repository == "uibcdf/consumer"
            )
            self.assertEqual(record.state, "excepted")
            exception["expires-on"] = "2000-01-01"
            self.assertEqual(self.cli(root, policy), 1)
            exception["expires-on"] = "2099-01-01"
            exception["reason"] = ""
            self.assertEqual(self.cli(root, policy), 1)

    def test_yaml_ambiguity_is_unavailable_and_backups_are_ignored(self):
        policy = self.policy()
        for text in ["jobs: [", "jobs: {}\njobs: {}\n"]:
            with self.subTest(text=text), tempfile.TemporaryDirectory() as temporary:
                root = self.workspace(Path(temporary), text)
                record = next(
                    r
                    for r in adoption_status.inventory(root, policy=policy)
                    if r.repository == "uibcdf/consumer"
                )
                self.assertEqual(record.state, "unavailable")
                self.assertEqual(self.cli(root, policy), 1)
        with tempfile.TemporaryDirectory() as temporary:
            root = self.workspace(Path(temporary), self.caller("policy-v9.1.0"))
            backup = root / "consumer/.github/workflows/backups"
            backup.mkdir()
            (backup / "old.yml").write_text(self.caller("policy-v9.0.0"))
            self.assertEqual(self.cli(root, policy), 0)

    def test_current_checker_enforces_the_rule_for_non_python_members(self):
        policy = self.policy()
        policy["members"][0]["capabilities"] = []
        with tempfile.TemporaryDirectory() as temporary:
            root = self.workspace(Path(temporary), self.caller("policy-v9.0.0"))
            with (
                patch.object(check_repository, "_load_policy", return_value=policy),
                patch.object(
                    check_repository, "_component_guide_findings", return_value=[]
                ),
                patch.object(
                    check_repository, "_governance_pointer", return_value=True
                ),
                patch.object(
                    check_repository.repository_badges,
                    "validate_readme",
                    return_value=[],
                ),
            ):
                findings = check_repository.check(root / "consumer", "uibcdf/consumer")
            self.assertEqual([f.code for f in findings], ["LATEST_POLICY"])

    def test_remote_target_is_latest_numeric_tag_and_keeps_peeled_identity(self):
        text = (
            "a" * 40
            + "\trefs/tags/policy-v1.9.0\n"
            + "b" * 40
            + "\trefs/tags/policy-v1.10.0\n"
            + "c" * 40
            + "\trefs/tags/policy-v1.10.0^{}\n"
        )
        with patch.object(
            suite_policy.subprocess,
            "run",
            return_value=subprocess.CompletedProcess([], 0, text, ""),
        ):
            self.assertEqual(
                suite_policy.published_policy_target(),
                {"release": "policy-v1.10.0", "tag_sha": "b" * 40, "commit": "c" * 40},
            )
        for invalid in ["", "bad-sha\trefs/tags/policy-v1.0.0\n", text + text]:
            with (
                self.subTest(invalid=invalid),
                patch.object(
                    suite_policy.subprocess,
                    "run",
                    return_value=subprocess.CompletedProcess([], 0, invalid, ""),
                ),
                self.assertRaises(ValueError),
            ):
                suite_policy.published_policy_target()


if __name__ == "__main__":
    unittest.main()
