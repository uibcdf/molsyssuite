---
summary: Refresh suite and MolI auxiliary editable installations with one command.
issue: uibcdf/molsyssuite#135
status: active
opened: 2026-10-24
closed:
verification: measured
area: [development, tooling]
guard: tests/test_workspace_reinstallation.py
normative:
blocked_by: []
supersedes: []
---

# Batch reinstallation of local suite and MolI Python sources

**Reported:** 2026-10-24, maintainer request during native bootstrap review.
**Status:** Published and hosted regression verified; complete-workspace receiving remains pending.

## What and why

Provide one command that repeats the standard no-deps/no-build-isolation
editable installation across all installable suite members and the auxiliary
Python packages belonging directly to MolI. Refreshing installation also
refreshes distribution metadata and versioningit-generated version files after
local Git commits/tags, without requiring manual work in every directory.

## Implementation scope

Extend `development_environment.py` with `reinstall --workspace PATH`, reusing
its source inventory, native-toolchain verification and batch installer.
Read suite Python capabilities from `suite.toml` and MolI direct Python
components from `WORKSPACE/moli/moli.toml` or `--moli-registry PATH`.
Currently this selects fifteen suite Python members and Sabueso, Praxis and
Recorda. Repositories without Python-package capability are outside pip's scope.

The general reinstall explicitly includes TopoMT at the maintainer's request;
it does not alter the fourteen-member qualified integration profile, scientific
qualification, suite membership or package admission. Missing sources and
metadata excluding Python 3.14 fail before pip. `--dry-run` inspects sources;
repeatable `--exclude NAME` records deliberate omissions. Branches, local work,
tags and dependencies are preserved. Pip/build/closure failures propagate.

The workspace argument defaults to the parent of the MolSysSuite clone, so
`python devtools/scripts/development_environment.py reinstall` is sufficient
for sibling clones. `--workspace` remains available for another layout.

## Observations and limits

The initial local TopoMT clone was 374 commits behind its remote and declared
Python >=3.10,<3.13. During this task the maintainer explicitly updated that
clone. The refreshed source at `86e6004` declares Python >=3.11,<3.15 and the
complete eighteen-source inventory now passes. Existing TopoMT readiness
ownership remains uibcdf/topomt#16 and uibcdf/molsyssuite#51. The agent does
not update primary clones or infer scientific integration from this inventory.

Suite state inspection also observes behind clones for MolSysMT (three commits),
Pytest Receptor (one), GH Run Receptor (four), DockingMT (one) and MolSys-AI
(58). Direct MolI inspection observes Sabueso one commit behind, with Praxis,
Recorda and the MolI registry current and clean. Fetches update remote refs
only. These are local observations, not decisions to install new sources.

Versioningit updates the configured `_version.py` at build/install time.
Publishing a tag does not refresh an existing installation. The standalone
`versioningit --write` updates only the configured version file, not installed
distribution metadata. MolSysMT reads installed metadata first in `__init__`.
The tag must exist in the local clone; the command does not fetch. Running
Python sessions may retain cached imported values until restarted.

## Acceptance and verification

- Single registry-derived batch command and documented dry-run/exclusions.
- All selected sources validated before installation; errors remain failures.
- Existing pip flags and toolchain preflight reused.
- An isolated real Git/tag/versioningit editable reinstall proves both generated
  file and installed metadata remain unchanged by tagging, then refresh together.
- Existing qualified profile, primary clones, user environment and prior native
  evidence retain their scope.

## Verification — 2026-10-24

The final CLI's complete dry-run validates eighteen current local sources;
an explicit TopoMT exclusion yields seventeen and records that omission.
An isolated venv installs two real fixture packages together using the shared
batch installer. The versioningit fixture starts at tag 0.1.0; creating another
commit and tag 0.2.0 leaves the generated file and installed metadata at 0.1.0.
Repeating the batch install refreshes both to 0.2.0. No fixture tag or package
is created in a primary repository/environment.

The full central suite runs 544 cases: 543 pass and one existing opt-in native
Mamba case is skipped. The focused selection runs 32 pytest cases plus 46
subtests successfully. Ruff, generated indexes and offline governance pass.
The [bounded receipt](../rollouts/workspace_reinstallation_135_20261024.json)
records sources, scope, CLI/code identities and results. Native bootstrap
evidence remains independently owned by uibcdf/molsyssuite#134 and its dated
receipt; it is not relabeled as an eighteen-component installation.

Metadata inspection finds five current source-cohort conflicts: Praxis requires
ArgDigest <0.17, SMonitor <0.22 and PyUnitWizard <0.29; Recorda requires ArgDigest
<0.17 and SMonitor <0.22. Selected provider sources calculate versions 0.17.0,
0.22.0 and 0.29.0 with their recorded local suffixes. This predicts dependency
check failures, not functional/scientific incompatibility. The human was
informed; the separately reviewed compatibility changes are now tracked in
uibcdf/praxis#14 and uibcdf/recorda#34. No owner bounds are changed, no complete eighteen-source
installation or closure is claimed, and the user's environment is preserved.

Temporary previews/logs under this task's
`/tmp/molsyssuite-reinstall-20261024-HH8NSI` were removed after retaining results.
The fixture venv, packages and repositories were removed by managed test cleanup.
Changes remain local/unpublished; the issue remains active for delivery and
applicable hosted receiving.

