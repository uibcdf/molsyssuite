"""Guard MolSysSuite ownership of effective member engineering policy."""

from __future__ import annotations

import copy
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import tomllib

from devtools.scripts import bootstrap_component, check_repository, suite_policy

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
        self.assertEqual(local["policies"]["python"]["requires-python"], ">=3.11,<3.15")
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
            ["3.11", "3.12", "3.13", "3.14"],
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


class ImmutableAdmissionTests(unittest.TestCase):
    def setUp(self):
        self.current = suite_policy.load_effective_registry()
        self.frozen = copy.deepcopy(self.current)
        self.frozen["members"] = [
            r for r in self.frozen["members"] if r["name"] != "opencastp"
        ]
        self.frozen["policies"]["python"]["transition"]["components"] = [
            r
            for r in self.frozen["policies"]["python"]["transition"]["components"]
            if r["name"] != "opencastp"
        ]

    def test_admission_repairs_missing_member_without_importing_rules_or_exceptions(
        self,
    ):
        admitted = copy.deepcopy(self.current)
        admitted["policies"]["python-quality"]["ruff-version"] = "999.0.0"
        admitted["policies"]["python"]["requires-python"] = ">=99"
        admitted["policies"]["python"]["transition"]["components"].append(
            {
                "name": "opencastp",
                "state": "authorized",
                "compatible-policy-releases": ["main"],
            }
        )
        admitted["members"].append(
            {"name": "unrelated", "repository": "uibcdf/unrelated"}
        )
        result = suite_policy.apply_admission(self.frozen, admitted, "uibcdf/opencastp")
        self.assertEqual(result["policies"], self.frozen["policies"])
        self.assertEqual(result["guides"], self.frozen["guides"])
        self.assertEqual(
            {k: v for k, v in result.items() if k != "members"},
            {k: v for k, v in self.frozen.items() if k != "members"},
        )
        self.assertEqual(result["members"][:-1], self.frozen["members"])
        self.assertEqual(
            set(result["members"][-1]),
            {
                "name",
                "repository",
                "role",
                "membership",
                "maturity",
                "development-mode",
                "capabilities",
            },
        )
        self.assertEqual(len(result["members"]), len(self.frozen["members"]) + 1)
        self.assertIsNone(check_repository._member(self.frozen, "uibcdf/opencastp"))
        self.assertIsNotNone(check_repository._member(result, "uibcdf/opencastp"))

    def test_existing_registration_and_all_policy_bytes_remain_unchanged(self):
        admitted = copy.deepcopy(self.current)
        row = next(r for r in admitted["members"] if r["name"] == "opencastp")
        row.update(role="unknown-future-role", capabilities=[])
        self.assertEqual(
            suite_policy.apply_admission(self.current, admitted, "uibcdf/opencastp"),
            self.current,
        )

    def test_admission_rejects_missing_duplicate_conflicting_or_future_classifications(
        self,
    ):
        mutations = [
            lambda d: d.update(members=[]),
            lambda d: d["members"].append(
                copy.deepcopy(next(r for r in d["members"] if r["name"] == "opencastp"))
            ),
            lambda d: next(r for r in d["members"] if r["name"] == "opencastp").update(
                role="future-role"
            ),
            lambda d: next(r for r in d["members"] if r["name"] == "opencastp").update(
                capabilities=["python-package", "future-capability"]
            ),
            lambda d: next(r for r in d["members"] if r["name"] == "opencastp").update(
                name="smonitor"
            ),
        ]
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                admitted = copy.deepcopy(self.current)
                mutation(admitted)
                with self.assertRaises(ValueError):
                    suite_policy.apply_admission(
                        self.frozen, admitted, "uibcdf/opencastp"
                    )

    def test_commit_reader_rejects_mutable_refs_and_ignores_dirty_working_tree(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / "suite.toml").write_bytes((ROOT / "suite.toml").read_bytes())
            subprocess.run(["git", "-C", str(root), "add", "suite.toml"], check=True)
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(root),
                    "-c",
                    "user.name=Fixture",
                    "-c",
                    "user.email=fixture@example.test",
                    "commit",
                    "-qm",
                    "Admission fixture",
                ],
                check=True,
            )
            commit = subprocess.check_output(
                ["git", "-C", str(root), "rev-parse", "HEAD"], text=True
            ).strip()
            (root / "suite.toml").write_text("uncommitted invalid registry")
            registry = suite_policy.registry_at_commit(root, commit)
            self.assertEqual(registry["members"], self.current["members"])
            with self.assertRaises(ValueError):
                suite_policy.admission_at_commit(root, commit)
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(root),
                    "remote",
                    "add",
                    "origin",
                    "https://github.com/uibcdf/molsyssuite.git",
                ],
                check=True,
            )
            with self.assertRaises(ValueError):
                suite_policy.admission_at_commit(root, commit)
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(root),
                    "update-ref",
                    "refs/remotes/origin/main",
                    commit,
                ],
                check=True,
            )
            self.assertEqual(suite_policy.admission_at_commit(root, commit), registry)
            for ref in ("main", "HEAD", commit[:7], "0" * 40):
                with self.subTest(ref=ref), self.assertRaises(ValueError):
                    suite_policy.registry_at_commit(root, ref)

    def test_starter_refuses_unpublished_policy_and_missing_admission_before_writes(
        self,
    ):
        with self.assertRaises(ValueError):
            bootstrap_component._published_policy("policy-v9999.0.0")
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "component"
            with (
                mock.patch.object(
                    bootstrap_component, "_published_policy", return_value=self.frozen
                ),
                self.assertRaisesRegex(ValueError, "absent.*admission-sha"),
            ):
                bootstrap_component.bootstrap(
                    target, "uibcdf/opencastp", "Admission qualification"
                )
            self.assertFalse(target.exists())

    def test_generated_admitted_member_passes_frozen_checker_and_retains_sha_in_caller(
        self,
    ):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "component"
            with (
                mock.patch.object(
                    bootstrap_component, "_published_policy", return_value=self.frozen
                ),
                mock.patch.object(
                    suite_policy, "admission_at_commit", return_value=self.current
                ),
            ):
                bootstrap_component.bootstrap(
                    target,
                    "uibcdf/opencastp",
                    "Admission qualification",
                    admission_sha="a" * 40,
                )
                with mock.patch.object(
                    check_repository, "_load_policy", return_value=self.frozen
                ):
                    self.assertEqual(
                        [
                            f.code
                            for f in check_repository.check(target, "uibcdf/opencastp")
                        ],
                        ["UNREGISTERED"],
                    )
                    self.assertEqual(
                        check_repository.check(
                            target,
                            "uibcdf/opencastp",
                            admission_root=ROOT,
                            admission_sha="a" * 40,
                        ),
                        [],
                    )
            caller = (target / ".github/workflows/molsyssuite-policy.yml").read_text()
            self.assertIn("admission_sha: " + "a" * 40, caller)
            self.assertIn("@" + self.frozen["governance"]["policy-release"], caller)


if __name__ == "__main__":
    unittest.main()
