"""Reject wrong installed provenance, changed resources and unchecked downloads."""

import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from devtools.scripts import installed_noarch as installed
from tests import test_noarch_conda as fixture_module


class InstalledNoarchTests(unittest.TestCase):
    def test_pytest_interpreter_cannot_hide_source_import_or_execute_no_tests(self):
        (self.root / "tests").mkdir()
        inventory = dict(
            self.inventory, installed_tests={"paths": ["tests"], "pytest_args": []}
        )

        def execute(arguments, plugins):
            guard = plugins[0]
            guard.pytest_sessionstart(None)
            guard.pytest_runtest_logreport(
                SimpleNamespace(when="call", outcome="passed")
            )
            guard.pytest_sessionfinish(None, 0)
            return 0

        def shadow(arguments, plugins):
            guard = plugins[0]
            guard.pytest_sessionstart(None)
            self.module.__file__ = str(self.root / "example/__init__.py")
            guard.pytest_sessionfinish(None, 0)
            return 0

        with (
            patch.object(installed.sys, "prefix", str(self.prefix)),
            patch.object(
                installed.importlib, "import_module", return_value=self.module
            ),
            patch.dict(
                installed.sys.modules,
                {"example": self.module, "pytest": SimpleNamespace(main=execute)},
            ),
        ):
            self.assertEqual(installed.run_tests(self.root, inventory), 0)
            with (
                patch.dict(
                    installed.sys.modules,
                    {"pytest": SimpleNamespace(main=lambda *args, **kwargs: 0)},
                ),
                self.assertRaises(installed.ContractError),
            ):
                installed.run_tests(self.root, inventory)
            with (
                patch.dict(
                    installed.sys.modules, {"pytest": SimpleNamespace(main=shadow)}
                ),
                self.assertRaises(installed.ContractError),
            ):
                installed.run_tests(self.root, inventory)

    def setUp(self):
        fixture = fixture_module.NoarchCondaTests()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        self.root = fixture.root
        self.plan, self.inventory = fixture.inspect()
        self.artifact = fixture.archive()
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.prefix = Path(self.temporary.name)
        for name in self.inventory["required_paths"]:
            target = self.prefix / name.removeprefix("site-packages/")
            target.parent.mkdir(parents=True, exist_ok=True)
            with installed.tarfile.open(self.artifact) as archive:
                target.write_bytes(archive.extractfile(name).read())
        (self.prefix / "conda-meta").mkdir()
        record = {
            "name": "example",
            "version": "1.2.3",
            "build": "py_2",
            "sha256": hashlib.sha256(self.artifact.read_bytes()).hexdigest(),
            "url": "https://conda.anaconda.org/uibcdf/label/staging/noarch/example-1.2.3-py_2.tar.bz2",
        }
        self.record = self.prefix / "conda-meta/example-1.2.3-py_2.json"
        self.record.write_text(json.dumps(record))
        self.distribution = SimpleNamespace(
            version="1.2.3", locate_file=lambda name: self.prefix / name
        )
        self.module = SimpleNamespace(
            __file__=str(self.prefix / "example/_version.py"), __version__="1.2.3"
        )

    def verify(self):
        with (
            patch.object(installed.sys, "prefix", str(self.prefix)),
            patch.object(
                installed.shutil, "which", return_value=str(self.prefix / "bin/example")
            ),
            patch.object(installed.sys, "platform", "linux"),
            patch.object(installed.platform, "machine", return_value="x86_64"),
            patch.object(
                installed.sys, "version_info", SimpleNamespace(major=3, minor=13)
            ),
            patch.object(
                installed.importlib.metadata,
                "distribution",
                return_value=self.distribution,
            ),
            patch.object(
                installed.importlib, "import_module", return_value=self.module
            ),
        ):
            return installed.verify_installed(
                self.root, self.plan, self.inventory, self.artifact, "linux-64", "3.13"
            )

    def test_exact_installed_bytes_and_provenance_pass(self):
        self.assertEqual(self.verify()["state"], "verified")

    def test_stale_version_changed_resource_and_source_import_fail(self):
        self.distribution.version = "0.0.0"
        with self.assertRaises(installed.ContractError):
            self.verify()
        self.distribution.version = "1.2.3"
        self.module.__file__ = str(self.root / "example/_version.py")
        with self.assertRaises(installed.ContractError):
            self.verify()
        self.module.__file__ = str(self.prefix / "example/_version.py")
        (self.prefix / "example/schema.json").write_text("changed")
        with self.assertRaises(installed.ContractError):
            self.verify()

    def test_wrong_conda_digest_and_staging_dependency_cannot_prove_public_closure(
        self,
    ):
        original = json.loads(self.record.read_text())
        altered = dict(original, sha256="b" * 64)
        self.record.write_text(json.dumps(altered))
        with self.assertRaises(installed.ContractError):
            self.verify()
        self.record.write_text(json.dumps(original))
        sibling = self.prefix / "conda-meta/sibling.json"
        sibling.write_text(
            json.dumps(
                {
                    "name": "sibling",
                    "url": "https://conda.anaconda.org/uibcdf/label/staging/noarch/sibling-1.0.0-py_0.conda",
                }
            )
        )
        with self.assertRaises(installed.ContractError):
            self.verify()

    def test_digest_checked_before_download_may_be_installed(self):
        contents = b"example immutable artifact"
        digest = hashlib.sha256(contents).hexdigest()
        with patch.object(installed, "urlopen", return_value=io.BytesIO(contents)):
            self.assertEqual(
                installed.download(self.prefix, self.plan, digest).read_bytes(),
                contents,
            )
        with (
            patch.object(installed, "urlopen", return_value=io.BytesIO(contents)),
            self.assertRaises(installed.ContractError),
        ):
            installed.download(self.prefix, self.plan, "c" * 64)

    def test_prepare_rejects_missing_cells_or_wrong_file_and_source(self):
        gate = self.inventory["installed_gate"]
        gate.update(
            prepare_job="installed / prepare",
            job_template="installed / {platform} · Python {python}",
        )
        with patch.object(installed.subprocess, "check_output", return_value="a" * 40):
            descriptor = installed.prepare(
                self.root,
                self.plan,
                self.inventory,
                "a" * 40,
                self.artifact.name,
                "b" * 64,
            )
            self.assertEqual(len(json.loads(descriptor["matrix"])["include"]), 6)
            with self.assertRaises(installed.ContractError):
                installed.prepare(
                    self.root,
                    self.plan,
                    self.inventory,
                    "c" * 40,
                    self.artifact.name,
                    "b" * 64,
                )
            with self.assertRaises(installed.ContractError):
                installed.prepare(
                    self.root,
                    self.plan,
                    self.inventory,
                    "a" * 40,
                    "another.tar.bz2",
                    "b" * 64,
                )
            gate["python_versions"] = ["3.13"]
            with self.assertRaises(installed.ContractError):
                installed.prepare(
                    self.root,
                    self.plan,
                    self.inventory,
                    "a" * 40,
                    self.artifact.name,
                    "b" * 64,
                )
