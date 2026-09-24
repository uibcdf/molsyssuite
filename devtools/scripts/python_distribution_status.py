"""Validate and report member adoption of the inherited MOLI distribution policy."""

from __future__ import annotations

import argparse
import json
import re
from datetime import UTC, date, datetime
from pathlib import Path

import tomllib

ROOT = Path(__file__).resolve().parents[2]
STATES = {"pending", "partial", "adopted", "excepted"}
READINESS = {"pending", "partial", "ready", "excepted"}
ACCESS = {"unknown", "confirmed", "unavailable", "not_applicable"}
ISSUE = re.compile(r"uibcdf/[A-Za-z0-9_.-]+#[1-9][0-9]*\Z")


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
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--require-adopted", action="store_true")
    args = parser.parse_args()
    data = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
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
