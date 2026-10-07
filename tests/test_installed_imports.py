"""Guard every declared runtime root against source and escaped imports."""

import importlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from devtools.scripts import installed_noarch


class InstalledImportTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.prefix = self.base / "prefix"
        self.source = self.base / "source"
        self.prefix.mkdir()
        self.source.mkdir()

    def provider(self):
        return importlib.import_module("devtools.scripts.installed_imports")

    def test_resource_roots_include_addons_and_modules_but_not_data(self):
        inventory = {
            "import_name": "core",
            "required_paths": [
                "site-packages/core/_version.py",
                "site-packages/addon/__init__.py",
                "site-packages/standalone.py",
                "site-packages/data/example.json",
            ],
        }
        self.assertEqual(
            self.provider().runtime_import_roots(inventory, "fallback"),
            ("core", "addon", "standalone"),
        )

    def test_explicit_roots_cannot_omit_declared_payload(self):
        inventory = {
            "import_name": "core",
            "required_paths": ["site-packages/addon/__init__.py"],
            "import_roots": ["core"],
        }
        with self.assertRaisesRegex(installed_noarch.ContractError, "omit"):
            self.provider().runtime_import_roots(inventory, "fallback")
        inventory["import_roots"].append("addon")
        self.assertEqual(
            self.provider().runtime_import_roots(inventory, "fallback"),
            ("core", "addon"),
        )

    def test_legacy_primary_and_invalid_root_declarations(self):
        api = self.provider()
        self.assertEqual(api.runtime_import_roots({}, "core"), ("core",))
        for roots in ([], "core", ["core", "core"], ["../source"], [True]):
            with (
                self.subTest(roots=roots),
                self.assertRaises(installed_noarch.ContractError),
            ):
                api.runtime_import_roots({"import_roots": roots}, "core")

    def test_loaded_descendant_and_namespace_paths_are_checked(self):
        api = self.provider()
        modules = {
            "core": SimpleNamespace(__file__=str(self.prefix / "core.py")),
            "addon": SimpleNamespace(
                __file__=None, __path__=[str(self.prefix / "addon")]
            ),
            "addon.child": SimpleNamespace(
                __file__=str(self.prefix / "addon/child.py")
            ),
        }
        with patch.dict(sys.modules, modules):
            api.check_installed_imports(("core", "addon"), self.prefix, self.source)
            modules["addon.child"].__file__ = str(self.source / "addon/child.py")
            with self.assertRaisesRegex(installed_noarch.ContractError, "addon.child"):
                api.check_installed_imports(("core", "addon"), self.prefix, self.source)

    def test_direct_checker_rejects_ambiguous_root_arguments(self):
        api = self.provider()
        for roots in ("core", (), ("core", "core"), ("../source",), (None,)):
            with (
                self.subTest(roots=roots),
                self.assertRaises(installed_noarch.ContractError),
            ):
                api.check_installed_imports(roots, self.prefix, self.source)

    def test_mixed_namespace_paths_and_unknown_origins_are_rejected(self):
        api = self.provider()
        for module in (
            SimpleNamespace(
                __file__=None, __path__=[str(self.prefix), str(self.source)]
            ),
            SimpleNamespace(__file__=None),
        ):
            with (
                self.subTest(module=module),
                patch.dict(sys.modules, {"addon": module}),
                self.assertRaises(installed_noarch.ContractError),
            ):
                api.check_installed_imports(("addon",), self.prefix, self.source)

    def test_source_inside_prefix_and_symlink_escape_are_rejected(self):
        api = self.provider()
        nested_source = self.prefix / "checkout"
        module = SimpleNamespace(__file__=str(nested_source / "core.py"))
        with (
            patch.dict(sys.modules, {"core": module}),
            self.assertRaises(installed_noarch.ContractError),
        ):
            api.check_installed_imports(("core",), self.prefix, nested_source)
        outside = self.base / "outside.py"
        outside.touch()
        link = self.prefix / "core.py"
        link.symlink_to(outside)
        module.__file__ = str(link)
        with (
            patch.dict(sys.modules, {"core": module}),
            self.assertRaises(installed_noarch.ContractError),
        ):
            api.check_installed_imports(("core",), self.prefix, self.source)

    def test_unloaded_optional_addon_is_not_imported(self):
        # Selecting roots must not import optional integrations or their dependencies.
        with patch.object(
            importlib, "import_module", side_effect=AssertionError("import")
        ):
            from devtools.scripts.installed_imports import check_installed_imports

            check_installed_imports(
                ("unused_optional_addon",), self.prefix, self.source
            )

    def execute_fixture(self, test_body, *, preload_addon=False, args=()):
        tests = self.source / "tests"
        tests.mkdir()
        (self.source / "pyproject.toml").write_text(
            '[tool.pytest.ini_options]\npythonpath = ["."]\n'
        )
        for directory, value in ((self.source, "source"), (self.prefix, "installed")):
            for name in ("demo_runtime", "demo_addon"):
                (directory / (name + ".py")).write_text(f'value = "{value}"\n')
        (tests / "test_selection.py").write_text(test_body)
        inventory = {
            "import_name": "demo_runtime",
            "required_paths": [
                "site-packages/demo_runtime.py",
                "site-packages/demo_addon.py",
            ],
            "installed_tests": {"paths": ["tests"], "pytest_args": list(args)},
        }
        command = (
            "import json,sys; from pathlib import Path; "
            "sys.path.insert(0,sys.argv[1]); "
            "from devtools.scripts.installed_noarch import run_tests; "
            "sys.prefix=sys.argv[2]; sys.path.insert(0,sys.prefix); "
            "__import__('demo_runtime'); "
        )
        if preload_addon:
            command += "sys.path.insert(0,sys.argv[3]); __import__('demo_addon'); sys.path.pop(0); "
        command += (
            "raise SystemExit(run_tests(Path(sys.argv[3]),json.loads(sys.argv[4])))"
        )
        environment = dict(os.environ, PYTEST_DISABLE_PLUGIN_AUTOLOAD="1")
        environment.pop("PYTEST_ADDOPTS", None)
        return subprocess.run(
            [
                sys.executable,
                "-P",
                "-c",
                command,
                str(Path(__file__).resolve().parents[1]),
                str(self.prefix),
                str(self.source),
                json.dumps(inventory),
            ],
            cwd=self.base,
            env=environment,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )

    def test_actual_runner_clears_inherited_pythonpath_for_installed_addon(self):
        result = self.execute_fixture(
            "def test_origin():\n    import demo_addon\n    assert demo_addon.value == 'installed'\n"
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_actual_runner_rejects_cached_source_addon_before_tests(self):
        result = self.execute_fixture(
            "def test_true():\n    assert True\n", preload_addon=True
        )
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("demo_addon", result.stdout + result.stderr)

    def test_component_args_cannot_restore_source_path_or_prepend_collection(self):
        result = self.execute_fixture(
            "def test_origin():\n    import demo_addon\n    assert demo_addon.value == 'installed'\n",
            args=("-o", "pythonpath=.", "--import-mode=prepend"),
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_actual_runner_rejects_addon_shadow_loaded_during_tests(self):
        result = self.execute_fixture(
            "import sys\nfrom pathlib import Path\n"
            "def test_true():\n"
            "    sys.path.insert(0,str(Path(__file__).resolve().parents[1]))\n"
            "    import demo_addon\n    assert demo_addon.value == 'source'\n"
        )
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("demo_addon", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
