"""Guard the shared development recipe, native bootstrap and coherent Qt stack."""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

import tomllib
import yaml

from devtools.scripts import development_environment

ROOT = Path(__file__).resolve().parents[1]
RECIPE = ROOT / "devtools/conda-envs/molsyssuite-dev-py314.yaml"


class DevelopmentEnvironmentTests(unittest.TestCase):
    def test_missing_native_or_python_build_tools_are_rejected(self):
        registry = tomllib.loads((ROOT / "suite.toml").read_text())
        recipe = yaml.safe_load(RECIPE.read_text())
        for dependency in (
            "git",
            "rust_linux-64>=1.97.1,<2",
            "setuptools",
            "setuptools-rust>=1.13,<2",
            "versioningit",
            "wheel",
        ):
            with self.subTest(dependency=dependency):
                changed = deepcopy(recipe)
                changed["dependencies"].remove(dependency)
                with self.assertRaisesRegex(ValueError, "required"):
                    development_environment.profile(registry, changed)

    def test_native_tools_cannot_fall_back_to_a_host_executable(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            prefix = root / "conda"
            host = root / "host"
            for directory in (prefix / "bin", host):
                directory.mkdir(parents=True)
                tool = directory / "rustc"
                tool.write_text("#!/bin/sh\nexit 0\n")
                tool.chmod(0o755)
            with (
                patch.dict(os.environ, {"PATH": str(host)}),
                self.assertRaisesRegex(ValueError, "active Conda prefix"),
            ):
                development_environment._prefix_tool("rustc", prefix)
            with patch.dict(os.environ, {"PATH": str(prefix / "bin")}):
                self.assertEqual(
                    development_environment._prefix_tool("rustc", prefix),
                    prefix / "bin/rustc",
                )
                with self.assertRaises(ValueError):
                    development_environment._prefix_tool("cargo", prefix)

    def test_toolchain_rejects_incomplete_records_before_compilation(self):
        with tempfile.TemporaryDirectory() as temporary:
            prefix = Path(temporary)
            (prefix / "conda-meta").mkdir()
            (prefix / "conda-meta/rust.json").write_text(
                json.dumps(
                    {
                        "name": "rust",
                        "version": "1.99.0",
                        "url": "https://conda.anaconda.org/conda-forge/linux-64/rust.conda",
                    }
                )
            )
            with (
                patch.object(development_environment.sys, "prefix", str(prefix)),
                patch.dict(os.environ, {"CONDA_PREFIX": str(prefix)}),
                patch.object(
                    development_environment,
                    "_prefix_tool",
                    return_value=prefix / "bin/tool",
                ),
                patch.object(development_environment.subprocess, "run") as run,
                self.assertRaisesRegex(ValueError, "complete conda-forge"),
            ):
                development_environment.verify_toolchain()
            run.assert_not_called()

    def test_toolchain_accepts_newer_rust_and_propagates_compile_failure_with_cleanup(
        self,
    ):
        with tempfile.TemporaryDirectory() as temporary:
            prefix = Path(temporary)
            (prefix / "conda-meta").mkdir()
            for name in development_environment.NATIVE_PACKAGES:
                (prefix / f"conda-meta/{name}.json").write_text(
                    json.dumps(
                        {
                            "name": name,
                            "version": "1.99.0",
                            "url": f"https://conda.anaconda.org/conda-forge/linux-64/{name}.conda",
                        }
                    )
                )
            work = None

            def fail_compile(args, **kwargs):
                nonlocal work
                work = Path(args[1]).parent
                self.assertTrue(work.exists())
                raise subprocess.CalledProcessError(1, args)

            with (
                patch.object(development_environment.sys, "prefix", str(prefix)),
                patch.dict(os.environ, {"CONDA_PREFIX": str(prefix)}),
                patch.object(
                    development_environment,
                    "_prefix_tool",
                    return_value=prefix / "bin/tool",
                ),
                patch.object(
                    development_environment.subprocess,
                    "check_output",
                    return_value="1.99.0",
                ),
                patch.object(
                    development_environment.subprocess, "run", side_effect=fail_compile
                ),
                self.assertRaises(subprocess.CalledProcessError),
            ):
                development_environment.verify_toolchain()
            self.assertIsNotNone(work)
            self.assertFalse(work.exists())

    def test_ci_verifies_native_tools_after_creating_and_activating_environment(self):
        workflow = yaml.safe_load(
            (ROOT / ".github/workflows/check-development-environment.yaml").read_text()
        )
        steps = workflow["jobs"]["fresh-linux"]["steps"]
        creation = next(
            i
            for i, step in enumerate(steps)
            if "setup-micromamba" in step.get("uses", "")
        )
        verification = next(
            i
            for i, step in enumerate(steps)
            if "development_environment.py toolchain" in step.get("run", "")
        )
        installation = next(
            i
            for i, step in enumerate(steps)
            if "development_environment.py install" in step.get("run", "")
        )
        self.assertLess(creation, verification)
        self.assertLess(verification, installation)
        self.assertEqual(steps[verification]["shell"], "bash -el {0}")
        self.assertIn("public-evidence/toolchain.json", steps[verification]["run"])
        self.assertFalse(
            any("cargo --version" in step.get("run", "") for step in steps[:creation])
        )

    def test_cargo_smoke_is_offline_with_a_disposable_cache(self):
        with tempfile.TemporaryDirectory() as temporary:
            prefix = Path(temporary)
            (prefix / "conda-meta").mkdir()
            for name in development_environment.NATIVE_PACKAGES:
                (prefix / f"conda-meta/{name}.json").write_text(
                    json.dumps(
                        {
                            "name": name,
                            "version": "1.99.0",
                            "url": f"https://conda.anaconda.org/conda-forge/linux-64/{name}.conda",
                        }
                    )
                )
            work = None

            def compile_smoke(args, **kwargs):
                nonlocal work
                if "build" not in args:
                    return
                work = Path(kwargs["cwd"])
                self.assertTrue(work.exists())
                self.assertIn("--offline", args)
                self.assertEqual(kwargs["env"]["CARGO_HOME"], str(work / "cargo-home"))
                self.assertEqual(
                    args[args.index("--target-dir") + 1], str(work / "target")
                )
                raise subprocess.CalledProcessError(1, args)

            def output(args, **kwargs):
                return "conda-c-ok\n" if str(args[0]).endswith("c-smoke") else "1.99.0"

            with (
                patch.object(development_environment.sys, "prefix", str(prefix)),
                patch.dict(
                    os.environ,
                    {"CONDA_PREFIX": str(prefix), "CARGO_HOME": "/caller-cache"},
                ),
                patch.object(
                    development_environment,
                    "_prefix_tool",
                    return_value=prefix / "bin/tool",
                ),
                patch.object(
                    development_environment.subprocess,
                    "check_output",
                    side_effect=output,
                ),
                patch.object(
                    development_environment.subprocess, "run", side_effect=compile_smoke
                ),
                self.assertRaises(subprocess.CalledProcessError),
            ):
                development_environment.verify_toolchain()
            self.assertIsNotNone(work)
            self.assertFalse(work.exists())

    def test_incompatible_source_metadata_fails_before_git_or_installation(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "example"
            source.mkdir()
            (source / "pyproject.toml").write_text(
                '[project]\nname = "example"\nrequires-python = ">=3.11,<3.14"\n'
            )
            plan = {"included": [{"name": "example", "repository": "uibcdf/example"}]}
            with (
                patch.object(development_environment.subprocess, "check_output") as git,
                self.assertRaisesRegex(ValueError, "metadata excludes"),
            ):
                development_environment.source_inventory(plan, Path(temporary))
            git.assert_not_called()

    def test_profile_distinguishes_development_authorization_from_public_admission(
        self,
    ):
        registry = tomllib.loads((ROOT / "suite.toml").read_text())
        plan = development_environment.profile(
            registry, yaml.safe_load(RECIPE.read_text())
        )
        states = {item["name"]: item["state"] for item in plan["included"]}
        self.assertEqual(states["molsysmt"], "admitted")
        self.assertEqual(states["molsysviewer"], "admitted")
        self.assertEqual(states["opencastp"], "admitted")
        self.assertEqual(states["ackredit"], "admitted")
        for name in ("lindelint", "elastnetmt", "pharmacophoremt", "dockingmt"):
            self.assertEqual(states[name], "authorized")
        self.assertEqual(len(states), 14)
        self.assertEqual(set(plan["excluded"]), {"topomt", "peptidemt"})

    def test_hidden_channels_pip_subsections_and_qt_forks_are_rejected(self):
        registry = tomllib.loads((ROOT / "suite.toml").read_text())
        recipe = yaml.safe_load(RECIPE.read_text())
        mutations = [
            {"channels": ["file:///private/channel", "conda-forge"]},
            {"dependencies": recipe["dependencies"] + [{"pip": ["private-package"]}]},
            {"dependencies": recipe["dependencies"] + ["pyside6-addons-uibcdf=6.10.1"]},
            {"dependencies": recipe["dependencies"] + ["private::package"]},
        ]
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                changed = deepcopy(recipe)
                changed.update(mutation)
                with self.assertRaises(ValueError):
                    development_environment.profile(registry, changed)

    def test_editable_install_keeps_the_conda_solution_and_propagates_pip_failure(self):
        with patch.object(development_environment.subprocess, "run") as run:
            development_environment.install_editables([{"path": "/tmp/example"}])
        args = run.call_args_list[0].args[0]
        self.assertIn("--no-deps", args)
        self.assertIn("--no-build-isolation", args)
        self.assertEqual(args[-2:], ["-e", "/tmp/example"])
        self.assertEqual(run.call_args_list[1].args[0][-2:], ["pip", "check"])
        with (
            patch.object(
                development_environment.subprocess,
                "run",
                side_effect=subprocess.CalledProcessError(1, args),
            ),
            self.assertRaises(subprocess.CalledProcessError),
        ):
            development_environment.install_editables([{"path": "/tmp/example"}])

    def test_python_314_recipe_uses_only_the_official_aligned_qt_family(self):
        recipe = yaml.safe_load(RECIPE.read_text(encoding="utf-8"))
        dependencies = set(recipe["dependencies"])

        self.assertEqual(recipe["name"], "molsyssuite@uibcdf_3.14")
        self.assertIn("python=3.14", dependencies)
        self.assertEqual(
            {
                dependency
                for dependency in dependencies
                if dependency.startswith(
                    ("pyside6=", "qt6-webengine=", "qt6-positioning=")
                )
            },
            {"pyside6=6.11.2", "qt6-webengine=6.11.2", "qt6-positioning=6.11.2"},
        )
        self.assertFalse(any("-uibcdf" in dependency for dependency in dependencies))
        self.assertTrue({"python-build", "imageio"} <= dependencies)


if __name__ == "__main__":
    unittest.main()
