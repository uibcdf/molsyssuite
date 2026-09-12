"""Check or synchronize integration guides declared in ``suite.toml``."""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    from devtools.scripts.check_repository import _load_policy
    from devtools.scripts.check_vendored_guides import MARKER, _source_url
except ImportError:
    from check_repository import _load_policy
    from check_vendored_guides import MARKER, _source_url

ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Relationship:
    """One canonical-source to consumer-copy relationship."""

    owner: str
    source_path: str
    consumer: str
    filename: str


def _name(repository: str) -> str:
    return repository.rsplit("/", 1)[-1]


def _repository_id(selector: str, registered: set[str]) -> str:
    normalized = selector.casefold()
    matches = {
        repository
        for repository in registered
        if normalized in {repository.casefold(), _name(repository).casefold()}
    }
    if len(matches) != 1:
        raise ValueError(f"unknown repository selector: {selector}")
    return matches.pop()


def relationships(
    *,
    guides: list[str] | None = None,
    repositories: list[str] | None = None,
) -> list[Relationship]:
    """Return registered relationships matching optional exact selectors."""
    policy = _load_policy()
    inventory = list(policy.get("guides", []))
    known_guides = {str(guide["filename"]) for guide in inventory}
    selected_guides = set(guides or known_guides)
    unknown_guides = selected_guides - known_guides
    if unknown_guides:
        names = ", ".join(sorted(unknown_guides))
        raise ValueError(f"unknown guide selector: {names}")

    registered = {str(member["repository"]) for member in policy["members"]}
    selected_repositories = (
        {_repository_id(selector, registered) for selector in repositories}
        if repositories
        else registered
    )

    selected: list[Relationship] = []
    for guide in inventory:
        filename = str(guide["filename"])
        if filename not in selected_guides:
            continue
        for consumer in guide["consumers"]:
            consumer = str(consumer)
            if consumer not in selected_repositories:
                continue
            selected.append(
                Relationship(
                    owner=str(guide["owner"]),
                    source_path=str(guide["source"]),
                    consumer=consumer,
                    filename=filename,
                )
            )
    return selected


def _preflight(workspace: Path, relation: Relationship) -> list[str]:
    source = workspace / _name(relation.owner) / relation.source_path
    consumer = workspace / _name(relation.consumer)
    if not source.is_file():
        return [f"{source}: canonical guide is missing"]
    source_text = source.read_text(encoding="utf-8", errors="replace")
    required_header = (MARKER, _source_url(relation.owner, relation.source_path))
    if not all(line in source_text for line in required_header):
        return [f"{source}: canonical guide lacks its synchronized marker"]
    if not consumer.is_dir():
        return [f"{consumer}: registered consumer repository is missing"]
    return []


def _git_output(root: Path, *arguments: str) -> str:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=root,
        capture_output=True,
        check=False,
        text=True,
        timeout=30,
    )
    if completed.returncode != 0:
        command = " ".join(("git", *arguments[:2]))
        raise RuntimeError(f"{root}: {command} failed")
    return completed.stdout.strip()


def verify_sources(workspace: Path, selected: list[Relationship]) -> list[str]:
    """Require committed canonical sources at the current remote ``main`` revision."""
    workspace = workspace.resolve()
    sources: dict[str, set[str]] = {}
    for relation in selected:
        sources.setdefault(relation.owner, set()).add(relation.source_path)

    errors: list[str] = []
    for owner, source_paths in sorted(sources.items()):
        root = workspace / _name(owner)
        try:
            status = _git_output(
                root,
                "status",
                "--porcelain",
                "--",
                *sorted(source_paths),
            )
            if status:
                errors.append(f"{root}: uncommitted canonical guide changes")
                continue
            local_head = _git_output(root, "rev-parse", "HEAD")
            remote_line = _git_output(
                root,
                "ls-remote",
                "--exit-code",
                "origin",
                "refs/heads/main",
            )
        except (OSError, RuntimeError, subprocess.TimeoutExpired) as error:
            errors.append(str(error))
            continue
        remote_head = remote_line.split(maxsplit=1)[0] if remote_line else ""
        if local_head != remote_head:
            errors.append(
                f"{root}: local HEAD {local_head} does not match remote main "
                f"{remote_head or '<missing>'}"
            )
    return errors


def verify_destinations(workspace: Path, selected: list[Relationship]) -> list[str]:
    """Refuse to overwrite drift that is also an uncommitted consumer edit."""
    workspace = workspace.resolve()
    changed: dict[str, set[str]] = {}
    for relation in selected:
        source = workspace / _name(relation.owner) / relation.source_path
        destination = workspace / _name(relation.consumer) / relation.filename
        if destination.is_file() and destination.read_bytes() != source.read_bytes():
            changed.setdefault(relation.consumer, set()).add(relation.filename)

    errors: list[str] = []
    for consumer, filenames in sorted(changed.items()):
        root = workspace / _name(consumer)
        try:
            status = _git_output(
                root,
                "status",
                "--porcelain",
                "--",
                *sorted(filenames),
            )
        except (OSError, RuntimeError, subprocess.TimeoutExpired) as error:
            errors.append(str(error))
            continue
        if status:
            errors.append(
                f"{root}: locally modified consumer guide would be overwritten"
            )
    return errors


def process(
    workspace: Path,
    selected: list[Relationship],
    *,
    write: bool,
) -> list[str]:
    """Check or synchronize selected relationships after a complete preflight."""
    workspace = workspace.resolve()
    preflight_errors = [
        error for relation in selected for error in _preflight(workspace, relation)
    ]
    if preflight_errors:
        return preflight_errors

    errors: list[str] = []
    for relation in selected:
        source = workspace / _name(relation.owner) / relation.source_path
        destination = workspace / _name(relation.consumer) / relation.filename
        expected = source.read_bytes()
        if destination.is_file() and destination.read_bytes() == expected:
            continue
        if write:
            destination.write_bytes(expected)
            print(f"wrote {destination}")
        else:
            errors.append(f"{destination}: missing or different")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "workspace",
        nargs="?",
        type=Path,
        default=ROOT.parent,
        help="directory containing sibling repository checkouts",
    )
    parser.add_argument(
        "--guide",
        action="append",
        dest="guides",
        help="limit to an exact registered root filename; repeatable",
    )
    parser.add_argument(
        "--repository",
        action="append",
        dest="repositories",
        help="limit to a registered consumer name or repository; repeatable",
    )
    parser.add_argument("--write", action="store_true")
    arguments = parser.parse_args()
    try:
        selected = relationships(
            guides=arguments.guides,
            repositories=arguments.repositories,
        )
    except ValueError as error:
        parser.error(str(error))

    errors = [
        error
        for relation in selected
        for error in _preflight(arguments.workspace.resolve(), relation)
    ]
    if arguments.write and not errors:
        errors = verify_sources(arguments.workspace, selected)
    if arguments.write and not errors:
        errors = verify_destinations(arguments.workspace, selected)
    if not errors:
        errors = process(arguments.workspace, selected, write=arguments.write)
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        return 1
    action = "synchronized" if arguments.write else "current"
    print(f"{len(selected)} registered guide copies are {action}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
