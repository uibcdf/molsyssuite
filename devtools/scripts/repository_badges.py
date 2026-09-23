"""Generate and validate the central MolSysSuite README badge baseline."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.parse import quote

import tomllib

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "suite.toml"

ROLE_LABELS = {
    "scientific-component": "scientific component",
    "support-library": "support library",
    "developer-tool": "developer tool",
    "specialist-subsystem": "specialist subsystem",
}
ROLE_COLORS = {
    "scientific-component": "0b7285",
    "support-library": "2563eb",
    "developer-tool": "6f42c1",
    "specialist-subsystem": "8b5cf6",
}
SHIELDS_LABEL_COLOR = "24292f"

_FINDING_BY_BADGE = {
    "identity": "IDENTITY_BADGE",
    "policy": "POLICY_BADGE",
    "python": "PYTHON_BADGE",
    "license": "LICENSE_BADGE",
}


@dataclass(frozen=True)
class Badge:
    """One canonical Markdown badge and its semantic position."""

    key: str
    markdown: str


@dataclass(frozen=True)
class Finding:
    """One independently actionable README badge-policy finding."""

    code: str
    message: str


def load_registry() -> dict[str, object]:
    """Load the central registry without consulting component repositories."""

    return tomllib.loads(REGISTRY.read_text(encoding="utf-8"))


def _member(data: dict[str, object], repository: str) -> dict[str, object]:
    wanted = repository.casefold()
    for member in data.get("members", []):
        if str(member.get("repository", "")).casefold() == wanted:
            return member
    raise ValueError(f"{repository} is not registered in suite.toml")


def _role_badge_url(role: str) -> str:
    label = quote(ROLE_LABELS[role], safe="")
    return (
        f"https://img.shields.io/badge/MolSysSuite-{label}-{ROLE_COLORS[role]}"
        f"?labelColor={SHIELDS_LABEL_COLOR}"
    )


def _python_versions(data: dict[str, object], member: dict[str, object]) -> list[str]:
    """Return the public Python claim authorized for one member."""

    policy = data.get("policies", {}).get("python", {})
    versions = [str(version) for version in policy.get("ci-versions", [])]
    transition = policy.get("transition", {})
    for component in transition.get("components", []):
        if (
            component.get("name") == member.get("name")
            and component.get("state") == "admitted"
        ):
            return [
                str(version)
                for version in transition.get("target-ci-versions", versions)
            ]
    return versions


def canonical_badges(data: dict[str, object], repository: str) -> list[Badge]:
    """Return the ordered baseline for a registered repository."""

    member = _member(data, repository)
    role = str(member.get("role", ""))
    if role not in ROLE_LABELS:
        raise ValueError(f"{repository} has unknown role {role!r}")
    label = ROLE_LABELS[role]
    suite_base = "https://github.com/uibcdf/molsyssuite"
    repo_base = f"https://github.com/{repository}"
    badges = [
        Badge(
            "identity",
            f"[![MolSysSuite: {label.title()}]"
            f"({_role_badge_url(role)})]"
            f"({suite_base}/blob/main/devguide/repository_badges.md#{role})",
        ),
        Badge(
            "policy",
            f"[![MolSysSuite policy]({repo_base}/actions/workflows/"
            f"molsyssuite-policy.yml/badge.svg?branch=main)]"
            f"({repo_base}/actions/workflows/molsyssuite-policy.yml)",
        ),
    ]
    if "python-package" in member.get("capabilities", []):
        python_versions = _python_versions(data, member)
        python_label = " | ".join(python_versions)
        badges.append(
            Badge(
                "python",
                f"[![Python {python_label}]"
                f"(https://img.shields.io/badge/Python-{quote(python_label, safe='')}-"
                "3776AB?logo=python&logoColor=white)]"
                f"({suite_base}/blob/main/devguide/python_policy.md)",
            )
        )
    badges.append(
        Badge(
            "license",
            f"[![License](https://img.shields.io/github/license/{repository})]"
            f"({repo_base}/blob/main/LICENSE)",
        )
    )
    return badges


def render_snippet(data: dict[str, object], repository: str) -> str:
    """Render the canonical baseline as one compact README row."""

    return (
        "\n".join(badge.markdown for badge in canonical_badges(data, repository)) + "\n"
    )


def _foreign_workflow_repositories(text: str, repository: str) -> set[str]:
    found = {
        match.group(1)
        for match in re.finditer(
            r"https://github\.com/([^/\s)]+/[^/\s)]+)/actions/workflows/", text
        )
    }
    return {
        candidate
        for candidate in found
        if candidate.casefold() != repository.casefold()
    }


def validate_readme(
    root: Path,
    repository: str,
    data: dict[str, object] | None = None,
) -> list[Finding]:
    """Validate only facts that can be established from a local checkout."""

    registry = data if data is not None else load_registry()
    expected = canonical_badges(registry, repository)
    readme = root / "README.md"
    if not readme.is_file():
        return [Finding("README_MISSING", "README.md is missing")]
    text = readme.read_text(encoding="utf-8", errors="replace")
    findings: list[Finding] = []
    positions: list[int] = []
    for badge in expected:
        position = text.find(badge.markdown)
        if position < 0:
            findings.append(
                Finding(
                    _FINDING_BY_BADGE[badge.key],
                    f"README.md lacks the canonical {badge.key} badge",
                )
            )
        else:
            positions.append(position)
    if len(positions) == len(expected) and positions != sorted(positions):
        findings.append(
            Finding("BADGE_ORDER", "canonical baseline badges are not in policy order")
        )

    member = _member(registry, repository)
    expected_role = str(member["role"])
    wrong_roles = [
        role
        for role in ROLE_LABELS
        if role != expected_role and _role_badge_url(role) in text
    ]
    if wrong_roles:
        findings.append(
            Finding(
                "WRONG_IDENTITY_BADGE",
                "README.md carries a badge for another MolSysSuite role: "
                + ", ".join(sorted(wrong_roles)),
            )
        )

    foreign = _foreign_workflow_repositories(text, repository)
    if foreign:
        findings.append(
            Finding(
                "FOREIGN_WORKFLOW_BADGE",
                "workflow badges target another repository: "
                + ", ".join(sorted(foreign)),
            )
        )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    snippet = subparsers.add_parser("snippet", help="render one canonical badge row")
    snippet.add_argument("--repository", required=True)

    check = subparsers.add_parser("check", help="validate a local README")
    check.add_argument("target", type=Path)
    check.add_argument("--repository", required=True)
    check.add_argument("--json", action="store_true")

    arguments = parser.parse_args()
    data = load_registry()
    if arguments.command == "snippet":
        print(render_snippet(data, arguments.repository), end="")
        return 0

    findings = validate_readme(arguments.target.resolve(), arguments.repository, data)
    if arguments.json:
        print(json.dumps([asdict(finding) for finding in findings], indent=2))
    elif findings:
        for finding in findings:
            print(f"[{finding.code}] {finding.message}")
    else:
        print(f"{arguments.repository} README badges conform to the central baseline.")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
