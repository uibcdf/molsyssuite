"""Reject unsafe routes, incomplete immutable inventories and weakened controls."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError

import tomllib

from devtools.scripts import conda_release_contract as contract
from devtools.scripts import preflight_conda_release as preflight

ROOT = Path(__file__).resolve().parents[1]
SHA = "a" * 40


def plan(route="staged", profile="noarch-python"):
    return {
        "schema": "molsyssuite.conda-plan@1",
        "package": "example",
        "version": "1.2.3",
        "build_number": 2,
        "route": route,
        "profile": profile,
        "reason": "Reviewed candidate",
        "decision_by": "Maintainers 2026-10-01",
        "artifact_subdirs": ["noarch"],
        "test_platforms": ["linux-64", "win-64"],
        "python_versions": ["3.13", "3.14"],
        "required_workflows": [".github/workflows/CI_full_matrix.yaml"],
        "requires_installed_gate": route == "staged",
        "new_compatibility_surface": False,
        "coupled_release": False,
        "dependencies_public": True,
    }


def evidence(decision):
    inventory = [
        {
            "package": "example",
            "version": "1.2.3",
            "subdir": subdir,
            "filename": "example-1.2.3-py_2.tar.bz2",
            "sha256": "b" * 64,
        }
        for subdir in decision["artifact_subdirs"]
    ]
    return {
        "candidate_sha": SHA,
        "checkout_sha": SHA,
        "tag_sha": SHA,
        "version": "1.2.3",
        "route": decision["route"],
        "event": "release",
        "gates": [
            {
                "workflow": decision["required_workflows"][0],
                "candidate_sha": SHA,
                "conclusion": "success",
                "run_id": 1,
            }
        ],
        "preflight": {
            "state": "absent",
            "http_status": 404,
            "scope": "all-labels",
            "checked_at": "2026-10-01T00:00:00Z",
        },
        "producer_receipt": {
            "state": "verified",
            "inventory": inventory,
            "candidate_sha": SHA,
            "recipe_tests": "success",
        },
        "promotion_receipt": {
            "state": "verified",
            "from_label": "staging",
            "to_label": "main",
            "inventory": inventory,
            "candidate_sha": SHA,
        },
        "inventory": inventory,
        "public": {
            "schema": "molsyssuite.public-conda@1",
            "state": "verified",
            "files": [
                dict(item, main_label="verified", solver_index="verified")
                for item in inventory
            ],
        },
        "installed_cells": [
            {
                "platform": platform,
                "python": python,
                "conclusion": "success",
                "candidate_sha": SHA,
                "installed_inventory": inventory,
            }
            for platform in decision["test_platforms"]
            for python in decision["python_versions"]
        ],
    }


WORKFLOW = """on:
  release:
    types: [released]
  workflow_dispatch:
jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ inputs.candidate_sha || github.event.release.tag_name }}
      - uses: mamba-org/setup-micromamba@v3.2.1
        with:
          condarc: 'channels: [uibcdf, conda-forge]'
      - id: staging
        if: github.event_name == 'workflow_dispatch'
        uses: uibcdf/action-build-and-upload-conda-packages@v2.2.2
        with:
          label: staging
      - id: public
        if: github.event_name == 'release' && steps.route.outputs.route == 'direct'
        uses: uibcdf/action-build-and-upload-conda-packages@v2.2.2
        with:
          label: main
      - if: always()
        uses: actions/upload-artifact@v4
        with:
          path: ${{ steps.staging.outputs.evidence_path }}
      - if: always()
        uses: actions/upload-artifact@v4
        with:
          path: ${{ steps.public.outputs.evidence_path }}
