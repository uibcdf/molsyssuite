"""Verify complete successful native matrix evidence without executing its tests."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import zipfile
from datetime import datetime, timezone
from pathlib import Path

try:
    from devtools.scripts._release_artifacts import acquire_json_artifact
    from devtools.scripts._release_http import read_json
except ModuleNotFoundError:
    from _release_artifacts import acquire_json_artifact
    from _release_http import read_json


class MatrixError(ValueError):
    """Native evidence does not prove the declared installed matrix."""


def acquire_source_binding(repository: str, run: dict, token: str) -> dict:
    """Read one bounded, attempt-qualified binding published by the native run."""
    name = f"installed-source-binding-{run['id']}-{run['run_attempt']}"
    try:
        receipts, _ = acquire_json_artifact(
            repository, run, name, token, reader=read_json
        )
    except ValueError as error:
        raise MatrixError(str(error)) from error
    if set(receipts) != {"installed-source-binding.json"}:
        raise MatrixError("source binding archive has unexpected members")
    return receipts["installed-source-binding.json"]


def verify_job(job: dict, run: dict, required_steps: list[str]) -> None:
    """Verify executed named steps and the run/source/attempt of one native job."""
    if (
        job.get("run_id") != run["id"]
        or job.get("run_attempt") != run["run_attempt"]
        or job.get("head_sha") != run["head_sha"]
    ):
        raise MatrixError("native jobs mix run/source/attempt identities")
    if job.get("status") != "completed" or job.get("conclusion") != "success":
        raise MatrixError("a required job failed, skipped or did not finish")
    steps = job.get("steps")
    if required_steps and not isinstance(steps, list):
        raise MatrixError("required step evidence is missing")
    for name in required_steps:
        matches = [
            step
            for step in steps
            if isinstance(step, dict) and step.get("name") == name
        ]
        if (
            len(matches) != 1
            or matches[0].get("status") != "completed"
            or matches[0].get("conclusion") != "success"
        ):
            raise MatrixError("required evidence step is missing, skipped or failed")


def acquire_snapshot(
    repository: str, run_id: int, token: str
) -> tuple[dict, list[dict], str]:
    """Acquire a bounded complete job inventory for one exact native attempt."""
    if (
        not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository)
        or type(run_id) is not int
        or run_id < 1
    ):
        raise MatrixError("native repository/run identity is not canonical")
    base = f"https://api.github.com/repos/{repository}/actions/runs/{run_id}"
    run = read_json(base, token)
    attempt = run.get("run_attempt")
    if type(attempt) is not int or attempt < 1:
        raise MatrixError("native attempt identity is missing")
    document = read_json(f"{base}/attempts/{attempt}/jobs?per_page=100", token)
    jobs = document.get("jobs")
    if (
        not isinstance(jobs, list)
        or len(jobs) > 100
        or document.get("total_count") != len(jobs)
    ):
        raise MatrixError("native job inventory is incomplete or exceeds its bound")
    return run, jobs, base


def check_snapshot_stable(base: str, run: dict, token: str) -> None:
    """A rerun during acquisition invalidates both matrix and selected-job receipts."""
    latest = read_json(base, token)
    if any(
        latest.get(field) != run.get(field)
        for field in (
            "id",
            "head_sha",
            "run_attempt",
            "status",
            "conclusion",
            "path",
            "display_title",
        )
    ):
        raise MatrixError("native source facts changed during acquisition")


def verify_native_gate(
    repository: str,
    run_id: int,
    candidate: str,
    workflow: str,
    requirements: dict[str, list[str]],
    token: str,
) -> dict:
    """Verify declared source-CI jobs; unrelated recovery/governance jobs may skip."""
    if (
        not re.fullmatch(r"[0-9a-f]{40}", candidate)
        or not requirements
        or len(requirements) > 100
    ):
        raise MatrixError(
            "native gate needs an immutable source and explicit job requirements"
        )
    if any(
        not isinstance(name, str)
        or not name
        or not isinstance(steps, list)
        or not steps
        or len(steps) != len(set(steps))
        or any(not isinstance(step, str) or not step for step in steps)
        for name, steps in requirements.items()
    ):
        raise MatrixError("native gate job/step requirements are malformed")
    run, jobs, base = acquire_snapshot(repository, run_id, token)
    if (
        run.get("id") != run_id
        or run.get("head_sha") != candidate
        or run.get("path") != workflow
        or run.get("status") != "completed"
        or run.get("conclusion") != "success"
    ):
        raise MatrixError(
            "native gate differs from the successful exact source/workflow"
        )
    measured = []
    for name, required_steps in requirements.items():
        matches = [
            job for job in jobs if isinstance(job, dict) and job.get("name") == name
        ]
        if len(matches) != 1:
            raise MatrixError("native gate omits or duplicates a required job")
        verify_job(matches[0], run, required_steps)
        measured.append(
            {
                "name": name,
                "job_id": matches[0].get("id"),
                "required_steps": required_steps,
            }
        )
    check_snapshot_stable(base, run, token)
    return {
        "schema": "molsyssuite.native-gate@1",
        "state": "verified",
        "run_id": run_id,
        "run_attempt": run["run_attempt"],
        "candidate_sha": candidate,
        "workflow": workflow,
        "jobs": measured,
    }


def expected_jobs(profile: dict) -> dict[str, dict]:
    if not isinstance(profile, dict):
        raise MatrixError("matrix descriptor must be a JSON object")
    for field in ("platforms", "python_versions", "required_steps"):
        values = profile.get(field)
        if (
            not isinstance(values, list)
            or not values
            or any(not isinstance(v, str) or not v for v in values)
            or len(set(values)) != len(values)
        ):
            raise MatrixError(f"matrix needs unique nonempty {field}")
    prepare = profile.get("prepare_job")
    if not isinstance(prepare, str) or not prepare:
        raise MatrixError("matrix needs its preparation job identity")
    result = {prepare: {"kind": "prepare"}}
    template = profile.get("job_template", "{platform} · Python {python}")
    if (
        not isinstance(template, str)
        or "{platform}" not in template
        or "{python}" not in template
        or "{" in template.replace("{platform}", "").replace("{python}", "")
    ):
        raise MatrixError("job template must name only platform and Python coordinates")
    for platform in profile["platforms"]:
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", platform):
            raise MatrixError("platform identity is not canonical")
        for python in profile["python_versions"]:
            if not re.fullmatch(r"[0-9]+\.[0-9]+", python):
                raise MatrixError("Python identity is not canonical")
            name = template.replace("{platform}", platform).replace("{python}", python)
            if name in result:
                raise MatrixError("matrix job identities collide")
            result[name] = {"kind": "installed", "platform": platform, "python": python}
    if len(result) > 100:
        raise MatrixError("installed matrix exceeds the 100-job evidence bound")
    return result


def verify_snapshot(
    run: dict,
    jobs: list[dict],
    *,
    run_id: int,
    candidate: str,
    workflow: str,
    title: str,
    profile: dict,
    qualification: str | None = None,
    binding: dict | None = None,
) -> dict:
    if not re.fullmatch(r"[0-9a-f]{40}", candidate):
        raise MatrixError("matrix needs a full immutable candidate SHA")
    qualification = qualification or candidate
    if not re.fullmatch(r"[0-9a-f]{40}", qualification):
        raise MatrixError("qualification workflow needs a full immutable SHA")
    if (
        run.get("id") != run_id
        or run.get("head_sha") != qualification
        or run.get("path") != workflow
        or run.get("display_title") != title
    ):
        raise MatrixError(
            "native run differs from the exact source/workflow/pair identity"
        )
    if qualification != candidate:
        pair = re.fullmatch(
            r"Installed ([a-z0-9][a-z0-9_.-]*\.tar\.bz2) ([0-9a-f]{64})", title
        )
        if (
            not pair
            or not isinstance(binding, dict)
            or binding.get("schema") != "molsyssuite.installed-source@1"
            or binding.get("candidate_sha") != candidate
            or binding.get("qualification_sha") != qualification
            or binding.get("run_id") != run_id
            or binding.get("run_attempt") != run.get("run_attempt")
            or binding.get("filename") != pair[1]
            or binding.get("sha256") != pair[2]
            or json.loads(binding.get("profile", "null")) != profile
        ):
            raise MatrixError(
                "qualification receipt does not bind the original source/file/matrix"
            )
    if (
        run.get("status") != "completed"
        or run.get("conclusion") != "success"
        or type(run.get("run_attempt")) is not int
        or run["run_attempt"] < 1
    ):
        raise MatrixError("native installed run is not a completed successful attempt")
    expected = expected_jobs(profile)
    names = [job.get("name") for job in jobs if isinstance(job, dict)]
    if (
        len(names) != len(jobs)
        or len(names) != len(set(names))
        or set(names) != set(expected)
    ):
        raise MatrixError("native jobs omit, duplicate or add a declared matrix cell")
    measured = []
    for job in jobs:
        coordinate = expected[job["name"]]
        verify_job(
            job,
            run,
            profile["required_steps"] if coordinate["kind"] == "installed" else [],
        )
        measured.append(
            dict(
                coordinate, name=job["name"], job_id=job.get("id"), conclusion="success"
            )
        )
    result = {
        "schema": "molsyssuite.installed-matrix@1",
        "state": "verified",
        "run_id": run_id,
        "run_attempt": run["run_attempt"],
        "candidate_sha": candidate,
        "workflow": workflow,
        "title": title,
        "jobs": measured,
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }
    if qualification != candidate:
        result.update(qualification_sha=qualification, source_binding=binding)
    return result


def verify(
    repository: str,
    run_id: int,
    candidate: str,
    workflow: str,
    title: str,
    profile: dict,
    token: str,
    qualification: str | None = None,
) -> dict:
    if (
        not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository)
        or type(run_id) is not int
        or run_id < 1
    ):
        raise MatrixError("matrix repository/run identity is not canonical")
    if not workflow.startswith(".github/workflows/") or not workflow.endswith(
        (".yaml", ".yml")
    ):
        raise MatrixError("matrix workflow path is not canonical")
    expected_jobs(profile)
    run, jobs, base = acquire_snapshot(repository, run_id, token)
    binding = (
        acquire_source_binding(repository, run, token)
        if qualification and qualification != candidate
        else None
    )
    result = verify_snapshot(
        run,
        jobs,
        run_id=run_id,
        candidate=candidate,
        workflow=workflow,
        title=title,
        profile=profile,
        qualification=qualification,
        binding=binding,
    )
    # A rerun started while acquiring jobs invalidates this capture.
    check_snapshot_stable(base, run, token)
    return dict(result, repository=repository)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--run-id", type=int, required=True)
    parser.add_argument("--candidate-sha", required=True)
    parser.add_argument("--qualification-sha")
    parser.add_argument("--workflow", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument(
        "--profile", required=True, help="Explicit JSON matrix descriptor"
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        if len(args.profile) > 65536:
            raise MatrixError("matrix descriptor exceeds 64 KiB")
        result = verify(
            args.repository,
            args.run_id,
            args.candidate_sha,
            args.workflow,
            args.title,
            json.loads(args.profile),
            os.environ.get("GH_TOKEN", ""),
            args.qualification_sha,
        )
        outcome = 0
    except (
        ValueError,
        OSError,
        subprocess.SubprocessError,
        zipfile.BadZipFile,
    ) as error:
        result = {
            "schema": "molsyssuite.installed-matrix@1",
            "state": "unverified",
            "error": str(error)[:1000],
        }
        outcome = 1
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, separators=(",", ":")))
    return outcome


if __name__ == "__main__":
    raise SystemExit(main())
