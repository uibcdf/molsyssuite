"""Acquire exact-source native gates and a fail-closed Conda route preflight."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import quote, urlencode

import tomllib

try:
    from devtools.scripts._release_http import read_json
    from devtools.scripts.conda_release_contract import (
        SHA,
        ContractError,
        validate_plan,
    )
    from devtools.scripts.verify_installed_matrix import MatrixError, verify_native_gate
except ModuleNotFoundError:
    from _release_http import read_json
    from conda_release_contract import SHA, ContractError, validate_plan
    from verify_installed_matrix import MatrixError, verify_native_gate


def acquire_gates(
    repository: str,
    candidate: str,
    workflows: list[str],
    token: str,
    job_requirements: dict | None = None,
) -> list[dict]:
    if not token:
        raise ContractError(
            "read-only GitHub token is required for native gate evidence"
        )
    gates = []
    for workflow in workflows:
        query = urlencode({"head_sha": candidate, "status": "success", "per_page": 100})
        url = f"https://api.github.com/repos/{repository}/actions/workflows/{quote(Path(workflow).name)}/runs?{query}"
        runs = read_json(url, token).get("workflow_runs")
        if not isinstance(runs, list):
            raise ContractError("GitHub native gate response is incomplete")
        matches = [
            run
            for run in runs
            if isinstance(run, dict)
            and run.get("head_sha") == candidate
            and run.get("status") == "completed"
            and run.get("conclusion") == "success"
            and run.get("path") == workflow
            and type(run.get("id")) is int
            and run["id"] > 0
        ]
        if not matches:
            raise ContractError(
                f"no successful exact-source native gate for {workflow}"
            )
        jobs = (job_requirements or {}).get(workflow)
        proof = None
        for selected in sorted(matches, key=lambda run: run["id"], reverse=True):
            if jobs is None:
                break
            try:
                proof = verify_native_gate(
                    repository, selected["id"], candidate, workflow, jobs, token
                )
                break
            except MatrixError:
                continue
        if jobs is not None and proof is None:
            raise ContractError(f"no successful executed native jobs for {workflow}")
        gate = {
            "workflow": workflow,
            "candidate_sha": candidate,
            "conclusion": "success",
            "run_id": selected["id"],
        }
        if proof is not None:
            gate["executed_jobs"] = proof
        gates.append(gate)
    return gates


def acquire_absence(owner: str, package: str, version: str) -> dict:
    url = f"https://api.anaconda.org/release/{owner}/{package}/{version}"
    try:
        read_json(url)
    except HTTPError as error:
        if error.code == 404:
            return {
                "state": "absent",
                "http_status": 404,
                "scope": "all-labels",
                "url": url,
                "checked_at": datetime.now(timezone.utc).isoformat(),
            }
        raise ContractError(
            f"all-label preflight unavailable: HTTP {error.code}"
        ) from error
    raise ContractError(
        "version already registered under some label; direct upload forbidden"
    )


def preflight(
    plan: dict,
    repository: str,
    candidate: str,
    checkout: str,
    tag: str | None,
    event: str,
    token: str,
    owner: str = "uibcdf",
) -> dict:
    validate_plan(plan)
    if not re.fullmatch(
        r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository
    ) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", owner):
        raise ContractError("repository or Conda owner is not canonical")
    if not SHA.fullmatch(candidate) or checkout != candidate:
        raise ContractError("checkout differs from the full immutable candidate SHA")
    if event not in {"release", "workflow_dispatch"}:
        raise ContractError(
            "publication preflight requires release or explicit staging dispatch"
        )
    if event == "release" and tag != candidate:
        raise ContractError("published tag differs from candidate SHA")
    if event == "workflow_dispatch" and plan["route"] != "staged":
        raise ContractError("manual dispatch cannot authorize public direct upload")
    receipt = {
        "schema": "molsyssuite.conda-preflight@1",
        "version": plan["version"],
        "package": plan["package"],
        "route": plan["route"],
        "candidate_sha": candidate,
        "checkout_sha": checkout,
        "tag_sha": tag,
        "event": event,
        "decision_by": plan["decision_by"],
        "reason": plan["reason"],
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "gates": acquire_gates(
            repository,
            candidate,
            plan["required_workflows"],
            token,
            plan.get("gate_jobs"),
        ),
    }
    if plan["route"] == "direct":
        receipt["preflight"] = acquire_absence(owner, plan["package"], plan["version"])
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--candidate-sha", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument(
        "--event", choices=("release", "workflow_dispatch"), required=True
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--github-output", type=Path)
    args = parser.parse_args()
    try:
        plan = tomllib.loads(args.plan.read_text(encoding="utf-8"))
        if plan.get("version") != args.version:
            raise ContractError("selected version differs from the committed plan")
        checkout = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True
        ).strip()
        tag = (
            subprocess.check_output(
                ["git", "rev-list", "-n", "1", args.version], text=True
            ).strip()
            if args.event == "release"
            else None
        )
        receipt = preflight(
            plan,
            args.repository,
            args.candidate_sha,
            checkout,
            tag,
            args.event,
            os.environ.get("GH_TOKEN", ""),
        )
        args.output.write_text(
            json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        if args.github_output:
            with args.github_output.open("a", encoding="utf-8") as stream:
                stream.write("route=" + receipt["route"] + "\n")
    except (ContractError, OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"Conda route not authorized: {error}")
        return 1
    print("Conda route preflight verified; publication remains a separate operation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
