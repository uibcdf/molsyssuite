"""Compare immutable Git inputs with installed PEP 610 metadata, without imports.

This bounded HTTPS/Git profile does not install, contact a repository, attest
native bytes, or infer whether an installer actually used --no-deps.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote, urlsplit, urlunsplit

from packaging.requirements import Requirement
from packaging.utils import canonicalize_name
from packaging.version import Version

from devtools.scripts.conda_release_contract import ContractError


def full_commit(value: str) -> str:
    """Accept only an immutable lowercase Git SHA-1 input in this profile."""
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{40}", value):
        raise ContractError("Git source needs a full lowercase commit")
    return value


def repository_url(value: str) -> str:
    """Normalize HTTPS repository identity; refuse credentials and ambiguous URLs."""
    if not isinstance(value, str):
        raise ContractError("Git repository needs an HTTPS URL")
    url = urlsplit(value)
    if (
        url.scheme != "https"
        or not url.hostname
        or url.username is not None
        or url.password is not None
        or url.port not in {None, 443}
        or url.query
        or url.fragment
        or not re.fullmatch(r"(?:/[A-Za-z0-9_.-]+){2,}", url.path)
        or any(part in {".", ".."} for part in url.path.split("/"))
    ):
        raise ContractError("Git repository URL needs the reviewed HTTPS profile")
    path = url.path.removesuffix(".git")
    return urlunsplit(("https", url.hostname.lower(), path, "", ""))


def parse_git_requirement(value: str) -> dict:
    """Read one fixed pip Git input, either bare or unconditional PEP 508 named."""
    name = None
    if not isinstance(value, str):
        raise ContractError("Git requirement must be a string")
    if value.startswith("git+"):
        url = value
    else:
        try:
            requirement = Requirement(value)
        except ValueError as error:
            raise ContractError("invalid Git requirement") from error
        if requirement.marker or requirement.extras or not requirement.url:
            raise ContractError("Git requirement needs an unconditional source URL")
        name, url = canonicalize_name(requirement.name), requirement.url
    if not url.startswith("git+https://") or "@" not in url:
        raise ContractError("Git requirement needs a pinned HTTPS source")
    repository, commit = url[4:].rsplit("@", 1)
    return {
        "name": name,
        "repository": repository_url(repository),
        "commit": full_commit(commit),
    }


def check_version(requirement: str, version: str, *, allow_unbounded=False) -> None:
    """Enforce every declared bound; an optional profile may accept no bound."""
    parsed = Requirement(requirement)
    if (
        parsed.marker
        or parsed.url
        or parsed.extras
        or (not parsed.specifier and not allow_unbounded)
    ):
        raise ContractError("source route requires unconditional version constraints")
    if not parsed.specifier.contains(Version(version), prereleases=True):
        raise ContractError(f"installed source {version} violates {parsed}")


def check_git_install(record: dict, requirement: str, distribution) -> dict:
    """Verify requested/resolved immutable identity and installed version.

    Installer metadata is evidence of origin, not tamper-proof attestation.
    Directory/editable and archive origins cannot satisfy a Git installation.
    """
    commit = full_commit(record["commit"])
    repository = repository_url(record["url"])
    if record.get("install") != "pip-no-deps-git":
        raise ContractError("Git install needs its explicit profile")
    check_version(requirement, distribution.version, allow_unbounded=True)
    raw = distribution.read_text("direct_url.json")
    if not raw:
        raise ContractError("installed Git source has no provenance")
    data = json.loads(raw)
    if not isinstance(data, dict) or set(data) & {
        "dir_info",
        "archive_info",
        "subdirectory",
    }:
        raise ContractError("installed source is not a reviewed root Git installation")
    vcs = data.get("vcs_info")
    if (
        not isinstance(vcs, dict)
        or vcs.get("vcs") != "git"
        or vcs.get("commit_id") != commit
        or vcs.get("requested_revision", commit) != commit
        or repository_url(data.get("url")) != repository
    ):
        raise ContractError(
            "installed Git repository/requested/resolved commit differs"
        )
    return {
        "name": canonicalize_name(Requirement(requirement).name),
        "repository": repository,
        "commit": commit,
        "version": distribution.version,
        "install": record["install"],
    }


def check_directory_install(
    record: dict, requirement: str, distribution, root: Path
) -> dict:
    """Bind a normal directory install to its clean, immutable root Git clone.

    Local Git reads verify the HTTPS origin and current commit; no remote is
    contacted. Installer metadata binds the actual directory and version, not
    native-byte integrity or scientific behavior. Editable installs are excluded.
    """
    commit = full_commit(record["commit"])
    repository = repository_url(record["url"])
    if record.get("install") != "pip-no-deps-directory":
        raise ContractError("directory install needs its explicit profile")
    root = Path(root).resolve()

    def git(*arguments):
        try:
            return subprocess.check_output(
                ["git", *arguments],
                cwd=root,
                text=True,
                timeout=30,
                stderr=subprocess.PIPE,
            ).strip()
        except (OSError, subprocess.SubprocessError) as error:
            raise ContractError("directory source Git inspection failed") from error

    if (
        Path(git("rev-parse", "--show-toplevel")).resolve() != root
        or git("rev-parse", "HEAD") != commit
        or git("status", "--porcelain")
        or repository_url(git("remote", "get-url", "origin")) != repository
    ):
        raise ContractError(
            "directory source root/repository/commit/cleanliness differs"
        )
    check_version(requirement, distribution.version, allow_unbounded=True)
    raw = distribution.read_text("direct_url.json")
    if not raw:
        raise ContractError("installed source has no directory provenance")
    data = json.loads(raw)
    if not isinstance(data, dict) or set(data) & {
        "vcs_info",
        "archive_info",
        "subdirectory",
    }:
        raise ContractError("installed source is not a reviewed directory installation")
    url = urlsplit(data.get("url", ""))
    info = data.get("dir_info")
    if (
        url.scheme != "file"
        or url.netloc not in {"", "localhost"}
        or url.query
        or url.fragment
        or Path(unquote(url.path)).resolve() != root
        or not isinstance(info, dict)
        or info.get("editable", False) is not False
    ):
        raise ContractError(
            "installed source is not from the reviewed normal directory"
        )
    return {
        "name": canonicalize_name(Requirement(requirement).name),
        "repository": repository,
        "commit": commit,
        "directory": str(root),
        "version": distribution.version,
        "install": record["install"],
    }
