"""Command receiving must reject wrong bytes/origins and actual launcher failures."""

import contextlib
import hashlib
import importlib.metadata
import io
import json
import subprocess
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import yaml

from devtools.scripts import public_noarch_commands as commands
from devtools.scripts.verify_installed_matrix import MatrixError, verify_snapshot


class PublicNoarchCommandTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="public-command-test-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.prefix = self.root / "prefix with spaces ; literal"
        self.site = self.prefix / "site-packages"
        self.site.mkdir(parents=True)
        self.module = self.site / "example.py"
        self.module.write_text("def main(): pass\n")
        self.launcher = self.prefix / "bin" / "example"
        self.launcher.parent.mkdir()
        self.calls = self.root / "args.json"
        self.make_launcher(0)
        self.index = {
            "name": "example",
            "version": "0.1.0",
            "build": "py_0",
            "build_number": 0,
            "subdir": "noarch",
            "noarch": "python",
            "depends": ["python >=3.11,<3.15"],
        }
        self.link = {
            "noarch": {"type": "python", "entry_points": ["example = example:main"]}
        }
        self.coordinate = {
            "package": "example",
            "version": "0.1.0",
            "subdir": "noarch",
            "filename": "example-0.1.0-py_0.tar.bz2",
            "sha256": "",
        }
        self.artifact = self.root / self.coordinate["filename"]
        self.make_archive()
        self.record_path = self.prefix / "conda-meta" / "example-0.1.0-py_0.json"
        self.record_path.parent.mkdir()
        self.record = dict(
            self.index,
            sha256=self.coordinate["sha256"],
            url="https://conda.anaconda.org/uibcdf/noarch/" + self.artifact.name,
        )
        self.record_path.write_text(json.dumps(self.record))
        entries = importlib.metadata.EntryPoints(
            [
                importlib.metadata.EntryPoint(
                    name="example", value="example:main", group="console_scripts"
                )
            ]
        )
        self.distribution = SimpleNamespace(
            version="0.1.0",
            entry_points=entries,
            locate_file=lambda path: self.site / path,
        )

    def make_archive(self):
        with tarfile.open(self.artifact, "w:bz2") as archive:
            contents = {
                "info/index.json": json.dumps(self.index).encode(),
                "info/link.json": json.dumps(self.link).encode(),
                "site-packages/example.py": self.module.read_bytes(),
            }
            for name, data in contents.items():
                member = tarfile.TarInfo(name)
                member.size = len(data)
                archive.addfile(member, io.BytesIO(data))
        self.coordinate["sha256"] = hashlib.sha256(
            self.artifact.read_bytes()
        ).hexdigest()

    def make_launcher(self, code):
        self.launcher.write_text(
            f"#!{sys.executable}\nimport json, sys\nfrom pathlib import Path\n"
            f"Path({str(self.calls)!r}).write_text(json.dumps(sys.argv[1:]))\n"
            f"print('usage: example')\nraise SystemExit({code})\n"
        )
        self.launcher.chmod(0o755)

    @contextlib.contextmanager
    def installed_context(self):
        with (
            contextlib.chdir(self.root),
            patch.object(commands.sys, "prefix", str(self.prefix)),
            patch.object(commands.sys, "platform", "linux"),
            patch.object(commands.platform, "machine", return_value="x86_64"),
            patch.object(
                commands.importlib.metadata,
                "distribution",
                return_value=self.distribution,
            ),
            patch.object(
                commands.importlib,
                "import_module",
                return_value=SimpleNamespace(__file__=str(self.module)),
            ),
            patch.object(commands.shutil, "which", return_value=str(self.launcher)),
        ):
            yield

    def verify(self):
        return commands.verify_commands(
            self.coordinate,
            commands.inspect_archive(self.artifact, self.coordinate),
            self.artifact,
            "linux-64",
            f"{sys.version_info.major}.{sys.version_info.minor}",
            self.prefix,
        )

    def test_real_command_executes_literal_help_and_preserves_caller_bytes(self):
        before = self.artifact.read_bytes()
        with self.installed_context():
            proof = self.verify()
        self.assertEqual(json.loads(self.calls.read_text()), ["--help"])
        self.assertEqual(proof["commands"][0]["exit_code"], 0)
        self.assertGreater(proof["commands"][0]["stdout"]["bytes"], 0)
        self.assertEqual(self.artifact.read_bytes(), before)
        self.assertTrue(self.record_path.is_file())

    def test_actual_failed_help_rejects_receiving(self):
        self.make_launcher(13)
        with self.installed_context(), self.assertRaisesRegex(ValueError, "failed.*13"):
            self.verify()
        self.assertEqual(json.loads(self.calls.read_text()), ["--help"])

    def test_absent_or_foreign_launcher_stops_before_execution(self):
        for path in (None, str(self.root / "foreign")):
            with (
                self.subTest(path=path),
                self.installed_context(),
                patch.object(commands.shutil, "which", return_value=path),
                self.assertRaisesRegex(ValueError, "launcher"),
            ):
                self.verify()
        self.assertFalse(self.calls.exists())

    def test_changed_installed_digest_url_or_module_stops_before_execution(self):
        for field, value in (
            ("sha256", "0" * 64),
            ("url", "https://example.org/file"),
            ("version", "0.1.1"),
        ):
            with self.subTest(field=field):
                self.record_path.write_text(
                    json.dumps(dict(self.record, **{field: value}))
                )
                with (
                    self.installed_context(),
                    self.assertRaisesRegex(ValueError, "Conda record"),
                ):
                    self.verify()
        self.record_path.write_text(json.dumps(self.record))
        self.module.write_text("changed bytes\n")
        with (
            self.installed_context(),
            self.assertRaisesRegex(ValueError, "original archive"),
        ):
            self.verify()
        self.assertFalse(self.calls.exists())

    def test_foreign_import_or_wrong_console_target_rejected(self):
        with (
            self.installed_context(),
            patch.object(
                commands.importlib,
                "import_module",
                return_value=SimpleNamespace(__file__=str(self.root / "foreign.py")),
            ),
            self.assertRaisesRegex(ValueError, "module"),
        ):
            self.verify()
        self.distribution.entry_points = importlib.metadata.EntryPoints(
            [
                importlib.metadata.EntryPoint(
                    name="example", value="example:wrong", group="console_scripts"
                )
            ]
        )
        with self.installed_context(), self.assertRaisesRegex(ValueError, "metadata"):
            self.verify()
        self.assertFalse(self.calls.exists())

    def test_archive_digest_native_type_duplicate_scripts_or_channel_specs_rejected(
        self,
    ):
        with self.assertRaisesRegex(ValueError, "digest"):
            commands.inspect_archive(
                self.artifact, dict(self.coordinate, sha256="0" * 64)
            )
        self.index["noarch"] = "generic"
        self.make_archive()
        with self.assertRaisesRegex(ValueError, "noarch"):
            commands.inspect_archive(self.artifact, self.coordinate)
        self.index["noarch"] = "python"
        self.link["noarch"]["entry_points"] *= 2
        self.make_archive()
        with self.assertRaisesRegex(ValueError, "duplicated"):
            commands.inspect_archive(self.artifact, self.coordinate)
        self.link["noarch"]["entry_points"] = ["example = example:main"]
        self.index["depends"] = ["other-channel::example"]
        self.make_archive()
        with self.assertRaisesRegex(ValueError, "Conda specs"):
            commands.inspect_archive(self.artifact, self.coordinate)

    def test_wrong_cell_stops_before_network_or_install(self):
        with (
            self.installed_context(),
            patch.object(commands, "verify_public") as network,
            patch.object(commands.subprocess, "run") as run,
            self.assertRaisesRegex(ValueError, "actual cell"),
        ):
            commands.receive(self.coordinate, "win-64", "3.14", self.prefix)
        network.assert_not_called()
        run.assert_not_called()

    def test_receiving_solves_public_closure_and_retires_download_on_success_or_failure(
        self,
    ):
        from devtools.scripts import installed_noarch

        downloads = []

        def download(directory, plan, digest):
            path = directory / self.artifact.name
            path.write_bytes(self.artifact.read_bytes())
            downloads.append(path)
            return path

        for failure in (False, True):
            with (
                self.subTest(failure=failure),
                self.installed_context(),
                patch.object(
                    commands, "verify_public", return_value=self.record["url"]
                ),
                patch.object(installed_noarch, "download", side_effect=download),
                patch.object(installed_noarch, "conda_command", return_value=["conda"]),
                patch.object(
                    commands, "verify_commands", return_value={"commands": []}
                ),
                patch.object(
                    commands.subprocess,
                    "run",
                    side_effect=subprocess.CalledProcessError(17, "conda")
                    if failure
                    else None,
                ) as run,
            ):
                arguments = (
                    self.coordinate,
                    "linux-64",
                    f"{sys.version_info.major}.{sys.version_info.minor}",
                    self.prefix,
                )
                if failure:
                    with self.assertRaises(subprocess.CalledProcessError):
                        commands.receive(*arguments)
                else:
                    proof = commands.receive(*arguments)
                    self.assertTrue(proof["temporary_download_removed"])
                    self.assertEqual(
                        proof["schema"], "molsyssuite.public-noarch-commands@1"
                    )
                    solve, exact = [call.args[0] for call in run.call_args_list]
                    self.assertEqual(exact[-1], self.record["url"])
                    self.assertIn("--strict-channel-priority", solve)
                    self.assertNotIn("staging", " ".join(solve))
                    self.assertNotIn("shell", run.call_args.kwargs)
            self.assertFalse(downloads[-1].parent.exists())
            self.assertTrue(self.artifact.exists())

    def test_timed_out_command_and_cli_error_cannot_emit_verified_receipt(self):
        with (
            self.installed_context(),
            patch.object(
                commands.subprocess,
                "run",
                side_effect=subprocess.TimeoutExpired("example", 30),
            ),
            self.assertRaises(subprocess.TimeoutExpired),
        ):
            self.verify()
        output = self.root / "receipt.json"
        args = [
            "receive",
            *[
                arg
                for key, value in self.coordinate.items()
                for arg in ("--" + key, value)
            ],
            "--platform",
            "linux-64",
            "--python",
            "3.14",
            "--prefix",
            str(self.prefix),
            "--output",
            str(output),
        ]
        with patch.object(commands, "receive", side_effect=ValueError("wrong bytes")):
            self.assertEqual(commands.main(args), 1)
        self.assertEqual(json.loads(output.read_text())["state"], "unverified")

    def test_selected_platforms_are_bounded_and_real_arm64_profile(self):
        self.assertEqual(
            commands.matrix(["osx-arm64"])["include"],
            [{"platform": "osx-arm64", "runner": "macos-15"}],
        )
        for bad in ([], ["linux-64", "linux-64"], ["osx-64"], "linux-64"):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                commands.matrix(bad)

    def test_command_run_cannot_satisfy_existing_full_installed_matrix(self):
        source = "a" * 40
        run = {
            "id": 1,
            "head_sha": source,
            "path": ".github/workflows/verify-public-noarch-commands.yaml",
            "display_title": "Commands example-0.1.0-py_0.tar.bz2 " + "b" * 64,
            "status": "completed",
            "conclusion": "success",
            "run_attempt": 1,
        }
        with self.assertRaisesRegex(MatrixError, "exact source/workflow"):
            verify_snapshot(
                run,
                [],
                run_id=1,
                candidate=source,
                workflow=".github/workflows/test-installed-noarch-conda.yaml",
                title="Installed example-0.1.0-py_0.tar.bz2 " + "b" * 64,
                profile={},
            )

    def test_workflow_has_no_build_science_or_publication_operation(self):
        root = Path(__file__).resolve().parents[1]
        data = yaml.load(
            (root / ".github/workflows/verify-public-noarch-commands.yaml").read_text(),
            Loader=yaml.BaseLoader,
        )
        self.assertEqual(set(data["jobs"]), {"prepare", "commands"})
        self.assertEqual(data["permissions"], {"contents": "read"})
        step = next(
            item
            for item in data["jobs"]["commands"]["steps"]
            if item.get("name")
            == "Verify exact public file and execute installed commands outside source"
        )
        self.assertEqual(step["working-directory"], "${{ runner.temp }}")
        self.assertIn(
            'python -P "$TOOL_ROOT/devtools/scripts/public_noarch_commands.py" receive',
            step["run"],
        )
        self.assertNotIn("pytest", step["run"])


if __name__ == "__main__":
    unittest.main()
