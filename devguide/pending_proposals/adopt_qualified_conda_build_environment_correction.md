---
summary: Adopt the qualified Conda build executable correction in shared publishers.
issue: uibcdf/molsyssuite#78
status: active
opened: 2026-10-03
closed:
verification: measured
area: [governance, packaging, ci]
guard:
normative:
blocked_by: []
supersedes: []
---

# Conda build executable correction

## What

The shared noarch publisher pins build action
`8a1f203c2cfe51acd63de7452117b4b6e9d609f4` (v2.2.2). Named publisher environments
contain conda-build, while the activation shell function can still invoke the
base manager, which cannot discover that plugin. Ackredit staging run
[37109889925](https://github.com/uibcdf/ackredit/actions/runs/37109889925)
and Pytest Receptor staging run
[37111808160](https://github.com/uibcdf/pytest-receptor/actions/runs/37111808160)
failed before producing an archive. The provider owns the fix as
uibcdf/action-build-and-upload-conda-packages#46, with fixture qualification in
uibcdf/action-build-and-upload-conda-packages#47; MOLI coordination is uibcdf/moli#38.

## How

The provider publishes the qualified correction at immutable
`8da628d9b393e184c3bf3722708b19dcfbf7ef0a`. The actual compilation and conversion
steps use `command conda` to select the executable on the activated environment's
PATH. Build/mambabuild, conversion options, recipe tests, outputs, failure
propagation and upload controls remain covered by the provider's regression
`tests/test_compilation_environment.py`.

The reviewed adoption is a build-action pin change in
`.github/workflows/publish-noarch-conda.yaml` and the two build steps in
`.github/workflows/build_and_upload_conda_packages.yaml`. The separate exact-file
upload and promotion pins serve other operations and do not need replacement
merely because the compilation executable changed. Consumers adopt a newly
published immutable shared workflow source; existing policy tags remain immutable.

## Why

This is a reusable provider capability, not a scientific package defect. Both
real consumers reproduce the same executable boundary. A local orchestration
workaround in uibcdf/pytest-receptor#34 should be retired after the qualified
shared route is adopted and actually builds the component's exact candidate.
Publication access, installed scientific gates and public delivery remain local.

## Measured provider evidence — 2026-10-03

Native [37115921728](https://github.com/uibcdf/action-build-and-upload-conda-packages/actions/runs/37115921728)
passes four real build cells at the exact correction commit: Linux named and
base, macOS ARM named and Windows named. Every cell executes the recipe tests,
archive inspection and retained upload-free producer evidence. Native
[37115921702](https://github.com/uibcdf/action-build-and-upload-conda-packages/actions/runs/37115921702)
passes unit tests plus Linux/Windows multi-variant build and installed-import
checks, with explicit installed interpreter, prefix and module-origin assertions.
The production diff changes the two executable invocations. These are provider
qualification receipts; they are not shared-caller or scientific artifact receipts.

## Scope and decisions

The user requested review of #78 after the Python-policy rollout. Review is
complete and the immutable provider source is qualified for adoption. Shared pin
changes, caller rollout and real shared-route integration are still pending.
No registry upload, promotion, component release or scientific test execution
has been performed by this review. The existing publisher's administrative/build
Python 3.13 is a tool runtime and is separate from the 3.14 routine package-test
baseline; no unsupported scientific platform claim is inferred from it.

## Acceptance criteria

- Adopt the reviewed immutable build-action source in applicable shared callers.
- Protect the selected compilation pin and existing publication controls with
  the maintained workflow guards.
- Verify the actual shared named-environment route with recipe tests and
  inspected archives, without public publication during qualification.
- Record component caller adoption and their owner issues; retain their full
  installed/public gates before closing their delivery work.
- Retire the temporary Pytest Receptor orchestration only after the shared route
  replaces it and passes for the selected exact candidate.

## Maintainer work order — 2026-10-03

After the current policy rollout, attend uibcdf/molsyssuite#78, then resolve
uibcdf/molsyssuite#81 as explicitly requested by the maintainer. The latter is
the prepared shared noarch build-reference change; review its exact source and
checks before adoption. Coordination review does not close #78 before its
publication/adoption handoff is actually complete.

## Local implementation issues

uibcdf/ackredit#22, uibcdf/ackredit#75 and uibcdf/ackredit#80 own its artifact and
public delivery. uibcdf/pytest-receptor#32 and uibcdf/pytest-receptor#34 own its
release and temporary workaround. uibcdf/molsyssuite#80 retains the second
consumer reproduction. Other publisher profiles require individual inspection.

## Provenance

Read provider #46, the exact production diff and native run/job/step JSON on
2026-10-03. Source and hosted evidence are pinned to the full commit above.
