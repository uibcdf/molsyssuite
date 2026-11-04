"""Acquire bounded public GitHub CI-selection inputs without executing member code."""

from __future__ import annotations

import hashlib
import re
import shutil
from pathlib import Path, PurePosixPath
from urllib.parse import quote, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

try:
    from devtools.scripts import ci_lane_inventory, python_ci_status
    from devtools.scripts._release_http import read_json
except ImportError:
    import ci_lane_inventory
    import python_ci_status
    from _release_http import read_json

MAX_TREE_ENTRIES = 25_000
MAX_FILE_BYTES = 1024 * 1024
MAX_SOURCE_BYTES = 8 * 1024 * 1024
MAX_FILES = 256
SHA = re.compile(r"[0-9a-f]{40}\Z")


class SourceUnavailable(ValueError):
    """A stable diagnostic category, never a raw service response or exception."""


def relative_path(value: str) -> PurePosixPath:
    """Require a bounded canonical path, without traversal or Git administration."""
    if (
        not isinstance(value, str)
        or not value
        or len(value) > 1024
        or any(ord(char) < 32 or ord(char) == 127 for char in value)
        or "\\" in value
        or ":" in value
    ):
        raise SourceUnavailable("unsupported_source_path")
    path = PurePosixPath(value)
    if (
        path.is_absolute()
        or path.as_posix() != value
        or path.parts == ()
        or len(path.parts) > 40
        or any(part in {".", "..", ".git"} for part in path.parts)
    ):
        raise SourceUnavailable("unsupported_source_path")
    return path


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def read_public_bytes(url: str) -> bytes:
    """Anonymous bounded raw-file GET; never follow redirects or use env tokens."""
    parsed = urlsplit(url)
    if (
        parsed.scheme != "https"
        or parsed.netloc != "raw.githubusercontent.com"
        or not parsed.path.startswith("/uibcdf/")
        or parsed.query
        or parsed.fragment
    ):
        raise SourceUnavailable("unsupported_public_url")
    request = Request(url, headers={"User-Agent": "molsyssuite-ci-observer/1"})
    with build_opener(_NoRedirect()).open(request, timeout=20) as response:
        payload = response.read(MAX_FILE_BYTES + 1)
    if len(payload) > MAX_FILE_BYTES:
        raise SourceUnavailable("source_file_limit")
    return payload


def workflow_budget(document: dict) -> None:
    """Bound alias graphs, static products and scenarios before the offline reader.

    These are observer resource limits, never component workflow requirements.
    The existing reader remains the owner of lane and selection interpretation.
    """
    pending, nodes = [(document, 0)], 0
    while pending:
        value, depth = pending.pop()
        nodes += 1
        if nodes > 20_000 or depth > 40:
            raise SourceUnavailable("workflow_structure_limit")
        children = (
            list(value.values())
            if isinstance(value, dict)
            else value
            if isinstance(value, list)
            else []
        )
        if len(children) + len(pending) > 20_000:
            raise SourceUnavailable("workflow_structure_limit")
        pending.extend((child, depth + 1) for child in children)
    jobs, triggers = document.get("jobs", {}), document.get("on", {})
    if not isinstance(jobs, dict) or len(jobs) > 64:
        raise SourceUnavailable("workflow_job_limit")
    if isinstance(triggers, dict):
        dispatch = triggers.get("workflow_dispatch", {})
        inputs = dispatch.get("inputs", {}) if isinstance(dispatch, dict) else {}
        schedules = triggers.get("schedule", [])
        if (
            not isinstance(inputs, dict)
            or not isinstance(schedules, list)
            or len(triggers) > 16
            or len(inputs) > 16
            or len(schedules) > 16
        ):
            raise SourceUnavailable("workflow_scenario_limit")
    cells = 0
    for job in jobs.values():
        if not isinstance(job, dict):
            continue
        steps, needs = job.get("steps", []), job.get("needs", [])
        if not isinstance(steps, list) or len(steps) > 256:
            raise SourceUnavailable("workflow_step_limit")
        if isinstance(needs, list) and len(needs) > 16:
            raise SourceUnavailable("workflow_dependency_limit")
        if any(
            isinstance(step, dict) and len(str(step.get("run", ""))) > 32768
            for step in steps
        ):
            raise SourceUnavailable("workflow_script_limit")
        strategy = job.get("strategy", {})
        matrix = strategy.get("matrix") if isinstance(strategy, dict) else None
        size = 1
        if isinstance(matrix, dict):
            for key, axis in matrix.items():
                if isinstance(axis, list):
                    if key in {"include", "exclude"}:
                        if len(axis) > 256:
                            raise SourceUnavailable("workflow_matrix_limit")
                    else:
                        size *= len(axis)
                        if size > 256:
                            raise SourceUnavailable("workflow_matrix_limit")
            includes = matrix.get("include", [])
            if isinstance(includes, list):
                size += len(includes)
            if size > 256:
                raise SourceUnavailable("workflow_matrix_limit")
        cells += size
        if cells > 2048:
            raise SourceUnavailable("workflow_matrix_limit")


