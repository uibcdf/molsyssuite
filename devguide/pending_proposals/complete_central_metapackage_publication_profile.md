---
summary: Finish reviewed plans and installed evidence for the central Conda metapackages.
issue: uibcdf/molsyssuite#67
status: partial
opened: 2026-10-01
closed:
verification: inspected
area: [governance, distribution]
guard:
normative: devguide/conda_publication_policy.md
blocked_by: []
supersedes: []
---

# Central metapackage publication profile

**Reported:** 2026-10-01 during the shared Conda contract review.
**Status:** Partial: publisher controls repaired; package plans and installed
profile evidence remain pending before an authorized package release.

## What

The `molsyssuite` and `molsyssuite-dev` recipes still have legacy calendar
versions and no reviewed candidate plans or measured installed metapackage
matrix. They cannot claim the new Conda publication profile is complete.

## How

Adopt per-package plans matching canonical version/build identity, establish the
actual supported dependency/capability matrix, and exercise a permitted route
with an explicitly authorized package candidate. The current source already
pins the publisher action, produces one noarch file per package, separates
manual staging from eligible automatic direct publication, queries exact native
gates/all-label absence, and preserves producer/independent public evidence.
Missing or mismatched plans fail before a registry mutation.

## Why

Central ownership does not grant a release-verification exemption. Metapackage
dependency/capability checks differ from the component scientific suites.

## What is measured and what is assumed

Source topology and administrative controls are inspected and contract-tested.
There is no new built/installed metapackage or public-release evidence.

## Alternatives and refuted paths

Running unrelated scientific suites would not establish this package profile.
Copying a component workflow would preserve its recipe-specific assumptions.
An undocumented publishing bypass would make incomplete adoption look complete.

## Scope and exclusions

The two central Conda metapackages. No current package publication authorization
and no changes to component scientific implementations or deferred science reviews.

## Acceptance criteria

- Reviewed matching package plans, recipes and exact candidate/build identities.
- Installed dependency/capability checks on the claimed platform/Python matrix.
- An authorized candidate exercising the chosen route with independent evidence.
- Remove the exception in `devguide/rollouts/conda_publication.md`.

## Local implementation issues

Owned centrally; common contract accepted under uibcdf/molsyssuite#27.

## Dependencies and risks

Responsible maintainers: dprada/LMMV. Exception review/expiry: 2026-12-31.
Missing/nonconforming plans block mutations. Governance `policy-v*` releases
do not trigger package publication.

## Provenance

2026-10-01; central source inspection and administrative contract tests only.
