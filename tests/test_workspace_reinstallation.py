"""Verify registry coverage, mutation boundaries and real editable version refresh."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import tomllib

from devtools.scripts import development_environment as development

ROOT = Path(__file__).resolve().parents[1]
MOLI = {
    "platform": {"repository": "uibcdf/moli"},
    "components": {
        name: {
            "repository": f"uibcdf/{name}",
            "governance": "direct",
            "capabilities": ["python-package"],
        }
        for name in ("sabueso", "praxis", "recorda")
    },
}


class WorkspaceReinstallationTests(unittest.TestCase):
    def test_all_python_members_and_moli_auxiliaries_without_admission_changes(self):
        suite = tomllib.loads((ROOT / "suite.toml").read_text())
        moli = {
            **MOLI,
            "components": {
                **MOLI["components"],
                "nextia": {"governance": "direct", "capabilities": []},
            },
        }
        plan = development.reinstallation_plan(suite, moli)
        names = {item["name"] for item in plan["included"]}
        self.assertEqual(len(names), 19)
        self.assertTrue({"topomt", "sabueso", "praxis", "recorda"} <= names)
        self.assertFalse({"molsys-ai", "nextia", "molsyssuite"} & names)
        self.assertNotIn(
            "topomt",
            {
                item["name"]
                for item in suite["policies"]["python"]["transition"]["components"]
            },
        )
        reduced = development.reinstallation_plan(
            suite, moli, excluded=["uibcdf/topomt", "recorda"]
        )
        self.assertEqual(
            {item["name"] for item in reduced["excluded"]}, {"topomt", "recorda"}
        )
        self.assertEqual(len(reduced["included"]), 17)
        for excluded in (["not-a-component"], ["molsyssuite"]):
            with self.subTest(excluded=excluded), self.assertRaises(ValueError):
                development.reinstallation_plan(suite, moli, excluded=excluded)

    def test_wrong_platform_and_duplicate_or_unsafe_identities_are_rejected(self):
        suite = {
            "members": [
                {
                    "name": "example",
                    "repository": "uibcdf/example",
                    "capabilities": ["python-package"],
                }
            ]
        }
        for moli in (
            {**MOLI, "platform": {"repository": "someone/else"}},
            {
                **MOLI,
                "components": {
                    "example": {
                        "repository": "uibcdf/example",
                        "governance": "direct",
                        "capabilities": ["python-package"],
                    }
                },
            },
            {
                **MOLI,
                "components": {
                    "../escape": {
                        "repository": "uibcdf/../escape",
                        "governance": "direct",
                        "capabilities": ["python-package"],
                    }
                },
            },
        ):
            with self.subTest(moli=moli), self.assertRaises(ValueError):
                development.reinstallation_plan(suite, moli)

    def test_entire_inventory_precedes_toolchain_and_pip_and_dry_run_is_read_only(self):
        with tempfile.TemporaryDirectory() as temporary:
            registry = Path(temporary) / "moli.toml"
            registry.write_text('[platform]\nrepository="uibcdf/moli"\n[components]\n')
            suite = {
                "members": [
                    {
                        "name": "example",
                        "repository": "uibcdf/example",
                        "capabilities": ["python-package"],
                    }
                ]
            }
            with (
                patch.object(development, "verify_toolchain") as toolchain,
                patch.object(development, "install_editables") as install,
                self.assertRaises(FileNotFoundError),
            ):
                development.reinstall_workspace(
                    suite, Path(temporary), moli_registry=registry, excluded=[]
                )
            toolchain.assert_not_called()
            install.assert_not_called()
            sources = [
                {
                    "name": "example",
                    "repository": "uibcdf/example",
                    "distribution": "example",
                }
            ]
            with (
                patch.object(development, "source_inventory", return_value=sources),
                patch.object(development, "verify_toolchain") as toolchain,
                patch.object(development, "install_editables") as install,
            ):
                result = development.reinstall_workspace(
                    suite,
                    Path(temporary),
                    moli_registry=registry,
                    excluded=[],
                    dry_run=True,
                )
            self.assertTrue(result["dry_run"])
            self.assertEqual(result["sources"], sources)
            toolchain.assert_not_called()
            install.assert_not_called()
            with (
                patch.object(development, "source_inventory", return_value=sources),
                patch.object(development, "verify_toolchain", return_value={}),
                patch.object(
                    development,
                    "install_editables",
                    side_effect=subprocess.CalledProcessError(1, ["pip"]),
                ),
                self.assertRaises(subprocess.CalledProcessError),
            ):
                development.reinstall_workspace(
                    suite, Path(temporary), moli_registry=registry, excluded=[]
                )

    def test_real_reinstall_refreshes_version_file_and_metadata_after_local_tag(self):
        with tempfile.TemporaryDirectory(
            prefix="suite-reinstall-version-"
        ) as temporary:
            root = Path(temporary)
            source = root / "source"
            source.mkdir()
            package = source / "suite_reinstall_fixture"
            package.mkdir()
            (package / "__init__.py").write_text("")
            (source / ".gitignore").write_text(
                "*.egg-info/\n__pycache__/\nsuite_reinstall_fixture/_version.py\n"
            )
            (source / "pyproject.toml").write_text(
                '[build-system]\nrequires=["setuptools", "versioningit"]\nbuild-backend="setuptools.build_meta"\n'
                '[project]\nname="suite-reinstall-fixture"\ndynamic=["version"]\n'
                '[tool.versioningit]\n[tool.versioningit.write]\nfile="suite_reinstall_fixture/_version.py"\n'
            )

            def git(*args):
                subprocess.run(
                    ["git", *args], cwd=source, check=True, capture_output=True
                )

            git("init", "--quiet")
            git("config", "user.name", "Reinstallation test")
            git("config", "user.email", "reinstall-test@example.invalid")
            git("config", "commit.gpgsign", "false")
            git("config", "tag.gpgsign", "false")
            git("add", ".")
            git("commit", "--quiet", "-m", "Initial fixture")
            git("tag", "0.1.0")
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "venv",
                    "--system-site-packages",
                    "--without-pip",
                    str(root / "venv"),
                ],
                check=True,
            )
            interpreter = root / "venv/bin/python"

            peer = root / "peer"
            peer.mkdir()
            (peer / "suite_reinstall_peer.py").write_text("")
            (peer / "pyproject.toml").write_text(
                '[build-system]\nrequires=["setuptools"]\nbuild-backend="setuptools.build_meta"\n'
                '[project]\nname="suite-reinstall-peer"\nversion="0.3.0"\n'
            )
            sources = [{"path": str(source)}, {"path": str(peer)}]

            def installed_version():
                return subprocess.check_output(
                    [
                        str(interpreter),
                        "-c",
                        "from importlib.metadata import version; print(version('suite-reinstall-fixture'))",
                    ],
                    cwd=root,
                    text=True,
                ).strip()

            with (
                patch.object(development.sys, "executable", str(interpreter)),
                patch.dict(
                    os.environ,
                    {"PIP_NO_INDEX": "1", "PIP_DISABLE_PIP_VERSION_CHECK": "1"},
                ),
            ):
                development.install_editables(sources)
                before = (package / "_version.py").read_text()
                self.assertEqual(installed_version(), "0.1.0")
                self.assertIn('"0.1.0"', before)
                git("commit", "--quiet", "--allow-empty", "-m", "Second fixture commit")
                git("tag", "0.2.0")
                self.assertEqual((package / "_version.py").read_text(), before)
                self.assertEqual(installed_version(), "0.1.0")
                development.install_editables(sources)
                self.assertEqual(installed_version(), "0.2.0")
                self.assertIn('"0.2.0"', (package / "_version.py").read_text())


if __name__ == "__main__":
    unittest.main()