def collect_public_profile(
    profile: dict,
    destination: Path,
    *,
    json_reader=read_json,
    bytes_reader=read_public_bytes,
) -> dict:
    """Build a fresh source-only projection; remove only owned output on failure.

    Read public default-branch metadata, an immutable commit/tree, selection
    inputs, root pytest configs and all declared-scope hooks. A complete bounded
    tree proves hook-name discovery; unrelated code/data are never downloaded.
    No credentials, archive extraction, Git checkout, imports or member commands.
    """
    repository = profile["repository"]
    if not re.fullmatch(r"uibcdf/[A-Za-z0-9_.-]+", repository) or repository.split("/")[
        1
    ] in {".", ".."}:
        raise ValueError("observer needs a registered uibcdf repository")
    base = "https://api.github.com/repos/" + repository
    meta = json_reader(base)  # Deliberately anonymous, even with tokens in env.
    if (
        meta.get("private") is not False
        or meta.get("visibility") != "public"
        or str(meta.get("full_name", "")).casefold() != repository.casefold()
    ):
        raise SourceUnavailable("public_repository_unavailable")
    branch = meta.get("default_branch")
    if not isinstance(branch, str) or not branch or len(branch) > 256:
        raise SourceUnavailable("invalid_public_metadata")
    commit = json_reader(base + "/commits/" + quote(branch, safe=""))
    head = commit.get("sha", "")
    details = commit.get("commit", {})
    tree_ref = details.get("tree", {}) if isinstance(details, dict) else {}
    tree_sha = tree_ref.get("sha", "") if isinstance(tree_ref, dict) else ""
    if (
        not isinstance(head, str)
        or not SHA.fullmatch(head)
        or not isinstance(tree_sha, str)
        or not SHA.fullmatch(tree_sha)
    ):
        raise SourceUnavailable("invalid_public_metadata")
    tree = json_reader(base + "/git/trees/" + tree_sha + "?recursive=1")
    entries = tree.get("tree")
    if (
        tree.get("sha") != tree_sha
        or tree.get("truncated") is not False
        or not isinstance(entries, list)
    ):
        raise SourceUnavailable("incomplete_public_tree")
    if len(entries) > MAX_TREE_ENTRIES:
        raise SourceUnavailable("source_tree_limit")
    indexed = {}
    for entry in entries:
        if not isinstance(entry, dict):
            raise SourceUnavailable("invalid_public_tree")
        path = relative_path(entry.get("path"))
        if (
            str(path) in indexed
            or not isinstance(entry.get("sha"), str)
            or not SHA.fullmatch(entry["sha"])
        ):
            raise SourceUnavailable("invalid_public_tree")
        if (entry.get("type"), entry.get("mode")) not in {
            ("tree", "040000"),
            ("blob", "100644"),
            ("blob", "100755"),
            ("blob", "120000"),
            ("commit", "160000"),
        }:
            raise SourceUnavailable("invalid_public_tree")
        indexed[str(path)] = entry
    roots = [relative_path(value) for value in profile.get("collection-roots", [])]
    selected = set(profile["inputs"]) | {
        p for p in python_ci_status.ROOT_PYTEST_CONFIGS if p in indexed
    }
    for root in roots:
        # os.walk counts descendants once and directory visits once more.
        descendants = [
            (path, entry)
            for path, entry in indexed.items()
            if str(root) + "/" == path[: len(str(root)) + 1]
        ]
        count = 1 + sum(2 if e["type"] == "tree" else 1 for _, e in descendants)
        if count > python_ci_status.MAX_COLLECTION_ENTRIES:
            raise SourceUnavailable("collection_inspection_limit")
        for path, entry in descendants:
            if entry["mode"] in {"120000", "160000"}:
                raise SourceUnavailable("unsupported_collection_link")
            if PurePosixPath(path).name == "conftest.py":
                selected.add(path)
        for parent in (root, *root.parents):
            hook = str(parent / "conftest.py")
            if hook in indexed:
                selected.add(hook)
    if len(selected) > MAX_FILES:
        raise SourceUnavailable("source_file_count_limit")

    def regular_path(relative, *, directory=False):
        path = relative_path(relative)
        for parent in path.parents:
            if (
                str(parent) != "."
                and indexed.get(str(parent), {}).get("mode") != "040000"
            ):
                raise SourceUnavailable("unsupported_source_ancestor")
        mode = indexed.get(relative, {}).get("mode")
        if mode not in ({"040000"} if directory else {"100644", "100755"}):
            raise SourceUnavailable("unsupported_source_entry")
        return path

    # Exclusive creation prevents deleting or replacing any caller-owned tree.
    destination.mkdir()
    complete = False
    try:
        total, files = 0, []
        for relative in sorted(selected):
            if relative not in indexed:
                continue  # A deleted bound input is observed drift, not HTTP failure.
            path = regular_path(relative)
            entry = indexed[relative]
            size = entry.get("size")
            if type(size) is not int or not 0 <= size <= MAX_FILE_BYTES:
                raise SourceUnavailable("source_file_limit")
            if total + size > MAX_SOURCE_BYTES:
                raise SourceUnavailable("source_bytes_limit")
            payload = bytes_reader(
                f"https://raw.githubusercontent.com/{repository}/{head}/{quote(relative, safe='/')}"
            )
            if not isinstance(payload, bytes) or len(payload) != size:
                raise SourceUnavailable("source_blob_mismatch")
            blob = hashlib.sha1(
                b"blob " + str(size).encode() + b"\0" + payload, usedforsecurity=False
            ).hexdigest()
            if blob != entry["sha"]:
                raise SourceUnavailable("source_blob_mismatch")
            payload.decode("utf-8")
            target = destination.joinpath(*path.parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(payload)
            files.append(
                {
                    "path": relative,
                    "bytes": size,
                    "git_blob": blob,
                    "sha256": hashlib.sha256(payload).hexdigest(),
                }
            )
            total += size
        for root in roots:
            if str(root) in indexed and indexed[str(root)]["type"] == "tree":
                regular_path(str(root), directory=True)
                destination.joinpath(*root.parts).mkdir(parents=True, exist_ok=True)
        for lane in profile["lanes"]:
            workflow = destination / ".github/workflows" / lane["workflow"]
            if workflow.is_file():
                try:
                    workflow_budget(ci_lane_inventory.load_workflow(workflow))
                except (
                    TypeError,
                    ValueError,
                    RecursionError,
                    ci_lane_inventory.yaml.YAMLError,
                ) as error:
                    if isinstance(error, SourceUnavailable):
                        raise
                    raise SourceUnavailable("unsupported_workflow_source") from None
        complete = True
        return {
            "repository": repository,
            "state": "observed",
            "default_branch": branch,
            "source_commit": head,
            "tree": tree_sha,
            "tree_entries": len(entries),
            "files": files,
            "bytes": total,
        }
    finally:
        if not complete:
            shutil.rmtree(destination)
