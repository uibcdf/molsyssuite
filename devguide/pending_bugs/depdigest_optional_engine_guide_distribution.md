---
summary: Restore byte-identical DepDigest optional-engine guide copies.
issue: uibcdf/molsyssuite#63
status: active
opened: 2026-09-30
closed:
severity: low
verification: reproduced
area: [governance, guides]
guard: tests/test_governance.py::VendoredGuideSynchronizationTests::test_modified_copy_is_reported_as_drift
normative:
blocked_by: []
supersedes: []
---

# DepDigest optional-engine guide distribution

**Reported:** 2026-09-30 during LinDelINT CI-route review.
**Status:** Active distribution under the user's direct-commit authorization.

## What

Central vendored-guide audit 36701423229 failed after DepDigest published
optional original-engine, executable-dependency and explicit installer-route
instructions in canonical standards/DEPDIGEST_GUIDE.md. Ten registered root
copies differ: ArgDigest, PyUnitWizard, MolSysMT, MolSysViewer, TopoMT,
PharmacophoreMT, ElastNetMT, LinDelINT, Ackredit and DockingMT.

## How

Use sync_vendored_guides.py with --guide DEPDIGEST_GUIDE.md and --write in
isolated current-main checkouts. The script verifies committed canonical
source at remote main and refuses uncommitted consumer guide edits. Publish
only the generated root copy per consumer through direct commits and pushes.
Run byte comparison and registered repository conformance before publishing;
then dispatch the shared hosted guide audit against current consumer mains.

## Why

Developers need consistent provider-owned guidance across the ecosystem.
Guide publication and runtime adoption remain separate, as
uibcdf/molsyssuite#62 and uibcdf/depdigest#22 require. This issue owns only the
independently verifiable distribution step; it does not close #62.

## What is measured and what is assumed

On 2026-09-30, suite_status.py fetched all registered remotes and found no
original checkout ahead. Original ArgDigest has an untracked environment
artifact and TopoMT has a modified version file; every original worktree is
preserved. Fifteen components were checked out at current main in a temporary
workspace. Source DepDigest 4de4c0aa3b96850af2f043e91000977f9d571b18 is committed;
check_vendored_guides.py reproduced exactly the ten reported drifts.

## Alternatives and refuted paths

Manual consumer edits violate provider ownership and byte-identity rules.
Changing runtime code or dependencies would confuse documented capability with
consumer adoption. Full product suites are not verification of copied Markdown;
the user permits internal direct commits without full suites and has deferred
scientific execution reviews in active MolSysMT/MolSysViewer development.

## Scope and exclusions

Only DEPDIGEST_GUIDE.md in the ten registered consumers and central reporting.
Preserve component implementation, existing tests, workflows, versions,
dependencies and human worktrees. Provider release, optional-engine scientific
parity and per-consumer runtime migration remain with #62/#22/component teams.

## Acceptance criteria

- All ten remote-main root copies match the exact committed canonical bytes.
- Only the intended generated guide is published in each component commit.
- The shared hosted vendored-guide audit succeeds after publication.
- The report is archived, the index regenerated and this issue closed with
  evidence; parent uibcdf/molsyssuite#62 remains open.

The existing VendoredGuideSynchronizationTests exercise drift detection,
byte-identical copying, complete preflight, stale canonical-source rejection
and preservation of human edits. They guard the mechanism; actual ten-repo
comparison and hosted audit establish this distribution's result.

## Local implementation issues

None: distribution is owned centrally in uibcdf/molsyssuite#63 and uses the
registered synchronizer without product changes.

## Dependencies and risks

The source must remain committed and equal remote main. Concurrent consumer
pushes are handled by fetch and fast-forward/rebase, never force pushing.
Internal documentation pushes may use the previously authorized skip-CI route;
skipped-commit debt then remains subject to each component's existing recovery
control. This work does not dispatch heavy component suites or certify scientific
CI health.

## Provenance

Linux host, Python 3.13.15. Source inspected at DepDigest 4de4c0a on 2026-09-30.
Initial failing hosted audit: https://github.com/uibcdf/molsyssuite/actions/runs/36701423229.

## Distribution verification before publication

All registered vendored-guide relationships passed after synchronizing the ten
copies from source 4de4c0a. Canonical SHA-256:
`dc68b389bee2cc398719f2a9482f7c19870e3254e3979c24e96850fbdc748786`.
Each consumer worktree contains exactly one tracked change, DEPDIGEST_GUIDE.md.
All ten passed Ruff lint/format, generated-index checks and central repository
conformance. The existing synchronizer regression class passed 11/11 tests.
Full scientific/product suites were deferred under the user's internal-push
exception for this generated-documentation-only distribution. Component pushes
use `[skip ci]`; existing recovery mechanisms retain debt until complete success.

Reporting checks also passed: ArgDigest 6 tests, PyUnitWizard 9, MolSysViewer
122, TopoMT 2, Ackredit 1 and DockingMT 1 via pytest-receptor llm. The standalone
unittest guards passed in PharmacophoreMT, ElastNetMT and LinDelINT. MolSysMT's
standalone developer-guide validator passed. Initial unittest discovery in
pytest-function modules collected zero tests; the correct pytest runner above
was then used, without modifying any tests or treating empty collection as success.

## Published consumer commits

All ten documentation-only direct pushes succeeded. Each commit changes only
the root generated guide. GitHub explicitly reported administrative PR/check
bypass on protected mains; no PR or force push was used.

| Repository | Commit |
| --- | --- |
| uibcdf/argdigest | `a0e678348` |
| uibcdf/pyunitwizard | `b879f5246` |
| uibcdf/molsysmt | `be9600eeb` |
| uibcdf/molsysviewer | `ef3dd4dcb` |
| uibcdf/topomt | `19ab4bf10` |
| uibcdf/pharmacophoremt | `d0215faed` |
| uibcdf/elastnetmt | `82905a88a` |
| uibcdf/lindelint | `4c30f5951` |
| uibcdf/ackredit | `37576047a` |
| uibcdf/dockingmt | `e4075ad57` |

The skipped documentation commits remain subject to existing recovery where
configured. No clean scientific-debt or full-CI claim is made for these heads;
components whose recovery is still unreviewed retain their separate CI rollout.
