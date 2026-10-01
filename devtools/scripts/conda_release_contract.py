"""Validate shared Conda decisions, evidence and publication workflow invariants."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import tomllib
import yaml

try:
    from devtools.scripts.verify_public_conda import (
        VerificationError,
        validate_coordinate,
    )
except ModuleNotFoundError:
    from verify_public_conda import VerificationError, validate_coordinate

SHA = re.compile(r"[0-9a-f]{40}\Z")
VERSION = re.compile(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\Z")
BUILD_ACTION = "uibcdf/action-build-and-upload-conda-packages@"
PROMOTE_ACTION = "uibcdf/action-build-and-upload-conda-packages/promote@"
UPLOAD_ACTION = "uibcdf/action-build-and-upload-conda-packages/upload@"
NOARCH_WORKFLOWS = (
    "uibcdf/molsyssuite/.github/workflows/publish-noarch-conda.yaml@",
    "uibcdf/molsyssuite/.github/workflows/promote-noarch-conda.yaml@",
    "uibcdf/molsyssuite/.github/workflows/test-installed-noarch-conda.yaml@",
)


class ContractError(ValueError):
    """A publication decision or proof contradicts the shared contract."""


def validate_plan(plan: dict) -> None:
    """Validate objective route conditions independently of component names."""
    if plan.get("schema") != "molsyssuite.conda-plan@1":
        raise ContractError("release plan needs schema molsyssuite.conda-plan@1")
    if not VERSION.fullmatch(str(plan.get("version", ""))):
        raise ContractError("release plan needs a canonical version")
    if (
        not re.fullmatch(r"[a-z0-9][a-z0-9-]*", str(plan.get("package", "")))
        or type(plan.get("build_number")) is not int
        or plan["build_number"] < 0
    ):
        raise ContractError(
            "release plan needs an exact package and nonnegative build number"
        )
    if plan.get("route") not in {"direct", "staged"}:
        raise ContractError("release plan needs direct or staged route")
    if plan.get("profile") not in {"native-abi3", "noarch-python", "metapackage"}:
        raise ContractError("release plan needs a supported artifact profile")
    for field in ("reason", "decision_by"):
        if not isinstance(plan.get(field), str) or not plan[field].strip():
            raise ContractError(f"release plan needs {field}")
    for field in (
        "artifact_subdirs",
        "test_platforms",
        "python_versions",
        "required_workflows",
    ):
        values = plan.get(field)
        if (
            not isinstance(values, list)
            or not values
            or any(not isinstance(v, str) or not v for v in values)
            or len(set(values)) != len(values)
        ):
            raise ContractError(f"release plan needs unique nonempty {field}")
    if any(
        not value.startswith(".github/workflows/")
        or not value.endswith((".yaml", ".yml"))
        for value in plan["required_workflows"]
    ):
        raise ContractError("required workflow identities are not canonical")
    if any(
        not re.fullmatch(r"[a-z0-9][a-z0-9-]*", value)
        for field in ("artifact_subdirs", "test_platforms")
        for value in plan[field]
    ) or any(
        not re.fullmatch(r"[0-9]+\.[0-9]+", value) for value in plan["python_versions"]
    ):
        raise ContractError("platform/Python matrix identities are not canonical")
    if plan["profile"] != "native-abi3" and plan["artifact_subdirs"] != ["noarch"]:
        raise ContractError("noarch profile must produce one noarch coordinate")
    if plan["profile"] == "native-abi3" and (
        "noarch" in plan["artifact_subdirs"]
        or not set(plan["artifact_subdirs"]).issubset(plan["test_platforms"])
    ):
        raise ContractError("native artifacts must retain every claimed test platform")
    flags = (
        "requires_installed_gate",
        "new_compatibility_surface",
        "coupled_release",
        "dependencies_public",
    )
    if any(type(plan.get(field)) is not bool for field in flags):
        raise ContractError("release plan needs explicit route-condition booleans")
    if plan["route"] == "direct" and (
        any(plan[field] for field in flags[:3]) or not plan["dependencies_public"]
    ):
        raise ContractError("direct route contradicts a mandatory staging condition")
    job_requirements = plan.get("gate_jobs", {})
    if not isinstance(job_requirements, dict) or any(
        workflow not in plan["required_workflows"] for workflow in job_requirements
    ):
        raise ContractError(
            "executed gate jobs must belong to declared native workflows"
        )
    for jobs in job_requirements.values():
        if not isinstance(jobs, dict) or not jobs or len(jobs) > 100:
            raise ContractError(
                "executed native gate needs a bounded explicit job inventory"
            )
        for name, steps in jobs.items():
            if (
                not isinstance(name, str)
                or not name
                or not isinstance(steps, list)
                or not steps
                or any(not isinstance(step, str) or not step for step in steps)
                or len(steps) != len(set(steps))
            ):
                raise ContractError(
                    "executed native jobs need unique nonempty step identities"
                )


def validate_transition(plan: dict, evidence: dict) -> None:
    """Check bound evidence; callers still acquire native/API proof independently."""
    validate_plan(plan)
    candidate = evidence.get("candidate_sha", "")
    if (
        not SHA.fullmatch(str(candidate))
        or evidence.get("checkout_sha") != candidate
        or evidence.get("tag_sha") != candidate
    ):
        raise ContractError("candidate, checkout and tag must be the same full SHA")
    if (
        evidence.get("version") != plan["version"]
        or evidence.get("route") != plan["route"]
    ):
        raise ContractError("evidence differs from the committed route decision")
    gates = evidence.get("gates")
    if not isinstance(gates, list):
        raise ContractError("native gate evidence is missing")
    for workflow in plan["required_workflows"]:
        matches = [
            gate
            for gate in gates
            if isinstance(gate, dict) and gate.get("workflow") == workflow
        ]
        if (
            len(matches) != 1
            or matches[0].get("candidate_sha") != candidate
            or matches[0].get("conclusion") != "success"
            or type(matches[0].get("run_id")) is not int
            or matches[0]["run_id"] <= 0
        ):
            raise ContractError(
                "required exact-source native gate is missing or unsuccessful"
            )
        requirements = plan.get("gate_jobs", {}).get(workflow)
        if requirements is not None:
            proof = matches[0].get("executed_jobs", {})
            jobs = proof.get("jobs", [])
            if (
                proof.get("schema") != "molsyssuite.native-gate@1"
                or proof.get("state") != "verified"
                or proof.get("candidate_sha") != candidate
                or proof.get("workflow") != workflow
                or proof.get("run_id") != matches[0]["run_id"]
                or type(proof.get("run_attempt")) is not int
                or proof["run_attempt"] < 1
            ):
                raise ContractError(
                    "executed-job native gate proof is missing or mismatched"
                )
            if (
                not isinstance(jobs, list)
                or len(jobs) != len(requirements)
                or any(not isinstance(job, dict) for job in jobs)
                or {job.get("name") for job in jobs} != set(requirements)
                or any(
                    job.get("required_steps") != requirements[job["name"]]
                    for job in jobs
                )
            ):
                raise ContractError(
                    "executed-job proof differs from the committed job/step inventory"
                )
    if plan["route"] == "direct":
        preflight = evidence.get("preflight", {})
        if (
            preflight.get("state") != "absent"
            or preflight.get("http_status") != 404
            or preflight.get("scope") != "all-labels"
            or not preflight.get("checked_at")
        ):
            raise ContractError(
                "direct route needs conclusive timestamped all-label absence"
            )
        if (
            evidence.get("overwrite")
            or evidence.get("no_test")
            or evidence.get("event") != "release"
        ):
            raise ContractError(
                "direct public route forbids overwrite, no-test and manual publication"
            )
        if evidence.get("producer_receipt", {}).get("state") != "verified":
            raise ContractError("successful tested producer receipt is missing")
    else:
        if evidence.get("promotion_receipt", {}).get("state") != "verified":
            raise ContractError("successful exact-file promotion receipt is missing")
        if (
            evidence.get("promotion_receipt", {}).get("from_label") != "staging"
            or evidence.get("promotion_receipt", {}).get("to_label") != "main"
        ):
            raise ContractError(
                "promotion label transition differs from staging to main"
            )
        if (
            evidence.get("overwrite")
            or evidence.get("no_test")
            or evidence.get("rebuild")
        ):
            raise ContractError(
                "public promotion forbids overwrite, no-test and rebuild"
            )
    inventory = evidence.get("inventory")
    if not isinstance(inventory, list) or not inventory:
        raise ContractError("exact immutable promotion inventory is missing")
    for item in inventory:
        if not isinstance(item, dict) or set(item) != {
            "package",
            "version",
            "subdir",
            "filename",
            "sha256",
        }:
            raise ContractError("immutable inventory fields differ from the contract")
        try:
            validate_coordinate(**item)
        except (VerificationError, TypeError) as error:
            raise ContractError("invalid immutable inventory coordinate") from error
        if (
            item["package"] != plan["package"]
            or item["version"] != plan["version"]
            or not re.search(
                r"_" + str(plan["build_number"]) + r"\.(?:conda|tar\.bz2)\Z",
                item["filename"],
            )
        ):
            raise ContractError(
                "inventory differs from the planned package/version/build"
            )
    subdirs = [item.get("subdir") for item in inventory if isinstance(item, dict)]
    if len(subdirs) != len(inventory) or sorted(subdirs) != sorted(
        plan["artifact_subdirs"]
    ):
        raise ContractError(
            "promotion inventory omits or duplicates a native/noarch artifact"
        )
    public = evidence.get("public", {})
    if (
        public.get("schema") != "molsyssuite.public-conda@1"
        or public.get("state") != "verified"
    ):
        raise ContractError("independent public label/index proof is missing")
    verified = [
        {
            key: item.get(key)
            for key in ("package", "version", "subdir", "filename", "sha256")
        }
        for item in public.get("files", [])
        if isinstance(item, dict)
        and item.get("main_label") == "verified"
        and item.get("solver_index") == "verified"
    ]
    if verified != inventory:
        raise ContractError("public proof differs from the exact promoted inventory")
    receipt = evidence[
        "producer_receipt" if plan["route"] == "direct" else "promotion_receipt"
    ]
    if (
        receipt.get("inventory") != inventory
        or receipt.get("candidate_sha") != candidate
    ):
        raise ContractError(
            "producer/promotion receipt is not bound to this source and inventory"
        )
    if plan["route"] == "direct" and receipt.get("recipe_tests") != "success":
        raise ContractError("direct producer has no successful recipe-test evidence")
    if plan["route"] == "direct":
        return
    cells = evidence.get("installed_cells", [])
    installed_inventory = inventory
    if plan["coupled_release"]:
        installed_inventory = evidence.get("pair_inventory")
        if (
            not isinstance(installed_inventory, list)
            or not all(item in installed_inventory for item in inventory)
            or not any(
                isinstance(item, dict) and item.get("package") != plan["package"]
                for item in installed_inventory
            )
        ):
            raise ContractError(
                "coupled installed gate needs the exact counterpart inventory"
            )
        for item in installed_inventory:
            try:
                validate_coordinate(**item)
            except (VerificationError, TypeError) as error:
                raise ContractError("invalid counterpart coordinate") from error
    expected = {
        (platform, python)
        for platform in plan["test_platforms"]
        for python in plan["python_versions"]
    }
    observed = {
        (cell.get("platform"), cell.get("python"))
        for cell in cells
        if isinstance(cell, dict)
        and cell.get("conclusion") == "success"
        and cell.get("candidate_sha") == candidate
        and cell.get("installed_inventory") == installed_inventory
    }
    if observed != expected or len(cells) != len(expected):
        raise ContractError(
            "installed artifact matrix omits, duplicates or fails a claimed cell"
        )


def workflow_findings(root: Path) -> list[str]:
    """Audit explicit publisher controls without inferring scientific correctness."""
    if not root.is_dir():
        raise ContractError("repository checkout is unavailable")
    findings = []
    directory = root / ".github/workflows"
    for path in sorted(directory.glob("*")):
        if path.suffix not in {".yml", ".yaml"}:
            continue
        data = yaml.load(path.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
        if not isinstance(data, dict):
            continue
        events = data.get("on", {})
        for job in data.get("jobs", {}).values():
            if not isinstance(job, dict):
                continue
            caller = str(job.get("uses", ""))
            if caller.startswith(NOARCH_WORKFLOWS):
                prefix = path.name + ": "
                if not SHA.fullmatch(caller.rsplit("@", 1)[-1]):
                    findings.append(
                        prefix + "shared noarch workflow must use a reviewed full SHA"
                    )
                options = job.get("with", {})
                installed = caller.startswith(NOARCH_WORKFLOWS[2])
                if not options.get("candidate_sha") or not options.get(
                    "filename" if installed else "version"
                ):
                    findings.append(
                        prefix
                        + "shared noarch workflow needs exact candidate and version inputs"
                    )
                if not installed and (
                    not isinstance(job.get("secrets"), dict)
                    or not job["secrets"].get("ANACONDA_TOKEN")
                ):
                    findings.append(
                        prefix
                        + "shared noarch workflow needs an explicit publication secret mapping"
                    )
                if installed and (
                    not options.get("sha256")
                    or job.get("secrets")
                    or not isinstance(events, dict)
                    or set(events) != {"workflow_dispatch"}
                ):
                    findings.append(
                        prefix
                        + "installed noarch qualification needs a manual exact file and no publication secrets"
                    )
                if caller.startswith(NOARCH_WORKFLOWS[1]) and (
                    not options.get("sha256")
                    or not options.get("installed_run_id")
                    or not isinstance(events, dict)
                    or set(events) != {"workflow_dispatch"}
                ):
                    findings.append(
                        prefix
                        + "shared noarch promotion needs explicit manual exact-file installed evidence"
                    )
            steps = job.get("steps", [])
            for step in steps:
                if not isinstance(step, dict):
                    continue
                uses = step.get("uses", "")
                is_build, is_promote, is_upload = (
                    uses.startswith(BUILD_ACTION),
                    uses.startswith(PROMOTE_ACTION),
                    uses.startswith(UPLOAD_ACTION),
                )
                if not (is_build or is_promote or is_upload):
                    continue
                ref = uses.rsplit("@", 1)[-1]
                prefix = path.name + ": "
                if not SHA.fullmatch(ref) and not re.fullmatch(
                    r"v[0-9]+\.[0-9]+\.[0-9]+", ref
                ):
                    findings.append(
                        prefix
                        + "publisher action must use a reviewed version or full SHA"
                    )
                options = step.get("with", {})
                if is_build and options.get("upload", "true") == "false":
                    continue
                label = options.get("label", "")
                condition = str(job.get("if", "")) + " " + str(step.get("if", ""))
                public_condition = str(step.get("if", job.get("if", "")))
                manual_only = isinstance(events, dict) and set(events) == {
                    "workflow_dispatch"
                }
                args = str(options.get("conda_build_args", ""))
                if is_build or is_upload:
                    if options.get("overwrite", "") not in {"", "false"} or re.search(
                        r"(?:^|\s)(?:--force|-f)(?:\s|$)",
                        str(options.get("anaconda_upload_args", "")),
                    ):
                        findings.append(
                            prefix + "immutable uploads forbid overwrite/force"
                        )
                    if label == "main" and (
                        "--no-test" in args
                        or "workflow_dispatch" in public_condition
                        or "github.event_name == 'release'" not in public_condition
                        or "direct" not in public_condition
                    ):
                        findings.append(
                            prefix + "public build requires a release-only tested route"
                        )
                    if label == "staging" and not (
                        manual_only
                        or "github.event_name == 'workflow_dispatch'" in condition
                    ):
                        findings.append(
                            prefix + "staging publication must be explicitly manual"
                        )
                    if label not in {"staging", "main"}:
                        findings.append(
                            prefix + "publisher needs a literal staging/main label"
                        )
                    if not any(
                        "candidate_sha" in str(s.get("with", {}).get("ref", ""))
                        for s in steps
                        if str(s.get("uses", "")).startswith("actions/checkout@")
                    ):
                        findings.append(
                            prefix
                            + "publisher checkout must bind an exact candidate input"
                        )
                    output = "receipt" if is_upload else "evidence_path"
                    if is_upload and any(
                        not options.get(field)
                        for field in (
                            "artifact",
                            "expected-sha256",
                            "package-spec",
                            "candidate-sha",
                        )
                    ):
                        findings.append(
                            prefix
                            + "exact-file upload needs artifact, coordinate, digest and source"
                        )
                    if (
                        is_upload
                        and label == "main"
                        and not any(
                            str(s.get("uses", "")).startswith(
                                "uibcdf/molsyssuite/.github/actions/verify-public-conda@"
                            )
                            and SHA.fullmatch(str(s["uses"]).rsplit("@", 1)[-1])
                            for s in steps
                        )
                    ):
                        findings.append(
                            prefix
                            + "exact public upload needs pinned independent public verification"
                        )
                else:
                    if (
                        not options.get("expected-sha256")
                        or not options.get("package-spec")
                        or options.get("from-label") != "staging"
                        or options.get("to-label") != "main"
                    ):
                        findings.append(
                            prefix
                            + "promotion needs an exact digest and staging/main labels"
                        )
                    if not any(
                        str(s.get("uses", "")).startswith(
                            "uibcdf/molsyssuite/.github/actions/verify-public-conda@"
                        )
                        and SHA.fullmatch(str(s["uses"]).rsplit("@", 1)[-1])
                        for s in steps
                    ):
                        findings.append(
                            prefix
                            + "promotion needs pinned independent public verification"
                        )
                    output = "receipt"
                identity = step.get("id")
                target = f"steps.{identity}.outputs.{output}" if identity else ""
                if not target or not any(
                    target in str(s.get("with", {}).get("path", ""))
                    and "always()" in str(s.get("if", ""))
                    for s in steps
                ):
                    findings.append(
                        prefix
                        + "producer/promotion evidence must be retained with always()"
                    )
            for step in steps:
                if isinstance(step, dict) and "/label/staging" in str(
                    step.get("with", {}).get("condarc", "")
                ):
                    condition = str(job.get("if", "")) + " " + str(step.get("if", ""))
                    manual_only = isinstance(events, dict) and set(events) == {
                        "workflow_dispatch"
                    }
                    if (
                        not manual_only
                        and "github.event_name == 'workflow_dispatch'" not in condition
                    ):
                        findings.append(
                            path.name
                            + ": ordinary environments must not default to staging"
                        )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path)
    parser.add_argument("--plan", type=Path)
    parser.add_argument("--evidence", type=Path)
    args = parser.parse_args()
    try:
        if args.root:
            findings = workflow_findings(args.root)
            for finding in findings:
                print(finding)
            if findings:
                return 1
        if args.plan:
            plan = tomllib.loads(args.plan.read_text(encoding="utf-8"))
            if args.evidence:
                validate_transition(
                    plan, json.loads(args.evidence.read_text(encoding="utf-8"))
                )
            else:
                validate_plan(plan)
        elif not args.root:
            raise ContractError("provide a repository root or release plan")
    except (ContractError, OSError, ValueError, yaml.YAMLError) as error:
        print(f"Conda publication contract failed: {error}")
        return 1
    print("Conda publication contract passed (administrative evidence only).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
