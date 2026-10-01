"""Verify one exact public Conda file without changing registry state."""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

OWNER = "uibcdf"
MAX_RESPONSE_BYTES = 16 * 1024 * 1024
VERSION = re.compile(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\Z")
NAME = re.compile(r"[a-z0-9][a-z0-9-]*\Z")
SUBDIR = re.compile(r"[a-z0-9][a-z0-9-]*\Z")
FILENAME = re.compile(r"[A-Za-z0-9_.+\-]+\.(?:conda|tar\.bz2)\Z")
SHA256 = re.compile(r"[0-9a-f]{64}\Z")


class VerificationPending(Exception):
    """The public label or index has not exposed the expected file yet."""


class VerificationError(Exception):
    """The public record contradicts the expected immutable coordinate."""


def validate_coordinate(
    package: str, version: str, subdir: str, filename: str, sha256: str
) -> None:
    """Reject unsafe or inconsistent coordinates before making network requests."""
    if not NAME.fullmatch(package) or not VERSION.fullmatch(version):
        raise VerificationError("package or version is not canonical")
    if not SUBDIR.fullmatch(subdir) or not FILENAME.fullmatch(filename):
        raise VerificationError("subdir or filename is not a single Conda coordinate")
    if not filename.startswith(f"{package}-{version}-") or not SHA256.fullmatch(sha256):
        raise VerificationError(
            "filename or SHA-256 does not match the expected coordinate"
        )


def fetch_json(url: str) -> dict:
    """Fetch a bounded, anonymous public JSON document."""
    request = Request(url, headers={"User-Agent": "uibcdf-conda-public-verifier/1"})
    with urlopen(request, timeout=20) as response:
        payload = response.read(MAX_RESPONSE_BYTES + 1)
    if len(payload) > MAX_RESPONSE_BYTES:
        raise VerificationError("public registry response exceeds the size limit")
    document = json.loads(payload)
    if not isinstance(document, dict):
        raise VerificationError("public registry response is not a JSON object")
    return document


def verify_snapshot(
    release: dict,
    repodata: dict,
    package: str,
    version: str,
    subdir: str,
    filename: str,
    sha256: str,
    owner: str = OWNER,
) -> str:
    """Check both Anaconda's public label and the solver-visible index."""
    basename = f"{subdir}/{filename}"
    distributions = release.get("distributions")
    if not isinstance(distributions, list):
        raise VerificationError("release metadata has no distributions list")
    matches = [
        entry
        for entry in distributions
        if isinstance(entry, dict) and entry.get("basename") == basename
    ]
    if not matches:
        raise VerificationPending(f"{basename} is not in the public release metadata")
    if len(matches) != 1:
        raise VerificationError(f"duplicate public release records for {basename}")
    distribution = matches[0]
    if distribution.get("sha256") != sha256:
        raise VerificationError(f"public release SHA-256 differs for {basename}")
    if (
        not isinstance(distribution.get("labels"), list)
        or "main" not in distribution["labels"]
    ):
        raise VerificationPending(f"{basename} does not yet have the main label")
    attrs = distribution.get("attrs")
    if not isinstance(attrs, dict) or attrs.get("subdir") != subdir:
        raise VerificationError(f"public release subdir differs for {basename}")

    info = repodata.get("info")
    if not isinstance(info, dict) or info.get("subdir") != subdir:
        raise VerificationError(f"public repodata is not for {subdir}")
    section = "packages.conda" if filename.endswith(".conda") else "packages"
    records = repodata.get(section)
    if records is None:
        raise VerificationPending(f"public repodata has no {section} mapping yet")
    if not isinstance(records, dict):
        raise VerificationError(f"public repodata has an invalid {section} mapping")
    record = records.get(filename)
    if record is None:
        raise VerificationPending(f"{basename} is not yet solver-visible")
    if not isinstance(record, dict) or record.get("sha256") != sha256:
        raise VerificationError(f"solver-visible SHA-256 differs for {basename}")
    if record.get("name") != package or record.get("version") != version:
        raise VerificationError(
            f"solver-visible package identity differs for {basename}"
        )
    build = filename[len(f"{package}-{version}-"):]
    build = build[:-6] if filename.endswith(".conda") else build[:-8]
    if record.get("build") != build:
        raise VerificationError(f"solver-visible build differs for {basename}")
    if record.get("subdir", subdir) != subdir:
        raise VerificationError(f"solver-visible subdir differs for {basename}")
    try:
        number = int(build.rsplit("_", 1)[1])
    except (IndexError, ValueError) as error:
        raise VerificationError("filename has no canonical build number") from error
    if type(record.get("build_number")) is not int or record["build_number"] != number:
        raise VerificationError(f"solver-visible build number differs for {basename}")
    return f"https://conda.anaconda.org/{owner}/{basename}"


def verify_public(
    package: str,
    version: str,
    subdir: str,
    filename: str,
    sha256: str,
    attempts: int = 6,
    interval: float = 15,
    owner: str = OWNER,
) -> str:
    """Retry bounded index propagation; never mutate or download a package."""
    validate_coordinate(package, version, subdir, filename, sha256)
    if not NAME.fullmatch(owner):
        raise VerificationError("owner is not canonical")
    if not 1 <= attempts <= 12 or not 0 <= interval <= 30:
        raise VerificationError("attempts must be 1-12 and interval 0-30 seconds")
    release_url = (
        f"https://api.anaconda.org/release/{owner}/{quote(package)}/{quote(version)}"
    )
    index_url = f"https://conda.anaconda.org/{owner}/{quote(subdir)}/repodata.json"
    for attempt in range(1, attempts + 1):
        try:
            release = fetch_json(release_url)
            repodata = fetch_json(index_url)
            return verify_snapshot(
                release, repodata, package, version, subdir, filename, sha256, owner
            )
        except HTTPError as error:
            if error.code not in (404, 429) and error.code < 500:
                raise VerificationError(
                    f"public registry rejected the query: HTTP {error.code}"
                ) from error
            pending = f"public registry returned HTTP {error.code}"
        except URLError as error:
            pending = f"public registry request failed: {error.reason}"
        except VerificationPending as error:
            pending = str(error)
        if attempt == attempts:
            raise VerificationError(
                f"not verified after {attempts} attempts: {pending}"
            )
        time.sleep(interval)
    raise AssertionError("unreachable retry state")


def main(argv: list[str] | None = None) -> int:
    """Verify an exact file or complete inventory and retain bounded evidence."""
    from datetime import datetime, timezone
    from pathlib import Path

    parser = argparse.ArgumentParser(description=__doc__)
    for field in ("package", "version", "subdir", "filename", "sha256"):
        parser.add_argument("--" + field)
    parser.add_argument("--owner", default=OWNER)
    parser.add_argument("--inventory", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--attempts", type=int, default=6)
    parser.add_argument("--interval", type=float, default=15)
    args = parser.parse_args(argv)
    report = {"schema": "molsyssuite.public-conda@1", "state": "unverified",
              "checked_at": datetime.now(timezone.utc).isoformat(), "files": []}
    try:
        names = ("package", "version", "subdir", "filename", "sha256")
        if args.inventory:
            if any(getattr(args, field) is not None for field in names):
                raise VerificationError("inventory and single-file inputs are exclusive")
            if args.inventory.stat().st_size > 65536:
                raise VerificationError("inventory exceeds 64 KiB")
            files = json.loads(args.inventory.read_text(encoding="utf-8"))
        else:
            files = [{field: getattr(args, field) for field in names}]
        if not isinstance(files, list) or not 1 <= len(files) <= 64:
            raise VerificationError("inventory must contain 1-64 exact coordinates")
        seen = set()
        for coordinate in files:
            if not isinstance(coordinate, dict) or set(coordinate) != set(names):
                raise VerificationError("inventory coordinate fields differ from the contract")
            if any(not isinstance(coordinate[field], str) for field in names):
                raise VerificationError("coordinate fields must be strings")
            validate_coordinate(**coordinate)
            identity = (coordinate["subdir"], coordinate["filename"])
            if identity in seen:
                raise VerificationError("inventory contains a duplicate coordinate")
            seen.add(identity)
        for coordinate in files:
            url = verify_public(**coordinate, owner=args.owner,
                                attempts=args.attempts, interval=args.interval)
            report["files"].append({**coordinate, "owner": args.owner, "url": url,
                                   "main_label": "verified", "solver_index": "verified"})
            print(url)
        report["state"] = "verified"
        outcome = 0
    except (VerificationError, ValueError, OSError) as error:
        report["error"] = str(error)[:1000]
        print(f"public Conda verification failed: {report['error']}", file=sys.stderr)
        outcome = 1
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return outcome


if __name__ == "__main__":
    raise SystemExit(main())
