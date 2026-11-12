"""Reject false absence from capped, failed or malformed GitHub inventories."""

import json
import subprocess
import unittest
from unittest.mock import patch

from devtools.scripts import component_issue_labels as labels
from devtools.scripts import github_inventory as inventory
from devtools.scripts import upstream_release_watch as watch


class InventoryConsumerTests(unittest.TestCase):
    def test_label_audit_sees_findings_beyond_the_old_thousand_label_cap(self):
        records = [
            {"name": f"area-{i}", "color": "000000", "description": ""}
            for i in range(1000)
        ]
        records.append({"name": "component:unregistered", "color": "000000"})

        def transport(arguments):
            if arguments[:2] == ["label", "list"]:
                return json.dumps(
                    records[: int(arguments[arguments.index("--limit") + 1])]
                )
            self.assertIn("--paginate", arguments)
            self.assertIn("--slurp", arguments)
            return json.dumps(
                [records[i : i + 100] for i in range(0, len(records), 100)]
            )

        with patch.object(labels, "_run_gh", side_effect=transport):
            acquired = labels._list_labels("uibcdf/molsyssuite")
        findings, _ = labels.analyze(
            "uibcdf/molsyssuite", acquired, labels._load_policy()
        )
        self.assertEqual(len(acquired), 1001)
        self.assertTrue(any(x.code == "UNKNOWN" for x in findings))

    def test_invalid_or_failed_issue_inventory_never_creates_a_duplicate_notice(self):
        notice = watch.inspect_release(
            "mamba-org/mamba",
            {
                "tag_name": "3.0.0",
                "draft": False,
                "prerelease": False,
                "html_url": "https://github.com/mamba-org/mamba/releases/tag/3.0.0",
            },
            ">=2,<3",
        )
        for value in ([], None, {}, [None], [[{"number": True, "state": "open"}]]):
            calls = []

            def request(arguments):
                calls.append(arguments)
                if "POST" in arguments:
                    self.fail("an incomplete acquisition must not authorize creation")
                return value

            with self.subTest(value=value), self.assertRaises(ValueError):
                watch.deliver_notice(
                    "uibcdf/molsyssuite", notice, "#171", request=request
                )
            self.assertTrue(all("POST" not in call for call in calls))

        def unavailable(arguments):
            raise subprocess.CalledProcessError(1, arguments)

        with self.assertRaises(ValueError):
            watch.deliver_notice(
                "uibcdf/molsyssuite", notice, "#171", request=unavailable
            )


class CompleteInventoryTests(unittest.TestCase):
    def test_native_transport_requests_all_states_and_pages_before_filtering_prs(self):
        rows = [
            {"number": i + 1, "state": "CLOSED" if i % 2 else "open", "body": None}
            for i in range(650)
        ]
        rows[0]["pull_request"] = {}
        pages = [rows[i : i + 100] for i in range(0, len(rows), 100)]
        completed = subprocess.CompletedProcess([], 0, json.dumps(pages), "")
        with patch.object(inventory.subprocess, "run", return_value=completed) as run:
            result = inventory.acquire_inventory("uibcdf/example", "issues")
        command = run.call_args.args[0]
        self.assertIn("--paginate", command)
        self.assertIn("--slurp", command)
        self.assertIn("state=all&per_page=100", command[-1])
        self.assertNotIn("--limit", command)
        self.assertTrue(run.call_args.kwargs["check"])
        self.assertEqual(result.page_count, 7)
        self.assertEqual(len(result.records), 649)
        self.assertEqual(result.records[-1]["number"], 650)
        self.assertEqual({x["state"] for x in result.records}, {"open", "closed"})
        self.assertEqual(result.pull_requests_excluded, 1)
        self.assertNotIn("records", result.summary())

    def test_valid_empty_and_blank_issue_bodies_remain_distinct_from_no_pages(self):
        self.assertEqual(
            inventory.acquire_inventory(
                "uibcdf/example", "issues", request=lambda args: [[]]
            ).records,
            [],
        )
        rows = [
            {"number": i + 1, "state": "open", "body": body}
            for i, body in enumerate((None, "", "normal body"))
        ]
        result = inventory.acquire_inventory(
            "uibcdf/example", "issues", request=lambda args: [rows]
        )
        self.assertEqual(len(result.records), 3)
        self.assertEqual(result.summary()["state"], "complete")

    def test_malformed_duplicate_and_over_bound_acquisitions_return_no_inventory(self):
        issue = {"number": 1, "state": "open", "body": ""}
        for payload in (
            [],
            {},
            None,
            [None],
            [[None]],
            [[issue, issue]],
            [[{**issue, "state": "unknown"}]],
            [[{**issue, "body": []}]],
            [[{**issue, "number": True}]],
            [[issue] * 101],
        ):
            with (
                self.subTest(payload=payload),
                self.assertRaises(inventory.InventoryUnavailable),
            ):
                inventory.acquire_inventory(
                    "uibcdf/example", "issues", request=lambda args: payload
                )
        with (
            patch.object(inventory, "MAX_PAGES", 1),
            self.assertRaises(inventory.InventoryUnavailable),
        ):
            inventory.acquire_inventory(
                "uibcdf/example", "issues", request=lambda args: [[issue], []]
            )
        with (
            patch.object(inventory, "MAX_RESPONSE_BYTES", 1),
            self.assertRaises(inventory.InventoryUnavailable),
        ):
            inventory.acquire_inventory(
                "uibcdf/example", "issues", request=lambda args: [[]]
            )
        with self.assertRaises(inventory.InventoryUnavailable):
            inventory.acquire_inventory(
                "uibcdf/example",
                "labels",
                request=lambda args: [[{"name": "Bug"}, {"name": "bug"}]],
            )

    def test_invalid_scope_makes_no_remote_request(self):
        for repository, resource in (
            ("../bad", "issues"),
            ("uibcdf/repo?token=x", "labels"),
            ("uibcdf/..", "issues"),
            ("uibcdf/example", "search"),
        ):
            with (
                self.subTest(repository=repository, resource=resource),
                self.assertRaises(inventory.InventoryUnavailable),
            ):
                inventory.acquire_inventory(
                    repository,
                    resource,
                    request=lambda args: self.fail("invalid request"),
                )

    def test_closed_notice_beyond_old_cap_is_preserved_and_pr_match_is_ignored(self):
        notice = watch.inspect_release(
            "mamba-org/mamba",
            {
                "tag_name": "3.0.0",
                "draft": False,
                "prerelease": False,
                "html_url": "https://github.com/mamba-org/mamba/releases/tag/3.0.0",
            },
            ">=2,<3",
        )
        rows = [{"number": i + 1, "state": "open", "body": None} for i in range(600)]
        rows[0].update({"pull_request": {}, "body": notice["marker"]})
        rows[-1].update(
            {
                "state": "CLOSED",
                "body": notice["marker"],
                "html_url": "https://github.com/uibcdf/molsyssuite/issues/600",
            }
        )
        calls = []

        def request(arguments):
            calls.append(arguments)
            self.assertNotIn("POST", arguments)
            return [rows[i : i + 100] for i in range(0, len(rows), 100)]

        result = watch.deliver_notice(
            "uibcdf/molsyssuite", notice, "#171", request=request
        )
        self.assertEqual(result["state"], "existing-owner-follow-up")
        self.assertEqual(result["number"], 600)
        self.assertEqual(result["issue_state"], "closed")
        self.assertEqual(len(calls), 1)
