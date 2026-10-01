"""Keep coverage publishing separate from untrusted test execution."""

import unittest
from pathlib import Path

import yaml


class CoverageWorkflowTests(unittest.TestCase):
    def workflow(self):
        path = (
            Path(__file__).resolve().parents[1]
            / ".github/workflows/validate_governance.yaml"
        )
        return yaml.load(path.read_text(), Loader=yaml.BaseLoader)

    def test_pr_tests_cannot_request_publisher_credentials(self):
        workflow = self.workflow()
        self.assertEqual(workflow["permissions"], {"contents": "read"})
        self.assertNotIn("permissions", workflow["jobs"]["governance"])
        publisher = workflow["jobs"]["coverage-upload"]
        self.assertEqual(publisher["needs"], "governance")
        self.assertEqual(
            publisher["if"],
            "github.event_name != 'pull_request' && github.ref == 'refs/heads/main'",
        )
        self.assertEqual(
            publisher["permissions"], {"contents": "read", "id-token": "write"}
        )
        upload = publisher["steps"][-1]
        self.assertEqual(upload["with"]["fail_ci_if_error"], "true")
        self.assertEqual(upload["with"]["use_oidc"], "true")
        self.assertEqual(upload["with"]["disable_search"], "true")
        self.assertRegex(upload["uses"], r"^codecov/codecov-action@[a-f0-9]{40}$")

    def test_existing_administrative_suite_is_measured_without_scientific_consumers(
        self,
    ):
        job = self.workflow()["jobs"]["governance"]
        measured = next(
            step
            for step in job["steps"]
            if step.get("name") == "Test the governance guard"
        )
        self.assertNotIn("if", measured)
        self.assertNotIn("continue-on-error", measured)
        self.assertIn(
            "--source=devtools/scripts -m unittest discover -s tests -v",
            measured["run"],
        )
        artifact = job["steps"][-1]
        self.assertEqual(artifact["with"]["path"], "coverage.xml")
        self.assertEqual(artifact["with"]["if-no-files-found"], "error")
