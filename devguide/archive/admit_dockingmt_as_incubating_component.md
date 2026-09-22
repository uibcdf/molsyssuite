---
summary: Admit DockingMT as an incubating MolSysSuite scientific component.
issue: uibcdf/molsyssuite#36
status: resolved
opened: 2026-09-21
closed: 2026-09-22
verification: measured
area: [governance, membership, integration]
guard: tests/test_governance.py::GovernanceTests::test_dockingmt_is_registered_as_incubating_scientific_component
normative:
blocked_by: []
supersedes: []
---

# Admit DockingMT as an incubating MolSysSuite member

**Reported:** 2026-09-21 by the DockingMT owner after freezing its initial scientific
and architectural seed.
**Status:** Resolved; the central classification and repository baseline are complete,
and `uibcdf/dockingmt#1` is closed with local and hosted evidence.

## What

Register `uibcdf/dockingmt` as a primary, active, incubating scientific component with
the `python-package` capability and optional Zenodo archival. DockingMT owns the suite's
molecular-docking layer. Incubating membership does not establish a stable API, a public
release, Python 3.14 support or a stabilization-priority assignment.

## How

Add the member to `suite.toml`; register it as a consumer of the canonical MolSysSuite,
SMonitor, DepDigest, ArgDigest, PyUnitWizard and GH Run Receptor guides; and add an
optional, unknown Zenodo inventory entry. Complete the current common repository
baseline under `uibcdf/dockingmt#1` without changing the frozen scientific seed, then
verify the checkout with its local gates and the central conformance checker.

## Why

DockingMT is intended to connect MolSysMT's molecular systems with the developing
topographic, pharmacophoric and flexibility layers through reproducible docking
workflows. Central registration makes its ownership and maturity explicit and prevents
it from inventing divergent development conventions while that scientific API evolves.

## What is measured and what is assumed

**Inspected 2026-09-21:** the repository declares Python `>=3.11,<3.14`, development in
3.13, Ruff 0.16.5, exact `X.Y.Z` versioningit tag parsing, pytest, and runtime dependencies
on SMonitor, DepDigest, ArgDigest, PyUnitWizard and MolSysMT. It contains the canonical
MolSysSuite guide and a frozen v0.1 design seed. It initially had no `.github` workflows,
canonical badges, external integration guides, or shared reporting queues; therefore the
opening issue's claim that the full governance bootstrap was already present was not yet
accurate.

**Unverified:** no Python 3.14 admission, public release, Zenodo deposit, stable public
API, docking-engine correctness or scientific validation is inferred from registration.

## Alternatives and refuted paths

- Block admission until the scientific MVP exists: rejected because incubating maturity
  exists precisely to govern a component while its contracts evolve.
- Register only the member row and retain the incomplete bootstrap claim: rejected
  because universal governance is independent of maturity and the missing surfaces are
  small, concrete work.
- Add DockingMT to the stabilization priority list: rejected because that initiative is
  intentionally focused on the existing six components.

## Scope and exclusions

This issue owns central admission and the common repository baseline. Docking engines,
the C0--C6 implementation gates and scientific validation remain local to DockingMT.
Admission does not authorize Python 3.14 or mandatory archival.

## Acceptance criteria

- The classification and consumed-guide relationships are guarded centrally.
- The DockingMT checkout passes its tests, Ruff checks and central conformance check.
- Hosted CI and the pinned policy gate execute against the admission commits.
- The Zenodo inventory and generated report indexes include the new member.
- The report is archived and both central and local issues close with durable evidence.

## Local implementation issues

`uibcdf/dockingmt#1` owns completion of the repository governance baseline.

## Dependencies and risks

The scientific seed predates central registration and must not be overwritten by the
starter template. Files are adopted selectively and adapted to the existing flat package
layout. Incubating status must not be read as exemption from suite governance.

## Resolution

DockingMT is registered as a primary, active, incubating scientific component with
optional archival and no implication of Python 3.14, stable API or stabilization
priority. Six real guide relationships are registered and synchronized. Its reviewed GH
Run Receptor configuration maps both hosted workflows to the CI profile by exact path.
The local baseline is archived under `uibcdf/dockingmt#1`; exact sibling-source pins keep
one hosted Conda topology working on Python 3.11--3.13 while the reusable dependency
design remains owned by `uibcdf/molsyssuite#31`.

Policy release `policy-v1.4.2` is the first immutable snapshot containing DockingMT's
registry entry. At final DockingMT baseline commit `1b8337f`, hosted policy run
`35695696499` passed its single job and CI run `35695696153` passed all four jobs, including
Python 3.11, 3.12 and 3.13. GH Run Receptor read both default-branch rules and reported
`PASS` with the CI profile. Local Python 3.13.15 evidence included 35 passing tests, Ruff
lint/format, current report indexes, central conformance, valid receptor configuration
and six byte-identical guide checks. The classification and guide relationships remain
protected by the guard named in the front matter.

## Provenance

Central registry and local DockingMT commit `597ff0b` inspected on Linux with Python 3.13
on 2026-09-21. The initial central checker result was `UNREGISTERED`.
