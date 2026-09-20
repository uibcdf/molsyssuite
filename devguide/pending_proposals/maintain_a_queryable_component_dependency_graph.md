---
summary: Maintain a queryable dependency graph for MolSysSuite components
issue: uibcdf/molsyssuite#30
status: active
opened: 2026-09-20
closed:
verification: inspected
area: [governance, dependencies, releases, tooling]
guard:
normative:
blocked_by: []
supersedes: []
---

# Maintain a queryable dependency graph for MolSysSuite components

**Reported:** 2026-09-20, after the Python 3.14 rollout required reconstructing the
SMonitor--DepDigest--ArgDigest--PyUnitWizard order from four package manifests.
**Status:** active; ownership and desired queries are defined, but the schema and generator
are not yet implemented.

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

The eventual guard belongs in `tests/test_governance.py`; the normative record should be a
new dependency-graph policy linked from the generated view.

## Dependencies and risks

The primary risks are confusing optional or development relationships with hard runtime
requirements, duplicating the existing guide-consumer graph, and emitting a plausible but
unsafe linear order through a dependency cycle. Typed direct edges, manifest checks, and
strong-component condensation address those risks.

## Provenance

Source inspection of `suite.toml` and registered component `pyproject.toml` files on
2026-09-20. The proposal was prompted by the sequencing work in `uibcdf/molsyssuite#29`.
