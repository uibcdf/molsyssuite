"""Guard the pinned platform-policy inheritance contract."""

from __future__ import annotations

import copy
import unittest
from pathlib import Path

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
        with self.assertRaisesRegex(ValueError, "must be at"):
            moli_policy.effective_registry(local)

    def test_duplicated_platform_value_is_rejected(self):
        local = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
        local = copy.deepcopy(local)
        local["policies"]["python-quality"]["ruff-version"] = "0.16.5"
        with self.assertRaisesRegex(ValueError, "duplicates a MOLI value"):
            moli_policy.effective_registry(local)


if __name__ == "__main__":
    unittest.main()
