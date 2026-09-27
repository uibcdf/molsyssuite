"""Validate and report member reviews of the phased Python CI lane policy."""

from __future__ import annotations

import argparse
import json
import re
from datetime import UTC, date, datetime
from pathlib import Path

import tomllib

ROOT = Path(__file__).resolve().parents[2]
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--require-adopted", action="store_true")
    args = parser.parse_args()
    data = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
    reviews = data.get("python-ci-reviews", [])
    errors = validate(data)
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
