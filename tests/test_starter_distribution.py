"""Build the real starter distributions and receive their license payload (#162)."""

from __future__ import annotations

import email
import subprocess
import sys
import tarfile
import tempfile
import unittest
import zipfile
from pathlib import Path

import tomllib
from packaging.requirements import Requirement

from devtools.scripts.bootstrap_component import bootstrap

ROOT = Path(__file__).resolve().parents[1]


class StarterDistributionTests(unittest.TestCase):
    def test_generated_sdist_and_rebuilt_wheel_include_declared_license(self):
        with tempfile.TemporaryDirectory(prefix="suite-license-test-") as temporary:
            root = Path(temporary)
            project = bootstrap(root / "source", "uibcdf/dockingmt", "Starter fixture")
            for arguments in (
                ["init", "-q"],
                ["add", "."],
                [
                    "-c",
                    "user.name=Fixture",
                    "-c",
                    "user.email=fixture@example.invalid",
                    "-c",
                    "commit.gpgsign=false",
                    "commit",
                    "-qm",
                    "Fixture",
                ],
                ["-c", "tag.gpgsign=false", "tag", "0.1.0"],
            ):
                subprocess.run(
                    ["git", *arguments], cwd=project, check=True, capture_output=True
                )
            script = (
                "import setuptools.build_meta as backend; "
                "backend.build_sdist('dist'); backend.build_wheel('dist')"
            )
            result = subprocess.run(
                [sys.executable, "-c", script],
                cwd=project,
                capture_output=True,
                text=True,
                timeout=90,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            original = next((project / "dist").glob("*.whl"))
            expected = (ROOT / "LICENSE").read_bytes()

            def check_wheel(path):
                with zipfile.ZipFile(path) as archive:
                    metadata_path = next(
                        n
                        for n in archive.namelist()
                        if n.endswith(".dist-info/METADATA")
                    )
                    metadata = email.message_from_bytes(archive.read(metadata_path))
                    self.assertEqual(metadata["License-Expression"], "MIT")
                    self.assertEqual(metadata.get_all("License-File"), ["LICENSE"])
                    prefix = metadata_path.rsplit("/", 1)[0]
                    self.assertEqual(
                        archive.read(prefix + "/licenses/LICENSE"), expected
                    )
                    self.assertFalse(
                        any(
                            v.startswith("License ::")
                            for v in metadata.get_all("Classifier", [])
                        )
                    )

            check_wheel(original)
            project_metadata = tomllib.loads((project / "pyproject.toml").read_text())
            backend = next(
                Requirement(raw)
                for raw in project_metadata["build-system"]["requires"]
                if Requirement(raw).name == "setuptools"
            )
            self.assertNotIn("76.1.0", backend.specifier)
            with tarfile.open(next((project / "dist").glob("*.tar.gz"))) as archive:
                license_path = next(
                    n for n in archive.getnames() if n.endswith("/LICENSE")
                )
                self.assertEqual(archive.extractfile(license_path).read(), expected)
                metadata_path = next(
                    n
                    for n in archive.getnames()
                    if n.count("/") == 1 and n.endswith("/PKG-INFO")
                )
                metadata = email.message_from_bytes(
                    archive.extractfile(metadata_path).read()
                )
                self.assertEqual(metadata["License-Expression"], "MIT")
                self.assertEqual(metadata.get_all("License-File"), ["LICENSE"])
                archive.extractall(root / "unpacked", filter="data")
            unpacked = next((root / "unpacked").iterdir())
            result = subprocess.run(
                [
                    sys.executable,
                    "-c",
                    "import setuptools.build_meta as b; b.build_wheel('dist')",
                ],
                cwd=unpacked,
                capture_output=True,
                text=True,
                timeout=90,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            check_wheel(next((unpacked / "dist").glob("*.whl")))


if __name__ == "__main__":
    unittest.main()
