"""Reject mixed source/file evidence and prepare existing callers without mutation."""

import copy
import hashlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from types import SimpleNamespace
from unittest.mock import patch

from devtools.scripts import _release_artifacts as artifacts
from devtools.scripts import noarch_release as release
from tests import test_noarch_conda as fixtures

SOURCE = "a" * 40
QUALIFICATION = "b" * 40
DIGEST = "c" * 64
REPOSITORY = "uibcdf/example"
RUN = {
    "id": 123,
    "run_attempt": 1,
    "head_sha": "d" * 40,
    "event": "workflow_dispatch",
    "status": "completed",
    "conclusion": "success",
}
COORDINATE = {
    "owner": "uibcdf",
    "package": "example",
    "version": "1.2.3",
    "subdir": "noarch",
    "filename": "example-1.2.3-py_2.tar.bz2",
}
STEPS = [
    "Acquire exact-source executed CI gates and route preflight",
    "Build once and run recipe tests without uploading or conversion",
    "Inspect exact built metadata, embedded version and resources",
    "Upload exact reviewed file to staging",
    "Retain candidate, producer and independent receipts",
]


class NoarchReleaseTests(unittest.TestCase):
    def setUp(self):
        fixture = fixtures.NoarchCondaTests()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        self.root = fixture.root
        self.plan, self.inventory = fixture.inspect()
        self.receipts = {
            "component/noarch-preflight.json": {
                "schema": "molsyssuite.conda-preflight@1",
                "candidate_sha": SOURCE,
                "checkout_sha": SOURCE,
                "event": "workflow_dispatch",
                "package": "example",
                "version": "1.2.3",
                "route": "staged",
            },
            "component/noarch-artifact.json": dict(
                COORDINATE, build_number=2, route="staged", sha256=DIGEST
            ),
            "_temp/conda-upload-receipt.json": {
                "schema": "uibcdf.conda-upload@1",
                "state": "verified",
                "label": "staging",
                "candidate_sha": SOURCE,
                "coordinate": COORDINATE,
                "sha256": DIGEST,
                "subject": {
                    "repository": REPOSITORY,
                    "run_id": "123",
                    "run_attempt": "1",
                },
            },
        }
        self.jobs = [
            dict(
                RUN,
                run_id=123,
                name="publish / publish",
                steps=[
                    {"name": name, "status": "completed", "conclusion": "success"}
                    for name in STEPS
                ],
            )
        ]

    def test_native_workflow_head_does_not_replace_original_producer(self):
        result = release.bind_producer(
            REPOSITORY, RUN, self.jobs, self.receipts, self.plan
        )
        self.assertEqual(result["candidate_sha"], SOURCE)
        self.assertNotEqual(result["candidate_sha"], RUN["head_sha"])

    def test_changed_upload_identity_and_unverified_receipts_fail_closed(self):
        for field, value in (
            ("candidate_sha", QUALIFICATION),
            ("sha256", "f" * 64),
            ("state", "unverified"),
            ("label", "main"),
            ("coordinate", dict(COORDINATE, filename="other.tar.bz2")),
            (
                "subject",
                {"repository": REPOSITORY, "run_id": "123", "run_attempt": "2"},
            ),
        ):
            with self.subTest(field=field), self.assertRaises(release.ContractError):
                receipts = copy.deepcopy(self.receipts)
                receipts["_temp/conda-upload-receipt.json"][field] = value
                release.bind_producer(REPOSITORY, RUN, self.jobs, receipts, self.plan)

    def test_skipped_native_build_or_changed_attempt_is_rejected(self):
        for field, value in (("run_attempt", 2), ("head_sha", SOURCE)):
            jobs = copy.deepcopy(self.jobs)
            jobs[0][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                release.bind_producer(REPOSITORY, RUN, jobs, self.receipts, self.plan)
        self.jobs[0]["steps"][1]["conclusion"] = "skipped"
        with self.assertRaises(ValueError):
            release.bind_producer(REPOSITORY, RUN, self.jobs, self.receipts, self.plan)

    def test_duplicate_inspection_receipts_are_ambiguous(self):
        self.receipts["other/noarch-artifact.json"] = self.receipts[
            "component/noarch-artifact.json"
        ]
        with self.assertRaises(release.ContractError):
            release.bind_producer(REPOSITORY, RUN, self.jobs, self.receipts, self.plan)

    def capture(self):
        return (
            patch.object(
                release, "acquire_snapshot", return_value=(RUN, self.jobs, "native-url")
            ),
            patch.object(
                release,
                "acquire_json_artifact",
                return_value=(self.receipts, {"id": 8}),
            ),
            patch.object(
                release,
                "git",
                side_effect=lambda root, *args: (
                    SOURCE if args[0] == "rev-parse" else ""
                ),
            ),
            patch.object(release, "check_snapshot_stable"),
            patch.object(
                release, "registered_file", return_value={"labels": ["staging"]}
            ),
        )

    def test_existing_public_file_emits_no_mutating_command(self):
        a, b, c, d, e = self.capture()
        with (
            a,
            b,
            c,
            d,
            e,
            patch.object(
                release, "verify", return_value={"state": "verified"}
            ) as installed,
            patch.object(release, "verify_public", return_value="https://public/file"),
        ):
            result = release.prepare_handoff(
                self.root,
                REPOSITORY,
                123,
                token="token",
                qualification_sha=QUALIFICATION,
                installed_run_id=456,
                public=True,
            )
        self.assertEqual(result["state"], "public-verified")
        self.assertIsNone(result["next_command"])
        self.assertFalse(result["mutation_performed"])
        self.assertEqual(installed.call_args.args[2], SOURCE)
        self.assertEqual(installed.call_args.args[-1], QUALIFICATION)

    def test_qualification_command_uses_filename_and_original_source(self):
        a, b, c, d, e = self.capture()
        with (
            a,
            b,
            c,
            d,
            e,
            patch.object(release, "read_json", return_value={"sha": QUALIFICATION}),
            patch.object(release, "caller", return_value="reviewed-caller"),
        ):
            result = release.prepare_handoff(
                self.root,
                REPOSITORY,
                123,
                token="token",
                qualification_sha=QUALIFICATION,
                workflow_ref="qualify/1.2.3",
            )
        command = result["next_command"]
        self.assertIn("candidate_sha=" + SOURCE, command)
        self.assertIn("filename=" + COORDINATE["filename"], command)
        self.assertIn("sha256=" + DIGEST, command)
        self.assertNotIn("version=1.2.3", command)

    def test_already_public_without_installed_receipt_cannot_repeat_publication(self):
        a, b, c, d, e = self.capture()
        with a, b, c, d, e as registry, self.assertRaises(release.ContractError):
            registry.return_value = {"labels": ["staging", "main"]}
            release.prepare_handoff(
                self.root, REPOSITORY, 123, token="token", workflow_ref="main"
            )

    def test_promoter_forwards_explicit_recovery_identity(self):
        a, b, c, d, e = self.capture()
        with (
            a,
            b,
            c,
            d,
            e,
            patch.object(release, "read_json", return_value={"sha": QUALIFICATION}),
            patch.object(release, "caller", return_value="reviewed-caller"),
            patch.object(release, "verify", return_value={"state": "verified"}),
        ):
            result = release.prepare_handoff(
                self.root,
                REPOSITORY,
                123,
                token="token",
                qualification_sha=QUALIFICATION,
                workflow_ref="qualify/1.2.3",
                installed_run_id=456,
                promotion_workflow=".github/workflows/promote.yaml",
            )
        self.assertIn("qualification_sha=" + QUALIFICATION, result["next_command"])
        self.assertIn("installed_run_id=456", result["next_command"])

    def test_moved_workflow_ref_and_dirty_checkout_emit_no_handoff(self):
        for dirty in (False, True):
            a, b, c, d, e = self.capture()
            with (
                a,
                b,
                c as git,
                d,
                e,
                patch.object(release, "read_json", return_value={"sha": "f" * 40}),
                self.assertRaises(release.ContractError),
            ):
                if dirty:
                    git.side_effect = lambda root, *args: (
                        SOURCE if args[0] == "rev-parse" else "M pyproject.toml"
                    )
                release.prepare_handoff(
                    self.root,
                    REPOSITORY,
                    123,
                    token="token",
                    qualification_sha=QUALIFICATION,
                    workflow_ref="main",
                )

    def test_caller_rejects_mutable_pin_or_dropped_identity(self):
        fields = ["candidate_sha", "sha256", "qualification_sha"]
        document = {
            "on": {"workflow_dispatch": {"inputs": {key: {} for key in fields}}},
            "jobs": {
                "promote": {
                    "uses": "uibcdf/molsyssuite/.github/workflows/promote-noarch-conda.yaml@"
                    + SOURCE,
                    "with": {key: "${{ inputs." + key + " }}" for key in fields},
                }
            },
        }
        for change in ("none", "mutable", "dropped"):
            modified = copy.deepcopy(document)
            if change == "mutable":
                modified["jobs"]["promote"]["uses"] = modified["jobs"]["promote"][
                    "uses"
                ].replace(SOURCE, "main")
            if change == "dropped":
                modified["jobs"]["promote"]["with"].pop("qualification_sha")
            with patch.object(release, "git", return_value=json.dumps(modified)):
                if change == "none":
                    release.caller(
                        self.root,
                        QUALIFICATION,
                        ".github/workflows/promote.yaml",
                        "promote",
                        fields,
                    )
                else:
                    with self.assertRaises(release.ContractError):
                        release.caller(
                            self.root,
                            QUALIFICATION,
                            ".github/workflows/promote.yaml",
                            "promote",
                            fields,
                        )

    def test_cli_help_works_outside_source_with_safe_path(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [sys.executable, "-P", release.__file__, "--help"],
                cwd=directory,
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(result.returncode, 0, result.stderr)


class ReleaseArtifactTests(unittest.TestCase):
    def test_receipt_zip_rejects_expiry_bad_digest_and_ambiguous_paths(self):
        for failure in (None, "expired", "digest", "escape", "duplicate", "large"):
            payload = io.BytesIO()
            with zipfile.ZipFile(payload, "w") as archive:
                name = "../receipt.json" if failure == "escape" else "receipt.json"
                archive.writestr(
                    name,
                    json.dumps(
                        {"value": "x" * 65536 if failure == "large" else "verified"}
                    ),
                )
                if failure == "duplicate":
                    archive.writestr("./receipt.json", "{}")
            contents = payload.getvalue()
            native = {
                "id": 9,
                "name": "receipts-123-1",
                "expired": failure == "expired",
                "size_in_bytes": len(contents),
                "workflow_run": {"id": 123, "head_sha": RUN["head_sha"]},
                "digest": "sha256:" + hashlib.sha256(contents).hexdigest(),
            }
            if failure == "digest":
                native["digest"] = "sha256:" + "0" * 64
            with (
                patch.object(
                    artifacts,
                    "read_json",
                    return_value={"total_count": 1, "artifacts": [native]},
                ),
                patch.object(
                    artifacts.subprocess,
                    "run",
                    return_value=SimpleNamespace(stdout=contents),
                ),
            ):
                if failure is None:
                    receipts, _ = artifacts.acquire_json_artifact(
                        REPOSITORY, RUN, native["name"], "token"
                    )
                    self.assertEqual(receipts["receipt.json"], {"value": "verified"})
                else:
                    with self.subTest(failure=failure), self.assertRaises(ValueError):
                        artifacts.acquire_json_artifact(
                            REPOSITORY, RUN, native["name"], "token"
                        )
