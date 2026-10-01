---
summary: Maintain a queryable dependency graph for MolSysSuite components
issue: uibcdf/molsyssuite#30
status: resolved
opened: 2026-09-20
closed: 2026-10-01
verification: measured
area: [governance, dependencies, releases, tooling]
guard: tests/test_dependency_graph.py
normative: devguide/dependency_graph_policy.md
blocked_by: []
supersedes: []
---

# Maintain a queryable dependency graph for MolSysSuite components

**Reported:** 2026-09-20, after the Python 3.14 rollout required reconstructing the
SMonitor--DepDigest--ArgDigest--PyUnitWizard order from four package manifests.
**Status:** Resolved: registry, queries, generated view and independent hosted
manifest audit are implemented and verified.

## What

Make `suite.toml` the authority for direct, suite-internal dependency relationships and
generate a human-readable dependency view from it. Maintainers must be able to ask where a
compatibility migration, coordinated staging window, or release sequence starts, which
components follow, and where cycles prevent an ordinary topological order.

The registry must type relationships rather than collapse unlike contracts. The initial
types are runtime, test tooling, CI tooling, and documentation tooling. Third-party
dependencies remain authoritative in component package metadata, and guide distribution
continues to use the separate `[[guides]]` consumer inventory.

## How

1. Add direct typed edges between registered members to `suite.toml`, with one documented
   edge direction and no transitive duplicates.
2. Validate endpoints, edge types, uniqueness, self-edges, and consistency between runtime
   edges and each available package manifest.
3. Compute strongly connected components before topological layers. A real cycle such as
   MolSysMT--MolSysViewer is reported as one ordered unit and never hidden by an arbitrary
   member ordering.
4. Add an offline command that can print the complete graph or filter it by relationship
   type, cohort, provider, or consumer, and can emit safe migration/release layers.
5. Generate a compact Markdown/Mermaid view under `devguide/` from the registry and verify
   it with `--check`; contributors edit the registry, never the rendered graph.
6. Document how component-specific optional relationships and temporary exceptions are
   represented without turning an import-time possibility into a hard runtime edge.

## Why

The 3.14 rollout exposed a recurrent coordination cost: the correct initial order had to
be rediscovered from scattered manifests and team memory. The same information controls
Conda staging, promotion, compatibility testing, provider-first debugging, and the impact
of changing a shared API. Recording it once prevents each component team from repeating
the analysis and makes central plans reviewable.

## What is measured and what is assumed

**Inspected on 2026-09-20:** package metadata currently declares the direct chain
SMonitor -> DepDigest -> ArgDigest and SMonitor/DepDigest -> PyUnitWizard. MolSysMT depends
on SMonitor, DepDigest, ArgDigest, PyUnitWizard, and MolSysViewer; MolSysViewer depends on
the same four support libraries and MolSysMT, forming a real runtime cycle. Pytest Receptor
depends on pytest rather than another suite member, while GH Run Receptor has no Python
runtime dependency; their suite relationships are tooling edges, not runtime edges.

**Assumed pending implementation:** the remaining registered members can be represented by
the initial edge vocabulary. Any relationship that cannot must produce a schema proposal,
not an untyped free-form label.

## Alternatives and refuted paths

- A manually maintained diagram was rejected because it can drift from the ordering used
  by automation.
- Deriving everything dynamically from package manifests was rejected because test and CI
  tooling relationships are not runtime requirements, and some component metadata is
  dynamic or distributed across formats.
- Treating guide consumers as package dependencies was rejected because synchronization
  topology does not imply installation or release order.
- Rejecting every cycle was rejected because the MolSysMT--MolSysViewer hard dependency
  cycle exists and must be made visible to coordinated staging rather than erased from the
  model.

## Scope and exclusions

The graph contains only registered MolSysSuite members. It does not inventory every
third-party package, replace lock files, infer import-level optional dependencies, or
declare that an edge has been tested. Evidence and current support state remain in rollout
records and component repositories.

## Acceptance criteria

- `suite.toml` represents every known direct suite-internal relationship with a bounded
  type and unambiguous direction.
- Offline validation rejects unknown endpoints, duplicate/self edges, invalid types, and
  stale generated documentation.
