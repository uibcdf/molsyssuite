---
summary: Provide a shared ABI3 recipe audit and an evidence-preserving native release composition.
issue: uibcdf/molsyssuite#113
status: partial
opened: 2026-10-10
closed:
verification: measured
area: [governance, distribution, compatibility]
guard: tests/test_native_conda.py
normative: devguide/python_distribution_policy.md
blocked_by: []
supersedes: []
---

# Shared native ABI3 distribution integration

**Reported:** 2026-10-10 by ElastNetMT, while integrating owned Rust kernels.
**Status:** Partial. Shared recipe audit implemented; component-native Conda
adapter qualification and owner acceptance remain pending.

## What

The accepted `native-abi3` plan describes per-platform immutable files, but
dependency-routes only accepted noarch recipe kinds. ElastNetMT cannot use
noarch artifact adapters for its embedded extension. Provide reusable native
declaration checks and identify the existing general release operations with
their explicit receiving boundaries.

## How

`native_conda.py` implements independent rendered/source recipe audits using
existing plan validation, sandbox rendering and dependency range comparison.
The optional `native-abi3-dependencies` recipe kind works with `@2`/`@3`.
Original `@1`, noarch kinds, pins and publisher workflows retain their contracts.
The [native integration guide](../native_abi3_conda_workflow.md) documents the
bounded profile, complete release composition and unresolved native receiving.

Selectors require a bound actual per-platform rendering or reviewed extension;
compiler/hash/Python placeholders never establish a real toolchain or file.
All receipts keep declaration checks separate from actual installed context,
native bytes, science, registry mutation and independent public observation.

## Why

Two existing native components and future native members need a general route.
Reuse shared declaration/gate/file operations while components keep their
architecture/linkage/resource/science validators. Do not copy noarch checks
into a consumer or relax their binary-payload refusal.

## What is measured and what is assumed

The pre-extension source rejects native recipe kinds. The new administrative
fixture exercises the optional kind, a rendered API, real CLI invocation,
negative dependency/Python/identity/ABI3/drift controls and `@3` actual installed
bounds while retaining `native_bytes_verified = false`. Existing noarch and
general transition/matrix/public tests are rerun for compatibility.

Inspected immutable publisher contracts are the established build
`8da628d9b393e184c3bf3722708b19dcfbf7ef0a`, upload
`1aa2011f902a1a9d533564572245bb29f6862e86` and promotion
`8a1f203c2cfe51acd63de7452117b4b6e9d609f4`. They accept native coordinates;
inspection does not qualify a new native candidate, binary or hosted adapter.
MolSysMT's existing component-specific ABI3 validator remains its own work.

ElastNetMT's active local work was inspected read-only after `suite_status.py`.
Its recipe/callers are suspended; historical renamed noarch fixtures remain
owned by the component. No current recipe, version, candidate or upload is
selected, and no source wheel result is treated as Conda proof.

## Alternatives and refuted paths

- A noarch exception for embedded native extensions contradicts payload
  applicability and would weaken existing guards.
- Duplicating the consumer's scientific/native validator centrally would move
  component-specific contracts away from their owner.
- Reusing the single-file noarch cross-source recovery descriptor for two native
  files would lose artifact binding. It requires its own reviewed extension.
- Automatically replacing existing member pins or launching scientific suites
  is unnecessary to qualify this additive declaration API.

## Scope and exclusions

Shared SDK declarations, integration guidance and owner handoff are in scope.
Native kernels/science, first release selection, new tags/packages/uploads,
action v2.3.0 and withdrawal are outside this implementation. Ordinary direct
push policy and scientific debt remain unchanged.

## Acceptance criteria

1. Shared independently usable native audit with meaningful positive/negative
   guards and existing noarch compatibility: implemented; verify exact pushed
   provider administrative CI before claiming hosted availability.
2. Explicit compatible build/installed/promotion/public composition and raw
   receipt boundaries: documented using established generic primitives.
3. Owner adopts an immutable qualified provider and registers reviewed native
   Conda adapters with source/file/matrix binding and archive/resource negatives:
   pending uibcdf/elastnetmt#18 and uibcdf/elastnetmt#26.
4. Distinguish preparation from the future real two-file/eight-cell candidate,
   installed science, promotion and public availability: retained. No candidate
   is required to qualify an offline declaration operation.

## Local implementation issues

- uibcdf/elastnetmt#18: native distribution adapter qualification and SDK adoption.
- uibcdf/elastnetmt#26: owned extension/resource/scientific receiving evidence.
- uibcdf/molsyssuite#45: distribution inventory remains partial for this member.

## Dependencies and risks

Owner active work must remain intact. New declarations cannot substitute for
binary inspection or native qualification; a component must not activate the
publication route merely because its early check turns green. Existing SDK
clients remain on their reviewed pins; affected receiving instructions are
delivered through the impact issue before publishing the additive SDK.

## Provenance

2026-10-10, this Linux development host, qualified
`molsyssuite@uibcdf_3.14`, CPython 3.14.7. The two editable receptors retain their
caller-owned primary import origins. `pip check` retains exactly the seven
accepted conflicts under uibcdf/molsyssuite#82; none is hidden or attributed to
this SDK change. Selected central administrative tests are not component
scientific tests. Exact commands, dependency versions, results, consumer scope
and provider handoff are recorded in the dated #113 receipt at completion.
