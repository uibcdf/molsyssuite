"""Validate and report member adoption of MolSysSuite distribution policy."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from datetime import UTC, date, datetime
from pathlib import Path

import tomllib
import yaml

ROOT = Path(__file__).resolve().parents[2]
STATES = {"pending", "partial", "adopted", "excepted"}
READINESS = {"pending", "partial", "ready", "excepted"}
ACCESS = {"unknown", "confirmed", "unavailable", "not_applicable"}
ISSUE = re.compile(r"uibcdf/[A-Za-z0-9_.-]+#[1-9][0-9]*\Z")
SHARED_PUBLISHER = "uibcdf/molsyssuite/.github/workflows/publish-noarch-conda.yaml@"
BUILD_PROVIDER = "uibcdf/action-build-and-upload-conda-packages@"


def observe_publishers(data: dict, workspace: Path) -> dict:
    """Inspect committed active publisher calls at fetched main; never fetch or write."""
    rows = []
    repositories = [data["governance"]["repository"]] + [
        member["repository"] for member in data["members"]
    ]
    for repository in repositories:
        checkout = workspace / repository.split("/")[-1]

        def git(*arguments: str, git_root: Path = checkout) -> str:
            return subprocess.check_output(
                ["git", *arguments], cwd=git_root, text=True
            ).strip()

        revision = "origin/main"
        source_sha = git("rev-parse", revision)
        paths = git(
            "ls-tree", "-r", "--name-only", revision, ".github/workflows"
        ).splitlines()
        calls = []
        for relative in paths:
            path = Path(relative)
            # GitHub does not execute workflows kept under backups/subdirectories.
            if len(path.parts) != 3 or path.suffix not in {".yaml", ".yml"}:
                continue
            document = yaml.load(
                git("show", f"{revision}:{relative}"), Loader=yaml.BaseLoader
            )
            for name, job in (document or {}).get("jobs", {}).items():
                if not isinstance(job, dict):
                    continue
                uses = job.get("uses", "")
                if uses.startswith(SHARED_PUBLISHER):
                    calls.append({"workflow": relative, "job": name, "uses": uses})
                for step in job.get("steps", []):
                    uses = step.get("uses", "")
                    if (
                        uses.startswith(BUILD_PROVIDER)
                        and str(step.get("with", {}).get("upload", "true")).lower()
                        != "false"
                    ):
                        calls.append(
                            {
                                "workflow": relative,
                                "job": name,
                                "step": step.get("id", step.get("name", "")),
                                "uses": uses,
                            }
                        )
        kind = "no-conda-publisher-observed"
        if calls:
            kinds = {
                "shared-noarch"
                if call["uses"].startswith(SHARED_PUBLISHER)
                else "local-provider"
                for call in calls
            }
            kind = next(iter(kinds)) if len(kinds) == 1 else "mixed"
        rows.append(
            {
                "repository": repository,
                "source_sha": source_sha,
                "kind": kind,
                "calls": calls,
            }
        )
    return {
        "schema": "molsyssuite.conda-publishers@1",
        "observed_on": datetime.now(tz=UTC).date().isoformat(),
        "coordination_issue": "uibcdf/molsyssuite#79",
        "rows": rows,
    }


def publisher_inventory(data: dict) -> dict:
    """Read the single publisher inventory registered in suite.toml."""
    relative = data["policies"]["conda-publication"]["publisher-inventory"]
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def validate_publishers(data: dict, inventory: dict) -> list[str]:
    expected = {data["governance"]["repository"]} | {
        member["repository"] for member in data["members"]
    }
    errors = []
    seen = set()
    if inventory.get("schema") != "molsyssuite.conda-publishers@1":
        errors.append("publisher inventory: invalid schema")
    for row in inventory.get("rows", []):
        repository = row.get("repository", "")
        if repository not in expected or repository in seen:
            errors.append(f"publisher inventory: unknown or duplicate {repository}")
        seen.add(repository)
        if re.fullmatch(r"[0-9a-f]{40}", row.get("source_sha", "")) is None:
            errors.append(f"publisher inventory: {repository} missing source SHA")
        calls = row.get("calls", [])
        kinds = {
            "shared-noarch"
            if call.get("uses", "").startswith(SHARED_PUBLISHER)
            else "local-provider"
            for call in calls
        }
        actual = (
            (next(iter(kinds)) if len(kinds) == 1 else "mixed")
            if calls
            else "no-conda-publisher-observed"
        )
        if row.get("kind") != actual:
            errors.append(f"publisher inventory: {repository} kind contradicts calls")
        for call in calls:
            uses = call.get("uses", "")
            if not uses.startswith((SHARED_PUBLISHER, BUILD_PROVIDER)):
                errors.append(f"publisher inventory: {repository} unknown provider")
            if (
                uses.startswith(SHARED_PUBLISHER)
                and re.fullmatch(r"[0-9a-f]{40}", uses.split("@")[-1]) is None
            ):
                errors.append(
                    f"publisher inventory: {repository} mutable shared source"
                )
    errors.extend(
        f"publisher inventory: missing {repository}"
        for repository in sorted(expected - seen)
    )
    return errors


def validate(data: dict[str, object]) -> list[str]:
    expected = {
        str(member["repository"])
        for member in data.get("members", [])
        if "python-package" in member.get("capabilities", [])
    }
    seen: set[str] = set()
    errors: list[str] = []
    for review in data.get("python-distribution-reviews", []):
        repository = str(review.get("repository", ""))
        if repository not in expected:
            errors.append(f"python distribution review: unknown member {repository!r}")
        if repository in seen:
            errors.append(
                f"python distribution review: duplicate member {repository!r}"
            )
        seen.add(repository)
        state = review.get("state")
        readiness = review.get("ci-recipe")
        access = review.get("publication-access")
        issue = str(review.get("review-issue", ""))
        if state not in STATES:
            errors.append(
                f"python distribution review: {repository} invalid state {state!r}"
            )
        if readiness not in READINESS:
            errors.append(
                f"python distribution review: {repository} invalid ci-recipe {readiness!r}"
            )
        if access not in ACCESS:
            errors.append(
                f"python distribution review: {repository} invalid publication-access {access!r}"
            )
        if ISSUE.fullmatch(issue) is None:
            errors.append(
                f"python distribution review: {repository} lacks a review issue"
            )
        if state in {"partial", "adopted", "excepted"} and not issue.startswith(
            f"{repository}#"
        ):
            errors.append(
                f"python distribution review: {repository} needs a member issue"
            )
        if (
            state in {"partial", "adopted"}
            and not str(review.get("evidence", "")).strip()
        ):
            errors.append(f"python distribution review: {repository} lacks evidence")
        if state == "adopted" and readiness not in {"ready", "excepted"}:
            errors.append(
                f"python distribution review: {repository} adopted without CI/recipe readiness"
            )
        if state == "excepted":
            for key in ("reason", "owner", "removal-condition"):
                if not str(review.get(key, "")).strip():
                    errors.append(
                        f"python distribution review: {repository} lacks {key}"
                    )
            try:
                expires = date.fromisoformat(str(review.get("expires-on", "")))
            except ValueError:
                errors.append(
                    f"python distribution review: {repository} lacks expires-on"
                )
            else:
                if expires < datetime.now(tz=UTC).date():
                    errors.append(
                        f"python distribution review: {repository} exception expired"
                    )
    for repository in sorted(expected - seen):
        errors.append(f"python distribution review: missing {repository}")
    if "publisher-inventory" in data.get("policies", {}).get("conda-publication", {}):
        try:
            errors.extend(validate_publishers(data, publisher_inventory(data)))
        except (OSError, ValueError, KeyError, TypeError) as error:
            errors.append(f"publisher inventory: unavailable: {error}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--require-adopted", action="store_true")
    parser.add_argument(
        "--publishers",
        action="store_true",
        help="show the recorded publisher inventory",
    )
    parser.add_argument(
        "--publisher-kind",
        choices=(
            "shared-noarch",
            "local-provider",
            "mixed",
            "no-conda-publisher-observed",
        ),
    )
    parser.add_argument(
        "--observe-publishers",
        type=Path,
        metavar="WORKSPACE",
        help="emit a fresh read-only JSON inventory from fetched origin/main",
    )
    parser.add_argument(
        "--check-publishers",
        type=Path,
        metavar="WORKSPACE",
        help="check recorded calls against fetched origin/main without executing CI",
    )
    args = parser.parse_args()
    data = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
    if args.observe_publishers:
        print(json.dumps(observe_publishers(data, args.observe_publishers), indent=2))
        return 0
    if args.publishers or args.publisher_kind or args.check_publishers:
        inventory = publisher_inventory(data)
        errors = validate_publishers(data, inventory)
        if args.check_publishers:
            observed = observe_publishers(data, args.check_publishers)
            recorded = {row["repository"]: row for row in inventory["rows"]}
            for row in observed["rows"]:
                if row["calls"] != recorded.get(row["repository"], {}).get("calls"):
                    errors.append(
                        f"publisher inventory: {row['repository']} caller drift"
                    )
        rows = [
            row
            for row in inventory["rows"]
            if not args.publisher_kind or row["kind"] == args.publisher_kind
        ]
        if args.format == "json":
            print(json.dumps(dict(inventory, rows=rows, errors=errors), indent=2))
        else:
            for row in rows:
                print(f"{row['repository']}: {row['kind']}")
                for call in row["calls"]:
                    print(f"  {call['workflow']}:{call['job']} {call['uses']}")
            for error in errors:
                print(f"ERROR: {error}")
        return 1 if errors else 0
    reviews = data.get("python-distribution-reviews", [])
    errors = validate(data)
    if args.require_adopted:
        errors.extend(
            f"{review['repository']}: distribution is not adopted"
            for review in reviews
            if review.get("state") not in {"adopted", "excepted"}
        )
    if args.format == "json":
        print(
            json.dumps(
                {
                    "member_policy_release": data["governance"]["policy-release"],
                    "platform_contract_ref": data["governance"]["platform-policy-ref"],
                    "reviews": reviews,
                    "errors": errors,
                },
                indent=2,
            )
        )
    else:
        for review in reviews:
            print(
                f"{review['repository']}: {review['state']} "
                f"ci-recipe={review['ci-recipe']} "
                f"publication-access={review['publication-access']} "
                f"issue={review['review-issue']}"
            )
        for error in errors:
            print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
