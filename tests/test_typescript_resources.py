"""Independent TypeScript and non-Python resource boundary regressions."""

from __future__ import annotations

import copy
import hashlib
import io
import json
import tarfile
import tempfile
import unittest
from pathlib import Path

from devtools.scripts import conda_release_contract as contract
from devtools.scripts import generic_resources, suite_policy, typescript_repository


def plan():
    return {
        "schema": "molsyssuite.conda-plan@1",
        "package": "tsfixture",
        "version": "1.2.3",
        "build_number": 0,
        "route": "staged",
        "profile": "generic-resources",
        "reason": "First independent resource surface.",
        "decision_by": "owner",
        "artifact_subdirs": ["noarch"],
        "test_platforms": ["linux-64"],
        "python_versions": [],
        "runtime_versions": ["node24"],
        "required_workflows": [".github/workflows/ci.yml"],
        "gate_jobs": {
            ".github/workflows/ci.yml": {"assets": ["Receive installed assets"]}
        },
        "requires_installed_gate": True,
        "new_compatibility_surface": True,
        "coupled_release": False,
        "dependencies_public": True,
    }


def payload():
    files = {
        "package.json": json.dumps(
            {
                "name": "@uibcdf/tsfixture",
                "version": "1.2.3",
                "license": "MIT",
                "type": "module",
                "exports": {
                    ".": {"import": "./dist/index.js", "types": "./dist/index.d.ts"}
                },
            }
        ).encode(),
        "LICENSE": b"MIT fixture notice",
        "dist/index.js": b"export const identity = 'fixture';",
        "dist/index.d.ts": b"export declare const identity: string;",
    }
    files["asset-manifest.json"] = json.dumps(
        {
            "schemaVersion": 1,
            "package": "tsfixture",
            "version": "1.2.3",
            "files": [
                {"path": k, "sha256": hashlib.sha256(v).hexdigest()}
                for k, v in files.items()
            ],
        }
    ).encode()
    return {"share/tsfixture/" + k: v for k, v in files.items()}


