"""Shared parsing and validation for MolSysSuite developer-guide reports."""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[2]
DEVGUIDE = ROOT / "devguide"

OPEN_STATUSES = ("active", "partial", "blocked", "open")
CLOSED_STATUSES = ("resolved", "withdrawn", "superseded")
VERIFICATIONS = {"reproduced", "measured", "inspected", "upstream", "asserted"}
SEVERITIES = {"critical", "high", "medium", "low"}
ISSUE = re.compile(r"^uibcdf/molsyssuite#[1-9]\d*$")
CROSS_REPOSITORY_ISSUE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+#[1-9]\d*$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
PYTHON_IDENTIFIER = re.compile(r"^[A-Za-z_]\w*$")
GUARD_POLICY_EFFECTIVE_DATE = "2026-09-20"
PYTEST_ROOTS = (PurePosixPath("tests"), PurePosixPath("devtools/tests"))


@dataclass(frozen=True)
class Report:
    path: Path
    fields: dict[str, object]
    kind: str
    archived: bool

    @property
    def relative_path(self) -> str:
        return self.path.relative_to(ROOT).as_posix()


def _value(raw: str) -> object:
    raw = raw.strip()
    if raw.startswith("[") and raw.endswith("]"):
        inner = raw[1:-1].strip()
        return [] if not inner else [item.strip() for item in inner.split(",")]
    return raw


def read_front_matter(path: Path) -> tuple[dict[str, object], list[str]]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or text.count("---\n") < 2:
        return {}, [f"{path.relative_to(ROOT)}: missing YAML front matter"]
    block = text.split("---\n", 2)[1]
    fields: dict[str, object] = {}
    for line in block.splitlines():
        if ":" not in line or line.startswith((" ", "#")):
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = _value(value)
    return fields, []


def load_reports() -> tuple[list[Report], list[str]]:
    reports: list[Report] = []
    errors: list[str] = []
    locations = (
        (DEVGUIDE / "pending_bugs", "bug", False),
        (DEVGUIDE / "pending_proposals", "proposal", False),
        (DEVGUIDE / "archive", "archive", True),
    )
    for directory, kind, archived in locations:
        if not directory.exists():
            errors.append(f"{directory.relative_to(ROOT)}: directory is missing")
            continue
        for path in sorted(directory.rglob("*.md")):
            if path.name == "README.md":
                continue
            fields, header_errors = read_front_matter(path)
            errors.extend(header_errors)
            if fields:
                reports.append(Report(path, fields, kind, archived))
    return reports, errors


def _references(value: object) -> list[str]:
    return value if isinstance(value, list) else []


def _is_test_class(node: ast.ClassDef) -> bool:
    if node.name.startswith("Test"):
        return True
    return any(
        (isinstance(base, ast.Name) and base.id.endswith("TestCase"))
        or (isinstance(base, ast.Attribute) and base.attr.endswith("TestCase"))
        for base in node.bases
    )


def _test_functions(nodes: list[ast.stmt]) -> dict[str, ast.AST]:
    return {
        node.name: node
        for node in nodes
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name.startswith("test_")
    }


