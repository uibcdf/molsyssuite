"""Read-only conformance audit for a registered MolSysSuite repository."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

import tomllib

POLICY_ROOT = Path(__file__).resolve().parents[2]
POLICY_FILE = POLICY_ROOT / "suite.toml"


@dataclass(frozen=True)
class Finding:
    code: str
    message: str


def _load_policy() -> dict[str, object]:
    return tomllib.loads(POLICY_FILE.read_text(encoding="utf-8"))


def _member(policy: dict[str, object], repository: str) -> dict[str, object] | None:
    wanted = repository.casefold()
    return next(
        (
            member
            for member in policy.get("members", [])
            if str(member.get("repository", "")).casefold() == wanted
        ),
        None,
    )


def _governance_pointer(root: Path) -> bool:
    candidates = (root / "AGENTS.md", root / "CONTRIBUTING.md")
    text = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in candidates
        if path.is_file()
    ).casefold()
    return "uibcdf/molsyssuite" in text


def _workflow_text(root: Path) -> str:
    directory = root / ".github" / "workflows"
    if not directory.is_dir():
        return ""
    return "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for suffix in ("*.yml", "*.yaml")
        for path in sorted(directory.glob(suffix))
    )


def _version_is_present(text: str, version: str) -> bool:
    return re.search(rf"(?<![\d.]){re.escape(version)}(?![\d.])", text) is not None


def _canonical_specifiers(value: object) -> frozenset[str]:
    """Normalize the simple minor-version bounds used by the suite policy."""
    normalized: set[str] = set()
    for raw in str(value or "").split(","):
        match = re.fullmatch(r"\s*(<=|>=|==|!=|~=|<|>)\s*(\d+(?:\.\d+)*)\s*", raw)
        if match is None:
            return frozenset()
        operator, version = match.groups()
        parts = version.split(".")
        while len(parts) > 2 and parts[-1] == "0":
            parts.pop()
        normalized.add(operator + ".".join(parts))
    return frozenset(normalized)


def _rule_is_covered(rule: str, selected: list[str]) -> bool:
    return "ALL" in selected or any(rule.startswith(choice) for choice in selected)


def _ruff_conforms(pyproject: dict[str, object], required: list[str]) -> bool:
    ruff = pyproject.get("tool", {}).get("ruff", {})
    if ruff.get("target-version") != "py311":
        return False
    lint = ruff.get("lint", {})
    selected = list(lint.get("select", [])) + list(lint.get("extend-select", []))
    return all(_rule_is_covered(rule, selected) for rule in required)


def _missing_ruff_ci_commands(workflow_text: str) -> list[str]:
    command = r"(?:python\s+-m\s+)?ruff"
    check_present = re.search(
        rf"(?m)^\s*(?:-?\s*run:\s*)?{command}\s+check(?:\s|$)", workflow_text
    )
    format_lines = [
        line
        for line in workflow_text.splitlines()
        if re.search(rf"^\s*(?:-?\s*run:\s*)?{command}\s+format(?:\s|$)", line)
    ]
    format_check_present = any("--check" in line for line in format_lines)
    missing = []
    if check_present is None:
        missing.append("ruff check")
    if not format_check_present:
        missing.append("ruff format --check")
    return missing


def _legacy_tools(root: Path, workflow_text: str) -> list[str]:
    active_text = workflow_text
    for name in ("pyproject.toml", "setup.cfg", "tox.ini"):
        path = root / name
        if path.is_file():
            active_text += "\n" + path.read_text(encoding="utf-8", errors="replace")
    return [
        tool
        for tool in ("black", "isort", "flake8")
        if re.search(rf"(?<![\w-]){tool}(?![\w-])", active_text, re.IGNORECASE)
    ]


def check(root: Path, repository: str) -> list[Finding]:
    """Return every independent policy finding without modifying *root*."""
    policy = _load_policy()
    member = _member(policy, repository)
    if member is None:
        return [
            Finding("UNREGISTERED", f"{repository} is not registered in suite.toml")
        ]

    findings: list[Finding] = []
    if not _governance_pointer(root):
        findings.append(
            Finding(
                "GOVERNANCE_POINTER",
                "AGENTS.md or CONTRIBUTING.md must route suite-wide work to uibcdf/molsyssuite",
            )
        )

    if "python-library" not in member.get("profiles", []):
        return findings

    python_policy = policy["policies"]["python"]
    quality_policy = policy["policies"]["python-quality"]
    pyproject_path = root / "pyproject.toml"
    if not pyproject_path.is_file():
        findings.append(Finding("PYPROJECT", "a Python member requires pyproject.toml"))
        return findings
    try:
        pyproject = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as error:
        findings.append(Finding("PYPROJECT", f"pyproject.toml is invalid: {error}"))
        return findings

    required_range = python_policy["requires-python"]
    actual_range = pyproject.get("project", {}).get("requires-python")
    if _canonical_specifiers(actual_range) != _canonical_specifiers(required_range):
        findings.append(
            Finding(
                "PYTHON_RANGE",
                f"project.requires-python must be {required_range!r}; found {actual_range!r}",
            )
        )

    workflow_text = _workflow_text(root)
    missing_versions = [
        version
        for version in python_policy["ci-versions"]
        if not _version_is_present(workflow_text, version)
    ]
    if missing_versions:
        findings.append(
            Finding(
                "PYTHON_CI",
                f"workflow version literals missing: {', '.join(missing_versions)}",
            )
        )

    required_rules = quality_policy["required-lint-rules"]
    if not _ruff_conforms(pyproject, required_rules):
        findings.append(
            Finding(
                "RUFF_CONFIG",
                "Ruff must target py311 and select the common lint baseline",
            )
        )

    missing_ruff_ci = _missing_ruff_ci_commands(workflow_text)
    if missing_ruff_ci:
        findings.append(
            Finding(
                "RUFF_CI",
                "active workflow commands missing: " + ", ".join(missing_ruff_ci),
            )
        )

    legacy = _legacy_tools(root, workflow_text)
    if legacy:
        findings.append(
            Finding(
                "LEGACY_TOOL", f"active replaced tooling remains: {', '.join(legacy)}"
            )
        )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()

    findings = check(arguments.target.resolve(), arguments.repository)
    if arguments.json:
        print(json.dumps([asdict(finding) for finding in findings], indent=2))
    elif findings:
        for finding in findings:
            print(f"[{finding.code}] {finding.message}")
    else:
        print(f"{arguments.repository} conforms to MolSysSuite policy 1.0.")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
