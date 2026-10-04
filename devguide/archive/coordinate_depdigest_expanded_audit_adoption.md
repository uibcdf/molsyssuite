---
summary: Coordinate expanded DepDigest source audits, canonical guide delivery and owner import-boundary reviews.
issue: uibcdf/molsyssuite#95
status: resolved
opened: 2026-10-04
closed: 2026-10-04
verification: measured
area: [governance, compatibility, tooling]
guard:
normative: devguide/cross_component_feedback.md
blocked_by: []
supersedes: []
---

# Coordinate expanded DepDigest source-audit adoption

**Reported:** 2026-10-04, provider notice from uibcdf/depdigest#27 and #29.
**Status:** Resolved; public scanner reviewed, ten guide copies and owner
notices delivered, and both measured import-boundary decisions reconciled.
Broader runtime and public-artifact adoption remain owner-local.

## What

DepDigest 0.13.0 expands its static audit to imports in module/class control flow.
The same consumer source can therefore gain findings and return exit 1. This
changes the observable audit result, while preserving JSON keys, source lines,
runtime guard APIs, explicit exemptions and visible `--allow-violations`.
The shared-provider notice rule in `devguide/cross_component_feedback.md` owns
coordination; DepDigest owns implementation, release and its canonical guide.

## How

Use the ten `DEPDIGEST_GUIDE.md` consumers registered in `suite.toml`.
Synchronize only through `sync_vendored_guides.py`; publish from isolated clones
without touching the original worktrees. Give actionable version/source and
migration notices through existing owner issues. Guide receipt, runtime version
adoption, static audit result and root-import behavior are separate evidence.
No common new audit gate, dependency floor or scientific execution is introduced.

## Why

Formerly clean audits can fail when a previously missed adapter import becomes
visible. Treating every static finding as a package-startup leak, suppressing a
whole adapter directory or assuming guide delivery updates installed tooling
would misstate compatibility and hide the actual decision from its owner.

## What is measured and what is assumed

Public version: `0.13.0`, immutable source
`df771e00e886fd9b12915adf54c1bd75c4b5476c`, file
`noarch/depdigest-0.13.0-py_0.tar.bz2`, SHA-256
`e011d725c8a831ae46cd6b8d114185d04248e32b4d6701c70f988d19cc69f67b`.
The central review downloaded that public file and verified its digest; its
scanner bytes equal the immutable release source. Provider delivery, twelve-cell
source/installed matrices, public receiving installation and archival evidence
are owned by uibcdf/depdigest#29. This review does not reexecute those gates or
independently certify every provider release surface.

The owning CLI was run on Linux/Python 3.14.7 from the unpacked exact public
artifact, against pinned consumer source snapshots. This is a static audit,
not a normal installed-package certification or an import of consumer runtime.
The command is `python -m depdigest audit --src-root PINNED_CONSUMER/PACKAGE
--soft-deps OWNER_OPTIONAL_ROOTS --json`, with `PYTHONPATH` selecting the
unpacked artifact or immutable prior scanner. The receipt records each root list.
Optional roots came from each consumer's literal `LIBRARIES` declaration;
mandatory Pint/NumPy were excluded. The previous scanner at
`34d2c78aa7554ecb3209cc1d45f8990c28e1a572` supplied the comparison.

| Consumer snapshot | Previous raw findings | Public 0.13.0 raw findings | Owner |
| --- | --- | --- | --- |
| ArgDigest `a31be2823a7575a774f02e4b8490f6af884c38b5` | 0, exit 0 | 1, exit 1; `contrib/pyunitwizard_support.py:13` | uibcdf/argdigest#22 |
| PyUnitWizard `d70bdffe7cfdd7685c4830330c5f75d6465878da` | 1, exit 1 | 11, exit 1; scaffold plus five backend modules | uibcdf/pyunitwizard#93 |

PyUnitWizard's existing template-only exemption leaves ten findings and exit 1;
it does not cover the runtime adapters. The CLI matches the supplied file path,
so the absolute source-root invocation supplies the corresponding absolute
template path. A first relative-path probe retained eleven findings; correcting
the invocation reproduced ten without changing scanner or consumer code.
No new exemption was accepted. The provider's earlier separate root-import
probes observed no optional-root leakage; static findings alone neither reproduce
nor refute a startup leak. Those root probes were not rerun here.

Primary central review: `devguide/rollouts/depdigest_audit_95.json`.
It records source identities, exact findings, current source deltas, candidate
guide consumers, and the bounded search for audit calls in `.github`/`devtools`.
Absence in that search is not proof that a consumer never uses the audit.
Only the pinned snapshots have the measured finding counts; current consumer
runtime compatibility and startup performance are not inferred.

## Alternatives and refuted paths

- Broad directory exemptions or a global permissive gate are not adopted.
  Intentional boundaries need narrow documented owner decisions and relevant
  import regressions; keep raw and exempted audit results visible separately.
