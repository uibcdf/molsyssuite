"""Audit declared runtime routes without installing, importing or rewriting a member.

The member inventory selects routes; pyproject.toml owns their requirements.
Noarch recipe checks and requirement comparisons reuse the existing shared tool.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote, urlsplit

import tomllib
import yaml
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name
from packaging.version import Version

try:
    from devtools.scripts.noarch_conda import (
        ContractError,
        inspect_recipe,
        local_path,
        required_constraints,
    )
except ModuleNotFoundError:
    from noarch_conda import (
        ContractError,
        inspect_recipe,
        local_path,
        required_constraints,
    )

SCHEMA = "molsyssuite.dependency-routes@1"


def _reason(record: dict) -> None:
    if not isinstance(record.get("reason"), str) or not record["reason"].strip():
        raise ContractError("route needs an explicit review reason")


def _inventory_paths(root: Path, records: list[dict], observed: set[str]) -> None:
    paths = []
    for record in records:
        _reason(record)
        local_path(root, record["path"])
        paths.append(record["path"])
    if len(paths) != len(set(paths)):
        raise ContractError("duplicate route path")
    if set(paths) != observed:
        raise ContractError(
            f"unclassified/missing routes: new={sorted(observed - set(paths))}, "
            f"missing={sorted(set(paths) - observed)}"
        )


def _files(root: Path, directory: str, patterns: tuple[str, ...]) -> set[str]:
    return {
        str(path.relative_to(root))
        for pattern in patterns
        for path in (root / directory).glob(pattern)
        if path.is_file()
    }


def _environment_requirements(content: dict) -> list[str]:
    dependencies = content.get("dependencies")
    if not isinstance(dependencies, list):
        raise ContractError("environment needs a dependencies list")
    result = []
    for entry in dependencies:
        if isinstance(entry, str):
            # A Conda minor pin is a wildcard, not a PEP 440 exact patch.
            if match := re.fullmatch(r"python\s*=\s*(\d+\.\d+)", entry):
                entry = f"python=={match[1]}.*"
            Requirement(entry)  # Unsupported Conda syntax needs an owned profile.
            result.append(entry)
        elif isinstance(entry, dict) and set(entry) == {"pip"}:
            if not isinstance(entry["pip"], list):
                raise ContractError("pip requirements must be a list")
            for item in entry["pip"]:
                parsed = Requirement(item)
                if parsed.marker or parsed.url:
                    raise ContractError("conditional/source pip route needs review")
                result.append(item)
        else:
            raise ContractError(f"unsupported environment requirement: {entry!r}")
    for item in result:
        parsed = Requirement(item)
        if parsed.marker or parsed.url:
            raise ContractError("conditional/source environment route needs review")
    return result


def _narrow_python(required: str, minor: str) -> list[str]:
    """Allow only a reviewed whole minor inside simple >= / < Python bounds."""
    if not re.fullmatch(r"\d+\.\d+", minor):
        raise ContractError("python_minor must name one complete major.minor")
    major, value = map(int, minor.split("."))
    lower, upper = Version(minor), Version(f"{major}.{value + 1}")
    rules = list(Requirement("python" + required).specifier)
    if not rules or any(rule.operator not in {">=", "<"} for rule in rules):
        raise ContractError("narrowed Python requires reviewed >= / < metadata bounds")
    if any(
        (rule.operator == ">=" and Version(rule.version) > lower)
        or (rule.operator == "<" and Version(rule.version) < upper)
        for rule in rules
    ):
        raise ContractError(f"Python {minor} is outside requires-python {required}")
    return [f"python=={minor}.*", f"python>={minor},<{upper}"]


def validate_source_version(requirement: str, version: str) -> None:
    """Refuse an installed source candidate violating its public requirement."""
    parsed = Requirement(requirement)
    if parsed.marker or parsed.url or not parsed.specifier:
        raise ContractError("source route requires unconditional version constraints")
    if not parsed.specifier.contains(Version(version), prereleases=True):
        raise ContractError(f"installed source {version} violates {parsed}")


def _source(record: dict, requirement: str, root: Path, distribution_for) -> None:
    _reason(record)
    commit = record.get("commit", "")
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ContractError("source route needs a reviewed full lowercase commit")
    if record.get("install") != "pip-no-deps-directory":
        raise ContractError("source install route needs an owned profile")

    def git(*arguments):
        return subprocess.check_output(
            ["git", *arguments], cwd=root, text=True, timeout=30
        ).strip()

    if git("rev-parse", "HEAD") != commit or git("status", "--porcelain"):
        raise ContractError("source checkout is dirty or differs from reviewed commit")
    distribution = distribution_for(Requirement(requirement).name)
    validate_source_version(requirement, distribution.version)
    direct = distribution.read_text("direct_url.json")
    if not direct:
        raise ContractError("installed source has no directory provenance")
    data = json.loads(direct)
    url = urlsplit(data["url"])
    if (
        url.scheme != "file"
        or url.netloc not in {"", "localhost"}
        or Path(unquote(url.path)).resolve() != root.resolve()
        or "dir_info" not in data
    ):
        raise ContractError("installed distribution is not from the reviewed directory")


def audit(
    root: Path,
    inventory_path: str = "devtools/dependency_routes.toml",
    *,
    source_roots: dict[str, Path] | None = None,
    distribution_for=importlib.metadata.distribution,
) -> dict:
    """Return bounded route evidence; refuse incomplete or inconsistent inputs.

    Source roots must be actual clean checkouts installed into this interpreter.
    This verifies metadata/provenance, not imports, native bytes or scientific use.
    """
    root = root.resolve()
    inventory = tomllib.loads(local_path(root, inventory_path).read_text())
    if inventory.get("schema") != SCHEMA:
        raise ContractError(f"expected {SCHEMA} inventory")
    _reason(inventory)
    project = tomllib.loads(local_path(root, "pyproject.toml").read_text())["project"]
    if "dependencies" in project.get("dynamic", []):
        raise ContractError("dynamic runtime dependencies need an owned profile")
    required = project.get("dependencies", [])
    required_constraints(required, required, {})
    names = [canonicalize_name(Requirement(value).name) for value in required]
    if len(names) != len(set(names)):
        raise ContractError("duplicate project runtime requirement")
    requirements = dict(zip(names, required))
    aliases = inventory.get("conda_names", {})
    python = "python" + project["requires-python"]
    source_records = inventory.get("source_routes", [])
    sources = {canonicalize_name(record["name"]): record for record in source_records}
    if len(sources) != len(source_records) or not set(sources) <= set(requirements):
        raise ContractError("duplicate or non-required source dependency")
    supplied_roots = source_roots or {}
    if set(supplied_roots) != set(sources):
        raise ContractError("provide exactly the inventoried required source checkouts")
    if not sources and not inventory.get("source_reason", "").strip():
        raise ContractError("absence of required source routes needs a review reason")

    evidence = {"schema": SCHEMA, "package": project["name"], "routes": []}
    for name, record in sources.items():
        try:
            _source(record, requirements[name], supplied_roots[name], distribution_for)
        except (
            ValueError,
            OSError,
            KeyError,
            subprocess.SubprocessError,
            importlib.metadata.PackageNotFoundError,
        ) as error:
            raise ContractError(f"source {name}: {error}") from error

    recipes = inventory.get("recipes", [])
    _inventory_paths(
        root, recipes, _files(root, "devtools", ("**/meta.yaml", "**/recipe.yaml"))
    )
    for recipe in recipes:
        try:
            if recipe["kind"] != "shared-noarch":
                raise ContractError("recipe kind needs an owned profile")
            plan = recipe["plan"]
            if local_path(root, plan).with_name("meta.yaml") != local_path(
                root, recipe["path"]
            ):
                raise ContractError("plan does not identify this recipe")
            inspect_recipe(root, plan, recipe["resources"])
        except (ValueError, OSError, KeyError, TypeError, yaml.YAMLError) as error:
            raise ContractError(f"{recipe['path']}: {error}") from error
        evidence["routes"].append({"path": recipe["path"], "kind": recipe["kind"]})

    environments = inventory.get("environments", [])
    _inventory_paths(
        root,
        environments,
        _files(root, "devtools/conda-envs", ("*.yaml", "*.yml")),
    )
    for environment in environments:
        path, kind = environment["path"], environment["kind"]
        try:
            content = yaml.safe_load(local_path(root, path).read_text())
            if kind == "runtime":
                if content.get("channels") != ["uibcdf", "conda-forge"]:
                    raise ContractError("runtime channels must be uibcdf, conda-forge")
                if environment.get("channel_priority") != "strict":
                    raise ContractError(
                        "runtime route must record strict channel priority"
                    )
                items = _environment_requirements(content)
                supplied = environment.get("source_supplied", [])
                if len(supplied) != len(set(supplied)) or not set(supplied) <= set(
                    sources
                ):
                    raise ContractError("environment names unreviewed source providers")
                installed_names = {
                    canonicalize_name(Requirement(item).name) for item in items
                }
                supplied_names = {
                    canonicalize_name(aliases.get(name, name)) for name in supplied
                }
                if installed_names & supplied_names:
                    raise ContractError(
                        "dependency is both source supplied and declared"
                    )
                expected = [
                    value
                    for name, value in requirements.items()
                    if name not in supplied
                ]
                required_constraints(items, expected, aliases)
                minor = environment.get("python_minor")
                python_contracts = (
                    _narrow_python(project["requires-python"], minor)
                    if minor
                    else [python]
                )
                if not any(
                    Requirement(item).name.lower() == "python"
                    and str(Requirement(item).specifier)
                    in {str(Requirement(value).specifier) for value in python_contracts}
                    for item in items
                ):
                    raise ContractError(
                        f"Python constraint differs from {python_contracts}"
                    )
                # Include Python in the shared duplicate check too.
                required_constraints(items, [], {})
            elif kind not in {"build-only", "resolved-package"}:
                raise ContractError("unclassified environment kind")
        except (
            ValueError,
            OSError,
            KeyError,
            TypeError,
            AttributeError,
            yaml.YAMLError,
        ) as error:
            raise ContractError(f"{path}: {error}") from error
        evidence["routes"].append({"path": path, "kind": kind})

    workflows = inventory.get("workflows", [])
    _inventory_paths(
        root, workflows, _files(root, ".github/workflows", ("*.yaml", "*.yml"))
    )
    for workflow in workflows:
        path = workflow["path"]
        with local_path(root, path).open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
        if digest != workflow.get("sha256"):
            raise ContractError(
                f"{path}: reviewed workflow changed; classify its actual routes again"
            )
        evidence["routes"].append(
            {"path": path, "kind": "reviewed-workflow", "sha256": digest}
        )
    evidence["source_dependencies"] = sorted(sources)
    return evidence


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--inventory", default="devtools/dependency_routes.toml")
    parser.add_argument(
        "--source-root", action="append", default=[], metavar="NAME=PATH"
    )
    args = parser.parse_args()
    try:
        sources = {}
        for item in args.source_root:
            name, path = item.split("=", 1)
            name = canonicalize_name(name)
            if name in sources:
                raise ContractError("duplicate source root")
            sources[name] = Path(path)
        result = audit(args.root, args.inventory, source_roots=sources)
    except (
        ValueError,
        OSError,
        KeyError,
        TypeError,
        AttributeError,
        yaml.YAMLError,
    ) as error:
        print(f"Dependency routes rejected: {error}")
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
