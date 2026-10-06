"""A solver or release receipt cannot guard a later weakened runtime route."""

import hashlib
import importlib.metadata
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from devtools.scripts import dependency_routes as routes


class DependencyRoutesTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.write(
            "pyproject.toml",
            """[project]
name = "example"
requires-python = ">=3.11,<3.15"
dependencies = ["smonitor>=0.16,<1"]
""",
        )
        self.write("example/_version.py", '__version__ = "1.2.3"\n')
        self.write(
            "devtools/conda-build/meta.yaml",
            """package:
  name: example
  version: "{{ environ['MOLSYSSUITE_CONDA_VERSION'] }}"
build:
  noarch: python
  number: 0
  string: py_0
requirements:
  host: ["python >=3.11,<3.15"]
  run: ["python >=3.11,<3.15", "smonitor >=0.16,<1"]
""",
        )
        self.write(
            "devtools/conda-build/release_plan.toml",
            """schema = "molsyssuite.conda-plan@1"
package = "example"
version = "1.2.3"
build_number = 0
route = "staged"
profile = "noarch-python"
reason = "First noarch qualification"
decision_by = "LMMV"
artifact_subdirs = ["noarch"]
test_platforms = ["linux-64"]
python_versions = ["3.11", "3.12", "3.13", "3.14"]
required_workflows = [".github/workflows/test.yaml"]
requires_installed_gate = true
new_compatibility_surface = true
coupled_release = false
dependencies_public = true
[gate_jobs.".github/workflows/test.yaml"]
"Tests" = ["Run tests"]
""",
        )
        self.write(
            "devtools/conda-build/resources.toml",
            """reason = "Installed Python version identity"
version_file = "site-packages/example/_version.py"
required_paths = ["site-packages/example/_version.py"]
""",
        )
        self.environment = """channels: [uibcdf, conda-forge]
dependencies: ["python >=3.11,<3.15", "smonitor >=0.16,<1", pip]
"""
        self.write("devtools/conda-envs/test.yaml", self.environment)
        self.write("devtools/conda-envs/build.yaml", "dependencies: [pip]\n")
        self.write(".github/workflows/test.yaml", "name: Tests\njobs: {}\n")
        digest = self.digest(".github/workflows/test.yaml")
        self.inventory = f'''schema = "{routes.SCHEMA}"
reason = "Reviewed example runtime and build routes"
source_routes = []
source_reason = "Runtime dependencies resolve through Conda"
[[recipes]]
path = "devtools/conda-build/meta.yaml"
kind = "shared-noarch"
plan = "devtools/conda-build/release_plan.toml"
resources = "devtools/conda-build/resources.toml"
reason = "Single noarch runtime artifact"
[[environments]]
path = "devtools/conda-envs/test.yaml"
kind = "runtime"
channel_priority = "strict"
reason = "Installs runtime before tests"
[[environments]]
path = "devtools/conda-envs/build.yaml"
kind = "build-only"
reason = "Build tools; runtime comes from the recipe host environment"
[[workflows]]
path = ".github/workflows/test.yaml"
sha256 = "{digest}"
reason = "Conda environment followed by no-deps source installation"
'''
        self.write("devtools/dependency_routes.toml", self.inventory)

    def write(self, path, content):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    def digest(self, path):
        return hashlib.sha256((self.root / path).read_bytes()).hexdigest()

    def audit(self, **kwargs):
        return routes.audit(self.root, **kwargs)

    def test_reviewed_inventory_passes_without_mutations(self):
        before = {
            path: path.read_bytes() for path in self.root.rglob("*") if path.is_file()
        }
        evidence = self.audit()
        self.assertEqual(evidence["schema"], routes.SCHEMA)
        self.assertEqual(len(evidence["routes"]), 4)
        self.assertEqual(evidence["source_dependencies"], [])
        self.assertEqual(
            before,
            {
                path: path.read_bytes()
                for path in self.root.rglob("*")
                if path.is_file()
            },
        )

    def test_omitted_recipe_requirement_fails_even_when_environments_pass(self):
        path = "devtools/conda-build/meta.yaml"
        self.write(
            path, (self.root / path).read_text().replace(', "smonitor >=0.16,<1"', "")
        )
        with self.assertRaisesRegex(routes.ContractError, "meta.yaml.*smonitor"):
            self.audit()

    def test_runtime_floors_ceilings_and_missing_names_fail(self):
        for spec in (
            "smonitor",
            "smonitor >=0.15,<1",
            "smonitor >=0.16",
            "other >=0.16,<1",
        ):
            with self.subTest(spec=spec):
                self.write(
                    "devtools/conda-envs/test.yaml",
                    self.environment.replace("smonitor >=0.16,<1", spec),
                )
                with self.assertRaisesRegex(
                    routes.ContractError, "test.yaml.*smonitor"
                ):
                    self.audit()

    def test_wider_python_or_duplicate_python_fails(self):
        for changed in (
            "python >=3.10,<3.15",
            "python >=3.11",
            'python >=3.11,<3.15", "python >=3.11,<3.15',
        ):
            with self.subTest(changed=changed):
                self.write(
                    "devtools/conda-envs/test.yaml",
                    self.environment.replace("python >=3.11,<3.15", changed),
                )
                with self.assertRaisesRegex(routes.ContractError, "test.yaml"):
                    self.audit()

    def test_reviewed_narrowed_minor_and_conda_pin_are_equivalent(self):
        self.write(
            "devtools/dependency_routes.toml",
            self.inventory.replace(
                'channel_priority = "strict"',
                'channel_priority = "strict"\npython_minor = "3.14"',
            ),
        )
        for spec in ("python=3.14", "python >=3.14,<3.15"):
            self.write(
                "devtools/conda-envs/test.yaml",
                self.environment.replace("python >=3.11,<3.15", spec),
            )
            self.audit()
        self.write(
            "devtools/conda-envs/test.yaml",
            self.environment.replace("python >=3.11,<3.15", "python=3.15"),
        )
        with self.assertRaisesRegex(routes.ContractError, "Python constraint"):
            self.audit()

    def test_narrowed_minor_cannot_bypass_python_metadata(self):
        for required in (
            ">=3.14.1,<3.15",
            ">=3.11,<3.14.1",
            ">=3.11,<3.14",
            ">=3.11,!=3.14.2,<3.15",
        ):
            with (
                self.subTest(required=required),
                self.assertRaises(routes.ContractError),
            ):
                routes._narrow_python(required, "3.14")

    def test_new_environment_recipe_or_workflow_requires_classification(self):
        for path in (
            "devtools/conda-envs/extra.yaml",
            "devtools/other/meta.yaml",
            ".github/workflows/extra.yml",
        ):
            with self.subTest(path=path):
                self.write(path, "unreviewed\n")
                with self.assertRaisesRegex(routes.ContractError, "unclassified"):
                    self.audit()
                (self.root / path).unlink()

    def test_changed_workflow_cannot_hide_a_new_source_route(self):
        self.write(
            ".github/workflows/test.yaml",
            "jobs:\n  test:\n    steps:\n      - run: pip install git+https://example.invalid/provider@main\n",
        )
        with self.assertRaisesRegex(routes.ContractError, "reviewed workflow changed"):
            self.audit()

    def test_unknown_inventory_and_missing_exclusion_reason_fail(self):
        for content in (
            self.inventory.replace(routes.SCHEMA, "unknown@2"),
            self.inventory.replace(
                'reason = "Build tools; runtime comes from the recipe host environment"',
                'reason = ""',
            ),
        ):
            self.write("devtools/dependency_routes.toml", content)
            with self.assertRaises(routes.ContractError):
                self.audit()

    def test_channel_order_and_conditional_requirements_fail(self):
        for content in (
            self.environment.replace("uibcdf, conda-forge", "conda-forge, uibcdf"),
            self.environment.replace(
                "smonitor >=0.16,<1", "smonitor >=0.16,<1; python_version < '3.14'"
            ),
        ):
            self.write("devtools/conda-envs/test.yaml", content)
            with self.assertRaisesRegex(routes.ContractError, "test.yaml"):
                self.audit()

    def test_below_floor_source_and_above_ceiling_candidates_are_rejected(self):
        for version in ("0.15.9", "0.15.9+local", "1.0", "1.1"):
            with (
                self.subTest(version=version),
                self.assertRaisesRegex(routes.ContractError, "installed source"),
            ):
                routes.validate_source_version("smonitor>=0.16,<1", version)
        for version in ("0.16.0", "0.16.0+local", "0.99"):
            routes.validate_source_version("smonitor>=0.16,<1", version)

    def test_source_preflight_checks_commit_cleanliness_version_and_install_origin(
        self,
    ):
        source = self.root / "source"
        source.mkdir()
        (source / "owned.txt").write_text("producer\n")

        def git(*arguments):
            return subprocess.check_output(
                ["git", *arguments], cwd=source, text=True
            ).strip()

        git("init", "-q")
        git("add", "owned.txt")
        git(
            "-c",
            "user.name=Test",
            "-c",
            "user.email=test@example.invalid",
            "commit",
            "-qm",
            "Producer",
        )
        pin = {
            "commit": git("rev-parse", "HEAD"),
            "install": "pip-no-deps-directory",
            "reason": "Reviewed source provider",
        }

        class Distribution:
            version = "0.16.0"

            def read_text(self, name):
                return json.dumps({"url": source.as_uri(), "dir_info": {}})

        distribution = Distribution()
        routes._source(pin, "smonitor>=0.16,<1", source, lambda name: distribution)
        distribution.version = "0.15"
        with self.assertRaisesRegex(routes.ContractError, "installed source"):
            routes._source(pin, "smonitor>=0.16,<1", source, lambda name: distribution)
        distribution.version = "0.16"
        distribution.read_text = lambda name: json.dumps(
            {"url": self.root.as_uri(), "dir_info": {}}
        )
        with self.assertRaisesRegex(routes.ContractError, "reviewed directory"):
            routes._source(pin, "smonitor>=0.16,<1", source, lambda name: distribution)
        (source / "owned.txt").write_text("modified\n")
        with self.assertRaisesRegex(routes.ContractError, "dirty"):
            routes._source(pin, "smonitor>=0.16,<1", source, lambda name: distribution)

        git("restore", "owned.txt")
        distribution.read_text = lambda name: json.dumps(
            {"url": source.as_uri(), "dir_info": {}}
        )
        inventory = self.inventory.replace("source_routes = []\n", "").replace(
            'channel_priority = "strict"',
            'channel_priority = "strict"\nsource_supplied = ["smonitor"]',
        )
        inventory += (
            '\n[[source_routes]]\nname = "smonitor"\n'
            f'commit = "{pin["commit"]}"\ninstall = "pip-no-deps-directory"\n'
            'reason = "Reviewed source provider"\n'
        )
        self.write("devtools/dependency_routes.toml", inventory)
        self.write(
            "devtools/conda-envs/test.yaml",
            self.environment.replace(', "smonitor >=0.16,<1"', ""),
        )
        evidence = self.audit(
            source_roots={"smonitor": source},
            distribution_for=lambda name: distribution,
        )
        self.assertEqual(evidence["source_dependencies"], ["smonitor"])

        def absent(name):
            raise importlib.metadata.PackageNotFoundError(name)

        with self.assertRaisesRegex(routes.ContractError, "source smonitor"):
            self.audit(source_roots={"smonitor": source}, distribution_for=absent)

    def test_cli_preserves_failure_exit_and_reports_offending_route(self):
        tool = Path(routes.__file__)
        command = [sys.executable, "-B", str(tool), "--root", str(self.root)]
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.write(
            "devtools/conda-envs/test.yaml",
            self.environment.replace("smonitor >=0.16,<1", "smonitor"),
        )
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("test.yaml", result.stdout)


if __name__ == "__main__":
    unittest.main()
