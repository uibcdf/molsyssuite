"""A job count cannot prove complete installed-matrix execution."""

import copy
import unittest
from unittest.mock import patch

from devtools.scripts import verify_installed_matrix as matrix

SHA = "a" * 40
PROFILE = dict(platforms=["linux-64", "win-64"], python_versions=["3.13", "3.14"],
               prepare_job="prepare", required_steps=["Install exact pair", "Validate installed files"])
RUN = dict(id=123, run_attempt=1, head_sha=SHA, path=".github/workflows/pair.yaml",
           display_title="Exact pair builds", status="completed", conclusion="success")


def jobs(profile=PROFILE):
    result = []
    for index, name in enumerate(matrix.expected_jobs(profile)):
        result.append(dict(id=index + 1, name=name, run_id=123, run_attempt=1, head_sha=SHA,
                      status="completed", conclusion="success", steps=[
                      dict(name=step, status="completed", conclusion="success") for step in profile["required_steps"]]))
    return result


def verify(run, observed, profile=PROFILE):
    return matrix.verify_snapshot(run, observed, run_id=123, candidate=SHA,
            workflow=RUN["path"], title=RUN["display_title"], profile=profile)


class InstalledMatrixTests(unittest.TestCase):
    def test_other_component_job_templates_are_supported_without_repo_names(self):
        profile = dict(PROFILE, job_template="Installed {python} on {platform}")
        self.assertEqual(verify(RUN, jobs(profile), profile)["state"], "verified")

    def test_four_and_five_platform_profiles_are_verified_by_cells(self):
        for platforms in (["linux-64", "linux-aarch64", "osx-arm64", "win-64"],
                          ["linux-64", "linux-aarch64", "osx-64", "osx-arm64", "win-64"]):
            profile = dict(PROFILE, platforms=platforms, python_versions=["3.11", "3.12", "3.13", "3.14"])
            self.assertEqual(verify(RUN, jobs(profile), profile)["state"], "verified")

    def test_equal_job_count_with_missing_or_duplicate_cell_fails(self):
        observed = jobs()
        observed[-1]["name"] = observed[-2]["name"]
        with self.assertRaises(matrix.MatrixError):
            verify(RUN, observed)
        observed[-1]["name"] = "unrelated successful job"
        with self.assertRaises(matrix.MatrixError):
            verify(RUN, observed)

    def test_successful_run_cannot_hide_skipped_or_failed_cells_and_steps(self):
        for conclusion in ("skipped", "failure", "cancelled"):
            observed = jobs()
            observed[-1]["conclusion"] = conclusion
            with self.assertRaises(matrix.MatrixError):
                verify(RUN, observed)
            observed = jobs()
            observed[-1]["steps"][-1]["conclusion"] = conclusion
            with self.assertRaises(matrix.MatrixError):
                verify(RUN, observed)
        observed = jobs()
        observed[-1]["steps"].pop()
        with self.assertRaises(matrix.MatrixError):
            verify(RUN, observed)

    def test_mixed_source_or_attempt_and_wrong_pair_title_fail(self):
        for field, value in (("head_sha", "b" * 40), ("run_attempt", 2), ("run_id", 456)):
            observed = jobs()
            observed[-1][field] = value
            with self.assertRaises(matrix.MatrixError):
                verify(RUN, observed)
        for field, value in (("display_title", "other pair"), ("path", ".github/workflows/other.yaml")):
            with self.assertRaises(matrix.MatrixError):
                verify(dict(RUN, **{field: value}), jobs())

    def test_incomplete_inventory_and_rerun_race_fail_closed(self):
        for document, last in ((dict(total_count=100, jobs=jobs()), RUN),
                               (dict(total_count=len(jobs()), jobs=jobs()), dict(RUN, run_attempt=2))):
            with patch.object(matrix, "read_json", side_effect=[copy.deepcopy(RUN), document, last]):
                with self.assertRaises(matrix.MatrixError):
                    matrix.verify("uibcdf/example", 123, SHA, RUN["path"], RUN["display_title"], PROFILE, "token")

    def test_native_acquisition_is_attempt_bound_and_read_only(self):
        with patch.object(matrix, "read_json", side_effect=[RUN, dict(total_count=len(jobs()), jobs=jobs()), RUN]) as read:
            result = matrix.verify("uibcdf/example", 123, SHA, RUN["path"], RUN["display_title"], PROFILE, "token")
        self.assertEqual(result["state"], "verified")
        self.assertIn("/attempts/1/jobs?per_page=100", read.call_args_list[1].args[0])
