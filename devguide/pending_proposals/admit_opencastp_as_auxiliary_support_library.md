---
summary: Admit OpenCASTp as an auxiliary incubating support library
issue: uibcdf/molsyssuite#70
status: active
opened: 2026-10-02
closed:
verification: inspected
area: [governance, membership, scientific-computing]
guard:
normative:
blocked_by: []
supersedes: []
---

# Admit OpenCASTp as an auxiliary support library

## What

The maintainer created uibcdf/opencastp and explicitly requested auxiliary
MolSysSuite membership. Classify it as support-library, auxiliary, incubating,
active, python-package, with optional Zenodo archival. Keep the existing
Python 3.11--3.13 baseline and do not add it to the stabilization initiative.

## How

Register the member, canonical suite-guide consumer and pending ecosystem,
distribution and archival evidence. Generate its repository with the official
starter kit. OpenCASTp owns the extracted local numerical engine; TopoMT owns
molecular preparation and the Topography adapter during the bounded migration.
The temporary duplicate implementation is tracked in uibcdf/opencastp#1.

## Why

A standalone local engine can serve TopoMT and external Python consumers without
depending on Topography or DFND. Auxiliary membership remains fully governed.
MOLI delegates member admission to MolSysSuite; no separate direct MOLI member
or platform architecture change is requested.

## What is measured and what is assumed

Inspected the empty repository, current suite starter kit and TopoMT source.
Scientific agreement, package publication and GPU/Rust acceleration are separate
claims and are not implied by admission. uibcdf/opencastp#2 owns provenance and
distribution qualification. Existing unrelated MolSysViewer review edits in
the central suite.toml must be preserved and excluded from the admission commit.

## Acceptance criteria

- Explicit classification and review records pass the admission regression guard.
- The official generated repository passes local and central conformance gates.
- Record the exact checks before resolving and archiving this admission.

## Local implementation issues

- uibcdf/opencastp#1: extraction and independent validation.
- uibcdf/opencastp#2: provenance, ecosystem and distribution qualification.

## Provenance

2026-10-02, local Python 3.13 development environment. Registration is not
public release, complete scientific equivalence or an archival claim.

## Current-policy reconciliation — 2026-10-02

The initial local suite checkout was behind origin/main. Admission is now
integrated in an isolated checkout of 362d440; unrelated human work in the
original checkout remains untouched. Resolve the report index from its actual
records, retain upstream dependency graph/rollouts and register OpenCASTp's
real required runtime, test and CI-tool edges using immutable engine source.
The current starter kit also supplies scoped developer instructions and the
optional-engine review worksheet. CI/coverage qualification is owned by
uibcdf/opencastp#3; unobserved platform claims remain pending.
