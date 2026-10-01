"""Bounded JSON acquisition shared by read-only release evidence tools."""

import json
from urllib.request import Request, urlopen


class EvidenceError(ValueError):
    """Public service evidence is malformed or exceeds its bound."""


def read_json(url: str, token: str | None = None) -> dict:
    headers = {"Accept": "application/json", "User-Agent": "molsyssuite-conda-preflight/1"}
    if token:
        headers["Authorization"] = "Bearer " + token
    with urlopen(Request(url, headers=headers), timeout=20) as response:
        payload = response.read(8 * 1024 * 1024 + 1)
    if len(payload) > 8 * 1024 * 1024:
        raise EvidenceError("preflight response exceeds 8 MiB")
    result = json.loads(payload)
    if not isinstance(result, dict):
        raise EvidenceError("preflight service returned non-object metadata")
    return result
