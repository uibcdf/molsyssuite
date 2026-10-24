"""Inspect and verify the default eligible Linux Python 3.14 development profile.

This source-development probe is not a package release or scientific-suite gate.
"""

from __future__ import annotations

import argparse
import importlib
import importlib.metadata
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import tomllib
import yaml
from packaging.specifiers import SpecifierSet
from packaging.version import Version

ROOT = Path(__file__).resolve().parents[2]
RECIPE = ROOT / "devtools/conda-envs/molsyssuite-dev-py314.yaml"
QT_PACKAGES = {"pyside6", "qt6-main", "qt6-webengine", "qt6-positioning"}
RUST_VERSIONS = SpecifierSet(">=1.97.1,<2")
NATIVE_PACKAGES = {
    "rust",
    "rust_linux-64",
    "gcc_linux-64",
    "gcc_impl_linux-64",
    "binutils_impl_linux-64",
    "ld_impl_linux-64",
    "sysroot_linux-64",
    "git",
}


def profile(registry: dict, recipe: dict) -> dict:
    """Validate the recipe and derive eligibility from the versioned registry."""
    if recipe.get("name") != "molsyssuite@uibcdf_3.14":
        raise ValueError("unexpected development environment name")
    if recipe.get("channels") != ["uibcdf", "conda-forge", "nodefaults"]:
        raise ValueError("development channels must be public and bounded")
    dependencies = recipe.get("dependencies")
    if not isinstance(dependencies, list) or not all(
        isinstance(item, str) for item in dependencies
    ):
        raise ValueError("dependencies must be Conda specs, without a pip subsection")
    if len(set(dependencies)) != len(dependencies):
        raise ValueError("duplicate dependency specification")
    required = {
        "python=3.14",
        "pip",
        "packaging",
        "pyyaml",
        "python-build",
        "setuptools",
        "wheel",
        "setuptools-rust>=1.13,<2",
        "versioningit",
        "git",
        "rust_linux-64>=1.97.1,<2",
        "imageio",
        "pyside6=6.11.2",
        "qt6-webengine=6.11.2",
        "qt6-positioning=6.11.2",
    }
    if not required.issubset(dependencies):
        raise ValueError("development recipe lost a required Python/tool/Qt spec")
    if any("::" in spec or "-uibcdf" in spec or "://" in spec for spec in dependencies):
        raise ValueError("hidden channels or historical Qt forks are not this profile")
    members = {
        member["name"]: member
        for member in registry["members"]
        if "python-package" in member.get("capabilities", [])
    }
    transition = registry["policies"]["python"]["transition"]
    included = []
    for entry in transition["components"]:
        name = entry["name"]
        if name not in members or entry["state"] not in {"authorized", "admitted"}:
            raise ValueError("invalid Python 3.14 development admission")
        if (
            not re.fullmatch(r"[a-z][a-z0-9-]*", name)
            or members[name]["repository"] != f"uibcdf/{name}"
        ):
            raise ValueError("development source identity is not a registered member")
        included.append(
            {
                "name": name,
                "repository": members[name]["repository"],
                "state": entry["state"],
                "issue": entry["issue"],
            }
        )
    if not included or len({item["name"] for item in included}) != len(included):
        raise ValueError("empty or duplicate development cohort")
    return {
        "python": "3.14",
        "platform": "linux-64",
        "included": included,
        "excluded": sorted(set(members) - {item["name"] for item in included}),
        "excluded_tracker": "uibcdf/molsyssuite#51",
    }


def _prefix_tool(command: str, prefix: Path) -> Path:
    """Resolve a single activated executable and reject host tool fallbacks."""
    executable = shutil.which(command) if command else None
    if executable is None or not Path(executable).resolve().is_relative_to(prefix):
        raise ValueError(f"tool must come from the active Conda prefix: {command!r}")
    return Path(executable).resolve()


