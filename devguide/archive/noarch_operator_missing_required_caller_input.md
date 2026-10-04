---
summary: Reject generated noarch dispatches missing a component-required input.
issue: uibcdf/molsyssuite#101
status: resolved
opened: 2026-10-04
closed: 2026-10-04
severity: medium
verification: reproduced
area: [distribution, tooling]
guard: tests/test_noarch_release.py::NoarchReleaseTests::test_required_extra_input_never_produces_promotion_command
normative:
blocked_by: []
supersedes: []
---

# Required caller inputs omitted by the standard noarch operator

## What

During uibcdf/molsyssuite#98 / #92 review, the operator's `caller()` accepted
ArgDigest's immutable promotion workflow at
`be39e899f3b9fef2d4ce705799ae19770f41f769` despite omitting its mandatory
`core_run_id`. Standard/recovery fields were declared and forwarded, so the
old subset check succeeded. No incomplete dispatch was attempted. The already
public package remains independently verified with no mutation.

## How

The owning reusable caller validator now checks all declared required inputs
against generated fields before constructing a dispatch. Missing fields yield
`ContractError` naming them and the reviewed-adapter/local-route alternative.
The bounded standard adapter does not choose required defaults implicitly;
optional extra inputs remain accepted. The component's special gate stays
owned and enforced by its workflow. No member workflow or pin changes.

## Why

A prepared administrative command must be complete for its declared caller.
The operator must expose unsupported custom orchestration before the operator
attempts a dispatch. Independent scientific/minimal-core gates cannot be
invented or dropped to fit a shared adapter.

## Measurements and guard relevance

Linux/Python 3.14.7, PyYAML 6.0.3, Jinja2 3.1.6 and packaging 26.3.
Direct reproduction against the real committed caller first returns the
shared provider; after correction it rejects `core_run_id`.
The regression exercises `prepare_handoff` with the same extra-required-input
shape and asserts that `dispatch_arguments` is never called. It fails before
repair with `ContractError not raised`, then passes. All 14 operator tests pass,
including the accepted optional-input case and original public no-mutation,
source, identity, dirty-checkout and recovery bindings. This is relevance
through a failing-before/passing-after reproducer, not just guard addressability.
The existing administrative interpreter is used; no package or scientific test
execution is required to reproduce the caller error.

## Scope and exclusions

Central operator preparation only. Current public receipts, artifact bytes,
scientific selections, component gates, workflow pins and provider v2.3.0
rollout are unchanged. Post-publication read-only verification is still valid.
A component-specific adapter is future separate work, not an inferred capability.

## Accepted result and provenance

The seven registered shared publishers receive prepublication owning-issue
notices; exact links and the actual consumer reproduction are retained in
`devguide/rollouts/release_pipeline_92_argdigest_014.json`.
The contract is documented in `devguide/noarch_release_operations.md`.
The consumer's publication and its wider receiving coordination remain #98;
ordinary operator qualification/effort measurement remains #92. This bounded
fix resolves #101 without closing those independent themes.
