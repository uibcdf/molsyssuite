"""Prevent executable payloads, coupling and unreviewed central recipe creation."""

import contextlib
import io
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

from devtools.scripts import central_metapackages as bundles
from devtools.scripts.conda_release_contract import ContractError

ROOT = Path(__file__).resolve().parents[1]
PLAN = """schema = "molsyssuite.conda-plan@1"
package = "PACKAGE"
version = "1.2.3"
build_number = 2
route = "staged"
profile = "metapackage"
reason = "Test fixture only, not a real release decision"
decision_by = "Test fixture"
artifact_subdirs = ["noarch"]
test_platforms = ["linux-64"]
python_versions = ["3.14"]
required_workflows = [".github/workflows/validate_governance.yaml"]
requires_installed_gate = true
new_compatibility_surface = true
coupled_release = false
dependencies_public = true
[gate_jobs.".github/workflows/validate_governance.yaml"]
governance = ["Test the governance guard"]
"""


class CentralMetapackageTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        for relative in [
            "suite.toml",
            bundles.DEVELOPMENT_RECIPE,
            *[f"devtools/conda-build/{name}/meta.yaml" for name in bundles.PACKAGES],
        ]:
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, target)
        for name in bundles.PACKAGES:
            self.plan(name).write_text(PLAN.replace("PACKAGE", name))

    def plan(self, package="molsyssuite"):
        return self.root / f"devtools/conda-build/{package}/release_plan.toml"

    def recipe(self, package="molsyssuite"):
        return self.plan(package).with_name("meta.yaml")

    def prepare(self, package="molsyssuite", version="1.2.3"):
        return bundles.prepare_recipe(self.root, package, version)

    def cli(self, package, output):
        with (
            patch(
                "sys.argv",
                [
                    "central_metapackages.py",
                    "--root",
                    str(self.root),
                    "--package",
                    package,
                    "--version",
                    "1.2.3",
                    "--output-directory",
                    str(output),
                ],
            ),
            contextlib.redirect_stdout(io.StringIO()),
        ):
            return bundles.main()

    def test_missing_or_mismatched_plan_cannot_create_recipe(self):
        output = self.root / "generated"
        self.plan().unlink()
        self.assertEqual(self.cli("molsyssuite", output), 1)
        self.assertFalse(output.exists())
        self.plan().write_text(PLAN.replace("PACKAGE", "molsyssuite-dev"))
        self.assertEqual(self.cli("molsyssuite", output), 1)
        self.assertFalse(output.exists())

    def test_candidate_version_profile_and_executed_gate_inventory_are_required(self):
        original = self.plan().read_text()
        for text in [
            original.replace('version = "1.2.3"', 'version = "2026.02.0"'),
            original.replace('profile = "metapackage"', 'profile = "noarch-python"'),
            original.split("[gate_jobs.")[0],
        ]:
            with self.subTest(text=text):
                self.plan().write_text(text)
                with self.assertRaises(ContractError):
                    self.prepare()
        self.plan().write_text(original)
        with self.assertRaises(ContractError):
            self.prepare(version="1.2.4")

    def test_source_payload_build_hooks_and_selectors_are_rejected(self):
        original = self.recipe().read_text()
        for change in [
            original + "\nsource:\n  path: ../../scripts\n",
            original.replace("noarch: generic", "noarch: python"),
            original.replace(
                "noarch: generic", "noarch: generic\n  script: pip install ."
            ),
            original.replace(
                "noarch: generic",
                "noarch: generic\n  entry_points: [molsys-dev-setup = helper:main]",
            ),
            original + "\noutputs: []\n",
            original.replace("- molsysmt", "- molsysmt  # [linux]"),
        ]:
            with self.subTest(change=change):
                self.recipe().write_text(change)
                with self.assertRaises(ContractError):
                    self.prepare()

    def test_runtime_bundle_cannot_silently_add_members_sources_or_duplicate_deps(self):
        original = self.recipe().read_text()
        for dependency in [
            "topomt",
            "molsyssuite-dev",
            "molsysmt",
            "uibcdf::molsysmt",
            "../molsysmt",
            "jupyterlab",
            "smonitor",
            "argdigest",
            "depdigest",
            "pyunitwizard",
        ]:
            with self.subTest(dependency=dependency):
                self.recipe().write_text(
                    original.replace(
                        "    - molsysviewer", f"    - molsysviewer\n    - {dependency}"
                    )
                )
                with self.assertRaises(ContractError):
                    self.prepare()

    def test_developer_dependencies_follow_maintained_environment_without_runtime_bundle(
        self,
    ):
        environment = self.root / bundles.DEVELOPMENT_RECIPE
        content = yaml.safe_load(environment.read_text())
        content["dependencies"].append("sphinx")
        environment.write_text(yaml.safe_dump(content))
        recipe, filename = self.prepare("molsyssuite-dev")
        self.assertEqual(recipe["requirements"]["run"], content["dependencies"])
        self.assertEqual(filename, "molsyssuite-dev-1.2.3-meta_2.tar.bz2")
        self.assertNotIn("molsyssuite", recipe["requirements"]["run"])
        self.assertNotIn("source", recipe)
        self.assertNotIn("entry_points", recipe["build"])
        content["dependencies"].append("molsyssuite")
        environment.write_text(yaml.safe_dump(content))
        with self.assertRaises(ContractError):
            self.prepare("molsyssuite-dev")

    def test_developer_bundle_rejects_source_installs_drift_and_unqualified_targets(
        self,
    ):
        original = self.recipe("molsyssuite-dev").read_text()
        self.recipe("molsyssuite-dev").write_text(
            original.replace("{% endfor %}", "{% endfor %}\n    - topomt")
        )
        with self.assertRaises(ContractError):
            self.prepare("molsyssuite-dev")
        self.recipe("molsyssuite-dev").write_text(original)
        self.plan("molsyssuite-dev").write_text(
            PLAN.replace("PACKAGE", "molsyssuite-dev").replace('"linux-64"', '"win-64"')
        )
        with self.assertRaises(ContractError):
            self.prepare("molsyssuite-dev")

    def test_removing_capability_tests_or_linking_clones_is_rejected(self):
        original = self.recipe("molsyssuite-dev").read_text()
        for text in [
            original.replace("    - ruff --version\n", ""),
            original.replace(
                "ruff --version", "python -m pip install --editable ../molsysmt"
            ),
        ]:
            self.recipe("molsyssuite-dev").write_text(text)
            with self.assertRaises(ContractError):
                self.prepare("molsyssuite-dev")

    def test_rendered_directory_has_only_metadata_and_never_clobbers_caller_files(self):
        output = self.root / "generated"
        self.assertEqual(self.cli("molsyssuite", output), 0)
        self.assertEqual(list(output.iterdir()), [output / "meta.yaml"])
        rendered = yaml.safe_load((output / "meta.yaml").read_text())
        self.assertEqual(
            rendered["requirements"]["run"],
            ["python >=3.11,<3.15", "molsysmt", "molsysviewer"],
        )
        self.assertEqual(
            rendered["build"], {"number": 2, "string": "meta_2", "noarch": "generic"}
        )
        (output / "caller-work").write_text("retained")
        self.assertEqual(self.cli("molsyssuite-dev", output), 1)
        self.assertEqual((output / "caller-work").read_text(), "retained")

    def test_failed_recipe_write_cleans_only_its_new_directory(self):
        output = self.root / "generated"
        original = Path.write_text

        def fail_metadata(path, *args, **kwargs):
            if path == output / "meta.yaml":
                raise OSError("synthetic write failure")
            return original(path, *args, **kwargs)

        with patch.object(Path, "write_text", fail_metadata):
            self.assertEqual(self.cli("molsyssuite", output), 1)
        self.assertFalse(output.exists())
        self.assertTrue(self.recipe().exists())

    def test_both_publisher_paths_use_prepared_generic_recipe_after_preflight(self):
        workflow = yaml.load(
            (
                ROOT / ".github/workflows/build_and_upload_conda_packages.yaml"
            ).read_text(),
            Loader=yaml.BaseLoader,
        )
        steps = workflow["jobs"]["conda_deployment"]["steps"]
        preparation = next(
            i for i, step in enumerate(steps) if step.get("id") == "recipe"
        )
        preflight = next(
            i for i, step in enumerate(steps) if step.get("id") == "preflight"
        )
        self.assertLess(preparation, preflight)
        for identity in ["staging", "direct"]:
            index = next(
                i for i, step in enumerate(steps) if step.get("id") == identity
            )
            self.assertLess(preflight, index)
            self.assertEqual(
                steps[index]["with"]["meta_yaml_dir"],
                "${{ steps.recipe.outputs.directory }}",
            )
            self.assertEqual(
                steps[index]["with"]["evidence_matrix_index"],
                "${{ strategy.job-index }}",
            )
        self.assertIn("steps.recipe.outputs.filename", str(steps))
        self.assertEqual(steps[-1]["name"], "Remove the finished task-owned recipe")
        self.assertIn("always()", steps[-1]["if"])


if __name__ == "__main__":
    unittest.main()
