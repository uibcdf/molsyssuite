"""Check synchronized guidance and explicit contributor routing for one member."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path

try:
    from devtools.scripts import agent_instructions
    from devtools.scripts.check_repository import (
        Finding,
        _component_guide_findings,
        _load_policy,
        _member,
    )
except ImportError:
    import agent_instructions
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
    if policy["policies"].get("working-instructions", {}).get("status") == "accepted":
        findings.extend(
            Finding(f.code, f.message)
            for f in agent_instructions.check(root, policy, repository)
        )
    modular = policy["policies"].get("modular-reusable-tools", {})
    if modular.get("status") == "accepted":
        agents = root / "AGENTS.md"
        text = agents.read_text(encoding="utf-8") if agents.is_file() else ""
        section = agent_instructions.mandatory_section(text)
        route = modular["agents-route"]
        if route not in section:
            findings.append(
                Finding(
                    "MODULAR_TOOLS_ROUTE",
                    f"AGENTS.md must delegate reusable-tool ownership through {route} in its mandatory suite section",
                )
            )
    return findings


def receipt(root: Path, repository: str, findings: list[Finding]) -> dict:
    """Bind a bounded public audit to committed guide/instruction inputs.

    No instruction contents, private paths, logs or finding messages are retained.
    """
    paths = ("MOLSYSSUITE_GUIDE.md", "AGENTS.md", "devguide/AGENTS.md")
    completed = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
        timeout=30,
    )
    source = completed.stdout.strip()
    if re.fullmatch(r"[0-9a-f]{40}", source) is None:
        raise ValueError("guide audit needs an immutable source commit")
    dirty = subprocess.run(
        ["git", "-C", str(root), "status", "--porcelain", "--", *paths],
        capture_output=True,
        text=True,
        check=True,
        timeout=30,
    ).stdout
    codes = sorted({finding.code for finding in findings})
    if dirty:
        codes.append("UNCOMMITTED_INPUT")
    return {
        "schema": "molsyssuite.component-guide-audit@1",
        "repository": repository,
        "source_commit": source,
        "state": "verified" if not codes else "failure",
        "finding_codes": codes,
        "inputs": {
            path: hashlib.sha256((root / path).read_bytes()).hexdigest()
            for path in paths
            if (root / path).is_file()
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--json", action="store_true")
    parser.add_argument(
        "--receipt", type=Path, help="write a bounded committed-input audit receipt"
    )
    arguments = parser.parse_args()
    findings = check(arguments.target.resolve(), arguments.repository)
    if arguments.receipt is not None:
        result = receipt(arguments.target.resolve(), arguments.repository, findings)
        arguments.receipt.parent.mkdir(parents=True, exist_ok=True)
        arguments.receipt.write_text(json.dumps(result, indent=2) + "\n")
        if result["state"] != "verified" and not findings:
            findings.append(
                Finding("UNCOMMITTED_INPUT", "guide audit inputs must be committed")
            )
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
