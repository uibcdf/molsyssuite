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

## Scope review and proposed first release — 2026-10-10

The principal maintainer asks to address #67 before #82 and #57. This authorizes
preparation and review, not a selected package candidate, version/tag or upload.
The existing publication exception and missing-plan mutation guard remain active.

### Inspected current inputs

| Surface | Current inspected state | Required disposition before a candidate |
| --- | --- | --- |
| Both recipes | `2026.02.0`, build 0, Python >=3.10, no release plans | Select a canonical version/build, reviewed scope, Python bounds and exact-source plans |
| `molsyssuite` | Dependency bundle: MolSysMT, MolSysViewer, SMonitor, ArgDigest, DepDigest, PyUnitWizard and JupyterLab; no installed project code is declared | Qualify the chosen public dependency closure and brief installed capabilities |
| `molsyssuite-dev` | Tool/scientific-dependency bundle plus a Python entry point and source reference to the scripts directory | Decide dependency-only bundle versus a separately qualified executable package |
| Legacy entry point | Recipe calls `molsys_dev_setup:setup_editable_repos`; `setup.py` instead calls `molsys_dev_setup:main`. The helper has a fixed six-clone list, ignores missing clones and catches installation errors | Do not advertise it as the maintained registry-derived installer; preserve or repair it under an explicit tool scope |
| Maintained workspace operator | `development_environment.py` derives eligible sources from `suite.toml`, propagates installation/closure failures and verifies actual origins; #82 governs its integration | Reuse it for local source development, not as installed public-metapackage evidence |
| Central publisher | Both package jobs still select Python 3.13, `noarch: python` and `py_<build>` filenames; no dedicated installed metapackage/promotion workflow | Adapt the local profile after its scope is accepted; do not feed a generic bundle to Python payload/resource adapters |

No executed build/launcher failure is claimed by this source inspection. The
existing development README already directs the qualified workspace away from
the legacy six-clone helper. No helper or component source is changed here.

### Recommended model, awaiting decision

Keep two dependency-only metapackages:

- **`molsyssuite`**: the existing six publicly available library names plus
  JupyterLab, with reviewed compatible constraints. This is a useful initial
  bundle, not a promise to install every registered or incubating member.
  Add another member only after its public dependency route is qualified.
- **`molsyssuite-dev`**: the development/test/docs dependency base, reviewed against
  `molsyssuite-dev-py314.yaml`. Keep the eligible source-clone installation a
  separate explicit workspace operation. It does not automatically install
  `molsyssuite`, link clones or inherit the runtime bundle's version constraints.
  Optional backends absent from the current base do not become mandatory merely
  because they appeared in the retained Python 3.12 environment.

The legacy installer stays as retained source history; the proposed new package
does not ship it. A future installed CLI would need its own module, package/build,
entry-point, failure and installed-command qualification rather than an entry
point added to a dependency bundle. No existing public file or tool is removed
by this proposal.

For metadata-only bundles, propose profile `metapackage`, `noarch: generic`,
explicit build string `meta_0` for build 0, and no executable/Python payload.
Conda documents that `generic` leaves contents unchanged, whereas `python`
performs Python-specific handling; choosing generic here is a proposed application
to dependency-only metadata, not a new rule for Python components.
[Conda-build metadata reference](https://docs.conda.io/projects/conda-build/en/stable/resources/define-metadata.html#architecture-independent-packages).
General exact-file/public verifiers can retain the explicit build string;
the current central caller's Python-specific assertions/filename construction
must be adapted and guarded locally. Existing noarch-Python consumers retain
their contracts, and this work does not require provider v2.3.0 adoption (#87).

Suggested initial version for review is **0.1.0**, build 0, for each package.
It is not a chosen candidate and no active release plan is committed yet. Their
package versions remain independent of immutable `policy-v*` governance releases.
Fresh exact-version/all-label checks and authorized credential access still occur
before any registry mutation; the observations below are not publication preflight.

Proposed first qualification targets:

| Package | Proposed target | Evidence required |
| --- | --- | --- |
| `molsyssuite` | Linux x86_64, macOS arm64 and Windows × Python 3.11–3.14 | One original bundle file; clean public dependency resolution, installed inventory/closure, actual public-library imports and chosen brief commands outside source clones |
| `molsyssuite-dev` | Linux x86_64 / Python 3.14, matching the existing development-base scope | One original bundle file; clean dependency resolution, installed closure and actual build/test/docs tool commands; source/editable and scientific/GUI qualification stay separate |

These are proposed targets, not support claims or a narrowed Python-component
policy. Missing public dependencies, conflicting bounds or failed imports stay
visible and owned; do not replace them with source installs or add unverified
platforms to a badge. Broader developer-platform targets need their own measured
profile. No component's full scientific suite is required merely to test that a
metapackage installs its declared dependencies and tools.

First qualification uses staging: installed evidence is missing for this changed
profile. Retain the two original package files with individual source/build/digest
receipts, qualify each selected matrix, then promote those same bytes under an
authorized route and independently verify public metadata/indexes. Do not rebuild
a staged coordinate or treat a declaration/solver-only result as installed proof.
The existing contract/preflight, generic builder/upload/promoter, exact native
matrix verifier and independent public verifier are reusable primitives; inspect
their profile boundaries before composing the local bundle adapter and its guards.

### Fresh public observation and limits

On 2026-10-10, anonymous package metadata queries for `uibcdf/molsyssuite` and
`uibcdf/molsyssuite-dev` each returned HTTP 404. A control query for
`uibcdf/molsysmt` returned HTTP 200. At `2026-10-10T10:18:34.913806+00:00`, the
public `uibcdf/noarch/repodata.json` returned HTTP 200 and contained no records
for either metapackage in `packages` or `packages.conda`.
This is a bounded observation of public metadata/main index, not proof of every
label, namespace authorization, candidate absence or installed compatibility.
No package is downloaded, built, installed, tagged or published by this review.

### Decision and next steps

Decide the package model first: **two dependency-only bundles** as above, or keep
an installed developer CLI in `molsyssuite-dev` and qualify its different payload.
The recommended route is the former, reusing the maintained workspace operator.
Version, final dependency constraints, exact source and publication timing remain
reviewable release choices; 0.1.0 is a suggestion, not permission to create it.
After scope acceptance, prepare guarded recipes/plans and local qualification
workflows. An actual staging/public release remains a separate final decision
after the candidate is concrete and its required gates have executed.
