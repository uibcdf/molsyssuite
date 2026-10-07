"""Regression guards for selective generation and checked manager operations."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import yaml

from devtools.scripts import conda_environment_tools as tools


class EnvironmentToolsTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.write(
            "pyproject.toml",
            """
[project]
name = "fixture"
requires-python = ">=3.11,<3.15"
dependencies = ["numpy>=2,<3", "provider>=1,<2"]
""",
        )
        self.production = "devtools/conda-envs/production.yaml"
        self.development = "devtools/conda-envs/development.yaml"
        self.science = "devtools/conda-envs/science.yaml"
        self.build = "devtools/conda-envs/build.yaml"
        for name in (self.production, self.science, self.build):
            self.write(
                name,
                yaml.safe_dump(
                    {
                        "name": "ignored",
                        "channels": ["uibcdf", "conda-forge"],
                        "dependencies": ["python>=3.11,<3.15", "pip", "numpy>=2,<3"]
                        + ([] if name == self.science else ["provider>=1,<2"]),
                    },
                    sort_keys=False,
                ),
            )
        self.write(
            self.development,
            (self.root / self.production)
            .read_text()
            .replace("python>=3.11,<3.15", "python=3.14"),
        )
        manifest = "devtools/requirements/sources.txt"
        self.write(
            manifest,
            "provider @ git+https://github.com/example/provider.git@" + "a" * 40 + "\n",
        )
        inventory = f'''schema = "molsyssuite.dependency-routes@3"
reason = "Fixture proof"
[[source_routes]]
id = "provider-fixed"
name = "provider"
role = "required-runtime"
url = "https://github.com/example/provider"
commit = "{"a" * 40}"
install = "pip-no-deps-git"
input = "{manifest}"
reason = "Reviewed fixed source"
[[source_inputs]]
path = "{manifest}"
sha256 = "{hashlib.sha256((self.root / manifest).read_bytes()).hexdigest()}"
reason = "Reviewed input"
'''
        for path, purpose, minor, sources in (
            (self.production, "production", "3.14", []),
            (self.development, "development", "3.14", []),
            (self.science, "test", "3.13", ["provider-fixed"]),
        ):
            inventory += f'''
[[environments]]
path = "{path}"
kind = "runtime"
purpose = "{purpose}"
channel_priority = "strict"
narrowing_reason = "Explicit fixture minor"
reason = "Reviewed fixture"
[[contexts]]
name = "{purpose}-{minor}"
environment = "{path}"
python_minor = "{minor}"
sources = {json.dumps(sources)}
overlays = []
reason = "Reviewed source/context selection"
'''
        inventory += f'''
[[environments]]
path = "{self.build}"
kind = "build-only"
reason = "Owner build tools"
'''
        self.write("devtools/dependency_routes.toml", inventory)
        self.write(
            "devtools/tools.yaml",
            """
runtime:
  channels: &channels [uibcdf, conda-forge]
  dependencies: [pip]
build:
  channels: *channels
  dependencies: [pip, numpy>=2,<3, provider>=1,<2]
