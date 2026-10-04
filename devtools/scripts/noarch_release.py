"""Prepare a staged noarch release handoff from native receipts, without mutations."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

import yaml

if not __package__:
    sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    from devtools.scripts._release_artifacts import acquire_json_artifact
    from devtools.scripts._release_http import read_json
    from devtools.scripts.conda_release_contract import SHA, ContractError
    from devtools.scripts.noarch_conda import inspect_recipe, promotion_descriptor
    from devtools.scripts.verify_installed_matrix import (
        acquire_snapshot,
        check_snapshot_stable,
        verify,
        verify_job,
    )
    from devtools.scripts.verify_public_conda import verify_public
except ModuleNotFoundError:
    from _release_artifacts import acquire_json_artifact
    from _release_http import read_json
    from conda_release_contract import SHA, ContractError
    from noarch_conda import inspect_recipe, promotion_descriptor
    from verify_installed_matrix import (
        acquire_snapshot,
        check_snapshot_stable,
        verify,
        verify_job,
    )
    from verify_public_conda import verify_public


def one_receipt(receipts: dict, filename: str) -> dict:
    matches = [value for name, value in receipts.items() if Path(name).name == filename]
    if len(matches) != 1:
        raise ContractError(f"producer evidence needs exactly one {filename}")
    return matches[0]


def bind_producer(
    repository: str, run: dict, jobs: list[dict], receipts: dict, plan: dict
) -> dict:
    """Bind original checkout, inspected coordinate and verified native upload."""
    preflight = one_receipt(receipts, "noarch-preflight.json")
    archive = one_receipt(receipts, "noarch-artifact.json")
    upload = one_receipt(receipts, "conda-upload-receipt.json")
    candidate = preflight.get("candidate_sha", "")
    filename = f"{plan['package']}-{plan['version']}-py_{plan['build_number']}.tar.bz2"
    coordinate = {
        "owner": "uibcdf",
        "package": plan["package"],
        "version": plan["version"],
        "subdir": "noarch",
        "filename": filename,
    }
    digest = archive.get("sha256", "")
    if (
        plan["route"] != "staged"
        or not SHA.fullmatch(str(candidate))
        or preflight.get("schema") != "molsyssuite.conda-preflight@1"
        or preflight.get("checkout_sha") != candidate
        or preflight.get("event") != "workflow_dispatch"
        or any(
            preflight.get(key) != plan[key] for key in ("package", "version", "route")
        )
        or any(
            archive.get(key) != value
            for key, value in coordinate.items()
            if key != "owner"
        )
        or archive.get("build_number") != plan["build_number"]
        or archive.get("route") != "staged"
        or not re.fullmatch(r"[0-9a-f]{64}", str(digest))
        or upload.get("schema") != "uibcdf.conda-upload@1"
        or upload.get("state") != "verified"
        or upload.get("label") != "staging"
        or upload.get("candidate_sha") != candidate
        or upload.get("coordinate") != coordinate
        or upload.get("sha256") != digest
        or upload.get("subject")
        != {
            "repository": repository,
            "run_id": str(run["id"]),
            "run_attempt": str(run["run_attempt"]),
        }
        or run.get("status") != "completed"
        or run.get("conclusion") != "success"
        or run.get("event") != "workflow_dispatch"
        or not SHA.fullmatch(str(run.get("head_sha", "")))
    ):
        raise ContractError(
            "producer receipts do not bind the successful exact staged file"
        )
    required = [
        "Acquire exact-source executed CI gates and route preflight",
        "Build once and run recipe tests without uploading or conversion",
        "Inspect exact built metadata, embedded version and resources",
        "Upload exact reviewed file to staging",
        "Retain candidate, producer and independent receipts",
    ]
    matches = [
        job
        for job in jobs
        if all(
            any(step.get("name") == name for step in job.get("steps", []))
            for name in required
        )
    ]
    if len(matches) != 1:
        raise ContractError("native producer needs one executed shared staging job")
    verify_job(matches[0], run, required)
    return dict(coordinate, sha256=digest, candidate_sha=candidate)


def git(root: Path, *arguments: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(root), *arguments], text=True, timeout=30
    ).strip()


def caller(
    root: Path, revision: str, workflow: str, kind: str, fields: list[str]
) -> str:
    """Accept a pinned caller with all required inputs generated and forwarded."""
    if not re.fullmatch(r"\.github/workflows/[A-Za-z0-9_.-]+\.ya?ml", workflow):
        raise ContractError("caller workflow path is not canonical")
    document = yaml.load(
        git(root, "show", f"{revision}:{workflow}"), Loader=yaml.BaseLoader
    )
    dispatch = document.get("on", {}).get("workflow_dispatch")
    if not isinstance(dispatch, dict) or not set(fields).issubset(
        dispatch.get("inputs", {})
    ):
        raise ContractError("caller does not declare every required dispatch input")
    extra_required = sorted(
        name
        for name, definition in dispatch["inputs"].items()
        if isinstance(definition, dict)
        and definition.get("required") in (True, "true")
        and name not in fields
    )
    if extra_required:
        raise ContractError(
            "caller requires inputs not generated by this adapter: "
            + ", ".join(extra_required)
            + "; use a reviewed component adapter or its existing local route"
        )
    prefix = f"uibcdf/molsyssuite/.github/workflows/{kind}-noarch-conda.yaml@"
    jobs = [
        job
        for job in document.get("jobs", {}).values()
        if job.get("uses", "").startswith(prefix)
    ]
    if len(jobs) != 1 or not SHA.fullmatch(jobs[0]["uses"].removeprefix(prefix)):
        raise ContractError("caller needs one shared workflow pinned to a full commit")
    if any(
        jobs[0].get("with", {}).get(field) != "${{ inputs." + field + " }}"
        for field in fields
    ):
        raise ContractError("caller does not forward generated inputs unchanged")
    return jobs[0]["uses"]


def dispatch_arguments(
    repository: str, workflow: str, ref: str, inputs: dict
) -> list[str]:
    """Return argv, never shell source or an executed command."""
    result = ["gh", "workflow", "run", workflow, "--repo", repository, "--ref", ref]
    for name, value in inputs.items():
        result.extend(["--raw-field", f"{name}={value}"])
    return result


def registered_file(identity: dict) -> dict:
    """Check the current exact-file poststate before preparing another operation."""
    document = read_json(
        f"https://api.anaconda.org/release/uibcdf/{identity['package']}/{identity['version']}"
    )
    distributions = document.get("distributions")
    if not isinstance(distributions, list):
        raise ContractError("current registry file inventory is unavailable")
    basename = "noarch/" + identity["filename"]
    matches = [
        item
        for item in distributions
        if isinstance(item, dict) and item.get("basename") == basename
    ]
    if len(matches) != 1 or matches[0].get("sha256") != identity["sha256"]:
        raise ContractError("current registered file differs from the producer archive")
    labels = matches[0].get("labels")
    if not isinstance(labels, list) or not {"staging", "main"}.intersection(labels):
        raise ContractError("registered file has no applicable staging or public label")
    return {"basename": basename, "sha256": identity["sha256"], "labels": labels}


def prepare_handoff(
    root: Path,
    repository: str,
    producer_run_id: int,
    *,
    token: str,
    qualification_sha: str | None = None,
    workflow_ref: str | None = None,
    installed_run_id: int | None = None,
    promotion_workflow: str | None = None,
    public: bool = False,
) -> dict:
    """Acquire evidence and compose the next existing wrapper's reviewed inputs."""
    plan, inventory = inspect_recipe(
        root,
        "devtools/conda-build/release_plan.toml",
        "devtools/conda-build/resources.toml",
    )
    run, jobs, base = acquire_snapshot(repository, producer_run_id, token)
    name = f"noarch-publication-{run['id']}-{run['run_attempt']}"
    receipts, artifact = acquire_json_artifact(repository, run, name, token)
    identity = bind_producer(repository, run, jobs, receipts, plan)
    candidate = identity["candidate_sha"]
    if git(root, "rev-parse", "HEAD") != candidate or git(
        root, "status", "--porcelain", "--untracked-files=no"
    ):
        raise ContractError("use a clean clone at the original producer candidate")
    qualification = qualification_sha or candidate
    if not SHA.fullmatch(qualification):
        raise ContractError("qualification needs a reviewed full immutable commit")
    descriptor = promotion_descriptor(root, plan, inventory, identity["sha256"])
    registry = registered_file(identity)
    result = {
        "schema": "molsyssuite.noarch-handoff@1",
        "state": "prepared",
        "repository": repository,
        "identity": identity,
        "qualification_sha": qualification,
        "producer": {
            "run_id": run["id"],
            "run_attempt": run["run_attempt"],
            "workflow_head_sha": run["head_sha"],
            "artifact": artifact,
        },
        "installed_profile": json.loads(descriptor["profile"]),
        "registry": registry,
        "next_command": None,
        "mutation_performed": False,
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }
    if installed_run_id is not None:
        result["installed"] = verify(
            repository,
            installed_run_id,
            candidate,
            descriptor["workflow"],
            descriptor["title"],
            json.loads(descriptor["profile"]),
            token,
            qualification,
        )
    if public or "main" in registry["labels"]:
        if installed_run_id is None:
            raise ContractError(
                "file is already public; provide its existing installed run, never repeat publication"
            )
        url = verify_public(
            identity["package"],
            identity["version"],
            "noarch",
            identity["filename"],
            identity["sha256"],
            attempts=1,
            interval=0,
        )
        result.update(state="public-verified", public_url=url)
    else:
        if not workflow_ref or workflow_ref.startswith("-"):
            raise ContractError("provide the reviewed workflow branch or tag")
        resolved = read_json(
            f"https://api.github.com/repos/{repository}/commits/{quote(workflow_ref, safe='')}",
            token,
        )
        if resolved.get("sha") != qualification:
            raise ContractError(
                "workflow ref differs from the reviewed qualification commit"
            )
        inputs = {
            "candidate_sha": candidate,
            "version": plan["version"],
            "sha256": identity["sha256"],
        }
        if installed_run_id is None:
            workflow, kind = descriptor["workflow"], "test-installed"
            inputs.pop("version")
            inputs["filename"] = identity["filename"]
        else:
            if not promotion_workflow:
                raise ContractError("provide the component's promotion workflow")
            workflow, kind = promotion_workflow, "promote"
            inputs["installed_run_id"] = str(installed_run_id)
            if qualification != candidate:
                inputs["qualification_sha"] = qualification
        result["caller"] = caller(root, qualification, workflow, kind, list(inputs))
        result["next_command"] = dispatch_arguments(
            repository, workflow, workflow_ref, inputs
        )
        result["next_operation"] = (
            "qualify-installed" if installed_run_id is None else "promote-existing"
        )
    check_snapshot_stable(base, run, token)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--producer-run-id", type=int, required=True)
    parser.add_argument("--qualification-sha")
    parser.add_argument("--workflow-ref")
    parser.add_argument("--installed-run-id", type=int)
    parser.add_argument("--promotion-workflow")
    parser.add_argument("--verify-public", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        token = (
            os.environ.get("GH_TOKEN", "")
            or subprocess.check_output(
                ["gh", "auth", "token"],
                text=True,
                timeout=30,
                stderr=subprocess.DEVNULL,
            ).strip()
        )
        result = prepare_handoff(
            args.root.resolve(),
            args.repository,
            args.producer_run_id,
            token=token,
            qualification_sha=args.qualification_sha,
            workflow_ref=args.workflow_ref,
            installed_run_id=args.installed_run_id,
            promotion_workflow=args.promotion_workflow,
            public=args.verify_public,
        )
        outcome = 0
    except (
        ValueError,
        KeyError,
        TypeError,
        OSError,
        subprocess.SubprocessError,
        zipfile.BadZipFile,
    ) as error:
        result = {
            "schema": "molsyssuite.noarch-handoff@1",
            "state": "unverified",
            "mutation_performed": False,
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
