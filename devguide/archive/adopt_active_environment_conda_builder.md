---
summary: Adopt the qualified build action in the shared named-environment noarch publisher.
issue: uibcdf/molsyssuite#78
status: resolved
opened: 2026-10-03
closed: 2026-10-03
verification: reproduced
area: [distribution, tooling, ci]
guard: tests/test_conda_release_contract.py::CondaReleaseContractTests::test_shared_noarch_build_uses_qualified_active_environment_provider
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

## Direct integration review — 2026-10-03

The maintainer authorized direct commits and requested resolving the existing
uibcdf/molsyssuite#81 after reviewing #78. Its exact prepared commit
`4c96e794d207c7fe527b1676302f280b2fb31bff` is integrated with current main,
regenerated indexes and a central regression for the qualified build pin.
Current local validation passes 273 unittest tests on Python 3.13.15 and the
offline governance guard; this is separate from the original prepared pytest
count above. Hosted validation remains Python 3.14. Coordination and the six
consumer handoffs are tracked in
[`adopt_qualified_conda_build_environment_correction.md`](adopt_qualified_conda_build_environment_correction.md).
The shared source is published at
`2a2a459cc3795bb92766fffa0fe28f4d80f01ad4`; uibcdf/molsyssuite#81 is merged.
Hosted governance 37125099269 passes, and all six known shared consumers receive
the exact source in their publication issues. Component caller adoption and
actual staged-file evidence remain pending under #78. No registry upload is
performed by integration.

## Exact-upload environment follow-up (2026-10-03)

After that accepted build correction, Ackredit producer `37127293886` and
Pytest Receptor producer `37127152850` pass real compilation, recipe tests and
archive inspection, then both fail at `Upload exact reviewed file to staging`.
The old upload subaction explicitly uses `shell: bash`, overriding the shared
publisher's login-shell default. Its error handler emits only an unverified
receipt. Independent package/release reads for Ackredit 0.9.0 return HTTP 404;
no occupied coordinate or successful upload is observed, and no automatic
retry is requested.

Provider issue uibcdf/action-build-and-upload-conda-packages#48 owns the repair.
Its regression executes the shell declared in the composite with a controlled
publishing-client activation boundary and the real upload helper. Before the
fix it fails with `FileNotFoundError: anaconda`; afterward the offline client
executes once. The subaction now uses the same login-shell contract as build
and promotion. Failed receipts retain only the exception type, never exception
text or raw client output. All 24 provider tests pass on Python 3.14.7; hosted
exact-upload contract run `37128312876` passes at immutable provider source
`6f65ba66d1afff74ded8442c3c3ee6448a5f3a60`.

This follow-up proposes adopting that source for both exact-upload steps only.
It preserves the separately qualified build pin, promotion pin, interpreter
support, sealed digest-bound bytes, occupied-coordinate rejection, single
mutation, no force/retries and independent poststate verification. Central
publication-contract tests guard the accepted pins. The older central
metapackage workflow uses the combined action, whose upload already runs in a
login shell; that different route does not qualify this separate upload step.
The shared publisher already uses Python 3.13, so changing a developer's local
3.14 environment cannot resolve this hosted shell boundary. Actual staged and
public delivery remain unverified until consumer execution after adoption.

## Fully qualified upload adoption — 2026-10-03

The maintainer authorized continuing after reviewing the later provider closure
notice uibcdf/molsyssuite#86. Integrating the existing PR #85 now selects
`1aa2011f902a1a9d533564572245bb29f6862e86` for both exact-upload steps, updating
the earlier prepared `6f65ba6...` proposal. Native provider run 37129463375 passes
the offline contract plus the actual composite in named Linux/macOS Conda
environments for success and write failure. Client/registry behavior is simulated;
no real consumer upload is certified by that qualification. The adopted central
regression rejects the earlier proposal and preserves the qualified build pin,
single-file upload-free compilation and both exact-upload operations.

Central review/adoption and the six member handoffs are tracked in
`adopt_qualified_exact_upload_environment.md` under #86. The existing #78 remains
the consumer integration record. Release decisions and any later mutation retain
the existing exact-source and independent state requirements.


## Resolution and queue correction — 2026-10-03

This prepared implementation history shares the resolved owning issue #78.
The final adoption record was already archived; this older companion remained
in the partial queue by mistake. Both records now agree with the closed issue.
Original observations and failed runs above remain historical evidence.

Ackredit producer 37136075066 and Pytest Receptor producer 37136074225 execute
real recipe builds, archive inspection and verified staging uploads through
the accepted shared publisher and active-environment provider. The central
guard rejects the original failing build pin. Installed matrices 37152044426
and 37148738757 and same-byte public promotions 37152421084 and 37151517509
are separate successful evidence. Details are in the final
[adoption record](adopt_qualified_conda_build_environment_correction.md),
`devguide/rollouts/installed_noarch_88_89.json` and
`devguide/rollouts/release_pipeline_92.json`.