""".replace(
                "dependencies: [pip, numpy>=2,<3, provider>=1,<2]",
                'dependencies: [pip, "numpy>=2,<3", "provider>=1,<2"]',
            ),
        )
        profile = f'''schema = "{tools.SCHEMA}"
tooling = "devtools/tools.yaml"
'''
        for path in (self.production, self.development, self.build):
            profile += f'''
[[environments]]
path = "{path}"
group = "{"build" if path == self.build else "runtime"}"
reason = "Explicit owner selection"
'''
            if path == self.development:
                profile += 'python_minor = "3.14"\n'
        self.write(tools.DEFAULT_PROFILE, profile)
        self.write(
            "devtools/conda-build/meta.yaml", "{% set marker = 'do not parse' %}\n"
        )
        self.write("devtools/conda-build/release_plan.toml", 'version = "0.0.0"\n')

    def write(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path

    def snapshot(self):
        return {
            str(p.relative_to(self.root)): p.read_bytes()
            for p in self.root.rglob("*")
            if p.is_file()
        }

    def test_generation_is_selective_preserves_inputs_and_propagates_metadata(self):
        before = self.snapshot()
        changed = tools.generate(self.root)
        self.assertEqual(set(changed), {self.production, self.development, self.build})
        self.assertEqual([], tools.generate(self.root, check=True))
        after = self.snapshot()
        for name in set(before) - set(changed):
            self.assertEqual(before[name], after[name])
        content = yaml.safe_load(after[self.production])
        self.assertIn("numpy<3,>=2", content["dependencies"])
        self.assertIn("provider<2,>=1", content["dependencies"])
        self.assertNotIn("name", content)
        self.write(
            "pyproject.toml",
            (self.root / "pyproject.toml")
            .read_text()
            .replace("numpy>=2,<3", "numpy>=2.1,<3"),
        )
        self.assertIn(
            "numpy<3,>=2.1",
            yaml.safe_load(tools.environment_documents(self.root)[self.production])[
                "dependencies"
            ],
        )

    def test_check_and_late_invalid_output_never_write(self):
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, "differ"):
            tools.generate(self.root, check=True)
        self.assertEqual(before, self.snapshot())
        self.write(
            "devtools/tools.yaml",
            (self.root / "devtools/tools.yaml")
            .read_text()
            .replace('"provider>=1,<2"', '"python=3.7"'),
        )
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, "metadata/context"):
            tools.generate(self.root)
        self.assertEqual(before, self.snapshot())

    def test_protected_unregistered_duplicate_and_symlink_targets_fail(self):
        original = (self.root / tools.DEFAULT_PROFILE).read_text()
        for value in (
            "devtools/conda-build/meta.yaml",
            "../outside.yaml",
            "devtools/conda-envs/unregistered.yaml",
        ):
            with self.subTest(value=value):
                self.write(
                    tools.DEFAULT_PROFILE, original.replace(self.production, value)
                )
                with self.assertRaises((ValueError, FileNotFoundError)):
                    tools.generate(self.root)
        self.write(tools.DEFAULT_PROFILE, original.replace(self.build, self.production))
        with self.assertRaisesRegex(ValueError, "duplicate"):
            tools.generate(self.root)
        self.write(tools.DEFAULT_PROFILE, original)
        path = self.root / self.production
        path.unlink()
        path.symlink_to(self.root / self.science)
        with self.assertRaisesRegex(ValueError, "symlink"):
            tools.generate(self.root)

    def test_routine_minor_patch_build_and_existing_scientific_ranges_are_preserved(
        self,
    ):
        with self.assertRaisesRegex(ValueError, "routine"):
            tools.selected_environment(self.root, self.development, "3.13")
        for selector in (
            "python>=3.14.2,<3.15",
            "python=3.14.2=build_0",
            "python=3.13",
        ):
            self.write(
                self.production,
                yaml.safe_dump(
                    {
                        "channels": ["uibcdf", "conda-forge"],
                        "dependencies": [selector, "numpy>=2,<3", "provider>=1,<2"],
                    }
                ),
            )
            with self.subTest(selector=selector), self.assertRaises(ValueError):
                tools.selected_environment(self.root, self.production, "3.14")
        self.write(
            self.production,
            yaml.safe_dump(
                {
                    "channels": ["uibcdf", "conda-forge"],
                    "dependencies": [
                        "python>=3.11,<3.15",
                        "numpy>=2.2,<3",
                        "provider>=1,<2",
                    ],
                }
            ),
        )
        with self.assertRaisesRegex(ValueError, "violates"):
            tools.generate(self.root)

    def test_source_minor_origin_and_manifest_controls_are_reused(self):
        selected = tools.selected_environment(self.root, self.science, "3.13")
        self.assertNotIn("provider", " ".join(selected["dependencies"]))
        with self.assertRaisesRegex(ValueError, "fixed-source"):
            tools.selected_environment(self.root, self.science, "3.14")
        self.write(
            "devtools/requirements/sources.txt",
            "git+https://github.com/example/provider@main\n",
        )
        with self.assertRaisesRegex(ValueError, "source input changed"):
            tools.environment_documents(self.root)

    def test_generation_can_reuse_source_context_without_inventing_public_bootstrap(
        self,
    ):
        profile = (self.root / tools.DEFAULT_PROFILE).read_text()
        self.write(
            tools.DEFAULT_PROFILE,
            profile
            + f'''
[[environments]]
path = "{self.science}"
group = "runtime"
reason = "Explicit existing source-context generation"
''',
        )
        self.assertNotIn(
            "provider",
            " ".join(
                yaml.safe_load(tools.environment_documents(self.root)[self.science])[
                    "dependencies"
                ]
            ),
        )

    def test_runtime_tool_duplicates_channel_and_special_fields_require_review(self):
        original = (self.root / "devtools/tools.yaml").read_text()
        for altered in (
            original.replace("dependencies: [pip]", 'dependencies: ["numpy>=2,<3"]'),
            original.replace("[uibcdf, conda-forge]", "[defaults]"),
        ):
            self.write("devtools/tools.yaml", altered)
            with self.assertRaises(ValueError):
                tools.environment_documents(self.root)
        self.write("devtools/tools.yaml", original)
        self.write(
            self.production,
            (self.root / self.production).read_text()
            + "variables: {SCIENCE: special}\n",
        )
        with self.assertRaisesRegex(ValueError, "specialized"):
            tools.environment_documents(self.root)

    def test_create_vectors_strict_priority_cleanup_and_failure_propagation(self):
        def execute(argv, **kwargs):
            self.assertTrue(kwargs["check"])
            self.assertNotIn("shell", kwargs)
            self.assertEqual("strict", kwargs["env"]["CONDA_CHANNEL_PRIORITY"])
            if "list" in argv:
                return subprocess.CompletedProcess(argv, 0, stdout='{"envs": []}')
            manifest = Path(argv[-1])
            captured.append(manifest)
            self.assertEqual("--name", argv[3])
            self.assertEqual("fixture@3.14", argv[4])
            self.assertEqual(
                ["python>=3.14,<3.15"],
                [
                    v
                    for v in yaml.safe_load(manifest.read_text())["dependencies"]
                    if v.startswith("python")
                ],
            )
            raise subprocess.CalledProcessError(7, argv)

        captured = []
        before = self.snapshot()
        with (
            patch.object(tools.shutil, "which", return_value="/explicit/mamba"),
            patch.object(tools.subprocess, "run", side_effect=execute),
            self.assertRaises(subprocess.CalledProcessError),
        ):
            tools.apply_environment(
                self.root, self.production, "3.14", manager="mamba", name="fixture@3.14"
            )
        self.assertEqual(before, self.snapshot())
        self.assertEqual(1, len(captured))
        self.assertFalse(captured[0].exists())

    def test_create_occupied_names_invalid_targets_and_missing_manager_fail(self):
        runner = Mock(
            return_value=subprocess.CompletedProcess(
                [], 0, stdout='{"envs": ["/envs/occupied"]}'
            )
        )
        with (
            patch.object(tools.shutil, "which", return_value="/conda"),
            patch.object(tools.subprocess, "run", runner),
        ):
            with self.assertRaisesRegex(ValueError, "unoccupied"):
                tools.apply_environment(
                    self.root, self.production, "3.14", manager="conda", name="occupied"
                )
            self.assertEqual(1, runner.call_count)
        for name in ("base", "bad;name", "-option"):
            with self.assertRaisesRegex(ValueError, "invalid"):
                tools.apply_environment(
                    self.root, self.production, "3.14", manager="conda", name=name
                )
        with self.assertRaisesRegex(ValueError, "exactly one"):
            tools.apply_environment(self.root, self.production, "3.14", manager="conda")
        with (
            patch.object(tools.shutil, "which", return_value=None),
            self.assertRaisesRegex(ValueError, "manager"),
        ):
            tools.apply_environment(
                self.root, self.production, "3.14", manager="missing", name="new"
            )

    def test_update_requires_active_interpreter_and_never_prunes_implicitly(self):
        prefix = self.root / "active"
        (prefix / "conda-meta").mkdir(parents=True)
        with self.assertRaisesRegex(ValueError, "active"):
            tools.apply_environment(
                self.root, self.production, "3.14", manager="conda", prefix=prefix
            )
        runner = Mock()
        with (
            patch.dict(os.environ, {"CONDA_PREFIX": str(prefix)}),
            patch.object(sys, "prefix", str(prefix)),
            patch.object(tools.shutil, "which", return_value="/conda"),
            patch.object(tools.subprocess, "run", runner),
        ):
            result = tools.apply_environment(
                self.root, self.production, "3.14", manager="conda", prefix=prefix
            )
        argv = runner.call_args.args[0]
        self.assertEqual(["/conda", "env", "update", "--prefix", str(prefix)], argv[:5])
        self.assertNotIn("--prune", argv)
        self.assertEqual("update", result["operation"])
        self.assertFalse(Path(argv[-1]).exists())

    def test_import_is_inert_even_with_cli_arguments(self):
        spec = importlib.util.spec_from_file_location(
            "inert_environment_tools", tools.__file__
        )
        module = importlib.util.module_from_spec(spec)
        with (
            patch.object(sys, "argv", ["tool", "--invalid"]),
            patch.object(
                subprocess,
                "run",
                side_effect=AssertionError("manager invoked at import"),
            ),
            patch.object(
                Path, "write_text", side_effect=AssertionError("write at import")
            ),
        ):
            spec.loader.exec_module(module)

    def test_cli_check_failure_is_nonmutating_outside_owner(self):
        before = self.snapshot()
        result = subprocess.run(
            [
                sys.executable,
                tools.__file__,
                "--root",
                str(self.root),
                "generate",
                "--check",
            ],
            cwd="/tmp",
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(1, result.returncode)
        self.assertIn("differ", result.stderr)
        self.assertEqual(before, self.snapshot())


if __name__ == "__main__":
    unittest.main()
