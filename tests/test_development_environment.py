"""Guard the shared Python 3.14 development recipe's coherent Qt stack."""

from __future__ import annotations

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
        self.assertEqual(states["molsysmt"], "authorized")
        self.assertEqual(states["molsysviewer"], "authorized")
        self.assertEqual(states["opencastp"], "admitted")
        self.assertEqual(states["ackredit"], "authorized")
        self.assertEqual(len(states), 10)
        self.assertEqual(
            set(plan["excluded"]),
            {
                "dockingmt",
                "elastnetmt",
                "lindelint",
                "pharmacophoremt",
                "topomt",
            },
        )

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
        import subprocess

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
