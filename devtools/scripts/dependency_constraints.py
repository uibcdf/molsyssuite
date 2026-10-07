"""Compare declared release ranges and verify actual installed public bounds.

The symbolic proof covers numeric release versions, with whole-segment Conda
prefix matching. It is deliberately paired with installed-version checks, which
also catch prereleases admitted by a selector but excluded by a public floor.
Unsupported expressions require review, never a successful guessed comparison.
"""

from __future__ import annotations

import importlib.metadata
import re
import sys
from dataclasses import dataclass

from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet
from packaging.utils import canonicalize_name
from packaging.version import Version

try:
    from devtools.scripts.conda_release_contract import ContractError
except ModuleNotFoundError:
    from conda_release_contract import ContractError

NUMBER = r"\d+(?:\.\d+)*"


@dataclass(frozen=True)
class RouteRequirement:
    """Keep the original selector and build independently of the range proof."""

    requirement: Requirement
    original: str
    version_kind: str = "range"
    build: str | None = None


def _prefix(value: str) -> tuple[Version, Version]:
    parts = [int(part) for part in value.split(".")]
    upper = [*parts[:-1], parts[-1] + 1]
    return Version(value), Version(".".join(map(str, upper)))


def release_range(specifier: SpecifierSet) -> tuple:
    """Prove a single interval over numeric releases, including open endpoints."""
    lower, lower_closed, upper, upper_closed = None, False, None, False

    def intersect(lo=None, lc=False, hi=None, hc=False):
        nonlocal lower, lower_closed, upper, upper_closed
        if lo is not None:
            if lower is None or lo > lower:
                lower, lower_closed = lo, lc
            elif lo == lower:
                lower_closed = lower_closed and lc
        if hi is not None:
            if upper is None or hi < upper:
                upper, upper_closed = hi, hc
            elif hi == upper:
                upper_closed = upper_closed and hc

    for rule in specifier:
        value = rule.version
        if rule.operator == "==" and value.endswith(".*"):
            if not re.fullmatch(NUMBER, value[:-2]):
                raise ContractError("unsupported release prefix; review required")
            lo, hi = _prefix(value[:-2])
            intersect(lo, True, hi, False)
            continue
        if not re.fullmatch(NUMBER, value):
            raise ContractError("non-release constraint needs review")
        version = Version(value)
        if rule.operator == ">=":
            intersect(lo=version, lc=True)
        elif rule.operator == ">":
            intersect(lo=version)
        elif rule.operator == "<=":
            intersect(hi=version, hc=True)
        elif rule.operator == "<":
            intersect(hi=version)
        elif rule.operator == "==":
            intersect(version, True, version, True)
        elif rule.operator == "~=":
            parts = value.split(".")
            if len(parts) < 2:
                raise ContractError("compatible release needs two version segments")
            _, hi = _prefix(".".join(parts[:-1]))
            intersect(version, True, hi, False)
        else:
            raise ContractError("unsupported release operator; review required")
    if (
        lower is not None
        and upper is not None
        and (lower > upper or (lower == upper and not (lower_closed and upper_closed)))
    ):
        raise ContractError("empty release range")
    return lower, lower_closed, upper, upper_closed


def conda_requirement(item: str) -> RouteRequirement:
    """Read bounded Conda selectors without discarding version/build semantics.

    Single '=' without a build is a prefix; name=version=build binds an exact
    version and retains the build. The normalized range describes releases only,
    not all versions the Conda solver could select. No file is rewritten.
    """
    match = re.fullmatch(r"([A-Za-z0-9_.-]+)\s*(.*)", item.strip())
    if not match:
        raise ContractError("invalid Conda requirement")
    name, expression = match.groups()
    expression = expression.strip()
    pin = re.fullmatch(
        rf"(==|=)?({NUMBER})(\.\*)?(?:\s*=\s*([A-Za-z0-9_.*-]+))?",
        expression,
    )
    kind, build = "range", None
    if pin:
        operator, value, wildcard, build = pin.groups()
        if wildcard and (build or operator == "=="):
            raise ContractError(
                "unsupported wildcard/build combination; review required"
            )
        if (operator == "=" and build is None) or wildcard:
            lo, hi = _prefix(value)
            expression, kind = f">={lo},<{hi}", "prefix"
        else:
            expression, kind = f"=={value}", "exact"
    elif expression and not re.fullmatch(
        rf"(?:>=|<=|>|<|==|~=){NUMBER}(?:\s*,\s*(?:>=|<=|>|<|==|~=){NUMBER})*",
        expression,
    ):
        raise ContractError(f"unsupported Conda expression; review required: {item}")
    requirement = Requirement(name + expression)
    release_range(requirement.specifier)
    return RouteRequirement(requirement, item, kind, build)


