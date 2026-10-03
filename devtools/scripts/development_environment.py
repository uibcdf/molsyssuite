"""Inspect and verify the default eligible Linux Python 3.14 development profile.

This source-development probe is not a package release or scientific-suite gate.
"""

from __future__ import annotations

import argparse
import importlib
import importlib.metadata
import json
import platform
import re
import subprocess
import sys
from pathlib import Path

import tomllib
import yaml
from packaging.specifiers import SpecifierSet

ROOT = Path(__file__).resolve().parents[2]
RECIPE = ROOT / "devtools/conda-envs/molsyssuite-dev-py314.yaml"
QT_PACKAGES = {"pyside6", "qt6-main", "qt6-webengine", "qt6-positioning"}


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
        "operation", choices=("profile", "checkout", "sources", "install", "runtime")
    )
    parser.add_argument("--workspace", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        plan = profile(
            tomllib.loads((ROOT / "suite.toml").read_text()),
            yaml.safe_load(RECIPE.read_text()),
        )
        result = plan
        if args.operation != "profile":
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
