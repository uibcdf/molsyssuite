"""Protect exact public coordinates and the historical logout failure boundary."""

import copy
import json
import os
import shlex
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError

import yaml

from devtools.scripts import verify_public_conda as verifier

ROOT = Path(__file__).resolve().parents[1]
COORDINATE = dict(package="example", version="1.2.3", subdir="noarch",
                  filename="example-1.2.3-py_2.tar.bz2", sha256="a" * 64)


def documents(coordinate=COORDINATE):
    c = coordinate
    build = c["filename"][len(c["package"] + "-" + c["version"] + "-"):]
    build = build[:-6] if build.endswith(".conda") else build[:-8]
    release = {"distributions": [{"basename": c["subdir"] + "/" + c["filename"],
               "sha256": c["sha256"], "labels": ["staging", "main"],
               "attrs": {"subdir": c["subdir"]}}]}
    section = "packages.conda" if c["filename"].endswith(".conda") else "packages"
    index = {"info": {"subdir": c["subdir"]}, section: {c["filename"]:
             {"name": c["package"], "version": c["version"], "sha256": c["sha256"],
              "build": build, "build_number": int(build.rsplit("_", 1)[1])}}}
    return release, index


class PublicCondaTests(unittest.TestCase):
    def test_successful_cli_returns_zero_with_separate_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            arguments = ["--output", str(output)]
            for key, value in COORDINATE.items():
                arguments.extend(["--" + key, value])
            with patch.object(verifier, "fetch_json", side_effect=documents()):
                self.assertEqual(verifier.main(arguments), 0)
            report = json.loads(output.read_text())
            self.assertEqual(report["state"], "verified")
            self.assertEqual(report["files"][0]["main_label"], "verified")
            self.assertEqual(report["files"][0]["solver_index"], "verified")
            self.assertNotIn("installed_pair", report)

    def test_native_and_noarch_file_formats(self):
        for coordinate in (COORDINATE, dict(COORDINATE, subdir="linux-aarch64",
                              filename="example-1.2.3-pyabi3h123_2.conda")):
            self.assertTrue(verifier.verify_snapshot(*documents(coordinate), **coordinate)
                            .endswith(coordinate["filename"]))

    def test_label_and_index_are_both_required(self):
        release, index = documents()
        release["distributions"][0]["labels"] = ["staging"]
        with self.assertRaises(verifier.VerificationPending):
            verifier.verify_snapshot(release, index, **COORDINATE)
        release, index = documents()
        index["packages"].clear()
        with self.assertRaises(verifier.VerificationPending):
            verifier.verify_snapshot(release, index, **COORDINATE)

    def test_identity_or_digest_contradictions_never_retry_into_success(self):
        for source, field, value in (("release", "sha256", "b" * 64),
                                     ("index", "sha256", "b" * 64),
                                     ("index", "name", "other"),
                                     ("index", "version", "1.2.4"),
                                     ("index", "build", "py_3"),
                                     ("index", "build_number", 3),
                                     ("index", "subdir", "linux-64")):
            release, index = documents()
            record = release["distributions"][0] if source == "release" else index["packages"][COORDINATE["filename"]]
            record[field] = value
            with patch.object(verifier, "fetch_json", side_effect=[release, index]) as fetch:
                with self.assertRaises(verifier.VerificationError):
                    verifier.verify_public(**COORDINATE, attempts=2, interval=0)
                self.assertEqual(fetch.call_count, 2)

    def test_ambiguity_and_unsafe_coordinates_fail(self):
        release, index = documents()
        release["distributions"].append(copy.deepcopy(release["distributions"][0]))
        with self.assertRaises(verifier.VerificationError):
            verifier.verify_snapshot(release, index, **COORDINATE)
        for changed in ({"filename": "../bad.conda"}, {"sha256": "A" * 64},
                        {"version": "01.2.3"}, {"filename": "other-1.2.3-py_2.tar.bz2"}):
            with self.assertRaises(verifier.VerificationError):
                verifier.validate_coordinate(**dict(COORDINATE, **changed))

    def test_bounded_propagation_retry(self):
        release, index = documents()
        release["distributions"][0]["labels"] = ["staging"]
        with patch.object(verifier, "fetch_json", side_effect=[release, index, *documents()]), patch.object(verifier.time, "sleep") as sleep:
            verifier.verify_public(**COORDINATE, attempts=2, interval=0.5)
        sleep.assert_called_once_with(0.5)

    def test_network_absence_is_not_public_success(self):
        error = HTTPError("https://api.anaconda.org", 404, "missing", {}, None)
        with patch.object(verifier, "fetch_json", side_effect=error) as fetch, patch.object(verifier.time, "sleep"):
            with self.assertRaisesRegex(verifier.VerificationError, "after 2 attempts"):
                verifier.verify_public(**COORDINATE, attempts=2, interval=0)
            self.assertEqual(fetch.call_count, 2)

    def test_inventory_rejects_missing_fields_and_duplicate_coordinates(self):
        for inventory in ([], [COORDINATE, COORDINATE], [{"package": "example"}]):
            with tempfile.TemporaryDirectory() as directory:
                source, output = Path(directory) / "inventory.json", Path(directory) / "report.json"
                source.write_text(json.dumps(inventory))
                with patch.object(verifier, "fetch_json") as fetch:
                    self.assertEqual(verifier.main(["--inventory", str(source), "--output", str(output)]), 1)
                fetch.assert_not_called()
                self.assertEqual(json.loads(output.read_text())["state"], "unverified")

    def test_complete_inventory_requires_every_expected_coordinate(self):
        second = dict(COORDINATE, package="counterpart", filename="counterpart-1.2.3-py_2.tar.bz2")
        with tempfile.TemporaryDirectory() as directory:
            source, output = Path(directory) / "inventory.json", Path(directory) / "report.json"
            source.write_text(json.dumps([COORDINATE, second]))
            with patch.object(verifier, "fetch_json", side_effect=[*documents(), *documents(second)]):
                self.assertEqual(verifier.main(["--inventory", str(source), "--output", str(output)]), 0)
            self.assertEqual(len(json.loads(output.read_text())["files"]), 2)

    def test_shared_action_exit_avoids_login_logout_failure(self):
        action = yaml.safe_load((ROOT / ".github/actions/verify-public-conda/action.yml").read_text())
        step = action["runs"]["steps"][0]
        self.assertEqual(step["shell"], "bash")
        # Run the selected shell at runner shell level 1. Changing it to bash -l
        # reintroduces the measured logout error on Debian/Ubuntu hosts.
        command = shlex.split(step["shell"])
        if command == ["bash"]:
            command += ["--noprofile", "--norc"]
        result = subprocess.run(command + ["-c", "set -euo pipefail; printf 'verified\\n'; exit 0"],
                                env=dict(os.environ, SHLVL="0"), capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "verified\n")
        self.assertNotIn("token", action["inputs"])
        self.assertNotIn("conda search", step["run"])
