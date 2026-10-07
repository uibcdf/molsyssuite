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
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import tomllib
import yaml
from jinja2 import TemplateError
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name
from packaging.version import Version

if not __package__:  # Resolve this provider before sibling editable namespaces.
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

try:
    from devtools.scripts import dependency_constraints as contracts
    from devtools.scripts import dependency_route_contexts as contexts
    from devtools.scripts.noarch_conda import (
        ContractError,
        inspect_recipe,
        inspect_recipe_dependencies,
        inspect_resources,
        local_path,
        required_constraints,
    )
except ImportError:
    import dependency_constraints as contracts
    import dependency_route_contexts as contexts
    from noarch_conda import (
        ContractError,
        inspect_recipe,
        inspect_recipe_dependencies,
        inspect_resources,
        local_path,
        required_constraints,
    )

SCHEMA = "molsyssuite.dependency-routes@1"
COMPATIBILITY_SCHEMA = "molsyssuite.dependency-routes@2"


def _compatible_environment(content: dict) -> list[contracts.RouteRequirement]:
    dependencies = content.get("dependencies")
    if not isinstance(dependencies, list):
        raise ContractError("environment needs a dependencies list")
    items = []
    for entry in dependencies:
        if isinstance(entry, str):
            items.append(contracts.conda_requirement(entry))
        elif (
            isinstance(entry, dict)
            and set(entry) == {"pip"}
            and isinstance(entry["pip"], list)
        ):
            items.extend(contracts.pip_requirement(item) for item in entry["pip"])
        else:
            raise ContractError(f"unsupported environment requirement: {entry!r}")
    contracts.compare_requirements(items, [])
    return items


