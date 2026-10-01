---
summary: Limit MolSysSuite macOS support to Apple Silicon and remove Intel from future gates.
issue: uibcdf/molsyssuite#59
status: resolved
opened: 2026-09-27
closed: 2026-10-01
verification: inspected
area: [compatibility, packaging, governance]
guard: tests/test_python_ci_policy.py
normative: devguide/python_ci_policy.md
blocked_by: []
supersedes: []
---

# Limit macOS support to Apple Silicon

**Reported:** 2026-09-27, by an explicit maintainer support-scope decision.
**Status:** Source/policy rollout delivered to all 15 registered members.
Member runtime and complete platform-claim review remain with their existing
local CI issues; no new scientific qualification is claimed.

2026-10-01 source review: all 15 registered members are inventoried with immutable
sources and local review ownership in `devguide/rollouts/macos_arm64.md`.
No enabled prospective Intel publication target or runner remains in inspected
active workflows. Standard `macos-latest` is currently arm64, as documented by
GitHub; it is not itself evidence of executed compatibility tests. The registry
now declares `macos-architectures = ["arm64"]`, and the offline CI-policy guard
rejects adding Intel. Current support pages in ArgDigest, PyUnitWizard and
GH Run Receptor are now qualified explicitly. The component-facing guide and
starter guidance state the boundary without manufacturing member support claims.
All 257 central administrative tests passed; ArgDigest's 16 documentation and
report checks passed. No full scientific matrix was run in this review.

## What

macOS support is currently limited to Apple Silicon (arm64). Intel-based macOS
(x86_64) is not part of the supported platform matrix. Support may be
reconsidered if there is demonstrated user demand.

This is a forward-looking support contract, not an assertion that historical
`osx-64` artifacts are absent or broken. A component without an evidenced
macOS arm64 capability must not use the common wording to imply that it has one.

## How

Inventory all registered components' user-facing support statements, native
build inputs, routine and release CI, Conda staging/promotion gates, and any
expectations in compact run summaries. Remove `osx-64` from prospective
matrices and retain dated Intel evidence as history. For a four-platform
MolSysMT/MolSysViewer Conda pair on Python 3.11–3.14, the new complete gate
has 16 runtime cells plus its preparation job. Revalidate the exact release
candidate before a future publication; do not transplant the old 20-cell
certificate to a changed candidate.

## Why

The expected initial user population is small, and maintaining a separate
Intel macOS native build and Qt/PySide route imposes disproportionate release
cost. A user request can reopen the decision. This does not remove existing
downloads or authorize deletion of fork repositories.

## What is measured and what is assumed

Inspected on 2026-09-27: MolSysMT's pre-change Conda and Rust wheel workflows
included `osx-64`/`macos-15-intel`; Viewer already disabled `osx-64` in its
noarch publishing action but still documented the Intel platform as undecided.
The published 0.22.4/0.23.4 pair passed a historical five-platform 20/20
matrix. No new four-platform hosted gate is claimed by this policy edit.

## Alternatives and refuted paths

Keeping Intel in every prospective release gate would preserve a costly
platform commitment without demonstrated demand. Deleting historical artifacts
or the UIBCDF Qt/PySide repositories is unnecessary and out of scope.

## Scope and exclusions

MolSysSuite owns its registered members and shared member CI policy. MOLI owns
the corresponding boundary for its direct components in `uibcdf/moli#31`.
This issue does not certify optional Qt-host runtime on macOS arm64, and it
does not alter Windows policy or Python-version bounds.

## Acceptance criteria

- Each applicable member displays the support boundary accurately, without
  suggesting unverified arm64 capability.
- Prospective Intel jobs and publication targets are removed; tests guard the
  declared native platform set and new installed-pair count where applicable.
- Historical 20/20 evidence stays dated, while current checkpoints and release
  instructions use the four-platform 16-cell contract.
- Local exceptions and remaining member actions are inventoried before closure.

## Local implementation issues

`uibcdf/molsysviewer#97` owns the Viewer platform/capability wording.
The initial MolSysMT and Viewer implementation is tracked by this central
issue; additional member-specific defects should get local issues if needed.

## Dependencies and risks

No blocker for adopting the policy. A component's supported macOS arm64 claim
still needs its own installed-package and runtime evidence.

## Resolution (2026-10-01)

The canonical boundary is published in every member guide. Immutable source
inspection and member documentation delivery are recorded in the rollout. The
CI-policy regression guard rejects an empty, non-list, Intel-only or mixed
architecture set. All 257 central administrative checks passed. Historical
Intel artifacts and the 20-cell release certificate retain their original scope.
Reconsideration requires a user need and an explicit suite decision. Local
installed/runtime reviews and Viewer Qt-host limits remain owned by their linked
issues; this policy retirement does not claim those capabilities.
