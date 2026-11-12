---
summary: Supply explicit workflow-cancellation facts to bounded CI predicate and matrix scenarios.
issue: uibcdf/molsyssuite#177
status: resolved
opened: 2026-11-09
closed: 2026-11-12
verification: measured
area: [ci, tooling]
guard: tests/test_ci_cancellation.py
normative:
blocked_by: []
supersedes: []
---

# Explicit cancellation in bounded CI observations

**Reported:** PharmacophoreMT #169, followed by Diego's implementation instruction
on 2026-11-12.
**Status:** Resolved central capability, with guarded source and local receiving;
the component's workflow correction was already delivered independently.

## What

Represent `cancelled()` and `!cancelled()` when a caller supplies an explicit
workflow-cancellation fact. Without it, retain unknown cancellation rather than
assuming that a manual, scheduled, push or PR event is not cancelled. This is a
prospective capability, not a correction of the old reader's truthful unknown.

## How

Extend existing `condition_outcome`, `scenario_matrix` and `inspect_event_routes`
with keyword-only `cancelled: bool | None = None`. Only actual booleans are
accepted; `None` is unknown and other values raise `ValueError`. A supplied
boolean selects bounded scenario semantics even without a context mapping.
Valid zero-argument `cancelled()` consumes this fact; arbitrary calls remain
unevaluated. Retain existing boolean and operand-preserving matrix semantics,
expression/AST/JSON/matrix bounds and native source/workflow ownership.

Explicit route reports retain the fact as `cancelled`; default reports omit the
new field and keep their previous outcomes and shape. Passing true predicates
or resolving a hypothetical matrix never establishes admission, successful
execution, actual cancellation or cleared CI debt.

## Why

PharmacophoreMT reports that `always()` kept expensive work running after normal
cancellation. Its owner replaced the predicate with `!cancelled()` in published
`af408e7007e27b88d049a09b6cc8ad11db5e8594`, preserving its other route fields.
The shared observer needs an explicit fact to interpret that condition without
forking the parser or fabricating execution state.

## What is measured and what is assumed

On original central `1dde9ebc03cd3d464c11d92966381a9a859f9fff`, seven new guard
methods yield six failures for the unavailable keyword and one passing
unknown/default control. After implementation all seven pass; 81 selected CI
observer/pilot/policy tests pass, followed by a clean 222-test selection including
governance. A missing-fact matrix control caught an initial candidate resolving
an unvisited cancellation call; preserving the older global call-admission
boundary restores its unknown result. A stale new-report index caused one
intermediate governance failure; it was regenerated before final acceptance.

Before/after default comparisons are equal for 19 workflow fixtures, 18
configured-route calls, 432 condition cases and 15 complete pilot reports.
Twelve other function ASTs are unchanged. The actual immutable PHMT workflow
at `af408e7007e27b88d049a09b6cc8ad11db5e8594` is received for eight explicit
source scenarios: cancellation suppresses the predicate; noncancellation retains
weekly/manual admission, manual probe suppression and unknown daily needs.
Its static eight cells stay configured observations in every case. Default
source-route reports are equal to the old reader.

This is administrative/source-predicate behavior, not component science or
native cancellation execution. The [source/test/compatibility receipt](../rollouts/ci_cancellation_177_20261112.json)
retains hashes, failed attempts, actual scope and limits. Final exact-source
central core/automatic informational observer evidence is retained in the owning
#177 closing comment after publication.

## Alternatives and refuted paths

- Inferring workflow cancellation from event names or `needs.*.result` conflates
  independent facts and is rejected.
- Defaulting to `False` would turn missing evidence into an unjustified known
  predicate; default `None` preserves earlier observations.
- A synthetic `github.*` context property would masquerade as a native GitHub
  property; the explicit keyword and report field keep its source clear.
- General expression evaluation, workflow execution or automatic consumer pin
  updates are unnecessary for this bounded observation.

## Scope and exclusions

Only the central shared observer, prospective tests and its tool documentation
change. Existing pilot/catalogue/review records, workflow files, immutable SDK
pins, policies, member sources, the shared prefix and scientific deferrals stay
unchanged. Default aggregate and pilot readers do not assume cancellation state.
This adds no required gate, CLI option or mandatory rollout.

## Acceptance criteria

- Explicit true/false and unknown are qualified across normal/manual/PR/schedule
  conditions, malformed calls/facts and genuine tri-state short-circuits.
- Matrices and configured route/job/test-step observations receive the same
  supplied fact without upgrading execution or dependency evidence.
- Existing relevant tests and a bounded before/after default-report comparison
  pass; no default scenario field or interpretation is silently changed.
- Record the guarded source and exact central hosted checkpoint; return the
  provider result to PharmacophoreMT #169 with independent adoption limits.
- Retire only task-owned temporary resources after durable proof.

## Local implementation issues

`uibcdf/pharmacophoremt#169` owns its already delivered cancellable workflow and
actual native/scientific receiving. The new shared API is optional; no consumer
change or new minimum SDK is commissioned here.

## Dependencies and risks

GitHub's implicit `success()` checks, dependencies, setup steps, server
reevaluation, runner signals and force-cancellation remain outside this reader.
True expression outcomes are not permission to start or qualify a job.

## Resolution and follow-up

The guard module's seven methods test actual booleans/unknown, malformed
facts/calls, tri-state predicates, conservative matrix selection and route/step
propagation. The original failed guards demonstrate the unavailable capability;
the extra red matrix control protects compatibility rather than merely API shape.
The contract is maintained in [the CI tool guide](../ci_pilot.md#explicit-cancellation-facts--2026-11-12).

Return the immutable provider source and native administrative evidence to
PharmacophoreMT #169. Existing callers can retain their qualified frozen SDK;
optional observer adoption remains theirs. No member edit, scientific rerun,
policy tag, mandatory rollout or new release is required. Retire task-only
captures/tools after the closing proof and retain the actual cleanup receipt in
#177; preserve primary work and useful #82 resources.

## Provenance

2026-11-12; Diego's Linux workstation, Python 3.14.7 in
`molsyssuite@uibcdf_3.14`, published Pytest Receptor 1.2.3 in a task-only overlay.
The host's twelve pre-existing dependency findings and primary member work are
preserved. Canonical semantics: GitHub's
[status functions](https://docs.github.com/en/actions/reference/workflows-and-actions/expressions#status-check-functions)
and [workflow cancellation](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-cancellation).
