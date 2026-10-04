"""Validate and report member reviews of the phased Python CI lane policy."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import UTC, date, datetime
from pathlib import Path

import tomllib

try:
    from devtools.scripts import ci_lane_inventory
except ImportError:
    import ci_lane_inventory

ROOT = Path(__file__).resolve().parents[2]
PILOT_PROFILES = ROOT / "devtools/ci_pilot_profiles.toml"
STATES = {"pending", "partial", "adopted", "excepted"}
TEST_LEVELS = {"unreviewed", "smoke", "full"}
PLATFORMS = {"linux", "macos", "windows"}
ISSUE = re.compile(r"uibcdf/[A-Za-z0-9_.-]+#[1-9][0-9]*\Z")


def validate(data: dict[str, object]) -> list[str]:
    """Keep CI claims explicit without equating configured jobs with passing runs."""
    expected = {
        str(member["repository"])
        for member in data.get("members", [])
        if "python-package" in member.get("capabilities", [])
    }
    seen: set[str] = set()
    errors: list[str] = []
    policy = data.get("policies", {}).get("python-ci", {})
    if policy.get("macos-architectures") != ["arm64"]:
        errors.append("python CI policy: prospective macOS support must be arm64 only")
    for review in data.get("python-ci-reviews", []):
        repository = str(review.get("repository", ""))
        if repository not in expected:
            errors.append(f"python CI review: unknown Python member {repository!r}")
        if repository in seen:
            errors.append(f"python CI review: duplicate member {repository!r}")
        seen.add(repository)
        state = review.get("state")
        level = review.get("routine-test-level")
        claims = review.get("platform-claims")
        claims_reviewed = review.get("platform-claims-reviewed")
        issue = str(review.get("review-issue", ""))
        if not isinstance(state, str) or state not in STATES:
            errors.append(f"python CI review: {repository} invalid state {state!r}")
        if not isinstance(level, str) or level not in TEST_LEVELS:
            errors.append(
                f"python CI review: {repository} invalid test level {level!r}"
            )
        if (
            not isinstance(claims, list)
            or any(
                not isinstance(platform, str) or platform not in PLATFORMS
                for platform in claims
            )
            or len(claims) != len(set(claims))
        ):
            errors.append(f"python CI review: {repository} invalid platform claims")
        if not isinstance(claims_reviewed, bool):
            errors.append(
                f"python CI review: {repository} lacks claims-reviewed boolean"
            )
        if ISSUE.fullmatch(issue) is None:
            errors.append(f"python CI review: {repository} lacks a review issue")
        if state in ("partial", "adopted", "excepted") and not issue.startswith(
            f"{repository}#"
        ):
            errors.append(f"python CI review: {repository} needs a member issue")
        if state == "pending" and (
            level != "unreviewed" or claims != [] or claims_reviewed is not False
        ):
            errors.append(f"python CI review: {repository} pending record makes claims")
        if (
            state in ("partial", "adopted")
            and not str(review.get("evidence", "")).strip()
        ):
            errors.append(f"python CI review: {repository} lacks review evidence")
        if state == "adopted":
            if level == "unreviewed" or claims_reviewed is not True:
                errors.append(f"python CI review: {repository} adoption is unreviewed")
            if level == "smoke" and not str(review.get("smoke-issue", "")).startswith(
                f"{repository}#"
            ):
                errors.append(
                    f"python CI review: {repository} smoke needs a member issue"
                )
            hosted_evidence = str(review.get("hosted-evidence", ""))
            run = rf"https://github\.com/{re.escape(repository)}/actions/runs/[1-9][0-9]*\b"
            if re.search(run, hosted_evidence) is None:
                errors.append(
                    f"python CI review: {repository} lacks a member hosted run URL"
                )
        if state == "excepted":
            for key in ("reason", "owner", "removal-condition"):
                if not str(review.get(key, "")).strip():
                    errors.append(f"python CI review: {repository} lacks {key}")
            try:
                expires = date.fromisoformat(str(review.get("expires-on", "")))
            except ValueError:
                errors.append(f"python CI review: {repository} lacks expires-on")
            else:
                if expires < datetime.now(tz=UTC).date():
                    errors.append(f"python CI review: {repository} exception expired")
    for repository in sorted(expected - seen):
        errors.append(f"python CI review: missing {repository}")
    return errors


def inspect_pilot(data: dict, workspace: Path, profiles: dict) -> dict:
    """Report bounded reviewed CI shapes; never fetch, run tests or enforce CI.

    Profiles bind selection review to exact input hashes. Drift and opaque
    routes remain unknown. Existing adoption and hosted evidence are separate.
    """
    if profiles.get("schema-version") != 1 or profiles.get("mode") != "informational":
        raise ValueError("pilot requires schema-version 1 and informational mode")
    members = {member["repository"]: member for member in data["members"]}
    reviews = {review["repository"]: review for review in data["python-ci-reviews"]}
    configured_profiles = profiles.get("profiles", [])
    if not isinstance(configured_profiles, list) or not configured_profiles:
        raise ValueError("pilot profiles must not be empty")
    seen = set()
    results = []
    for profile in configured_profiles:
        if not isinstance(profile, dict):
            raise TypeError("pilot profiles must be mappings")
        repository = profile.get("repository")
        if repository not in members or repository not in reviews or repository in seen:
            raise ValueError(f"unknown or duplicate pilot member: {repository}")
        seen.add(repository)
        review = reviews[repository]
        if profile.get("review-issue") != review["review-issue"]:
            raise ValueError(f"{repository}: profile must name its owning CI review")
        if not re.fullmatch(r"[0-9a-f]{40}", profile.get("reviewed-source", "")):
            raise ValueError(f"{repository}: profile needs immutable reviewed source")
        root = workspace / members[repository]["name"]
        bindings = profile.get("lanes", [])
        inputs = profile.get("inputs", {})
        if (
            not isinstance(bindings, list)
            or not bindings
            or not isinstance(inputs, dict)
            or not inputs
            or "pyproject.toml" not in inputs
        ):
            raise ValueError(f"{repository}: profile needs lanes and selection inputs")
        input_rows = []
        for relative, expected in inputs.items():
            path = Path(relative)
            if (
                path.is_absolute()
                or ".." in path.parts
                or not re.fullmatch(r"[0-9a-f]{64}", expected)
            ):
                raise ValueError(f"{repository}: invalid profile input {relative}")
            try:
                actual = hashlib.sha256((root / path).read_bytes()).hexdigest()
            except OSError:
                actual = None
            input_rows.append(
                {
                    "path": relative,
                    "expected_sha256": expected,
                    "observed_sha256": actual,
                    "matches": actual == expected,
                }
            )
        current = all(row["matches"] for row in input_rows)
        lanes = []
        schedules = []
        for binding in bindings:
            if (
                not isinstance(binding, dict)
                or not isinstance(binding.get("events"), dict)
                or not binding["events"]
            ):
                raise ValueError(f"{repository}: lane needs event targets")
            workflow = binding.get("workflow", "")
            relative = f".github/workflows/{workflow}"
            level = binding.get("test-level")
            if (
                Path(workflow).name != workflow
                or not workflow.endswith((".yml", ".yaml"))
                or relative not in inputs
            ):
                raise ValueError(f"{repository}: lane needs a bound active workflow")
            if level not in {"full", "smoke"} or not binding.get("job"):
                raise ValueError(f"{repository}: invalid test level or job")
            smoke_issue = str(binding.get("smoke-issue", ""))
            if level == "smoke" and (
                not smoke_issue.startswith(repository + "#")
                or ISSUE.fullmatch(smoke_issue) is None
            ):
                raise ValueError(f"{repository}: smoke profile needs owner issue")
            try:
                document = ci_lane_inventory.load_workflow(root / relative)
                rows = [
                    row
                    for row in ci_lane_inventory.inventory_workflow(
                        root / relative, repository
                    )
                    if row["job"] == binding["job"]
                ]
                events = document.get("on", {})
                if isinstance(events, dict):
                    schedules.extend(
                        {"workflow": workflow, **item}
                        for item in events.get("schedule", [])
                        if isinstance(item, dict)
                    )
                error = None
            except (OSError, RuntimeError, TypeError, ValueError) as exc:
                rows, error = [], str(exc)
            for event, versions in binding.get("events", {}).items():
                if (
                    event
                    not in {"push", "pull_request", "schedule", "workflow_dispatch"}
                    or not isinstance(versions, list)
                    or not versions
                ):
                    raise ValueError(f"{repository}: invalid event/version target")
                for version in versions:
                    if (
                        not isinstance(version, str)
                        or re.fullmatch(r"[0-9]+\.[0-9]+", version) is None
                    ):
                        raise ValueError(f"{repository}: invalid Python minor target")
                    candidates = [
                        row
                        for row in rows
                        if row["event"] == event
                        and row["os"].startswith("ubuntu")
                        and row["python"] == version
                        and row["test_command_observed"]
                    ]
                    uncertain = [
                        row
                        for row in rows
                        if row["event"] == event
                        and (
                            row["matrix_status"] == "unresolved"
                            or row["os"] == "unknown"
                            or row["python"] == "unknown"
                            or not row["test_command_observed"]
                        )
                    ]
                    if not current or error:
                        state = "unknown"
                    elif any(
                        row["event_eligible"] is True
                        and row["gating"] is True
                        and not row["path_filtered"]
                        and not row["tag_only"]
                        for row in candidates
                    ):
                        state = "configured"
                    elif any(
                        row["event_eligible"] is not False
                        and row["gating"] is not False
                        for row in candidates
                    ):
                        state = "conditional"
                    elif candidates and any(
                        row["gating"] is False for row in candidates
                    ):
                        state = "non_gating"
                    elif uncertain:
                        state = "unknown"
                    else:
                        state = "not_observed"
                    target_level = (
                        review["routine-test-level"] if event == "push" else "full"
                    )
                    lanes.append(
                        {
                            "workflow": workflow,
                            "job": binding["job"],
                            "event": event,
                            "python": version,
                            "os": "linux",
                            "state": state,
                            "reviewed_test_level": level if current else "unknown",
                            "target_test_level": target_level,
                            "reviewed_level_matches_target": current
                            and level == target_level,
                            "smoke_issue": binding.get("smoke-issue"),
                            "observations": candidates or uncertain,
                            "input_error": error,
                        }
                    )
        results.append(
            {
                "repository": repository,
                "review_issue": review["review-issue"],
                "existing_adoption_state": review["state"],
                "reviewed_source": profile["reviewed-source"],
                "profile_inputs_current": current,
                "inputs": input_rows,
                "lanes": lanes,
                "configured_schedules": schedules,
                "prior_hosted_review": review.get("hosted-evidence", ""),
                "execution_evidence": "not_requested",
                "backlog_clearance": "not_evaluated",
            }
        )
    return {
        "schema": "molsyssuite.ci-pilot@1",
        "mode": "informational",
        "coordination_issue": "uibcdf/molsyssuite#39",
        "members": results,
        "limits": [
            "configured and profile-reviewed selections, not executed outcomes",
            "no policy compliance or scientific/release qualification verdict",
            "ref filters, schedule/input contexts, wrappers and reusable calls may remain unresolved",
            "cron cadence and daily recovery semantics remain owner-reviewed",
            "historical review links are not new exact-head execution evidence",
            "no branch-protection, dependency-closure or backlog-watermark inference",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--require-adopted", action="store_true")
    parser.add_argument(
        "--pilot",
        type=Path,
        metavar="WORKSPACE",
        help="emit a read-only informational report using reviewed pilot profiles",
    )
    parser.add_argument(
        "--profiles",
        type=Path,
        default=PILOT_PROFILES,
        help="explicit pilot profile source; no effect on ordinary review status",
    )
    parser.add_argument(
        "--repository", action="append", help="select a member in the pilot profiles"
    )
    args = parser.parse_args(argv)
    data = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
    reviews = data.get("python-ci-reviews", [])
    errors = validate(data)
    if args.pilot:
        if args.require_adopted:
            parser.error("--pilot cannot be combined with --require-adopted")
        try:
            profiles = tomllib.loads(args.profiles.read_text(encoding="utf-8"))
            if args.repository:
                available = {row["repository"] for row in profiles.get("profiles", [])}
                if not set(args.repository) <= available:
                    raise ValueError("requested member has no pilot profile")
                profiles["profiles"] = [
                    row
                    for row in profiles["profiles"]
                    if row["repository"] in args.repository
                ]
            report = inspect_pilot(data, args.pilot, profiles)
        except (OSError, KeyError, TypeError, ValueError) as exc:
            parser.error(str(exc))
        report["profile_source"] = str(args.profiles)
        report["registry_errors"] = errors
        if args.format == "json":
            print(json.dumps(report, indent=2))
        else:
            print("INFORMATIONAL PILOT: no executed-test or policy-compliance verdict")
            for error in errors:
                print(f"REGISTRY FINDING: {error}")
            for member in report["members"]:
                print(
                    f"{member['repository']} profile_current={member['profile_inputs_current']} owner={member['review_issue']}"
                )
                for lane in member["lanes"]:
                    print(
                        f"  {lane['event']} Linux/Python {lane['python']} {lane['workflow']}:{lane['job']} {lane['state']} selection={lane['reviewed_test_level']}"
                    )
        return 0
    if args.repository:
        parser.error("--repository requires --pilot")
    if args.require_adopted:
        errors.extend(
            f"{review['repository']}: Python CI is not adopted"
            for review in reviews
            if review.get("state") not in {"adopted", "excepted"}
        )
    if args.format == "json":
        print(json.dumps({"reviews": reviews, "errors": errors}, indent=2))
    else:
        for review in reviews:
            print(
                f"{review['repository']}: {review['state']} "
                f"routine={review['routine-test-level']} "
                f"platform-claims-reviewed={review['platform-claims-reviewed']} "
                f"platform-claims={','.join(review['platform-claims']) or '(none)'} "
                f"issue={review['review-issue']}"
            )
        for error in errors:
            print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
