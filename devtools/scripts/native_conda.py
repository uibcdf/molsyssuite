"""Audit bounded ABI3 recipe declarations without building or admitting bytes.

Native archive layout, architecture/ABI, resources and installed science remain
component-owned. Publication orchestration reuses the general Conda contracts.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

import tomllib
from packaging.utils import canonicalize_name
from packaging.version import Version

try:
    from devtools.scripts import dependency_constraints as constraints
    from devtools.scripts.conda_release_contract import ContractError, validate_plan
    from devtools.scripts.noarch_conda import local_path, render_recipe
except ModuleNotFoundError:
    import dependency_constraints as constraints
    from conda_release_contract import ContractError, validate_plan
    from noarch_conda import local_path, render_recipe


def inspect_rendered_dependencies(
    recipe: dict,
    project: dict,
    plan: dict,
    abi3_minimum: str,
    aliases: dict | None = None,
) -> dict:
    """Check one rendered native declaration, not its producer or emitted files.

    This independently usable operation also accepts an actual conda-build
    rendering. Its caller still owns source/render binding and run exports.
    """
    validate_plan(plan)
    if "dependencies" in project.get("dynamic", []):
        raise ContractError("dynamic runtime dependencies need an owned profile")
    if plan["profile"] != "native-abi3":
        raise ContractError("native recipe needs a native-abi3 plan")
    if not re.fullmatch(r"3\.\d+", abi3_minimum):
        raise ContractError("ABI3 minimum must name one CPython major.minor")
    # The bounded initial profile builds against the oldest advertised minor.
    lower = constraints.release_range(
        constraints.pip_requirement(
            "python" + project["requires-python"]
        ).requirement.specifier
    )[0]
    if lower != Version(abi3_minimum):
        raise ContractError("ABI3 minimum must match the advertised Python floor")
    for minor in plan["python_versions"]:
        constraints.narrow_python(project["requires-python"], minor)
        if Version(minor) < Version(abi3_minimum):
            raise ContractError("installed Python matrix crosses the ABI3 minimum")
    package = recipe.get("package", {})
    if (
        canonicalize_name(package.get("name", "")) != canonicalize_name(project["name"])
        or package.get("name") != plan["package"]
        or str(package.get("version")) != plan["version"]
    ):
        raise ContractError("native recipe/project/plan package identity differs")
    if "outputs" in recipe:
        raise ContractError("multiple native outputs need a reviewed profile")
    build = recipe.get("build", {})
    if "noarch" in build or "noarch_python" in build:
        raise ContractError("native recipe must not declare a noarch build")
    if build.get("python_version_independent") is not True:
        raise ContractError("native ABI3 recipe needs python_version_independent: true")
    if type(build.get("number")) is not int or build["number"] != plan["build_number"]:
        raise ContractError("native recipe build number differs from its plan")
    if build.get("skip") not in (None, False):
        raise ContractError("skipped native recipe cannot establish a runtime route")
    requirements = recipe.get("requirements", {})
    run = requirements.get("run")
    host = requirements.get("host")
    if any(
        not isinstance(items, list) or any(not isinstance(v, str) for v in items)
        for items in (run, host)
    ):
        raise ContractError("native host/run requirements must be lists of strings")
    constraints.compare_requirements(
        [constraints.conda_requirement(item) for item in run],
        ["python" + project["requires-python"], *project.get("dependencies", [])],
        aliases,
    )
    constraints.compare_requirements(
        [constraints.conda_requirement(item) for item in host],
        [f"python=={abi3_minimum}.*", f"python-abi3=={abi3_minimum}.*"],
    )
    if any(
        canonicalize_name(constraints.conda_requirement(item).requirement.name)
        == "python-abi"
        for item in run
    ):
        raise ContractError("native ABI3 route retains a minor-specific python_abi")
    return {
        "scope": "declared-native-abi3-dependencies",
        "package": project["name"],
        "abi3_minimum": abi3_minimum,
        "artifact_subdirs": plan["artifact_subdirs"],
        "python_versions": plan["python_versions"],
        "qualification": "declared-only",
        "native_bytes_verified": False,
    }


def _compiler(language: str) -> str:
    """Parse a compiler declaration without resolving or qualifying a toolchain."""
    if language not in {"c", "cxx", "fortran", "rust"}:
        raise ContractError("compiler declaration needs a reviewed language profile")
    return language + "-compiler"


def inspect_recipe_dependencies(
    root: Path,
    recipe_path: str,
    plan_path: str,
    abi3_minimum: str,
    aliases: dict | None = None,
    *,
    environment_from_plan: dict | None = None,
) -> dict:
    """Audit one selector-free meta.yaml with explicit version/build inputs.

    compiler() is a declaration placeholder, never conda-build's resolved
    compiler. PKG_HASH is deliberately symbolic. Conditional selectors, unknown
    macros and multi-output recipes fail for an owned extension/equivalent.
    """
    paths = (recipe_path, plan_path, "pyproject.toml")
    inputs = {path: local_path(root, path).read_bytes() for path in paths}
    plan = tomllib.loads(inputs[plan_path].decode("utf-8"))
    validate_plan(plan)
    project = tomllib.loads(inputs["pyproject.toml"].decode("utf-8"))["project"]
    environment = {
        "GIT_DESCRIBE_TAG": plan["version"],
        "MOLSYSSUITE_CONDA_VERSION": plan["version"],
        "MOLSYSSUITE_CONDA_BUILD_NUMBER": str(plan["build_number"]),
    }
    for key, field in (environment_from_plan or {}).items():
        if not re.fullmatch(r"[A-Z][A-Z0-9_]*", key) or field not in {
            "version",
            "build_number",
        }:
            raise ContractError(
                "recipe context maps only explicit plan version/build inputs"
            )
        environment[key] = str(plan[field])
    recipe, source = render_recipe(
        root,
        recipe_path,
        environment,
        template_context={
            "compiler": _compiler,
            "PKG_HASH": "DECLARED_ONLY",
            "PKG_BUILDNUM": plan["build_number"],
            "PYTHON": "DECLARED_PYTHON",
        },
    )
    if re.search(r"#\s*\[", source):
        raise ContractError("native selectors need per-platform rendered review")
    result = inspect_rendered_dependencies(recipe, project, plan, abi3_minimum, aliases)
    if any(
        local_path(root, path).read_bytes() != content
        for path, content in inputs.items()
    ):
        raise ContractError("native recipe inputs changed during the audit")
    result["rendering"] = "bounded-declaration-not-conda-build"
    result["input_sha256"] = {
        path: hashlib.sha256(content).hexdigest() for path, content in inputs.items()
    }
    return result