def reinstallation_plan(
    suite_registry: dict, moli_registry: dict, *, excluded: list[str] | None = None
) -> dict:
    """Select every registered Python source for an explicit local reinstall.

    This does not expand the qualified integration cohort or confer membership
    on MolI's direct components. Explicit exclusions remain visible in receipts.
    """
    if moli_registry.get("platform", {}).get("repository") != "uibcdf/moli":
        raise ValueError("reinstallation requires the MolI platform registry")
    candidates = []
    for owner, members in (
        ("molsyssuite", suite_registry["members"]),
        (
            "moli",
            [
                {**component, "name": name}
                for name, component in moli_registry["components"].items()
                if component.get("governance") == "direct"
            ],
        ),
    ):
        for member in members:
            if "python-package" not in member.get("capabilities", []):
                continue
            name = member["name"]
            if (
                not re.fullmatch(r"[a-z][a-z0-9-]*", name)
                or member["repository"] != f"uibcdf/{name}"
            ):
                raise ValueError("reinstallation source identity is not registered")
            candidates.append(
                {"name": name, "repository": member["repository"], "owner": owner}
            )
    if len({item["name"] for item in candidates}) != len(candidates):
        raise ValueError("duplicate source across suite and MolI registries")
    excluded_names = set()
    for selector in excluded or []:
        matches = [
            item["name"]
            for item in candidates
            if selector in {item["name"], item["repository"]}
        ]
        if len(matches) != 1:
            raise ValueError(f"unknown reinstallation exclusion: {selector}")
        excluded_names.add(matches[0])
    included = [item for item in candidates if item["name"] not in excluded_names]
    if not included:
        raise ValueError("reinstallation selection is empty")
    return {
        "python": "3.14",
        "platform": "linux-64",
        "scope": "explicit local reinstall; integration/admission states unchanged",
        "included": included,
        "excluded": [item for item in candidates if item["name"] in excluded_names],
    }


def verify_toolchain() -> dict:
    """Verify Conda tool origins and compile/run C and dependency-free Rust.

    Requires an activated Linux x86_64/Python 3.14 environment. Cargo runs
    offline, with isolated sources/targets; no clone or caller cache is modified.
    """
    prefix = Path(sys.prefix).resolve()
    if (
        sys.version_info[:2] != (3, 14)
        or sys.platform != "linux"
        or platform.machine() != "x86_64"
        or Path(os.environ.get("CONDA_PREFIX", "")).resolve() != prefix
    ):
        raise ValueError("toolchain probe requires activated Linux x86_64/Python 3.14")
    tools = {
        name: _prefix_tool(command, prefix)
        for name, command in {
            "rustc": os.environ.get("RUSTC", "rustc"),
            "cargo": os.environ.get("CARGO", "cargo"),
            "git": "git",
            "cc": os.environ.get("CC", ""),
            "linker": os.environ.get(
                "CARGO_TARGET_X86_64_UNKNOWN_LINUX_GNU_LINKER", ""
            ),
        }.items()
    }
    records = {
        record["name"]: record
        for path in (prefix / "conda-meta").glob("*.json")
        if (record := json.loads(path.read_text()))["name"] in NATIVE_PACKAGES
    }
    if set(records) != NATIVE_PACKAGES or any(
        not str(record.get("url", "")).startswith(
            "https://conda.anaconda.org/conda-forge/"
        )
        for record in records.values()
    ):
        raise ValueError(
            "native toolchain must have complete conda-forge package records"
        )
    if (
        any(
            Version(records[name]["version"]) not in RUST_VERSIONS
            for name in ("rust", "rust_linux-64")
        )
        or records["rust"]["version"] != records["rust_linux-64"]["version"]
    ):
        raise ValueError("Rust and activation versions must match the supported range")
    versions = {
        name: subprocess.check_output([str(path), "--version"], text=True).strip()
        for name, path in tools.items()
    }
    with tempfile.TemporaryDirectory(prefix="molsyssuite-toolchain-") as temporary:
        work = Path(temporary)
        c_source = work / "smoke.c"
        c_source.write_text(
            '#include <stdio.h>\nint main(void) { puts("conda-c-ok"); }\n'
        )
        subprocess.run(
            [str(tools["cc"]), str(c_source), "-o", str(work / "c-smoke")], check=True
        )
        if (
            subprocess.check_output([str(work / "c-smoke")], text=True).strip()
            != "conda-c-ok"
        ):
            raise ValueError("compiled C smoke returned unexpected output")
        (work / "src").mkdir()
        (work / "src/main.rs").write_text('fn main() { println!("conda-rust-ok"); }\n')
        (work / "Cargo.toml").write_text(
            '[package]\nname = "conda-rust-smoke"\nversion = "0.0.0"\nedition = "2021"\n'
        )
        subprocess.run(
            [
                str(tools["cargo"]),
                "build",
                "--offline",
                "--quiet",
                "--manifest-path",
                str(work / "Cargo.toml"),
                "--target",
                "x86_64-unknown-linux-gnu",
                "--target-dir",
                str(work / "target"),
            ],
            cwd=work,
            env={**os.environ, "CARGO_HOME": str(work / "cargo-home")},
            check=True,
        )
        binary = work / "target/x86_64-unknown-linux-gnu/debug/conda-rust-smoke"
        if subprocess.check_output([str(binary)], text=True).strip() != "conda-rust-ok":
            raise ValueError("compiled Rust smoke returned unexpected output")
    return {
        "python": platform.python_version(),
        "prefix": str(prefix),
        "tools": {
            name: {"path": str(path), "version": versions[name]}
            for name, path in tools.items()
        },
        "packages": {
            name: {
                key: record.get(key) for key in ("version", "build", "url", "sha256")
            }
            for name, record in records.items()
        },
        "smoke": {"c_compile_run": True, "cargo_offline_compile_run": True},
    }


