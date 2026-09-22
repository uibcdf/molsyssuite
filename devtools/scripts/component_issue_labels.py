"""Audit and synchronize cross-component GitHub issue labels."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

import tomllib

ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class LabelSpec:
    """Canonical attributes for one registered component label."""

    name: str
    color: str
    description: str


@dataclass(frozen=True)
class LabelFinding:
    """One label-contract deviation."""

    code: str
    repository: str
    label: str
    detail: str
    next_action: str


@dataclass(frozen=True)
class LabelAction:
    """One safe create or update operation."""

    operation: str
    repository: str
    spec: LabelSpec


def _load_policy() -> dict[str, object]:
    return tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))


def catalog(policy: dict[str, object]) -> dict[str, LabelSpec]:
    """Return canonical labels derived only from registered suite members."""
    label_policy = policy["policies"]["cross-component-issue-labels"]
    prefix = str(label_policy["prefix"])
    color = str(label_policy["color"]).removeprefix("#").casefold()
    template = str(label_policy["description-template"])
    return {
        str(member["name"]): LabelSpec(
            name=f"{prefix}{member['name']}",
            color=color,
            description=template.format(repository=member["repository"]),
        )
        for member in policy["members"]
    }


def _repositories(policy: dict[str, object]) -> dict[str, str]:
    repositories = {
        str(member["name"]): str(member["repository"]) for member in policy["members"]
    }
    governance_repository = str(policy["governance"]["repository"])
    repositories[governance_repository.rsplit("/", 1)[-1]] = governance_repository
    return repositories


def _resolve_repositories(requested: list[str], policy: dict[str, object]) -> list[str]:
    registered = _repositories(policy)
    by_identity = {
        identity.casefold(): repository
        for name, repository in registered.items()
        for identity in (name, repository)
    }
    if not requested:
        return sorted(set(registered.values()))
    resolved: list[str] = []
    for value in requested:
        try:
            repository = by_identity[value.casefold()]
        except KeyError as error:
            raise ValueError(f"unknown repository {value!r}") from error
        if repository not in resolved:
            resolved.append(repository)
    return resolved


def analyze(
    repository: str,
    labels: list[dict[str, object]],
    policy: dict[str, object],
    *,
    required_components: list[str] | None = None,
) -> tuple[list[LabelFinding], list[LabelAction]]:
    """Return findings and safe repairs for one repository label inventory."""
    label_policy = policy["policies"]["cross-component-issue-labels"]
    prefix = str(label_policy["prefix"])
    specs = catalog(policy)
    members_by_repository = {
        str(member["repository"]): str(member["name"]) for member in policy["members"]
    }
    if repository not in set(_repositories(policy).values()):
        raise ValueError(f"unknown repository {repository!r}")

    required = list(dict.fromkeys(required_components or []))
    for component in required:
        if component not in specs:
            raise ValueError(f"unknown component {component!r}")
        if members_by_repository.get(repository) == component:
            raise ValueError(
                f"component label {component!r} cannot point to its owning repository"
            )

    findings: list[LabelFinding] = []
    actions: list[LabelAction] = []
    existing: dict[str, dict[str, object]] = {}
    for label in labels:
        name = str(label.get("name", ""))
        if not name.startswith(prefix):
            continue
        existing[name] = label
        component = name.removeprefix(prefix)
        if component not in specs:
            findings.append(
                LabelFinding(
                    code="UNKNOWN",
                    repository=repository,
                    label=name,
                    detail="suffix is not a registered MolSysSuite member",
                    next_action="rename or remove the label after reviewing its issues",
                )
            )
            continue
        if members_by_repository.get(repository) == component:
            findings.append(
                LabelFinding(
                    code="SELF",
                    repository=repository,
                    label=name,
                    detail="a component repository cannot label itself as a relation",
                    next_action="remove the self-relationship label after reviewing its issues",
                )
            )
            continue
        spec = specs[component]
        observed_color = str(label.get("color", "")).removeprefix("#").casefold()
        observed_description = str(label.get("description") or "")
        if observed_color != spec.color or observed_description != spec.description:
            findings.append(
                LabelFinding(
                    code="STALE",
                    repository=repository,
                    label=name,
                    detail=(
                        f"expected color={spec.color!r} description={spec.description!r}"
                    ),
                    next_action="run this command with --write to update the label",
                )
            )
            actions.append(LabelAction("update", repository, spec))

    for component in required:
        spec = specs[component]
        if spec.name in existing:
            continue
        findings.append(
            LabelFinding(
                code="MISSING",
                repository=repository,
                label=spec.name,
                detail="requested relationship label does not exist",
                next_action="run this command with --write to create the label",
            )
        )
        actions.append(LabelAction("create", repository, spec))

    findings.sort(key=lambda finding: (finding.code, finding.label))
    actions.sort(key=lambda action: (action.operation, action.spec.name))
    return findings, actions


def _run_gh(arguments: list[str]) -> str:
    try:
        completed = subprocess.run(
            ["gh", *arguments],
            capture_output=True,
            check=False,
            text=True,
            timeout=60,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise RuntimeError(f"could not run gh: {error}") from error
    if completed.returncode:
        message = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(f"gh {' '.join(arguments[:2])} failed: {message}")
    return completed.stdout


def _list_labels(repository: str) -> list[dict[str, object]]:
    output = _run_gh(
        [
            "label",
            "list",
            "--repo",
            repository,
            "--limit",
            "1000",
            "--json",
            "name,color,description",
        ]
    )
    return json.loads(output)


def _apply(action: LabelAction) -> None:
    arguments = [
        "label",
        action.operation,
        action.spec.name,
        "--repo",
        action.repository,
        "--color",
        action.spec.color,
        "--description",
        action.spec.description,
    ]
    _run_gh(arguments)


def _render_text(findings: list[LabelFinding], repositories: list[str]) -> str:
    if not findings:
        return "\n".join(
            f"CURRENT labels {repository}" for repository in sorted(repositories)
        )
    return "\n".join(
        f"{finding.code} labels {finding.repository} {finding.label} "
        f"detail={finding.detail} next={finding.next_action}"
        for finding in findings
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repository",
        action="append",
        default=[],
        help="registered repository name or OWNER/REPO; repeatable",
    )
    parser.add_argument(
        "--component",
        action="append",
        default=[],
        help="related registered component whose label must exist; repeatable",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="create requested missing labels and update known stale labels",
    )
    parser.add_argument("--format", choices=("text", "json"), default="text")
    arguments = parser.parse_args()
    policy = _load_policy()
    try:
        repositories = _resolve_repositories(arguments.repository, policy)
        if arguments.component and len(repositories) != 1:
            raise ValueError("--component requires exactly one --repository")
        findings: list[LabelFinding] = []
        for repository in repositories:
            labels = _list_labels(repository)
            repository_findings, actions = analyze(
                repository,
                labels,
                policy,
                required_components=arguments.component,
            )
            if arguments.write:
                for action in actions:
                    _apply(action)
                labels = _list_labels(repository)
                repository_findings, _ = analyze(
                    repository,
                    labels,
                    policy,
                    required_components=arguments.component,
                )
            findings.extend(repository_findings)
    except (RuntimeError, ValueError, json.JSONDecodeError) as error:
        print(f"component issue label audit failed: {error}", file=sys.stderr)
        return 2

    if arguments.format == "json":
        print(json.dumps([asdict(finding) for finding in findings], indent=2))
    else:
        print(_render_text(findings, repositories))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
