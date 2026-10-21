"""Validate public test-tool dependencies before noarch build and installation."""

import re

from packaging.requirements import InvalidRequirement, Requirement
from packaging.utils import canonicalize_name

try:
    from devtools.scripts.conda_release_contract import ContractError
except ModuleNotFoundError:
    from conda_release_contract import ContractError


TEST_TOOLS = ["pytest>=8,<10", "pytest-cov>=6,<8", "pytest-xdist>=3.6,<4"]


def test_dependencies(plan: dict, inventory: dict) -> list[str]:
    """Resolve bounded public Conda test tools from the committed candidate inventory."""
    extra = inventory.get("installed_tests", {}).get("conda_dependencies", [])
    if not isinstance(extra, list) or len(extra) > 64:
        raise ContractError(
            "installed test dependencies need a list of at most 64 specs"
        )
    dependencies = list(TEST_TOOLS)
    candidate = canonicalize_name(plan["package"])
    if candidate != "pytest-receptor":
        dependencies.append("pytest-receptor==1.2.0")
    for spec in extra:
        if (
            not isinstance(spec, str)
            or len(spec) > 256
            or any(c in spec for c in "\r\n\t")
        ):
            raise ContractError(
                "installed test dependency must be one bounded package spec"
            )
        try:
            requirement = Requirement(spec)
        except InvalidRequirement as error:
            raise ContractError(
                "installed test dependencies need public package names and version bounds"
            ) from error
        if requirement.url or requirement.marker or requirement.extras:
            raise ContractError(
                "installed test dependencies cannot use URLs, markers or extras"
            )
        if canonicalize_name(requirement.name) in {"python", candidate}:
            raise ContractError(
                "test tools cannot replace the candidate or matrix interpreter"
            )
        operators = {item.operator for item in requirement.specifier}
        if not operators <= {"==", "!=", ">=", ">", "<=", "<"} or not (
            "==" in operators or (operators & {">=", ">"} and operators & {"<=", "<"})
        ):
            raise ContractError(
                "test dependencies need an exact version or explicit lower and upper bounds"
            )
        dependencies.append(re.sub(r"\s+", "", spec))
    return dependencies
