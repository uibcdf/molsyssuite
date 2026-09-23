"""Inspect member review state for the inherited MOLI Python ecosystem policies."""

from __future__ import annotations

import argparse
import json
import re
from datetime import UTC, date, datetime
from pathlib import Path

import tomllib

ROOT = Path(__file__).resolve().parents[2]
STATES = {"pending", "partial", "adopted", "excepted"}
POLICIES = ("support-libraries", "developer-tools")
ISSUE = re.compile(r"uibcdf/[A-Za-z0-9_.-]+#[1-9][0-9]*\Z")


def validate(data: dict[str, object]) -> list[str]:
    """Require one honest review record for each Python member and policy."""

    expected = {
        str(member["repository"])
        for member in data.get("members", [])
        if "python-package" in member.get("capabilities", [])
    }
    reviews = data.get("python-ecosystem-reviews", [])
    seen: set[str] = set()
    errors: list[str] = []
    for review in reviews:
        repository = str(review.get("repository", ""))
        if repository not in expected:
            errors.append(
                f"python ecosystem review: unknown Python member {repository!r}"
            )
        if repository in seen:
            errors.append(f"python ecosystem review: duplicate member {repository!r}")
        seen.add(repository)
        issue = str(review.get("review-issue", ""))
        if ISSUE.fullmatch(issue) is None:
            errors.append(f"python ecosystem review: {repository} lacks a review issue")
        for policy in POLICIES:
            state = review.get(policy)
            if state not in STATES:
                errors.append(
                    f"python ecosystem review: {repository} has invalid {policy} state {state!r}"
                )
            if state in {"partial", "adopted", "excepted"} and not issue.startswith(
                f"{repository}#"
            ):
                errors.append(
                    f"python ecosystem review: {repository} needs a member review issue for {policy}"
                )
            if state == "adopted" and not review.get(f"{policy}-evidence"):
                errors.append(
                    f"python ecosystem review: {repository} claims {policy} adoption without evidence"
                )
            if state == "excepted":
                for key in ("reason", "owner", "removal-condition"):
                    if not str(review.get(f"{policy}-{key}", "")).strip():
                        errors.append(
                            f"python ecosystem review: {repository} lacks {policy}-{key}"
                        )
                try:
                    expires = date.fromisoformat(
                        str(review.get(f"{policy}-expires-on", ""))
                    )
                except ValueError:
                    errors.append(
                        f"python ecosystem review: {repository} lacks {policy}-expires-on"
                    )
                else:
                    if expires < datetime.now(tz=UTC).date():
                        errors.append(
                            f"python ecosystem review: {repository} {policy} exception expired"
                        )
    for repository in sorted(expected - seen):
        errors.append(f"python ecosystem review: missing {repository}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--require-adopted", action="store_true")
    args = parser.parse_args()
    data = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
    errors = validate(data)
    reviews = data.get("python-ecosystem-reviews", [])
    if args.format == "json":
        print(
            json.dumps(
                {
                    "platform_policy_ref": data["governance"]["platform-policy-ref"],
                    "reviews": reviews,
                    "errors": errors,
                },
                indent=2,
            )
        )
    else:
        for review in reviews:
            print(
                f"{review['repository']}: "
                f"support-libraries={review['support-libraries']} "
                f"developer-tools={review['developer-tools']} "
                f"issue={review['review-issue']}"
            )
        for error in errors:
            print(f"ERROR: {error}")
    if args.require_adopted:
        for review in reviews:
            for policy in POLICIES:
                if review.get(policy) not in {"adopted", "excepted"}:
                    errors.append(f"{review['repository']}: {policy} is not adopted")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
