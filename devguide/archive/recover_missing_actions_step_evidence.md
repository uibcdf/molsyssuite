---
summary: Recover executed-step evidence when successful Actions jobs expose empty step inventories.
issue: uibcdf/molsyssuite#118
status: resolved
opened: 2026-10-13
closed: 2026-10-14
severity: medium
verification: reproduced
area: [governance, ci, evidence]
guard: tests/test_installed_matrix_verifier.py
normative: devguide/python_ci_policy.md
blocked_by: []
supersedes: []
---

# Missing native executed-step evidence

**Reported:** 2026-10-13 during published-provider receiving and registered guide delivery.
**Status:** Resolved by recovering and independently verifying native required-step facts on 2026-10-14. Original diagnosis and unknown service cause are retained below.

## What

Successful exact-source Actions jobs return `steps: []`. The shared
`verify_native_gate` correctly refuses to certify their required executed steps.
Eleven member guide-delivery runs and SMonitor's promotion expose this gap.
This is an evidence limitation, not a demonstrated component test failure.

## How

Authenticated native reproduction:

```bash
gh api repos/uibcdf/argdigest/actions/runs/38474026582/attempts/1/jobs
gh api repos/uibcdf/smonitor/actions/runs/38466664766/attempts/5/jobs
gh api repos/uibcdf/smonitor/actions/jobs/115550097426
```

ArgDigest's successful `policy / conformance` job is bound to
`823146808b4af3203b8d3886c1d215b46b2c9f6f`. SMonitor's successful promoter
job is bound to `f6230af431a7fc185209fa44364c017d711cc2b7`, run attempt 5.
Both run-attempt and direct-job endpoints omit steps. All eleven selected
guide-delivery profiles expose the same empty arrays, including Viewer's
additional metadata job. Original source/installed acquisition earlier in the
task supplied verifiable required steps; that completed evidence is retained.

GH Run Receptor's actual full capture of ArgDigest reports the native run
conclusion `PASS`, one successful job and no artifacts. A generic conclusion
report does not establish required-step execution. Native metadata, available
same-attempt logs, promotion/public receipts and local execution keep separate
identities and limits in the receiving receipt.

## Why

Inferring executed gates from a green conclusion would weaken publication and
admission evidence. Missing server data must remain visible. Administrative
guide deliveries can use their already accepted manual route; that route does
not clear scientific/full-suite debt or certify a new installed release.

## What is measured and what is assumed

The named Python 3.14.7 environment and authenticated GitHub CLI observed the
empty arrays; `verify_native_gate` rejects the real run records. Exact published
member sources independently pass their unchanged, immutable policy versions'
conformance and Ruff 0.16.5 controls, plus Viewer's metadata audit. These are
manual local administrative results. Hosted required-step certification remains
unverified. Cause, persistence and broader service impact are unknown.

The shared environment currently has Ruff 0.16.10; a disposable private tooling
prefix supplies the policy-required 0.16.5 without modifying that environment.
Older immutable policy scripts require their own module context to avoid local
editable `devtools` namespace interference. The unchanged scripts pass when
invoked from their own policy root with the explicit member target. This local
invocation recovery is separate from GitHub's missing step data.

## Alternatives and refuted paths

- Empty requirements or fabricated steps cannot replace executed evidence.
- Rebuilding/repeating scientific qualification cannot repair a metadata gap
  by assertion or reuse a different candidate's results.
- Raw logs or provider artifacts need their own reviewed identity and execution
  interpretation before a shared verifier may treat them as an alternative.

## Scope and exclusions

Recover exact-source/workflow/attempt/required-step evidence. This report accepts
no new Action, mandatory instrumentation, policy relaxation or release operation.
Original published provider bytes and independently acquired installed evidence
are preserved. No component scientific code is changed.

## Acceptance criteria

- Diagnose and recover reliable native required-step facts, or explicitly review
  a qualified alternative at the owning tool.
- Preserve rejection of absent, skipped, failed or mismatched evidence, with
  meaningful positive and negative controls before adopting another mechanism.
- Reconcile the affected original runs without relabeling their sources/attempts
  or administrative results as scientific/public qualification.

## Local implementation issues

None selected. Request provider work only if diagnosis establishes a concrete
missing reusable operation; do not assume GH Run Receptor caused the native gap.
Existing affected work: uibcdf/molsyssuite#106, uibcdf/molsyssuite#115 and
uibcdf/molsyssuite#92; publication uibcdf/smonitor#50.

## Dependencies and risks

Recovery may require an external metadata change or a separately reviewed
evidence capability. Preserve incomplete evidence and its recovery owner.

## Provenance

2026-10-13, Linux, administrative Python 3.14.7. Commands, exact member runs,
immutable policy/copy identities, manual outputs and limits are retained in
`devguide/rollouts/providers_public_guides_106_115_20261013.json`.


## Resolution — 2026-10-14

Native metadata now exposes complete required executed steps for **all fourteen
original affected runs**: eleven member policy/guide runs, SMonitor 0.20.0
promotion attempt 5 and both central push governance runs. The unchanged shared
verifier binds each original source/workflow/event/current attempt, exact job
inventory and successful required steps; Viewer includes its metadata audit.
No workflow was rerun, artifact rebuilt, source/attempt relabeled or requirement
relaxed. Independently verified SMonitor 0.21.0 publication uses separate runs
and cannot substitute for this original-run recovery.

The cause of the earlier native omissions is unknown. This closure records
recovered evidence, not an attributed server fix or a guarantee against recurrence.
Earlier absent/partial records and manually executed administrative controls
remain historical. A renewed omission must still fail verification and be
reported with its exact identities; generic green conclusions do not certify
required executed steps.

Guard relevance: `tests/test_installed_matrix_verifier.py` exercises rejection of
missing/failed/skipped steps, omitted/duplicated jobs, mixed source/attempt and
wrong candidate bindings, plus attempt-qualified read-only native acquisition.
Its existing 10 tests and 7 subtests pass on Python 3.14.7. The real recovered
runs provide positive evidence; existing negative assertions prevent a future
metadata gap from being accepted merely because a run is green. No new tool,
mandatory Action or instrumentation is needed for this recovery.

[Immutable recovery receipt](../rollouts/native_evidence_recovery_118_20261014.json)
retains the original targets/requirements and currently observed native jobs.
Administrative guide qualification, original/public provider qualification and
each consumer's scientific/full-suite debt remain separate. #106/#115/#92 keep
their own owner-adoption and release-operator criteria.
