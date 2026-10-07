"""Negative guards for fixed Git input and actual installed-origin comparison."""

import json
import unittest

from devtools.scripts import source_provenance as provenance


class TestSourceProvenance(unittest.TestCase):
    def setUp(self):
        self.pin = {
            "url": "https://github.com/example/provider.git",
            "commit": "a" * 40,
            "install": "pip-no-deps-git",
        }
        self.direct = {
            "url": "https://github.com/example/provider",
            "vcs_info": {
                "vcs": "git",
                "commit_id": "a" * 40,
                "requested_revision": "a" * 40,
            },
        }
        self.distribution = type("Distribution", (), {"version": "0.16.0"})()
        self.distribution.read_text = lambda name: json.dumps(self.direct)

    def check(self, requirement="smonitor>=0.16,<1"):
        return provenance.check_git_install(self.pin, requirement, self.distribution)

    def test_named_and_unnamed_fixed_inputs_normalize_repository_suffix(self):
        for prefix in ["", "smonitor @ "]:
            result = provenance.parse_git_requirement(
                prefix + "git+" + self.pin["url"] + "@" + self.pin["commit"]
            )
            self.assertEqual(
                result["repository"], "https://github.com/example/provider"
            )
            self.assertEqual(result["commit"], self.pin["commit"])
        self.assertEqual(self.check()["version"], "0.16.0")

    def test_mutable_short_uppercase_subdirectory_and_conditional_inputs_fail(self):
        for suffix in [
            "main",
            "v1.2.3",
            "a" * 12,
            "A" * 40,
            "a" * 40 + "#subdirectory=src",
        ]:
            with (
                self.subTest(suffix=suffix),
                self.assertRaises(provenance.ContractError),
            ):
                provenance.parse_git_requirement(
                    "git+" + self.pin["url"] + "@" + suffix
                )
        for text in ["smonitor[gpu] @ ", "smonitor @ "]:
            value = text + "git+" + self.pin["url"] + "@" + self.pin["commit"]
            if text == "smonitor @ ":
                value += ' ; python_version < "3.14"'
            with self.assertRaises(provenance.ContractError):
                provenance.parse_git_requirement(value)

    def test_credentials_query_escape_and_other_transport_fail(self):
        for url in [
            "https://user:secret@github.com/a/b",
            "https://github.com/a/b?token=secret",
            "https://github.com/a/../b",
            "https://github.com/a/%62",
            "file:///tmp/a",
            "ssh://git@github.com/a/b",
            "https://github.com/a/b/",
        ]:
            with self.subTest(url=url), self.assertRaises(provenance.ContractError):
                provenance.repository_url(url)

    def test_wrong_repository_requested_commit_resolved_commit_and_vcs_fail(self):
        for key, value in [
            ("commit_id", "b" * 40),
            ("requested_revision", "main"),
            ("requested_revision", "b" * 40),
            ("vcs", "hg"),
        ]:
            original = self.direct["vcs_info"][key]
            self.direct["vcs_info"][key] = value
            with self.subTest(key=key), self.assertRaises(provenance.ContractError):
                self.check()
            self.direct["vcs_info"][key] = original
        self.direct["url"] = "https://github.com/other/provider"
        with self.assertRaises(provenance.ContractError):
            self.check()

    def test_missing_malformed_directory_archive_and_subdirectory_provenance_fail(self):
        for data in [
            None,
            "{",
            "[]",
            json.dumps({"url": self.pin["url"], "dir_info": {}}),
            json.dumps({**self.direct, "archive_info": {}}),
            json.dumps({**self.direct, "subdirectory": "src"}),
            json.dumps({**self.direct, "vcs_info": []}),
        ]:
            self.distribution.read_text = lambda name, raw=data: raw
            with self.subTest(data=data), self.assertRaises((ValueError, TypeError)):
                self.check()

    def test_metadata_bounds_are_enforced_and_unbounded_metadata_is_not_invented(self):
        for version in ["0.15.9", "1.0", "0.16.0rc1"]:
            self.distribution.version = version
            with (
                self.subTest(version=version),
                self.assertRaises(provenance.ContractError),
            ):
                self.check()
        self.distribution.version = "0.15.9"
        self.assertEqual(self.check("smonitor")["version"], "0.15.9")
        self.distribution.version = "not-a-version"
        with self.assertRaises(ValueError):
            self.check("smonitor")


if __name__ == "__main__":
    unittest.main()