def pip_requirement(item: str) -> RouteRequirement:
    """Retain an unconditional PEP 440 selection for the same bounded proof."""
    requirement = Requirement(item)
    if requirement.marker or requirement.url or requirement.extras:
        raise ContractError("conditional/source/extra route needs review")
    release_range(requirement.specifier)
    return RouteRequirement(requirement, item, "pep440")


def _subset(actual: tuple, required: tuple) -> bool:
    lo, lc, hi, hc = actual
    rlo, rlc, rhi, rhc = required
    return (
        rlo is None
        or (lo is not None and (lo > rlo or (lo == rlo and (rlc or not lc))))
    ) and (
        rhi is None
        or (hi is not None and (hi < rhi or (hi == rhi and (rhc or not hc))))
    )


def compare_requirements(
    items: list[RouteRequirement],
    expected: list[str],
    aliases: dict | None = None,
    *,
    allow_narrowing: bool = False,
    narrowing_reason: str = "",
) -> list[str]:
    """Check every required name and range; return justified narrowed names.

    Public routes retain the advertised numeric release interval. Development,
    test and documentation routes may narrow it with an explicit review reason.
    This does not infer solver results, build provenance or scientific support.
    """
    aliases = aliases or {}
    observed = {}
    for item in items:
        name = canonicalize_name(item.requirement.name)
        if name in observed:
            raise ContractError(f"duplicate runtime requirement: {name}")
        observed[name] = item
    narrowed = []
    for value in expected:
        requirement = Requirement(value)
        if requirement.marker or requirement.url or requirement.extras:
            raise ContractError("conditional/source/extra metadata needs review")
        name = canonicalize_name(aliases.get(requirement.name, requirement.name))
        if name not in observed:
            raise ContractError(f"missing runtime requirement: {name}")
        actual = release_range(observed[name].requirement.specifier)
        required = release_range(requirement.specifier)
        if not _subset(actual, required):
            raise ContractError(
                f"{observed[name].original} violates public {requirement}"
            )
        if actual != required:
            if not allow_narrowing:
                raise ContractError(f"{name} changes the advertised public range")
            if not isinstance(narrowing_reason, str) or not narrowing_reason.strip():
                raise ContractError(f"{name} needs a narrowing reason")
            narrowed.append(name)
    return sorted(narrowed)


def check_installed(
    project: dict,
    *,
    version_for=importlib.metadata.version,
    python_version: str | None = None,
) -> dict[str, str]:
    """Check actual public floors/ceilings, including selected non-release versions.

    Invoke in the resolved environment before tests/builds. This is not a
    transitive pip-check, import-origin check, solver or installed-file verifier.
    """
    python_version = python_version or ".".join(map(str, sys.version_info[:3]))
    if not SpecifierSet(project["requires-python"]).contains(
        Version(python_version), prereleases=True
    ):
        raise ContractError(f"Python {python_version} violates requires-python")
    versions = {"python": python_version}
    for value in project.get("dependencies", []):
        requirement = Requirement(value)
        if requirement.marker or requirement.url or requirement.extras:
            raise ContractError("conditional/source/extra metadata needs review")
        version = version_for(requirement.name)
        if not requirement.specifier.contains(Version(version), prereleases=True):
            raise ContractError(
                f"installed {requirement.name} {version} violates {requirement}"
            )
        versions[canonicalize_name(requirement.name)] = version
    return versions


def narrow_python(required: str, minor: str) -> list[str]:
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
