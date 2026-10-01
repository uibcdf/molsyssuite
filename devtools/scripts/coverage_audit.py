"""Inspect public Codecov evidence without running tests or changing repositories."""

from __future__ import annotations

import argparse
import json
import math
import re
import urllib.error
import urllib.request
from datetime import datetime, timezone
from urllib.parse import quote
from xml.etree import ElementTree

MAX_BYTES = 8_000_000
TIMEOUT = 20
IDENTITY = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+")
SHA = re.compile(r"[a-f0-9]{40}")


class EvidenceUnavailable(RuntimeError):
    """The service did not provide public evidence; this is not non-applicability."""


class EvidenceInvalid(ValueError):
    """A received response cannot establish the claimed report."""


def public_payload(url: str, *, svg: bool = False) -> object:
    """Read bounded public JSON/SVG with no credentials; never expose response bodies."""
    request = urllib.request.Request(
        url, headers={"User-Agent": "MolSysSuite-coverage-audit"}
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            raw = response.read(MAX_BYTES + 1)
    except urllib.error.HTTPError as error:
        raise EvidenceUnavailable(f"HTTP {error.code}") from error
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        raise EvidenceUnavailable("network request failed") from error
    if len(raw) > MAX_BYTES:
        raise EvidenceInvalid("response exceeds the supported size")
    try:
        return raw.decode("utf-8") if svg else json.loads(raw)
    except (UnicodeError, ValueError) as error:
        raise EvidenceInvalid("response is not valid UTF-8/JSON") from error


def numeric_badge(svg: str) -> list[str]:
    """Extract rendered SVG percentage text; unknown/broken badges fail closed."""
    try:
        root = ElementTree.fromstring(svg)
    except ElementTree.ParseError as error:
        raise EvidenceInvalid("badge is not valid XML") from error
    if root.tag != "{http://www.w3.org/2000/svg}svg":
        raise EvidenceInvalid("badge is not an SVG")
    values = sorted(
        {
            text
            for node in root.iter("{http://www.w3.org/2000/svg}text")
            if re.fullmatch(
                r"(?:\d{1,3})(?:\.\d+)?%", text := "".join(node.itertext()).strip()
            )
            and 0 <= float(text[:-1]) <= 100
        }
    )
    if not values:
        raise EvidenceInvalid("badge has no rendered coverage percentage")
    return values


def complete_report(payload: object, branch: str) -> dict[str, object] | None:
    """Select explicit completed evidence, never totals inherited by a skipped commit.

    Codecov's timestamp is retained as commit_timestamp, not claimed as upload time.
    Zero coverage is valid; pending/error/skipped states cannot satisfy completion.
    """
    if not isinstance(payload, dict):
        raise EvidenceInvalid("commit is not an object")
    if payload.get("state") != "complete" or payload.get("branch") != branch:
        return None
    totals = payload.get("totals")
    if not isinstance(totals, dict):
        raise EvidenceInvalid("complete commit has no totals")
    value = totals.get("coverage")
    if (
        isinstance(value, bool)
        or not isinstance(value, (float, int))
        or not math.isfinite(value)
        or not 0 <= value <= 100
    ):
        raise EvidenceInvalid("coverage is not a finite percentage")
    sha = payload.get("commitid")
    if not isinstance(sha, str) or not SHA.fullmatch(sha):
        raise EvidenceInvalid("complete commit has no full source SHA")
    timestamp = payload.get("timestamp")
    try:
        parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except (AttributeError, TypeError, ValueError) as error:
        raise EvidenceInvalid("complete commit has no valid timestamp") from error
    if parsed.tzinfo is None:
        raise EvidenceInvalid("commit timestamp has no timezone")
    return {
        "source_sha": sha,
        "branch": branch,
        "commit_timestamp": timestamp,
        "coverage": value,
    }


def inspect_codecov(
    repository: str, *, fetch=public_payload, pages: int = 3
) -> dict[str, object]:
    """Audit one public project using GitHub's actual default branch.

    The newest completed commit in a bounded scan is reported separately from
    Codecov's branch cache and live SVG. No age, applicability, full-suite, latest
    HEAD or accepted upload-time claim is inferred. Missing evidence returns a
    distinct incomplete state. Inject fetch(url, svg=False) for offline consumers.
    """
    if not IDENTITY.fullmatch(repository) or pages < 1 or pages > 10:
        raise ValueError("use an owner/repository identity and 1–10 pages")
    receipt: dict[str, object] = {
        "repository": repository,
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "state": "incomplete",
    }
    try:
        github = fetch(f"https://api.github.com/repos/{repository}")
        if (
            not isinstance(github, dict)
            or not isinstance(github.get("default_branch"), str)
            or not github["default_branch"]
        ):
            raise EvidenceInvalid("GitHub default branch is missing")
        branch = github["default_branch"]
        receipt["default_branch"] = branch
        owner, name = repository.split("/")
        base = f"https://api.codecov.io/api/v2/github/{owner}/repos/{name}"
        receipt["project_url"] = f"https://app.codecov.io/gh/{repository}"
        receipt["badge_url"] = (
            f"https://codecov.io/gh/{repository}/branch/{quote(branch, safe='')}/graph/badge.svg"
        )
        # Services may independently be unavailable. Preserve usable evidence from the others.
        errors = {}
        try:
            receipt["badge_percentages"] = numeric_badge(
                fetch(receipt["badge_url"], svg=True)
            )
        except (EvidenceInvalid, EvidenceUnavailable) as error:
            errors["badge"] = str(error)
        try:
            cache = fetch(f"{base}/branches/{quote(branch, safe='')}/")
            if not isinstance(cache, dict) or cache.get("name") != branch:
                raise EvidenceInvalid("Codecov branch identity differs")
            head = cache.get("head_commit") or {}
            if not isinstance(head, dict):
                raise EvidenceInvalid("Codecov branch head is invalid")
            receipt["branch_updated_at"] = cache.get("updatestamp")
            receipt["branch_cache"] = {
                key: head.get(key)
                for key in ("commitid", "state", "timestamp", "totals")
            }
        except (EvidenceInvalid, EvidenceUnavailable) as error:
            errors["branch"] = str(error)
        try:
            receipt["scanned_pages"] = 0
            for page in range(1, pages + 1):
                commits = fetch(
                    f"{base}/commits/?branch={quote(branch, safe='')}&page_size=100&page={page}"
                )
                if not isinstance(commits, dict) or not isinstance(
                    commits.get("results"), list
                ):
                    raise EvidenceInvalid("commit list has no results array")
                receipt["scanned_pages"] = page
                candidates = [
                    report
                    for item in commits["results"]
                    if (report := complete_report(item, branch)) is not None
                ]
                if candidates:
                    receipt["latest_complete_report"] = max(
                        candidates,
                        key=lambda item: datetime.fromisoformat(
                            item["commit_timestamp"].replace("Z", "+00:00")
                        ),
                    )
                    break
                if not commits.get("next"):
                    break
            receipt["search_bound_pages"] = pages
        except (EvidenceInvalid, EvidenceUnavailable) as error:
            errors["commits"] = str(error)
        receipt["errors"] = errors
        if (
            receipt.get("latest_complete_report")
            and receipt.get("badge_percentages")
            and not errors
        ):
            receipt["state"] = "complete-report-observed"
        elif errors:
            receipt["state"] = "unavailable-or-invalid"
    except (EvidenceInvalid, EvidenceUnavailable) as error:
        receipt["state"] = "unavailable-or-invalid"
        receipt["errors"] = {"github": str(error)}
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--pages", type=int, default=3)
    args = parser.parse_args()
    try:
        receipt = inspect_codecov(args.repository, pages=args.pages)
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps(receipt, indent=2, allow_nan=False))
    return 0 if receipt["state"] == "complete-report-observed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
