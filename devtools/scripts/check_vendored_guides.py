"""Validate registered integration-guide copies against their canonical sources."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from devtools.scripts.check_repository import Finding, _load_policy
except ImportError:
    from check_repository import Finding, _load_policy

MARKER = "SYNCHRONIZED MOLSYSSUITE GUIDE — DO NOT EDIT COMPONENT COPIES."


def _name(repository: str) -> str:
    return repository.rsplit("/", 1)[-1]


def _source_url(owner: str, source_path: str) -> str:
    return f"Canonical source: https://github.com/{owner}/blob/main/{source_path}"


def check_one(
    workspace: Path,
    *,
    owner: str,
    source_path: str,
    consumer: str,
    filename: str,
) -> list[Finding]:
    """Check one declared source-to-consumer relationship."""
    source = workspace / _name(owner) / source_path
    target = workspace / _name(consumer) / filename
    if not source.is_file():
        return [Finding("GUIDE_SOURCE", f"canonical guide is missing: {source}")]
    if not target.is_file():
        return [Finding("GUIDE_MISSING", f"vendored guide is missing: {target}")]

    expected = source.read_bytes()
    source_text = source.read_text(encoding="utf-8", errors="replace")
    required_header = (MARKER, _source_url(owner, source_path))
    if not all(line in source_text for line in required_header):
        return [Finding("GUIDE_MARKER", f"canonical guide lacks its marker: {source}")]
    if target.read_bytes() != expected:
        return [Finding("GUIDE_DRIFT", f"{target} differs from {source}")]
    return []


def check(workspace: Path) -> list[Finding]:
    """Check the full guide inventory declared in ``suite.toml``."""
    findings: list[Finding] = []
    for guide in _load_policy().get("guides", []):
        for consumer in guide["consumers"]:
            findings.extend(
                check_one(
                    workspace,
                    owner=str(guide["owner"]),
                    source_path=str(guide["source"]),
                    consumer=str(consumer),
                    filename=str(guide["filename"]),
                )
            )
    return findings


def repositories() -> list[str]:
    """Return the registered repository identifiers needed by the full audit."""
    policy = _load_policy()
    repositories = {str(member["repository"]) for member in policy["members"]}
    repositories.add(str(policy["governance"]["repository"]))
    return sorted(repositories)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", nargs="?", type=Path)
    parser.add_argument("--list-repositories", action="store_true")
    arguments = parser.parse_args()
    if arguments.list_repositories:
        for repository in repositories():
            print(repository)
        return 0
    if arguments.workspace is None:
        parser.error("workspace is required unless --list-repositories is used")

    findings = check(arguments.workspace.resolve())
    for finding in findings:
        print(f"[{finding.code}] {finding.message}", file=sys.stderr)
    if not findings:
        print("All registered vendored guides match their canonical sources.")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
