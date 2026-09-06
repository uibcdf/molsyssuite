"""Render queue indexes from report front matter."""

from __future__ import annotations

import argparse
import sys

try:
    from devtools.scripts.devguide_reports import (
        OPEN_STATUSES,
        ROOT,
        Report,
        validate_all,
    )
except ImportError:
    from devguide_reports import OPEN_STATUSES, ROOT, Report, validate_all


BEGIN = "<!-- generated: devguide_index -->"
END = "<!-- /generated -->"
QUEUES = {
    "bug": ROOT / "devguide" / "pending_bugs" / "README.md",
    "proposal": ROOT / "devguide" / "pending_proposals" / "README.md",
}
HEADINGS = {
    "active": "In progress",
    "partial": "Partially resolved",
    "blocked": "Blocked",
    "open": "Open",
}


def _issue_link(reference: str) -> str:
    repository, number = reference.rsplit("#", 1)
    return f"[#{number}](https://github.com/{repository}/issues/{number})"


def _render(reports: list[Report]) -> str:
    if not reports:
        return "*No entries.*"
    lines: list[str] = []
    for status in OPEN_STATUSES:
        group = sorted(
            (report for report in reports if report.fields["status"] == status),
            key=lambda report: report.path.name,
        )
        if not group:
            continue
        lines.extend((f"### {HEADINGS[status]} ({len(group)})", ""))
        for report in group:
            fields = report.fields
            qualifiers = [
                str(fields[key])
                for key in ("severity", "verification")
                if fields.get(key)
            ]
            suffix = f" *({', '.join(qualifiers)})*" if qualifiers else ""
            lines.append(
                f"- [`{report.path.name}`]({report.path.name}) — "
                f"{_issue_link(str(fields['issue']))} — {fields['summary']}{suffix}"
            )
        lines.append("")
    return "\n".join(lines).rstrip()


def _replace(text: str, body: str) -> str:
    if BEGIN not in text or END not in text:
        raise ValueError("generated index markers are missing")
    head, rest = text.split(BEGIN, 1)
    _, tail = rest.split(END, 1)
    return f"{head}{BEGIN}\n\n{body}\n\n{END}{tail}"


def process(check: bool) -> list[str]:
    reports, errors = validate_all()
    if errors:
        raise ValueError("\n".join(errors))
    stale: list[str] = []
    for kind, readme in QUEUES.items():
        selected = [
            report for report in reports if report.kind == kind and not report.archived
        ]
        updated = _replace(readme.read_text(encoding="utf-8"), _render(selected))
        if updated == readme.read_text(encoding="utf-8"):
            continue
        stale.append(readme.relative_to(ROOT).as_posix())
        if not check:
            readme.write_text(updated, encoding="utf-8")
    return stale


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    try:
        stale = process(arguments.check)
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1
    if arguments.check and stale:
        print("stale generated indexes: " + ", ".join(stale), file=sys.stderr)
        return 1
    for path in stale:
        print(f"wrote {path}")
    if arguments.check:
        print("Generated queue indexes are current.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
