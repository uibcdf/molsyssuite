"""Opt-in environment generation and checked Conda/Mamba management.

Owner selections and tooling stay local. Existing dependency/context operations
own range and source proofs. This module never builds or qualifies a release.
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path, PurePosixPath
from tempfile import TemporaryDirectory

import tomllib
import yaml
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

if not __package__:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from devtools.scripts import dependency_constraints as contracts
from devtools.scripts import dependency_route_contexts as contexts
from devtools.scripts import dependency_routes as routes
from devtools.scripts.noarch_conda import ContractError, local_path

SCHEMA = "molsyssuite.environment-tools@1"
DEFAULT_PROFILE = "devtools/environment_tools.toml"


def flatten(values: list) -> list[str]:
    """Read nested owner tooling lists without executing or interpreting them."""
    if not isinstance(values, list):
        raise ContractError("tooling groups must be lists")
    result = []
    for value in values:
        if isinstance(value, list):
            items = flatten(value)
        elif isinstance(value, str) and value.strip():
            items = [value]
        else:
            raise ContractError("tooling groups need nonempty strings")
        for item in items:
            if item not in result:
                result.append(item)
    return result


def _inputs(root: Path, inventory_path: str) -> tuple:
    project = tomllib.loads(local_path(root, "pyproject.toml").read_text())["project"]
    if "dependencies" in project.get("dynamic", []):
        raise ContractError("dynamic dependencies require an owner profile")
    runtime = {}
    for value in project.get("dependencies", []):
        parsed = contracts.pip_requirement(value).requirement
        name = canonicalize_name(parsed.name)
        if name in runtime or name == "python":
            raise ContractError("duplicate/invalid runtime metadata")
        runtime[name] = value
    contracts.release_range(
        Requirement("python" + project["requires-python"]).specifier
    )
    inventory = tomllib.loads(local_path(root, inventory_path).read_text())
    if inventory.get("schema") != contexts.SCHEMA:
        raise ContractError("environment operations require dependency-routes@3")
    sources, selections, _ = contexts.describe(root, inventory, runtime)
    records = {}
    for record in inventory.get("environments", []):
        path = record["path"]
        if path in records:
            raise ContractError("duplicate environment route")
        contexts.reason(record)
        records[path] = record
    return project, runtime, inventory, sources, selections, records


def _environment_path(root: Path, relative: str) -> Path:
    """Restrict operations to existing registered owner environment documents."""
    value = PurePosixPath(relative)
    if (
        value.parent != PurePosixPath("devtools/conda-envs")
        or value.suffix not in {".yaml", ".yml"}
        or value.name in {"meta.yaml", "recipe.yaml"}
    ):
        raise ContractError("select an ordinary registered environment YAML")
    path = local_path(root, relative)
    # Do not replace another file through an alias, even inside the repository.
    if path != root.resolve() / relative:
        raise ContractError("environment symlink needs owner review")
    return path


def _document(path: Path) -> dict:
    content = yaml.safe_load(path.read_text())
    if not isinstance(content, dict) or set(content) - {
        "name",
        "prefix",
        "channels",
        "dependencies",
    }:
        raise ContractError("specialized environment fields need owner review")
    channels = content.get("channels")
    if (
        not isinstance(channels, list)
        or not channels
        or any(
            not isinstance(c, str) or not re.fullmatch(r"[A-Za-z0-9_-]+", c)
            for c in channels
        )
        or len(channels) != len(set(channels))
    ):
        raise ContractError("environment needs unique literal channels")
    items = routes._compatible_environment(content)
    if not items:
        raise ContractError("environment needs dependencies")
    if sum(canonicalize_name(i.requirement.name) == "python" for i in items) > 1:
        raise ContractError("duplicate Python selectors")
    return content


def _python(project: dict, content: dict, minor: str | None) -> str:
    python_items = [
        item
        for item in routes._compatible_environment(content)
        if canonicalize_name(item.requirement.name) == "python"
    ]
    if python_items and python_items[0].build:
        raise ContractError("Python build selection requires explicit owner review")
    selected = (
        contracts.narrow_python(project["requires-python"], minor)[1]
        if minor is not None
        else "python" + project["requires-python"]
    )
    expected = ["python" + project["requires-python"]]
    if python_items:
        expected.append(str(python_items[0].requirement))
    for required in expected:
        contracts.compare_requirements(
            [contracts.conda_requirement(selected)],
            [required],
            allow_narrowing=True,
            narrowing_reason="Explicit environment selection",
        )
    return selected


def _validate(content: dict, record: dict, inputs: tuple, *, minor=None) -> None:
    project, runtime, inventory, sources, selections, _ = inputs
    items = routes._compatible_environment(content)
    if record["kind"] == "build-only":
        return
    if record["kind"] != "runtime":
        raise ContractError("environment kind requires an owner profile")
    selected = {
        k: copy.deepcopy(v)
        for k, v in selections.items()
        if v["environment"] == record["path"]
    }
    if minor is not None:
        sourced = [v for v in selected.values() if v.get("sources")]
        if sourced:
            selected = {k: v for k, v in selected.items() if v["python_minor"] == minor}
            if not selected:
                raise ContractError(
                    "Python minor differs from the fixed-source context"
                )
        else:
            # This is a selection proof, not a new installed-context receipt.
            for v in selected.values():
                v["python_minor"] = minor
    if not selected:
        raise ContractError("runtime environment has no reviewed context")
    contexts.audit_environment(
        record,
        content,
        items,
        selected,
        sources,
        runtime,
        contracts.narrow_python(project["requires-python"], minor)[1]
        if minor is not None
        else "python" + project["requires-python"],
        inventory.get("conda_names", {}),
    )


def environment_documents(
    root: Path,
    profile_path: str = DEFAULT_PROFILE,
) -> dict[str, str]:
    """Validate and render only explicit owner outputs; perform no writes."""
    root = root.resolve()
    profile = tomllib.loads(local_path(root, profile_path).read_text())
    if profile.get("schema") != SCHEMA:
        raise ContractError(f"expected {SCHEMA}")
    inputs = _inputs(root, profile.get("inventory", "devtools/dependency_routes.toml"))
    project, runtime, inventory, sources, selections, records = inputs
    groups = yaml.safe_load(local_path(root, profile["tooling"]).read_text())
    if not isinstance(groups, dict):
        raise ContractError("owner tooling needs a mapping")
    documents = {}
    outputs = profile.get("environments")
    if not isinstance(outputs, list) or not outputs:
        raise ContractError("select nonempty environment outputs")
    for output in outputs:
        contexts.reason(output)
        relative = output["path"]
        path = _environment_path(root, relative)
        if relative in documents or relative not in records:
            raise ContractError("duplicate or unregistered output")
        record = records[relative]
        if record["kind"] not in {"runtime", "build-only"}:
            raise ContractError("specialized environment is not a generation target")
        original = _document(path)
        group = groups[output["group"]]
        if not isinstance(group, dict):
            raise ContractError("tooling group needs a mapping")
        channels = flatten(group["channels"])
        if channels != original["channels"]:
            raise ContractError("generation cannot change reviewed channels")
        minor = output.get("python_minor")
        if record.get("purpose") == "development" and minor != "3.14":
            raise ContractError("routine development requires Python 3.14")
        python = _python(project, original, minor)
        required = dict(runtime) if record["kind"] == "runtime" else {}
        selected_contexts = [
            v for v in selections.values() if v["environment"] == relative
        ]
        replacements = []
        for context in selected_contexts:
            replacements.append(
                {
                    sources[s]["name"]
                    for s in context.get("sources", [])
                    if sources[s]["role"] == "required-runtime"
                    and sources[s]["name"] not in context.get("overlays", [])
                }
            )
        if replacements and any(r != replacements[0] for r in replacements):
            raise ContractError(
                "contexts need different bootstrap documents; owner review"
            )
        for name in replacements[0] if replacements else []:
            required.pop(name)
        aliases = inventory.get("conda_names", {})
        reserved = {canonicalize_name(aliases.get(n, n)) for n in runtime}
        tools = flatten(group["dependencies"])
        for tool in tools:
            name = canonicalize_name(contracts.conda_requirement(tool).requirement.name)
            if name == "python" or (record["kind"] == "runtime" and name in reserved):
                raise ContractError(
                    "metadata/context owns Python and runtime, not tooling"
                )
        dependencies = [python, *tools]
        for value in required.values():
            requirement = Requirement(value)
            name = canonicalize_name(requirement.name)
            dependencies.append(
                aliases.get(name, requirement.name) + str(requirement.specifier)
            )
        content = {"channels": channels, "dependencies": dependencies}
        # A generator may propagate a new metadata floor, but must not erase an
        # existing scientific/tool selector for a dependency it retains.
        previous = {
            canonicalize_name(i.requirement.name): i
            for i in routes._compatible_environment(original)
        }
        for item in routes._compatible_environment(content):
            name = canonicalize_name(item.requirement.name)
            if name in previous:
                if previous[name].build != item.build:
                    raise ContractError(
                        "generation would change a reviewed build selector"
                    )
                contracts.compare_requirements(
                    [item],
                    [str(previous[name].requirement)],
                    allow_narrowing=True,
                    narrowing_reason=output["reason"],
                )
        _validate(content, record, inputs)
        documents[relative] = yaml.safe_dump(content, sort_keys=False)
    return documents


def generate(
    root: Path, profile_path: str = DEFAULT_PROFILE, *, check=False
) -> list[str]:
    """Validate all outputs before writes; drift mode is always non-mutating."""
    documents = environment_documents(root, profile_path)
    changed = [
        name for name, value in documents.items() if (root / name).read_text() != value
    ]
    if check and changed:
        raise ContractError("generated environments differ: " + ", ".join(changed))
    if not check:
        for name in changed:
            (root / name).write_text(documents[name])
    return changed


def selected_environment(
    root: Path,
    relative: str,
    minor: str,
    *,
    inventory_path: str = "devtools/dependency_routes.toml",
) -> dict:
    """Narrow a registered document without widening metadata or source selection."""
    inputs = _inputs(root, inventory_path)
    project, _, _, _, _, records = inputs
    if relative not in records:
        raise ContractError("unregistered environment")
    record = records[relative]
    if record.get("purpose") == "development" and minor != "3.14":
        raise ContractError("routine development requires Python 3.14")
    content = _document(_environment_path(root, relative))
    _validate(content, record, inputs)
    python = _python(project, content, minor)
    result = copy.deepcopy(content)
    result["dependencies"] = [python] + [
        item
        for item in result["dependencies"]
        if not isinstance(item, str)
        or canonicalize_name(contracts.conda_requirement(item).requirement.name)
        != "python"
    ]
    result.pop("name", None)
    result.pop("prefix", None)
    _validate(result, record, inputs, minor=minor)
    return result


def apply_environment(
    root: Path,
    relative: str,
    minor: str,
    *,
    manager: str,
    name: str | None = None,
    prefix: Path | None = None,
    inventory_path: str = "devtools/dependency_routes.toml",
) -> dict:
    """Create a new name or update this active prefix; propagate every failure."""
    if (name is None) == (prefix is None):
        raise ContractError("select exactly one new name or active prefix")
    if name is not None and (
        name == "base" or not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_.@-]*", name)
    ):
        raise ContractError("invalid new environment name")
    if prefix is not None:
        prefix = prefix.resolve()
        active = os.environ.get("CONDA_PREFIX")
        if (
            not active
            or Path(active).resolve() != prefix
            or Path(sys.prefix).resolve() != prefix
            or not (prefix / "conda-meta").is_dir()
        ):
            raise ContractError(
                "update requires this interpreter's active Conda prefix"
            )
    content = selected_environment(root, relative, minor, inventory_path=inventory_path)
    executable = shutil.which(manager)
    if not executable:
        raise ContractError("explicit manager does not identify an executable")
    environment = {**os.environ, "CONDA_CHANNEL_PRIORITY": "strict"}
    if name is not None:
        response = subprocess.run(
            [executable, "env", "list", "--json"],
            check=True,
            capture_output=True,
            text=True,
            env=environment,
        )
        occupied = json.loads(response.stdout).get("envs")
        if not isinstance(occupied, list) or any(
            not isinstance(p, str) for p in occupied
        ):
            raise ContractError("manager returned an invalid environment inventory")
        if any(Path(p).name == name for p in occupied):
            raise ContractError("create requires an unoccupied new name")
    with TemporaryDirectory(prefix="molsyssuite-environment-") as temporary:
        manifest = Path(temporary) / "environment.yaml"
        manifest.write_text(yaml.safe_dump(content, sort_keys=False))
        arguments = (
            ["create", "--name", name] if name else ["update", "--prefix", str(prefix)]
        )
        subprocess.run(
            [executable, "env", *arguments, "--file", str(manifest)],
            check=True,
            env=environment,
        )
    return {
        "operation": arguments[0],
        "environment": relative,
        "python_minor": minor,
        "manager": executable,
        "target": name or str(prefix),
        "scope": "manager execution only; no science or release qualification",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    subparsers = parser.add_subparsers(dest="operation", required=True)
    generator = subparsers.add_parser("generate")
    generator.add_argument("--profile", default=DEFAULT_PROFILE)
    generator.add_argument("--check", action="store_true")
    for operation in ("create", "update"):
        command = subparsers.add_parser(operation)
        command.add_argument("environment")
        command.add_argument("--python-minor", required=True)
        command.add_argument("--manager", required=True)
        command.add_argument("--inventory", default="devtools/dependency_routes.toml")
        command.add_argument(
            "--name" if operation == "create" else "--prefix", required=True
        )
    args = parser.parse_args()
    try:
        if args.operation == "generate":
            result = {
                "changed": generate(args.root.resolve(), args.profile, check=args.check)
            }
        else:
            target = (
                {"name": args.name}
                if args.operation == "create"
                else {"prefix": Path(args.prefix)}
            )
            result = apply_environment(
                args.root.resolve(),
                args.environment,
                args.python_minor,
                manager=args.manager,
                inventory_path=args.inventory,
                **target,
            )
    except (
        ValueError,
        OSError,
        KeyError,
        TypeError,
        subprocess.SubprocessError,
        yaml.YAMLError,
    ) as exc:
        print(f"Environment operation: FAIL — {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