def source_inventory(plan: dict, workspace: Path) -> list[dict]:
    """Require every eligible source and its actual Python metadata before pip."""
    sources = []
    for member in plan["included"]:
        path = workspace.resolve() / member["name"]
        project = tomllib.loads((path / "pyproject.toml").read_text())["project"]
        if "3.14" not in SpecifierSet(project["requires-python"]):
            raise ValueError(f"{member['repository']}: metadata excludes Python 3.14")
        git_root = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], cwd=path, text=True
        ).strip()
        if Path(git_root).resolve() != path:
            raise ValueError(
                f"{member['repository']}: source is not its own Git checkout"
            )
        sha = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=path, text=True
        ).strip()
        dirty = subprocess.check_output(
            ["git", "status", "--porcelain"], cwd=path, text=True
        ).strip()
        sources.append(
            {
                **member,
                "path": str(path),
                "distribution": project["name"],
                "sha": sha,
                "dirty": bool(dirty),
            }
        )
    return sources


def checkout_sources(plan: dict, workspace: Path) -> list[dict]:
    """Create fresh registered source checkouts and record their immutable heads."""
    workspace.mkdir(parents=True, exist_ok=True)
    if any((workspace / member["name"]).exists() for member in plan["included"]):
        raise ValueError("fresh checkout refuses an occupied member directory")
    for member in plan["included"]:
        subprocess.run(
            [
                "git",
                "clone",
                "--filter=blob:none",
                "--branch",
                "main",
                "--",
                f"https://github.com/{member['repository']}.git",
                str(workspace.resolve() / member["name"]),
            ],
            check=True,
        )
    return source_inventory(plan, workspace)


def install_editables(sources: list[dict]) -> None:
    """Install the complete checked cohort without changing the Conda closure."""
    if not sources:
        raise ValueError("editable installation requires a complete source cohort")
    args = [sys.executable, "-m", "pip", "install", "--no-deps", "--no-build-isolation"]
    for source in sources:
        args.extend(["-e", source["path"]])
    subprocess.run(args, check=True)
    subprocess.run([sys.executable, "-m", "pip", "check"], check=True)


def reinstall_workspace(
    registry: dict,
    workspace: Path,
    *,
    moli_registry: Path,
    excluded: list[str],
    dry_run: bool = False,
) -> dict:
    """Preflight every selected clone, then refresh editables and their metadata.

    Uses only local Git state. It never fetches tags, updates branches or
    installs dependencies. A dry run does not require the native toolchain.
    """
    plan = reinstallation_plan(
        registry, tomllib.loads(moli_registry.read_text()), excluded=excluded
    )
    sources = source_inventory(plan, workspace)
    result = {**plan, "sources": sources, "dry_run": dry_run}
    if not dry_run:
        result["toolchain"] = verify_toolchain()
        install_editables(sources)
        result["installed_versions"] = {
            source["repository"]: importlib.metadata.version(source["distribution"])
            for source in sources
        }
    return result