class TypeScriptResourceTests(unittest.TestCase):
    def test_generic_plan_uses_real_runtime_cells_without_fake_python(self):
        contract.validate_plan(plan())
        for changed in (
            {"python_versions": ["3.14"]},
            {"runtime_versions": []},
            {"gate_jobs": {}},
        ):
            with (
                self.subTest(changed=changed),
                self.assertRaises(contract.ContractError),
            ):
                contract.validate_plan({**plan(), **changed})

    def test_generic_transition_requires_real_runtime_and_exact_consumer_receipts(self):
        from tests.test_conda_release_contract import evidence

        decision = plan()
        decision.update(package="example", build_number=2)
        data = evidence(decision)
        name = "example-1.2.3-res_2.tar.bz2"
        data["inventory"][0]["filename"] = name
        data["public"]["files"][0]["filename"] = name
        workflow = decision["required_workflows"][0]
        data["gates"][0]["executed_jobs"] = {
            "schema": "molsyssuite.native-gate@1",
            "state": "verified",
            "candidate_sha": "a" * 40,
            "workflow": workflow,
            "run_id": 1,
            "run_attempt": 1,
            "jobs": [
                {
                    "name": "assets",
                    "job_id": 2,
                    "required_steps": ["Receive installed assets"],
                }
            ],
        }
        assets = {
            "schema": "molsyssuite.generic-resources@1",
            "state": "verified",
            "package": "example",
            "version": "1.2.3",
            "candidate_sha": "a" * 40,
            "artifact_sha256": "b" * 64,
            "resource_root": "share/example",
            "files": {"dist/index.js": "c" * 64},
            "consumer": "passed",
            "node_version": "24.22.1",
        }
        cell = {
            "platform": "linux-64",
            "runtime": "node24",
            "conclusion": "success",
            "candidate_sha": "a" * 40,
            "installed_inventory": data["inventory"],
            "asset_receipt": assets,
        }
        data["installed_cells"] = [cell]
        contract.validate_transition(decision, data)
        for change in (
            "missing",
            "duplicate",
            "wrong-runtime",
            "identity-only",
            "wrong-bytes",
        ):
            bad = copy.deepcopy(data)
            if change == "missing":
                bad["installed_cells"] = []
            elif change == "duplicate":
                bad["installed_cells"].append(copy.deepcopy(cell))
            elif change == "wrong-runtime":
                bad["installed_cells"][0]["runtime"] = "node25"
            elif change == "identity-only":
                bad["installed_cells"][0]["asset_receipt"].pop("consumer")
            else:
                bad["installed_cells"][0]["asset_receipt"]["artifact_sha256"] = "d" * 64
            with self.subTest(change=change), self.assertRaises(contract.ContractError):
                contract.validate_transition(decision, bad)
        direct = copy.deepcopy(decision)
        direct.update(
            route="direct",
            requires_installed_gate=False,
            new_compatibility_surface=False,
        )
        data["route"] = "direct"
        data["installed_cells"] = []
        with self.assertRaises(contract.ContractError):
            contract.validate_transition(direct, data)

    def test_generic_plan_never_weakens_existing_python_matrix(self):
        p = plan()
        p["profile"] = "noarch-python"
        with self.assertRaises(contract.ContractError):
            contract.validate_plan(p)

    def test_payload_binds_complete_assets_and_real_entries(self):
        r = generic_resources.inspect_payload(payload(), "tsfixture", "1.2.3")
        self.assertEqual(r["state"], "verified")
        mutations = [
            lambda f: f.pop("share/tsfixture/dist/index.d.ts"),
            lambda f: f.update({"share/tsfixture/dist/index.js": b"changed"}),
            lambda f: f.update({"share/tsfixture/unlisted.txt": b"unexpected"}),
            lambda f: f.update({"site-packages/hidden.py": b"x=1"}),
            lambda f: f.update({"share/tsfixture/native.dat": b"\x7fELFabc"}),
            lambda f: f.update({"share/tsfixture/../escape": b"x"}),
        ]
        for change in mutations:
            files = payload()
            change(files)
            with self.subTest(change=change), self.assertRaises(contract.ContractError):
                generic_resources.inspect_payload(files, "tsfixture", "1.2.3")
        with self.assertRaises(contract.ContractError):
            generic_resources.inspect_payload(payload(), "tsfixture", "1.2.4")

    def test_installed_prefix_refuses_aliases_and_retains_hashes_after_relocation(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name, data in payload().items():
                p = root / name
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(data)
            self.assertEqual(
                generic_resources.inspect_prefix(root, "tsfixture", "1.2.3")["state"],
                "verified",
            )
            p = root / "share/tsfixture/dist/index.js"
            p.unlink()
            p.symlink_to(root / "share/tsfixture/LICENSE")
            with self.assertRaises(contract.ContractError):
                generic_resources.inspect_prefix(root, "tsfixture", "1.2.3")

    def test_archive_refuses_wrong_noarch_type_and_duplicate_or_linked_paths(self):
        with tempfile.TemporaryDirectory() as temporary:
            p = Path(temporary) / "tsfixture-1.2.3-res_0.tar.bz2"
            index = {
                "name": "tsfixture",
                "version": "1.2.3",
                "build": "res_0",
                "build_number": 0,
                "subdir": "noarch",
                "noarch": "generic",
                "depends": [],
            }
            for mutation in (None, "python", "duplicate", "link"):
                files = {
                    **payload(),
                    "info/index.json": json.dumps(
                        {
                            **index,
                            "noarch": "python" if mutation == "python" else "generic",
                        }
                    ).encode(),
                }
                with tarfile.open(p, "w:bz2") as z:
                    for name, data in files.items():
                        m = tarfile.TarInfo(name)
                        m.size = len(data)
                        z.addfile(m, io.BytesIO(data))
                    if mutation == "duplicate":
                        m = tarfile.TarInfo("share/tsfixture/LICENSE")
                        z.addfile(m, io.BytesIO())
                    if mutation == "link":
                        m = tarfile.TarInfo("share/tsfixture/alias")
                        m.type = tarfile.SYMTYPE
                        m.linkname = "/outside"
                        z.addfile(m)
                if mutation is None:
                    self.assertEqual(
                        generic_resources.inspect_artifact(p, plan())["state"],
                        "verified",
                    )
                else:
                    with (
                        self.subTest(mutation=mutation),
                        self.assertRaises(contract.ContractError),
                    ):
                        generic_resources.inspect_artifact(p, plan())

    def test_wrong_language_gate_cannot_manufacture_current_adoption(self):
        from devtools.scripts import adoption_status

        policy = suite_policy.load_effective_registry()
        member = {
            "name": "tsfixture",
            "repository": "uibcdf/tsfixture",
            "capabilities": ["typescript-package"],
        }
        policy["members"] = [member]
        policy["guides"] = []
        policy["policies"]["adoption-lifecycle"]["include-central"] = False
        release = policy["governance"]["policy-release"]
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            directory = root / "tsfixture/.github/workflows"
            directory.mkdir(parents=True)
            path = directory / "policy.yml"
            wrong = (
                "jobs:\n  p:\n    uses: "
                + suite_policy.POLICY_CALLER_PREFIX
                + release
                + "\n"
            )
            path.write_text(wrong)
            row = adoption_status.inventory(root, policy=policy)[0]
            self.assertNotEqual(row.state, "current")
            self.assertTrue(
                suite_policy.latest_policy_mismatch(policy, "uibcdf/tsfixture", [wrong])
            )
            right = wrong.replace(
                suite_policy.POLICY_CALLER_PREFIX, typescript_repository.CALLER_PREFIX
            )
            path.write_text(right)
            self.assertEqual(
                adoption_status.inventory(root, policy=policy)[0].state, "current"
            )

    def test_actual_typescript_callers_and_mixed_refs_are_visible(self):
        prefix = typescript_repository.CALLER_PREFIX
        text = f"jobs:\n  typed:\n    uses: {prefix}policy-v1.6.0\n"
        self.assertEqual(suite_policy.policy_caller_releases([text]), ["policy-v1.6.0"])
        self.assertEqual(
            suite_policy.policy_caller_releases(["# " + prefix + "policy-v1.6.0"]), []
        )
        self.assertEqual(
            suite_policy.policy_caller_releases(
                [
                    text,
                    "jobs:\n  python:\n    uses: "
                    + suite_policy.POLICY_CALLER_PREFIX
                    + "policy-v1.5.12\n",
                ]
            ),
            ["policy-v1.5.12", "policy-v1.6.0"],
        )

    def test_typescript_profile_requires_real_native_manifest_and_lock_inputs(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / ".github/workflows").mkdir(parents=True)
            manifest = {
                "name": "@uibcdf/tsfixture",
                "version": "0.0.0",
                "type": "module",
                "engines": {"node": ">=24"},
                "types": "dist/index.d.ts",
                "exports": {
                    ".": {"import": "./dist/index.js", "types": "./dist/index.d.ts"}
                },
                "devDependencies": {"typescript": "5.9.3", "prettier": "3.6.2"},
                "scripts": {
                    "typecheck": "tsc --noEmit",
                    "format:check": "prettier --check .",
                    "test": "node --test tests/*.test.mjs",
                    "pack:check": "node pack.mjs",
                    "pack:conda:check": "node assets.mjs",
                    "check:reports": "python reports.py",
                    "check:version": "node version.mjs",
                },
            }
            lock = {
                "name": manifest["name"],
                "version": "0.0.0",
                "packages": {"": copy.deepcopy(manifest)},
            }
            (root / "package.json").write_text(json.dumps(manifest))
            (root / "package-lock.json").write_text(json.dumps(lock))
            (root / "tsconfig.json").write_text('{"compilerOptions":{"strict":true}}')
            (root / "LICENSE").write_text("MIT")
            (root / ".github/workflows/policy.yml").write_text(
                "jobs:\n  p:\n    uses: "
                + typescript_repository.CALLER_PREFIX
                + "policy-v1.6.0\n"
            )
            policy = {"governance": {"policy-release": "policy-v1.6.0"}}
            self.assertEqual(
                typescript_repository.check(root, "uibcdf/tsfixture", policy), []
            )
            manifest["devDependencies"]["typescript"] = "^5.9.3"
            (root / "package.json").write_text(json.dumps(manifest))
            self.assertTrue(
                typescript_repository.check(root, "uibcdf/tsfixture", policy)
            )
