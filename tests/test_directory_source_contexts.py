"""Qualify real immutable directory installs and preserve contextual Git behavior."""

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from devtools.scripts import dependency_routes as routes
from devtools.scripts import source_provenance as provenance
from tests import test_dependency_route_contexts as fixtures


class DirectoryInstallTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.git("init", "-q")
        self.git("config", "user.name", "Fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("remote", "add", "origin", "https://github.com/example/provider.git")
        (self.root / "module.py").write_text("value = 1\n")
        self.git("add", "module.py")
        self.git("commit", "-qm", "fixture")
        self.record = {
            "url": "https://github.com/example/provider",
            "commit": self.git("rev-parse", "HEAD"),
            "install": "pip-no-deps-directory",
        }
        self.direct = {"url": self.root.as_uri(), "dir_info": {}}
        self.distribution = type("Distribution", (), {"version": "0.16.0"})()
        self.distribution.read_text = lambda name: json.dumps(self.direct)

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.root, text=True).strip()

    def check(self, requirement="provider>=0.16,<1"):
        return provenance.check_directory_install(
            self.record, requirement, self.distribution, self.root
        )

    def test_normal_directory_install_records_actual_clone_and_version(self):
        result = self.check()
        self.assertEqual(result["commit"], self.record["commit"])
        self.assertEqual(result["repository"], self.record["url"])
        self.assertEqual(result["directory"], str(self.root))
        self.assertEqual(result["version"], "0.16.0")

    def test_wrong_commit_repository_and_dirty_tracked_or_untracked_clone_fail(self):
        original = self.record["commit"]
        self.record["commit"] = "b" * 40
        with self.assertRaises(provenance.ContractError):
            self.check()
        self.record["commit"] = original
        self.git("remote", "set-url", "origin", "https://github.com/other/provider")
        with self.assertRaises(provenance.ContractError):
            self.check()
        self.git("remote", "set-url", "origin", self.record["url"])
        for path in ["module.py", "extra.py"]:
            (self.root / path).write_text("changed = True\n")
            with self.subTest(path=path), self.assertRaises(provenance.ContractError):
                self.check()
            if path == "module.py":
                self.git("restore", "module.py")
            else:
                (self.root / path).unlink()

    def test_other_directory_git_archive_editable_or_malformed_origins_fail(self):
        original = dict(self.direct)
        for direct in [
            {"url": self.root.parent.as_uri(), "dir_info": {}},
            {**original, "dir_info": {"editable": True}},
            {**original, "archive_info": {}},
            {**original, "vcs_info": {"vcs": "git"}},
            {**original, "subdirectory": "src"},
            {**original, "dir_info": []},
            {"url": self.root.as_uri()},
            {"url": "file://otherhost" + str(self.root), "dir_info": {}},
            {"url": self.root.as_uri() + "?query", "dir_info": {}},
        ]:
            self.direct = direct
            with (
                self.subTest(direct=direct),
                self.assertRaises(provenance.ContractError),
            ):
                self.check()
        self.direct = original
        for raw in [None, "{", "[]"]:
            self.distribution.read_text = lambda name, value=raw: value
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                self.check()

    def test_missing_or_nested_clone_and_non_directory_profile_fail(self):
        nested = self.root / "nested"
        nested.mkdir()
        with self.assertRaises(provenance.ContractError):
            provenance.check_directory_install(
                self.record, "provider", self.distribution, nested
            )
        self.record["install"] = "pip-no-deps-git"
        with self.assertRaises(provenance.ContractError):
            self.check()

    def test_public_floors_and_unbounded_metadata_remain_distinct(self):
        self.distribution.version = "0.15.9"
        with self.assertRaises(provenance.ContractError):
            self.check()
        self.assertEqual(self.check("provider")["version"], "0.15.9")


