---
summary: Admit AlloMT through the official Python starter with explicit initial scope.
issue: uibcdf/molsyssuite#202
status: active
opened: 2026-11-15
closed:
verification: inspected
area: [admission, scientific-components]
guard:
normative:
blocked_by: []
supersedes: []
---

# AlloMT initial member admission

**Reported:** Diego requested AlloMT's initial structure and registration on 2026-11-15.
**Status:** Registration proposed; component qualification remains owner-local.

## What

AlloMT (Allostery MultiToolkit), `uibcdf/allomt`, will provide prediction and
characterization of allosteric mechanisms as a MolSysSuite component within MolI.
Register it as a primary, active, incubating `scientific-component` with the
`python-package` capability. Incubation does not assert a scientific API or
platform support.

## How

Publish the accepted registry admission on central `main`, then generate into an
empty stage with the official starter and the latest published policy. Record the
full published admission commit in the generated policy caller. Integrate the
stage into the existing repository without replacing its Git history or local work.

Register all eight applicable canonical guide relationships. The support-library
guides are design references for future boundaries, not declarations of runtime
dependencies. Source initialization has no required scientific runtime dependencies.
Use the official synchronizer for canonical copies.

Keep ecosystem, CI and distribution reviews pending until received evidence exists.
Python 3.14 transition authorization permits qualification; it does not mark it
admitted. Zenodo archival is optional while incubating. The publisher inventory
observes the existing README-only source, with no publisher or package claim.

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

## Dependencies and alternatives

Generation depends on published central admission (uibcdf/molsyssuite#73).
Do not copy an arbitrary component or fabricate an admission identity. No new
policy release, numerical backend or parallel implementation is needed for this
registration. The latest-policy rollout is coordinated separately under #201.
