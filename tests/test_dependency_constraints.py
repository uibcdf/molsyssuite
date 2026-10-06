"""Shared compatibility checks must protect floors across route purposes."""

import unittest

from devtools.scripts import dependency_constraints as contracts


class DependencyConstraintsTests(unittest.TestCase):
    def test_conda_prefix_and_build_pin_retain_different_semantics(self):
        prefix = contracts.conda_requirement("provider =0.14.0")
        exact = contracts.conda_requirement("provider =0.14.0=py_0")
        self.assertEqual(str(prefix.requirement.specifier), "<0.14.1,>=0.14.0")
        self.assertEqual(prefix.version_kind, "prefix")
        self.assertIsNone(prefix.build)
        self.assertEqual(str(exact.requirement.specifier), "==0.14.0")
        self.assertEqual(exact.build, "py_0")
        self.assertEqual(exact.version_kind, "exact")

    def test_conda_prefix_uses_whole_segments(self):
        requirement = contracts.conda_requirement("python=3.14").requirement
        self.assertIn("3.14.9", requirement.specifier)
        self.assertNotIn("3.140", requirement.specifier)
        self.assertNotIn("3.15", requirement.specifier)

    def test_reviewed_narrowing_is_general_and_checks_the_entire_release_range(self):
        items = [contracts.conda_requirement("provider=0.14.0")]
        self.assertEqual(
            contracts.compare_requirements(
                items,
                ["provider>=0.14.0,<1"],
                allow_narrowing=True,
                narrowing_reason="Test the qualified public provider selection",
            ),
            ["provider"],
        )
        for expected in ("provider>=0.14.0,<0.14.0.5", "provider>=0.14.0.1"):
            with self.subTest(expected=expected), self.assertRaises(ValueError):
                contracts.compare_requirements(
                    items, [expected], allow_narrowing=True, narrowing_reason="test"
                )

    def test_missing_weaker_wider_and_empty_constraints_fail(self):
        for selected in (
            "other>=0.16,<1",
            "provider",
            "provider>=0.15,<1",
            "provider>=0.16",
            "provider>=0.16,<=1",
            "provider>=0.17,<0.17",
        ):
            with self.subTest(selected=selected), self.assertRaises(ValueError):
                contracts.compare_requirements(
                    [contracts.conda_requirement(selected)],
                    ["provider>=0.16,<1"],
                    allow_narrowing=True,
                    narrowing_reason="Reviewed test selection",
                )

    def test_public_routes_preserve_the_advertised_range(self):
        with self.assertRaisesRegex(ValueError, "public range"):
            contracts.compare_requirements(
                [contracts.conda_requirement("provider>=0.17,<1")],
                ["provider>=0.16,<1"],
            )
        contracts.compare_requirements(
            [contracts.conda_requirement("provider<1,>=0.16.0")],
            ["provider>=0.16,<1"],
        )

    def test_narrowing_needs_a_reason_and_cannot_excuse_incompatibility(self):
        with self.assertRaisesRegex(ValueError, "narrowing reason"):
            contracts.compare_requirements(
                [contracts.conda_requirement("provider>=0.17,<1")],
                ["provider>=0.16,<1"],
                allow_narrowing=True,
            )
        with self.assertRaisesRegex(ValueError, "violates"):
            contracts.compare_requirements(
                [contracts.conda_requirement("provider=0.15")],
                ["provider>=0.16,<1"],
                allow_narrowing=True,
                narrowing_reason="An explanation cannot waive the floor",
            )

    def test_unsupported_or_conditional_expressions_fail_for_review(self):
        for expression in (
            "provider>=1|<0.5",
            "provider>=1rc1",
            "provider>=1,!=1.2",
            "provider=",
            "provider=1=",
            "provider>=1; python_version<'3.14'",
            "channel::provider=1",
        ):
            with self.subTest(expression=expression), self.assertRaises(ValueError):
                contracts.conda_requirement(expression)

    def test_resolved_versions_protect_prerelease_floor_and_missing_installations(self):
        project = {
            "requires-python": ">=3.11,<3.15",
            "dependencies": ["provider>=0.14.0,<1"],
        }
        result = contracts.check_installed(
            project, version_for=lambda name: "0.14.0", python_version="3.14.7"
        )
        self.assertEqual(result["provider"], "0.14.0")
        for version in ("0.13.9", "0.14.0.dev1", "1.0"):
            with self.subTest(version=version), self.assertRaises(ValueError):
                contracts.check_installed(
                    project,
                    version_for=lambda name, selected=version: selected,
                    python_version="3.14.7",
                )
        with self.assertRaisesRegex(ValueError, "Python"):
            contracts.check_installed(
                project, version_for=lambda name: "0.14.0", python_version="3.15"
            )


if __name__ == "__main__":
    unittest.main()
