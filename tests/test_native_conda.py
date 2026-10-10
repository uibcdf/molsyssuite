"""A native declaration cannot inherit noarch admission or hide public drift."""

import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import tomllib
import yaml

from devtools.scripts import dependency_routes, native_conda, noarch_conda

PLAN = """schema = "molsyssuite.conda-plan@1"
package = "example"
version = "1.2.3"
build_number = 2
route = "staged"
profile = "native-abi3"
reason = "First bundled native surface"
decision_by = "LMMV"
artifact_subdirs = ["linux-64", "osx-arm64"]
test_platforms = ["linux-64", "osx-arm64"]
python_versions = ["3.11", "3.12", "3.13", "3.14"]
required_workflows = [".github/workflows/CI.yaml"]
requires_installed_gate = true
new_compatibility_surface = true
coupled_release = false
dependencies_public = true
[gate_jobs.".github/workflows/CI.yaml"]
"Installed science" = ["Run tests"]
"""
PROJECT = """[project]
name = "example"
requires-python = ">=3.11,<3.15"
dependencies = ["smonitor>=0.16,<1"]
"""
RECIPE = """package:
  name: example
  version: "{{ environ['MOLSYSSUITE_CONDA_VERSION'] }}"
build:
  number: {{ environ['MOLSYSSUITE_CONDA_BUILD_NUMBER'] }}
  string: pyabi3h{{ PKG_HASH }}_{{ PKG_BUILDNUM }}
  python_version_independent: true
  script: "{{ PYTHON }} -m pip install . --no-deps --no-build-isolation"
requirements:
  build:
    - {{ compiler('rust') }}
  host: ["python 3.11.*", "python-abi3 3.11.*", pip, maturin]
  run: ["python >=3.11,<3.15", "smonitor >=0.16,<1"]
"""


class NativeCondaTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="molsyssuite-native-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        for path, content in {
            "pyproject.toml": PROJECT,
            "devtools/conda-build/meta.yaml": RECIPE,
            "devtools/conda-build/plan.toml": PLAN,
            "devtools/dependency_routes.toml": """schema = "molsyssuite.dependency-routes@2"
reason = "Reviewed native recipe; no runtime environments or workflows in this fixture"
source_routes = []
source_reason = "Public runtime dependencies"
[[recipes]]
path = "devtools/conda-build/meta.yaml"
kind = "native-abi3-dependencies"
plan = "devtools/conda-build/plan.toml"
abi3_minimum = "3.11"
reason = "First native migration"
""",
        }.items():
            self.write(path, content)

    def write(self, path, content):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)

    def inspect(self):
        return native_conda.inspect_recipe_dependencies(
            self.root,
            "devtools/conda-build/meta.yaml",
            "devtools/conda-build/plan.toml",
            "3.11",
        )

    def test_native_profile_retains_scope_identity_inputs_and_no_mutation(self):
        before = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        evidence = dependency_routes.audit(self.root)
        route = evidence["routes"][0]
        self.assertEqual(route["scope"], "declared-native-abi3-dependencies")
        self.assertEqual(route["artifact_subdirs"], ["linux-64", "osx-arm64"])
        self.assertEqual(route["qualification"], "declared-only")
        self.assertFalse(route["native_bytes_verified"])
        self.assertEqual(evidence["qualification"], "declared-only")
        self.assertEqual(
            route["input_sha256"]["pyproject.toml"],
            hashlib.sha256(PROJECT.encode()).hexdigest(),
        )
        self.assertEqual(
            before, {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        )

    def test_runtime_missing_weakened_narrowed_or_duplicate_constraints_fail(self):
        for replacement in (
            "",
            ', "smonitor >=0.15,<1"',
            ', "smonitor >=0.16"',
            ', "smonitor >=0.17,<1"',
            ', "smonitor >=0.16,<1", "smonitor >=0.16,<1"',
        ):
            with self.subTest(replacement=replacement):
                self.write(
                    "devtools/conda-build/meta.yaml",
                    RECIPE.replace(', "smonitor >=0.16,<1"', replacement),
                )
                with self.assertRaisesRegex(native_conda.ContractError, "smonitor"):
                    self.inspect()

    def test_host_must_pin_python_and_abi3_to_same_floor(self):
        for old, new in (
            ('"python-abi3 3.11.*", ', ""),
            ("python-abi3 3.11.*", "python-abi3 3.12.*"),
            ("python 3.11.*", "python >=3.11"),
            ("python 3.11.*", "python 3.14.*"),
        ):
            with self.subTest(new=new):
                self.write("devtools/conda-build/meta.yaml", RECIPE.replace(old, new))
                with self.assertRaises(native_conda.ContractError):
                    self.inspect()

    def test_python_public_bounds_and_minor_specific_runtime_fail(self):
        for old, new in (
            ("python >=3.11,<3.15", "python >=3.11"),
            ("python >=3.11,<3.15", "python >=3.12,<3.15"),
            ('"smonitor >=0.16,<1"', '"smonitor >=0.16,<1", "python_abi 3.11.*"'),
        ):
            with self.subTest(new=new):
                self.write("devtools/conda-build/meta.yaml", RECIPE.replace(old, new))
                with self.assertRaises(native_conda.ContractError):
                    self.inspect()

    def test_native_identity_build_skip_noarch_and_multi_output_fail(self):
        for old, new in (
            ("name: example", "name: another"),
            ("\"{{ environ['MOLSYSSUITE_CONDA_VERSION'] }}\"", '"1.2.4"'),
            ("{{ environ['MOLSYSSUITE_CONDA_BUILD_NUMBER'] }}", "3"),
            ("python_version_independent: true", "python_version_independent: false"),
            (
                "python_version_independent: true",
                "python_version_independent: true\n  noarch: python",
            ),
            (
                "python_version_independent: true",
                "python_version_independent: true\n  noarch_python: false",
            ),
            (
                "python_version_independent: true",
                "python_version_independent: true\n  skip: true",
            ),
            ("requirements:", "outputs: []\nrequirements:"),
        ):
            with self.subTest(new=new):
                self.write("devtools/conda-build/meta.yaml", RECIPE.replace(old, new))
                with self.assertRaises(native_conda.ContractError):
                    self.inspect()

    def test_selector_variants_fail_before_silent_platform_filtering(self):
        for selector in ("# [linux]", "#[linux]", "#\t[not win]"):
            with self.subTest(selector=selector):
                self.write(
                    "devtools/conda-build/meta.yaml",
                    RECIPE.replace(
                        "compiler('rust') }}", "compiler('rust') }} " + selector
                    ),
                )
                with self.assertRaisesRegex(native_conda.ContractError, "per-platform"):
                    self.inspect()

    def test_plan_floor_matrix_profile_and_staging_conditions_are_checked(self):
        for old, new in (
            ('profile = "native-abi3"', 'profile = "noarch-python"'),
            ('route = "staged"', 'route = "direct"'),
            ('"3.14"]', '"3.15"]'),
            ('["linux-64", "osx-arm64"]', '["noarch"]'),
        ):
            with self.subTest(new=new):
                self.write("devtools/conda-build/plan.toml", PLAN.replace(old, new))
                with self.assertRaises(native_conda.ContractError):
                    self.inspect()
        self.write("devtools/conda-build/plan.toml", PLAN)
        self.write("pyproject.toml", PROJECT.replace(">=3.11", ">=3.12"))
        with self.assertRaisesRegex(native_conda.ContractError, "floor"):
            self.inspect()

    def test_rendered_api_can_use_actual_recipe_without_assuming_source_binding(self):
        rendered = yaml.safe_load(
            RECIPE.replace("{{ compiler('rust') }}", "rust_linux-64")
            .replace("{{ environ['MOLSYSSUITE_CONDA_VERSION'] }}", "1.2.3")
            .replace("{{ environ['MOLSYSSUITE_CONDA_BUILD_NUMBER'] }}", "2")
            .replace("{{ PKG_HASH }}", "1234567")
            .replace("{{ PKG_BUILDNUM }}", "2")
            .replace("{{ PYTHON }}", "/build/bin/python")
        )
        project = tomllib.loads(PROJECT)["project"]
        plan = tomllib.loads(PLAN)
        result = native_conda.inspect_rendered_dependencies(
            rendered, project, plan, "3.11"
        )
        self.assertFalse(result["native_bytes_verified"])
        bad = copy.deepcopy(rendered)
        bad["requirements"]["run"] = ["python >=3.11,<3.15"]
        with self.assertRaisesRegex(native_conda.ContractError, "smonitor"):
            native_conda.inspect_rendered_dependencies(bad, project, plan, "3.11")

    def test_name_alias_is_explicit_and_keeps_bounds(self):
        self.write("pyproject.toml", PROJECT.replace("smonitor", "python-smonitor"))
        with self.assertRaisesRegex(native_conda.ContractError, "missing"):
            self.inspect()
        result = native_conda.inspect_recipe_dependencies(
            self.root,
            "devtools/conda-build/meta.yaml",
            "devtools/conda-build/plan.toml",
            "3.11",
            {"python-smonitor": "smonitor"},
        )
        self.assertEqual(result["scope"], "declared-native-abi3-dependencies")

    def test_path_escape_and_unclassified_recipe_remain_fail_closed(self):
        with self.assertRaises(native_conda.ContractError):
            native_conda.inspect_recipe_dependencies(
                self.root, "../meta.yaml", "devtools/conda-build/plan.toml", "3.11"
            )
        self.write("devtools/new/recipe.yaml", RECIPE)
        with self.assertRaisesRegex(native_conda.ContractError, "unclassified"):
            dependency_routes.audit(self.root)

    def test_noarch_validator_still_refuses_native_source(self):
        self.write(
            "devtools/conda-build/meta.yaml",
            RECIPE.replace("{{ compiler('rust') }}", "rust-compiler")
            .replace("{{ PKG_HASH }}", "1234567")
            .replace("{{ PKG_BUILDNUM }}", "2")
            .replace("{{ PYTHON }}", "python"),
        )
        with self.assertRaisesRegex(native_conda.ContractError, "noarch: python"):
            noarch_conda.inspect_recipe_dependencies(
                self.root,
                "devtools/conda-build/meta.yaml",
                {
                    "MOLSYSSUITE_CONDA_VERSION": "1.2.3",
                    "MOLSYSSUITE_CONDA_BUILD_NUMBER": "2",
                },
            )

    def test_cli_declared_only_is_explicit_and_default_checks_actual_metadata(self):
        self.write(
            "pyproject.toml", PROJECT.replace("smonitor", "nonexistent-native-provider")
        )
        self.write(
            "devtools/conda-build/meta.yaml",
            RECIPE.replace("smonitor", "nonexistent-native-provider"),
        )
        command = [
            sys.executable,
            "-B",
            dependency_routes.__file__,
            "--root",
            str(self.root),
        ]
        result = subprocess.run(
            command + ["--declared-only"], capture_output=True, text=True, check=False
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["qualification"], "declared-only")
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("nonexistent-native-provider", result.stdout)

    def test_context_schema_keeps_native_bytes_separate_from_installed_bounds(self):
        self.write(
            "devtools/conda-envs/test.yaml",
            'channels: [uibcdf, conda-forge]\ndependencies: ["python >=3.11,<3.15", "smonitor >=0.16,<1"]\n',
        )
        path = self.root / "devtools/dependency_routes.toml"
        path.write_text(
            path.read_text().replace("dependency-routes@2", "dependency-routes@3")
            + """
[[environments]]
path = "devtools/conda-envs/test.yaml"
kind = "runtime"
purpose = "test"
channel_priority = "strict"
reason = "Reviewed full runtime"
[[contexts]]
name = "ci-3.14"
environment = "devtools/conda-envs/test.yaml"
python_minor = "3.14"
sources = []
reason = "Public runtime context"
"""
        )
        result = dependency_routes.audit(
            self.root,
            context="ci-3.14",
            check_installed=True,
            python_version="3.14.7",
            distribution_for=lambda _: SimpleNamespace(version="0.16.0"),
        )
        self.assertEqual(result["qualification"], "declared-and-installed-context")
        self.assertEqual(result["routes"][0]["qualification"], "declared-only")
        self.assertFalse(result["routes"][0]["native_bytes_verified"])

    def test_unknown_macros_or_plan_environment_inputs_cannot_be_guessed(self):
        for old, new in (
            ("compiler('rust')", "compiler('unknown')"),
            ("{{ PYTHON }}", "{{ load_setup_py_data() }}"),
        ):
            with self.subTest(new=new):
                self.write("devtools/conda-build/meta.yaml", RECIPE.replace(old, new))
                with self.assertRaises(
                    (native_conda.ContractError, noarch_conda.TemplateError)
                ):
                    self.inspect()
        self.write("devtools/conda-build/meta.yaml", RECIPE)
        with self.assertRaisesRegex(native_conda.ContractError, "only explicit"):
            native_conda.inspect_recipe_dependencies(
                self.root,
                "devtools/conda-build/meta.yaml",
                "devtools/conda-build/plan.toml",
                "3.11",
                environment_from_plan={"SECRET": "token"},
            )

    def test_legacy_inventory_does_not_silently_adopt_native_kind(self):
        path = self.root / "devtools/dependency_routes.toml"
        path.write_text(
            path.read_text().replace("dependency-routes@2", "dependency-routes@1")
        )
        with self.assertRaisesRegex(native_conda.ContractError, "owned profile"):
            dependency_routes.audit(self.root)

    def test_resource_fields_cannot_imply_a_missing_native_resource_audit(self):
        path = self.root / "devtools/dependency_routes.toml"
        original = path.read_text()
        for field in ("resources", "resource_inventory", "python_build_section"):
            with self.subTest(field=field):
                path.write_text(original + f'{field} = "unverified"\n')
                with self.assertRaisesRegex(
                    native_conda.ContractError, "owned adapter"
                ):
                    dependency_routes.audit(self.root)

    def test_input_change_cannot_be_reported_with_a_new_unchecked_digest(self):
        render = native_conda.render_recipe

        def changed(*args, **kwargs):
            result = render(*args, **kwargs)
            self.write(
                "pyproject.toml", PROJECT.replace("smonitor>=0.16", "smonitor>=0.17")
            )
            return result

        with (
            patch.object(native_conda, "render_recipe", changed),
            self.assertRaisesRegex(native_conda.ContractError, "changed during"),
        ):
            self.inspect()
