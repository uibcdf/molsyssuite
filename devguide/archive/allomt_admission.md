---
summary: Admit AlloMT through the official Python starter with explicit initial scope.
issue: uibcdf/molsyssuite#202
status: resolved
opened: 2026-11-15
closed: 2026-11-16
verification: measured
area: [admission, scientific-components]
guard: tests/test_governance.py::GovernanceTests::test_registry_contains_the_agreed_members
normative: devguide/new_component_starter_kit.md
blocked_by: []
supersedes: []
---

# AlloMT initial member admission

**Reported:** Diego requested AlloMT's initial structure and registration on 2026-11-15.
**Status:** Resolved for central admission and actual official source/caller
receiving. Broader owner qualification remains separately tracked in AlloMT #1.

## What

AlloMT (Allostery MultiToolkit), `uibcdf/allomt`, will provide prediction and
characterization of allosteric mechanisms as a MolSysSuite component within MolI.
Register it as a primary, active, incubating `scientific-component` with the
`python-package` capability. Incubation does not assert a scientific API or
platform support.

## How

Publish the accepted registry admission on central `main`, then generate into an
empty stage with the official starter and the latest published policy. Record the
full published admission commit when the member is absent from that frozen
policy; retain the genuine identity as provenance when a newer snapshot already
contains it. Integrate the stage into the existing repository without replacing its Git history or local work.

Register all eight applicable canonical guide relationships. The support-library
guides are design references for future boundaries, not declarations of runtime
dependencies. Source initialization has no required scientific runtime dependencies.
Use the official synchronizer for canonical copies.

Keep ecosystem, CI and distribution reviews pending until received evidence exists.
Python 3.14 transition authorization permits qualification; it does not mark it
admitted. Zenodo archival is optional while incubating. The publisher inventory
initially observed README-only source. Current foundation receiving still makes
no publisher or public package claim.

## Why and ownership

AlloMT owns allostery-specific analysis, interpretation and result contracts.
MolSysMT owns molecular representation, selections and structural operations;
ElastNetMT owns elastic-network numerical methods. Specialized topology, binding,
pharmacophore and visualization operations remain with their existing owners.
An elastic mode, correlation or visualization alone does not establish an
allosteric mechanism. Scientific methods and evidence thresholds require a later
owner-local contract before implementation.

MolSysSuite owns this registration and shared engineering applicability. AlloMT
owns its source, tests and qualification in uibcdf/allomt#1. The separate prospective
latest-policy requirement remains uibcdf/molsyssuite#201.

## Evidence and limits

The initial AlloMT local and published `main` are
`3c4a9d0a4ff397f3b37b88f62a91fab3d619f98b`: a README without package or workflows.
The official starter and frozen `policy-v1.5.12` were inspected from central
`e4d97ba1ac5341aa2d1cd50b56096098e59bb940` in an isolated checkout.
Record executed validation with this proposal; configured gates, source tests,
hosted matrices, public distribution and scientific validation remain distinct.

Local receiving on 2026-11-15 used the existing
`molsyssuite@uibcdf_3.14` Conda interpreter, Python 3.14.9 and Ruff 0.16.5.
`validate_governance.py`, `git diff --check`, Ruff lint/format of the changed test
and 150 governance/starter/admission tests passed. The test command was
`PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -p pytest_receptor.plugin
tests/test_governance.py tests/test_suite_policy.py --receptor=llm`.
The installed PytestReceptor was the existing local `1.2.2+8.gacd8897` editable.
An initial default-plugin run failed before collection because the pre-existing
SMonitor editable could not import `smonitor.core.manager`. Selective plugin
loading scopes this administrative check; it does not repair or qualify that
shared environment, substitute for published-tool component qualification or
establish hosted CI. No sibling source or caller-owned environment was changed.

## Acceptance criteria

- Central registry, guide inventories, generated dependency view and applicable
  admission/governance checks pass.
- Accepted membership is published on central `main`, providing a genuine immutable
  admission identity for the official generator.
- AlloMT receives the official scaffold and synchronized guides, with executed
  source checks and missing evidence recorded in uibcdf/allomt#1.
- Hosted compatibility, shared-workspace receiving, first scientific contract and
  public distribution retain explicit owner-local follow-up.

## Central receiving after withdrawal — 2026-11-15

Diego explicitly selects central admission followed by #201. Withdrawn PR #203
is not reopened or merged. Its reviewed registration changes are received from
`14569063ab6342a2afffd5d13d0e060d0682386e` and completed in the active central
checkout. All eighteen members now have explicit coverage-applicability rows;
AlloMT's initial row claims no executable producer or percentage. The planned
development cohort and explicit reinstall tests now include AlloMT without
asserting successful shared installation. Whole-source/human trees and the
paused #82 prefix remain untouched.

The initial PR failures are retained: native governance 43764999836 has three
failed inventory/count assertions, while development preflight 43764999759 has
the two corresponding count failures. The corrected 173-test governance,
admission, coverage and workspace selection passes using published Pytest Receptor
1.2.3 in a temporary overlay with plugin autoload disabled. All 641 top-level
central pytest cases complete: 640 pass and the existing opt-in native Mamba
case skips. This follows the native central module scope. An earlier exploratory
recursive pytest invocation collected the nested installed-tool fixture outside
its installation context and failed collection; it executed no cases and is not
reported as a product-test failure or pass.

Ruff's required py311 target and formatting pass on touched Python files;
legacy import ordering, a concatenated command string and explicit check=False
are corrected only in those touched tests without changing their behavior.
Indexes, generated dependency view, diff checks and offline governance pass.
Local execution uses the existing Linux/Python 3.14.7 named interpreter, without
installing into or repairing it. The published-tool overlay preserves the owner
environment; the prior proposal's editable tool measurements remain historical.

