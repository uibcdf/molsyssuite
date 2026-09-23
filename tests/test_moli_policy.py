"""Guard the pinned platform-policy inheritance contract."""

from __future__ import annotations

import copy
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import tomllib

from devtools.scripts import moli_policy

ROOT = Path(__file__).resolve().parents[1]


class MoliPolicyTests(unittest.TestCase):
    def test_effective_registry_inherits_values_without_local_copies(self):
        local = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
        effective = moli_policy.effective_registry(local)
        self.assertNotIn("ruff-version", local["policies"]["python-quality"])
        self.assertEqual(
            effective["policies"]["python-quality"]["ruff-version"], "0.16.5"
        )
        self.assertEqual(
            effective["policies"]["python"]["requires-python"], ">=3.11,<3.14"
        )

    def test_wrong_moli_revision_is_rejected(self):
        local = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
        local["governance"]["platform-policy-ref"] = "0" * 40
        with self.assertRaisesRegex(ValueError, "does not contain pinned commit"):
            moli_policy.effective_registry(local)

    def test_duplicated_platform_value_is_rejected(self):
        local = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
        local = copy.deepcopy(local)
        local["policies"]["python-quality"]["ruff-version"] = "0.16.5"
        with self.assertRaisesRegex(ValueError, "duplicates a MOLI value"):
            moli_policy.effective_registry(local)

    def test_newer_worktree_uses_the_pinned_commit(self):
        local = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
        reference = local["governance"]["platform-policy-ref"]
        committed = subprocess.check_output(
            [
                "git",
                "-C",
                str(moli_policy._moli_root()),
                "show",
                f"{reference}:moli.toml",
            ]
        )
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / "moli.toml").write_bytes(committed)
            subprocess.run(["git", "-C", str(root), "add", "moli.toml"], check=True)
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(root),
                    "-c",
                    "user.name=Governance Test",
                    "-c",
                    "user.email=test@example.invalid",
                    "commit",
                    "-qm",
                    "pinned",
                ],
                check=True,
            )
            local["governance"]["platform-policy-ref"] = subprocess.check_output(
                ["git", "-C", str(root), "rev-parse", "HEAD"], text=True
            ).strip()
            (root / "moli.toml").write_text(
                'schema_version = "later"\n', encoding="utf-8"
            )
            subprocess.run(["git", "-C", str(root), "add", "moli.toml"], check=True)
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(root),
                    "-c",
                    "user.name=Governance Test",
                    "-c",
                    "user.email=test@example.invalid",
                    "commit",
                    "-qm",
                    "later",
                ],
                check=True,
            )
            with mock.patch.dict(os.environ, {"MOLI_POLICY_ROOT": str(root)}):
                effective = moli_policy.effective_registry(local)
        self.assertEqual(
            effective["policies"]["python-quality"]["ruff-version"], "0.16.5"
        )


if __name__ == "__main__":
    unittest.main()
