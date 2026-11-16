"""Qualify administrative TypeScript/resource fixtures, never a member release."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import shlex
import subprocess
import sys
from pathlib import Path

import yaml

if __package__:
    from . import (
        bootstrap_typescript,
        generic_resources,
        suite_policy,
        typescript_repository,
    )
else:
    import bootstrap_typescript
    import generic_resources
    import suite_policy
    import typescript_repository


def prepare(stage: Path) -> None:
    """Use current-source provider inputs explicitly, without a frozen/latest claim."""
    policy = copy.deepcopy(suite_policy.load_effective_registry())
    policy["members"].append(
        {
            "name": "tsfixture",
            "repository": "uibcdf/tsfixture",
            "role": "developer-tool",
            "membership": "auxiliary",
            "maturity": "incubating",
            "development-mode": "active",
            "capabilities": ["typescript-package"],
        }
    )
    bootstrap_typescript.render_stage(
        stage,
        "uibcdf/tsfixture",
        "Private administrative TypeScript profile fixture",
        policy,
    )
    subprocess.run(
        [sys.executable, str(stage / "devtools/devguide_index.py")],
        cwd=stage,
        check=True,
    )


def receive(stage: Path, *, build_archive: bool) -> dict:
    """Exercise independent addressability refusals and real relocated assets."""
    if not __debug__:
        raise ValueError("fixture qualification requires enabled assertions")
    provider_paths = [
        Path(__file__),
        bootstrap_typescript.ROOT / "devtools/scripts/generic_resources.py",
        bootstrap_typescript.ROOT / "devtools/scripts/bootstrap_typescript.py",
    ]
    provider_inputs = {
        str(p.relative_to(bootstrap_typescript.ROOT)): hashlib.sha256(
            p.read_bytes()
        ).hexdigest()
        for p in provider_paths
    }
    stage_inputs = {
        p.relative_to(stage).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in stage.rglob("*")
        if p.is_file()
        and not p.is_symlink()
        and "node_modules" not in p.relative_to(stage).parts
        and "dist" not in p.relative_to(stage).parts
    }
    node = "node"
    findings = typescript_repository.check(
        stage, "uibcdf/tsfixture", suite_policy.load_effective_registry()
    )
    if findings:
        raise ValueError("provider fixture conformance: " + "; ".join(findings))
    resolver = stage / "devtools/check-node-guard.mjs"
    cases = {
        "comments.test.mjs": "// import test from 'node:test'; test('fake',()=>{});\n",
        "unrelated.test.mjs": "import test from 'other'; test('fake',()=>{});\n",
        "dynamic.test.mjs": "import test from 'node:test'; function f(){test('hidden',()=>{});}\n",
        "valid.test.mjs": "import {test as check} from 'node:test'; check('real',()=>{});\n",
    }
    checks = []
    try:
        for name, text in cases.items():
            (stage / "tests" / name).write_text(text)
            r = subprocess.run(
                [node, str(resolver), "tests/" + name],
                cwd=stage,
                capture_output=True,
                check=False,
            )
            assert (r.returncode == 0) == (name == "valid.test.mjs"), name
            checks.append({"case": name, "accepted": r.returncode == 0})
        r = subprocess.run(
            [node, str(resolver), "../outside.test.mjs"],
            cwd=stage,
            capture_output=True,
            check=False,
        )
        assert r.returncode
        alias = stage / "tests/alias.test.mjs"
        alias.symlink_to(stage / "tests/import.test.mjs")
        r = subprocess.run(
            [node, str(resolver), "tests/alias.test.mjs"],
            cwd=stage,
            capture_output=True,
            check=False,
        )
        assert r.returncode
        checks += [
            {"case": "traversal", "accepted": False},
            {"case": "symlink", "accepted": False},
        ]
    finally:
        for name in [*cases, "alias.test.mjs"]:
            (stage / "tests" / name).unlink(missing_ok=True)
    prefix = stage.parent / "generic-fixture-prefix"
    subprocess.run(
        [node, str(stage / "devtools/check-assets.mjs"), "conda", str(prefix)],
        cwd=stage,
        check=True,
    )
    moved = stage.parent / "generic-relocated-prefix"
    prefix.rename(moved)
    assets = generic_resources.inspect_prefix(moved, "tsfixture", "0.0.0")
    result = {
        "schema": "molsyssuite.typescript-provider-qualification@1",
        "state": "verified",
        "scope": "current-source administrative fixture only; not published admission or a component artifact",
        "node": subprocess.check_output([node, "--version"], text=True).strip(),
        "guard_controls": checks,
        "relocated_assets": assets,
        "archive": None,
    }
    if build_archive:
        # Finite fixture over conda-build's public API, not a competing publisher.
        from conda_build.api import build
        from conda_build.config import Config

        recipe = stage.parent / "generic-fixture-recipe"
        recipe.mkdir()
        document = {
            "package": {"name": "tsfixture", "version": "0.0.0"},
            "source": {"path": str(moved)},
            "build": {
                "noarch": "generic",
                "number": 0,
                "string": "res_0",
                "script": 'mkdir -p "$PREFIX/share"\ncp -R share/tsfixture "$PREFIX/share/tsfixture"',
            },
            "requirements": {"run": []},
            "test": {
                "requires": ["nodejs=24.22.1"],
                "commands": [
                    "node -e \"import('file://' + process.env.PREFIX + '/share/tsfixture/dist/index.js').then(m => { if(m.component !== 'tsfixture') throw Error('wrong installed module'); })\""
                ],
            },
            "about": {
                "license": "MIT",
                "license_file": "share/tsfixture/LICENSE",
                "summary": "Private administrative fixture, never a member release",
            },
        }
        consumer_script = recipe / "installed-consumer.mjs"
        compiler = str(stage / "node_modules/typescript/bin/tsc")
        consumer_script.write_text(
            "import assert from 'node:assert/strict';\n"
            "import {mkdtempSync,writeFileSync,rmSync} from 'node:fs';\n"
            "import {join} from 'node:path'; import {tmpdir} from 'node:os';\n"
            "import {execFileSync} from 'node:child_process'; import {pathToFileURL} from 'node:url';\n"
            "assert.equal(process.versions.node,'24.22.1');\n"
            "const file=join(process.env.PREFIX,'share/tsfixture/dist/index.js');\n"
            "assert.equal((await import(pathToFileURL(file).href)).component,'tsfixture');\n"
            "const t=mkdtempSync(join(tmpdir(),'suite-installed-types-'));\n"
            "try { writeFileSync(join(t,'package.json'),JSON.stringify({type:'module'}));\n"
            "writeFileSync(join(t,'check.ts'),'import {component} from '+JSON.stringify(file)+'; const value:string=component; void value;');\n"
            + "execFileSync(process.execPath,["
            + json.dumps(compiler)
            + ", '--noEmit','--strict','--module','NodeNext','--moduleResolution','NodeNext',join(t,'check.ts')],{cwd:t,stdio:'inherit'});\n"
            + "console.log(JSON.stringify({installed_node:process.versions.node,import:'passed',declarations:'passed'}));\n"
            + "} finally {rmSync(t,{recursive:true,force:true});}\n"
        )
        document["test"]["commands"] = [shlex.join(["node", str(consumer_script)])]
        (recipe / "meta.yaml").write_text(yaml.safe_dump(document, sort_keys=False))
        config = Config(
            croot=str(stage.parent / "fixture-conda-build"),
            output_folder=str(stage.parent / "fixture-archives"),
            channel_urls=["conda-forge"],
            override_channels=True,
            anaconda_upload=False,
            conda_pkg_format=1,
        )
        paths = build(str(recipe), config=config, notest=False)
        assert len(paths) == 1
        decision = {
            "schema": "molsyssuite.conda-plan@1",
            "package": "tsfixture",
            "version": "0.0.0",
            "build_number": 0,
            "route": "staged",
            "profile": "generic-resources",
            "reason": "Private engineering fixture",
            "decision_by": "authorized central #199 qualification",
            "artifact_subdirs": ["noarch"],
            "test_platforms": ["linux-64"],
            "python_versions": [],
            "runtime_versions": ["node24"],
            "required_workflows": [".github/workflows/check-typescript-profile.yaml"],
            "gate_jobs": {
                ".github/workflows/check-typescript-profile.yaml": {
                    "profile": [
                        "Receive real generic archive and static Node guard controls"
                    ]
                }
            },
            "requires_installed_gate": True,
            "new_compatibility_surface": True,
            "coupled_release": False,
            "dependencies_public": True,
        }
        result["archive"] = generic_resources.inspect_artifact(Path(paths[0]), decision)
        result["archive"]["recipe_tests"] = "passed real installed Node consumer"
        result["archive"]["scope"] = (
            "original private fixture only; no upload, member candidate or browser/scientific claim"
        )
    result["provider_inputs"] = provider_inputs
    result["stage_inputs"] = stage_inputs
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("prepare", "receive"))
    parser.add_argument("stage", type=Path)
    parser.add_argument("--build-archive", action="store_true")
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    stage = args.stage.resolve()
    if args.operation == "prepare":
        prepare(stage)
        return 0
    result = receive(stage, build_archive=args.build_archive)
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(json.dumps(result, indent=2) + "\n")
    print(
        json.dumps(
            {
                "state": result["state"],
                "node": result["node"],
                "archive": bool(result["archive"]),
                "scope": result["scope"],
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
