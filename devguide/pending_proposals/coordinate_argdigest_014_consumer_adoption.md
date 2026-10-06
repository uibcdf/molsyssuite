---
summary: Coordinate ArgDigest 0.14.0 dependency and digestion changes with registered consumers.
issue: uibcdf/molsyssuite#98
status: partial
opened: 2026-10-04
closed:
verification: measured
area: [governance, compatibility, distribution]
guard:
normative: devguide/cross_component_feedback.md
blocked_by: []
supersedes: []
---

# ArgDigest 0.14.0 consumer coordination

## What

ArgDigest published 0.14.0 under completed uibcdf/argdigest#24. NumPy becomes an optional
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
| PyUnitWizard | runtime and test tooling after receiving review | uibcdf/pyunitwizard#89 | ArgDigest >=0.14.0 is now required at runtime for configuration normalization; NumPy remains explicit. |
| TopoMT | runtime, tests, docs, guide | uibcdf/topomt#56 | Explicit NumPy and PyUnitWizard in project/recipe. |

Nine receiving owners are identified. PyUnitWizard's original test-tooling
relationship now includes its reviewed runtime use. Seven registered ArgDigest guide copies already match their
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

The initial pre-release candidate was
`13239a9d631799eb88ea7bed92f04eb3205b029d`; its notice and static-review scope
remain in the first receipt. The independently reviewed public checkpoint follows.

## Public delivery reconciliation — 2026-10-04

Numeric tag and public release 0.14.0 bind original producer
`0fa776af2d271065c60727c28480b20c3ce09aee`. The shared read-only operator at
central `482fa7351b8b2ec2e169d278fec250263345fc25` independently verifies
producer `37210475369`, full installed `37213239915` and the exact public
`noarch/argdigest-0.14.0-py_0.tar.bz2`, SHA-256
`983dca0f6bd0944d81fb1efc01e1dfa5c951e95abac6e7a0a08a13b7370d3b9e`.
The registry/index receipt reports `public-verified`, labels staging/main,
no next command and no mutation. The twelve installed cells execute all four
required install/resource/scientific-test/provenance steps. Administrative
qualification remains separately bound to
`be39e899f3b9fef2d4ce705799ae19770f41f769`; no original bytes are rebuilt.

Published GH Run Receptor 1.2.0 independently confirms the twelve source test
jobs in `37210325527`, all twelve minimal-core verification steps in
`37211211381`, promotion `37215001335`, and release-triggered `37214985408`
which skips rebuilding. The original failed build and Windows qualification
remain preserved under #92/#99/#100. Fresh public installation, deployed docs
and source-only Zenodo details retain their provider completion record;
this central slice does not rerun those checks or assert Conda archival.

All nine final public-release notices are delivered. At that earlier checkpoint,
reading every owner issue found no settled 0.14.0 receiving outcome. The
subsequent PyUnitWizard reconciliation below now supplies the first outcome. Ackredit
#72 and MolSysViewer #110 are closed historical governance reviews; that state
does not establish review of this newly published version. Their notice links
remain stable, and outstanding version-specific receiving work stays visible
in #98 until the owners supply an outcome and an active local home if needed.
No historical issue is reopened or scientific test schedule changed centrally.

Primary checkpoint: `devguide/rollouts/argdigest_014_public_review_98.json`.
The publisher inventory was refreshed through its existing observation tool
from fetched main references; caller strings are unchanged. Notice delivery,
source-guide inspection and exact public bytes remain separate from receiving
behavior. The issue originally stayed partial for nine owning outcomes. The receiving
checkpoint below now settles PyUnitWizard's outcome; eight remain pending.

## PyUnitWizard receiving reconciliation — 2026-10-04

uibcdf/pyunitwizard#89 supplies a concrete public-provider receiving outcome.
The central support-library review is now `adopted`, with developer-tool adoption
retained. Runtime configuration normalization uses ArgDigest's public `to_list`
in `load_library`, `set_standard_units` and `add_standard_units`; direct NumPy,
SMonitor and DepDigest requirements remain. The source graph now registers the
required runtime edge separately from its existing test-tooling edge.

Independent published GH Run Receptor 1.2.0 and native jobs/logs corroborate
matrix [37230868062](https://github.com/uibcdf/pyunitwizard/actions/runs/37230868062)
at `1a10ae9cca56b5766d09426e9964687771b6cb2a`: eight executed Linux/macOS
Python 3.11–3.14 cells, each importing public ArgDigest 0.14.0 and passing
686 tests with 22 documented skips. Two schedule-only jobs are skipped;
this review does not infer later skip-debt clearance. Corrected release profile
[37231437144](https://github.com/uibcdf/pyunitwizard/actions/runs/37231437144)
at `bd5be9e4853a3b3a8783618463ae3d641613f6c8` executes four full suites,
four 16-test smokes, packaging and documentation. Earlier profile failure
37230869147 remains owned by uibcdf/pyunitwizard#99, not overwritten.

Current inspected main `ef85201d619d2e50d4fd200a9196035d177f5a79` retains
the qualified runtime tree, receiving guards, metadata and CI/matrix inputs.
Optional Ackredit, sibling-source and strict-JSON skips remain explicit.
The owner-local installed pair used a development wheel with dirty-source and
system-site-packages limitations; it is neither a newly public PyUnitWizard
package nor a fresh isolated solver qualification. Published ArgDigest bytes
retain the independently qualified identity already recorded above.

The graph has no new required runtime cycle: ArgDigest's reverse PyUnitWizard
edge is optional. No optional edge becomes mandatory by inference. Central
reconciliation uses administrative/static inspection only, without importing
consumer runtime or dispatching scientific tests. Primary receipt:
`devguide/rollouts/pyunitwizard_argdigest_receiving_98_20261004.json`.

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
new common requirement. Public 0.14.0 is independently verified; that does not
automatically certify consumer adoption or change their version constraints.

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


## Owning-response refresh — 2026-10-05

A read-only refresh of all nine receiving issues confirms PyUnitWizard #89
is now closed by its owner, explicitly reconciling central commit
`4234be4a222846f189af290600a04c6162fde701` in
[the closure handoff](https://github.com/uibcdf/pyunitwizard/issues/89#issuecomment-5989296423).
The already recorded outcome remains adopted. The eight other issues supply
no additional version-specific receiving outcome at this checkpoint; historical
closed issue states remain insufficient. Counts stay one settled/eight pending.
No new consumer test, dependency change or scientific qualification is claimed.
