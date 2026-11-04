"""Public source observations cannot execute members or become CI acceptance."""

from __future__ import annotations

import copy
import hashlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError, URLError

import yaml

from devtools.scripts import observe_ci_profiles as observer
from devtools.scripts import public_ci_sources as sources


class CIProfileObserverTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.scratch = Path(temporary.name)
        self.repository = "uibcdf/example"
        self.head, self.tree = "a" * 40, "b" * 40
        self.files = {
            "pyproject.toml": b'[tool.pytest.ini_options]\ntestpaths=["tests"]\n',
            ".github/workflows/ci.yml": b"""on:
  push:
  workflow_dispatch:
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python: ["3.14"]
    steps:
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python }}
      - run: python -m pytest tests
""",
            "tests/conftest.py": b'raise RuntimeError("member code must never run")\n',
        }
        self.data = {
            "members": [{"repository": self.repository, "name": "example"}],
            "python-ci-reviews": [
                {
                    "repository": self.repository,
                    "review-issue": self.repository + "#1",
                    "state": "partial",
                    "routine-test-level": "full",
                }
            ],
        }
        self.profiles = {
            "schema-version": 2,
            "mode": "informational",
            "profiles": [
                {
                    "repository": self.repository,
                    "review-issue": self.repository + "#1",
                    "reviewed-source": "c" * 40,
                    "inputs": {
                        path: hashlib.sha256(raw).hexdigest()
                        for path, raw in self.files.items()
                    },
                    "collection-roots": ["tests"],
                    "lanes": [
                        {
                            "workflow": "ci.yml",
                            "job": "test",
                            "test-level": "full",
                            "events": {"push": ["3.14"]},
                        }
                    ],
                }
            ],
        }
        self.metadata = {
            "private": False,
            "visibility": "public",
            "full_name": self.repository,
            "default_branch": "main",
        }
        self.requests = []
        self.extra_entries = []
        self.truncated = False

    def entries(self):
        rows, parents = [], set()
        for path, raw in self.files.items():
            parents.update(str(p) for p in Path(path).parents if str(p) != ".")
            blob = hashlib.sha1(
                b"blob " + str(len(raw)).encode() + b"\0" + raw, usedforsecurity=False
            ).hexdigest()
            rows.append(
                {
                    "path": path,
                    "mode": "100644",
                    "type": "blob",
                    "sha": blob,
                    "size": len(raw),
                }
            )
        rows += [
            {"path": path, "mode": "040000", "type": "tree", "sha": "d" * 40}
            for path in sorted(parents)
        ]
        return rows + self.extra_entries

    def read_json(self, url):
        self.requests.append(url)
        base = "https://api.github.com/repos/" + self.repository
        if url == base:
            return copy.deepcopy(self.metadata)
        if url == base + "/commits/main":
            return {"sha": self.head, "commit": {"tree": {"sha": self.tree}}}
        if url == base + "/git/trees/" + self.tree + "?recursive=1":
            return {
                "sha": self.tree,
                "truncated": self.truncated,
                "tree": self.entries(),
            }
        self.fail("unexpected service request")

    def read_bytes(self, url):
        self.requests.append(url)
        prefix = f"https://raw.githubusercontent.com/{self.repository}/{self.head}/"
        self.assertTrue(url.startswith(prefix))
        return self.files[url[len(prefix) :]]

    def observe(self, **kwargs):
        return observer.observe(
            self.data,
            self.profiles,
            scratch_parent=self.scratch,
            json_reader=kwargs.pop("json_reader", self.read_json),
            bytes_reader=kwargs.pop("bytes_reader", self.read_bytes),
            **kwargs,
        )

    def assert_unknown(self, report):
        self.assertTrue(
            all(
                lane["state"] == "unknown"
                for lane in report["pilot_report"]["members"][0]["lanes"]
            )
        )
        self.assertEqual(list(self.scratch.iterdir()), [])

    def test_public_immutable_projection_reuses_reader_without_member_execution(self):
        with patch.dict(
            os.environ, {"GITHUB_TOKEN": "must-not-be-used", "GH_TOKEN": "also-private"}
        ):
            report = self.observe()
        self.assertEqual(report["acquisition"][0]["source_commit"], self.head)
        member = report["pilot_report"]["members"][0]
        self.assertTrue(member["profile_inputs_current"])
        self.assertEqual(member["lanes"][0]["state"], "configured")
        self.assertEqual(member["execution_evidence"], "not_requested")
        self.assertEqual(member["backlog_clearance"], "not_evaluated")
        self.assertNotEqual(member["reviewed_source"], self.head)
        self.assertEqual(len(report["acquisition"][0]["files"]), 3)
        self.assertEqual(list(self.scratch.iterdir()), [])
        self.assertNotIn("must-not-be-used", json.dumps(report))

    def test_drift_deleted_input_and_new_config_hook_invalidate_review(self):
        baseline = copy.deepcopy(self.files)
        for change in ("drift", "deleted", "config", "hook"):
            with self.subTest(change=change):
                self.files = copy.deepcopy(baseline)
                if change == "drift":
                    self.files["pyproject.toml"] += b"# changed\n"
                elif change == "deleted":
                    del self.files["tests/conftest.py"]
                elif change == "config":
                    self.files["pytest.ini"] = b"[pytest]\naddopts=-k subset\n"
                else:
                    self.files["tests/nested/conftest.py"] = (
                        b"raise RuntimeError('do not import')\n"
                    )
                report = self.observe()
                self.assertEqual(report["acquisition"][0]["state"], "observed")
                self.assert_unknown(report)

    def test_private_identity_redirect_and_service_failures_do_not_leak_or_accept(self):
        for failure in ("private", "identity", "404", "network", "late"):
            with self.subTest(failure=failure):

                def broken(url, failure=failure):
                    if failure == "private":
                        return {
                            **self.metadata,
                            "private": True,
                            "visibility": "private",
                            "default_branch": "secret-branch",
                        }
                    if failure == "identity":
                        return {**self.metadata, "full_name": "uibcdf/renamed"}
                    if failure == "404":
                        raise HTTPError(url, 404, "sensitive-password", {}, None)
                    if failure == "network":
                        raise URLError("sensitive-password")
                    return self.read_json(url)

                def late(url):
                    if url.endswith("tests/conftest.py"):
                        raise URLError("sensitive-password")
                    return self.read_bytes(url)

                report = self.observe(json_reader=broken, bytes_reader=late)
                self.assertEqual(report["acquisition"][0]["state"], "unavailable")
                self.assert_unknown(report)
                self.assertNotIn("sensitive-password", json.dumps(report))
                self.assertNotIn("secret-branch", json.dumps(report))

    def test_complete_safe_tree_and_byte_identity_are_required(self):
        for failure in (
            "truncated",
            "traversal",
            "duplicate",
            "symlink",
            "submodule",
            "blob",
            "oversize",
        ):
            with self.subTest(failure=failure):
                self.extra_entries = []
                self.truncated = failure == "truncated"
                if failure in {"traversal", "duplicate", "symlink", "submodule"}:
                    entry = {
                        "path": "tests/../escape"
                        if failure == "traversal"
                        else "tests/linked",
                        "mode": "100644",
                        "type": "blob",
                        "sha": "e" * 40,
                        "size": 1,
                    }
                    if failure == "duplicate":
                        entry = self.entries()[0]
                    elif failure == "symlink":
                        entry["mode"] = "120000"
                    elif failure == "submodule":
                        entry.update(mode="160000", type="commit")
                    self.extra_entries = [entry]
                read = (
                    (lambda url: b"different bytes")
                    if failure == "blob"
                    else self.read_bytes
                )
                with patch.object(
                    sources,
                    "MAX_FILE_BYTES",
                    1 if failure == "oversize" else 1024 * 1024,
                ):
                    report = self.observe(bytes_reader=read)
                self.assertEqual(report["acquisition"][0]["state"], "unavailable")
                self.assert_unknown(report)

    def test_remote_collection_limit_is_checked_before_projecting_hook_names(self):
        with patch.object(sources.python_ci_status, "MAX_COLLECTION_ENTRIES", 1):
            report = self.observe()
        self.assertEqual(
            report["acquisition"][0]["reason"], "collection_inspection_limit"
        )
        self.assert_unknown(report)

    def test_dynamic_branches_survive_but_expansion_and_yaml_cycles_are_bounded(self):
        original = self.files[".github/workflows/ci.yml"]
        for failure in ("product", "alias", "script", "scenarios"):
            with self.subTest(failure=failure):
                document = yaml.load(original, Loader=yaml.BaseLoader)
                if failure == "product":
                    document["jobs"]["test"]["strategy"]["matrix"] = {
                        "a": list(range(17)),
                        "b": list(range(17)),
                    }
                elif failure == "alias":
                    document["cycle"] = document
                elif failure == "script":
                    document["jobs"]["test"]["steps"][-1]["run"] = "x" * 32769
                else:
                    document["on"]["schedule"] = [{"cron": "0 1 * * *"}] * 17
                self.files[".github/workflows/ci.yml"] = yaml.dump(document).encode()
                report = self.observe()
                self.assertEqual(report["acquisition"][0]["state"], "unavailable")
                self.assert_unknown(report)
        self.files[".github/workflows/ci.yml"] = original

    def test_malformed_catalogue_is_an_invocation_error_before_network(self):
        self.profiles["schema-version"] = 99
        with self.assertRaises(ValueError):
            self.observe()
        self.assertEqual(self.requests, [])
        self.assertEqual(list(self.scratch.iterdir()), [])

    def test_one_unavailable_member_does_not_hide_other_members(self):
        self.data["members"].append({"repository": "uibcdf/second", "name": "second"})
        review = copy.deepcopy(self.data["python-ci-reviews"][0])
        review.update(repository="uibcdf/second", **{"review-issue": "uibcdf/second#1"})
        self.data["python-ci-reviews"].append(review)
        profile = copy.deepcopy(self.profiles["profiles"][0])
        profile.update(
            repository="uibcdf/second", **{"review-issue": "uibcdf/second#1"}
        )
        self.profiles["profiles"].append(profile)

        def reader(url):
            if "/example" in url:
                raise URLError("private diagnostic")
            result = self.read_json(url.replace("/second", "/example"))
            if "full_name" in result:
                result["full_name"] = "uibcdf/second"
            return result

        report = self.observe(
            json_reader=reader,
            bytes_reader=lambda url: self.read_bytes(
                url.replace("/second", "/example")
            ),
        )
        self.assertEqual(
            [r["state"] for r in report["acquisition"]], ["unavailable", "observed"]
        )
        self.assertFalse(report["pilot_report"]["members"][0]["profile_inputs_current"])
        self.assertTrue(report["pilot_report"]["members"][1]["profile_inputs_current"])
        self.assertEqual(list(self.scratch.iterdir()), [])

    def test_tree_file_total_and_time_bounds_leave_unknown_not_partial_success(self):
        for name, value in [
            ("MAX_TREE_ENTRIES", 1),
            ("MAX_FILES", 1),
            ("MAX_SOURCE_BYTES", 1),
        ]:
            with self.subTest(limit=name), patch.object(sources, name, value):
                self.assert_unknown(self.observe())
        with patch.object(observer, "MAX_OBSERVATION_SECONDS", -1):
            report = self.observe()
        self.assertEqual(report["acquisition"][0]["reason"], "observation_time_limit")
        self.assert_unknown(report)
        self.files["tests/conftest.py"] = b"\xff"
        self.assert_unknown(self.observe())

    def test_cli_writes_normalized_artifacts_and_works_from_neutral_directory(self):
        report = self.observe()
        output = self.scratch / "report"
        with (
            patch.object(observer, "observe", return_value=report),
            redirect_stdout(io.StringIO()),
        ):
            self.assertEqual(observer.main(["--output", str(output)]), 0)
        saved = json.loads((output / "observation.json").read_text())
        self.assertEqual(saved["schema"], "molsyssuite.ci-profile-observation@1")
        self.assertIn("profiles_sha256", saved["central_inputs"])
        self.assertIn("Source/configuration", (output / "summary.md").read_text())
        script = Path(observer.__file__).resolve()
        result = subprocess.run(
            [sys.executable, str(script), "--help"],
            cwd=self.scratch,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--scratch-parent", result.stdout)

    def test_existing_destination_is_never_removed(self):
        target = self.scratch / "existing"
        target.mkdir()
        (target / "human").write_text("keep")
        with self.assertRaises(FileExistsError):
            sources.collect_public_profile(
                self.profiles["profiles"][0],
                target,
                json_reader=self.read_json,
                bytes_reader=self.read_bytes,
            )
        self.assertEqual((target / "human").read_text(), "keep")

    def test_transport_is_anonymous_bounded_and_does_not_follow_redirects(self):
        response = MagicMock()
        response.__enter__.return_value.read.return_value = b"content"
        opener = MagicMock()
        opener.open.return_value = response
        url = "https://raw.githubusercontent.com/uibcdf/example/" + self.head + "/file"
        with patch.object(sources, "build_opener", return_value=opener) as build:
            self.assertEqual(sources.read_public_bytes(url), b"content")
        request = opener.open.call_args.args[0]
        self.assertNotIn("Authorization", dict(request.header_items()))
        response.__enter__.return_value.read.assert_called_once_with(
            sources.MAX_FILE_BYTES + 1
        )
        self.assertIsNone(
            build.call_args.args[0].redirect_request(
                None, None, 302, "", {}, "https://elsewhere"
            )
        )
        for bad in (
            "http://raw.githubusercontent.com/uibcdf/example",
            "https://token@raw.githubusercontent.com/uibcdf/example",
            "https://example.org/uibcdf/example",
        ):
            with self.subTest(url=bad), self.assertRaises(sources.SourceUnavailable):
                sources.read_public_bytes(bad)

    def test_output_contract_refuses_overwrite_and_shows_unknown_as_diagnostic(self):
        report = self.observe(
            bytes_reader=lambda url: (_ for _ in ()).throw(URLError("unavailable"))
        )
        summary = observer.render_summary(report)
        self.assertIn("unavailable", summary)
        self.assertIn("review required / unknown", summary)
        self.assertIn("not executed tests", summary)
        with (
            patch.object(observer, "observe", return_value=report),
            redirect_stdout(io.StringIO()),
            redirect_stderr(io.StringIO()),
        ):
            with self.assertRaises(SystemExit) as caught:
                observer.main(["--output", str(self.scratch)])
            self.assertEqual(caught.exception.code, 2)


class CIObserverWorkflowTests(unittest.TestCase):
    def test_independent_triggers_permissions_and_artifacts_never_dispatch_members(
        self,
    ):
        root = Path(__file__).resolve().parents[1]
        workflow = yaml.load(
            (root / ".github/workflows/observe-ci-profiles.yaml").read_text(),
            Loader=yaml.BaseLoader,
        )
        self.assertEqual(set(workflow["on"]), {"push", "schedule", "workflow_dispatch"})
        self.assertEqual(workflow["permissions"], {"contents": "read"})
        self.assertEqual(workflow["on"]["push"]["branches"], ["main"])
        self.assertEqual(len(workflow["on"]["schedule"]), 1)
        steps = workflow["jobs"]["observe"]["steps"]
        commands = "\n".join(step.get("run", "") for step in steps)
        self.assertIn("observe_ci_profiles.py", commands)
        self.assertNotIn("pytest", commands)
        self.assertNotIn("workflow run", commands)
        self.assertNotIn("secrets.", json.dumps(workflow))
        self.assertFalse(any("needs" in job for job in workflow["jobs"].values()))
        self.assertEqual(steps[0]["with"]["persist-credentials"], "false")
        artifact = next(
            step
            for step in steps
            if step.get("uses", "").startswith("actions/upload-artifact@")
        )
        self.assertEqual(artifact["with"]["if-no-files-found"], "error")
        self.assertEqual(artifact["with"]["retention-days"], "30")


if __name__ == "__main__":
    unittest.main()
