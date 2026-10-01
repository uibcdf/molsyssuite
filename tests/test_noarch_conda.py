"""Reject metadata/resource drift before the shared noarch publisher may upload."""

import io
import json
import tarfile
import tempfile
import unittest
from pathlib import Path

from devtools.scripts import noarch_conda as noarch
from devtools.scripts.conda_release_contract import ContractError

PLAN = """schema = "molsyssuite.conda-plan@1"
package = "example"
version = "1.2.3"
build_number = 2
route = "staged"
profile = "noarch-python"
reason = "First noarch migration; installed qualification required"
decision_by = "dprada and LMMV"
artifact_subdirs = ["noarch"]
test_platforms = ["linux-64", "osx-arm64"]
python_versions = ["3.11", "3.12", "3.13"]
required_workflows = [".github/workflows/CI.yaml"]
requires_installed_gate = true
new_compatibility_surface = true
coupled_release = false
dependencies_public = true
[gate_jobs.".github/workflows/CI.yaml"]
"Full scientific tests" = ["Run tests"]
"""
PROJECT = """[build-system]
requires = ["setuptools>=61", "versioningit~=2.0"]
build-backend = "setuptools.build_meta"
[project]
name = "example"
dynamic = ["version"]
requires-python = ">=3.11,<3.14"
dependencies = ["smonitor>=0.12"]
[project.scripts]
example = "example.cli:main"
[tool.versioningit]
default-version = "0.0.0"
[tool.versioningit.write]
file = "example/_version.py"
[tool.setuptools]
include-package-data = false
"""
RECIPE = """package:
  name: example
  version: "{{ environ['MOLSYSSUITE_CONDA_VERSION'] }}"
build:
  number: {{ environ['MOLSYSSUITE_CONDA_BUILD_NUMBER'] }}
  string: py_{{ environ['MOLSYSSUITE_CONDA_BUILD_NUMBER'] }}
  noarch: python
  entry_points: ["example = example.cli:main"]
requirements:
  host: ["python >=3.11,<3.14", pip, setuptools, versioningit]
  run: ["python >=3.11,<3.14", "smonitor >=0.12"]
"""
INVENTORY = """reason = "Python version and packaged schema are required at runtime"
version_file = "site-packages/example/_version.py"
required_paths = ["site-packages/example/_version.py", "site-packages/example/schema.json"]
[installed_gate]
workflow = ".github/workflows/installed.yaml"
platforms = ["linux-64", "osx-arm64"]
python_versions = ["3.11", "3.12", "3.13"]
prepare_job = "prepare"
required_steps = ["Install exact artifact", "Validate installed files", "Run installed tests"]
job_template = "{platform} · Python {python}"
"""


class NoarchCondaTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        for relative, text in {
            "pyproject.toml": PROJECT,
            "devtools/conda-build/release_plan.toml": PLAN,
            "devtools/conda-build/meta.yaml": RECIPE,
            "devtools/conda-build/resources.toml": INVENTORY,
            "example/_version.py": '__version__ = "0.0.0"\n',
            "example/schema.json": "{}",
            ".github/workflows/installed.yaml": "on: workflow_dispatch\n",
        }.items():
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)

    def inspect(self):
        return noarch.inspect_recipe(
            self.root,
            "devtools/conda-build/release_plan.toml",
            "devtools/conda-build/resources.toml",
        )

    def archive(self, changes=None, missing=()):
        data = {
            "info/index.json": json.dumps(
                {
                    "name": "example",
                    "version": "1.2.3",
                    "build": "py_2",
                    "build_number": 2,
                    "subdir": "noarch",
                    "depends": ["python >=3.11,<3.14", "smonitor >=0.12"],
                }
            ),
            "info/link.json": json.dumps({"noarch": {"type": "python"}}),
            "site-packages/example-1.2.3.dist-info/METADATA": "Name: example\nVersion: 1.2.3\n",
            "site-packages/example/_version.py": '__version__ = "1.2.3"\n',
            "site-packages/example/schema.json": "{}",
        }
        data.update(changes or {})
        path = self.root / "example-1.2.3-py_2.tar.bz2"
        with tarfile.open(path, "w:bz2") as archive:
            for name, value in data.items():
                if name in missing:
                    continue
                contents = value.encode()
                member = tarfile.TarInfo(name)
                member.size = len(contents)
                archive.addfile(member, io.BytesIO(contents))
        return path

    def test_freeze_and_exact_artifact_inspection(self):
        plan, inventory = self.inspect()
        noarch.freeze_version(self.root, plan, inventory)
        metadata = noarch.tomllib.loads((self.root / "pyproject.toml").read_text())
        self.assertEqual(metadata["project"]["version"], "1.2.3")
        self.assertNotIn("versioningit", metadata["tool"])
        self.assertEqual(
            noarch.embedded_version((self.root / "example/_version.py").read_text()),
            "1.2.3",
        )
        result = noarch.inspect_artifact(self.archive(), plan, inventory)
        self.assertEqual(result["filename"], "example-1.2.3-py_2.tar.bz2")
        self.assertEqual(len(result["sha256"]), 64)
        self.inspect()  # Prepared static metadata preserves recipe parity.

    def test_missing_or_weaker_requirements_and_wrong_commands_fail_early(self):
        path = self.root / "devtools/conda-build/meta.yaml"
        for altered in (
            RECIPE.replace('"smonitor >=0.12"', '"smonitor"'),
            RECIPE.replace(', "smonitor >=0.12"', ""),
            RECIPE.replace("example.cli:main", "example.cli:wrong"),
            RECIPE.replace("noarch: python", "noarch: generic"),
            RECIPE + "# [win]\n",
        ):
            path.write_text(altered)
            with self.assertRaises(ContractError):
                self.inspect()

    def test_resource_and_version_failures_are_independent_of_recipe_success(self):
        plan, inventory = self.inspect()
        for changes, missing in (
            ({}, ["site-packages/example/schema.json"]),
            ({"site-packages/example/_version.py": '__version__ = "0.0.0"'}, []),
            ({"site-packages/example/native.so": "binary"}, []),
            (
                {
                    "info/index.json": json.dumps(
                        {
                            "name": "example",
                            "version": "1.2.3",
                            "build": "py_2",
                            "build_number": 2,
                            "subdir": "linux-64",
                        }
                    )
                },
                [],
            ),
        ):
            with self.assertRaises(ContractError):
                noarch.inspect_artifact(self.archive(changes, missing), plan, inventory)

    def test_archive_traversal_is_rejected_without_extraction(self):
        plan, inventory = self.inspect()
        with self.assertRaises(ContractError):
            noarch.inspect_artifact(self.archive({"../escape": "bad"}), plan, inventory)
        self.assertFalse((self.root.parent / "escape").exists())

    def test_missing_committed_resource_and_escaping_input_fail(self):
        (self.root / "example/schema.json").unlink()
        with self.assertRaises(ContractError):
            self.inspect()
        with self.assertRaises(ContractError):
            noarch.local_path(self.root, "../pyproject.toml")

    def test_declared_generated_version_can_be_missing_before_build(self):
        (self.root / "example/_version.py").unlink()
        plan, inventory = self.inspect()
        noarch.freeze_version(self.root, plan, inventory)
        self.assertEqual(
            noarch.embedded_version((self.root / "example/_version.py").read_text()),
            "1.2.3",
        )

    def test_overall_green_gate_is_insufficient_without_declared_jobs(self):
        path = self.root / "devtools/conda-build/release_plan.toml"
        path.write_text(PLAN.split("[gate_jobs.")[0])
        with self.assertRaises(ContractError):
            self.inspect()

    def test_promotion_binds_every_installed_cell_and_exact_digest(self):
        plan, inventory = self.inspect()
        descriptor = noarch.promotion_descriptor(self.root, plan, inventory, "a" * 64)
        self.assertEqual(
            descriptor["title"], "Installed example-1.2.3-py_2.tar.bz2 " + "a" * 64
        )
        inventory["installed_gate"]["python_versions"].pop()
        with self.assertRaises(ContractError):
            noarch.promotion_descriptor(self.root, plan, inventory, "a" * 64)
