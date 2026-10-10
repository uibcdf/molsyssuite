"""Protect private-member audit access, disclosure and genuine failure results."""

from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import yaml

from devtools.scripts import repository_read_access as access


class RepositoryReadAccessTests(unittest.TestCase):
    def test_credentials_are_scoped_to_registered_https_paths(self):
        request = "protocol=https\nhost=github.com\npath=uibcdf/opencastp.git\n"
        allowed = {"uibcdf/opencastp"}
        self.assertIn(
            "password=example", access.credential_response(request, "example", allowed)
        )
        for changed in (
            request.replace("https", "http"),
            request.replace("github.com", "github.com.evil.invalid"),
            request.replace("opencastp", "unregistered"),
            request.replace("uibcdf", "another-owner"),
            "protocol=https\nhost=github.com\n",
        ):
            with self.subTest(request=changed):
                self.assertEqual(
                    access.credential_response(changed, "example", allowed), ""
                )
        self.assertEqual(access.credential_response(request, "", allowed), "")
        self.assertEqual(
            access.credential_response(request, "example\nextra=value", allowed), ""
        )

    def test_real_git_helper_neither_persists_the_token_nor_uses_cached_credentials(
        self,
    ):
        with tempfile.TemporaryDirectory() as temporary:
            config = Path(temporary) / "gitconfig"
            config.write_text("[credential]\n\thelper = store\n")
            environment = access.git_environment(
                {
                    **os.environ,
                    "GIT_CONFIG_GLOBAL": str(config),
                    access.TOKEN_VARIABLE: "example-credential",
                }
            )
            # git_environment replaces inherited GIT_CONFIG_*; explicitly isolate
            # this test's host settings after constructing the invocation config.
            environment["GIT_CONFIG_GLOBAL"] = str(config)
            environment["GIT_CONFIG_NOSYSTEM"] = "1"
            request = "protocol=https\nhost=github.com\npath=uibcdf/opencastp.git\n\n"
            result = subprocess.run(
                ["git", "credential", "fill"],
                input=request,
                text=True,
                capture_output=True,
                env=environment,
                check=True,
            )
            self.assertIn("password=example-credential", result.stdout)
            for operation in ("approve", "reject"):
                subprocess.run(
                    ["git", "credential", operation],
                    input=result.stdout,
                    text=True,
                    capture_output=True,
                    env=environment,
                    check=True,
                )
            self.assertEqual(config.read_text(), "[credential]\n\thelper = store\n")
            self.assertEqual(
                sorted(path.name for path in Path(temporary).iterdir()), ["gitconfig"]
            )
            denied = subprocess.run(
                ["git", "credential", "fill"],
                input=request.replace("github.com", "evil.invalid"),
                text=True,
                capture_output=True,
                env=environment,
                check=False,
            )
            self.assertNotEqual(denied.returncode, 0)
            self.assertNotIn("example-credential", denied.stdout + denied.stderr)

    def test_private_stdout_stderr_and_failure_remain_bounded(self):
        with tempfile.TemporaryDirectory() as temporary:
            receipt = Path(temporary) / "receipt.json"
            for exit_code in (0, 7):
                with (
                    self.subTest(exit_code=exit_code),
                    redirect_stdout(io.StringIO()) as output,
                ):
                    status = access.run_audit(
                        [
                            sys.executable,
                            "-c",
                            (
                                "import sys; print('PRIVATE SOURCE'); "
                                "print('PRIVATE TRACE', file=sys.stderr); "
                                f"sys.exit({exit_code})"
                            ),
                        ],
                        private_output=True,
                        receipt=receipt,
                    )
                    self.assertEqual(status, exit_code)
                    self.assertNotIn("PRIVATE", output.getvalue() + receipt.read_text())
                    self.assertEqual(
                        json.loads(receipt.read_text())["returncode"], exit_code
                    )

    def test_launch_errors_do_not_publish_private_paths(self):
        with (
            tempfile.TemporaryDirectory() as temporary,
            redirect_stdout(io.StringIO()) as output,
        ):
            receipt = Path(temporary) / "receipt.json"
            self.assertEqual(
                access.run_audit(
                    ["/private/source/does-not-exist"],
                    private_output=True,
                    receipt=receipt,
                ),
                1,
            )
            self.assertNotIn("/private/source", output.getvalue() + receipt.read_text())
            self.assertEqual(json.loads(receipt.read_text())["status"], "failure")

    def test_non_git_commands_do_not_receive_the_read_secret(self):
        with (
            patch.dict(os.environ, {access.TOKEN_VARIABLE: "example"}),
            patch.object(
                access.subprocess,
                "run",
                return_value=subprocess.CompletedProcess([], 0),
            ) as run,
        ):
            access.run_audit(["python", "audit.py"])
            self.assertNotIn(access.TOKEN_VARIABLE, run.call_args.kwargs["env"])

    def test_public_source_receipt_strips_private_metadata_and_rejects_unknown_identity(
        self,
    ):
        with tempfile.TemporaryDirectory() as temporary:
            inventory = Path(temporary) / "sources.json"
            source = {
                "repository": "uibcdf/opencastp",
                "sha": "a" * 40,
                "distribution": "PRIVATE",
                "path": "/private/source",
                "version": "PRIVATE",
            }
            inventory.write_text(json.dumps({"sources": [source]}))
            self.assertEqual(
                access.public_source_heads(inventory),
                [
                    {"repository": "uibcdf/opencastp", "sha": "a" * 40},
                ],
            )
            for mutation in ({"sha": "PRIVATE"}, {"repository": "evil/private"}):
                inventory.write_text(json.dumps({"sources": [{**source, **mutation}]}))
                with self.assertRaises(ValueError):
                    access.public_source_heads(inventory)
            with redirect_stdout(io.StringIO()):
                receipt = Path(temporary) / "receipt.json"
                self.assertEqual(
                    access.run_audit(
                        [sys.executable, "-c", "pass"],
                        private_output=True,
                        receipt=receipt,
                        source_inventory=inventory,
                    ),
                    1,
                )
                self.assertEqual(json.loads(receipt.read_text())["status"], "failure")

    def test_secret_consumers_have_trusted_main_routes_and_private_receipts(self):
        for filename in (
            "check-component-guides.yaml",
            "check-component-dependencies.yaml",
            "check-vendored-guides.yaml",
            "audit-component-issue-labels.yaml",
            "check-development-environment.yaml",
        ):
            with self.subTest(workflow=filename):
                workflow = yaml.load(
                    (access.ROOT / ".github/workflows" / filename).read_text(),
                    Loader=yaml.BaseLoader,
                )
                self.assertNotIn("pull_request_target", workflow["on"])
                self.assertEqual(workflow["on"]["push"]["branches"], ["main"])
                for job in workflow["jobs"].values():
                    if "SUITE_REPOSITORIES_READ_TOKEN" not in json.dumps(job):
                        continue
                    controlling_job = (
                        workflow["jobs"][job["needs"]] if "needs" in job else job
                    )
                    self.assertIn(
                        "github.ref == 'refs/heads/main'", controlling_job["if"]
                    )
                    if "pull_request" in workflow["on"]:
                        self.assertIn(
                            "github.event_name != 'pull_request'", controlling_job["if"]
                        )
                    for step in job["steps"]:
                        if step.get("uses", "").startswith("actions/checkout"):
                            self.assertEqual(
                                step["with"]["persist-credentials"], "false"
                            )
                        if step.get("uses", "").startswith("actions/upload-artifact"):
                            self.assertEqual(step["with"]["path"], "public-evidence/")
                    checks = [step["run"] for step in job["steps"] if "run" in step]
                    self.assertTrue(
                        any("--private-output" in command for command in checks)
                    )


if __name__ == "__main__":
    unittest.main()
