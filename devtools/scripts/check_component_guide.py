"""Check only the synchronized MolSysSuite guide contract for one member."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

try:
    from devtools.scripts.check_repository import (
        Finding,
        _component_guide_findings,
        _load_policy,
        _member,
    )
except ImportError:
    from check_repository import (
        Finding,
        _component_guide_findings,
        _load_policy,
        _member,
    )


def check(root: Path, repository: str) -> list[Finding]:
    policy = _load_policy()
    if _member(policy, repository) is None:
        return [
            Finding("UNREGISTERED", f"{repository} is not registered in suite.toml")
        ]
    return _component_guide_findings(root, policy)


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
        print(f"{arguments.repository} carries the current MolSysSuite guide.")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
