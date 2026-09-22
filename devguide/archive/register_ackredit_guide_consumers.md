---
summary: Register scientific-component consumers for ACKREDIT_GUIDE.md.
issue: uibcdf/molsyssuite#35
status: resolved
opened: 2026-09-21
closed: 2026-09-22
verification: measured
area: [governance, documentation, attribution]
guard: tests/test_governance.py::GovernanceTests::test_ackredit_is_registered_as_incubating_support_library
normative: devguide/adoption_lifecycle.md
blocked_by: []
supersedes: []
---

# Register scientific-component consumers for the Ackredit guide

**Reported:** 2026-09-21, after Ackredit made its host-integration guide suitable for
distribution under `uibcdf/ackredit#24`.
**Status:** Resolved on 2026-09-22 as the first concrete rollout exercising the ongoing
adoption procedure in `uibcdf/molsyssuite#34`.

## What

Register `ACKREDIT_GUIDE.md` for the five repositories classified as
`scientific-component`: MolSysMT, MolSysViewer, TopoMT, PharmacophoreMT and ElastNetMT.
The guide was registered centrally with Ackredit as owner but no consumers. The proposed
registry now names all five scientific components.

## How

Use the publication-to-adoption lifecycle being defined in `uibcdf/molsyssuite#34`:
verify the canonical Ackredit source and owner revision, add the five registry consumers,
generate reviewable byte-identical copies, record a per-member owner and state, run each
member's local checks, and require the central drift inventory to converge.

This is a guide-only rollout. It does not change the member policy-workflow pin unless an
independent required policy release demands that change.

## Why

Scientific components own algorithms, datasets and methods whose dependencies need
traceable credit. Support libraries and developer tools have dependencies to acknowledge
but do not expose the same scientific attribution surface, so distributing the guide to
every member would add irrelevant instructions.

The guide now explains Ackredit's purpose, required host behavior and diagnostic codes.
Distributing it before the first integration lets the integrator follow the contract;
waiting until afterwards reverses the intended ownership model.

## What is measured and what is assumed

Inspected `suite.toml`: `ACKREDIT_GUIDE.md` has Ackredit as owner and an empty consumer
list. The requested five consumers exactly match the current `scientific-component`
classification and the existing ArgDigest/PyUnitWizard scientific-library boundary.

The issue reports that Ackredit's guide improvements and diagnostic-code guard landed
under `uibcdf/ackredit#24`. Their current source revision and member-local compatibility
must be rechecked immediately before rollout.

On 2026-09-22, the canonical source digest was measured as `c75eda29adfe`. Byte-identical
copies were generated only through `sync_vendored_guides.py` and published in MolSysMT
`82866414a`, MolSysViewer `541b179d`, TopoMT `291b56d`, PharmacophoreMT `3702243`, and
ElastNetMT `221c156`. Each repository also points its root agent instructions at the guide
and excludes synchronized guide prose from Ruff without changing its runtime API.

## Alternatives and refuted paths

- Register every member: rejected because the guide's scientific-attribution obligations
  are not relevant to developer tools and support libraries.
- Wait for Ackredit's first public package: rejected for guide distribution because a
  first integrator needs instructions before integration. Publication remains a separate
  release gate and a consumer cannot ship an unavailable dependency.
- Copy files without registry adoption state: rejected because it repeats the coordination
  gap tracked by `uibcdf/molsyssuite#34`.

## Scope and exclusions

This issue owns guide registration and synchronized copies for the five scientific
components. It does not authorize an Ackredit release, require immediate product
integration, or change any policy-workflow pin.

## Acceptance criteria

- The registry derives the consumer set from the five current scientific components.
- The canonical source revision and all five byte-identical copies are recorded.
- Each consumer has reviewable adoption evidence, an owner and a next action or an
  explicit expiring exception.
- Central guide synchronization and repository conformance checks pass after rollout.
- The resulting evidence exercises and informs the operational procedure from
  `uibcdf/molsyssuite#34`.

## Local implementation issues

Open a member issue only if copying the guide exposes repository-specific integration or
validation work. Receiving the guide alone is a coordinated central rollout.

## Dependencies and risks

Ackredit is not yet available on a package channel. The guide must not be interpreted as
authorization to ship an integration before the dependency's release gate is satisfied.

## Provenance

Central registry and issue inspection on 2026-09-21 from the MolSysSuite checkout.
Canonical and consumer content was measured again on 2026-09-22 after publication.

## Resolution evidence

The central registry change and adoption inventory were published in MolSysSuite commit
`8a5e99e`. All five consumer copies have SHA-256 prefix `c75eda29adfe` and the exact-copy
guard reports them current. The same rollout synchronized the updated central ambassador
guide in all 14 registered consumers.

Hosted reruns after consumer publication passed: vendored guide synchronization run
`35703246578` attempt 2 passed its single job, and component guide synchronization run
`35703246618` attempt 2 passed all 15 jobs. Local governance validation passed with 93
tests. Pre-existing Ruff debt in early-stage scientific components remains outside this
guide-only issue.
