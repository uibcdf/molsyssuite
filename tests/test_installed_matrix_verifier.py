"""A job count cannot prove complete installed-matrix execution."""

import copy
import hashlib
import io
import json
import unittest
import zipfile
from types import SimpleNamespace
from unittest.mock import patch

from devtools.scripts import verify_installed_matrix as matrix

SHA = "a" * 40
PROFILE = {
    "platforms": ["linux-64", "win-64"],
    "python_versions": ["3.13", "3.14"],
    "prepare_job": "prepare",
    "required_steps": ["Install exact pair", "Validate installed files"],
}
RUN = {
    "id": 123,
    "run_attempt": 1,
    "head_sha": SHA,
    "path": ".github/workflows/pair.yaml",
    "display_title": "Exact pair builds",
    "status": "completed",
    "conclusion": "success",
}


def jobs(profile=PROFILE):
    result = []
    for index, name in enumerate(matrix.expected_jobs(profile)):
        result.append(
            {
                "id": index + 1,
                "name": name,
                "run_id": 123,
                "run_attempt": 1,
                "head_sha": SHA,
                "status": "completed",
                "conclusion": "success",
                "steps": [
                    {"name": step, "status": "completed", "conclusion": "success"}
                    for step in profile["required_steps"]
                ],
            }
        )
    return result


def verify(run, observed, profile=PROFILE):
    return matrix.verify_snapshot(
        run,
        observed,
        run_id=123,
        candidate=SHA,
        workflow=RUN["path"],
        title=RUN["display_title"],
        profile=profile,
    )


