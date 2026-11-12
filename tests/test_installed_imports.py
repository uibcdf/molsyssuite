"""Guard every declared runtime root against source and escaped imports."""

import importlib
import json
import os
import pickle
import shutil
import subprocess
import sys
import tempfile
import textwrap
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

    def isolated_sdk(self, layout, code, replacements=None):
        """Exercise the actual three-file reader SDK without site packages."""
        with tempfile.TemporaryDirectory(dir=self.base) as temporary:
            root = Path(temporary)
            scripts = root / "devtools/scripts" if layout == "repository" else root
            scripts.mkdir(parents=True, exist_ok=True)
            owner = Path(__file__).resolve().parents[1] / "devtools/scripts"
            for name in (
                "installed_imports.py",
                "conda_release_contract.py",
                "verify_public_conda.py",
            ):
                shutil.copyfile(owner / name, scripts / name)
            for name, content in (replacements or {}).items():
                (scripts / name).write_text(content)
            return subprocess.run(
                [
                    sys.executable,
                    "-I",
                    "-S",
                    "-c",
                    textwrap.dedent(code),
                    str(root),
                    layout,
                    str(self.prefix),
                    str(self.source),
                ],
                cwd=self.base,
                capture_output=True,
                text=True,
                timeout=15,
                check=False,
            )

    def test_minimal_sdk_checks_real_origins_in_both_import_layouts(self):
        (self.prefix / "minimal_runtime.py").write_text("value = 'installed'\n")
        (self.source / "minimal_runtime.py").write_text("value = 'source'\n")
        code = """\
            import importlib, importlib.util, json, sys
            from pathlib import Path
            sys.path.insert(0, sys.argv[1])
            stem = 'devtools.scripts.' if sys.argv[2] == 'repository' else ''
            checker = importlib.import_module(stem + 'installed_imports')
            contract = importlib.import_module(stem + 'conda_release_contract')
            assert checker.ContractError is contract.ContractError
            assert checker.ContractError.__module__ == stem + 'conda_release_contract'
            assert issubclass(checker.ContractError, ValueError)
            prefix, source = map(Path, sys.argv[3:5])
            sys.path.insert(0, str(prefix))
            import minimal_runtime
            sys.path.pop(0)
            assert minimal_runtime.value == 'installed'
            roots = checker.runtime_import_roots({}, 'minimal_runtime')
            result = checker.check_installed_imports(roots, prefix, source)
            assert result['state'] == 'verified-loaded-imports'
            assert result['loaded'] == ['minimal_runtime']
            spec = importlib.util.spec_from_file_location(
                'minimal_runtime', source / 'minimal_runtime.py')
            shadow = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(shadow)
            assert shadow.value == 'source'
            sys.modules['minimal_runtime'] = shadow
            try:
                checker.check_installed_imports(roots, prefix, source)
            except contract.ContractError as error:
                assert 'from source' in str(error)
            else:
                raise AssertionError('source import accepted')
            checker.check_installed_imports(('unloaded_optional',), prefix, source)
            assert 'unloaded_optional' not in sys.modules
            for name in ('yaml', 'jinja2', 'markupsafe', 'packaging',
                         stem + 'noarch_conda'):
                assert name not in sys.modules, name
            print(json.dumps({'state': 'verified', 'layout': sys.argv[2]}))
        """
        for layout in ("repository", "scripts"):
            with self.subTest(layout=layout):
                result = self.isolated_sdk(layout, code)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual(json.loads(result.stdout)["state"], "verified")

    def test_minimal_sdk_preserves_transitive_missing_dependency(self):
        code = """\
            import importlib, sys
            sys.path.insert(0, sys.argv[1])
            stem = 'devtools.scripts.' if sys.argv[2] == 'repository' else ''
            try:
                importlib.import_module(stem + 'installed_imports')
            except ModuleNotFoundError as error:
                assert error.name == 'missing_sdk_dependency', repr(error)
            else:
                raise AssertionError('missing dependency was suppressed')
        """
        for layout in ("repository", "scripts"):
            for sibling in ("conda_release_contract.py", "verify_public_conda.py"):
                with self.subTest(layout=layout, sibling=sibling):
                    result = self.isolated_sdk(
                        layout,
                        code,
                        {
                            sibling: "raise ModuleNotFoundError('missing transitive dependency', "
                            "name='missing_sdk_dependency')\n"
                        },
                    )
                    self.assertEqual(
                        result.returncode, 0, result.stdout + result.stderr
                    )

    def test_contract_error_keeps_identity_and_pickle_compatibility(self):
        from devtools.scripts import conda_release_contract, noarch_conda

        error_type = self.provider().ContractError
        self.assertIs(error_type, conda_release_contract.ContractError)
        self.assertIs(error_type, noarch_conda.ContractError)
        self.assertIs(error_type, installed_noarch.ContractError)
        original = error_type("original contract failure")
        restored = pickle.loads(pickle.dumps(original))
        self.assertIs(type(restored), error_type)
        self.assertEqual(restored.args, original.args)

    def test_workflow_audit_preserves_its_missing_yaml_dependency(self):
        code = """\
            import importlib, sys
            from pathlib import Path
            sys.path.insert(0, sys.argv[1])
            stem = 'devtools.scripts.' if sys.argv[2] == 'repository' else ''
            contract = importlib.import_module(stem + 'conda_release_contract')
            try:
                contract.workflow_findings(Path(sys.argv[4]))
            except ModuleNotFoundError as error:
                assert error.name == 'yaml', repr(error)
            else:
                raise AssertionError('workflow analysis accepted absent PyYAML')
        """
        for layout in ("repository", "scripts"):
            with self.subTest(layout=layout):
                result = self.isolated_sdk(layout, code)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

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
