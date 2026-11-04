"""Publish source-only informational CI observations; never a component CI gate."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import tempfile
import tomllib
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from time import monotonic
from urllib.error import HTTPError, URLError

try:
    from devtools.scripts import public_ci_sources, python_ci_status
    from devtools.scripts._release_http import EvidenceError
except ImportError:
    import public_ci_sources
    import python_ci_status
    from _release_http import EvidenceError

ROOT = Path(__file__).resolve().parents[2]
MAX_OBSERVATION_SECONDS = 600


def observe(
    data: dict,
    profiles: dict,
    *,
    scratch_parent=None,
    json_reader=public_ci_sources.read_json,
    bytes_reader=public_ci_sources.read_public_bytes,
) -> dict:
    """Inspect public source projections in a fresh managed workspace.

    A transport/inspection limitation clears that member's whole projection;
    the existing reader then reports unknown. Drift is diagnostic and never
    updates its profile, CI adoption or test-debt state. Programmer/catalogue
    errors remain errors of this central observer, not member test failures.
    """
    acquisition = []
    started = monotonic()

    def bounded(reader, url):
        if monotonic() - started > MAX_OBSERVATION_SECONDS:
            raise public_ci_sources.SourceUnavailable("observation_time_limit")
        return reader(url)

    with tempfile.TemporaryDirectory(
        prefix="molsyssuite-ci-observer-", dir=scratch_parent
    ) as temporary:
        workspace = Path(temporary)
        # Validate all trusted local declarations before making any remote request.
        python_ci_status.inspect_pilot(data, workspace, profiles)
        members = {m["repository"]: m for m in data["members"]}
        for profile in profiles["profiles"]:
            repository = profile["repository"]
            if not re.fullmatch(r"uibcdf/[A-Za-z0-9_.-]+", repository):
                raise ValueError("observer needs registered uibcdf repositories")
            name = members[repository]["name"]
            if name != repository.split("/")[-1]:
                raise ValueError("observer member folder must match repository name")
            for path in profile["inputs"]:
                public_ci_sources.relative_path(path)
            for lane in profile["lanes"]:
                path = public_ci_sources.relative_path(
                    ".github/workflows/" + lane["workflow"]
                )
                if len(path.parts) != 3 or path.suffix not in {".yml", ".yaml"}:
                    raise ValueError(
                        "observer needs active top-level workflow bindings"
                    )
        for profile in profiles["profiles"]:
            repository = profile["repository"]
            try:
                result = public_ci_sources.collect_public_profile(
                    profile,
                    workspace / members[repository]["name"],
                    json_reader=lambda url: bounded(json_reader, url),
                    bytes_reader=lambda url: bounded(bytes_reader, url),
                )
            except HTTPError as error:
                status = error.code if type(error.code) is int else 0
                error.close()
                result = {
                    "repository": repository,
                    "state": "unavailable",
                    "reason": f"http_{status}",
                }
            except public_ci_sources.SourceUnavailable as error:
                reason = str(error)
                result = {
                    "repository": repository,
                    "state": "unavailable",
                    "reason": reason
                    if re.fullmatch(r"[a-z_]{1,64}", reason)
                    else "source_unavailable",
                }
            except (
                URLError,
                TimeoutError,
                ConnectionError,
                EvidenceError,
                json.JSONDecodeError,
                UnicodeError,
            ):
                result = {
                    "repository": repository,
                    "state": "unavailable",
                    "reason": "public_source_unavailable",
                }
            acquisition.append(result)
        report = python_ci_status.inspect_pilot(data, workspace, profiles)
    return {
        "schema": "molsyssuite.ci-profile-observation@1",
        "observed_at_utc": datetime.now(UTC).isoformat(),
        "mode": "informational",
        "coordination_issue": "uibcdf/molsyssuite#39",
        "acquisition": acquisition,
        "pilot_report": report,
        "limits": [
            "public default-branch source only; no credentials, private-repository access or member execution",
            "bounded selection inputs/root configs/hooks, not complete runtime or scientific-source qualification",
            "unavailable/unsupported/incomplete source is unknown, never passing execution evidence",
            "no automatic profile refresh, adoption, backlog clearance, required gate or issue publication",
        ],
        "temporary_sources": "managed projection workspace removed before returning",
    }


def render_summary(observation: dict) -> str:
    """Render bounded known identities/counts; never raw source/error payloads."""
    sources = {row["repository"]: row for row in observation["acquisition"]}
    lines = [
        "# Informational public CI profile observation",
        "",
        "Source/configuration observations only; **not executed tests, adoption or debt clearance**.",
        "",
        "| Member | Observed source | Acquisition | Bound review inputs | Lane states |",
        "| --- | --- | --- | --- | --- |",
    ]
    for member in observation["pilot_report"]["members"]:
        source = sources[member["repository"]]
        counts = Counter(lane["state"] for lane in member["lanes"])
        states = ", ".join(f"{key}: {value}" for key, value in sorted(counts.items()))
        status = (
            "unchanged"
            if member["profile_inputs_current"]
            else "review required / unknown"
        )
        acquisition = source["state"] + (
            ": " + source["reason"] if "reason" in source else ""
        )
        lines.append(
            f"| {member['repository']} | {source.get('source_commit', 'unavailable')[:12]} | {acquisition} | {status} | {states} |"
        )
    lines += [
        "",
        "Unavailable inputs and drift are diagnostic findings; they do not block component CI.",
        "Private OpenCASTp and members without public Python profiles are outside this catalogue.",
        "Use observation.json for immutable source/blob/input hashes and complete bounded-reader details.",
        "",
    ]
    return "\n".join(lines)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=ROOT / "suite.toml")
    parser.add_argument(
        "--profiles", type=Path, default=python_ci_status.PILOT_PROFILES
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="new output directory; existing paths are refused",
    )
    parser.add_argument(
        "--scratch-parent",
        type=Path,
        help="existing parent for managed source projections",
    )
    args = parser.parse_args(argv)
    if args.output.exists() or args.output.is_symlink():
        parser.error("output must be a new directory")
    try:
        registry_bytes = args.registry.read_bytes()
        profile_bytes = args.profiles.read_bytes()
        data, profiles = (
            tomllib.loads(registry_bytes.decode()),
            tomllib.loads(profile_bytes.decode()),
        )
        result = observe(data, profiles, scratch_parent=args.scratch_parent)
        result["central_inputs"] = {
            "central_commit": os.environ.get("GITHUB_SHA")
            if re.fullmatch(r"[0-9a-f]{40}", os.environ.get("GITHUB_SHA", ""))
            else None,
            "registry_sha256": hashlib.sha256(registry_bytes).hexdigest(),
            "profiles_sha256": hashlib.sha256(profile_bytes).hexdigest(),
            "tool_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "acquisition_tool_sha256": hashlib.sha256(
                Path(public_ci_sources.__file__).read_bytes()
            ).hexdigest(),
            "reader_sha256": hashlib.sha256(
                Path(python_ci_status.__file__).read_bytes()
            ).hexdigest(),
            "inventory_reader_sha256": hashlib.sha256(
                Path(public_ci_sources.ci_lane_inventory.__file__).read_bytes()
            ).hexdigest(),
            "json_transport_sha256": hashlib.sha256(
                Path(public_ci_sources.read_json.__code__.co_filename).read_bytes()
            ).hexdigest(),
        }
        args.output.mkdir(parents=True)
        (args.output / "observation.json").write_text(
            json.dumps(result, indent=2) + "\n", encoding="utf-8"
        )
        (args.output / "summary.md").write_text(
            render_summary(result), encoding="utf-8"
        )
    except (ValueError, OSError) as error:
        parser.error(str(error))
    print(
        f"Informational observation written for {len(result['acquisition'])} public profiles; no member tests executed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
