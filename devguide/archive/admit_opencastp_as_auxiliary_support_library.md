---
summary: Admit OpenCASTp as an auxiliary incubating support library
issue: uibcdf/molsyssuite#70
status: resolved
opened: 2026-10-02
closed: 2026-10-02
verification: measured
area: [governance, membership, scientific-computing]
guard: tests/test_opencastp_admission.py
normative: devguide/member_classification.md
blocked_by: []
supersedes: []
---

# Admit OpenCASTp as an auxiliary support library

## What

The maintainer created uibcdf/opencastp and explicitly requested auxiliary
MolSysSuite membership. Classify it as support-library, auxiliary, incubating,
active, python-package, with optional Zenodo archival. Keep the existing
Python 3.11--3.13 baseline initially. The maintainer subsequently requested
3.14; its component-specific transition authorization is uibcdf/opencastp#5.
Do not add the member to the stabilization initiative.

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

## Python 3.14 steering — 2026-10-02

The maintainer explicitly requires support through 3.14. Authorize the
component-specific target >=3.11,<3.15 and four CI minors; routine development
remains 3.13. Admission/public badge promotion follows actual installed and
scientific lane evidence under uibcdf/opencastp#5. The shared development
profile derives eligibility from this same authorization; its admin guard
now includes OpenCASTp and does not alter existing component states.

## Resolution — 2026-10-02

The official starter, canonical guidance, package/result boundaries, report
lifecycle and real numerical extraction are published. Current-source central
conformance passes; the administrative suite passed 275 tests. Scientific and
installed CI at OpenCASTp 762db29693f030ac61baa423de0371993ad6a454 passed all
four requested minors, including actual Python 3.14.7, with 26 tests each.
Native executed steps and GH Run Receptor preserve the distinction between
configured and completed gates. The member-specific 3.14 transition is admitted.

The admission guard initially failed for missing membership, then for missing
3.14 authorization; its assertions protect classification, non-priority status,
review ownership and the wider component contract. Broader science, source
rights, distribution, coverage and the published frozen-registry defect remain
separate issues (#1/#2/#3 in OpenCASTp and central #73). The bounded policy
exception remains explicit and dated; admission is not published policy adoption.
TopoMT remains unchanged; original central human work was preserved through an
isolated current-source checkout.

## Additional independent governance audit — 2026-10-02

This admission and its original archived resolution are preserved from central
commit `2707ef9`. The complementary audit uibcdf/molsyssuite#72 independently
checked the exact published `762db29693f030ac61baa423de0371993ad6a454` source:
component conformance, reporting/index validation and the focused reporting
regression, Ruff (40 files), and four byte-identical registered guides pass.
Native run 37058867837 confirms the bounded bootstrap executes the deadline,
exact checker identity, conformance, lint and formatting successfully; the old
published-policy job is explicitly skipped. That success does not imply adopted
published policy. Permanent repair stays under #73, with the accepted exception
owned by uibcdf/opencastp#3 through 2026-12-31.

The receipt in devguide/rollouts/opencastp_admission.json retains initial,
intermediate and final source evidence without overwriting active component
work. The dated audit table and issue handoffs are archived separately under
#72. The optional TopoMT adapter transition is uibcdf/topomt#90; coexistence
still authorizes no deletion. No scientific suite was rerun by this audit.

### Badge and bootstrap pin promotion — 2026-10-02

The team then published `6303af50318286476fac949015f9800e90c917ca`, promoting
the admitted Python badge to four minors and updating the immutable bootstrap
checker pin to `2707ef9389e0579ece75138b0b5c5e1fdb2a1a34`. An independent read-only
source check now confirms agreement with the admitted registry state: conformance,
reporting/index and focused reporting regression, Ruff (42 files), four guide
comparisons and the runtime manifest graph pass. Native policy run 37061097124
passes the bounded source route. This does not claim published-policy adoption
or rerun the scientific qualification supplied by the component team.
