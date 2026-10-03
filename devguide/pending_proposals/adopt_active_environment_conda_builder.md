---
summary: Adopt the qualified build action in the shared named-environment noarch publisher.
issue: uibcdf/molsyssuite#78
status: active
opened: 2026-10-03
closed:
verification: reproduced
area: [distribution, tooling, ci]
guard:
normative: devguide/noarch_conda_workflow.md
blocked_by: []
supersedes: []
---

# Shared noarch publisher selects the base manager without its build plugin

## What

Ackredit staging run `37109889925` and Pytest Receptor staging run
`37111808160` install conda-build in `noarch-publisher`, then fail before archive
production because the action's shell function invokes a base Conda manager
without that plugin. Source preflight and recipe/resource inspection pass;
neither run supplies an uploaded artifact or installed delivery receipt.

## How

The provider correction is published on
`uibcdf/action-build-and-upload-conda-packages` at
`8da628d9b393e184c3bf3722708b19dcfbf7ef0a`. Compilation and conversion use
`command conda` to select the active environment's executable on PATH.
Provider issues uibcdf/action-build-and-upload-conda-packages#46 and
uibcdf/action-build-and-upload-conda-packages#47 record the runtime correction
and repaired multi-variant verification, respectively.

The prepared central change updates only the build action reference in
`.github/workflows/publish-noarch-conda.yaml`. Exact-upload and promotion pins,
recipe testing, version freeze, resource inspection, source gate acquisition,
installed matrices, secrets and independent public verification are retained.
The historical central metapackage profile is excluded from this noarch repair.

## Why

The named-environment publisher is shared by registered members. A local
consumer workaround would obscure the owning executable correction and leave
other consumers broken. Platform coordination is uibcdf/moli#38; component
delivery remains owned by uibcdf/ackredit#22/#75/#80 and
uibcdf/pytest-receptor#32. The separate installed-test dependency limitation is
uibcdf/molsyssuite#77.

## What is measured and what is assumed

An isolated Conda 26.9.1 base/Python 3.14 manager without conda-build plus an
activated Python 3.13 publisher containing conda-build 26.9.0 reproduces
`conda build --version` exit 2 and `command conda build --version` success.
The provider regression executes its actual compilation script with this
shadowing boundary and verifies build/conversion failure propagation.

At the exact published provider source, hosted run `37115921728` passes four
real noarch recipe-test cells: Linux named/base, macOS arm64 named and Windows
named, retaining inspected archives and producer evidence. Run `37115921702`
passes unit and both Linux/Windows variant jobs: every host checks eight archive
payloads and imports fresh Python 3.11/3.12 installations with asserted prefix,
minor, module origin and version. All 23 local provider tests pass on Python
3.14.7. GH Run Receptor confirms both completed hosted successes.

Ackredit's independent local noarch 0.9.0 diagnostic passes recipe tests,
resource inspection, a normal fresh Python 3.14.7 installation, saved original
bibliography, reused capture and pip check. That file is not staged or public;
it cannot substitute for the actual shared producer and installed matrix.

## Alternatives and refuted paths

Installing conda-build in a developer's environment does not repair the hosted
manager/plugin boundary. Adding a login shell does not help: both the original
publisher and action already use login shells. Skipping recipe tests or copying
publisher implementation into consumers would weaken the shared contract.

## Scope and exclusions

This is an implementation pin repair under the existing publication contract,
not a change to Python support, release eligibility or public-promotion authority.
It does not require changing the versioned member policy caller. Consumer
workflow-pin adoption and component releases remain separate, owned work.

## Acceptance criteria

- Review the immutable provider source and the executed qualification above.
- Pass central offline governance and existing publication-contract tests.
- Publish the repaired shared source and identify its immutable commit to callers.
- Keep owner issues and component labels for Ackredit and Pytest Receptor.
- Record actual shared staging/installed/public evidence before any delivery claim.

The normative pin and evidence boundaries remain in
`devguide/noarch_conda_workflow.md`. The independently callable provider owns
the executable regression in `tests/test_compilation_environment.py`; central
publication tests preserve immutable pins and the noarch workflow controls.

## Provenance

Prepared on 2026-10-03 from central source
`e459ea0e8ac6aa8017e17a2f171c50d122b9e0b7`. Local checks use
`molsyssuite@uibcdf_3.14`, Python 3.14.7. The primary central checkout and its
unpublished PyUnitWizard guide-registration changes are preserved.


## Prepared local verification

`python devtools/scripts/validate_governance.py` passes. The full local central
suite passes 277 tests with `python -m pytest --receptor=llm` on Python 3.14.7.
The change is prepared in an isolated clone; central publication and actual
consumer adoption are not claimed by these checks.
