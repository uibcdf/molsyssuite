---
summary: Migrate the six remaining Python components to 3.14
issue: uibcdf/molsyssuite#51
status: active
opened: 2026-09-26
closed:
verification: inspected
area: [python, compatibility, packaging, ci]
guard:
normative:
blocked_by: []
supersedes: []
---

# Migrate the six remaining Python components to 3.14

**Reported:** 2026-09-26, while constructing a Python 3.14 development environment
from the editable packages in the existing Python 3.13 environment.
**Status:** Active; source metadata has been inventoried, but compatibility and release
evidence remain component-owned.

## What

Complete the Python 3.14 transition for the registered Python packages that still
exclude that interpreter in their source metadata. This is the remaining-cohort
tracker under the phased suite rollout in `uibcdf/molsyssuite#29`, not a claim that
editing a version bound alone establishes support.

| Component | Source declaration inspected on 2026-09-26 |
| --- | --- |
| Ackredit | `pyproject.toml:10`: `>=3.11,<3.14` |
| DockingMT | `pyproject.toml:22`: `>=3.11,<3.14` |
| ElastNetMT | `pyproject.toml:21`: `>=3.11.0,<3.14.0` |
| LindeLint | `pyproject.toml:21`: `>=3.11.0,<3.14.0` |
| PharmacophoreMT | `pyproject.toml:21`: `>=3.11,<3.14` |
| TopoMT | `pyproject.toml:21`: `>=3.11,<3.14` |

## How

Each component owner should verify the Python 3.14 dependency chain, run the relevant
local and hosted tests, align package metadata, Conda recipes, CI, documentation and
release gates, and test a clean installed package. Native or upstream blockers need
explicit component issues and a bounded suite exception. Admit packages in dependency
order; do not use `--ignore-requires-python` to make the development environment appear
complete.

## Why

The new `molsyssuite@uibcdf_3.14` environment can legitimately install the already
compatible core pair and tooling in editable mode, but cannot reproduce all editable
members of the older 3.13 environment until these six move. A central remaining-cohort
tracker prevents the first successful pair from being mistaken for suite-wide coverage.

## What is measured and what is assumed

**Inspected:** The six `requires-python` fields above were read from fetched
`origin/main` refs after the suite status check. Several local checkouts lag those
refs, and PharmacophoreMT's local checkout still declares the older lower bound
`>=3.10.0`. The suite registry lists all six with `python-package` capability.
The other eight registered Python packages declare a range including 3.14.

**Not yet measured here:** Importability, full test results, Conda solves, native
extension availability, and public installed-package behavior for the six. Those
results belong to each component's implementation record.

## Alternatives and refuted paths

Forcing the six editable installs with `--ignore-requires-python` would bypass their
published contract and conceal compatibility failures. It is unsuitable as evidence.
No other migration strategy has been evaluated yet.

## Scope and exclusions

This central issue coordinates Ackredit, DockingMT, ElastNetMT, LindeLint,
PharmacophoreMT and TopoMT. Component-specific code, tests and release decisions remain
in their respective repositories. The already-admitted first cohort and the
MolSysMT--MolSysViewer pair are tracked by `uibcdf/molsyssuite#29` and their own issues.

## Acceptance criteria

- Each listed component has its own Python 3.14 compatibility evidence and an aligned
  declared package contract, or a documented, time-bounded exception linked from suite
  policy.
- Clean installed-package evidence and release provenance are recorded before a
  component is marked admitted.
- The suite registry and this tracker identify no unaccounted registered Python package
  still excluding 3.14.
- Closure names the normative suite policy or an automated registry/metadata audit
  that prevents a silent regression.

## Local implementation issues

Ackredit adoption is owned by uibcdf/ackredit#80, also needed by Sabueso's
required dependency closure under uibcdf/sabueso#108. The other component
owners retain their own implementation and scientific qualification work.

## Universal requirement decision — 2026-10-02

The maintainer explicitly requires Python 3.14 support from every registered
Python component now. The common required range is `>=3.11,<3.15`, with four
required full CI minors; development remains Python 3.13. Initial-cohort
membership no longer controls applicability. The common guide conveys this
to all members. Adoption remains measured separately from the requirement,
and pending migration cannot create a delivered-support badge or public
artifact claim.

Ackredit's root instructions still explicitly denied authorization and its
metadata capped Python below 3.14 at source `6420407`. Its successful earlier
two-platform feasibility run `36693052801` is source evidence, not ordinary
installed/public delivery: the old workflow used `--ignore-requires-python`.
The suite authorizes its migration under #80, requiring normal installation,
required 3.14 CI, coherent environments/recipe/instructions, and delivery
evidence before admission. The common gate and starter require four minors;
the regression
`tests/test_governance.py::GovernanceTests::test_every_python_member_requires_314_without_inheriting_admission`
checks universal applicability without promoting an unqualified badge.

## Qualified Ackredit source and guide delivery — 2026-10-02

Immutable `policy-v1.5.3` at central `4010595` publishes the universal
requirement and includes the admitted OpenCASTp registry entry. All 16 member
copies of the canonical guide are synchronized and pushed through the central
tool. Active original checkouts remain preserved; MolSysMT/MolSysViewer receive
only the guide, with scientific suites still deferred.

Ackredit source `e4a006a6931f3fb5f97be5b09767c144dfb35662` passes ordinary
routine CI `37073478950`, shared policy `37073479396`, and full Linux/macOS
arm64 Python 3.11–3.14 matrix `37074118479`. Native evidence confirms all eight
normal install, off-checkout import, interpreter/architecture and full test
steps executed successfully. Local isolated Python 3.13 regression passes
1,530 tests. Its seventh strict required PR check is Linux 3.14, with the
existing internal bypass preserved. Recovery probe `37075039313` recognizes
the four-minor source watermark with zero pending skips and omits heavy jobs.

Ackredit remains `authorized`: public portable-API delivery and independent
consumer installation are still pending under #80/#22/#75. DockingMT,
ElastNetMT, LinDelINT, PharmacophoreMT and TopoMT still have source declarations
excluding 3.14; their mandatory adoption remains open in this tracker and is
not certified by the new guide. Full machine receipts and source observations
are in `devguide/rollouts/python314_required_adoption.json`.
Platform coordination is raised in uibcdf/moli#37.

After documentary push `16b9598 [skip ci]`, native GitHub confirms the
administrator route bypasses the seven required checks. Brief probe
`37075787493` detects exactly one pending skipped commit since `e4a006a`;
probe mode intentionally omits heavy jobs and leaves nightly recovery due.
This is evidence of debt retention, not a successful recovery-suite claim.

## Dependencies and risks

No strict issue blocker is established yet. Native packages and optional scientific
dependencies may have different release paths; an editable source import alone does not
prove a distributable 3.14 package.

## Provenance

Source inspection on 2026-09-26 from fetched `origin/main` refs in
`/home/diego/repos@uibcdf`, host `nauta`;
the new development environment uses CPython 3.14.7. No runtime measurement for the six
is claimed by this report.
