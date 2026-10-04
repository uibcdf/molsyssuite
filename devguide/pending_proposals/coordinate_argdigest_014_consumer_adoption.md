---
summary: Coordinate ArgDigest 0.14.0 dependency and digestion changes with registered consumers.
issue: uibcdf/molsyssuite#98
status: partial
opened: 2026-10-04
closed:
verification: inspected
area: [governance, compatibility, distribution]
guard:
normative: devguide/cross_component_feedback.md
blocked_by: []
supersedes: []
---

# ArgDigest 0.14.0 consumer coordination

## What

ArgDigest prepares 0.14.0 under uibcdf/argdigest#24. NumPy becomes an optional
scientific dependency, only literal boolean `True` bypasses digestion,
classmethod receivers leave the digested argument set, and digesters may
optionally accept runtime `qualname`. PyUnitWizard is loaded when an operation
executes rather than when an adapter is created. Core dependency floors remain
DepDigest 0.11.0 and SMonitor 0.16.0.

These are provider-owned implementation and release changes. This central
issue coordinates affected consumers and truthful adoption state under the
existing shared-provider notice policy; it introduces no new release approval
gate or mandatory scientific-suite run.

## How

Use `suite.toml` and the existing `dependency_graph.py` query, including runtime,
test and documentation edges and optional relationships. Recheck committed
manifests, recipes and Conda environments at fetched immutable source heads.
Use existing owning ecosystem reviews for actionable handoffs. Keep notice,
guide equality, runtime receiving review and public artifact qualification
separate. ArgDigest owns its candidate, source and installed matrices,
minimal-core gate, exact-file promotion and independently verified archival.

## Why

Scientific consumers must declare their own NumPy/PyUnitWizard needs rather
than relying on ArgDigest's former dependency closure. Literal bypass values
and deferred provider diagnostics can change observed behavior even when the
dependency manifest is already compatible. Requiring every scientific suite
centrally would duplicate component ownership and interrupt active work.

## Inspected consumer inventory — 2026-10-04

| Consumer | Registered relation | Owner review | Static dependency result |
| --- | --- | --- | --- |
| Ackredit | runtime, tests, docs | uibcdf/ackredit#72 | ArgDigest >=0.13.0; no declared scientific NumPy/PyUnitWizard dependency. |
| DockingMT | runtime, guide | uibcdf/dockingmt#19 | Explicit NumPy and PyUnitWizard; no Conda recipe observed. |
| ElastNetMT | runtime, guide | uibcdf/elastnetmt#14 | Explicit NumPy and PyUnitWizard in project/recipe. |
| LinDelINT | runtime, tests, docs, guide | uibcdf/lindelint#9 | Explicit NumPy and PyUnitWizard in project/recipe. |
| MolSysMT | runtime, docs, guide | uibcdf/molsysmt#244 | Explicit NumPy >=1.26,<3 and PyUnitWizard >=0.25.0 in project/recipe. |
| MolSysViewer | runtime, tests, docs, guide | uibcdf/molsysviewer#110 | Explicit NumPy and PyUnitWizard >=0.25.0 in project/recipe. |
| PharmacophoreMT | runtime, guide | uibcdf/pharmacophoremt#6 | Explicit NumPy and PyUnitWizard in project/recipe. |
| PyUnitWizard | test tooling | uibcdf/pyunitwizard#89 | ArgDigest is a test dependency; NumPy is explicitly declared at runtime. |
| TopoMT | runtime, tests, docs, guide | uibcdf/topomt#56 | Explicit NumPy and PyUnitWizard in project/recipe. |

Nine receiving owners are identified, eight for runtime and PyUnitWizard for
test tooling. Seven registered ArgDigest guide copies already match their
canonical source under the official synchronizer; no consumer copy is manually
edited. The canonical guide already explains optional scientific dependencies,
literal-True bypass and optional `qualname`.

The runtime-package search for suspicious literal `skip_digestion=1` or string
assignments found none in those fetched clones. This bounded text search does
not certify positional/dynamic calls, test fixtures, return semantics,
scientific compatibility or absent optional providers. Receiving owners still
review their relevant call paths and diagnostics. No dependency bump or code
change is inferred solely from manifest inspection.

ArgDigest has also adopted shared noarch publishers at immutable MolSysSuite
`5090a656cd8223826947575f329ee52aa664c725`. The maintained publisher inventory
is refreshed through its existing observation operation. This is an observed
caller adoption, not installed artifact or public-release evidence, and does
not adopt the deferred Conda Action v2.3.0 under #87.

## Handoff and remaining evidence

Each receiving issue gets the old/new source identity, exact provider candidate,
behavior changes, its own inspected dependency result and review request.
Review literal bypass calls, any reliance on early PyUnitWizard import failures,
classmethod argument contracts and scientific pipelines. Existing digesters
need no signature change unless they want optional runtime `qualname`.

MolSysMT/MolSysViewer retain their scientific deferrals and active work. Each
receiving owner decides relevant tests, adoption timing and any justified
fallback or tracked exception; a notice is not an assertion of compatibility.
The producer retains its independent release decision under the existing
contract without a central preapproval gate.

All nine owning notices are delivered; exact links are retained in the primary
receipt. The provider handoff is
[uibcdf/argdigest#24](https://github.com/uibcdf/argdigest/issues/24#issuecomment-5981301948).
The maintained publisher inventory and its current-caller check pass. No local
scientific source, test environment or version constraint was changed.

The source candidate reported by the provider is
`13239a9d631799eb88ea7bed92f04eb3205b029d`. The provider reports passing
source/administrative gates and a twelve-cell full source run, then staging
dispatch. This central record does not newly verify or certify those runtime
claims. Completion/promotion evidence remains with uibcdf/argdigest#24.

## Acceptance criteria

- Preserve provider-owned old/new identities and compatibility/migration scope.
- Identify consumers from maintained inventories and deliver actionable owning
  issue notices, with immutable inspected source/dependency facts.
- Verify canonical guide equality separately from behavioral adoption.
- Reconcile provider release evidence and owner review, adoption or explicit
  deferral outcomes before claiming complete central coordination.
- Preserve independent publication/archival identity and owner-local scientific
  validation; keep unresolved receiving work and its owner visible.

## Scope and exclusions

Central notice, inventory and coordination only. No component source change,
scientific matrix, package build/upload/promotion, version-floor migration or
new common requirement. Public 0.13.0 is not replaced by a candidate claim.

## Dependencies and risks

The release and receiving decisions are still owned by their issues. Missing
receiving evidence keeps this coordination partial. Static declarations do not
prove behavior when external dependency closure changes.

## Provenance

2026-10-04, Linux, administrative Python 3.14.7. `suite_status.py` fetched the
original clones without altering their worktrees; original ArgDigest/TopoMT
dirty files remain untouched. Isolated fetched clones provide static sources.
`devguide/rollouts/argdigest_014_consumer_review_98.json` retains source commits,
dependency/guide relationships, manifest/recipe/environment facts, bounded
search scope, notices and remaining receiving work. Normative stewardship is
`devguide/cross_component_feedback.md`.
