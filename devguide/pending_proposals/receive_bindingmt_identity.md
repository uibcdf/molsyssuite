---
summary: Receive BindingMT as the continuing member identity and coordinate adoption.
issue: uibcdf/molsyssuite#190
status: active
opened: 2026-11-11
closed:
verification: inspected
area: [governance, integration]
guard: tests/test_governance.py::GovernanceTests::test_bindingmt_is_registered_as_incubating_scientific_component
normative: suite.toml
blocked_by: []
supersedes: []
---

# Receive the continuing BindingMT member

## What

Replace the current DockingMT identity with `uibcdf/bindingmt` / `bindingmt`,
preserving repository ID **1380446251**, Git and issue history, the incubating
primary scientific classification and every existing qualification limitation.
The maintainer accepted this early-development rename in
`uibcdf/bindingmt#108`; platform receiving remains `uibcdf/moli#97`.

## How

Update current registry/review/guide/dependency/profile identities and current
roster indexes. Preserve immutable/datetime-bound evidence and archived claims.
Publish **policy-v1.5.12** as a new immutable registry snapshot: 1.5.11 and older
tags remain untouched. BindingMT adopts the canonical caller; other members
retain their previously accepted callers and engineering values. The separate
new-member admission input is unsuitable: it would add a parallel member while
retaining the old identity in the frozen registry.

Publish the canonical MolSysSuite-guide revision first and distribute its
registered copies with `sync_vendored_guides.py`. Existing release/guide notices
#192, #191, #188, #187 and #165 own their separate provider snapshots. Canonical
sources and consumers are inspected at immutable published commits; primary
dirty/ahead/behind worktrees and the paused shared prefix are preserved.

## Why and ownership

The accepted domain covers molecular docking, fixed-identity complex prediction,
refinement, binding free-energy calculation and prediction, and binding-interface
characterization. Current bounded Vina/Vinardo/interaction-viewing profiles are
distinct from future capabilities. No new engine, numerical method, release,
public package or general support claim follows from central identity receiving.
MolSysMT retains generic molecular operations, TopoMT numerical topography,
MolSysViewer visualization and PeptideMT peptide-specific design/evaluation.

The owner supplies selected installed, administrative and DOM evidence at
`c4ba46ec1ad39dd59deede41fbe5887924ed615b`; its full ordinary gate remains
incomplete after a memory interruption. Those are owner results, not new central
scientific execution. The published receiving source selected here is recorded
in the rollout receipt. BindingMT's incremental `[skip ci]` and prohibition on
automatic manual remote dispatch remain in force; hosted evidence must retain
its actual scope and any missing qualification remains owned.

## Acceptance and regression relevance

- Exactly one canonical continuing member, with no parallel `dockingmt` member;
  the existing classification, Python transition and public-readiness states stay
  truthful. The named guard checks uniqueness, guide relationships and the
  canonical caller boundary, detecting accidental duplicate/legacy registration.
- Current registry, graph, source/profile and label identities match; original
  evidence is retained. The repository ID and previous/current remote identity
  are independently observed and retained in the receipt.
- A new immutable policy revision and actual component caller identify the
  canonical member. Executed central gates and member gates remain separate.
- Canonical guide deliveries have immutable consumer commits and exact-byte
  checks. Known consumers have an owning next step and MolI receives the handoff.
- Preserve task ownership; retire temporary clones/cache only after the necessary
  evidence is durable. Do not remove other sessions' retained #82 resources.

## Current state

Central receiving is active. No completed rollout, policy tag publication,
member runtime/public qualification or global green inventory is claimed yet.
