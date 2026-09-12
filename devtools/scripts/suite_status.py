"""Report local and upstream state across registered MolSysSuite components."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

try:
    from devtools.scripts.check_repository import _load_policy
except ImportError:
    from check_repository import _load_policy

ROOT = Path(__file__).resolve().parents[2]
COHORTS = ("wave-1", "infrastructure", "auxiliary", "incubating")


@dataclass(frozen=True)
class Target:
    """One registered repository and its stabilization cohort."""

    repository: str
    cohort: str

    @property
    def name(self) -> str:
        return self.repository.rsplit("/", 1)[-1]


@dataclass(frozen=True)
class RepositoryStatus:
    """Measured local and upstream state for one component."""

    repository: str
    cohort: str
    root: str
    branch: str = ""
    head: str = ""
    upstream: str = ""
    ahead: int = 0
    behind: int = 0
    worktree: tuple[str, ...] = ()
    error: str = ""

    @property
    def healthy(self) -> bool:
        return (
            not self.error and not self.worktree and not self.ahead and not self.behind
        )

    @property
    def state(self) -> str:
        if self.error:
            return "error"
        return "current" if self.healthy else "attention"


def registered_targets() -> list[Target]:
    """Return members in the suite's declared stabilization order."""
    policy = _load_policy()
    members = {
        str(member["name"]): str(member["repository"]) for member in policy["members"]
    }
    targets: list[Target] = []
    for cohort in COHORTS:
        for name in policy["stabilization"].get(cohort, []):
            targets.append(Target(repository=members[str(name)], cohort=cohort))
    return targets


def _git_output(root: Path, *arguments: str) -> str:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=root,
        capture_output=True,
        check=False,
        text=True,
        timeout=60,
    )
    if completed.returncode != 0:
        command = " ".join(("git", *arguments[:2]))
        detail = completed.stderr.strip().splitlines()
        suffix = f": {detail[-1]}" if detail else ""
        raise RuntimeError(f"{root}: {command} failed{suffix}")
    return completed.stdout.strip()


def inspect_repository(
    root: Path,
    *,
    repository: str,
    cohort: str,
    fetch: bool,
) -> RepositoryStatus:
    """Inspect one checkout without modifying its worktree."""
    root = root.resolve()
    if not root.is_dir():
        return RepositoryStatus(
            repository=repository,
            cohort=cohort,
            root=str(root),
            error="repository checkout is missing",
        )
    try:
        if fetch:
            _git_output(root, "fetch", "--prune", "--quiet")
        worktree_text = _git_output(root, "status", "--porcelain")
        upstream = _git_output(
            root,
            "rev-parse",
            "--abbrev-ref",
            "--symbolic-full-name",
            "@{upstream}",
        )
        counts = _git_output(
            root, "rev-list", "--left-right", "--count", f"HEAD...{upstream}"
        )
        ahead_text, behind_text = counts.split()
        branch = _git_output(root, "rev-parse", "--abbrev-ref", "HEAD")
        head = _git_output(root, "rev-parse", "--short=12", "HEAD")
    except (OSError, RuntimeError, subprocess.TimeoutExpired, ValueError) as error:
        return RepositoryStatus(
            repository=repository,
            cohort=cohort,
            root=str(root),
            error=str(error),
        )
    worktree = tuple(
        line.strip() for line in worktree_text.splitlines() if line.strip()
    )
    return RepositoryStatus(
        repository=repository,
        cohort=cohort,
        root=str(root),
        branch=branch,
        head=head,
        upstream=upstream,
        ahead=int(ahead_text),
        behind=int(behind_text),
        worktree=worktree,
    )


def inspect(
    workspace: Path,
    targets: list[Target],
    *,
    fetch: bool,
) -> list[RepositoryStatus]:
    """Inspect all selected targets."""
    workspace = workspace.resolve()
    return [
        inspect_repository(
            workspace / target.name,
            repository=target.repository,
            cohort=target.cohort,
            fetch=fetch,
        )
        for target in targets
    ]


def _render_text(statuses: list[RepositoryStatus]) -> str:
    lines = [
        "STATE      COHORT          REPOSITORY                       BRANCH       AHEAD BEHIND DIRTY",
    ]
    for status in statuses:
        lines.append(
            f"{status.state.upper():<10} "
            f"{status.cohort:<15} "
            f"{status.repository:<32} "
            f"{status.branch or '-':<12} "
            f"{status.ahead:>5} "
            f"{status.behind:>6} "
            f"{len(status.worktree):>5}"
        )
        if status.error:
            lines.append(f"  error: {status.error}")
        for entry in status.worktree:
            lines.append(f"  {entry}")
    current = sum(status.healthy for status in statuses)
    lines.append(f"{current}/{len(statuses)} repositories are current and clean.")
    return "\n".join(lines)


def render_json(statuses: list[RepositoryStatus]) -> str:
    """Render statuses with explicit derived state for automation."""
    payload = [
        {**asdict(status), "healthy": status.healthy, "state": status.state}
        for status in statuses
    ]
    return json.dumps(payload, indent=2)


def _select_targets(selectors: list[str] | None) -> list[Target]:
    targets = registered_targets()
    if not selectors:
        return targets
    selected: list[Target] = []
    for selector in selectors:
        matches = [
            target
            for target in targets
            if selector.casefold()
            in {target.name.casefold(), target.repository.casefold()}
        ]
        if len(matches) != 1:
            raise ValueError(f"unknown repository selector: {selector}")
        if matches[0] not in selected:
            selected.append(matches[0])
    return selected


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "workspace",
        nargs="?",
        type=Path,
        default=ROOT.parent,
        help="directory containing sibling component checkouts",
    )
    parser.add_argument(
        "--repository",
        action="append",
        dest="repositories",
        help="limit to a registered component name or repository; repeatable",
    )
    parser.add_argument(
        "--no-fetch",
        action="store_true",
        help="inspect cached upstream references without fetching first",
    )
    parser.add_argument("--format", choices=("text", "json"), default="text")
    arguments = parser.parse_args()
    try:
        targets = _select_targets(arguments.repositories)
    except ValueError as error:
        parser.error(str(error))
    statuses = inspect(arguments.workspace, targets, fetch=not arguments.no_fetch)
    if arguments.format == "json":
        print(render_json(statuses))
    else:
        print(_render_text(statuses))
    return 0 if all(status.healthy for status in statuses) else 1


if __name__ == "__main__":
    sys.exit(main())