Published admission is `adaef199b74c6da72ca43c21401c245990c70727`.
The real official empty-stage generator succeeds using that admission SHA and
policy-v1.5.12 (peeled source `bb641488bc22b262549f795857d6ede529b14ca1`).
All eight guides are synchronized through the official tool; the frozen policy
checker passes and both generated-stage tests pass. A second actual generation
with the #201 direct CLI and fresh authoritative target check also succeeds.
An initial direct invocation failed before writes on the pre-existing foreign
`devtools` namespace; module-qualified generation worked, and #201 repairs the
owning import boundary. Stage execution is not owner-repository publication.

GH Run Receptor 1.1.1 is followed by native exact-job/step inspection. Core run
43766681190 succeeds at the admission SHA: governance job 132973283319 executes
all four required validation/test/publisher/artifact steps, and coverage job
132973487022 executes the upload. Hosted component/source audits retain their
limits: AlloMT private checkout is Not Found before inspection; guide/manifest
and development audits do not establish component or environment qualification.
TopoMT's instruction failure and OpenCASTp's dependency failure remain with their
existing owners. No credential diagnosis or scope change is inferred.
The published admission/stage identities and access limit are handed to
uibcdf/allomt#1; uibcdf/allomt#2 owns its workflow. The owner source remains the
README-only immutable source in the initial observation. The accompanying
[policy rollout receipt](../rollouts/latest_policy_adoption_201_20261115.json)
retains exact central evidence and acquisition limits. This report and #202 stay
partial for the owner's actual scaffold/caller receiving. Owner-local foundation work stays intact; no scientific method,
engine, public package or platform support is admitted by this registration.

## Dependencies and alternatives

Generation depends on published central admission (uibcdf/molsyssuite#73).
Do not copy an arbitrary component or fabricate an admission identity. No new
policy release, numerical backend or parallel implementation is needed for this
registration. The latest-policy rollout is coordinated separately under #201.

## Selected continuation — 2026-11-15 Mexico City / 2026-11-16 UTC

[Current source/delivery/owner receipt](../rollouts/six_issue_receiving_20261115.json)
receives the actual AlloMT foundation at 162b73505f55c556137dfd7302d4968bc34da593. Eight
full source files bind Git blobs/SHA256: import/build metadata, actual two source tests,
bootstrap/provenance and real policy workflow. The guide-only published successor
0d3698b559d8c15b0d3a79abd99e7b5eba01e84e receives the current common guide; its other
seven registered copies were already current.

Published GH Run Receptor 1.5.0 precedes independent native verification of original
owner source 8f0b82fdbfc87ef7757a714cd7f671b98bff801f: routine 43778869097 and
owner-dispatched historical compatibility 43778947014. Quality and the five actual Linux
install/pip-check/test cells pass; configured event skips remain skips. Two tests per
cell is owner-reported; these historical executions are not relabelled as qualification
of 162b or the guide commit.

The current actual caller is policy-v1.5.12, workflow_dispatch only, with a required
human admission input rather than a retained genuine central admission constant. Owner
provenance still says pre-admission/missing membership. This is no longer README-only
source, but actual official accepted-member integration and automatic valid frozen
member gate are still pending in AlloMT #1. The published admission
adaef199b74c6da72ca43c21401c245990c70727 remains valid; policy-v1.6.0 already includes
AlloMT, while old 1.5.12 requires the separate admission route. Keep #202 partial for
that concrete original scope; current 1.6.0 adoption remains #201 and wider
protection/workspace/first-science/public qualification remain owner-local.

## Resolution — 2026-11-16 Mexico City / 2026-11-17 UTC

AlloMT source `1acb324e4b48139cc27203263f8ae158b7c91603` receives the actual
official frozen policy-v1.6.0 generator and its automatic push/PR/manual caller,
with four generated identity badges and complete provenance. The source parent
`30e6971f9f2ed8b83aa2e6e0d96a82aef17b21d4` includes the owner's later research,
design and Discussions work; only six administrative paths change and the rest
are hash-preserved. The generated caller has only a trailing blank line normalized.
The policy already registers AlloMT, so no dispatch-time admission input is needed;
the genuine original admission remains unchanged in the record.

The [exact receiving receipt](../rollouts/allomt_foundation_receiving_202_20261116.json)
binds all generated files, owner receipt Git blob/SHA256, preserved input manifest,
eight unchanged current canonical guides, two actual stage tests and two actual
source import/report tests. Five prior checker findings become zero; the independently
verified published-target observation reports CURRENT. Published GH Run Receptor 1.5.0
precedes native exact-source policy run 43989586910, attempt 1, job 133726449814:
repository conformance, Ruff lint/imports and formatting all execute and pass.

The separate source CI 43989586153 is **failed**, not passing: quality/index job
133726448059 passes, while test job 133726447645 fails acquiring the uibcdf Conda
repodata before install/pip-check/pytest. Zero hosted test passes are claimed at
this source. One bounded channel preflight also times out; no unchanged retry,
dependency weakening, unrelated pin update or environment substitution is made.
AlloMT #1 retains this exact run and its channel-recovery retry condition, plus
protection/workspace/broader review. First science and Discussions UI/form evidence
remain #2/#4, with no public platform, scientific or package claim.

This satisfies the original central registry/published admission and actual
official scaffold/guide/source-check receiving criteria. The original final
criterion explicitly keeps wider qualification owner-local; no acceptance is
deleted or changed into a passing claim. The exact expected-member guard above
protects AlloMT registration, while the frozen owner gate protects the exercised
caller/badge integration. #201 receives this one actual latest-policy row, not
all-member completion; #197 receives only the bounded administrative profile.
Withdrawn PR #203 remains closed/unmerged and the #82 shared-prefix pause remains.