"""


class CondaReleaseContractTests(unittest.TestCase):
    def test_green_probe_cannot_replace_a_completed_scientific_gate(self):
        workflow = plan()["required_workflows"][0]
        runs = [
            {
                "id": number,
                "head_sha": SHA,
                "status": "completed",
                "conclusion": "success",
                "path": workflow,
            }
            for number in (124, 123)
        ]
        requirements = {workflow: {"science": ["Run tests"]}}
        with (
            patch.object(preflight, "read_json", return_value={"workflow_runs": runs}),
            patch.object(
                preflight,
                "verify_native_gate",
                side_effect=[
                    preflight.MatrixError("science skipped"),
                    {"state": "verified"},
                ],
            ),
        ):
            proof = preflight.acquire_gates(
                "uibcdf/example", SHA, [workflow], "token", requirements
            )
            self.assertEqual(proof[0]["run_id"], 123)
        with (
            patch.object(preflight, "read_json", return_value={"workflow_runs": runs}),
            patch.object(
                preflight,
                "verify_native_gate",
                side_effect=preflight.MatrixError("science skipped"),
            ),
            self.assertRaises(contract.ContractError),
        ):
            preflight.acquire_gates(
                "uibcdf/example", SHA, [workflow], "token", requirements
            )

    def test_explicit_job_plan_requires_bound_execution_proof(self):
        decision = plan("direct")
        workflow = decision["required_workflows"][0]
        decision["gate_jobs"] = {workflow: {"science": ["Run tests"]}}
        proof = evidence(decision)
        with self.assertRaises(contract.ContractError):
            contract.validate_transition(decision, proof)
        proof["gates"][0]["executed_jobs"] = {
            "schema": "molsyssuite.native-gate@1",
            "state": "verified",
            "candidate_sha": SHA,
            "workflow": workflow,
            "run_id": 1,
            "run_attempt": 1,
            "jobs": [{"name": "science", "required_steps": ["Run tests"]}],
        }
        contract.validate_transition(decision, proof)
        proof["gates"][0]["executed_jobs"]["jobs"][0]["required_steps"] = []
        with self.assertRaises(contract.ContractError):
            contract.validate_transition(decision, proof)

    def test_shared_noarch_wrappers_and_provider_controls_are_audited(self):
        text = (
            """on:
  workflow_dispatch:
jobs:
  publish:
    uses: uibcdf/molsyssuite/.github/workflows/publish-noarch-conda.yaml@"""
            + "a" * 40
            + """
    with:
      candidate_sha: ${{ inputs.candidate_sha }}
      version: ${{ inputs.version }}
    secrets:
      ANACONDA_TOKEN: ${{ secrets.ANACONDA_TOKEN }}
