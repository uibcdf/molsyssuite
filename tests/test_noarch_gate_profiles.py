"""Additional evidence cannot bypass the owner guard or change producer bytes."""

import copy
import hashlib
import json
import unittest
from unittest.mock import patch

from devtools.scripts import noarch_release as release
from devtools.scripts import verify_installed_matrix as matrix
from tests import test_noarch_release as fixtures


class AdditionalGateTests(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.NoarchReleaseTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.root, self.plan = self.fixture.root, self.fixture.plan
        self.workflow = ".github/workflows/promote.yaml"
        self.core_workflow = ".github/workflows/core.yaml"
        fields = [
            "candidate_sha",
            "version",
            "sha256",
            "installed_run_id",
            "qualification_sha",
        ]
        self.document = {
            "on": {
                "workflow_dispatch": {
                    "inputs": {
                        **{name: {"required": True} for name in fields},
                        "core_run_id": {"required": True, "type": "string"},
                    }
                }
            },
            "jobs": {
                "release": {
                    "steps": [
                        {
                            "name": "Verify core",
                            "env": {"CORE_RUN_ID": "${{ inputs.core_run_id }}"},
                            "run": "owner verifier",
                        }
                    ]
                },
                "promote": {
                    "needs": "release",
                    "uses": "uibcdf/molsyssuite/.github/workflows/promote-noarch-conda.yaml@"
                    + fixtures.SOURCE,
                    "with": {name: "${{ inputs." + name + " }}" for name in fields},
                },
            },
        }
        self.profile = {
            "name": "example-core",
            "repository": fixtures.REPOSITORY,
            "owner-issue": fixtures.REPOSITORY + "#1",
            "reviewed-source": fixtures.QUALIFICATION,
            "caller": self.workflow,
            "promotion-job": "promote",
            "caller-inputs": {},
            "producer-inputs": {
                self.core_workflow: hashlib.sha256(b"core workflow").hexdigest()
            },
            "gates": [
                {
                    "input": "core_run_id",
                    "guard-job": "release",
                    "guard-step": "Verify core",
                    "guard-env": "CORE_RUN_ID",
                    "workflow": self.core_workflow,
                    "title-template": "Core installed {filename} {sha256}",
                    "job-template": "Core {runner} / Python {python}",
                    "required-steps": ["Verify core installed"],
                    "runners": {
                        "linux-64": "ubuntu-latest",
                        "osx-arm64": "macos-latest",
                    },
                }
            ],
        }
        self.run = dict(
            fixtures.RUN,
            id=789,
            head_sha=fixtures.SOURCE,
            path=self.core_workflow,
            display_title=f"Core installed {fixtures.COORDINATE['filename']} {fixtures.DIGEST}",
        )
        self.jobs = [
            dict(
                self.run,
                id=index + 10,
                run_id=789,
                name=f"Core {runner} / Python {minor}",
                steps=[
                    {
                        "name": "Verify core installed",
                        "status": "completed",
                        "conclusion": "success",
                    }
                ],
            )
            for index, (runner, minor) in enumerate(
                (runner, minor)
                for runner in ("ubuntu-latest", "macos-latest")
                for minor in self.plan["python_versions"]
            )
        ]

    def handoff(self, failure=None, *, promotion_source=None, public=False):
        document, profile = copy.deepcopy(self.document), copy.deepcopy(self.profile)
        run, jobs = copy.deepcopy(self.run), copy.deepcopy(self.jobs)
        if failure == "dependency":
            document["jobs"]["promote"].pop("needs")
        if failure == "guard_skip":
            document["jobs"]["release"]["if"] = "false"
        if failure == "tolerated_guard":
            document["jobs"]["release"]["continue-on-error"] = True
        if failure == "input_not_consumed":
            document["jobs"]["release"]["steps"][0]["env"] = {}
        blob = json.dumps(document).encode()
        profile["caller-inputs"][self.workflow] = hashlib.sha256(blob).hexdigest()
        if failure == "source_drift":
            profile["caller-inputs"][self.workflow] = "0" * 64
        if failure == "forbidden_ref":
            profile["workflow-refs"] = ["main"]
        if failure == "wrong_file":
            run["display_title"] = "Core installed wrong-file " + fixtures.DIGEST
        if failure == "wrong_source":
            run["head_sha"] = fixtures.QUALIFICATION
        if failure == "wrong_workflow":
            run["path"] = ".github/workflows/other.yaml"
        if failure == "wrong_event":
            run["event"] = "pull_request"
        if failure == "skipped_test":
            jobs[0]["steps"][0]["conclusion"] = "skipped"
        if failure == "incomplete":
            jobs.pop()
        if failure == "extra_job":
            jobs.append(dict(jobs[0], name="Unreviewed cell"))
        if failure == "wrong_attempt":
            jobs[0]["run_attempt"] = 2
        if failure == "reserved_input":
            profile["gates"][0]["input"] = "candidate_sha"
        assignments = {"core_run_id": 789}
        if failure == "missing_input":
            assignments = {}
        a, b, c, d, e = self.fixture.capture()
        with (
            a,
            b,
            c as git,
            d,
            e as registry,
            patch.object(release, "load_gate_profile", return_value=profile),
            patch.object(
                release.subprocess,
                "check_output",
                side_effect=lambda command, **kwargs: (
                    blob if command[-1].endswith(self.workflow) else b"core workflow"
                ),
            ),
            patch.object(
                release,
                "read_json",
                return_value={
                    "sha": "f" * 40
                    if failure == "moved_promotion_ref"
                    else promotion_source or fixtures.QUALIFICATION
                },
            ),
            patch.object(
                release, "verify", return_value={"state": "verified"}
            ) as installed,
            patch.object(release, "verify_public", return_value="https://public/file"),
            patch.object(
                matrix, "acquire_snapshot", return_value=(run, jobs, "core-url")
            ),
            patch.object(matrix, "check_snapshot_stable") as stable,
            patch.object(
                release, "dispatch_arguments", wraps=release.dispatch_arguments
            ) as command,
        ):
            git.side_effect = lambda root, *args: (
                fixtures.SOURCE
                if args[0] == "rev-parse"
                else json.dumps(document)
                if args[0] == "show"
                else ""
            )
            if failure == "rerun":
                stable.side_effect = matrix.MatrixError(
                    "native source facts changed during acquisition"
                )
            arguments = {
                "token": "token",
                "qualification_sha": fixtures.QUALIFICATION,
                "workflow_ref": "qualify/1.2.3",
                "installed_run_id": 456,
                "promotion_workflow": self.workflow,
                "gate_profile": "example-core",
                "gate_runs": assignments,
                "promotion_sha": promotion_source,
            }
            if public:
                registry.return_value = {"labels": ["staging", "main"]}
            if failure:
                with self.assertRaises(ValueError):
                    release.prepare_handoff(
                        self.root, fixtures.REPOSITORY, 123, **arguments
                    )
                command.assert_not_called()
                return
            result = release.prepare_handoff(
                self.root, fixtures.REPOSITORY, 123, **arguments
            )
            self.assertEqual(result["additional_gates"]["state"], "verified")
            self.assertEqual(
                result["additional_gates"]["promotion_sha"],
                promotion_source or fixtures.QUALIFICATION,
            )
            self.assertEqual(installed.call_args.args[-1], fixtures.QUALIFICATION)
            git.assert_any_call(
                self.root,
                "show",
                f"{promotion_source or fixtures.QUALIFICATION}:{self.workflow}",
            )
            if promotion_source:
                self.assertNotIn(
                    unittest.mock.call(
                        self.root, "show", f"{fixtures.QUALIFICATION}:{self.workflow}"
                    ),
                    git.call_args_list,
                )
            if public:
                self.assertEqual(result["state"], "public-verified")
                self.assertIsNone(result["next_command"])
                command.assert_not_called()
                return
            self.assertIn("core_run_id=789", result["next_command"])
            self.assertIn("candidate_sha=" + fixtures.SOURCE, result["next_command"])
            self.assertIn("sha256=" + fixtures.DIGEST, result["next_command"])
            self.assertIn(
                "qualification_sha=" + fixtures.QUALIFICATION, result["next_command"]
            )
            self.assertFalse(result["mutation_performed"])

    def test_complete_guarded_handoff_preserves_original_source_file_and_repair(self):
        self.handoff()

    def test_invalid_gate_never_emits_a_dispatch_command(self):
        for failure in (
            "dependency",
            "guard_skip",
            "tolerated_guard",
            "input_not_consumed",
            "source_drift",
            "wrong_file",
            "wrong_source",
            "wrong_workflow",
            "wrong_event",
            "skipped_test",
            "incomplete",
            "extra_job",
            "wrong_attempt",
            "reserved_input",
            "missing_input",
            "rerun",
            "forbidden_ref",
        ):
            with self.subTest(failure=failure):
                self.handoff(failure)

    def test_promoter_commit_is_independent_of_installed_repair_identity(self):
        self.handoff(promotion_source="e" * 40)
        self.handoff("moved_promotion_ref", promotion_source="e" * 40)

    def test_qualified_public_file_never_prepares_another_promotion(self):
        self.handoff(promotion_source="e" * 40, public=True)

    def test_default_profile_is_explicit_and_repository_scoped(self):
        self.assertEqual(
            release.load_gate_profile(
                release.GATE_PROFILES, "argdigest-core", "uibcdf/argdigest"
            )["owner-issue"],
            "uibcdf/argdigest#24",
        )
        for name, repository in (
            ("unknown", "uibcdf/argdigest"),
            ("argdigest-core", "uibcdf/example"),
        ):
            with (
                self.subTest(name=name, repository=repository),
                self.assertRaises(ValueError),
            ):
                release.load_gate_profile(release.GATE_PROFILES, name, repository)

    def test_extra_arguments_without_profile_are_not_accepted(self):
        a, b, c, d, e = self.fixture.capture()
        with a, b, c, d, e, self.assertRaisesRegex(ValueError, "explicit reviewed"):
            release.prepare_handoff(
                self.root,
                fixtures.REPOSITORY,
                123,
                token="token",
                gate_runs={"core_run_id": 789},
            )

    def test_reviewed_profile_revision_preserves_the_legacy_source_binding(self):
        legacy = release.load_gate_profile(
            release.GATE_PROFILES, "argdigest-core", "uibcdf/argdigest"
        )
        revised = release.load_gate_profile(
            release.GATE_PROFILES, "argdigest-core-v2", "uibcdf/argdigest"
        )
        probe = "devtools/conda-build/core_runtime_probe.py"
        self.assertEqual(
            legacy["producer-inputs"][probe],
            "948d4d8c5d36412afef05a6164b968563708bfcb9339dcf460df8d988219d027",
        )
        self.assertEqual(
            revised["producer-inputs"][probe],
            "61d99d59322c89ed8b134d0cd07904a4f7e3fd0c08071e06faea3b1260bd9121",
        )
        self.assertEqual(legacy["caller-inputs"], revised["caller-inputs"])
        self.assertEqual(legacy["gates"], revised["gates"])
        self.assertEqual(
            {
                key: value
                for key, value in legacy["producer-inputs"].items()
                if key != probe
            },
            {
                key: value
                for key, value in revised["producer-inputs"].items()
                if key != probe
            },
        )
        with self.assertRaisesRegex(ValueError, "another owner"):
            release.load_gate_profile(
                release.GATE_PROFILES, "argdigest-core-v2", "uibcdf/example"
            )
