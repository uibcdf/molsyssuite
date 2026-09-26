"""Guard MolSysSuite ownership of effective member engineering policy."""

from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import tomllib

from devtools.scripts import suite_policy

ROOT = Path(__file__).resolve().parents[1]


class SuitePolicyTests(unittest.TestCase):
    def _registry(self):
        return tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))

    def test_member_values_are_owned_locally(self):
        local = self._registry()
        effective = suite_policy.effective_registry(local)
        self.assertEqual(
            local["governance"]["engineering-baseline-owner"], "uibcdf/molsyssuite"
        )
        self.assertEqual(local["policies"]["python-quality"]["ruff-version"], "0.16.5")
        self.assertEqual(local["policies"]["python"]["requires-python"], ">=3.11,<3.14")
        self.assertEqual(
            local["policies"]["python-ci"]["baseline-os"], ["linux", "macos"]
        )
        self.assertEqual(
            effective["policies"]["release-version"]["versioningit-pattern"],
            r"^(?P<version>(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*))$",
        )
        self.assertNotIn("versioningit-pattern", local["policies"]["release-version"])

    def test_moli_revision_does_not_change_member_values(self):
        local = self._registry()
        local["governance"]["platform-policy-ref"] = "0" * 40
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "suite.toml").write_bytes((ROOT / "suite.toml").read_bytes())
            with mock.patch.object(suite_policy, "ROOT", root):
                effective = suite_policy.load_effective_registry()
        self.assertEqual(
            effective["policies"]["python-quality"]["ruff-version"], "0.16.5"
        )
        self.assertEqual(
            suite_policy.effective_registry(local)["policies"]["python"]["ci-versions"],
            ["3.11", "3.12", "3.13"],
        )

    def test_missing_or_delegated_member_value_is_rejected(self):
        local = self._registry()
        missing = copy.deepcopy(local)
        del missing["policies"]["python-quality"]["ruff-version"]
        with self.assertRaisesRegex(ValueError, "lacks local values"):
            suite_policy.effective_registry(missing)
        delegated = copy.deepcopy(local)
        delegated["policies"]["python-quality"]["inheritance"] = "moli-baseline"
        with self.assertRaisesRegex(ValueError, "still delegates"):
            suite_policy.effective_registry(delegated)


if __name__ == "__main__":
    unittest.main()
