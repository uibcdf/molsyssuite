"""Report guide-copy and policy-caller adoption as independent records."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tomllib
from dataclasses import asdict, dataclass
from datetime import UTC, date, datetime
from pathlib import Path

if __package__:
    from . import check_repository, suite_policy
else:  # Direct scripts resolve siblings from their own script directory.
    import check_repository
    import suite_policy

ROOT = Path(__file__).resolve().parents[2]
POLICY_CALLER = re.compile(
    r"uibcdf/molsyssuite/\.github/workflows/"
    r"check-python-repository\.yaml@(?P<release>[^\s'\"}]+)"
)
KINDS = ("guide", "policy")
CURRENT_STATES = {"current", "compatible", "excepted"}


@dataclass(frozen=True)
class AdoptionRecord:
    """One consumer-owned adoption fact and its next action."""

    kind: str
    repository: str
    item: str
    state: str
    owner: str
    expected: str
    observed: str
    source_revision: str
    consumer_revision: str
    exception: str
    next_action: str


def _load_policy() -> dict[str, object]:
    return tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))


def _name(repository: str) -> str:
    return repository.rsplit("/", 1)[-1]


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_exceptions(policy: dict[str, object]) -> list[str]:
    """Return schema, relationship, and expiry errors for adoption exceptions."""
    registered = {str(member["repository"]) for member in policy.get("members", [])}
    guide_consumers = {
        (str(guide["filename"]), str(consumer))
        for guide in policy.get("guides", [])
        for consumer in guide["consumers"]
    }
    today = datetime.now(tz=UTC).date()
    errors: list[str] = []
    seen: set[tuple[str, str, str]] = set()
    for index, exception in enumerate(policy.get("adoption-exceptions", []), start=1):
        prefix = f"adoption exception {index}"
        kind = str(exception.get("kind", ""))
        repository = str(exception.get("repository", ""))
        item = str(exception.get("item", ""))
        key = (kind, repository, item)
        if key in seen:
            errors.append(f"{prefix}: duplicate relationship {key!r}")
        seen.add(key)
        if kind not in KINDS:
            errors.append(f"{prefix}: kind must be guide or policy")
        if repository not in registered:
            errors.append(f"{prefix}: unknown repository {repository!r}")
        if kind == "guide" and (item, repository) not in guide_consumers:
            errors.append(f"{prefix}: item is not a registered guide relationship")
        if kind == "policy" and item != "policy-caller":
            errors.append(f"{prefix}: policy item must be 'policy-caller'")
        issue = str(exception.get("issue", ""))
        if not re.fullmatch(r"uibcdf/[A-Za-z0-9_.-]+#[1-9][0-9]*", issue):
            errors.append(f"{prefix}: issue must identify a UIBCDF GitHub issue")
        if not str(exception.get("reason", "")).strip():
            errors.append(f"{prefix}: reason is required")
        if not str(exception.get("removal-condition", "")).strip():
            errors.append(f"{prefix}: removal-condition is required")
        try:
            expires = date.fromisoformat(str(exception.get("expires-on", "")))
        except ValueError:
            errors.append(f"{prefix}: expires-on must be an ISO date")
        else:
            if expires < today:
                errors.append(f"{prefix}: exception expired on {expires.isoformat()}")
    return errors


def _exception(
    policy: dict[str, object], *, kind: str, repository: str, item: str
) -> dict[str, object] | None:
    today = datetime.now(tz=UTC).date()
    for candidate in policy.get("adoption-exceptions", []):
        if (
            candidate.get("kind") != kind
            or candidate.get("repository") != repository
            or candidate.get("item") != item
        ):
            continue
        try:
            expires = date.fromisoformat(str(candidate.get("expires-on", "")))
        except ValueError:
            return None
        if expires < today:
            return None
        return candidate
    return None


def _apply_exception(
    record: AdoptionRecord, policy: dict[str, object]
) -> AdoptionRecord:
    latest = record.kind == "policy" and suite_policy.requires_latest_policy(policy)
    if record.state == "current" or (record.state == "compatible" and not latest):
        return record
    exception = (
        suite_policy.active_policy_exception(policy, record.repository)
        if latest and record.item == "policy-caller"
        else _exception(
            policy, kind=record.kind, repository=record.repository, item=record.item
        )
    )
    if exception is None:
        return record
    issue = str(exception["issue"])
    expires = str(exception["expires-on"])
    return AdoptionRecord(
        **{
            **asdict(record),
            "state": "excepted",
            "exception": issue,
            "next_action": (
                f"resolve {issue} before {expires}: "
                f"{exception.get('removal-condition', '<missing removal condition>')}"
            ),
        }
    )


def _guide_records(workspace: Path, policy: dict[str, object]) -> list[AdoptionRecord]:
    records: list[AdoptionRecord] = []
    for guide in policy.get("guides", []):
        filename = str(guide["filename"])
        source_owner = str(guide["owner"])
        source_path = str(guide["source"])
        source = workspace / _name(source_owner) / source_path
        for raw_consumer in guide["consumers"]:
            consumer = str(raw_consumer)
            target = workspace / _name(consumer) / filename
            expected = f"{source_owner}:{source_path}"
            if not source.is_file():
                record = AdoptionRecord(
                    kind="guide",
                    repository=consumer,
                    item=filename,
                    state="unavailable",
                    owner=consumer,
                    expected=expected,
                    observed="<source-unavailable>",
                    source_revision="",
                    consumer_revision=_digest(target) if target.is_file() else "",
                    exception="",
                    next_action=f"restore canonical source {expected}",
                )
            elif not (workspace / _name(consumer)).is_dir():
                record = AdoptionRecord(
                    kind="guide",
                    repository=consumer,
                    item=filename,
                    state="unavailable",
                    owner=consumer,
                    expected=expected,
                    observed="<consumer-unavailable>",
                    source_revision=_digest(source),
                    consumer_revision="",
                    exception="",
                    next_action=f"provide checkout for {consumer}",
                )
            elif not target.is_file():
                record = AdoptionRecord(
                    kind="guide",
                    repository=consumer,
                    item=filename,
                    state="missing",
                    owner=consumer,
                    expected=expected,
                    observed="<missing>",
                    source_revision=_digest(source),
                    consumer_revision="",
                    exception="",
                    next_action=(
                        "sync with sync_vendored_guides.py "
                        f"--guide {filename} --repository {_name(consumer)} --write"
                    ),
                )
            else:
                source_revision = _digest(source)
                consumer_revision = _digest(target)
                state = "current" if source_revision == consumer_revision else "stale"
                record = AdoptionRecord(
                    kind="guide",
                    repository=consumer,
                    item=filename,
                    state=state,
                    owner=consumer,
                    expected=expected,
                    observed=f"{consumer}:{filename}",
                    source_revision=source_revision,
                    consumer_revision=consumer_revision,
                    exception="",
                    next_action=(
                        "none"
                        if state == "current"
                        else (
                            "sync with sync_vendored_guides.py "
                            f"--guide {filename} --repository {_name(consumer)} --write"
                        )
                    ),
                )
            records.append(_apply_exception(record, policy))
    return records


def _policy_records(workspace: Path, policy: dict[str, object]) -> list[AdoptionRecord]:
    required = str(policy["policies"]["release-version"]["required-policy-release"])
    central = str(policy["governance"]["policy-release"])
    release_gates = check_repository.accepted_release_gates(policy)
    records: list[AdoptionRecord] = []
    latest = suite_policy.requires_latest_policy(policy)
    for member in policy.get("members", []):
        python_member = "python-package" in member.get("capabilities", [])
        if not latest and not python_member:
            continue
        repository = str(member["repository"])
        root = workspace / _name(repository)
        workflow_root = root / ".github/workflows"
        if not root.is_dir():
            state = "unavailable"
            observed = "<consumer-unavailable>"
            next_action = f"provide checkout for {repository}"
        else:
            paths = (
                sorted(workflow_root.glob("*.yml"))
                + sorted(workflow_root.glob("*.yaml"))
                if workflow_root.is_dir()
                else []
            )
            documents = [
                path.read_text(encoding="utf-8", errors="replace") for path in paths
            ]
            workflow_text = "\n".join(documents)
            parse_failure = False
            try:
                releases = (
                    suite_policy.policy_caller_releases(documents)
                    if latest
                    else sorted(
                        {
                            match.group("release")
                            for match in POLICY_CALLER.finditer(workflow_text)
                        }
                    )
                )
            except (TypeError, ValueError):
                releases = []
                parse_failure = True
            observed = ",".join(releases) if releases else "<missing>"
            if parse_failure:
                state = "unavailable"
                observed = "<workflow-unavailable>"
            elif not releases:
                state = "missing"
            elif releases == [central]:
                state = "current"
            elif (all if latest else any)(
                release in release_gates for release in releases
            ) and (
                not python_member
                or not check_repository.missing_ruff_ci_commands(
                    workflow_text,
                    check_repository.accepted_quality_callers(policy, member),
                )
            ):
                state = "compatible"
            else:
                state = "stale"
            next_action = (
                "none"
                if state == "current"
                else (
                    f"adopt latest published policy {central}; technical compatibility is not adoption"
                    if latest
                    else f"review adoption of central {central} when scheduled"
                    if state == "compatible"
                    else (
                        f"review caller compatibility and adopt an admitted release "
                        f"at or above {required}"
                    )
                )
            )
        record = AdoptionRecord(
            kind="policy",
            repository=repository,
            item="policy-caller",
            state=state,
            owner=repository,
            expected=central,
            observed=observed,
            source_revision=central,
            consumer_revision=observed,
            exception="",
            next_action=next_action,
        )
        records.append(_apply_exception(record, policy))
    if latest and policy["policies"]["adoption-lifecycle"].get("include-central"):
        repository = str(policy["governance"]["repository"])
        root = workspace / _name(repository)
        observed = "<central-unavailable>"
        state = "unavailable"
        try:
            own_policy = tomllib.loads(
                (root / "suite.toml").read_text(encoding="utf-8")
            )
            observed = str(own_policy["governance"]["policy-release"])
            state = (
                "current"
                if observed == central
                and suite_policy.requires_latest_policy(own_policy)
                else "stale"
            )
        except (OSError, ValueError, KeyError, TypeError):
            pass
        records.append(
            AdoptionRecord(
                kind="policy",
                repository=repository,
                item="central-governance",
                state=state,
                owner=repository,
                expected=central,
                observed=observed,
                source_revision=central,
                consumer_revision=observed,
                exception="",
                next_action="receive exact-source central governance independently; member reusable caller is not applicable"
                if state == "current"
                else f"adopt {central} in central registry and live governance",
            )
        )
    return records


def satisfied(record: AdoptionRecord, policy: dict) -> bool:
    """Separate current-policy adoption from the legacy capability check."""
    if record.kind == "policy" and suite_policy.requires_latest_policy(policy):
        return record.state in {"current", "excepted"}
    return record.state in CURRENT_STATES


def inventory(
    workspace: Path, *, policy: dict[str, object] | None = None
) -> list[AdoptionRecord]:
    """Return the complete current guide and policy-caller adoption inventory."""
    workspace = workspace.resolve()
    policy = policy or _load_policy()
    records = _guide_records(workspace, policy) + _policy_records(workspace, policy)
    return sorted(records, key=lambda item: (item.repository, item.kind, item.item))


def _select(
    records: list[AdoptionRecord], kinds: list[str], repositories: list[str]
) -> list[AdoptionRecord]:
    selected_kinds = set(kinds or KINDS)
    selected_repositories = {value.casefold() for value in repositories}
    return [
        record
        for record in records
        if record.kind in selected_kinds
        and (
            not selected_repositories
            or record.repository.casefold() in selected_repositories
            or _name(record.repository).casefold() in selected_repositories
        )
    ]


def _render_text(records: list[AdoptionRecord]) -> str:
    lines = []
    for record in records:
        source_revision = (
            record.source_revision[:12]
            if record.kind == "guide"
            else record.source_revision
        )
        consumer_revision = (
            record.consumer_revision[:12]
            if record.kind == "guide"
            else record.consumer_revision
        )
        revisions = f" source={source_revision or '-'} copy={consumer_revision or '-'}"
        exception = f" exception={record.exception}" if record.exception else ""
        lines.append(
            f"{record.state.upper()} {record.kind} {record.repository} {record.item}"
            f" owner={record.owner} expected={record.expected}"
            f" observed={record.observed}{revisions}{exception}"
            f" next={record.next_action}"
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "workspace",
        nargs="?",
        type=Path,
        default=ROOT.parent,
        help="directory containing sibling repository checkouts",
    )
    parser.add_argument("--kind", choices=KINDS, action="append", default=[])
    parser.add_argument("--repository", action="append", default=[])
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument(
        "--verify-published-policy",
        action="store_true",
        help="verify the registered target against all authoritative published policy tags",
    )
    parser.add_argument(
        "--receipt",
        type=Path,
        help="retain bounded selected records and exact source/workflow hashes",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="return nonzero for stale, missing, unavailable, or expired records",
    )
    arguments = parser.parse_args()
    policy = _load_policy()
    published = None
    if arguments.verify_published_policy:
        try:
            published = suite_policy.published_policy_target()
            if published["release"] != policy["governance"]["policy-release"]:
                raise ValueError(
                    "registered target differs from latest published policy"
                )
        except (OSError, ValueError, subprocess.SubprocessError) as error:
            if arguments.receipt is not None:
                arguments.receipt.parent.mkdir(parents=True, exist_ok=True)
                arguments.receipt.write_text(
                    json.dumps(
                        {
                            "schema": "molsyssuite.policy-adoption-observation@1",
                            "observed_at_utc": datetime.now(UTC).isoformat(),
                            "status": "target-unavailable",
                            "target": policy["governance"]["policy-release"],
                            "published_target": published,
                            "failure_class": type(error).__name__,
                            "records": [],
                            "sources": [],
                            "scope": "target not verified; adoption inventory not acquired",
                        },
                        indent=2,
                    )
                    + "\n",
                    encoding="utf-8",
                )
            print(f"policy target unavailable: {type(error).__name__}", file=sys.stderr)
            return 2
    records = _select(
        inventory(arguments.workspace, policy=policy),
        arguments.kind,
        arguments.repository,
    )
    if arguments.receipt is not None:
        sources = []
        for repository in sorted({r.repository for r in records}):
            root = arguments.workspace / _name(repository)
            try:
                head = subprocess.check_output(
                    ["git", "-C", str(root), "rev-parse", "HEAD"],
                    text=True,
                    stderr=subprocess.DEVNULL,
                ).strip()
            except (OSError, subprocess.SubprocessError):
                head = ""
            paths = sorted((root / ".github/workflows").glob("*"))
            sources.append(
                {
                    "repository": repository,
                    "source_commit": head,
                    "workflow_sha256": {
                        p.relative_to(root).as_posix(): _digest(p)
                        for p in paths
                        if p.is_file() and p.suffix in {".yaml", ".yml"}
                    },
                }
            )
        arguments.receipt.parent.mkdir(parents=True, exist_ok=True)
        arguments.receipt.write_text(
            json.dumps(
                {
                    "schema": "molsyssuite.policy-adoption-observation@1",
                    "observed_at_utc": datetime.now(UTC).isoformat(),
                    "target": policy["governance"]["policy-release"],
                    "published_target": published,
                    "records": [asdict(record) for record in records],
                    "sources": sources,
                    "scope": "selected source declarations only; no executed gate, semantic compliance or scientific/public qualification inferred",
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
    if arguments.format == "json":
        print(json.dumps([asdict(record) for record in records], indent=2))
    else:
        print(_render_text(records))
    if arguments.check and any(not satisfied(record, policy) for record in records):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
