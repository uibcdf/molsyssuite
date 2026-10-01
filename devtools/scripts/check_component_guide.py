"""Check synchronized guidance and explicit contributor routing for one member."""

from __future__ import annotations

import argparse
import json
import re
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
    findings = _component_guide_findings(root, policy)
    modular = policy["policies"].get("modular-reusable-tools", {})
    if modular.get("status") == "accepted":
        agents = root / "AGENTS.md"
        text = agents.read_text(encoding="utf-8") if agents.is_file() else ""
        # An inactive example or comment does not deliver contributor instructions.
        text = re.sub(r"(?s)<!--.*?-->", "", text)
        text = re.sub(r"(?ms)^(`{3,}|~{3,})[^\n]*\n.*?^\1[ \t]*$", "", text)
        section = re.search(
            r"(?ms)^## Modular reusable tools[ \t]*\n(.*?)(?=^#{1,2}[ \t]|\Z)",
            text,
        )
        route = modular["agents-route"]
        if section is None or route not in section.group(1):
            findings.append(
                Finding(
                    "MODULAR_TOOLS_ROUTE",
                    "AGENTS.md must explicitly route its Modular reusable tools "
                    f"instruction through {route}",
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
        print(
            f"{arguments.repository} carries current guidance and contributor routes."
        )
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
