---
summary: Qualify immutable local clone installations in explicit dependency contexts.
issue: uibcdf/molsyssuite#109
status: resolved
opened: 2026-10-07
closed: 2026-10-07
verification: reproduced
area: [governance, distribution, compatibility]
guard: tests/test_directory_source_contexts.py
normative: devguide/dependency_route_preflight.md
blocked_by: []
supersedes: []
---

# Context-specific directory installation provenance

**Reported:** 2026-10-07 from uibcdf/dockingmt#47.
**Status:** Resolved shared capability; optional consumer qualification remains independently owned.

## What

DockingMT's existing workflows normally install exact ArgDigest/MolSysMT/Viewer
clones with pip --no-deps. Their optional Viewer revisions differ by Python
minor. The @3 SDK initially accepts Git-URL provenance only; legacy @1/@2
supports global required directory sources, without contextual integration roles.
The unchanged consumer route needs a contextual directory profile.

## How

Extend source_provenance with a reusable normal directory checker and @3 with
explicit selected-source-ID bindings. Verify actual root, clean Git HEAD/HTTPS
origin, public version bounds and normal PEP610 directory origin. Retain the
contextual Python, overlay and required/integration rules. Reject roots for
unselected/Git sources, missing/extra bindings and Git inputs on directory routes.
Declaration-only evidence remains declaration-only. No installers are changed.

## Why

Use one provider-owned operation for reusable provenance rather than changing a
scientific route to satisfy a checker or copying one checker into each component.
Existing Git and legacy clients keep immutable pins and behavior. Qualifying
source provenance neither qualifies science nor permits artifact publication.

## What is measured and what is assumed

Test-first local Git fixtures reproduced the missing operation and rejected
@3 profile before implementation. Tests cover a normal exact clone, wrong
commit/repository, tracked/untracked modifications, wrong/nested directories,
editable/archive/Git/ambiguous origins, public version floors, required/integration
roles and mixed Git/directory contexts. Subsequent test results and native source
acceptance are recorded at delivery. No actual scientific clone installation or
artifact qualification is asserted by these fixtures.

## Alternatives and refuted paths

Changing DockingMT's directory installs to Git URL installs would change a
reviewed receiving route. A global @2 inventory cannot express its conditional
optional Viewer revisions. Contextual directory support is an additive explicit
profile; existing clients are not forced to adopt it.

## Scope and exclusions

Provider operation, optional @3 schema/API/CLI and documentation; no new schema
identifier, policy release, guide synchronization, installer transport change,
package build/release, credential change or component scientific dispatch.
HTTPS origins and clean root clones are bounded applicability; other transports
or generated source modifications need explicit reviewed handling.

## Acceptance criteria

- Reusable API and explicit @3 CLI accept the exact normal directory case.
- Negative guards reject all identified mismatches and context ambiguity.
- Existing Git/legacy tests and exact-head hosted administrative gates pass.
- Deliver an immutable accepted provider identity before optional DockingMT rollout.

## Local implementation issues

uibcdf/dockingmt#47 owns the first prospective inventory/adapter adoption.
Other known dependency clients in suite.toml retain their accepted pins.

## Dependencies and risks

Local Git/installer metadata is bounded origin evidence, not tamper-proof native
attestation. A source-only installation cannot establish public dependency closure.
No inventory permits dirty or editable scientific clones through this profile.

## Provenance

Linux x86_64; qualified molsyssuite@uibcdf_3.14, Python 3.14.7. Existing seven
workspace pip-check conflicts remain tracked in uibcdf/molsyssuite#82. No shared
environment dependency change or extra scientific execution is performed.

## Accepted implementation and guard relevance — 2026-10-07

Immutable provider `738fe8dd731abb99dac421b0bb2acc8564110180` is accepted.
Ten new actual-Git/context guards and 61 focused directory/Git/legacy/constraint
cases pass locally; exact-source native governance 37593849810 executes all
416 tests, publisher controls and dependent coverage upload. Native repository,
workflow, event, commit, attempt, jobs and required executed steps are independently
verified. The original missing directory operation/@3 profile failed the test-first
fixtures; the guard now proves correct normal clone provenance and rejects the
listed mismatches, selected-root ambiguity and changed floors. It exercises the
reported receiving mechanism rather than merely checking selector addressability.

Advance notice and immutable acceptance were delivered to uibcdf/dockingmt#47:
https://github.com/uibcdf/dockingmt/issues/47#issuecomment-6034048417 and
https://github.com/uibcdf/dockingmt/issues/47#issuecomment-6034104614 .
Existing source SDK consumers retain their immutable versions. DockingMT explicitly
adopts the new capability at 1d67d3838bb1fd18a59fad8800c317767f7683a6, with
18 receiving guards/one reporting test and exact native administrative review
recorded in its central receipt. Actual science/artifact delivery is not a provider
closure criterion and remains with uibcdf/dockingmt#47.

The separate inherited source-path/multiple-import-root need is now
uibcdf/molsyssuite#110. Its owner-linked receiving control does not alter this
directory API or silently migrate publication callers. No component dependency,
installer transport, policy release, scientific dispatch or package mutation
is performed by this provider delivery.

Consumer source correction — Initial DockingMT preflight correctly rejects
its ArgDigest annotated tag object as HEAD. Corrected source
50f0abbdf14a08b77d26b293d1b670d6dfc204a0 records the tag's actual target commit
separately from unchanged original checkout_ref. An additional actual-tag guard
raises receiving distribution tests to 19, plus one reporting check. The SDK
requires the real commit and is not weakened; first and corrected source/native
evidence are retained separately in the receipt.

Final receiving observation — DockingMT corrected source 50f0abb passes exact
routine Linux CI 37596655381, including all four Python3.11–3.14 scientific
jobs and context/install/test steps. This consumer evidence supplements the
independently accepted provider; it is not full candidate or installed/public
archive qualification.