- A finding is not itself scientific or package-startup failure evidence.
- Consumer decisions do not block an independently qualified provider release.
- Public 0.12.0 remains an explicit older-auditor fallback when an owner needs
  a tracked review; this does not mean 0.13.0 is unreleased or unqualified.

## Scope and exclusions

All ten registered guide consumers receive the canonical integration text and
notice. Direct measured import-boundary effects are ArgDigest and PyUnitWizard;
the other eight are candidates, not newly qualified audit/runtime consumers.
No consumer implementation, dependency constraint, audit job, exemption or
scientific test selection is changed. MolSysMT/MolSysViewer scientific deferrals
remain; no new producer tool, build, upload, promotion or withdrawal is performed.

## Acceptance criteria

- Verify immutable provider source/public identity and retain bounded review facts.
- Publish all ten canonical guide copies and recheck them against remote heads.
- Deliver actionable notices with migration/fallback and explicit owner limits.
- Reconcile the measured import-boundary outcomes in uibcdf/argdigest#22 and
  uibcdf/pyunitwizard#93 after their owners review them; keep missing decisions
  open without inventing runtime adoption or startup certification.
- Record runtime/caller adoption only where measured. Normative shared-provider
  notice and guide-adoption policies guard the eventual coordination closure.

## Local implementation issues

uibcdf/depdigest#27 owns the resolved scanner correction; uibcdf/depdigest#29
owns the resolved public release. uibcdf/argdigest#22 and uibcdf/pyunitwizard#93
own the now-resolved import boundaries recorded below. Candidate notices use the registered
ecosystem review issues; documentation-only guide delivery requires no invented
local implementation issue.

## Dependencies and risks

Provider release is complete, not a blocker. The remaining owner decisions do
not block delivery of the guide or independent provider publication. A later
consumer source change needs its own review; old measurements are not reused
as evidence for altered import boundaries.

## Provenance

2026-10-04, Linux, Python 3.14.7. Public file and immutable source identities are
above; current registered guide revisions, pinned consumer inputs and command
results are retained in the central receipt. Runtime SMonitor for the static
reader is supplied by the already qualified public Python 3.14 environment;
unpacked artifact execution is explicitly distinguished from normal installation.


## Delivered coordination checkpoint

All ten canonical guide copies are published from the committed provider source
`ba67009` through the official synchronizer. Each consumer commit changes only
`DEPDIGEST_GUIDE.md`; notices are in its existing owner issue and linked in the
receipt. No local runtime adoption or boundary decision is inherited. The two measured owner outcomes were pending at the initial delivery checkpoint.
The reconciliation below settles both, including the PyUnitWizard runtime
adapters in its explicitly expanded owner review.


## Resolution — owner outcomes reconciled, 2026-10-04

uibcdf/argdigest#22 resolves the adapter through execution-time guarded loading,
without a scanner exemption. Current `42b2f93346fdcd1573ade66a3f82a1717a496184`
retains the qualified adapter/import guard from merged PR #23 at
`91543cfc638ef81d6daf1028296c4561af3554cb`. The already independently reviewed
PR/main/scheduled runs remain in `devguide/rollouts/argdigest_ci_review_39_20261004.json`;
this checkpoint does not rerun them.

uibcdf/pyunitwizard#93 expands its original template review to all five requested
runtime adapters. The owner preserves first-demand dispatch, documents six
individually justified exact-file exceptions and guards root/public-export
imports plus each backend's isolation. No directory exemption or
`--allow-violations` route is accepted. The maintained decision is in
`docs/content/developer/implementation-patterns.md` at
`9abae2a48cd50084eb8a8ccb9c589d25f8c696d5`; its import guards and guidance
remain identical at current `ef85201d619d2e50d4fd200a9196035d177f5a79`.

The central read-only/static review independently executes the same public
DepDigest 0.13.0 archive against both pinned current source trees. ArgDigest:
zero raw findings, exit 0. PyUnitWizard: eleven raw findings, exit 1;
template-only ten, exit 1; six exact-file exceptions zero, exit 0. Raw findings
remain visible separately from accepted scope. No consumer runtime is imported.
Source findings alone do not certify startup isolation or scientific behavior.

Published GH Run Receptor 1.2.0 and native jobs/logs corroborate PyUnitWizard
full matrix 37223629790 at `71de829a53ab50964f180ac558ea0307510ee0cb`:
eight executed Linux/macOS Python 3.11–3.14 cells, 676 passed and 22 documented
skips each. Final 9abae2a CI 37224861491 executes the same counts on Linux
3.14. Two schedule-only matrix jobs are skipped; no new debt clearance is
inferred. Those are existing owner executions, not suites dispatched here.

Primary reconciliation:
`devguide/rollouts/depdigest_owner_reconciliation_95_20261004.json`.
The initial ten guide deliveries/notices stay in the earlier receipt; the
current two affected copies retain the accepted canonical hash. Central
coordination is complete under the normative shared-provider notice policy.
Runtime/tool version adoption, component releases and scientific qualification
retain their owners; this closure creates no new common gate or exception.
