"""Check durable working-instruction routes without judging instruction prose."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from datetime import UTC, date, datetime
from pathlib import Path

import tomllib

ROOT = Path(__file__).resolve().parents[2]
ROUTE = "MOLSYSSUITE_GUIDE.md#durable-working-instructions"


@dataclass(frozen=True)
class Finding:
    code: str
    message: str


def active_markdown(text: str) -> str:
    """Remove comments and fenced examples before checking actionable routes."""
    text = re.sub(r"(?s)<!--.*?(?:-->|\Z)", "", text)
    lines: list[str] = []
    fence: str | None = None
    length = 0
    for line in text.splitlines():
        match = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence is None:
            if match:
                fence, length = match[1][0], len(match[1])
            elif not line.startswith(("    ", "\t", ">")):
                lines.append(line)
        elif (
            match
            and match[1][0] == fence
            and len(match[1]) >= length
            and not match[2].strip()
        ):
            fence = None
    return "\n".join(lines)


def validate_exceptions(policy: dict, today: date | None = None) -> list[str]:
    today = today or datetime.now(tz=UTC).date()
    registered = {m["repository"] for m in policy.get("members", [])}
    seen: set[str] = set()
    errors: list[str] = []
    for entry in policy.get("working-instruction-exceptions", []):
        repository = entry.get("repository", "")
        prefix = f"working instruction exception {repository!r}"
        if repository not in registered or repository in seen:
            errors.append(f"{prefix}: unknown or duplicate repository")
        seen.add(repository)
        issue = str(entry.get("issue", ""))
        if not any(
            re.fullmatch(re.escape(owner) + r"#[1-9][0-9]*", issue)
            for owner in (repository, "uibcdf/molsyssuite")
        ):
            errors.append(f"{prefix}: issue must belong to the member or suite")
        for key in ("owner", "reason", "removal-condition"):
            if not str(entry.get(key, "")).strip():
                errors.append(f"{prefix}: {key} is required")
        try:
            expires = date.fromisoformat(str(entry.get("expires-on", "")))
        except ValueError:
            errors.append(f"{prefix}: expires-on must be an ISO date")
        else:
            if expires < today:
                errors.append(f"{prefix}: expired on {expires}")
    return errors


def check(root: Path, policy: dict, repository: str) -> list[Finding]:
    registered = {m["repository"] for m in policy.get("members", [])}
    if repository not in registered | {"uibcdf/molsyssuite"}:
        return [Finding("UNREGISTERED", f"{repository} is not a suite repository")]
    errors = validate_exceptions(policy)
    if errors:
        return [Finding("INSTRUCTION_EXCEPTION", error) for error in errors]
    if any(
        e.get("repository") == repository
        for e in policy.get("working-instruction-exceptions", [])
    ):
        return []
    findings: list[Finding] = []
    root_agents = root / "AGENTS.md"
    nested_agents = root / "devguide/AGENTS.md"
    for path in (root_agents, nested_agents):
        if not path.is_file():
            findings.append(
                Finding("INSTRUCTION_FILE", f"{path.relative_to(root)} is missing")
            )
    root_text = (
        active_markdown(root_agents.read_text()) if root_agents.is_file() else ""
    )
    section = re.search(
        r"(?ms)^## Durable working instructions[ \t]*\n(.*?)(?=^#{1,2}[ \t]|\Z)",
        root_text,
    )
    if (
        section is None
        or ROUTE not in section[1]
        or "devguide/AGENTS.md" not in section[1]
    ):
        findings.append(
            Finding(
                "INSTRUCTION_ROOT_ROUTE",
                "AGENTS.md requires an active Durable working instructions section routing to the canonical guide and devguide/AGENTS.md",
            )
        )
    nested_text = (
        active_markdown(nested_agents.read_text()) if nested_agents.is_file() else ""
    )
    for route in ("../AGENTS.md", "reporting_protocol.md", "../" + ROUTE):
        if route not in nested_text:
            findings.append(
                Finding(
                    "INSTRUCTION_NESTED_ROUTE",
                    f"devguide/AGENTS.md must actively route to {route}",
                )
            )
        target = nested_agents.parent / route.split("#", 1)[0]
        if not target.is_file():
            findings.append(
                Finding(
                    "INSTRUCTION_TARGET", f"devguide route target is missing: {route}"
                )
            )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    policy = tomllib.loads((ROOT / "suite.toml").read_text())
    findings = check(args.target.resolve(), policy, args.repository)
    if args.json:
        print(json.dumps([asdict(f) for f in findings], indent=2))
    else:
        for finding in findings:
            print(f"[{finding.code}] {finding.message}")
        if not findings:
            print(f"{args.repository}: working-instruction routes conform.")
    return bool(findings)


if __name__ == "__main__":
    raise SystemExit(main())
