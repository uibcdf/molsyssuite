"""Prepare a staged noarch release handoff from native receipts, without mutations."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

import tomllib
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
        verify_native_gate,
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
        verify_native_gate,
    )
    from verify_public_conda import verify_public


GATE_PROFILES = Path(__file__).resolve().parents[1] / "noarch_gate_profiles.toml"


def load_gate_profile(path: Path, name: str, repository: str) -> dict:
    """Select one explicitly reviewed data profile; no component code is loaded."""
    document = tomllib.loads(path.read_text(encoding="utf-8"))
    if document.get("schema-version") != 1:
        raise ContractError("unsupported additional-gate profile schema")
    profiles = document.get("profiles", [])
    if not isinstance(profiles, list) or any(not isinstance(p, dict) for p in profiles):
        raise ContractError("additional-gate profiles must be records")
    matches = [p for p in profiles if p.get("name") == name]
    if len(matches) != 1 or matches[0].get("repository") != repository:
        raise ContractError(
            "additional-gate profile is unknown or belongs to another owner"
        )
    profile = matches[0]
    if (
        not SHA.fullmatch(str(profile.get("reviewed-source", "")))
        or not str(profile.get("owner-issue", "")).startswith(repository + "#")
        or not profile.get("gates")
        or not profile.get("caller-inputs")
        or not profile.get("producer-inputs")
    ):
        raise ContractError("additional-gate profile lacks reviewed source/contracts")
    for key in ("caller-inputs", "producer-inputs"):
        if not isinstance(profile[key], dict) or any(
            not isinstance(relative, str)
            or not re.fullmatch(r"[0-9a-f]{64}", str(digest))
            for relative, digest in profile[key].items()
        ):
            raise ContractError(
                "additional-gate source inputs must be path/digest records"
            )
    gates = profile["gates"]
    if (
        not isinstance(gates, list)
        or len(gates) > 20
        or any(not isinstance(g, dict) for g in gates)
    ):
        raise ContractError("additional gates must be a bounded list of records")
    for gate in gates:
        if (
            any(
                not isinstance(gate.get(key), str) or not gate[key]
                for key in (
                    "input",
                    "guard-job",
                    "guard-step",
                    "guard-env",
                    "workflow",
                    "title-template",
                    "job-template",
                )
            )
            or not isinstance(gate.get("runners"), dict)
            or not gate["runners"]
            or any(
                not isinstance(value, str) or not value
                for value in gate["runners"].values()
            )
            or not isinstance(gate.get("required-steps"), list)
            or not gate["required-steps"]
        ):
            raise ContractError(
                "additional gate lacks explicit guard/matrix/step bindings"
            )
    return profile


def verify_additional_gates(
    root: Path,
    repository: str,
    qualification: str,
    workflow: str,
    identity: dict,
    plan: dict,
    profile: dict,
    gate_runs: dict[str, int],
    token: str,
    *,
    promotion_sha: str | None = None,
) -> dict:
    """Bind an optional component guard and its native evidence before handoff.

    The component retains scientific selection and the guard before promotion.
    This operation only reads pinned source and existing GitHub evidence.
    """
    if workflow != profile.get("caller"):
        raise ContractError(
            "additional-gate profile belongs to another promotion caller"
        )
    for key, revision in (
        ("caller-inputs", promotion_sha or qualification),
        ("producer-inputs", identity["candidate_sha"]),
    ):
        for relative, expected in profile[key].items():
            path = Path(relative)
            if (
                path.is_absolute()
                or ".." in path.parts
                or not re.fullmatch(r"[0-9a-f]{64}", str(expected))
            ):
                raise ContractError("additional-gate source binding is malformed")
            # Preserve Git's exact blob bytes, including final newlines.
            blob = subprocess.check_output(
                ["git", "-C", str(root), "show", f"{revision}:{relative}"], timeout=30
            )
            if hashlib.sha256(blob).hexdigest() != expected:
                raise ContractError(f"additional-gate source drift: {relative}")
    gates = profile["gates"]
    fields = [gate["input"] for gate in gates]
    reserved = {
        "candidate_sha",
        "version",
        "sha256",
        "filename",
        "installed_run_id",
        "qualification_sha",
    }
    if (
        len(set(fields)) != len(fields)
        or set(gate_runs) != set(fields)
        or reserved.intersection(fields)
        or workflow not in profile["caller-inputs"]
    ):
        raise ContractError("supply exactly the additional-gate profile's run inputs")
    document = yaml.load(
        git(root, "show", f"{promotion_sha or qualification}:{workflow}"),
        Loader=yaml.BaseLoader,
    )
    jobs = document.get("jobs", {})
    promotion = jobs.get(profile["promotion-job"], {})
    needs = promotion.get("needs", [])
    if isinstance(needs, str):
        needs = [needs]
    measured = []
    for gate in gates:
        field = gate["input"]
        if (
            not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", field)
            or type(gate_runs[field]) is not int
            or gate_runs[field] < 1
        ):
            raise ContractError(
                "additional gate needs a canonical input and positive run ID"
            )
        guard = jobs.get(gate["guard-job"], {})
        steps = [
            step
            for step in guard.get("steps", [])
            if step.get("name") == gate["guard-step"]
        ]
        definition = (
            document.get("on", {})
            .get("workflow_dispatch", {})
            .get("inputs", {})
            .get(field, {})
        )
        if (
            gate["guard-job"] not in needs
            or guard.get("if") not in (None, "true")
            or promotion.get("if") not in (None, "true")
            or guard.get("continue-on-error", "false") != "false"
            or len(steps) != 1
            or steps[0].get("if") not in (None, "true")
            or steps[0].get("continue-on-error", "false") != "false"
            or steps[0].get("env", {}).get(gate["guard-env"])
            != "${{ inputs." + field + " }}"
            or definition.get("required") != "true"
        ):
            raise ContractError(
                "additional gate is not a required input/guard before promotion"
            )
        runners = gate["runners"]
        if (
            gate["workflow"] not in profile["producer-inputs"]
            or "{runner}" not in gate["job-template"]
            or "{python}" not in gate["job-template"]
            or "{filename}" not in gate["title-template"]
            or "{sha256}" not in gate["title-template"]
            or "{"
            in gate["job-template"].replace("{runner}", "").replace("{python}", "")
            or "{"
            in gate["title-template"].replace("{filename}", "").replace("{sha256}", "")
        ):
            raise ContractError(
                "additional-gate templates/source binding omit the exact file or matrix"
            )
        platforms, minors = plan["test_platforms"], plan["python_versions"]
        if not platforms or not minors or any(p not in runners for p in platforms):
            raise ContractError(
                "additional-gate profile does not cover the candidate matrix"
            )
        requirements = {
            gate["job-template"].format(runner=runners[platform], python=minor): gate[
                "required-steps"
            ]
            for platform in platforms
            for minor in minors
        }
        if len(requirements) != len(platforms) * len(minors):
            raise ContractError(
                "additional-gate job names do not identify each matrix cell"
            )
        evidence = verify_native_gate(
            repository,
            gate_runs[field],
            identity["candidate_sha"],
            gate["workflow"],
            requirements,
            token,
            title=gate["title-template"].format(
                filename=identity["filename"], sha256=identity["sha256"]
            ),
            exact_jobs=True,
            event="workflow_dispatch",
        )
        measured.append(
            {"input": field, "guard_job": gate["guard-job"], "evidence": evidence}
        )
    return {
        "schema": "molsyssuite.additional-release-gates@1",
        "state": "verified",
        "profile": profile["name"],
        "profile_reviewed_source": profile["reviewed-source"],
        "owner_issue": profile["owner-issue"],
        "candidate_sha": identity["candidate_sha"],
        "qualification_sha": qualification,
        "promotion_sha": promotion_sha or qualification,
        "filename": identity["filename"],
        "sha256": identity["sha256"],
        "gates": measured,
    }


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
    root: Path,
    revision: str,
    workflow: str,
    kind: str,
    fields: list[str],
    *,
    component_gate_fields: list[str] | None = None,
) -> str:
    """Check standard forwarding plus fields verified by verify_additional_gates."""
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
        and name not in fields + (component_gate_fields or [])
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
    gate_profile: str | None = None,
    gate_runs: dict[str, int] | None = None,
    gate_profiles: Path = GATE_PROFILES,
    promotion_sha: str | None = None,
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
    promotion_source = promotion_sha or qualification
    if not SHA.fullmatch(promotion_source) or (
        promotion_sha and installed_run_id is None
    ):
        raise ContractError(
            "promotion source needs an immutable commit and installed evidence"
        )
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
    additional_fields = {}
    if gate_profile is not None:
        if installed_run_id is None or not promotion_workflow:
            raise ContractError(
                "additional gates require installed evidence and the promotion caller"
            )
        profile = load_gate_profile(gate_profiles, gate_profile, repository)
        result["additional_gates"] = verify_additional_gates(
            root,
            repository,
            qualification,
            promotion_workflow,
            identity,
            plan,
            profile,
            gate_runs or {},
            token,
            promotion_sha=promotion_source,
        )
        result["additional_gates"]["profile_source"] = str(gate_profiles)
        result["additional_gates"]["profile_source_sha256"] = hashlib.sha256(
            gate_profiles.read_bytes()
        ).hexdigest()
        additional_fields = {
            field: str(run_id) for field, run_id in (gate_runs or {}).items()
        }
        result["caller"] = caller(
            root,
            promotion_source,
            promotion_workflow,
            "promote",
            ["candidate_sha", "version", "sha256", "installed_run_id"]
            + (["qualification_sha"] if qualification != candidate else []),
            component_gate_fields=list(additional_fields),
        )
        result["promotion_sha"] = promotion_source
    elif gate_runs:
        raise ContractError(
            "additional run inputs require an explicit reviewed gate profile"
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
        dispatch_source = (
            promotion_source if installed_run_id is not None else qualification
        )
        if resolved.get("sha") != dispatch_source:
            raise ContractError(
                "workflow ref differs from the reviewed dispatch commit"
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
            result["promotion_sha"] = promotion_source
            if gate_profile and workflow_ref not in profile.get(
                "workflow-refs", [workflow_ref]
            ):
                raise ContractError(
                    "additional-gate caller requires another workflow branch/tag"
                )
        if not additional_fields:
            result["caller"] = caller(
                root, dispatch_source, workflow, kind, list(inputs)
            )
        inputs.update(additional_fields)
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
    parser.add_argument(
        "--promotion-sha",
        help="immutable promoter source; installed qualification remains separate",
    )
    parser.add_argument("--verify-public", action="store_true")
    parser.add_argument(
        "--gate-profile", help="opt-in reviewed additional-gate profile"
    )
    parser.add_argument("--gate-profiles", type=Path, default=GATE_PROFILES)
    parser.add_argument(
        "--gate-run", action="append", default=[], metavar="INPUT=RUN_ID"
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        gate_runs = {}
        for assignment in args.gate_run:
            field, separator, value = assignment.partition("=")
            if (
                not separator
                or field in gate_runs
                or not re.fullmatch(r"[1-9][0-9]*", value)
            ):
                raise ContractError(
                    "gate-run needs unique INPUT=positive-run-ID assignments"
                )
            gate_runs[field] = int(value)
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
            gate_profile=args.gate_profile,
            gate_runs=gate_runs,
            gate_profiles=args.gate_profiles,
            promotion_sha=args.promotion_sha,
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