## Praxis/Recorda audit before reinstall — 2026-10-24

At the maintainer's request, the five constraints were audited before running
the complete reinstall. Historical uibcdf/praxis#10 and uibcdf/recorda#24 are
closed for their original 2026-10-20 public cohort: ArgDigest 0.16.0,
SMonitor 0.21.0, DepDigest 0.15.1 and PyUnitWizard 0.28.1. Their bounded receiving
does not automatically admit the newer provider minors now in the workspace.

Two task-owned venvs inherited the current Python 3.14.9 Conda base. One used
the public ArgDigest 0.17.0/SMonitor 0.22.0/DepDigest 0.15.1/PyUnitWizard 0.29.0
files, with 189 managed Python files byte-verified using Recorda's reusable
path/provenance checker. The other used recorded primary provider source copies.
Both used unchanged consumer source copies, published pytest-receptor 1.2.1,
explicit SMonitor recovery and a recorded optional Ackredit source copy.

Recorda passes all 376 tests and Praxis passes 199 tests in each environment:
1,150 existing test executions without failures or skips. Praxis's optional
real-MolSysMT provider module is explicitly excluded, so these outcomes do not
qualify its scientific execution. Both unchanged-metadata environments reproduce
exactly the five pip-check conflicts above.

In separate disposable copies, widening only the five pyproject upper bounds
to admit the current minors gives clean `pip check` and six passing quantity,
recording and attribution integration tests. Runtime implementations remain
unchanged. This supports a metadata-receiving diagnosis for the tested cases;
the synthetic overlay is not a coherent recipe/CI change or qualified release.

Before the complete reinstall can yield clean closure, Praxis/Recorda owners
need to review this new receiving, align pyproject and Conda recipe constraints,
review their pinned build/test/development environments and exact-provider
identity checks, and execute their applicable gates. Owning issues for this
cohort are uibcdf/praxis#14 and uibcdf/recorda#34, preserving the completed
historical issues and public files.
No owner source, package, release, tag or primary environment is changed here.

The [audit receipt](../rollouts/praxis_recorda_support_audit_135_20261024.json)
records all versions, source identities, native/JUnit outcomes, original
conflicts, synthetic overlay and qualification limits. Task-owned audit resources
under `/tmp/molsyssuite-praxis-recorda-audit-20261024-eGKi2P` were removed after
retaining the receipt. Earlier native and reinstallation receipts retain their own scope.

### Provenance correction and owner handoff — 2026-10-24

Preparing the authorized owner issues exposed a provenance error in the first
source-provider lane: its editable distribution versions had development suffixes,
but the module paths still resolved to the inherited public Conda copies. That
original lane is withdrawn as source-runtime receiving; the public-provider
execution and its byte checks remain valid.

The same seven recorded source commits were checked out again in a separate
task-owned venv. Explicit source roots precede the inherited dependency path
through a `.pth` file, including in child processes. Actual module origins for
all seven packages were asserted both normally and with Python `-I`. The
repeated runs pass 376 Recorda and 199 Praxis tests, with the same explicit
real-MolSysMT exclusion and five reproduced metadata conflicts. The receipt
retains withdrawn XML identities separately and binds the replacement results
to their verified source origins. Thus the 1,150 valid executions now comprise
575 public-provider cases and 575 corrected source-provider cases.

Authorized owner reports are uibcdf/praxis#14 and uibcdf/recorda#34, cross-linked
to this central issue and each other. They preserve the previously completed
cohort decisions and request reviewed bounds, recipe/environment and provider
identity adoption. No owner code, primary checkout or named environment is
changed by filing these reports.
The replacement audit venv and source copies were removed after preserving
the corrected receipt and both owner handoffs.

## Published implementation and remaining receiving — 2026-10-24

The command, guidance, tests and corrected audit are published in
`a985c12865c39a233cdfb4c4ec176d6fcf9a20be`. The lightweight hosted test
environment correction in `283607369c45bd77dc19638511338b0959b01d67` passes
governance/coverage run
[40132369611](https://github.com/uibcdf/molsyssuite/actions/runs/40132369611),
including the actual Git/tag/versioningit editable refresh regression.
The [delivery receipt](../rollouts/development_delivery_134_135_20261024.json)
retains exact native steps and the separate fresh fourteen-member environment
result. Neither result is an eighteen-source installation claim.

At closeout inspection, uibcdf/recorda#34 is closed and reports source/editable
receiving at `28fe4912be30873cfc1bd6400c4a7f2c6783288c`, with closure evidence
at `6f5b064648e618e63cd7fdb4c0aeb54f1c81fecb`. Its owner reports reviewed
ArgDigest <0.18 / SMonitor <0.23 bounds and public/source/editable gates;
the original public 0.3.2 remains unchanged. This is an observed owner handoff,
not a centrally replayed consumer qualification. uibcdf/praxis#14 remains open.

Keep this central issue active for the remaining owner handoff and explicit
receiving of the intended current workspace. No primary clone is updated and
the complete reinstall is not executed during this publication/guide task.
The historical five-conflict audit remains bound to its original source
snapshots; it is not asserted against Recorda's subsequent fix.