"""
        )
        self.assertEqual(self.findings(text), [])
        for altered in (
            text.replace("@" + "a" * 40, "@main"),
            text.replace("      candidate_sha: ${{ inputs.candidate_sha }}\n", ""),
            text.replace(
                "    secrets:\n      ANACONDA_TOKEN: ${{ secrets.ANACONDA_TOKEN }}",
                "    secrets: inherit",
            ),
        ):
            self.assertTrue(self.findings(altered))
        self.assertEqual(contract.workflow_findings(ROOT), [])

    def test_valid_direct_and_staged_profiles(self):
        for route in ("direct", "staged"):
            for profile in ("noarch-python", "metapackage", "native-abi3"):
                decision = plan(route, profile)
                if profile == "native-abi3":
                    decision["artifact_subdirs"] = ["linux-64", "win-64"]
                contract.validate_transition(decision, evidence(decision))

    def test_template_is_versioned_and_valid(self):
        contract.validate_plan(
            tomllib.loads(
                (ROOT / "devguide/templates/conda_release_plan.toml").read_text()
            )
        )

    def test_direct_route_rejects_every_staging_condition(self):
        for field, value in (
            ("requires_installed_gate", True),
            ("new_compatibility_surface", True),
            ("coupled_release", True),
            ("dependencies_public", False),
        ):
            decision = plan("direct")
            decision[field] = value
            with self.assertRaises(contract.ContractError):
                contract.validate_plan(decision)

    def test_direct_route_rejects_occupied_or_inconclusive_registry(self):
        decision = plan("direct")
        for absence_proof in (
            {},
            {
                "state": "occupied",
                "http_status": 200,
                "scope": "all-labels",
                "checked_at": "now",
            },
            {
                "state": "absent",
                "http_status": 503,
                "scope": "all-labels",
                "checked_at": "now",
            },
            {
                "state": "absent",
                "http_status": 404,
                "scope": "main",
                "checked_at": "now",
            },
        ):
            proof = evidence(decision)
            proof["preflight"] = absence_proof
            with self.assertRaises(contract.ContractError):
                contract.validate_transition(decision, proof)

    def test_mutable_or_mismatched_candidate_never_passes(self):
        decision = plan()
        for changed in (
            {"candidate_sha": "main"},
            {"checkout_sha": "c" * 40},
            {"tag_sha": "d" * 40},
        ):
            proof = dict(evidence(decision), **changed)
            with self.assertRaises(contract.ContractError):
                contract.validate_transition(decision, proof)

    def test_missing_or_failed_native_gate_never_passes(self):
        decision = plan()
        for changed in (
            {"conclusion": "failure"},
            {"candidate_sha": "c" * 40},
            {"run_id": 0},
        ):
            proof = evidence(decision)
            proof["gates"][0].update(changed)
            with self.assertRaises(contract.ContractError):
                contract.validate_transition(decision, proof)
        proof = evidence(decision)
        proof["gates"] = []
        with self.assertRaises(contract.ContractError):
            contract.validate_transition(decision, proof)

    def test_public_no_test_overwrite_and_rebuild_are_rejected(self):
        for route in ("direct", "staged"):
            decision = plan(route)
            for changed in (
                {"overwrite": True},
                {"no_test": True},
                {"event": "workflow_dispatch"}
                if route == "direct"
                else {"rebuild": True},
            ):
                with self.assertRaises(contract.ContractError):
                    contract.validate_transition(
                        decision, dict(evidence(decision), **changed)
                    )

    def test_producer_receipt_and_public_poststate_are_independent_requirements(self):
        for route, field in (
            ("direct", "producer_receipt"),
            ("staged", "promotion_receipt"),
            ("direct", "public"),
            ("staged", "public"),
        ):
            decision = plan(route)
            proof = evidence(decision)
            proof[field] = {"state": "failed"}
            with self.assertRaises(contract.ContractError):
                contract.validate_transition(decision, proof)
        for route, field in (
            ("direct", "producer_receipt"),
            ("staged", "promotion_receipt"),
        ):
            proof = evidence(plan(route))
            proof[field]["inventory"] = []
            with self.assertRaises(contract.ContractError):
                contract.validate_transition(plan(route), proof)
        proof = evidence(plan("direct"))
        proof["producer_receipt"]["recipe_tests"] = "skipped"
        with self.assertRaises(contract.ContractError):
            contract.validate_transition(plan("direct"), proof)

    def test_native_platform_and_installed_cell_omissions_fail(self):
        decision = plan(profile="native-abi3")
        decision["artifact_subdirs"] = ["linux-64", "win-64"]
        for field in ("inventory", "installed_cells"):
            proof = evidence(decision)
            proof[field].pop()
            with self.assertRaises(contract.ContractError):
                contract.validate_transition(decision, proof)
        proof = evidence(decision)
        proof["installed_cells"][0]["installed_inventory"] = []
        with self.assertRaises(contract.ContractError):
            contract.validate_transition(decision, proof)

    def test_coupled_pair_needs_exact_counterpart_in_every_installed_cell(self):
        decision = plan()
        decision["coupled_release"] = True
        proof = evidence(decision)
        with self.assertRaises(contract.ContractError):
            contract.validate_transition(decision, proof)
        proof["pair_inventory"] = proof["inventory"] + [
            {
                "package": "counterpart",
                "version": "2.0.0",
                "subdir": "noarch",
                "filename": "counterpart-2.0.0-py_0.tar.bz2",
                "sha256": "c" * 64,
            }
        ]
        for cell in proof["installed_cells"]:
            cell["installed_inventory"] = proof["pair_inventory"]
        contract.validate_transition(decision, proof)
        proof["installed_cells"][0]["installed_inventory"] = proof["inventory"]
        with self.assertRaises(contract.ContractError):
            contract.validate_transition(decision, proof)

    def findings(self, text):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / ".github/workflows/publish.yaml"
            path.parent.mkdir(parents=True)
            path.write_text(text)
            return contract.workflow_findings(root)

    def test_guard_preserves_eligible_automatic_release_and_manual_staging(self):
        self.assertEqual(self.findings(WORKFLOW), [])
        # A job admits both events, but its public step remains release-only.
        text = WORKFLOW.replace(
            "    runs-on: ubuntu-latest",
            "    if: github.event_name == 'workflow_dispatch' || !startsWith(github.event.release.tag_name, 'policy-v')\n    runs-on: ubuntu-latest",
        )
        self.assertEqual(self.findings(text), [])

    def test_guard_rejects_public_no_test_manual_main_and_force_retry(self):
        for change in (
            "          label: main\n          conda_build_args: --no-test\n",
            "          label: main\n          overwrite: true\n",
        ):
            self.assertTrue(
                self.findings(WORKFLOW.replace("          label: main\n", change))
            )
        self.assertTrue(
            self.findings(
                WORKFLOW.replace(
                    "github.event_name == 'release'",
                    "github.event_name == 'workflow_dispatch'",
                )
            )
        )

    def test_guard_rejects_mutable_checkout_or_action_and_missing_receipts(self):
        for text in (
            WORKFLOW.replace(
                "${{ inputs.candidate_sha || github.event.release.tag_name }}", "main"
            ),
            WORKFLOW.replace("@v2.2.2", "@main"),
            WORKFLOW.replace("if: always()", "if: success()"),
        ):
            self.assertTrue(self.findings(text))

    def test_guard_rejects_default_staging_channels(self):
        self.assertTrue(
            self.findings(
                WORKFLOW.replace(
                    "[uibcdf, conda-forge]", "[uibcdf/label/staging, conda-forge]"
                )
            )
        )

    def test_guard_does_not_treat_build_only_jobs_as_publishers(self):
        text = WORKFLOW.replace(
            "          label: main", "          upload: false\n          label: ignored"
        ).replace("@v2.2.2", "@v2.2.2")
        self.assertEqual(self.findings(text), [])

    def test_native_gate_acquisition_rejects_wrong_sha_and_failure(self):
        workflow = ".github/workflows/CI_full_matrix.yaml"
        valid = {
            "id": 123,
            "head_sha": SHA,
            "status": "completed",
            "conclusion": "success",
            "path": workflow,
        }
        for changed in (
            {"head_sha": "c" * 40},
            {"conclusion": "failure"},
            {"path": ".github/workflows/other.yaml"},
        ):
            with (
                patch.object(
                    preflight,
                    "read_json",
                    return_value={"workflow_runs": [dict(valid, **changed)]},
                ),
                self.assertRaises(contract.ContractError),
            ):
                preflight.acquire_gates(
                    "uibcdf/example", SHA, [workflow], "read-only-token"
                )
        with patch.object(
            preflight, "read_json", return_value={"workflow_runs": [valid]}
        ):
            self.assertEqual(
                preflight.acquire_gates(
                    "uibcdf/example", SHA, [workflow], "read-only-token"
                )[0]["run_id"],
                123,
            )

    def test_actual_preflight_requires_conclusive_all_label_absence(self):
        for response in (
            {"distributions": [{"labels": ["staging"]}]},
            {},
            {"distributions": []},
        ):
            with (
                patch.object(preflight, "read_json", return_value=response),
                self.assertRaises(contract.ContractError),
            ):
                preflight.acquire_absence("uibcdf", "example", "1.2.3")
        for code in (403, 429, 500):
            with (
                patch.object(
                    preflight,
                    "read_json",
                    side_effect=HTTPError(
                        "https://api.anaconda.org", code, "unavailable", {}, None
                    ),
                ),
                self.assertRaises(contract.ContractError),
            ):
                preflight.acquire_absence("uibcdf", "example", "1.2.3")
        with patch.object(
            preflight,
            "read_json",
            side_effect=HTTPError("https://api.anaconda.org", 404, "absent", {}, None),
        ):
            result = preflight.acquire_absence("uibcdf", "example", "1.2.3")
            self.assertEqual(result["scope"], "all-labels")
            self.assertTrue(result["checked_at"])

    def test_manual_direct_preflight_never_queries_registry_or_authorizes_main(self):
        with patch.object(preflight, "acquire_absence") as query:
            with self.assertRaises(contract.ContractError):
                preflight.preflight(
                    plan("direct"),
                    "uibcdf/example",
                    SHA,
                    SHA,
                    None,
                    "workflow_dispatch",
                    "token",
                )
            query.assert_not_called()

    def test_successful_preflight_binds_exact_source_gates_and_registry(self):
        with (
            patch.object(
                preflight,
                "acquire_gates",
                return_value=evidence(plan("direct"))["gates"],
            ),
            patch.object(
                preflight,
                "acquire_absence",
                return_value=evidence(plan("direct"))["preflight"],
            ),
        ):
            result = preflight.preflight(
                plan("direct"), "uibcdf/example", SHA, SHA, SHA, "release", "token"
            )
        self.assertEqual(result["candidate_sha"], SHA)
        self.assertEqual(result["tag_sha"], SHA)
        self.assertEqual(result["preflight"]["http_status"], 404)
