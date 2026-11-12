"""Acquire complete GitHub issue/label inventories or refuse absence claims.

Pagination belongs to native gh, not a search/list result cap. Resource bounds
refuse the inventory rather than returning a usable partial prefix. This is an
observed traversal, not a transactionally frozen or search-index snapshot.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from dataclasses import dataclass

MAX_PAGES = 100
MAX_RESPONSE_BYTES = 16 * 1024 * 1024


class InventoryUnavailable(ValueError):
    """Acquisition/completeness is unknown; no absence decision is permitted."""


@dataclass(frozen=True)
class GitHubInventory:
    repository: str
    resource: str
    records: list[dict]
    page_count: int
    pull_requests_excluded: int
    payload_sha256: str

    def summary(self) -> dict:
        """Retain scope/completeness without publishing issue bodies."""
        return {
            "schema": "molsyssuite.github-inventory@1",
            "state": "complete",
            "repository": self.repository,
            "resource": self.resource,
            "scope": "all states; issues only"
            if self.resource == "issues"
            else "all labels",
            "page_count": self.page_count,
            "record_count": len(self.records),
            "pull_requests_excluded": self.pull_requests_excluded,
            "payload_sha256": self.payload_sha256,
        }


def _gh_json(arguments: list[str]) -> object:
    result = subprocess.run(
        ["gh", *arguments], capture_output=True, text=True, timeout=60, check=True
    )
    if len(result.stdout.encode()) > MAX_RESPONSE_BYTES:
        raise InventoryUnavailable("GitHub inventory exceeds the response bound")
    return json.loads(result.stdout)


def acquire_inventory(
    repository: str, resource: str, *, request=None
) -> GitHubInventory:
    """Read issues (all states, excluding PRs) or labels through native pagination.

    request, when supplied, accepts gh argument tokens and returns decoded JSON
    after successful acquisition. A failed transport must raise. A valid empty
    response is at least one empty page, not zero observed pages. No write,
    search-index inference, retry or partial success is performed here.
    """
    if (
        not isinstance(repository, str)
        or not re.fullmatch(r"[A-Za-z0-9_-]+/[A-Za-z0-9_.-]+", repository)
        or repository.split("/")[-1] in {".", ".."}
        or not isinstance(resource, str)
        or resource not in {"issues", "labels"}
    ):
        raise InventoryUnavailable(
            "inventory needs an explicit repository/resource scope"
        )
    endpoint = f"repos/{repository}/{resource}?"
    if resource == "issues":
        endpoint += "state=all&"
    endpoint += "per_page=100"
    try:
        pages = (_gh_json if request is None else request)(
            ["api", "--hostname", "github.com", "--paginate", "--slurp", endpoint]
        )
    except (
        OSError,
        subprocess.SubprocessError,
        ValueError,
        TypeError,
        RuntimeError,
    ) as error:
        raise InventoryUnavailable("GitHub inventory acquisition failed") from error
    if (
        not isinstance(pages, list)
        or not pages
        or len(pages) > MAX_PAGES
        or any(not isinstance(page, list) or len(page) > 100 for page in pages)
    ):
        raise InventoryUnavailable(
            "GitHub inventory pages are missing, malformed or over bound"
        )
    try:
        payload = json.dumps(pages, sort_keys=True, separators=(",", ":")).encode()
    except (TypeError, ValueError) as error:
        raise InventoryUnavailable("GitHub inventory payload is malformed") from error
    if len(payload) > MAX_RESPONSE_BYTES:
        raise InventoryUnavailable("GitHub inventory exceeds the response bound")
    records, seen, excluded = [], set(), 0
    for page in pages:
        for item in page:
            if not isinstance(item, dict):
                raise InventoryUnavailable("GitHub inventory record is malformed")
            item = dict(item)
            if resource == "issues":
                identity, state = item.get("number"), item.get("state")
                if (
                    type(identity) is not int
                    or identity <= 0
                    or not isinstance(state, str)
                    or state.casefold() not in {"open", "closed"}
                    or (
                        item.get("body") is not None
                        and not isinstance(item["body"], str)
                    )
                ):
                    raise InventoryUnavailable(
                        "GitHub issue identity/state/body is malformed"
                    )
                item["state"] = state.casefold()
            else:
                name = item.get("name")
                if not isinstance(name, str) or not name:
                    raise InventoryUnavailable("GitHub label identity is malformed")
                identity = name.casefold()
            if identity in seen:
                raise InventoryUnavailable(
                    "GitHub inventory repeats an identity across pages"
                )
            seen.add(identity)
            if resource == "issues" and "pull_request" in item:
                excluded += 1
            else:
                records.append(item)
    return GitHubInventory(
        repository,
        resource,
        records,
        len(pages),
        excluded,
        hashlib.sha256(payload).hexdigest(),
    )
