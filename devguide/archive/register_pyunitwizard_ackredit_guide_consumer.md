---
summary: Register PyUnitWizard as an Ackredit guide consumer and synchronize portable attribution guidance.
issue: uibcdf/molsyssuite#71
status: resolved
opened: 2026-10-02
closed: 2026-10-04
verification: inspected
area: [guides, integration]
guard: tests/test_governance.py::GovernanceTests::test_ackredit_is_registered_as_incubating_support_library
normative:
blocked_by: []
supersedes: []
---

# PyUnitWizard consumes the Ackredit integration guide

**Reported:** 2026-10-02, maintainer-authorized optional attribution pilot.
**Status:** Canonical source published and six local guide copies synchronized; central registry publication pending.

## What

Add PyUnitWizard as an Ackredit integration-guide consumer. The maintainer
explicitly requested delivery of the reviewed canonical guide to the client
libraries in MOLI/MolSysSuite after the provider API and guide are ready.

## How

The local `ACKREDIT_GUIDE.md` consumer list now includes `uibcdf/pyunitwizard`,
beside MolSysMT, MolSysViewer, TopoMT, PharmacophoreMT and ElastNetMT.
Use the registered central synchronizer after the canonical provider source is
committed and published at `origin/main`; preserve unrelated working-tree edits.
Never repair consumer copies locally or bypass its source/destination preflight.

## Why

PyUnitWizard is the smaller real consumer of the portable attribution provider
under uibcdf/ackredit#75. Its explicit optional Pint/unyt attribution pilot under
uibcdf/pyunitwizard#92 now needs the provider integration guidance. This extends
the distribution registry without changing the policy adopted in #68.

## What is measured and what is assumed

Inspection of the registry found five consumers, excluding PyUnitWizard. The
central synchronizer verifies committed canonical source and remote-main identity
before writing. These requirements establish source fidelity, not runtime
adoption or a published provider installation. Validation and final delivery
evidence will be appended when those steps finish.

## Alternatives and refuted paths

Manual consumer edits or direct helper calls that skip the synchronizer's
preflight are not accepted distribution. Host-owned result schemas and runtime
adapters remain separate implementation choices.

## Scope and exclusions

Registry and byte-identical guide distribution only. No runtime implementation
changes in MolSysMT, new dependency extra, release, or Python support decision.
The pre-existing local MolSysViewer ecosystem-evidence edit is preserved and
excluded from this proposal.

## Acceptance criteria

- PyUnitWizard is registered as a consumer and central governance passes.
- Canonical Ackredit source is committed and published before distribution.
- All six registered consumer copies are byte-identical to that source.
- Runtime adoption/publication remain separately tracked by member owners.

## Local implementation issues

- uibcdf/ackredit#75: provider API and canonical guide.
- uibcdf/pyunitwizard#92: optional executed-backend attribution pilot.
- uibcdf/molsysmt#292: member-owned provider adoption requested for uibcdf/molsysmt#27.

## Dependencies and risks

Distribution awaits the canonical source's committed/published revision under
uibcdf/ackredit#75. Changes are local, and no delivery claim is made before the
central source/destination checks pass.

## Provenance

2026-10-02; local MolSysSuite registry and synchronizer inspection.


Local `python devtools/scripts/validate_governance.py` passed after the registry
addition. The pre-existing MolSysViewer review/evidence hunk is unchanged and
excluded from the prepared guide-registration commit.


## Completed local delivery (2026-10-02)

Ackredit commits `4228444` and `4577c83` are published on `origin/main`.
`python -m devtools.scripts.sync_vendored_guides --guide ACKREDIT_GUIDE.md --write`
passed the canonical source and destination guards and synchronized all six
registered consumer copies. The subsequent read-only invocation reports all
six current; independent byte comparisons also pass. Guide distribution does
not establish runtime adoption or a released provider installation. The local
registry commits remain unpublished: this checkout is behind remote main and
contains separate maintainer work, so its main branch must not be pushed.
The record remains partial pending central registry publication.


## Registry review preparation

The registration is now prepared on remote main `2707ef9` in a clean separate
checkout. It contains only the PyUnitWizard consumer relationship, the exact
governance assertion and this issue-backed record/index. Original local main
commits and unrelated maintainer changes are excluded. Source and delivery
criteria are satisfied; this proposal remains partial until registry merge.

The remote-based proposal passes governance validation and all 129 tests in
`tests/test_governance.py` on Python 3.13.


## Owner acceptance and current delivery — 2026-10-03

The owning maintainers accepted the bounded registry addition from reviewed
commit `8f4e578` through the authorized direct-commit route. PR #74 remains
closed without merge. Historical local-delivery claims above refer to their
original source revisions; final current-source delivery and remote consumer
publication will be recorded separately. Ackredit 0.9.0 public bytes are now
verified under uibcdf/molsyssuite#88; guide fidelity still does not prove
consumer runtime adoption. The source-ready optional pilot remains owned by
uibcdf/pyunitwizard#92, with the other owner handoffs unchanged.


## Resolution — 2026-10-04

The central registry now adds PyUnitWizard using the reviewed one-row change;
`test_ackredit_is_registered_as_incubating_support_library` asserts the exact
six-consumer relationship and would fail if it were removed. Official guarded
synchronization and read-only follow-up pass for all six copies. Their clean,
fetched published main snapshots already contain the canonical bytes, so no
consumer source changes or additional guide pushes are required for #71.

Canonical source main is `a8219b86e85f9b9fc29e8bfee7982040ffe27215`; the latest guide-changing commit
is `840aab3d415312144e4f5754d5def11b3068832f`, with SHA-256 `24615e3a8894c7cba67fc92fd0323369e725c3bd88096df9eda9311ab8890ff5`.
`devguide/rollouts/ackredit_guide_consumers_71.json` retains each independent
consumer commit/hash comparison. Original active developer clones are preserved.
This closes registry and guide delivery, without asserting runtime adoption,
new mandatory dependencies or installed platform support. The historical PR
and local-delivery claims above retain their original scope.