- A command reports dependency layers for a selected cohort or relationship type.
- Strongly connected components are explicit in text and machine-readable output.
- The Python 3.14 cohort order is reproducible from the graph.
- The generated human view is linked from `devguide/README.md` and explains how it is
  maintained.
- Runtime registry edges are checked against static package metadata where available,
  with explicit tracked exceptions for dynamic or non-Python manifests.

The guard is the focused `tests/test_dependency_graph.py`; the normative record
is `devguide/dependency_graph_policy.md`, linked from the generated view.

## Dependencies and risks

The primary risks are confusing optional or development relationships with hard runtime
requirements, duplicating the existing guide-consumer graph, and emitting a plausible but
unsafe linear order through a dependency cycle. Typed direct edges, manifest checks, and
strong-component condensation address those risks.

## Provenance

Source inspection of `suite.toml` and registered component `pyproject.toml` files on
2026-09-20. The proposal was prompted by the sequencing work in `uibcdf/molsyssuite#29`.

## Implementation and source inventory, 2026-10-01

The schema-v1 registry contains 131 direct typed relationships across all 15
registered members: 44 runtime (41 required, three extra-conditional), 43 test
profile/tooling, 13 CI/operator tooling and 31 documentation profile/tooling.
Each carries immutable inspected-source references. Runtime and extra declarations
were acquired from 14 fetched isolated static Python manifests; test/docs profiles
come from their actual extras, environments and workflow bootstraps. CI/operator
relationships use explicit instructions/configuration or dated operator evidence,
not merely guide-copy presence. These are dependency declarations, not passing
scientific tests or installation claims. MolSys-AI's non-Python umbrella has no
invented runtime edge; its child repositories are outside this registered graph.

The graph reuses the existing sibling requirement parser and owned bounded
exception validator. No component code, metadata or scientific tests were
changed. The current inventory needs no manifest exception. Known missing
component dependency declarations retain their component issues; an import
observation is not silently promoted into a public package requirement.

Required-runtime queries reproduce the Python 3.14 roster in four layers:
SMonitor plus independent receptor tools; DepDigest; ArgDigest and PyUnitWizard;
the coordinated MolSysMT–MolSysViewer unit. PyUnitWizard is optional for ArgDigest's
`all`/`pyunitwizard` extras; it is not a required ArgDigest edge. This supersedes
any interpretation of the initial chain sketch as a literal serial ordering.
Provider queries include transitive affected consumers and prerequisites; consumer
and cohort queries keep prerequisite closure. Optional and tooling relationships
do not change default required-runtime ordering. All selected cycles remain
explicit groups in both JSON and the generated Markdown/Mermaid view.

Thirteen regression tests exercise direction/layers, deterministic output,
strongly connected cycles with external providers, cohort/consumer prerequisite
closure, provider impact, optional/tooling isolation, unknown selectors,
malformed/duplicate/self edges, immutable evidence, manifest/extra drift, missing
or dynamic manifests, bounded exception isolation and stale generated views.
The full local metadata comparison and generated-view check passed. Hosted
14-member manifest audit runs separately from the offline governance gate and
executes no package imports, installations or scientific suites.

## Resolution and acceptance audit, 2026-10-01

Provider `80475629675ab6465f1e499411e19c4ee846ae97` implements the registered
normative policy, schema-v1 registry, shared query/generator and independent
manifest checker. Thirteen mechanism-focused graph tests and the complete
237-test administrative suite passed. Native governance 36877755554 passed;
native manifest audit 36877755471 passed all 14 Python member checks against
their current remote source. Component-guide audit 36877755345 and vendored-guide
audit 36877755239 also passed. No exception was required for the measured inventory.

Every acceptance criterion is met: bounded typed direct relationships with
immutable provenance; negative validation and stale-view rejection; executable
cohort/type/provider/consumer queries with safe prerequisite closure; explicit
strong components and provider-first layers; reproducible 3.14 roster ordering;
linked generated Markdown/Mermaid; and source-only comparison with available
static manifests. The focused guard rejects the graph and drift failure mechanisms;
its successful addressability does not certify scientific package behavior.

The central record owns the graph and its new metadata audit. No member metadata,
scientific implementation, CI execution profile or package release was changed
for this proposal. Existing component defects, scientific reviews and publication
authorization retain their owners and scope.