class InstalledMatrixTests(unittest.TestCase):
    def setUp(self):
        sleeping = patch.object(matrix, "sleep")
        sleeping.start()
        self.addCleanup(sleeping.stop)

    def test_source_gate_waits_for_pending_steps_and_preserves_complete_selection(self):
        complete = jobs()[1]
        missing = copy.deepcopy(complete)
        missing["steps"][0].update(status="pending", conclusion=None)
        with patch.object(
            matrix,
            "read_json",
            side_effect=[
                RUN,
                {"total_count": 1, "jobs": [missing]},
                RUN,
                RUN,
                {"total_count": 1, "jobs": [complete]},
                RUN,
            ],
        ):
            result = matrix.verify_native_gate(
                "uibcdf/example",
                123,
                SHA,
                RUN["path"],
                {complete["name"]: PROFILE["required_steps"]},
                "token",
                exact_jobs=True,
            )
        self.assertEqual("verified", result["state"])
        self.assertEqual([complete["id"]], [j["job_id"] for j in result["jobs"]])

    def test_one_jobs_explicit_failure_overrides_its_missing_step(self):
        observed = jobs()
        observed[-1]["steps"].pop(0)
        observed[-1]["steps"][0]["conclusion"] = "failure"
        with (
            patch.object(
                matrix,
                "read_json",
                side_effect=[RUN, {"total_count": len(observed), "jobs": observed}],
            ),
            patch.object(matrix, "sleep") as sleep,
            self.assertRaises(matrix.MatrixError) as raised,
        ):
            matrix.verify(
                "uibcdf/example",
                123,
                SHA,
                RUN["path"],
                RUN["display_title"],
                PROFILE,
                "token",
            )
        self.assertNotIsInstance(raised.exception, matrix.MetadataPending)
        sleep.assert_not_called()

    def test_completed_job_step_metadata_can_arrive_without_a_new_test_run(self):
        missing = jobs()
        missing[-1]["steps"] = []
        with (
            patch.object(
                matrix,
                "read_json",
                side_effect=[
                    RUN,
                    {"total_count": len(missing), "jobs": missing},
                    RUN,
                    RUN,
                    {"total_count": len(jobs()), "jobs": jobs()},
                    RUN,
                ],
            ) as read,
            patch.object(matrix, "sleep", create=True) as sleep,
        ):
            result = matrix.verify(
                "uibcdf/example",
                123,
                SHA,
                RUN["path"],
                RUN["display_title"],
                PROFILE,
                "token",
            )
        self.assertEqual("verified", result["state"])
        sleep.assert_called_once_with(5)
        self.assertTrue(
            all(
                "/attempts/1/jobs" in call.args[0]
                for call in read.call_args_list
                if "/jobs?" in call.args[0]
            )
        )

    def test_metadata_wait_expires_without_turning_missing_steps_into_success(self):
        missing = jobs()
        missing[-1]["steps"] = []
        with (
            patch.object(
                matrix,
                "read_json",
                side_effect=[
                    item
                    for _ in range(3)
                    for item in (
                        RUN,
                        {"total_count": len(missing), "jobs": missing},
                        RUN,
                    )
                ],
            ),
            patch.object(matrix, "sleep", create=True) as sleep,
            self.assertRaises(matrix.MatrixError) as raised,
        ):
            matrix.verify(
                "uibcdf/example",
                123,
                SHA,
                RUN["path"],
                RUN["display_title"],
                PROFILE,
                "token",
            )
        self.assertEqual("metadata_pending", raised.exception.category)
        self.assertEqual(2, sleep.call_count)

    def test_metadata_wait_rejects_reruns_and_job_replacement(self):
        for changed_run, changed_jobs in (
            (dict(RUN, run_attempt=2), jobs()),
            (RUN, [dict(j, id=j["id"] + 100) for j in jobs()]),
        ):
            missing = jobs()
            missing[-1]["steps"] = []
            with (
                self.subTest(run=changed_run, jobs=changed_jobs),
                patch.object(
                    matrix,
                    "read_json",
                    side_effect=[
                        RUN,
                        {"total_count": len(missing), "jobs": missing},
                        RUN,
                        changed_run,
                        {"total_count": len(changed_jobs), "jobs": changed_jobs},
                    ],
                ),
                patch.object(matrix, "sleep", create=True),
                self.assertRaises(matrix.MatrixError),
            ):
                matrix.verify(
                    "uibcdf/example",
                    123,
                    SHA,
                    RUN["path"],
                    RUN["display_title"],
                    PROFILE,
                    "token",
                )

    def test_explicit_failure_is_not_hidden_by_another_jobs_pending_metadata(self):
        observed = jobs()
        observed[1]["steps"] = []
        observed[-1]["steps"][-1]["conclusion"] = "failure"
        with (
            patch.object(
                matrix,
                "read_json",
                side_effect=[RUN, {"total_count": len(observed), "jobs": observed}],
            ),
            patch.object(matrix, "sleep", create=True) as sleep,
            self.assertRaises(matrix.MatrixError) as raised,
        ):
            matrix.verify(
                "uibcdf/example",
                123,
                SHA,
                RUN["path"],
                RUN["display_title"],
                PROFILE,
                "token",
            )
        self.assertNotEqual(
            "metadata_pending", getattr(raised.exception, "category", None)
        )
        sleep.assert_not_called()

    def test_corrected_workflow_requires_binding_original_source_file_matrix_attempt(
        self,
    ):
        qualification = "b" * 40
        filename, digest = "example-1.2.3-py_0.tar.bz2", "c" * 64
        run = dict(
            RUN, head_sha=qualification, display_title=f"Installed {filename} {digest}"
        )
        observed = [dict(job, head_sha=qualification) for job in jobs()]
        binding = {
            "schema": "molsyssuite.installed-source@1",
            "candidate_sha": SHA,
            "qualification_sha": qualification,
            "run_id": 123,
            "run_attempt": 1,
            "filename": filename,
            "sha256": digest,
            "profile": json.dumps(PROFILE),
        }

        def qualify(proof=binding, expected=qualification):
            return matrix.verify_snapshot(
                run,
                observed,
                run_id=123,
                candidate=SHA,
                qualification=expected,
                binding=proof,
                workflow=RUN["path"],
                title=run["display_title"],
                profile=PROFILE,
            )

        self.assertEqual(qualify()["candidate_sha"], SHA)
        self.assertEqual(qualify()["qualification_sha"], qualification)
        for field, value in (
            ("candidate_sha", qualification),
            ("qualification_sha", SHA),
            ("run_id", 456),
            ("run_attempt", 2),
            ("filename", "other.tar.bz2"),
            ("sha256", "d" * 64),
            ("profile", "{}"),
        ):
            with self.subTest(field=field), self.assertRaises(matrix.MatrixError):
                qualify(dict(binding, **{field: value}))
        with self.assertRaises(matrix.MatrixError):
            qualify(None)
        with self.assertRaises(matrix.MatrixError):
            qualify(expected="d" * 40)
        observed[0]["head_sha"] = SHA
        with self.assertRaises(matrix.MatrixError):
            qualify()

    def test_binding_acquisition_is_bounded_and_rejects_changed_archive_digest(self):
        payload = io.BytesIO()
        with zipfile.ZipFile(payload, "w") as archive:
            archive.writestr(
                "installed-source-binding.json", '{"candidate_sha":"source"}'
            )
        contents = payload.getvalue()
        artifact = {
            "id": 9,
            "name": "installed-source-binding-123-1",
            "expired": False,
            "size_in_bytes": len(contents),
            "workflow_run": {"id": 123, "head_sha": SHA},
            "digest": "sha256:" + hashlib.sha256(contents).hexdigest(),
        }
        with (
            patch.object(
                matrix,
                "read_json",
                return_value={"total_count": 1, "artifacts": [artifact]},
            ),
            patch.object(
                matrix.subprocess, "run", return_value=SimpleNamespace(stdout=contents)
            ) as read,
        ):
            self.assertEqual(
                matrix.acquire_source_binding("uibcdf/example", RUN, "token"),
                {"candidate_sha": "source"},
            )
            self.assertEqual(
                read.call_args.args[0][-1],
                "repos/uibcdf/example/actions/artifacts/9/zip",
            )
            artifact["digest"] = "sha256:" + "c" * 64
            with self.assertRaises(matrix.MatrixError):
                matrix.acquire_source_binding("uibcdf/example", RUN, "token")

    def test_source_gate_requires_executed_science_but_allows_skipped_optional_jobs(
        self,
    ):
        required = {"science": ["Run tests"]}
        science = {
            "id": 1,
            "name": "science",
            "run_id": 123,
            "run_attempt": 1,
            "head_sha": SHA,
            "status": "completed",
            "conclusion": "success",
            "steps": [
                {"name": "Run tests", "status": "completed", "conclusion": "success"}
            ],
        }
        optional = dict(science, name="conditional recovery", conclusion="skipped")

        def capture(observed, last=RUN):
            return patch.object(
                matrix,
                "read_json",
                side_effect=[
                    RUN,
                    {"total_count": len(observed), "jobs": observed},
                    last,
                ]
                * 3,
            )

        with capture([science, optional]):
            self.assertEqual(
                matrix.verify_native_gate(
                    "uibcdf/example", 123, SHA, RUN["path"], required, "token"
                )["state"],
                "verified",
            )
        for changed in (
            dict(science, conclusion="skipped"),
            dict(science, steps=[]),
            dict(science, run_attempt=2),
            dict(science, head_sha="b" * 40),
        ):
            with capture([changed, optional]), self.assertRaises(matrix.MatrixError):
                matrix.verify_native_gate(
                    "uibcdf/example", 123, SHA, RUN["path"], required, "token"
                )
        with (
            capture([science, optional], dict(RUN, run_attempt=2)),
            self.assertRaises(matrix.MatrixError),
        ):
            matrix.verify_native_gate(
                "uibcdf/example", 123, SHA, RUN["path"], required, "token"
            )

    def test_other_component_job_templates_are_supported_without_repo_names(self):
        profile = dict(PROFILE, job_template="Installed {python} on {platform}")
        self.assertEqual(verify(RUN, jobs(profile), profile)["state"], "verified")

    def test_four_and_five_platform_profiles_are_verified_by_cells(self):
        for platforms in (
            ["linux-64", "linux-aarch64", "osx-arm64", "win-64"],
            ["linux-64", "linux-aarch64", "osx-64", "osx-arm64", "win-64"],
        ):
            profile = dict(
                PROFILE,
                platforms=platforms,
                python_versions=["3.11", "3.12", "3.13", "3.14"],
            )
            self.assertEqual(verify(RUN, jobs(profile), profile)["state"], "verified")

    def test_equal_job_count_with_missing_or_duplicate_cell_fails(self):
        observed = jobs()
        observed[-1]["name"] = observed[-2]["name"]
        with self.assertRaises(matrix.MatrixError):
            verify(RUN, observed)
        observed[-1]["name"] = "unrelated successful job"
        with self.assertRaises(matrix.MatrixError):
            verify(RUN, observed)

    def test_successful_run_cannot_hide_skipped_or_failed_cells_and_steps(self):
        for conclusion in ("skipped", "failure", "cancelled"):
            observed = jobs()
            observed[-1]["conclusion"] = conclusion
            with self.assertRaises(matrix.MatrixError):
                verify(RUN, observed)
            observed = jobs()
            observed[-1]["steps"][-1]["conclusion"] = conclusion
            with self.assertRaises(matrix.MatrixError):
                verify(RUN, observed)
        observed = jobs()
        observed[-1]["steps"].pop()
        with self.assertRaises(matrix.MatrixError):
            verify(RUN, observed)

    def test_mixed_source_or_attempt_and_wrong_pair_title_fail(self):
        for field, value in (
            ("head_sha", "b" * 40),
            ("run_attempt", 2),
            ("run_id", 456),
        ):
            observed = jobs()
            observed[-1][field] = value
            with self.assertRaises(matrix.MatrixError):
                verify(RUN, observed)
        for field, value in (
            ("display_title", "other pair"),
            ("path", ".github/workflows/other.yaml"),
        ):
            with self.assertRaises(matrix.MatrixError):
                verify(dict(RUN, **{field: value}), jobs())

    def test_incomplete_inventory_and_rerun_race_fail_closed(self):
        for document, last in (
            ({"total_count": 100, "jobs": jobs()}, RUN),
            ({"total_count": len(jobs()), "jobs": jobs()}, dict(RUN, run_attempt=2)),
        ):
            with (
                patch.object(
                    matrix,
                    "read_json",
                    side_effect=[copy.deepcopy(RUN), document, last],
                ),
                self.assertRaises(matrix.MatrixError),
            ):
                matrix.verify(
                    "uibcdf/example",
                    123,
                    SHA,
                    RUN["path"],
                    RUN["display_title"],
                    PROFILE,
                    "token",
                )

    def test_native_acquisition_is_attempt_bound_and_read_only(self):
        with patch.object(
            matrix,
            "read_json",
            side_effect=[RUN, {"total_count": len(jobs()), "jobs": jobs()}, RUN],
        ) as read:
            result = matrix.verify(
                "uibcdf/example",
                123,
                SHA,
                RUN["path"],
                RUN["display_title"],
                PROFILE,
                "token",
            )
        self.assertEqual(result["state"], "verified")
        self.assertIn("/attempts/1/jobs?per_page=100", read.call_args_list[1].args[0])