class DirectoryContextTests(unittest.TestCase):
    # Reuse the existing contextual fixture, without inheriting its tests twice.
    setUp = fixtures.TestDependencyRouteContexts.setUp
    write = fixtures.TestDependencyRouteContexts.write
    digest = fixtures.TestDependencyRouteContexts.digest
    save = fixtures.TestDependencyRouteContexts.save
    audit = fixtures.TestDependencyRouteContexts.audit
    installed = fixtures.TestDependencyRouteContexts.installed

    def prepare_directory(self):
        fixture = DirectoryInstallTests(
            "test_normal_directory_install_records_actual_clone_and_version"
        )
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        self.content = self.content.replace(
            'install = "pip-no-deps-git"', 'install = "pip-no-deps-directory"'
        )
        self.content = self.content.replace('input = "' + self.manifest + '"\n', "")
        start = self.content.index("[[source_inputs]]")
        end = self.content.index("[[contexts]]", start)
        self.content = self.content[:start] + self.content[end:]
        self.content = self.content.replace("a" * 40, fixture.record["commit"])
        self.content = self.content.replace(
            "https://github.com/example/smonitor", fixture.record["url"]
        )
        self.save()
        self.distribution = fixture.distribution
        return fixture

    def test_directory_context_is_explicit_and_declaration_reads_no_clone(self):
        fixture = self.prepare_directory()
        self.assertEqual(self.audit()["qualification"], "declared-only")
        result = self.installed(source_roots={"smonitor-old": fixture.root})
        self.assertEqual(result["installed_sources"][0]["directory"], str(fixture.root))
        for roots in [
            {},
            {"smonitor": fixture.root},
            {"smonitor-old": fixture.root, "extra": fixture.root},
        ]:
            with self.subTest(roots=roots), self.assertRaises(routes.ContractError):
                self.installed(source_roots=roots)
        with self.assertRaises(routes.ContractError):
            self.audit(source_roots={"smonitor-old": fixture.root})

    def test_directory_sources_cannot_claim_git_manifest_inputs(self):
        self.prepare_directory()
        self.content = self.content.replace(
            'install = "pip-no-deps-directory"',
            'install = "pip-no-deps-directory"\ninput = "unreviewed.txt"',
        )
        self.save()
        with self.assertRaisesRegex(routes.ContractError, "directory.*input"):
            self.audit()

    def test_git_only_context_rejects_directory_roots_and_directory_metadata(self):
        with self.assertRaises(routes.ContractError):
            self.installed(source_roots={"smonitor-old": self.root})
        self.distribution.read_text = lambda name: json.dumps(
            {"url": self.root.as_uri(), "dir_info": {}}
        )
        with self.assertRaises(routes.ContractError):
            self.installed()

    def test_optional_directory_provider_is_qualified_in_its_selected_context(self):
        fixture = self.prepare_directory()
        self.content += f'''\n[[source_routes]]
id = "viewer"
name = "viewer"
role = "integration"
url = "{fixture.record["url"]}"
commit = "{fixture.record["commit"]}"
install = "pip-no-deps-directory"
reason = "Explicit optional integration clone"
'''
        self.content = self.content.replace(
            'sources = ["smonitor-old"]', 'sources = ["smonitor-old", "viewer"]'
        )
        self.save()
        result = self.installed(
            source_roots={"smonitor-old": fixture.root, "viewer": fixture.root}
        )
        self.assertEqual(
            [s["name"] for s in result["installed_sources"]], ["smonitor", "viewer"]
        )

    def test_git_and_directory_contexts_bind_only_their_selected_sources(self):
        fixture = self.prepare_directory()
        self.content += (
            '\n[[source_routes]]\nid="smonitor-new"\nname="smonitor"\nrole="required-runtime"\nurl="https://github.com/example/provider"\ncommit="'
            + "b" * 40
            + '"\ninstall="pip-no-deps-git"\nreason="Separate Git context"\n'
        )
        self.content += '\n[[contexts]]\nname="ci-3.13"\nenvironment="devtools/conda-envs/test.yaml"\npython_minor="3.13"\nsources=["smonitor-new"]\noverlays=["smonitor"]\noverlay_reason="Original bootstrap replacement"\nreason="Separate older-minor Git input"\n'
        self.save()
        self.assertEqual(len(self.audit()["contexts"]), 2)
        self.assertEqual(
            self.installed(source_roots={"smonitor-old": fixture.root})[
                "installed_sources"
            ][0]["install"],
            "pip-no-deps-directory",
        )
        self.distribution.read_text = lambda n: json.dumps(
            {
                "url": fixture.record["url"],
                "vcs_info": {"vcs": "git", "commit_id": "b" * 40},
            }
        )
        result = self.audit(
            context="ci-3.13",
            check_installed=True,
            distribution_for=lambda n: self.distribution,
            python_version="3.13.9",
        )
        self.assertEqual(result["installed_sources"][0]["install"], "pip-no-deps-git")
        with self.assertRaises(routes.ContractError):
            self.audit(
                context="ci-3.13",
                check_installed=True,
                distribution_for=lambda n: self.distribution,
                python_version="3.13.9",
                source_roots={"smonitor-old": fixture.root},
            )


if __name__ == "__main__":
    unittest.main()
