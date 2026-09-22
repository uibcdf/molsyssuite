---
summary: Standardize cross-component issue labels across MolSysSuite.
issue: uibcdf/molsyssuite#38
status: active
opened: 2026-09-22
closed:
verification: measured
area: [governance, issues, coordination]
guard: tests/test_governance.py::ComponentIssueLabelTests
normative: devguide/reporting_protocol.md
blocked_by: []
supersedes: []
---

# Standardize cross-component issue labels across MolSysSuite

**Reported:** 2026-09-22, after identifying that issues owned by one component often
exist to satisfy a requirement from another component.
**Status:** Active implementation. The namespace, on-demand synchronizer, offline tests
and first real label are implemented; hosted verification remains pending.

## What

Introduce a common `component:<member>` issue-label namespace. The label records an
explicit relationship between the issue and another registered MolSysSuite member. An
issue may name multiple related components.

In a component repository, the label normally identifies another member that consumes,
requests, blocks or is affected by the work. In the central repository, it identifies
members affected by a suite-level issue. The issue body remains responsible for explaining
and linking the concrete relationship.

## How

Derive allowed names from the member repositories in `suite.toml`. Give every relationship
label a common color and a generated description such as `Cross-component relationship
with uibcdf/dockingmt`. Provide one central, idempotent synchronization and audit tool so
repositories do not maintain independent label vocabularies.

Document when maintainers add, update and remove these labels in the reporting protocol.
The first implementation must exercise the convention on a real cross-component issue.

## Why

Cross-component obligations are currently embedded in prose and are hard to find during
triage. Consistent labels make them searchable and expose consumers and blockers without
moving ownership away from the repository where the work belongs.

The prefix is necessary. MolSysMT already has an unprefixed `argdigest` label described as
an internal area, so bare component names would collide semantically with repository-local
taxonomies.

## What is measured and what is assumed

On 2026-09-22, the central label set contained workflow labels such as `proposal`,
`needs-triage`, `in-progress`, `blocked` and `partial`, but no component namespace.
MolSysMT had an unprefixed `argdigest` label with the description `Area: argdigest`.

It is assumed that all registered repositories keep GitHub Issues enabled. The
implementation must detect and report repositories where label synchronization is not
available instead of treating absence of evidence as success.

The first live audit on 2026-09-22 inspected the central repository and all 14 registered
members. None contained a pre-existing invalid `component:` label. The on-demand command
then created canonical `component:dockingmt` in MolSysMT and a native GitHub operation
applied it to `uibcdf/molsysmt#215`, whose body already links the consuming requirement
in `uibcdf/dockingmt#3`. A second audit reported the MolSysMT label current.

## Alternatives and refuted paths

- Bare labels such as `dockingmt`: rejected because they collide with local area labels
  and do not communicate cross-component semantics.
- Encode relation types in many label families such as `requested-by:` and `blocks:`:
  deferred because a relationship can have several meanings over its lifetime; the issue
  body and linked issue provide the authoritative detail.
- Record the relationship only in prose: rejected because it cannot be inventoried or
  searched consistently.

## Scope and exclusions

This proposal covers issue discoverability. It does not replace repository ownership,
issue links, dependency metadata, project boards or synchronized devguide reports.

## Acceptance criteria

- Normative naming and semantics use `component:<registered-member>`.
- Allowed component names derive from `suite.toml` rather than a second manual list.
- Labels have one synchronized color and generated description.
- A central idempotent command creates, updates and audits the labels.
- The reporting protocol explains when the labels are required and how their evidence is
  recorded in the issue body.
- A guard reports unknown, stale or ambiguous relationship labels.
- One real issue demonstrates the complete workflow.

## Local implementation issues

None yet. The central proposal owns the convention and tooling before component-specific
adoption work is opened.

## Dependencies and risks

Creating every label in every repository would improve selection in the GitHub UI but
expand the maintained surface quadratically as the suite grows. The accepted implementation
therefore creates labels on demand and audits the namespace centrally. Contributors must
run the ensure command before selecting a relationship that has not yet appeared locally.

## Provenance

GitHub label inventories for `uibcdf/molsyssuite` and `uibcdf/molsysmt`, inspected on
2026-09-22, plus the DockingMT-to-MolSysMT SDF-support example supplied by the maintainer.
