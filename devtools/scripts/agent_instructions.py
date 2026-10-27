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
ENTRY_HEADING = "## Mandatory MolSysSuite instructions"
READ_REQUIREMENT = (
    "Read and follow `MOLSYSSUITE_GUIDE.md` before working in this repository."
)
PRECEDENCE_REQUIREMENT = (
    "Within their stated scope, its common rules take precedence over this file "
    "and any nested `AGENTS.md`. Local instructions may refine them; deviations "
    "require the documented policy exception process."
)


def render_entry() -> str:
    """Render the small mandatory delegation entry, without copying suite rules."""
    return (
        f"{ENTRY_HEADING}\n\n{READ_REQUIREMENT}\n\n"
        "Within their stated scope, its common rules take precedence over this file\n"
        "and any nested `AGENTS.md`. Local instructions may refine them; deviations\n"
        "require the documented policy exception process.\n\n"
        "The synchronized guide is owned by `uibcdf/molsyssuite`. It includes the\n"
        "[reusable-tool ownership rules](MOLSYSSUITE_GUIDE.md#modular-reusable-tools)\n"
        "and [working-instruction rules](MOLSYSSUITE_GUIDE.md#durable-working-instructions).\n"
        "For work under `devguide/`, also read `devguide/AGENTS.md` and its local\n"
        "reporting protocol. Keep repository-specific instructions below.\n"
    )


def mandatory_section(text: str) -> str:
    """Read an active root delegation section, excluding quoted examples."""
    active = active_markdown(text)
    first = re.search(r"(?m)^## [^\n]+", active)
    if first is None or first[0].strip() != ENTRY_HEADING:
        return ""
    section = re.search(
        rf"(?ms)^{re.escape(ENTRY_HEADING)}[ \t]*\n(.*?)(?=^#{{1,2}}[ \t]|\Z)",
        active,
    )
    return section[1] if section else ""


def _paragraphs(text: str) -> set[str]:
    return {" ".join(part.split()) for part in re.split(r"\n\s*\n", text)}


def common_policy_findings(policy: dict, text: str) -> list[Finding]:
    """Require the ambassador to route every accepted registered policy."""
    active = active_markdown(text)
    findings = []
    for name, rule in policy.get("policies", {}).items():
        path = rule.get("normative")
        if (
            rule.get("status") != "accepted"
            or not path
            or path == "MOLSYSSUITE_GUIDE.md"
        ):
            continue
        route = f"https://github.com/uibcdf/molsyssuite/blob/main/{path}"
        if route not in active:
            findings.append(
                Finding(
                    "COMMON_POLICY_ROUTE", f"canonical guide must route {name}: {path}"
                )
            )
    return findings


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
    section = mandatory_section(root_text)
    paragraphs = _paragraphs(section)
    if READ_REQUIREMENT not in paragraphs:
        findings.append(
            Finding(
                "INSTRUCTION_REQUIRED_GUIDE",
                "AGENTS.md must actively require reading and following the canonical guide",
            )
        )
    if PRECEDENCE_REQUIREMENT not in paragraphs:
        findings.append(
            Finding(
                "INSTRUCTION_PRECEDENCE",
                "AGENTS.md must declare scoped common-rule precedence and the policy exception route",
            )
        )
    if ROUTE not in section or "devguide/AGENTS.md" not in section:
        findings.append(
            Finding(
                "INSTRUCTION_ROOT_ROUTE",
                "AGENTS.md requires an active mandatory suite section routing to working instructions and devguide/AGENTS.md",
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
