"""Reject metadata/resource drift before the shared noarch publisher may upload."""

import io
import json
import subprocess
import sys
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

    def test_recipe_rejects_installed_test_dependencies_before_building(self):
        resources = self.root / "devtools/conda-build/resources.toml"
        for spec in (
            "packaging>=24",
            "packaging",
            "python>=3.11,<3.14",
            "example>=1,<2",
            "packaging @ https://example.invalid/tool.whl",
        ):
            with self.subTest(spec=spec):
                resources.write_text(
                    INVENTORY
                    + "\n[installed_tests]\nconda_dependencies = "
                    + json.dumps([spec])
                    + "\n"
                )
                with self.assertRaises(ContractError):
                    self.inspect()

    def test_publisher_cli_rejects_unbounded_tests_before_freezing(self):
        resources = self.root / "devtools/conda-build/resources.toml"
        resources.write_text(
            INVENTORY + '\n[installed_tests]\nconda_dependencies = ["packaging>=24"]\n'
        )
        original = {
            name: (self.root / name).read_bytes()
            for name in ("pyproject.toml", "example/_version.py")
        }
        output = self.root / "publisher-output"
        command = [
            sys.executable,
            str(Path(noarch.__file__).resolve()),
            "--root",
            str(self.root),
            "--freeze-version",
            "--github-output",
            str(output),
        ]
        result = subprocess.run(
            command, capture_output=True, text=True, timeout=30, check=False
        )
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("explicit lower and upper bounds", result.stdout)
        self.assertFalse(output.exists())
        for name, data in original.items():
            self.assertEqual(data, (self.root / name).read_bytes())

    def test_recipe_accepts_reviewed_bounded_test_tools(self):
        resources = self.root / "devtools/conda-build/resources.toml"
        resources.write_text(
            INVENTORY
            + "\n[installed_tests]\n"
            + 'conda_dependencies = ["packaging>=24,<27", "pytest-subtests==0.14.1"]\n'
        )
        plan, inventory = self.inspect()
        self.assertEqual("example", plan["package"])
        self.assertEqual(
            ["packaging>=24,<27", "pytest-subtests==0.14.1"],
            inventory["installed_tests"]["conda_dependencies"],
        )

    def test_resource_review_is_independent_of_publisher_plan(self):
        (self.root / "devtools/conda-build/release_plan.toml").unlink()
        result = noarch.inspect_resources(
            self.root, "devtools/conda-build/resources.toml"
        )
        self.assertIn("site-packages/example/schema.json", result["required_paths"])
        (self.root / "example/schema.json").unlink()
        with self.assertRaisesRegex(ContractError, "missing"):
            noarch.inspect_resources(self.root, "devtools/conda-build/resources.toml")

    def test_absent_runtime_list_identifies_the_missing_public_requirement(self):
        with self.assertRaisesRegex(ContractError, "python>=3.11"):
            noarch.required_constraints(None, ["python>=3.11,<3.15"], {})

    def test_external_runtime_floor_binds_recipe_and_exact_archive(self):
        inventory = self.root / "devtools/conda-build/resources.toml"
        inventory.write_text(
            'external_run_requirements = ["gh>=2.48.0"]\n'
            'external_run_reason = "Network operations use the installed command"\n'
            + INVENTORY
        )
        with self.assertRaisesRegex(ContractError, "gh>=2.48.0"):
            self.inspect()
        recipe = self.root / "devtools/conda-build/meta.yaml"
        recipe.write_text(RECIPE.replace('"smonitor >=0.12"]', '"smonitor >=0.12", "gh >=2.48.0"]'))
        plan, resources = self.inspect()
        for constraint in (None, "gh >=2.47.0", "gh >=2.48.0"):
            with self.subTest(constraint=constraint):
                index = {
                    "name": "example", "version": "1.2.3", "build": "py_2",
                    "build_number": 2, "subdir": "noarch",
                    "depends": ["python >=3.11,<3.14", "smonitor >=0.12"],
                }
                if constraint:
                    index["depends"].append(constraint)
                archive = self.archive({"info/index.json": json.dumps(index)})
                if constraint == "gh >=2.48.0":
                    self.assertEqual(noarch.inspect_artifact(archive, plan, resources)["version"], "1.2.3")
                else:
                    with self.assertRaisesRegex(ContractError, "gh>=2.48.0"):
                        noarch.inspect_artifact(archive, plan, resources)

    def test_external_requirements_reject_ambiguous_or_reserved_inputs(self):
        project = noarch.tomllib.loads(PROJECT)["project"]
        for requirements in (
            "gh>=2.48.0", ["gh"], ["python>=3.11"], ["example>=1"],
            ["smonitor>=0.12"], ["gh>=2.48.0", "GH>=2.48.0"],
            ["gh[extra]>=2.48.0"], ["conda-forge::gh>=2.48.0"],
            ["gh>=2.48.0; sys_platform == 'win32'"], ["gh @ https://example.invalid/gh"],
            [12],
        ):
            with self.subTest(requirements=requirements):
                with self.assertRaises(ValueError):
                    noarch.external_run_constraints(
                        {"external_run_requirements": requirements, "external_run_reason": "reviewed"},
                        project,
                    )
        with self.assertRaisesRegex(ContractError, "review reason"):
            noarch.external_run_constraints({"external_run_requirements": ["gh>=2.48.0"]}, project)
        self.assertEqual(noarch.external_run_constraints({}, project), [])

    def test_legacy_build_python_section_is_explicit_and_preserves_checks(self):
        recipe = self.root / "devtools/conda-build/meta.yaml"
        recipe.write_text(RECIPE.replace("  host:", "  build:"))
        context = {
            "MOLSYSSUITE_CONDA_VERSION": "1.2.3",
            "MOLSYSSUITE_CONDA_BUILD_NUMBER": "2",
        }
        result = noarch.inspect_recipe_dependencies(
            self.root, "devtools/conda-build/meta.yaml", context, python_section="build"
        )
        self.assertEqual(result["python_build_section"], "build")
        recipe.write_text(
            recipe.read_text().replace("python >=3.11,<3.14", "python >=3.10,<3.14", 1)
        )
        with self.assertRaisesRegex(ContractError, "python"):
            noarch.inspect_recipe_dependencies(
                self.root,
                "devtools/conda-build/meta.yaml",
                context,
                python_section="build",
            )
        with self.assertRaisesRegex(ContractError, "section"):
            noarch.inspect_recipe_dependencies(
                self.root,
                "devtools/conda-build/meta.yaml",
                context,
                python_section="run",
            )

    def test_resource_review_refuses_a_different_generated_version_target(self):
        path = self.root / "pyproject.toml"
        path.write_text(PROJECT.replace("example/_version.py", "example/stale.py"))
        with self.assertRaisesRegex(ContractError, "generated version target"):
            noarch.inspect_resources(self.root, "devtools/conda-build/resources.toml")

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

    def test_src_source_paths_do_not_change_installed_archive_coordinates(self):
        source = self.root / "src"
        source.mkdir()
        (self.root / "example").rename(source / "example")
        project = self.root / "pyproject.toml"
        project.write_text(project.read_text().replace(
            'file = "example/_version.py"', 'file = "src/example/_version.py"'
        ))
        resources = self.root / "devtools/conda-build/resources.toml"
        resources.write_text('source_root = "src"\n' + resources.read_text())
        plan, inventory = self.inspect()
        generated = source / "example/_version.py"
        generated.unlink()
        self.inspect()  # A declared generated target may be absent.
        noarch.freeze_version(self.root, plan, inventory)
        self.assertEqual(noarch.embedded_version(generated.read_text()), "1.2.3")
        self.assertFalse((self.root / "example").exists())
        self.assertEqual(noarch.inspect_artifact(self.archive(), plan, inventory)["version"], "1.2.3")
        self.inspect()

    def test_source_root_rejects_unsupported_layout_and_aliases(self):
        for prefix in (None, True, "", "../src", "/src", "src/", "other", "src\\bad"):
            with self.subTest(prefix=prefix), self.assertRaises(noarch.ContractError):
                noarch.source_resource(self.root, {"source_root": prefix}, "example/schema.json")
        with self.assertRaises(noarch.ContractError):
            noarch.source_resource(self.root, {"source_root": "src"}, "example/schema.json")
        try:
            (self.root / "src").symlink_to(self.root, target_is_directory=True)
        except OSError:
            return  # Windows without symlink privilege still exercises literal/missing cases.
        with self.assertRaisesRegex(noarch.ContractError, "symlink"):
            noarch.source_resource(self.root, {"source_root": "src"}, "example/schema.json")

    def test_src_version_target_mismatch_fails_before_freezing(self):
        (self.root / "src").mkdir()
        (self.root / "example").rename(self.root / "src/example")
        resources = self.root / "devtools/conda-build/resources.toml"
        resources.write_text('source_root = "src"\n' + resources.read_text())
        with self.assertRaisesRegex(noarch.ContractError, "version target"):
            self.inspect()

    def test_declared_support_is_validated_as_input_and_refused_in_runtime_archive(self):
        import hashlib
        helper = self.root / "example_test_support/helper.py"
        helper.parent.mkdir(); helper.write_text("VALUE='support'\n")
        digest = hashlib.sha256(helper.read_bytes()).hexdigest()
        resources = self.root / "devtools/conda-build/resources.toml"
        resources.write_text(resources.read_text() + f'''
[installed_tests.support]
schema = "molsyssuite.installed-test-support@1"
namespace = "example_test_support"
reason = "Unshipped fixture support"
[[installed_tests.support.files]]
source = "example_test_support/helper.py"
target = "example_test_support/helper.py"
sha256 = "{digest}"
''')
        plan, inventory = self.inspect()
        noarch.inspect_artifact(self.archive(), plan, inventory)
        with self.assertRaisesRegex(ContractError, "unshipped test support"):
            noarch.inspect_artifact(self.archive({"site-packages/example_test_support/helper.py": helper.read_text()}), plan, inventory)
        helper.write_text("VALUE='changed'\n")
        with self.assertRaisesRegex(ContractError, "digest changed"):
            noarch.inspect_resources(self.root, "devtools/conda-build/resources.toml")

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
