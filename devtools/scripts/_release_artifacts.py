"""Acquire bounded JSON receipts bound to a native GitHub artifact and attempt."""

from __future__ import annotations

import hashlib
import io
import json
import os
import stat
import subprocess
import zipfile
from pathlib import PurePosixPath
from urllib.parse import urlencode

try:
    from devtools.scripts._release_http import EvidenceError, read_json
except ModuleNotFoundError:
    from _release_http import EvidenceError, read_json


def acquire_json_artifact(
    repository: str, run: dict, name: str, token: str, *, reader=None
) -> tuple[dict[str, dict], dict]:
    """Read JSON without extraction; refuse incomplete, expired or changed evidence."""
    reader = reader or read_json
    query = urlencode({"per_page": 100, "name": name})
    document = reader(
        f"https://api.github.com/repos/{repository}/actions/runs/{run['id']}/artifacts?{query}",
        token,
    )
    artifacts = document.get("artifacts")
    if (
        not isinstance(artifacts, list)
        or any(not isinstance(item, dict) for item in artifacts)
        or document.get("total_count") != len(artifacts)
        or len(artifacts) > 100
    ):
        raise EvidenceError("native receipt artifact inventory is incomplete")
    matches = [item for item in artifacts if item.get("name") == name]
    if len(matches) != 1:
        raise EvidenceError("native receipt artifact is missing or ambiguous")
    artifact = matches[0]
    if (
        type(artifact.get("id")) is not int
        or artifact["id"] < 1
        or artifact.get("expired") is not False
        or type(artifact.get("size_in_bytes")) is not int
        or not 0 < artifact["size_in_bytes"] <= 1024 * 1024
        or artifact.get("workflow_run", {}).get("id") != run["id"]
        or artifact.get("workflow_run", {}).get("head_sha") != run["head_sha"]
    ):
        raise EvidenceError("native receipt artifact identity or bounds are invalid")
    response = subprocess.run(
        ["gh", "api", f"repos/{repository}/actions/artifacts/{artifact['id']}/zip"],
        capture_output=True,
        check=True,
        timeout=60,
        env=dict(os.environ, GH_TOKEN=token) if token else None,
    )
    payload = response.stdout
    if (
        len(payload) > 1024 * 1024
        or artifact.get("digest") != "sha256:" + hashlib.sha256(payload).hexdigest()
    ):
        raise EvidenceError("native receipt ZIP digest differs from artifact evidence")
    receipts = {}
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        members = archive.infolist()
        names = [member.filename for member in members]
        if (
            not members
            or len(members) > 100
            or len(names) != len(set(names))
            or sum(member.file_size for member in members) > 1024 * 1024
        ):
            raise EvidenceError("native receipt ZIP inventory exceeds its bounds")
        for member in members:
            path = PurePosixPath(member.filename)
            if (
                path.is_absolute()
                or str(path) != member.filename.removesuffix("/")
                or ".." in path.parts
                or "\\" in member.filename
                or stat.S_ISLNK(member.external_attr >> 16)
            ):
                raise EvidenceError("native receipt ZIP has an unsafe member")
            if member.is_dir():
                continue
            if path.suffix != ".json" or member.file_size > 65536:
                raise EvidenceError("native receipt is not a bounded JSON file")
            result = json.loads(archive.read(member))
            if not isinstance(result, dict):
                raise EvidenceError("native receipt is not a JSON object")
            receipts[member.filename] = result
    return receipts, {
        key: artifact[key]
        for key in ("id", "name", "digest", "size_in_bytes", "workflow_run")
    }