def _local_recipe(root: Path, record: dict, aliases: dict) -> dict:
    """Derive rendering inputs from a committed plan without adopting its publisher."""
    plan = tomllib.loads(local_path(root, record["plan"]).read_text())
    if not re.fullmatch(r"\d+\.\d+\.\d+", str(plan.get("version", ""))):
        raise ContractError("recipe context needs a numeric version in its local plan")
    number = plan.get("build_number")
    if type(number) is not int or number < 0:
        raise ContractError("recipe context needs a nonnegative local build number")
    environment = {
        "GIT_DESCRIBE_TAG": plan["version"],
        "MOLSYSSUITE_CONDA_VERSION": plan["version"],
        "MOLSYSSUITE_CONDA_BUILD_NUMBER": str(number),
    }
    for key, field in record.get("environment_from_plan", {}).items():
        if not re.fullmatch(r"[A-Z][A-Z0-9_]*", key) or field not in {
            "version",
            "build_number",
        }:
            raise ContractError(
                "recipe context maps only explicit plan version/build inputs"
            )
        environment[key] = str(plan[field])
    result = inspect_recipe_dependencies(
        root,
        record["path"],
        environment,
        aliases,
        python_section=record.get("python_build_section", "host"),
    )
    if "resource_inventory" in record:
        inventory = inspect_resources(root, record["resource_inventory"])
        result["resources"] = {
            "scope": "declared-resources",
            "path": record["resource_inventory"],
            "required_paths": inventory["required_paths"],
            "version_file": inventory["version_file"],
        }
    return result


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
    """Compatibility alias for the independently reusable minor validator."""
    return contracts.narrow_python(required, minor)


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
    context: str | None = None,
    check_installed: bool = False,
    python_version: str | None = None,
) -> dict:
    """Return bounded route evidence; refuse incomplete or inconsistent inputs.

    Source roots must be actual clean checkouts installed into this interpreter.
    This verifies metadata/provenance, not imports, native bytes or scientific use.
    """
    root = root.resolve()
    inventory = tomllib.loads(local_path(root, inventory_path).read_text())
    schema = inventory.get("schema")
    if schema not in {SCHEMA, COMPATIBILITY_SCHEMA, contexts.SCHEMA}:
        raise ContractError(f"expected {SCHEMA} inventory")
    contextual = schema == contexts.SCHEMA
    compatible = schema in {COMPATIBILITY_SCHEMA, contexts.SCHEMA}
    if not contextual and (context is not None or check_installed):
        raise ContractError("context API qualification requires @3")
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
    if contextual:
        if source_roots:
            raise ContractError("@3 Git profile does not accept directory source roots")
        sources, reviewed_contexts, source_inputs = contexts.describe(
            root, inventory, requirements
        )
        if context is not None and context not in reviewed_contexts:
            raise ContractError("unknown reviewed context")
        source_records = []
    else:
        source_records = inventory.get("source_routes", [])
        sources = {
            canonicalize_name(record["name"]): record for record in source_records
        }
    if not contextual and (
        len(sources) != len(source_records) or not set(sources) <= set(requirements)
    ):
        raise ContractError("duplicate or non-required source dependency")
    supplied_roots = source_roots or {}
    if not contextual and set(supplied_roots) != set(sources):
        raise ContractError("provide exactly the inventoried required source checkouts")
    if not sources and not inventory.get("source_reason", "").strip():
        raise ContractError("absence of required source routes needs a review reason")

    evidence = {"schema": schema, "package": project["name"], "routes": []}
    if compatible:
        evidence.update(
            proof_domain="numeric-release-versions",
            installed_check_required=True,
            qualification="declared-only",
        )
    if contextual:
        evidence.update(
            contexts=[],
            source_inputs=source_inputs,
            selected_context=context,
            source_routes=[
                {"id": identity, **record} for identity, record in sources.items()
            ],
        )
    for name, record in [] if contextual else sources.items():
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
            if compatible and recipe["kind"] == "noarch-dependencies":
                result = _local_recipe(root, recipe, aliases)
                evidence["routes"].append(
                    {"path": recipe["path"], "kind": recipe["kind"], **result}
                )
                continue
            if recipe["kind"] != "shared-noarch":
                raise ContractError("recipe kind needs an owned profile")
            plan = recipe["plan"]
            if local_path(root, plan).with_name("meta.yaml") != local_path(
                root, recipe["path"]
            ):
                raise ContractError("plan does not identify this recipe")
            inspect_recipe(root, plan, recipe["resources"])
        except (
            ValueError,
            OSError,
            KeyError,
            TypeError,
            yaml.YAMLError,
            TemplateError,
        ) as error:
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
                if contextual:
                    measured = contexts.audit_environment(
                        environment,
                        content,
                        _compatible_environment(content),
                        reviewed_contexts,
                        sources,
                        requirements,
                        python,
                        aliases,
                    )
                    evidence["contexts"].extend(measured)
                    evidence["routes"].append(
                        {"path": path, "kind": kind, "purpose": environment["purpose"]}
                    )
                    continue
                allowed_channels = [["uibcdf", "conda-forge"]]
                if compatible:
                    allowed_channels.append(["uibcdf", "conda-forge", "nodefaults"])
                if content.get("channels") not in allowed_channels:
                    raise ContractError("runtime channels must be uibcdf, conda-forge")
                if environment.get("channel_priority") != "strict":
                    raise ContractError(
                        "runtime route must record strict channel priority"
                    )
                parsed_items = _compatible_environment(content) if compatible else None
                items = (
                    [str(item.requirement) for item in parsed_items]
                    if parsed_items is not None
                    else _environment_requirements(content)
                )
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
                if compatible:
                    purpose = environment.get("purpose")
                    if purpose not in {
                        "production",
                        "development",
                        "test",
                        "documentation",
                        "optional-runtime",
                    }:
                        raise ContractError("runtime route needs its general purpose")
                    narrowed = contracts.compare_requirements(
                        parsed_items,
                        [python, *expected],
                        aliases,
                        allow_narrowing=purpose != "production",
                        narrowing_reason=environment.get("narrowing_reason", ""),
                    )
                    evidence["routes"].append(
                        {
                            "path": path,
                            "kind": kind,
                            "purpose": purpose,
                            "narrowed": narrowed,
                            "selectors": [
                                {
                                    "original": item.original,
                                    "version_kind": item.version_kind,
                                    "build": item.build,
                                }
                                for item in parsed_items
                            ],
                        }
                    )
                    continue
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
    if contextual and check_installed:
        evidence.update(
            contexts.qualify(
                project,
                reviewed_contexts,
                sources,
                context,
                distribution_for,
                python_version or ".".join(map(str, sys.version_info[:3])),
            )
        )
    return evidence


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--inventory", default="devtools/dependency_routes.toml")
    parser.add_argument(
        "--source-root", action="append", default=[], metavar="NAME=PATH"
    )
    parser.add_argument(
        "--context", help="Select one reviewed @3 environment/Python/source context"
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--check-installed",
        action="store_true",
        help="Also check resolved public bounds",
    )
    mode.add_argument(
        "--declared-only",
        action="store_true",
        help="Offline review only; no installed qualification",
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
        schema = tomllib.loads(
            local_path(args.root.resolve(), args.inventory).read_text()
        ).get("schema")
        result = audit(
            args.root,
            args.inventory,
            source_roots=sources,
            context=args.context,
            check_installed=schema == contexts.SCHEMA and not args.declared_only,
        )
        if result["schema"] != contexts.SCHEMA and (
            args.check_installed
            or (result["schema"] == COMPATIBILITY_SCHEMA and not args.declared_only)
        ):
            project = tomllib.loads(
                local_path(args.root, "pyproject.toml").read_text()
            )["project"]
            result["installed_versions"] = contracts.check_installed(project)
            result["qualification"] = "declared-and-installed-public-bounds"
    except (
        ValueError,
        OSError,
        KeyError,
        TypeError,
        AttributeError,
        yaml.YAMLError,
        TemplateError,
        importlib.metadata.PackageNotFoundError,
    ) as error:
        print(f"Dependency routes rejected: {error}")
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
