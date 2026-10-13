"""Guard major-release notices, official identity and idempotent owner decisions."""

import json
import shlex
import unittest
from pathlib import Path

import yaml
from packaging.specifiers import SpecifierSet

from devtools.scripts import conda_environment_tools as environments
from devtools.scripts import upstream_release_watch as watch


class ReleaseWatchTests(unittest.TestCase):
    def notice(self, tag="3.0.0"):
        return watch.inspect_release("mamba-org/mamba", {
            "tag_name": tag, "draft": False, "prerelease": False,
            "html_url": "https://github.com/mamba-org/mamba/releases/tag/" + tag,
        }, ">=2.9.0,<3")

    def test_future_major_alert_and_current_minor_membership_are_distinct_from_tests(self):
        self.assertEqual("within-declared-range", self.notice("2.9.0")["state"])
        self.assertEqual("within-declared-range", self.notice("2.10.0")["state"])
        self.assertEqual("review-required", self.notice()["state"])
        self.assertEqual(self.notice()["marker"], self.notice("3.1.0")["marker"])

    def test_unverified_prerelease_and_foreign_identity_are_rejected(self):
        for alterations in ({"prerelease": True}, {"draft": True},
                            {"html_url": "https://example.com/untrusted"},
                            {"tag_name": "3.0.0rc1"}):
            with self.subTest(alterations=alterations), self.assertRaises(ValueError):
                watch.inspect_release("mamba-org/mamba", {
                    "tag_name": "3.0.0", "draft": False, "prerelease": False,
                    "html_url": self.notice()["url"], **alterations,
                }, ">=2.9.0,<3")

    def test_existing_open_or_closed_issue_prevents_repeat_or_overwriting_human_decision(self):
        for state in ("open", "closed"):
            calls = []
            def request(arguments):
                calls.append(arguments)
                return [[{"number": 1, "state": state, "html_url": "https://github.com/uibcdf/molsyssuite/issues/1",
                          "body": self.notice()["marker"] + "\nHuman decision retained."}]]
            result = watch.deliver_notice("uibcdf/molsyssuite", self.notice(), "uibcdf/molsyssuite#116", request=request)
            self.assertEqual("existing-owner-follow-up", result["state"])
            self.assertEqual(state, result["issue_state"])
            self.assertEqual(1, len(calls))

    def test_creation_uses_exact_structured_body_and_retires_its_private_input(self):
        paths = []
        def request(arguments):
            if "POST" not in arguments:
                return [[], []]
            path = Path(arguments[-1]); paths.append(path)
            body = json.loads(path.read_text())
            self.assertIn(self.notice()["marker"], body["body"])
            self.assertIn("uibcdf/molsyssuite#116", body["body"])
            self.assertEqual(["proposal"], body["labels"])
            return {"number": 3, "html_url": "https://github.com/uibcdf/molsyssuite/issues/3"}
        self.assertEqual("created-owner-follow-up", watch.deliver_notice(
            "uibcdf/molsyssuite", self.notice(), "uibcdf/molsyssuite#116", request=request)["state"])
        self.assertFalse(paths[0].exists())

    def test_duplicate_or_invalid_inventory_fails_without_mutation(self):
        item = {"body": self.notice()["marker"]}
        for value in (None, {}, [[item, item]]):
            with self.subTest(value=value), self.assertRaises(ValueError):
                watch.deliver_notice("uibcdf/molsyssuite", self.notice(), "#116", request=lambda arguments: value)

    def test_admitted_release_makes_no_issue_requests(self):
        def request(arguments):
            self.fail("compatible range does not need an issue request")
        self.assertEqual({"state": "no-notice-needed"}, watch.deliver_notice(
            "uibcdf/molsyssuite", self.notice("2.9.0"), "#116", request=request))

    def test_workflow_observes_the_operator_range_and_restricts_notification_writes(self):
        root = Path(__file__).resolve().parents[1]
        workflow = yaml.safe_load((root / '.github/workflows/check-conda-channel-compatibility.yaml').read_text())
        native = workflow['jobs']['native-compatibility']
        latest = next(cell for cell in native['strategy']['matrix']['include'] if cell['label'] == 'latest-2.x')
        self.assertEqual(SpecifierSet(environments.MAMBA_CHANNEL_RANGE), SpecifierSet(latest['spec'].removeprefix('mamba')))
        observer = workflow['jobs']['release-watch']
        invocation = shlex.split(next(step['run'] for step in observer['steps'] if 'run' in step and 'upstream_release_watch.py' in step['run']))
        self.assertEqual(SpecifierSet(environments.MAMBA_CHANNEL_RANGE), SpecifierSet(invocation[invocation.index('--supported-range') + 1]))
        self.assertEqual('write', observer['permissions']['issues'])
        self.assertIn("github.event_name != 'pull_request'", observer['if'])
        self.assertNotIn('issues', native.get('permissions', {}))
        triggers = workflow.get('on', workflow.get(True))
        self.assertIn('schedule', triggers)
        self.assertIn('workflow_dispatch', triggers)