def verify_runtime(sources: list[dict]) -> dict:
    """Verify editable import origins and the official Qt closure on Linux-64."""
    if (
        sys.version_info[:2] != (3, 14)
        or sys.platform != "linux"
        or platform.machine() != "x86_64"
    ):
        raise ValueError("runtime probe requires Linux x86_64 and Python 3.14")
    prefix = Path(sys.prefix).resolve()
    conda_records = [
        json.loads(path.read_text()) for path in (prefix / "conda-meta").glob("*.json")
    ]
    selected = {
        record["name"]: record
        for record in conda_records
        if record["name"] in QT_PACKAGES
    }
    if set(selected) != QT_PACKAGES or any(
        record.get("version") != "6.11.2"
        or not str(record.get("url", "")).startswith(
            "https://conda.anaconda.org/conda-forge/"
        )
        for record in selected.values()
    ):
        raise ValueError("runtime Qt closure must be official conda-forge 6.11.2")
    if any("-uibcdf" in record["name"] for record in conda_records):
        raise ValueError("historical Qt fork is present in the canonical environment")
    imports = []
    for source in sources:
        module = importlib.import_module(source["name"].replace("-", "_"))
        origin = Path(module.__file__).resolve()
        if not origin.is_relative_to(Path(source["path"]).resolve()):
            raise ValueError(
                f"{source['repository']}: import is not from the checked editable"
            )
        distribution = importlib.metadata.distribution(source["distribution"])
        direct = json.loads(distribution.read_text("direct_url.json") or "{}")
        if direct.get("dir_info", {}).get("editable") is not True:
            raise ValueError(f"{source['repository']}: distribution is not editable")
        imports.append(
            {**source, "version": distribution.version, "origin": str(origin)}
        )
    qt = importlib.import_module("PySide6.QtCore")
    importlib.import_module("PySide6.QtWebEngineCore")
    importlib.import_module("PySide6.QtWebEngineWidgets")
    if qt.qVersion() != "6.11.2":
        raise ValueError("loaded Qt runtime disagrees with the recipe")
    if not Path(qt.__file__).resolve().is_relative_to(prefix):
        raise ValueError("Qt imported outside the created environment")
    return {
        "python": platform.python_version(),
        "prefix": str(prefix),
        "sources": imports,
        "qt": {
            name: {
                key: record.get(key) for key in ("version", "build", "url", "sha256")
            }
            for name, record in selected.items()
        },
        "scope": "editable development imports; no full science or public admission claim",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "operation",
        choices=(
            "profile",
            "toolchain",
            "checkout",
            "sources",
            "install",
            "reinstall",
            "runtime",
        ),
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        help="clone parent directory; reinstall defaults to this repository's parent",
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--moli-registry",
        type=Path,
        help="reinstall: defaults to WORKSPACE/moli/moli.toml",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="reinstall: explicitly omit a registered Python repository; repeatable",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="reinstall: inspect all selected clones without installing",
    )
    args = parser.parse_args()
    try:
        registry = tomllib.loads((ROOT / "suite.toml").read_text())
        plan = profile(
            registry,
            yaml.safe_load(RECIPE.read_text()),
        )
        if args.operation != "reinstall" and (
            args.dry_run or args.exclude or args.moli_registry
        ):
            raise ValueError(
                "--dry-run, --exclude and --moli-registry require reinstall"
            )
        result = plan
        if args.operation == "toolchain":
            result = verify_toolchain()
        elif args.operation == "reinstall":
            workspace = args.workspace or ROOT.parent
            result = reinstall_workspace(
                registry,
                workspace,
                moli_registry=args.moli_registry or workspace / "moli/moli.toml",
                excluded=args.exclude,
                dry_run=args.dry_run,
            )
        elif args.operation != "profile":
            if args.workspace is None:
                raise ValueError("source operations require --workspace")
            sources = (
                checkout_sources(plan, args.workspace)
                if args.operation == "checkout"
                else source_inventory(plan, args.workspace)
            )
            result = {**plan, "sources": sources}
            if args.operation == "install":
                if (
                    sys.version_info[:2] != (3, 14)
                    or sys.platform != "linux"
                    or platform.machine() != "x86_64"
                ):
                    raise ValueError(
                        "editable installation requires Linux x86_64 and Python 3.14"
                    )
                result["toolchain"] = verify_toolchain()
                install_editables(sources)
            elif args.operation == "runtime":
                result = {**plan, **verify_runtime(sources)}
        output = json.dumps(result, indent=2) + "\n"
        if args.output:
            args.output.write_text(output)
        else:
            print(output, end="")
    except (
        OSError,
        ValueError,
        KeyError,
        ImportError,
        subprocess.CalledProcessError,
    ) as error:
        print(f"development environment check failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
