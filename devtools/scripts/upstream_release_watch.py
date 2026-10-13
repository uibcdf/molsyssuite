"""Review official upstream releases against an owner-selected compatibility range.

Default execution is read-only. --notify creates one issue per excluded major,
respecting existing open or closed human follow-ups without duplicate notices.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import quote

from packaging.specifiers import SpecifierSet
from packaging.version import Version


def repository_name(value: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*/[A-Za-z0-9_][A-Za-z0-9_.-]*", value):
        raise ValueError("watch needs an owner/repository identity")
    return value


def inspect_release(provider: str, release: dict, supported: str) -> dict:
    """Validate official stable release identity; range membership is not testing."""
    repository_name(provider)
    if not isinstance(release, dict):
        raise ValueError("invalid official release response")
    tag = release.get("tag_name")
    if not isinstance(tag, str) or not re.fullmatch(r"v?\d+\.\d+\.\d+", tag):
        raise ValueError("watch requires a recognized stable release tag")
    version = Version(tag.removeprefix("v"))
    url = f"https://github.com/{provider}/releases/tag/{quote(tag, safe='')}"
    if release.get("draft") is not False or release.get("prerelease") is not False or release.get("html_url") != url:
        raise ValueError("watch requires the provider's official stable release")
    allowed = SpecifierSet(supported)
    return {
        "provider": provider, "version": str(version), "url": url,
        "supported_range": str(allowed),
        "state": "within-declared-range" if version in allowed else "review-required",
        "marker": f"<!-- molsyssuite-upstream-watch:{provider}:major-{version.major} -->",
        "title": f"Review {provider} {version.major}.x compatibility",
    }


def existing_notice(issues: list[dict], notice: dict) -> dict | None:
    """Find the durable marker, without search-index lag or overwriting humans."""
    if any(not isinstance(issue, dict) for issue in issues):
        raise ValueError("invalid issue identity inventory")
    matches = [issue for issue in issues if not issue.get("pull_request")
               and notice["marker"] in (issue.get("body") or "")]
    if len(matches) > 1:
        raise ValueError("multiple upstream follow-ups need owner reconciliation")
    return matches[0] if matches else None


def gh_json(arguments: list[str]) -> object:
    return json.loads(subprocess.run(
        ["gh", *arguments], check=True, text=True, capture_output=True, timeout=60,
    ).stdout)


def deliver_notice(owner: str, notice: dict, context: str, *, request=gh_json) -> dict:
    """Idempotent authorized write; never auto-admit, reopen or close a review."""
    repository_name(owner)
    if notice["state"] != "review-required":
        return {"state": "no-notice-needed"}
    pages = request(["api", "--paginate", "--slurp",
                     f"repos/{owner}/issues?state=all&per_page=100"])
    if not isinstance(pages, list) or any(not isinstance(page, list) for page in pages):
        raise ValueError("invalid issue inventory; refusing duplicate-prone creation")
    previous = existing_notice([issue for page in pages for issue in page], notice)
    if previous:
        return {"state": "existing-owner-follow-up", "number": previous["number"],
                "issue_state": previous["state"], "url": previous["html_url"]}
    body = f'''{notice['marker']}
What — Official upstream release {notice['version']} is outside the currently admitted range `{notice['supported_range']}`.

How — Review the [official release]({notice['url']}) and execute the existing native positive, inherited-channel negative, warm-cache and installed digest controls before changing the compatibility boundary.

Why — Avoid a permanently frozen version and keep new major releases visible to maintainers. Range membership is not version-specific test evidence. This notice does not change an SDK pin, admit the new major, publish a component or require scientific suites.

Owner context — {context}

Resolution — Record compatible qualification and the adopted range, a tracked deferral, or a reasoned rejection. Existing closed decisions are respected; the watcher does not reopen them or post repeated comments.
'''
    with TemporaryDirectory(prefix="molsyssuite-release-notice-") as directory:
        path = Path(directory) / "issue.json"
        path.write_text(json.dumps({"title": notice["title"], "body": body, "labels": ["proposal"]}))
        created = request(["api", "--method", "POST", f"repos/{owner}/issues", "--input", str(path)])
    return {"state": "created-owner-follow-up", "number": created["number"], "url": created["html_url"]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider", required=True, type=repository_name)
    parser.add_argument("--supported-range", required=True)
    parser.add_argument("--owner", required=True, type=repository_name)
    parser.add_argument("--context", required=True)
    parser.add_argument("--notify", action="store_true")
    args = parser.parse_args()
    try:
        notice = inspect_release(args.provider, gh_json(["api", f"repos/{args.provider}/releases/latest"]), args.supported_range)
        if args.notify:
            notice["delivery"] = deliver_notice(args.owner, notice, args.context)
        print(json.dumps(notice, indent=2))
        summary = os.environ.get("GITHUB_STEP_SUMMARY")
        if summary:
            with Path(summary).open("a") as output:
                output.write(f"Upstream {notice['provider']}: {notice['version']}, {notice['state']}.\n")
        return 0
    except (ValueError, OSError, KeyError, TypeError, subprocess.SubprocessError) as error:
        print(f"Upstream release watch failed: {type(error).__name__}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
