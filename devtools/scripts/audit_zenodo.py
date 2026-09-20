"""Validate the suite Zenodo inventory and optionally its public record evidence."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from datetime import date
from pathlib import Path

import tomllib

ROOT = Path(__file__).resolve().parents[2]
DOI_RE = re.compile(r"^10\.5281/zenodo\.\d+$")
CHECKSUM_RE = re.compile(r"^(?:md5:[0-9a-f]{32}|sha256:[0-9a-f]{64})$")
STATES = {
    "unknown",
    "enabled_reported",
    "webhook_observed",
    "release_published",
    "ingestion_pending",
    "verified",
    "absent",
    "invalid",
    "temporarily_unavailable",
    "not_applicable",
}
MODES = {"required", "optional", "exception"}
MAX_RESPONSE_BYTES = 2_000_000
REQUEST_TIMEOUT_SECONDS = 20


class PublicEvidenceInvalid(ValueError):
    """A public response was received but cannot serve as valid evidence."""


def _load(path: Path) -> dict[str, object]:
    return tomllib.loads(path.read_text(encoding="utf-8"))


def validate_inventory(
    policy: dict[str, object], inventory: dict[str, object]
) -> list[str]:
    """Return static inventory violations without network access."""
    errors: list[str] = []
    members = policy.get("members", [])
    registered = {str(member.get("repository")): member for member in members}
    components = inventory.get("components", [])
    if not isinstance(components, list):
        return ["zenodo inventory: components must be an array"]
    repositories = [str(item.get("repository", "")) for item in components]
    if len(repositories) != len(set(repositories)):
        errors.append("zenodo inventory: component repositories must be unique")
    missing = sorted(set(registered) - set(repositories))
    extra = sorted(set(repositories) - set(registered))
    if missing:
        errors.append("zenodo inventory: missing repositories: " + ", ".join(missing))
    if extra:
        errors.append(
            "zenodo inventory: unregistered repositories: " + ", ".join(extra)
        )

    stabilization = policy.get("stabilization", {})
    required_names = {
        name
        for cohort in ("wave-1", "infrastructure")
        for name in stabilization.get(cohort, [])
    }
    for repository, member in registered.items():
        mode = member.get("zenodo-archival")
        if mode not in MODES:
            errors.append(f"suite.toml: {repository} has invalid Zenodo mode {mode!r}")
        expected = "required" if member.get("name") in required_names else "optional"
        if mode != expected and mode != "exception":
            errors.append(
                f"suite.toml: {repository} Zenodo mode must be {expected!r} or an exception"
            )
        if mode == "exception" and not member.get("zenodo-exception-issue"):
            errors.append(f"suite.toml: {repository} Zenodo exception has no issue")

    for item in components:
        repository = str(item.get("repository", "<missing>"))
        state = item.get("state")
        if state not in STATES:
            errors.append(f"zenodo inventory: {repository} has invalid state {state!r}")
        observed = item.get("evidence-date")
        if not isinstance(observed, date):
            errors.append(f"zenodo inventory: {repository} has no ISO evidence date")
        if state == "not_applicable":
            member = registered.get(repository, {})
            if member.get("zenodo-archival") != "exception":
                errors.append(
                    f"zenodo inventory: {repository} is not_applicable without an exception"
                )
        if state != "verified":
            continue
        for field in (
            "verified-version",
            "concept-doi",
            "version-doi",
            "record-id",
            "evidence-issue",
            "archive-coverage",
            "files",
        ):
            if not item.get(field):
                errors.append(f"zenodo inventory: verified {repository} lacks {field}")
        for field in ("concept-doi", "version-doi"):
            if not DOI_RE.fullmatch(str(item.get(field, ""))):
                errors.append(f"zenodo inventory: {repository} has invalid {field}")
        files = item.get("files", [])
        if not isinstance(files, list):
            errors.append(f"zenodo inventory: {repository} files must be an array")
            continue
        names: list[str] = []
        for evidence in files:
            name = str(evidence.get("name", ""))
            names.append(name)
            if (
                not name
                or not isinstance(evidence.get("size"), int)
                or evidence["size"] < 1
            ):
                errors.append(
                    f"zenodo inventory: {repository} has invalid file evidence"
                )
            if not CHECKSUM_RE.fullmatch(str(evidence.get("checksum", ""))):
                errors.append(f"zenodo inventory: {repository} has invalid checksum")
        if len(names) != len(set(names)):
            errors.append(f"zenodo inventory: {repository} has duplicate file evidence")
    return errors


def verify_record(entry: dict[str, object], payload: dict[str, object]) -> list[str]:
    """Compare a public Zenodo record with one registered verified entry."""
    errors: list[str] = []
    repository = str(entry["repository"])
    metadata = payload.get("metadata")
    if not isinstance(metadata, dict):
        return ["public record metadata is missing"]
    if payload.get("id") != entry.get("record-id"):
        errors.append("public record ID differs from the registered evidence")
    if payload.get("doi") != entry.get("version-doi"):
        errors.append("public version DOI differs from the registered evidence")
    if payload.get("conceptdoi") != entry.get("concept-doi"):
        errors.append("public concept DOI differs from the registered evidence")
    if payload.get("status") != "published":
        errors.append("public record is not published")
    if metadata.get("version") != entry.get("verified-version"):
        errors.append("public version differs from the registered evidence")
    if metadata.get("access_right") != "open":
        errors.append("public record is not open access")
    resource_type = metadata.get("resource_type", {})
    if not isinstance(resource_type, dict) or resource_type.get("type") != "software":
        errors.append("public record is not typed as software")
    identifiers = metadata.get("related_identifiers", [])
    expected_source = f"https://github.com/{repository}"
    custom = metadata.get("custom", {})
    custom_repository = (
        custom.get("code:codeRepository") if isinstance(custom, dict) else None
    )
    related_repository_is = any(
        isinstance(item, dict) and item.get("identifier") == expected_source
        for item in identifiers
    )
    if not related_repository_is and custom_repository != expected_source:
        errors.append("public record does not identify the registered repository")
    expected_files = {
        (item["name"], item["size"], item["checksum"])
        for item in entry.get("files", [])
    }
    actual_files = {
        (item.get("key"), item.get("size"), item.get("checksum"))
        for item in payload.get("files", [])
        if isinstance(item, dict)
    }
    if actual_files != expected_files:
        errors.append("public file inventory differs from the registered evidence")
    return errors


def _fetch_record(record_id: int) -> dict[str, object]:
    request = urllib.request.Request(
        f"https://zenodo.org/api/records/{record_id}",
        headers={
            "Accept": "application/json",
            "User-Agent": "MolSysSuite-Zenodo-Audit/1",
        },
    )
    with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
        content_length = response.headers.get("Content-Length")
        if content_length and int(content_length) > MAX_RESPONSE_BYTES:
            raise PublicEvidenceInvalid("public response exceeds the audit size bound")
        body = response.read(MAX_RESPONSE_BYTES + 1)
    if len(body) > MAX_RESPONSE_BYTES:
        raise PublicEvidenceInvalid("public response exceeds the audit size bound")
    try:
        payload = json.loads(body)
    except json.JSONDecodeError as error:
        raise PublicEvidenceInvalid("public response is not valid JSON") from error
    if not isinstance(payload, dict):
        raise PublicEvidenceInvalid("public response is not a JSON object")
    return payload


def audit_public(inventory: dict[str, object]) -> int:
    """Verify every inventory entry currently asserted as verified."""
    outcome = 0
    for entry in inventory.get("components", []):
        repository = entry.get("repository")
        state = str(entry.get("state"))
        if state != "verified":
            print(f"{state.upper()} {repository}")
            continue
        try:
            payload = _fetch_record(int(entry["record-id"]))
        except PublicEvidenceInvalid as error:
            print(f"INVALID {repository}: {error}", file=sys.stderr)
            outcome = max(outcome, 1)
            continue
        except (OSError, TimeoutError, ValueError) as error:
            print(f"TEMPORARILY_UNAVAILABLE {repository}: {error}", file=sys.stderr)
            outcome = max(outcome, 2)
            continue
        errors = verify_record(entry, payload)
        if errors:
            for error in errors:
                print(f"INVALID {repository}: {error}", file=sys.stderr)
            outcome = max(outcome, 1)
        else:
            print(
                f"VERIFIED {repository} {entry['verified-version']} "
                f"{entry['version-doi']}"
            )
    return outcome


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--public", action="store_true")
    arguments = parser.parse_args()
    policy = _load(ROOT / "suite.toml")
    inventory_path = ROOT / policy["policies"]["zenodo-archival"]["inventory"]
    inventory = _load(inventory_path)
    errors = validate_inventory(policy, inventory)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("Zenodo inventory is structurally valid.")
    return audit_public(inventory) if arguments.public else 0


if __name__ == "__main__":
    sys.exit(main())
