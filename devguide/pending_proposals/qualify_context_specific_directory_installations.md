---
summary: Qualify immutable local clone installations in explicit dependency contexts.
issue: uibcdf/molsyssuite#109
status: active
opened: 2026-10-07
closed:
verification: reproduced
area: [governance, distribution, compatibility]
guard: tests/test_directory_source_contexts.py
normative: devguide/dependency_route_preflight.md
blocked_by: []
supersedes: []
---

# Context-specific directory installation provenance

**Reported:** 2026-10-07 from uibcdf/dockingmt#47.
**Status:** Active implementation; immutable acceptance and consumer adoption pending.

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
