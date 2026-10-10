"""Prepare central dependency-only recipes from reviewed plans, without publishing.

Compose the shared plan validator, template renderer and development validator.
This local operation does not qualify installed bundles, connect clones or
authorize registry mutations. Python artifact adapters stay separate.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

import tomllib
import yaml

try:
    from devtools.scripts.conda_release_contract import ContractError, validate_plan
    from devtools.scripts.development_environment import profile
    from devtools.scripts.noarch_conda import local_path, render_recipe
except ModuleNotFoundError:
    from conda_release_contract import ContractError, validate_plan
    from development_environment import profile
    from noarch_conda import local_path, render_recipe


PACKAGES = ("molsyssuite", "molsyssuite-dev")
DEVELOPMENT_RECIPE = "devtools/conda-envs/molsyssuite-dev-py314.yaml"
CAPABILITY_COMMANDS = {
    "molsyssuite": [
        'python -c "import molsysmt, molsysviewer"',
    ],
    "molsyssuite-dev": [
        'python -c "import sys; assert sys.version_info[:2] == (3, 14)"',
        "python -m pytest --version",
        "python -m build --version",
        "ruff --version",
    ],
}


def prepare_recipe(root: Path, package: str, version: str) -> tuple[dict, str]:
    """Return a plan-bound metadata-only recipe and filename without writing.

    Missing plans fail closed. Developer dependencies derive from the maintained
    environment; no clone or runtime-bundle installation and no version fallback.
    """
    if package not in PACKAGES:
        raise ContractError("unknown central metapackage")
    directory = f"devtools/conda-build/{package}"
    plan = tomllib.loads(local_path(root, directory + "/release_plan.toml").read_text())
    validate_plan(plan)
    if plan["package"] != package or plan["version"] != version:
        raise ContractError("selected package/version differs from its reviewed plan")
    if plan["profile"] != "metapackage":
        raise ContractError("central dependency bundles need the metapackage profile")
    if set(plan.get("gate_jobs", {})) != set(plan["required_workflows"]):
        raise ContractError("each native gate needs explicit executed jobs and steps")
    context = {}
    if package == "molsyssuite-dev":
        environment = yaml.safe_load(local_path(root, DEVELOPMENT_RECIPE).read_text())
        registry = tomllib.loads(local_path(root, "suite.toml").read_text())
        profile(registry, environment)
        if plan["test_platforms"] != ["linux-64"] or plan["python_versions"] != [
            "3.14"
        ]:
            raise ContractError(
                "developer bundle currently has only the Linux/3.14 profile"
            )
        context["development_dependencies"] = environment["dependencies"]
    elif not set(plan["python_versions"]).issubset({"3.11", "3.12", "3.13", "3.14"}):
        raise ContractError("runtime matrix is outside its declared Python bounds")
    build = plan["build_number"]
    recipe, source = render_recipe(
        root,
        directory + "/meta.yaml",
        {
            "MOLSYSSUITE_CONDA_VERSION": version,
            "MOLSYSSUITE_CONDA_BUILD_NUMBER": str(build),
        },
        template_context=context,
    )
    if (
        set(recipe) != {"package", "build", "requirements", "test", "about"}
        or "# [" in source
    ):
        raise ContractError(
            "dependency bundles forbid source, outputs and platform selectors"
        )
    if recipe["package"] != {"name": package, "version": version} or recipe[
        "build"
    ] != {"noarch": "generic", "number": build, "string": f"meta_{build}"}:
        raise ContractError(
            "bundle identity/build differs or adds executable build behavior"
        )
    requirements = recipe["requirements"]
    if not isinstance(requirements, dict) or set(requirements) != {"run"}:
        raise ContractError("dependency bundles declare only run requirements")
    dependencies = requirements["run"]
    if not isinstance(dependencies, list) or not dependencies:
        raise ContractError("dependency bundle needs explicit Conda requirements")
    names = []
    for dependency in dependencies:
        match = re.fullmatch(
            r"([a-z0-9][a-z0-9-]*)(?:\s*[<>=!][0-9a-zA-Z.*<>=!,_-]+)?", str(dependency)
        )
        if not isinstance(dependency, str) or match is None:
            raise ContractError(
                "requirements must be plain Conda specs, without channels or sources"
            )
        names.append(match[1])
    if len(names) != len(set(names)) or any(name in PACKAGES for name in names):
        raise ContractError(
            "bundle dependencies duplicate or couple the central bundles"
        )
    if package == "molsyssuite-dev":
        if dependencies != context["development_dependencies"]:
            raise ContractError(
                "developer requirements drifted from the maintained environment"
            )
    elif (
        set(names)
        != {
            "python",
            "molsysmt",
            "molsysviewer",
        }
        or dependencies[names.index("python")] != "python >=3.11,<3.15"
    ):
        raise ContractError(
            "runtime selection or Python bounds need an explicit scope review"
        )
    tests = recipe["test"]
    commands = tests.get("commands") if isinstance(tests, dict) else None
    if (
        not isinstance(tests, dict)
        or set(tests) != {"commands"}
        or commands != CAPABILITY_COMMANDS[package]
    ):
        raise ContractError(
            "bundle must retain its reviewed brief installed capability commands"
        )
    return recipe, f"{package}-{version}-meta_{build}.tar.bz2"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--package", choices=PACKAGES, required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--output-directory", type=Path, required=True)
    parser.add_argument("--github-output", type=Path)
    args = parser.parse_args()
    created = False
    try:
        recipe, filename = prepare_recipe(
            args.root.resolve(), args.package, args.version
        )
        destination = args.output_directory.resolve()
        if any(character in str(destination) for character in "\r\n"):
            raise ContractError("render destination must be a single-line path")
        if destination.exists():
            raise ContractError("render destination must be a new task-owned directory")
        destination.mkdir(parents=True)
        created = True
        (destination / "meta.yaml").write_text(yaml.safe_dump(recipe, sort_keys=False))
        if args.github_output:
            with args.github_output.open("a") as stream:
                stream.write(f"directory={destination}\nfilename={filename}\n")
        print(
            json.dumps(
                {
                    "package": args.package,
                    "filename": filename,
                    "directory": str(destination),
                    "scope": "recipe preparation only; no installed or publication evidence",
                }
            )
        )
    except (ContractError, OSError, ValueError, KeyError, TypeError) as error:
        if created:
            try:
                shutil.rmtree(destination)
            except OSError as cleanup_error:
                print(
                    f"Failed to clean task-owned recipe {destination}: {cleanup_error}"
                )
        print(f"Central metapackage preparation blocked: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
