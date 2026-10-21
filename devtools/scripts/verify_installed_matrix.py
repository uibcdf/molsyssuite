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
from time import sleep

try:
    from devtools.scripts._release_artifacts import acquire_json_artifact
    from devtools.scripts._release_http import (
        EvidenceUnavailable,
        error_category,
        read_json,
    )
except ModuleNotFoundError:
    from _release_artifacts import acquire_json_artifact
    from _release_http import EvidenceUnavailable, error_category, read_json


class MatrixError(ValueError):
    """Native evidence does not prove the declared installed matrix."""


class MetadataPending(MatrixError):
    """A completed successful job has not exposed all required step metadata."""

    category = "metadata_pending"


def acquire_source_binding(repository: str, run: dict, token: str) -> dict:
    """Read one bounded, attempt-qualified binding published by the native run."""
    name = f"installed-source-binding-{run['id']}-{run['run_attempt']}"
    try:
        receipts, _ = acquire_json_artifact(
            repository, run, name, token, reader=read_json
        )
    except EvidenceUnavailable:
        raise
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
    if required_steps and steps is None:
        raise MetadataPending("required step metadata is not available yet")
    if required_steps and not isinstance(steps, list):
        raise MatrixError("required step evidence is malformed")
    pending = False
    for name in required_steps:
        matches = [
            step
            for step in steps
            if isinstance(step, dict) and step.get("name") == name
        ]
        if len(matches) > 1:
            raise MatrixError("required step evidence is duplicated")
        if not matches:
            pending = True
            continue
        step = matches[0]
        if step.get("conclusion") not in (None, "success") or step.get(
            "status"
        ) not in (
            None,
            "pending",
            "queued",
            "in_progress",
            "completed",
        ):
            raise MatrixError("required evidence step is missing, skipped or failed")
        if step.get("status") != "completed" or step.get("conclusion") != "success":
            pending = True
    if pending:
        raise MetadataPending("required step metadata is not available yet")


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
            "event",
        )
    ):
        raise MatrixError("native source facts changed during acquisition")


def observe_snapshot(repository: str, run_id: int, token: str, checker):
    """Verify up to three same-identity snapshots; wait only for missing step facts.

    The checker validates the complete declared contract on every observation.
    Permanent failures and acquisition errors are never converted into polling.
    """
    original = None
    for observation in range(3):
        run, jobs, base = acquire_snapshot(repository, run_id, token)
        if any(not isinstance(job, dict) for job in jobs):
            raise MatrixError("native job metadata is malformed")
        identity = (
            tuple(
                run.get(key)
                for key in (
                    "id",
                    "head_sha",
                    "run_attempt",
                    "path",
                    "display_title",
                    "event",
                    "status",
                    "conclusion",
                )
            ),
            sorted(
                json.dumps(
                    {
                        key: job.get(key)
                        for key in (
                            "id",
                            "name",
                            "run_id",
                            "run_attempt",
                            "head_sha",
                        )
                    },
                    sort_keys=True,
                )
                for job in jobs
            ),
        )
        if original is not None and identity != original:
            raise MatrixError(
                "native run/attempt/job identities changed during metadata observation"
            )
        original = identity
        try:
            result = checker(run, jobs)
        except MetadataPending:
            check_snapshot_stable(base, run, token)
            if observation == 2:
                raise MetadataPending(
                    "required step metadata remains unavailable after three observations"
                ) from None
            sleep(5)
        else:
            check_snapshot_stable(base, run, token)
            return result


def verify_native_gate(
    repository: str,
    run_id: int,
    candidate: str,
    workflow: str,
    requirements: dict[str, list[str]],
    token: str,
    *,
    title: str | None = None,
    exact_jobs: bool = False,
    event: str | None = None,
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

    def check(run, jobs):
        return _verify_native_snapshot(
            run,
            jobs,
            run_id,
            candidate,
            workflow,
            requirements,
            title=title,
            exact_jobs=exact_jobs,
            event=event,
        )

    return observe_snapshot(repository, run_id, token, check)


def _verify_native_snapshot(
    run, jobs, run_id, candidate, workflow, requirements, *, title, exact_jobs, event
):
    if (
        run.get("id") != run_id
        or run.get("head_sha") != candidate
        or run.get("path") != workflow
        or run.get("status") != "completed"
        or run.get("conclusion") != "success"
        or (title is not None and run.get("display_title") != title)
        or (event is not None and run.get("event") != event)
    ):
        raise MatrixError(
            "native gate differs from the successful exact source/workflow"
        )
    if exact_jobs and (
        len(jobs) != len(requirements)
        or {job.get("name") for job in jobs} != set(requirements)
    ):
        raise MatrixError("native gate has unexpected or incomplete matrix jobs")
    measured, pending = [], None
    for name, required_steps in requirements.items():
        matches = [
            job for job in jobs if isinstance(job, dict) and job.get("name") == name
        ]
        if len(matches) != 1:
            raise MatrixError("native gate omits or duplicates a required job")
        try:
            verify_job(matches[0], run, required_steps)
        except MetadataPending as error:
            pending = error
        measured.append(
            {
                "name": name,
                "job_id": matches[0].get("id"),
                "required_steps": required_steps,
            }
        )
    if pending is not None:
        raise pending
    return {
        "schema": "molsyssuite.native-gate@1",
        "state": "verified",
        "run_id": run_id,
        "run_attempt": run["run_attempt"],
        "candidate_sha": candidate,
        "workflow": workflow,
        "jobs": measured,
        **({"title": title} if title is not None else {}),
        **({"event": event} if event is not None else {}),
        **({"exact_jobs": True} if exact_jobs else {}),
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
    measured, pending = [], None
    for job in jobs:
        coordinate = expected[job["name"]]
        try:
            verify_job(
                job,
                run,
                profile["required_steps"] if coordinate["kind"] == "installed" else [],
            )
        except MetadataPending as error:
            pending = error
        measured.append(
            dict(
                coordinate, name=job["name"], job_id=job.get("id"), conclusion="success"
            )
        )
    if pending is not None:
        raise pending
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
    bindings = {}

    def check(run, jobs):
        binding = None
        if qualification and qualification != candidate:
            if not bindings:
                bindings["value"] = acquire_source_binding(repository, run, token)
            binding = bindings["value"]
        return verify_snapshot(
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

    result = observe_snapshot(repository, run_id, token, check)
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
            "error_category": error_category(error),
        }
        outcome = 1
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, separators=(",", ":")))
    return outcome


if __name__ == "__main__":
    raise SystemExit(main())
