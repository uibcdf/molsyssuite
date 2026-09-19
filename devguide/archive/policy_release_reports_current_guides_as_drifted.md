---
summary: A pinned policy release reports current guides as drifted.
issue: uibcdf/molsyssuite#22
status: resolved
opened: 2026-09-14
closed: 2026-09-19
severity: high
verification: reproduced
area: [ci, governance, guides]
guard: tests/test_governance.py::RepositoryConformanceTests::test_versioned_policy_can_delegate_guide_bytes_to_live_sync_guard
normative:
blocked_by: []
supersedes: []
---

# A pinned policy release reports current guides as drifted

**Reported:** 2026-09-14, during wave-1 Python/Ruff adoption.
**Status:** Active; the corrected policy release is being validated.

## What

The `policy-v1.1.5` reusable workflow fails with `GUIDE_DRIFT` for current,
byte-identical `MOLSYSSUITE_GUIDE.md` copies. This occurred in SMonitor run
`34890225749`, PyUnitWizard run `34890230285`, and MolSysViewer run
`34890248371`.

## How

The tagged workflow checks out the tagged suite repository, then invokes
`check_repository.py`. That checker compares the member's guide against the
older guide bundled in the immutable tag. The central guide acquired the
`suite_status.py` section after `policy-v1.1.5`; consumers received exact
copies of current `main`, so the tag incorrectly calls the newer guide drift.

The policy workflow should continue to require the guide and the `AGENTS.md`
pointer, but delegate byte comparison to the independent cross-repository
guide-sync guard, which checks current sources. The local checker retains byte
comparison by default. Publish this as immutable `policy-v1.1.6` and update
active callers.

## Why

This blocks the new wave-1 quality gates and would affect already adopted
components on their next policy run. Guide updates should not require a new
Python-quality policy release merely to avoid a false finding.

## What is measured and what is assumed

Measured: the three GitHub runs above fail at the conformance step with
`GUIDE_DRIFT`. `git diff policy-v1.1.5 -- MOLSYSSUITE_GUIDE.md` shows the
new cross-repository status section. The local `main` checker passes against
the current consumer copies. We assume no unrelated guide drift; the live
cross-repository guard remains responsible for testing that independently.

## Alternatives and refuted paths

- Revert the guide copies to the older tag: violates the single canonical
  source and would erase the published status-tool instructions.
- Track moving `main` inside the pinned policy checker: would make the quality
  gate's policy source mutable and weaken reproducibility.
- Publish a new policy tag for every guide edit: would perpetuate avoidable
  coupling between independent guide and Python-quality lifecycles.

## Scope and exclusions

This changes only the pinned Python conformance workflow's byte-drift check.
It does not weaken the live guide-sync guard or permit local guide edits.

## Acceptance criteria

- Unit tests prove that the versioned checker skips only guide content drift,
  while still requiring the guide and pointer.
- The local default checker still reports real content drift.
- A new immutable release checks out its own tag and the four new wave-1
  callers pass the remote policy workflow.

## Local implementation issues

The rollout issues are `uibcdf/smonitor#12`, `uibcdf/pyunitwizard#74`,
`uibcdf/molsysmt#211`, and `uibcdf/molsysviewer#87`.

## Dependencies and risks

The separate guide-sync workflow on current `main` must remain active and
truthful. Release tags are immutable; do not move `policy-v1.1.5`.

## Provenance

GitHub Actions runs on Ubuntu 24.04 / Python 3.13.15, 2026-09-14.
Local checker on Linux / Python 3.13.15, 2026-09-14.

## Resolution

Policy release 1.1.6 keeps presence and `AGENTS.md` pointer checks in the pinned
workflow but delegates byte equality to the live cross-repository guide-sync guard.
The local checker still compares bytes by default. All nine active policy callers
passed the 1.1.6 workflow on 2026-09-19, including the four newly migrated wave-1
components.
