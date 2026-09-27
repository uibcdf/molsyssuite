"""Guard the shared Python 3.14 development recipe's coherent Qt stack."""

from __future__ import annotations

import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
RECIPE = ROOT / "devtools/conda-envs/molsyssuite-dev-py314.yaml"


class DevelopmentEnvironmentTests(unittest.TestCase):
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
