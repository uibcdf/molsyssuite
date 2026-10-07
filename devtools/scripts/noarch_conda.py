"""Bind a single noarch Python artifact to its recipe, metadata and resources."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import shlex
import tarfile
from email.parser import Parser
from pathlib import Path, PurePosixPath

import tomllib
import yaml
from jinja2 import StrictUndefined, TemplateError
from jinja2.sandbox import SandboxedEnvironment
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

try:
    from devtools.scripts.conda_release_contract import ContractError, validate_plan
except ModuleNotFoundError:
    from conda_release_contract import ContractError, validate_plan


def local_path(root: Path, relative: str, *, generated: bool = False) -> Path:
    """Resolve a committed input without escaping the component checkout."""
    value = PurePosixPath(relative)
    if value.is_absolute() or ".." in value.parts or not value.parts:
        raise ContractError("release input must be a relative component path")
    path = root.joinpath(*value.parts).resolve()
    if not path.is_relative_to(root.resolve()) or (
        not path.is_file()
        and not (generated and not path.exists() and path.parent.is_dir())
    ):
        raise ContractError(
            f"release input is missing or outside the checkout: {relative}"
        )
    return path


def required_constraints(items: list[str], expected: list[str], aliases: dict) -> None:
    """Reject missing, weakened or duplicate declared runtime constraints."""
    if not isinstance(items, list):
        raise ContractError(
            "runtime requirements need a list declaring: " + ", ".join(expected)
        )
    observed = {}
    for item in items:
        requirement = Requirement(item)
        name = canonicalize_name(requirement.name)
        if name in observed:
            raise ContractError(f"duplicate runtime requirement: {name}")
        observed[name] = requirement
    for item in expected:
        requirement = Requirement(item)
        if requirement.marker or requirement.url:
            raise ContractError(
                "conditional/source metadata needs a reviewed local profile"
            )
        name = canonicalize_name(aliases.get(requirement.name, requirement.name))
        actual = observed.get(name)
        if actual is None or actual.specifier != requirement.specifier:
            raise ContractError(
                f"runtime constraint disagrees with project metadata: {item}"
            )


def render_recipe(root: Path, recipe_path: str, environment: dict) -> tuple[dict, str]:
    """Render one committed recipe in the existing sandbox with explicit inputs.

    This operation parses only; publication identity/resources require their
    separate checks. It never reads process environment variables implicitly.
    """
    source = local_path(root, recipe_path).read_text()
    rendered = (
        SandboxedEnvironment(undefined=StrictUndefined)
        .from_string(source)
        .render(environ=environment)
    )
    recipe = yaml.safe_load(rendered)
    if not isinstance(recipe, dict):
        raise ContractError("recipe must render to a mapping")
    return recipe, source


def inspect_recipe_dependencies(
    root: Path,
    recipe_path: str,
    environment: dict,
    aliases: dict | None = None,
    *,
    python_section: str = "host",
) -> dict:
    """Check public noarch dependency claims independently of publisher layout.

    Local publishers retain their own version/resource/native/file checks; this
    operation does not validate a release plan or authorize a publication.
    """
    if python_section not in {"host", "build"}:
        raise ContractError("Python requirements section must be host or build")
    recipe, source = render_recipe(root, recipe_path, environment)
    if "# [" in source:
        raise ContractError("platform selectors need a reviewed noarch profile")
    project = tomllib.loads(local_path(root, "pyproject.toml").read_text())["project"]
    if canonicalize_name(recipe["package"]["name"]) != canonicalize_name(
        project["name"]
    ):
        raise ContractError("recipe/project package identity differs")
    if recipe["build"].get("noarch") != "python":
        raise ContractError("dependency-only noarch route must declare noarch: python")
    expected = ["python" + project["requires-python"], *project.get("dependencies", [])]
    required_constraints(recipe["requirements"]["run"], expected, aliases or {})
    required_constraints(
        recipe["requirements"][python_section],
        ["python" + project["requires-python"]],
        {},
    )
    result = {"scope": "declared-noarch-dependencies", "package": project["name"]}
    if python_section != "host":
        result["python_build_section"] = python_section
    return result


def inspect_resources(root: Path, inventory_path: str) -> dict:
    """Review declared noarch resources independently of publication orchestration.

    This checks committed source paths and the generated version target only;
    archive bytes and installed behavior require their separate operations.
    """
    inventory = tomllib.loads(local_path(root, inventory_path).read_text())
    paths = inventory.get("required_paths")
    if (
        not isinstance(paths, list)
        or not paths
        or any(not isinstance(value, str) for value in paths)
        or len(paths) != len(set(paths))
    ):
        raise ContractError("resource inventory needs unique required artifact paths")
    if not str(inventory.get("reason", "")).strip():
        raise ContractError(
            "resource inventory needs its applicability/review rationale"
        )
    version_file = inventory.get("version_file")
    for value in paths:
        if (
            not isinstance(value, str)
            or not value.startswith("site-packages/")
            or ".." in PurePosixPath(value).parts
        ):
            raise ContractError(
                "resource paths must name literal noarch site-packages files"
            )
        local_path(
            root, value.removeprefix("site-packages/"), generated=value == version_file
        )
    if version_file not in paths or not version_file.endswith("/_version.py"):
        raise ContractError("inventory must include its embedded Python version module")
    metadata = tomllib.loads(local_path(root, "pyproject.toml").read_text())
    project = metadata["project"]
    external_run_constraints(inventory, project)
    try:
        from devtools.scripts.installed_imports import runtime_import_roots
    except ModuleNotFoundError:
        from installed_imports import runtime_import_roots
    runtime_import_roots(
        inventory, canonicalize_name(project["name"]).replace("-", "_")
    )
    if project.get("dynamic") == ["version"] and metadata.get("tool", {}).get(
        "versioningit", {}
    ).get("write", {}).get("file") != version_file.removeprefix("site-packages/"):
        raise ContractError(
            "generated version target differs from the declared inventory"
        )
    return inventory


def external_run_constraints(inventory: dict, project: dict) -> list[str]:
    """Bind optional non-Python Conda dependencies without certifying behavior."""
    requirements = inventory.get("external_run_requirements", [])
    if not isinstance(requirements, list) or len(requirements) > 100:
        raise ContractError("external runtime requirements need a bounded list")
    reason = inventory.get("external_run_reason", "")
    if requirements and (not isinstance(reason, str) or not reason.strip()):
        raise ContractError("external runtime requirements need a review reason")
    aliases = inventory.get("conda_names", {})
    names = {"python", canonicalize_name(project["name"])}
    for value in project.get("dependencies", []):
        parsed = Requirement(value)
        names.add(canonicalize_name(aliases.get(parsed.name, parsed.name)))
    for value in requirements:
        if not isinstance(value, str) or not re.fullmatch(
            r"[a-zA-Z0-9][a-zA-Z0-9_.-]*\s*[<>=!~][a-zA-Z0-9.*<>=!~, -]+",
            value,
        ):
            raise ContractError(
                "external runtime requirements need ordinary versioned Conda specs"
            )
        parsed = Requirement(value)
        name = canonicalize_name(parsed.name)
        if (
            parsed.marker
            or parsed.url
            or parsed.extras
            or not parsed.specifier
            or name in names
        ):
            raise ContractError(
                "external runtime requirement is conditional, duplicate or reserved"
            )
        names.add(name)
    return list(requirements)


def inspect_recipe(
    root: Path, plan_path: str, inventory_path: str
) -> tuple[dict, dict]:
    """Check the early noarch contract; this does not install or publish anything."""
    plan_file = local_path(root, plan_path)
    plan = tomllib.loads(plan_file.read_text())
    validate_plan(plan)
    if plan["profile"] != "noarch-python":
        raise ContractError("this workflow accepts only the noarch-python profile")
    # A native scientific workflow may succeed with only governance jobs executed.
    # This adapter requires explicit executed-job evidence in addition to its conclusion.
    if not plan.get("gate_jobs") or set(plan["gate_jobs"]) != set(
        plan["required_workflows"]
    ):
        raise ContractError(
            "noarch publication needs declared executed native gate jobs"
        )
    inventory = inspect_resources(root, inventory_path)
    recipe_file = plan_file.with_name("meta.yaml")
    environment = {
        "MOLSYSSUITE_CONDA_VERSION": plan["version"],
        "MOLSYSSUITE_CONDA_BUILD_NUMBER": str(plan["build_number"]),
        "GIT_DESCRIBE_TAG": plan["version"],
    }
    recipe, recipe_source = render_recipe(
        root, str(recipe_file.relative_to(root.resolve())), environment
    )
    metadata = tomllib.loads(local_path(root, "pyproject.toml").read_text())
    project = metadata["project"]
    if canonicalize_name(project["name"]) != plan["package"] or recipe["package"] != {
        "name": plan["package"],
        "version": plan["version"],
    }:
        raise ContractError(
            "recipe/project identity differs from the reviewed package/version"
        )
    build = recipe["build"]
    if (
        build.get("noarch") != "python"
        or build.get("number") != plan["build_number"]
        or build.get("string") != f"py_{plan['build_number']}"
    ):
        raise ContractError(
            "recipe must build the planned single noarch Python coordinate"
        )
    if "# [" in recipe_source:
        raise ContractError("platform selectors need a reviewed local noarch profile")
    requirements = recipe["requirements"]["run"]
    expected = [
        "python" + project["requires-python"],
        *project.get("dependencies", []),
        *external_run_constraints(inventory, project),
    ]
    required_constraints(requirements, expected, inventory.get("conda_names", {}))
    required_constraints(
        recipe["requirements"]["host"], ["python" + project["requires-python"]], {}
    )
    scripts = project.get("scripts", {})
    entries = build.get("entry_points", [])
    if not isinstance(entries, list) or sorted(entries) != sorted(
        f"{name} = {target}" for name, target in scripts.items()
    ):
        raise ContractError("recipe console entry points differ from project.scripts")
    inventory["expected_run"] = expected
    inventory["conda_names"] = inventory.get("conda_names", {})
    inventory["import_name"] = inventory.get(
        "import_name", plan["package"].replace("-", "_")
    )
    return plan, inventory


def freeze_version(root: Path, plan: dict, inventory: dict) -> None:
    """Freeze reviewed version metadata only in the ephemeral build checkout.

    The bounded adapter supports setuptools/versioningit with one dynamic version.
    Other build backends require a reviewed local implementation.
    """
    project_file = local_path(root, "pyproject.toml")
    source = project_file.read_text()
    metadata = tomllib.loads(source)
    if metadata["build-system"]["build-backend"] != "setuptools.build_meta" or metadata[
        "project"
    ].get("dynamic") != ["version"]:
        raise ContractError(
            "static-version preparation needs the reviewed setuptools/versioningit profile"
        )
    relative = inventory["version_file"].removeprefix("site-packages/")
    if metadata["tool"]["versioningit"]["write"]["file"] != relative:
        raise ContractError(
            "versioningit target differs from the reviewed version resource"
        )
    target = local_path(root, relative, generated=True)
    lines, section, changes = [], "", 0
    for line in source.splitlines(keepends=True):
        if line.strip().startswith("["):
            section = line.strip()
        if section == "[tool.versioningit]" or section.startswith(
            "[tool.versioningit."
        ):
            continue
        if section == "[project]" and re.match(r"^dynamic\s*=", line):
            line = f'version = "{plan["version"]}"\n'
            changes += 1
        lines.append(line)
    frozen = "".join(lines)
    if (
        changes != 1
        or tomllib.loads(frozen)["project"].get("version") != plan["version"]
    ):
        raise ContractError("cannot prepare unambiguous static project version")
    project_file.write_text(frozen)
    target.write_text(f'__version__ = "{plan["version"]}"\n')


def embedded_version(source: str) -> str:
    """Read a single literal version assignment without executing package code."""
    values = []
    for node in ast.parse(source).body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "__version__"
            for target in node.targets
        ):
            if not isinstance(node.value, ast.Constant) or not isinstance(
                node.value.value, str
            ):
                raise ContractError("embedded version is not a literal string")
            values.append(node.value.value)
    if len(values) != 1:
        raise ContractError("embedded version is absent or ambiguous")
    return values[0]


def inspect_artifact(path: Path, plan: dict, inventory: dict) -> dict:
    """Inspect the exact tar.bz2 without extracting or importing its contents."""
    filename = f"{plan['package']}-{plan['version']}-py_{plan['build_number']}.tar.bz2"
    if path.name != filename or not path.is_file():
        raise ContractError("built file differs from the planned immutable coordinate")
    with tarfile.open(path, "r:bz2") as archive:
        members = archive.getmembers()
        if len(members) > 100000:
            raise ContractError("artifact path inventory exceeds its review bound")
        names = [member.name for member in members]
        if len(names) != len(set(names)):
            raise ContractError("artifact has duplicate path identities")
        for member in members:
            name = PurePosixPath(member.name)
            if (
                name.is_absolute()
                or ".." in name.parts
                or member.issym()
                or member.islnk()
            ):
                raise ContractError("artifact contains an unsafe or linked path")
            if not member.name.startswith("info/") and member.isfile():
                with archive.extractfile(member) as stream:
                    header = stream.read(4)
                if (
                    name.suffix.lower() in {".so", ".pyd", ".dll", ".dylib", ".exe"}
                    or header.startswith((b"\x7fELF", b"MZ"))
                    or header
                    in {
                        b"\xfe\xed\xfa\xce",
                        b"\xce\xfa\xed\xfe",
                        b"\xfe\xed\xfa\xcf",
                        b"\xcf\xfa\xed\xfe",
                        b"\xca\xfe\xba\xbe",
                    }
                ):
                    raise ContractError(
                        "noarch Python payload contains a native binary"
                    )
        for name in inventory["required_paths"]:
            if name not in names or not archive.getmember(name).isfile():
                raise ContractError(f"required artifact resource is missing: {name}")
        version_member = archive.getmember(inventory["version_file"])
        if version_member.size > 1024 * 1024:
            raise ContractError("embedded version module exceeds its bound")
        with archive.extractfile(version_member) as stream:
            if embedded_version(stream.read().decode("utf-8")) != plan["version"]:
                raise ContractError(
                    "embedded Python version differs from the Conda coordinate"
                )
        member = archive.getmember("info/index.json")
        if not member.isfile() or member.size > 1024 * 1024:
            raise ContractError("artifact metadata is not a bounded regular file")
        with archive.extractfile(member) as stream:
            index = json.load(stream)
        link = archive.getmember("info/link.json")
        if not link.isfile() or link.size > 1024 * 1024:
            raise ContractError("noarch install metadata is not a bounded regular file")
        with archive.extractfile(link) as stream:
            if json.load(stream).get("noarch", {}).get("type") != "python":
                raise ContractError(
                    "artifact does not declare noarch Python installation"
                )
        expected = {
            "name": plan["package"],
            "version": plan["version"],
            "build": f"py_{plan['build_number']}",
            "build_number": plan["build_number"],
            "subdir": "noarch",
        }
        if any(index.get(key) != value for key, value in expected.items()):
            raise ContractError(
                "embedded artifact metadata differs from the candidate coordinate"
            )
        required_constraints(
            index["depends"], inventory["expected_run"], inventory["conda_names"]
        )
        metadata_path = f"site-packages/{plan['package'].replace('-', '_')}-{plan['version']}.dist-info/METADATA"
        metadata_member = archive.getmember(metadata_path)
        if not metadata_member.isfile() or metadata_member.size > 1024 * 1024:
            raise ContractError("installed distribution metadata exceeds its bound")
        with archive.extractfile(metadata_member) as stream:
            metadata = Parser().parsestr(stream.read().decode("utf-8"))
        if metadata.get_all("Version") != [plan["version"]] or metadata.get_all(
            "Name"
        ) != [plan["package"]]:
            raise ContractError(
                "Python installed distribution identity differs from Conda"
            )
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    return {
        "package": plan["package"],
        "version": plan["version"],
        "subdir": "noarch",
        "filename": filename,
        "sha256": digest,
        "artifact": str(path.resolve()),
    }


def promotion_descriptor(root: Path, plan: dict, inventory: dict, digest: str) -> dict:
    """Bind the installed gate title and every cell to the exact proposed file."""
    try:
        from devtools.scripts.verify_installed_matrix import expected_jobs
    except ModuleNotFoundError:
        from verify_installed_matrix import expected_jobs
    if plan["route"] != "staged" or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise ContractError(
            "promotion requires a staged plan and exact artifact digest"
        )
    gate = inventory.get("installed_gate", {})
    workflow = gate.get("workflow", "")
    local_path(root, workflow)
    if not workflow.startswith(".github/workflows/") or not workflow.endswith(
        (".yaml", ".yml")
    ):
        raise ContractError("installed gate needs a committed component workflow")
    profile = {
        key: gate[key]
        for key in (
            "platforms",
            "python_versions",
            "prepare_job",
            "required_steps",
            "job_template",
        )
    }
    if (
        profile["platforms"] != plan["test_platforms"]
        or profile["python_versions"] != plan["python_versions"]
    ):
        raise ContractError("installed gate differs from every claimed plan cell")
    expected_jobs(profile)
    filename = f"{plan['package']}-{plan['version']}-py_{plan['build_number']}.tar.bz2"
    return {
        "workflow": workflow,
        "profile": json.dumps(profile),
        "title": f"Installed {filename} {digest}",
        "filename": filename,
        "package": plan["package"],
        "version": plan["version"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--plan", default="devtools/conda-build/release_plan.toml")
    parser.add_argument("--inventory", default="devtools/conda-build/resources.toml")
    parser.add_argument(
        "--built-paths", help="Exact producer built_paths output; one tar.bz2 only"
    )
    parser.add_argument(
        "--freeze-version", action="store_true", help="Ephemeral build checkout only"
    )
    parser.add_argument(
        "--promotion-sha256", help="Acquire the committed installed-gate descriptor"
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument("--github-output", type=Path)
    args = parser.parse_args()
    try:
        plan, inventory = inspect_recipe(args.root, args.plan, args.inventory)
        result = {
            "package": plan["package"],
            "version": plan["version"],
            "build_number": plan["build_number"],
            "route": plan["route"],
        }
        if args.freeze_version:
            freeze_version(args.root, plan, inventory)
        if args.promotion_sha256 is not None:
            result.update(
                promotion_descriptor(args.root, plan, inventory, args.promotion_sha256)
            )
        if args.built_paths is not None:
            paths = shlex.split(args.built_paths)
            if len(paths) != 1:
                raise ContractError("a noarch publisher must build exactly one file")
            result.update(inspect_artifact(Path(paths[0]), plan, inventory))
        if args.output:
            args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        if args.github_output:
            with args.github_output.open("a") as stream:
                for key, value in result.items():
                    stream.write(f"{key}={value}\n")
    except (
        OSError,
        ValueError,
        KeyError,
        TypeError,
        yaml.YAMLError,
        TemplateError,
        tarfile.TarError,
    ) as error:
        print(f"Noarch candidate rejected: {error}")
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