def validate_pytest_guard(root: Path, selector: str) -> list[str]:
    """Validate the safe static pytest selector subset used by the Python profile."""

    if any(character.isspace() for character in selector) or any(
        token in selector for token in (",", "(", ")", "*", "?")
    ):
        return [f"guard {selector!r} uses unsupported selector syntax"]

    parts = selector.split("::")
    if not 1 <= len(parts) <= 3 or any(not part for part in parts):
        return [f"guard {selector!r} uses unsupported selector syntax"]
    if any("[" in part or "]" in part for part in parts[1:]):
        return [
            (
                f"guard {selector!r}: parameterized selectors are not supported by "
                "the static Python profile; name the unparameterized test or the module"
            )
        ]

    relative = PurePosixPath(parts[0])
    if (
        relative.is_absolute()
        or ".." in relative.parts
        or relative.suffix != ".py"
        or not any(relative.is_relative_to(base) for base in PYTEST_ROOTS)
    ):
        return [
            (
                f"guard {selector!r} must name a safe Python file under tests/ or "
                "devtools/tests/"
            )
        ]

    target = root.joinpath(*relative.parts)
    if not target.is_file():
        return [f"guard {selector!r} names a file that does not exist"]
    try:
        tree = ast.parse(target.read_text(encoding="utf-8"), filename=str(target))
    except (OSError, SyntaxError) as error:
        return [f"guard {selector!r} cannot be statically indexed: {error}"]

    functions = _test_functions(tree.body)
    classes = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.ClassDef) and _is_test_class(node)
    }
    if len(parts) == 1:
        if functions or any(_test_functions(node.body) for node in classes.values()):
            return []
        return [f"guard {selector!r} does not resolve to a collected test"]

    if not all(PYTHON_IDENTIFIER.fullmatch(part) for part in parts[1:]):
        return [f"guard {selector!r} uses unsupported selector syntax"]
    if len(parts) == 2 and parts[1] in functions:
        return []
    if len(parts) == 3:
        class_node = classes.get(parts[1])
        if class_node is not None and parts[2] in _test_functions(class_node.body):
            return []
    return [f"guard {selector!r} does not resolve to a collected test"]


def validate_report(report: Report) -> list[str]:
    errors: list[str] = []
    fields = report.fields
    prefix = report.relative_path
    required = ("summary", "issue", "status", "opened", "verification", "area")
    for key in required:
        if not fields.get(key):
            errors.append(f"{prefix}: {key} is missing or empty")

    issue = str(fields.get("issue", ""))
    if not ISSUE.fullmatch(issue):
        errors.append(f"{prefix}: issue must be uibcdf/molsyssuite#<positive integer>")

    opened = str(fields.get("opened", ""))
    if not DATE.fullmatch(opened):
        errors.append(f"{prefix}: opened must be an ISO date")

    status = str(fields.get("status", ""))
    if status not in OPEN_STATUSES + CLOSED_STATUSES:
        errors.append(f"{prefix}: unknown status {status!r}")
    if report.archived and status not in CLOSED_STATUSES:
        errors.append(f"{prefix}: an archived report must have a closed status")
    if not report.archived and status in CLOSED_STATUSES:
        errors.append(f"{prefix}: closed reports belong under devguide/archive/")

    closed = str(fields.get("closed", ""))
    if status in CLOSED_STATUSES and not DATE.fullmatch(closed):
        errors.append(f"{prefix}: a closed status requires an ISO closed date")
    if status in OPEN_STATUSES and closed:
        errors.append(f"{prefix}: an open status cannot have a closed date")

    verification = str(fields.get("verification", ""))
    if verification not in VERIFICATIONS:
        errors.append(f"{prefix}: unknown verification {verification!r}")

    area = fields.get("area")
    if not isinstance(area, list) or not area:
        errors.append(f"{prefix}: area must be a non-empty inline list")

    if report.kind == "bug" and fields.get("severity") not in SEVERITIES:
        errors.append(f"{prefix}: a bug requires a valid severity")

    blocked_by = _references(fields.get("blocked_by", []))
    if status == "blocked" and not blocked_by:
        errors.append(f"{prefix}: blocked must name at least one blocked_by issue")
    for key in ("blocked_by", "supersedes"):
        value = fields.get(key, [])
        if not isinstance(value, list):
            errors.append(f"{prefix}: {key} must be an inline list")
            continue
        for reference in value:
            if not CROSS_REPOSITORY_ISSUE.fullmatch(reference):
                errors.append(f"{prefix}: invalid {key} reference {reference!r}")

    if status == "resolved" and not (fields.get("guard") or fields.get("normative")):
        errors.append(f"{prefix}: resolved requires guard or normative")
    closed = str(fields.get("closed", ""))
    guard = fields.get("guard")
    if status == "resolved" and guard and closed >= GUARD_POLICY_EFFECTIVE_DATE:
        errors.extend(
            f"{prefix}: {error}" for error in validate_pytest_guard(ROOT, str(guard))
        )
    return errors


def validate_all() -> tuple[list[Report], list[str]]:
    reports, errors = load_reports()
    for report in reports:
        errors.extend(validate_report(report))
    return reports, errors
