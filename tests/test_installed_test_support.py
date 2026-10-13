"""Guard explicit support bytes, origin, source binding and owned lifecycle."""

import copy
import hashlib
import importlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import ModuleType
from unittest.mock import patch

from devtools.scripts import installed_test_support as support


class SupportTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="suite117-unit-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.namespace = "suite117_test_support"
        self.declaration = {"schema": support.SCHEMA, "namespace": self.namespace,
                            "reason": "Reviewed fixture", "files": []}
        self.file(self.namespace + "/helper.py", "from .neighbor import VALUE\n")
        self.file(self.namespace + "/neighbor.py", "VALUE = 'reviewed'\n")
        self.file("tests/data/control.txt", "fixture")
        self.runtime = ("suite117_runtime", "suite117_addon")

    def file(self, relative, data, *, target=None):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(data)
        self.declaration["files"].append({"source": relative, "target": target or relative,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
        return path

    def test_plan_is_inert_and_stage_support_uses_normal_package_imports_without_parent_paths(self):
        before = list(sys.path)
        with patch.object(importlib, "import_module", side_effect=AssertionError("import")):
            plan = support.support_plan(self.root, self.declaration, self.runtime)
        self.assertEqual(3, len(plan["files"]))
        with support.staged_support(self.root, self.declaration, self.runtime) as stage:
            module = importlib.import_module(self.namespace + ".helper")
            self.assertEqual("reviewed", module.VALUE)
            self.assertEqual(before, sys.path)
            self.assertNotIn(str(stage.root), sys.path)
            self.assertEqual("fixture", (stage.root / "tests/data/control.txt").read_text())
            stage.check()
            root = stage.root
        self.assertFalse(root.exists())
        self.assertNotIn(self.namespace, sys.modules)
        self.assertTrue(stage.receipt["resources_retired"])
        self.assertTrue(stage.receipt["imports_retired"])
        self.assertEqual("unknown", stage.receipt["binding"]["source_state"])

    def test_regular_initializer_nested_namespace_and_late_test_failure_retire_owned_resources(self):
        self.file(self.namespace + "/__init__.py", "from .helper import VALUE\n")
        self.file(self.namespace + "/nested/leaf.py", "VALUE=42\n")
        sdk = sys.modules["devtools.scripts.installed_test_support"]
        with self.assertRaisesRegex(RuntimeError, "test failure"):
            with support.staged_support(self.root, self.declaration, self.runtime) as stage:
                self.assertEqual("reviewed", importlib.import_module(self.namespace).VALUE)
                self.assertEqual(42, importlib.import_module(self.namespace + ".nested.leaf").VALUE)
                root = stage.root
                raise RuntimeError("test failure")
        self.assertFalse(root.exists())
        self.assertFalse(any(name.startswith(self.namespace) for name in sys.modules))
        self.assertIs(sdk, sys.modules["devtools.scripts.installed_test_support"])

    def test_namespace_and_source_payload_collisions_fail_before_staging(self):
        for namespace in ("devtools", "pytest", "json", "tests", "suite117_runtime", "suite117_addon", "bad.name"):
            declaration = {**self.declaration, "namespace": namespace}
            with self.subTest(namespace=namespace), self.assertRaises(support.ContractError):
                support.support_plan(self.root, declaration, self.runtime)
        self.file("suite117_addon/private.py", "value=1\n", target=self.namespace + "/alias.py")
        with self.assertRaisesRegex(support.ContractError, "runtime payload source"):
            support.support_plan(self.root, self.declaration, self.runtime)

    def test_cached_resolvable_and_detached_child_collisions_preserve_caller_modules(self):
        old = ModuleType(self.namespace)
        for key in (self.namespace, self.namespace + ".old"):
            with patch.dict(sys.modules, {key: old}), self.assertRaisesRegex(support.ContractError, "already loaded"):
                with support.staged_support(self.root, self.declaration, self.runtime):
                    self.fail("collision admitted")
            self.assertNotIn(key, sys.modules)
        with patch.object(importlib.util, "find_spec", return_value=object()), self.assertRaisesRegex(support.ContractError, "resolvable"):
            with support.staged_support(self.root, self.declaration, self.runtime):
                self.fail("resolvable collision admitted")

    def test_invalid_file_hash_alias_target_and_executable_data_require_review(self):
        alterations = [
            {"source": "../escape.py"}, {"target": "/absolute.py"}, {"target": "."},
            {"target": "a/../b.txt"}, {"target": "C:\\bad"}, {"target": "NUL.txt"},
            {"target": "tests/data/hidden.py"}, {"target": "tests/data/hidden.PY"},
            {"target": "tests/data/hidden.pth"}, {"sha256": "a" * 64},
        ]
        for alteration in alterations:
            declaration = copy.deepcopy(self.declaration)
            declaration["files"][0].update(alteration)
            with self.subTest(alteration=alteration), self.assertRaises(support.ContractError):
                support.support_plan(self.root, declaration, self.runtime)
        declaration = copy.deepcopy(self.declaration)
        declaration["files"].append(declaration["files"][0])
        with self.assertRaisesRegex(support.ContractError, "duplicate"):
            support.support_plan(self.root, declaration, self.runtime)

    def test_symlink_size_and_module_package_collisions_are_nonmutating(self):
        path = self.root / self.declaration["files"][0]["source"]
        target = self.root / "original.py"
        path.rename(target); path.symlink_to(target)
        with self.assertRaisesRegex(support.ContractError, "symlink"):
            support.support_plan(self.root, self.declaration, self.runtime)
        path.unlink(); target.rename(path)
        with patch.object(support, "MAX_FILE_BYTES", 1), self.assertRaisesRegex(support.ContractError, "size"):
            support.support_plan(self.root, self.declaration, self.runtime)
        self.file(self.namespace + "/helper/__init__.py", "value=1\n")
        with self.assertRaisesRegex(support.ContractError, "module/package"):
            support.support_plan(self.root, self.declaration, self.runtime)

    def test_staged_data_and_helper_origin_mutations_fail_and_retire_everything(self):
        for mutation in ("data", "origin", "package-path"):
            with self.subTest(mutation=mutation), self.assertRaises(support.ContractError):
                with support.staged_support(self.root, self.declaration, self.runtime) as stage:
                    root = stage.root
                    module = importlib.import_module(self.namespace + ".helper")
                    if mutation == "data":
                        (stage.root / "tests/data/control.txt").write_text("changed")
                    elif mutation == "origin":
                        module.__file__ = str(self.root / self.namespace / "helper.py")
                    else:
                        sys.modules[self.namespace].__path__.append(str(self.root))
            self.assertFalse(root.exists())
            self.assertNotIn(self.namespace, sys.modules)
            self.assertTrue(stage.receipt["resources_retired"])

    def test_initializer_and_copy_failures_preserve_resources_and_caller_identities(self):
        self.file(self.namespace + "/__init__.py", "raise RuntimeError('initializer failed')\n")
        directories = []
        native = support.TemporaryDirectory
        def temporary(**kwargs):
            result = native(**kwargs); directories.append(Path(result.name)); return result
        with patch.object(support, "TemporaryDirectory", side_effect=temporary), self.assertRaisesRegex(RuntimeError, "initializer failed"):
            with support.staged_support(self.root, self.declaration, self.runtime):
                self.fail("initializer failure was hidden")
        self.assertTrue(directories)
        self.assertFalse(directories[0].exists())
        self.assertNotIn(self.namespace, sys.modules)
        directories.clear()
        with (
            patch.object(support, "TemporaryDirectory", side_effect=temporary),
            patch.object(Path, "write_bytes", side_effect=OSError("copy failed")),
            self.assertRaisesRegex(OSError, "copy failed"),
        ):
            with support.staged_support(self.root, self.declaration, self.runtime):
                self.fail("copy failure was hidden")
        self.assertFalse(directories[0].exists())
        self.assertNotIn(self.namespace, sys.modules)

    def test_missing_files_and_invalid_binding_fail_before_allocating_resources(self):
        contexts = ({"run_id": 0}, {"run_attempt": True}, {"candidate_sha": "main"},
                    {"sha256": "short"}, {"filename": "../artifact.tar.bz2"},
                    {"provider_sha": "a" * 40}, {"unknown": "value"})
        for context in contexts:
            with (
                self.subTest(context=context),
                patch.object(support, "TemporaryDirectory", side_effect=AssertionError("allocated")),
                self.assertRaises(support.ContractError),
            ):
                with support.staged_support(self.root, self.declaration, self.runtime, context=context):
                    self.fail("invalid binding admitted")
        (self.root / self.declaration["files"][0]["source"]).unlink()
        with self.assertRaisesRegex(support.ContractError, "missing"):
            support.support_plan(self.root, self.declaration, self.runtime)

    def test_source_commit_and_archive_identities_remain_distinct_and_exact(self):
        def git(*args):
            return subprocess.run(["git", "-C", str(self.root), *args], check=True,
                                  text=True, capture_output=True).stdout.strip()
        git("init", "-q"); git("add", ".")
        git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "fixture")
        candidate = git("rev-parse", "HEAD")
        context = {"candidate_sha": candidate, "qualification_sha": "b" * 40,
                   "filename": "candidate-1.0.0-py_0.tar.bz2", "sha256": "c" * 64,
                   "run_id": 123, "run_attempt": 2}
        with support.staged_support(self.root, self.declaration, self.runtime, context=context) as stage:
            self.assertEqual(context, {k:v for k,v in stage.receipt["binding"]["context"].items() if v is not None})
            self.assertEqual("verified-commit-and-selected-files", stage.receipt["binding"]["source_state"])
        with self.assertRaisesRegex(support.ContractError, "checked-out commit"):
            with support.staged_support(self.root, self.declaration, self.runtime, context={**context,"candidate_sha":"a"*40}):
                self.fail("wrong source admitted")
        path = self.root / self.namespace / "helper.py"
        path.write_text("VALUE='uncommitted'\n")
        declaration = copy.deepcopy(self.declaration)
        declaration["files"][0]["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        with self.assertRaisesRegex(support.ContractError, "bound source commit"):
            with support.staged_support(self.root, declaration, self.runtime, context=context):
                self.fail("dirty helper admitted as original source")


class SupportRunnerTests(unittest.TestCase):
    def fixture(self, case="positive"):
        with tempfile.TemporaryDirectory(prefix="suite117-runner-") as temporary:
            task = Path(temporary); root = task / "component"; prefix = task / "prefix"
            (root / "tests").mkdir(parents=True); prefix.mkdir()
            namespace = "suite117_runner_support"
            (root / namespace).mkdir()
            files = {
                namespace + "/helper.py": "from pathlib import Path\nfrom .neighbor import VALUE\nDATA=Path(__file__).resolve().parents[1]/'tests/data/control.txt'\n",
                namespace + "/neighbor.py": "VALUE='helper'\n",
                "tests/data/control.txt": "fixture",
            }
            for relative, text in files.items():
                path = root / relative; path.parent.mkdir(parents=True, exist_ok=True); path.write_text(text)
            for base, value in ((root, "source"), (prefix, "installed")):
                for name in ("suite117_runtime", "suite117_addon"):
                    (base / (name + ".py")).write_text(f"VALUE='{value}'\n")
            (root / "pyproject.toml").write_text('[tool.pytest.ini_options]\npythonpath=["."]\n')
            inventory = {"import_name":"suite117_runtime", "required_paths":["site-packages/suite117_runtime.py", "site-packages/suite117_addon.py"],
                "installed_tests":{"paths":["tests/test_case.py"], "pytest_args":["-q"], "support":{
                    "schema":support.SCHEMA,"namespace":namespace,"reason":"Reviewed synthetic installed controls",
                    "files":[{"source":p,"target":p,"sha256":hashlib.sha256((root/p).read_bytes()).hexdigest()} for p in files]}}}
            body = "from suite117_runner_support.helper import VALUE,DATA\nimport suite117_runtime\ndef test_case():\n    assert VALUE=='helper' and DATA.read_text()=='fixture'\n    assert suite117_runtime.VALUE=='installed'\n"
            if case == "source-addon":
                body += "    import sys\n    from pathlib import Path\n    sys.path.insert(0,str(Path(__file__).resolve().parents[1]))\n    import suite117_addon\n    sys.path.pop(0)\n"
            elif case == "data-mutation": body += "    DATA.write_text('changed')\n"
            elif case == "test-failure": body += "    assert False\n"
            elif case == "workers":
                (root / "tests/conftest.py").write_text("def pytest_addoption(parser):\n    parser.addoption('--numprocesses',type=int,default=0)\n")
                inventory["installed_tests"]["pytest_args"].extend(["--numprocesses", "2"])
            elif case == "missing-support": inventory["installed_tests"].pop("support")
            elif case == "collision": inventory["installed_tests"]["support"]["namespace"] = "devtools"
            (root / "tests/test_case.py").write_text(body)
            receipt = task / "receipt.json"
            command = "import json,sys;from pathlib import Path;sys.path.insert(0,sys.argv[1]);from devtools.scripts.installed_noarch import run_tests;sys.prefix=sys.argv[2];sys.path.insert(0,sys.prefix);raise SystemExit(run_tests(Path(sys.argv[3]),json.loads(sys.argv[4]),support_output=Path(sys.argv[5])))"
            environment = dict(os.environ,PYTEST_DISABLE_PLUGIN_AUTOLOAD="1")
            environment.pop("PYTEST_ADDOPTS",None)
            result = subprocess.run([sys.executable,"-P","-c",command,str(Path(__file__).resolve().parents[1]),str(prefix),str(root),json.dumps(inventory),str(receipt)],
                cwd=task,env=environment,capture_output=True,text=True,timeout=30)
            record = json.loads(receipt.read_text()) if receipt.exists() else None
            if record:
                self.assertFalse(Path(record["staging_path"]).exists())
            self.assertFalse(any(name.startswith("suite117_runner_support") for name in sys.modules))
            return result, record

    def test_actual_runner_support_preserves_installed_roots_and_retired_receipt(self):
        result, receipt = self.fixture()
        self.assertEqual(0,result.returncode,result.stdout+result.stderr)
        self.assertEqual(0,receipt["pytest_exit_code"])
        self.assertEqual(1,receipt["executed_tests"])
        self.assertTrue(receipt["resources_retired"] and receipt["imports_retired"])
        self.assertIn("suite117_runner_support.helper",receipt["loaded"])

    def test_actual_runner_negative_source_addon_and_support_bytes_remain_failures(self):
        for case in ("source-addon","data-mutation","test-failure","missing-support","collision","workers"):
            with self.subTest(case=case):
                result, receipt = self.fixture(case)
                self.assertNotEqual(0,result.returncode,result.stdout+result.stderr)
                if receipt:
                    self.assertTrue(receipt["resources_retired"] and receipt["imports_retired"])
                if case == "workers":
                    self.assertEqual(0, receipt["executed_tests"])
