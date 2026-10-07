"""Exercise context/source drift and truthful declaration versus installation."""

import importlib.metadata
import json
import subprocess
import sys
import unittest

from devtools.scripts import dependency_route_contexts as contexts
from devtools.scripts import dependency_routes as routes
from tests import test_dependency_routes as fixtures


class TestDependencyRouteContexts(unittest.TestCase):
    write = fixtures.DependencyRoutesTests.write
    digest = fixtures.DependencyRoutesTests.digest

    def setUp(self):
        fixtures.DependencyRoutesTests.setUp(self)
        self.manifest = "devtools/requirements/sources.txt"
        self.write(
            self.manifest,
            "git+https://github.com/example/smonitor.git@" + "a" * 40 + "\n",
        )
        self.content = (
            self.inventory.replace(routes.SCHEMA, contexts.SCHEMA)
            .replace("source_routes = []\n", "")
            .replace(
                'channel_priority = "strict"',
                'channel_priority = "strict"\npurpose = "test"\nnarrowing_reason = "Reviewed source test profile"',
            )
        )
        self.content += f'''
[[source_routes]]
id = "smonitor-old"
name = "smonitor"
role = "required-runtime"
url = "https://github.com/example/smonitor"
commit = "{"a" * 40}"
install = "pip-no-deps-git"
input = "{self.manifest}"
reason = "Reviewed existing Git pin"
[[source_inputs]]
path = "{self.manifest}"
sha256 = "{self.digest(self.manifest)}"
reason = "Actual no-deps pip input"
[[contexts]]
name = "ci-3.14"
environment = "devtools/conda-envs/test.yaml"
python_minor = "3.14"
sources = ["smonitor-old"]
overlays = ["smonitor"]
overlay_reason = "Conda bootstrap replaced by this fixed source"
reason = "Python-specific source CI input"
'''
        self.save()
        self.distribution = type("Distribution", (), {"version": "0.16.0"})()
        self.distribution.read_text = lambda name: json.dumps(
            {
                "url": "https://github.com/example/smonitor.git",
                "vcs_info": {
                    "vcs": "git",
                    "commit_id": "a" * 40,
                    "requested_revision": "a" * 40,
                },
            }
        )

    def save(self):
        self.write("devtools/dependency_routes.toml", self.content)

    def audit(self, **kwargs):
        return routes.audit(self.root, **kwargs)

    def installed(self, **kwargs):
        return self.audit(
            context="ci-3.14",
            check_installed=True,
            distribution_for=lambda name: self.distribution,
            python_version="3.14.7",
            **kwargs,
        )

    def test_declaration_does_not_read_distribution_and_actual_context_records_provenance(
        self,
    ):
        def absent(name):
            raise AssertionError("Declaration-only must not read installed metadata")

        evidence = self.audit(distribution_for=absent)
        self.assertEqual(evidence["qualification"], "declared-only")
        self.assertEqual(evidence["contexts"][0]["overlays"], ["smonitor"])
        self.assertNotIn("installed_sources", evidence)
        evidence = self.installed()
        self.assertEqual(evidence["qualification"], "declared-and-installed-context")
        self.assertEqual(evidence["installed_sources"][0]["commit"], "a" * 40)

    def test_context_and_interpreter_must_be_explicit_and_match(self):
        for kwargs in [
            {"check_installed": True},
            {"context": "unknown"},
            {"context": "ci-3.14", "check_installed": True, "python_version": "3.13.9"},
        ]:
            with self.subTest(kwargs=kwargs), self.assertRaises(routes.ContractError):
                self.audit(**kwargs)

    def test_manifest_changed_and_refreshed_hash_cannot_hide_wrong_pin(self):
        old = self.digest(self.manifest)
        self.write(
            self.manifest,
            (self.root / self.manifest).read_text().replace("a" * 40, "b" * 40),
        )
        with self.assertRaisesRegex(routes.ContractError, "source input changed"):
            self.audit()
        self.content = self.content.replace(old, self.digest(self.manifest))
        self.save()
        with self.assertRaisesRegex(
            routes.ContractError, "manifest and inventory differ"
        ):
            self.audit()

    def test_unclassified_manifest_entry_and_wrong_named_provider_fail(self):
        for content in [
            "smonitor @ git+https://github.com/example/other@" + "a" * 40,
            "wrong-name @ git+https://github.com/example/smonitor@" + "a" * 40,
            "git+https://github.com/example/smonitor@"
            + "a" * 40
            + "\ngit+https://github.com/example/other@"
            + "b" * 40,
        ]:
            old = self.digest(self.manifest)
            self.write(self.manifest, content)
            self.content = self.content.replace(old, self.digest(self.manifest))
            self.save()
            with self.subTest(content=content), self.assertRaises(routes.ContractError):
                self.audit()

    def test_missing_required_route_and_bootstrap_overlay_drift_fail(self):
        original = self.content
        for old, new in [
            ('sources = ["smonitor-old"]', "sources = []"),
            ('overlays = ["smonitor"]', "overlays = []"),
            ('role = "required-runtime"', 'role = "integration"'),
            (
                'overlay_reason = "Conda bootstrap replaced by this fixed source"',
                'overlay_reason = ""',
            ),
        ]:
            self.content = original.replace(old, new)
            self.save()
            with self.subTest(new=new), self.assertRaises(routes.ContractError):
                self.audit()

    def test_source_only_provider_removes_only_its_own_required_bootstrap(self):
        self.content = self.content.replace('overlays = ["smonitor"]', "overlays = []")
        self.save()
        self.write(
            "devtools/conda-envs/test.yaml",
            self.environment.replace(', "smonitor >=0.16,<1"', ""),
        )
        self.assertEqual(self.installed()["installed_sources"][0]["name"], "smonitor")
        self.distribution.version = "0.15"
        with self.assertRaisesRegex(routes.ContractError, "violates"):
            self.installed()

    def test_weak_bootstrap_bound_and_wrong_python_minor_fail(self):
        self.write(
            "devtools/conda-envs/test.yaml",
            self.environment.replace("smonitor >=0.16,<1", "smonitor"),
        )
        with self.assertRaisesRegex(routes.ContractError, "violates"):
            self.audit()
        self.write("devtools/conda-envs/test.yaml", self.environment)
        self.content = self.content.replace(
            'python_minor = "3.14"', 'python_minor = "3.15"'
        )
        self.save()
        with self.assertRaises(routes.ContractError):
            self.audit()

    def test_reviewed_channel_extension_preserves_order_and_needs_a_reason(self):
        self.content = self.content.replace(
            'channel_priority = "strict"',
            'channel_priority = "strict"\nadditional_channels = ["ambermd"]\nchannel_reason = "Scientific native bootstrap"',
        )
        self.save()
        self.write(
            "devtools/conda-envs/test.yaml",
            self.environment.replace(
                "uibcdf, conda-forge", "uibcdf, conda-forge, ambermd"
            ),
        )
        self.audit()
        self.content = self.content.replace(
            'channel_reason = "Scientific native bootstrap"', 'channel_reason = ""'
        )
        self.save()
        with self.assertRaisesRegex(routes.ContractError, "channels need"):
            self.audit()

    def test_unused_source_duplicate_provider_and_uncovered_runtime_fail(self):
        for addition in [
            self.content.split("[[source_routes]]")[1].split("[[source_inputs]]")[0],
            '\n[[contexts]]\nname="other"\nenvironment="missing.yaml"\npython_minor="3.14"\nsources=[]\nreason="Wrong environment"\n',
        ]:
            old = self.content
            self.content += (
                ("\n[[source_routes]]" + addition)
                if addition.startswith("\nid")
                else addition
            )
            self.save()
            with self.assertRaises(routes.ContractError):
                self.audit()
            self.content = old
        self.save()

    def test_actual_missing_or_false_git_provenance_cannot_pass(self):
        self.distribution.read_text = lambda name: None
        with self.assertRaisesRegex(routes.ContractError, "provenance"):
            self.installed()

        def absent(name):
            raise importlib.metadata.PackageNotFoundError(name)

        with self.assertRaises(importlib.metadata.PackageNotFoundError):
            self.audit(
                context="ci-3.14",
                check_installed=True,
                distribution_for=absent,
                python_version="3.14.7",
            )

    def test_cli_default_requires_context_and_declaration_only_is_truthful(self):
        command = [sys.executable, "-B", routes.__file__, "--root", str(self.root)]
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 1)
        self.assertIn("explicit reviewed context", result.stdout)
        result = subprocess.run(
            [*command, "--declared-only"], capture_output=True, text=True, check=False
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["qualification"], "declared-only")

    def test_python_specific_source_variants_verify_only_selected_revision(self):
        self.content += (
            '\n[[source_routes]]\nid="smonitor-new"\nname="smonitor"\nrole="required-runtime"\nurl="https://github.com/example/smonitor"\ncommit="'
            + "b" * 40
            + '"\ninstall="pip-no-deps-git"\nreason="Reviewed second inline fixed pin"\n'
        )
        self.content += '\n[[contexts]]\nname="ci-3.13"\nenvironment="devtools/conda-envs/test.yaml"\npython_minor="3.13"\nsources=["smonitor-new"]\noverlays=["smonitor"]\noverlay_reason="Retain older Python-specific source selection"\nreason="Older supported source cell"\n'
        self.save()
        self.assertEqual(len(self.audit()["contexts"]), 2)
        self.distribution.read_text = lambda name: json.dumps(
            {
                "url": "https://github.com/example/smonitor",
                "vcs_info": {"vcs": "git", "commit_id": "b" * 40},
            }
        )
        evidence = self.audit(
            context="ci-3.13",
            check_installed=True,
            distribution_for=lambda n: self.distribution,
            python_version="3.13.9",
        )
        self.assertEqual(evidence["installed_sources"][0]["id"], "smonitor-new")
        with self.assertRaisesRegex(routes.ContractError, "commit differs"):
            self.installed()

    def test_integration_provider_is_explicit_and_also_checked_when_installed(self):
        self.content = self.content.replace(
            'sources = ["smonitor-old"]', 'sources = ["smonitor-old", "viewer"]'
        )
        self.content += (
            '\n[[source_routes]]\nid="viewer"\nname="viewer"\nrole="integration"\nurl="https://github.com/example/viewer"\ncommit="'
            + "c" * 40
            + '"\ninstall="pip-no-deps-git"\nreason="Pinned integration provider, not a required dependency"\n'
        )
        self.save()
        other = type("Distribution", (), {"version": "0.22.0"})()
        other.read_text = lambda n: json.dumps(
            {
                "url": "https://github.com/example/viewer",
                "vcs_info": {"vcs": "git", "commit_id": "c" * 40},
            }
        )
        getter = lambda n: other if n == "viewer" else self.distribution
        evidence = self.audit(
            context="ci-3.14",
            check_installed=True,
            distribution_for=getter,
            python_version="3.14.7",
        )
        self.assertEqual(
            [s["name"] for s in evidence["installed_sources"]], ["smonitor", "viewer"]
        )
        other.read_text = lambda n: None
        with self.assertRaisesRegex(routes.ContractError, "source viewer"):
            self.audit(
                context="ci-3.14",
                check_installed=True,
                distribution_for=getter,
                python_version="3.14.7",
            )

    def test_unbounded_requirement_is_accepted_without_weakening_legacy_helper(self):
        for path in [
            "pyproject.toml",
            "devtools/conda-build/meta.yaml",
            "devtools/conda-envs/test.yaml",
        ]:
            self.write(
                path,
                (self.root / path)
                .read_text()
                .replace("smonitor>=0.16,<1", "smonitor")
                .replace("smonitor >=0.16,<1", "smonitor"),
            )
        self.distribution.version = "0.1.0"
        self.assertEqual(self.installed()["installed_versions"]["smonitor"], "0.1.0")
        with self.assertRaises(routes.ContractError):
            routes.validate_source_version("smonitor", "0.1.0")

    def test_installed_non_source_versions_must_match_selected_environment(self):
        self.content = self.content.replace(
            'sources = ["smonitor-old"]', "sources = []"
        ).replace('overlays = ["smonitor"]', "overlays = []")
        self.content = (
            self.content.split("[[source_routes]]")[0]
            + "source_routes = []\n"
            + "[[contexts]]"
            + self.content.split("[[contexts]]")[1]
        )
        self.save()
        self.write(
            "devtools/conda-envs/test.yaml",
            self.environment.replace("smonitor >=0.16,<1", "smonitor=0.16.0"),
        )
        self.distribution.version = "0.17.0"
        with self.assertRaisesRegex(
            routes.ContractError, "selected environment constraint"
        ):
            self.installed()

    def test_partial_minor_and_channel_reordering_cannot_claim_context_match(self):
        self.write(
            "devtools/conda-envs/test.yaml",
            self.environment.replace("python >=3.11,<3.15", "python >=3.14,<3.14.1"),
        )
        with self.assertRaisesRegex(routes.ContractError, "violates"):
            self.audit()
        self.write(
            "devtools/conda-envs/test.yaml",
            self.environment.replace("uibcdf, conda-forge", "conda-forge, uibcdf"),
        )
        with self.assertRaisesRegex(routes.ContractError, "channels/strict"):
            self.audit()


if __name__ == "__main__":
    unittest.main()
