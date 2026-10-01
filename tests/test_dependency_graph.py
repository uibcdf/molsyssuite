from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

import tomllib

from devtools.scripts import dependency_graph

ROOT = Path(__file__).resolve().parents[1]
SHA = "a" * 40


def edge(consumer, provider, kind="runtime", optional=False, **kwargs):
    return dict(
        consumer=consumer,
        provider=provider,
        kind=kind,
        optional=optional,
        evidence=[f"uibcdf/{consumer}@{SHA}:pyproject.toml"],
        **kwargs,
    )


class DependencyGraphTests(unittest.TestCase):
    def setUp(self):
        self.policy = {
            "members": [
                {
                    "name": n,
                    "repository": "uibcdf/" + n,
                    "capabilities": ["python-package"],
                }
                for n in ("a", "b", "c", "d")
            ],
            "dependency-graph": {
                "schema-version": 1,
                "edges": [edge("b", "a"), edge("c", "b"), edge("d", "c")],
            },
            "initiatives": {"pilot": {"priority-members": ["c"]}},
            "policies": {"python": {"transition": {"components": [{"name": "b"}]}}},
        }

    def test_provider_first_layers_are_deterministic(self):
        data = dependency_graph.query(self.policy)
        self.assertEqual(data["layers"], [[["a"]], [["b"]], [["c"]], [["d"]]])
        self.assertEqual(data["cycles"], [])
        self.policy["dependency-graph"]["edges"].reverse()
        self.assertEqual(data, dependency_graph.query(self.policy))

    def test_cycle_is_one_unit_with_external_prerequisites(self):
        self.policy["dependency-graph"]["edges"].append(edge("b", "c"))
        data = dependency_graph.query(self.policy)
        self.assertEqual(data["cycles"], [["b", "c"]])
        self.assertEqual(data["layers"], [[["a"]], [["b", "c"]], [["d"]]])

    def test_consumer_and_cohort_keep_prerequisite_closure(self):
        for kwargs in ({"consumers": ["c"]}, {"cohort": "pilot"}):
            self.assertEqual(
                dependency_graph.query(self.policy, **kwargs)["members"],
                ["a", "b", "c"],
            )
        self.assertEqual(
            dependency_graph.query(self.policy, cohort="python-3.14")["members"],
            ["a", "b"],
        )

    def test_provider_query_includes_transitive_consumers(self):
        data = dependency_graph.query(self.policy, providers=["b"])
        self.assertEqual(data["members"], ["a", "b", "c", "d"])

    def test_optional_and_tooling_edges_do_not_change_default_runtime(self):
        self.policy["dependency-graph"]["edges"].extend(
            [
                edge("a", "b", optional=True, extras=["science"]),
                edge("b", "c", kind="ci-tooling"),
            ]
        )
        self.assertEqual(dependency_graph.query(self.policy)["cycles"], [])
        self.assertEqual(
            dependency_graph.query(self.policy, include_optional=True)["cycles"],
            [["a", "b"]],
        )
        self.assertEqual(
            dependency_graph.query(self.policy, kinds={"ci-tooling"})["edges"][0][
                "kind"
            ],
            "ci-tooling",
        )

    def test_unknown_selectors_fail(self):
        for kwargs in (
            {"consumers": ["missing"]},
            {"providers": ["missing"]},
            {"cohort": "missing"},
            {"kinds": {"unknown"}},
            {"kinds": set()},
        ):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                dependency_graph.query(self.policy, **kwargs)

    def test_schema_rejects_duplicates_self_unknown_type_and_endpoints(self):
        for added in (
            edge("b", "a"),
            edge("a", "a"),
            edge("b", "missing"),
            edge("b", "a", kind="other"),
            {"consumer": []},
        ):
            policy = copy.deepcopy(self.policy)
            policy["dependency-graph"]["edges"].append(added)
            self.assertTrue(dependency_graph.validate(policy))

    def test_optional_and_immutable_evidence_contract_failures(self):
        for added in (
            edge("a", "b", optional=True),
            dict(edge("a", "b"), evidence=["uibcdf/a@main:pyproject.toml"]),
            dict(edge("a", "b"), evidence=[]),
            dict(edge("a", "b"), optional="false"),
        ):
            policy = copy.deepcopy(self.policy)
            policy["dependency-graph"]["edges"].append(added)
            self.assertTrue(dependency_graph.validate(policy))

    def manifests(self, workspace):
        for name, deps in (
            ("a", []),
            ("b", ["a>=1; python_version >= '3.11'"]),
            ("c", ["b"]),
            ("d", ["c"]),
        ):
            root = workspace / name
            root.mkdir()
            (root / "pyproject.toml").write_text(
                '[project]\nname="' + name + '"\ndependencies=' + repr(deps) + "\n"
            )

    def test_manifest_comparison_detects_missing_and_extra_runtime_edges(self):
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            self.manifests(workspace)
            self.assertEqual(
                dependency_graph.manifest_findings(self.policy, workspace), []
            )
            self.policy["dependency-graph"]["edges"].remove(edge("b", "a"))
            self.assertTrue(dependency_graph.manifest_findings(self.policy, workspace))
            self.policy["dependency-graph"]["edges"].extend(
                [edge("b", "a"), edge("d", "a")]
            )
            self.assertTrue(dependency_graph.manifest_findings(self.policy, workspace))

    def test_optional_extra_drift_is_detected_without_promoting_it_to_required(self):
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            self.manifests(workspace)
            path = workspace / "a/pyproject.toml"
            path.write_text(
                path.read_text() + '[project.optional-dependencies]\nscience=["b"]\n'
            )
            self.assertTrue(dependency_graph.manifest_findings(self.policy, workspace))
            self.policy["dependency-graph"]["edges"].append(
                edge("a", "b", optional=True, extras=["science"])
            )
            self.assertEqual(
                dependency_graph.manifest_findings(self.policy, workspace), []
            )
            path.write_text(path.read_text().replace('["b"]', "[]"))
            self.assertTrue(dependency_graph.manifest_findings(self.policy, workspace))

    def test_missing_dynamic_manifests_and_unknown_audit_selector_fail(self):
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            self.assertTrue(dependency_graph.manifest_findings(self.policy, workspace))
            self.manifests(workspace)
            (workspace / "a/pyproject.toml").write_text(
                '[project]\ndynamic=["dependencies"]\n'
            )
            self.assertTrue(dependency_graph.manifest_findings(self.policy, workspace))
            self.assertTrue(
                dependency_graph.manifest_findings(self.policy, workspace, ["unknown"])
            )

    def test_manifest_exception_cannot_suppress_schema_errors(self):
        self.policy["dependency-manifest-exceptions"] = [
            {
                "repository": "uibcdf/a",
                "issue": "uibcdf/a#1",
                "owner": "maintainers",
                "reason": "dynamic metadata",
                "removal-condition": "static profile",
                "expires-on": "2099-12-31",
            }
        ]
        with tempfile.TemporaryDirectory() as temporary:
            self.assertEqual(
                dependency_graph.manifest_findings(self.policy, Path(temporary), ["a"]),
                [],
            )
            self.policy["dependency-graph"]["edges"].append(edge("a", "a"))
            self.assertTrue(
                dependency_graph.manifest_findings(self.policy, Path(temporary), ["a"])
            )

    def test_generated_view_detects_staleness_and_names_real_suite_cycle(self):
        policy = tomllib.loads((ROOT / "suite.toml").read_text())
        text = dependency_graph.render(policy)
        self.assertIn("molsysmt, molsysviewer", text)
        self.assertEqual(
            dependency_graph.query(policy, cohort="python-3.14")["cycles"],
            [["molsysmt", "molsysviewer"]],
        )
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "graph.md"
            self.assertTrue(dependency_graph.view_findings(policy, target))
            target.write_text(text)
            self.assertEqual(dependency_graph.view_findings(policy, target), [])
            target.write_text(text.replace("molsysviewer", "wrong"))
            self.assertTrue(dependency_graph.view_findings(policy, target))


if __name__ == "__main__":
    unittest.main()
