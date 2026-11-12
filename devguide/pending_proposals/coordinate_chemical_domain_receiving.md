---
summary: Coordinate owner receiving of the independent ChemicalStates source model.
issue: uibcdf/molsyssuite#155
status: partial
opened: 2026-10-29
closed:
verification: measured
area: [compatibility, governance, molecular-modeling]
guard:
normative: devguide/cross_component_feedback.md
blocked_by: []
supersedes: []
---

# Independent chemical-domain receiving

**Reported:** MolSysMT's maintainer-approved pre-1.0 migration under #255.
**Status:** Provider integrated on main, with #531/#532 corrections independently
bound to successful smoke gates. DockingMT, PharmacophoreMT and Viewer source adoption
are received; TopoMT remains partial. Installed/public qualification remains
separately owned. Current observations are dated 2026-11-03.

## Central tooling-graph request resolved — 2026-11-04

DockingMT's explicit registry request in central #155 comment 6617667130 is
resolved. Published owner source `92d31e0bf6aaf128b79f8990732dbd5ac49b45e8`
declares and directly acquires ArgDigest, MolSysMT and MolSysViewer in both
the routine and full-matrix test jobs. All three are installed from their
explicit immutable checkouts with `--no-deps`; both minor-specific checkout
branches and the four source routes bind. The inspected current fetched source
retains those selected acquisition facts despite unrelated file changes.

The registry adds three direct `test-tooling` edges, including the requested
Viewer relationship. This records real test acquisition rather than transitive
closure or new public runtime requirements. Existing runtime edges, the Viewer
optional runtime `viewer` extra, default runtime query/layers and all non-graph
registry fields remain unchanged. The generated human graph is regenerated.
[Exact inputs, selected facts and controls](../rollouts/dockingmt_test_dependencies_155_20261104.json).

This central inventory correction is complete; no component implementation,
pin/floor update, scientific execution, matrix/public artifact qualification,
guide/policy change or developer response is requested. The broader #155 client
and installed/public scopes retain their owning teams and existing limits.

## What

Coordinate MolSysViewer, DockingMT, PharmacophoreMT and TopoMT receiving of
MolSysMT's independent ChemicalStates model. Topology retains stable inventory;
state-local bonds, assignments and components belong to ChemicalStates. Molecular
implementation stays with MolSysMT; visualization, docking, pharmacophore and
topography behavior stays with the respective client owners.

## How

MolSysMT #255 is closed and the refactor is integrated on main at
`00abb958fb93649131d5ce5fe5e12e90cf4900e9`. Central Git inspection confirms
identical objects for `molsysmt`, `rust`, `tests`, `pyproject.toml` and
`MANIFEST.in` against qualified development source
`de7ffad2aef18ff3bccd184133dc69e081cb506e`. This binds implementation inputs;
it does not relabel a private wheel producer or a development run as main.

Later closed owner corrections are #531 at
`0faf1584d05ac47ddcebfc20d9c9978b7f4f230e` (component-column dtype preservation)
and #532 at `2e5c8b64b7a2e4aa270c09b6311691cd88800ac2` (explicit typed-dictionary
domain composition). Both have independently verified successful exact-source
smoke gates and selected, statically addressable regression guards. Read the
provider's immutable [migration guide at #532](https://github.com/uibcdf/molsysmt/blob/2e5c8b64b7a2e4aa270c09b6311691cd88800ac2/devguide/chemical_states_migration.md)
and core specification instead of duplicating a changing provider contract here.
That guide is 9,073 bytes, SHA-256
`cf5db6f1e94ccf2063ad0a6355ff092aae2560d91eb0b76effab9b6992d07a0d`.
Each consumer's results remain bound to its own tested provider, rather than a
universal moving latest head.

Receive actual native/dictionary queries, state selection, unknown/absent/empty
domains, stable identity and maps, independent copies, controlled edits, units,
provenance and persistence through supported provider operations. Nine chemical
graph tools move to `chemical_states`; sequence operations remain in `topology`.
Latest TopologyDict/MolSysDict use 0.2; H5MSM remains 0.5. A text search or import
alone cannot qualify this migration. Preserve the original scientific assertions
and record the exact provider/consumer sources for each result.

## Why

Removing a Topology chemistry facade before receiving its clients breaks shared
molecular operations. Generic conformance or old public-package evidence cannot
establish source-cutover compatibility. Central coordination makes client
dispositions visible while their owners retain implementation and scientific review.

## Current owner inventory — 2026-11-03

| Owner | Received observation | Remaining owner action |
| --- | --- | --- |
| MolSysViewer #269, resolved | Provider `d8ea626a` receives original Windows/macOS `d72f93f7` (3,320 passes / 52 skips each) plus successful Linux `c1137ebb` (3,358 / 25). Original ZIP/JUnit digests and all five copy cases per host bind; native gates and unchanged-runtime reuse are independently verified. | Newer #291, addon/GUI #264 and future canonical installed/public/candidate gates remain independent. Original Linux failure is preserved; this is not a new single-SHA matrix. |
| DockingMT #56 / #47 / #60 | Earlier source adoption remains accepted. New private-addon checkpoint `9f8b787` preserves wheel producer `376679c`; six linked evidence files and 62 nongenerated payload hashes bind. Owner reports 1,430 complete private installed cases and five real-kernel cells on Linux/Python 3.14.8; selected producer CI jobs pass independently. | Complete producer/checkpoint hosted matrices and public/minimum/Conda/platform qualification remain #30/#47. Browser/C6 stay #60; original wheel/provider identities and warnings remain separate. |
| PharmacophoreMT #69, resolved | Candidate `7e5b5a5`/provider `0faf1584` has all eight native source test cells accepted. Seven original successes and the recovered macOS/3.14 execution are bound separately. Six tracked trees match code integration `76f43ffa` and main checkpoint `0485c176`; the guard/report closure is verified. Earlier 1,009 source records and 110 bounded local-wheel cases retain their limits. | #9 owns current/later main CI; candidate acceptance is not a new main-head execution. #23/#10 retain installed/public delivery. The XML accounting clarification has its independent open #71; source adoption stays accepted. |
| TopoMT #100 | The original bounded 81-pass owner result remains the latest receiving disposition. | Owning indirect/engine/persistence review remains; preserve early-maturity and coverage deferrals. No new full suite is imposed by this refresh. |

The [current separated receipt](../rollouts/chemical_domain_receiving_155_20261103.json)
retains exact commits, native gates, source objects and owner-report boundaries.
Central did not execute these component tests, rebuild wheels or alter pins.

Later same-day [source-adoption receiving](../rollouts/chemical_domain_pharmacophore_adoption_155_20261103.json)
updates PharmacophoreMT independently of that earlier pending observation.

### PharmacophoreMT evidence and recovery limits

The owner's main `53c15415` publishes a summary and compressed full receipt.
Central verifies both compressed/uncompressed lengths and SHA-256, all 39 embedded
text-file digests, the three actual JUnit case-record counts (4/1,009/110), all
22 original node identities and the four typed CCD nodes inside the full run.
All 56 listed test-file hashes match the exact consumer Git source. Before/after
consumer, provider-source/native and test manifests match; package metadata
lookups differ as disclosed. The inherited environment still has seven dependency
findings. The installed local wheel uses editable providers and does not qualify
a clean complete public/Conda environment.

The full JUnit XML declares `tests="1026"` at suite level but contains 1,009
actual passing case records. The owner's reported count matches those records;
the discrepancy remains explicit in open PharmacophoreMT #71 for owning clarification,
after #69 closes its source-adoption scope. No extra seventeen
passes, skips or failures are inferred, and full collection/completeness is not
independently certified from that counter.

Native attempt 1 of `41674239397` ends in failure with seven successful test jobs
and cancelled macOS arm64/Python 3.14 job `126050438777`, which has zero steps.
Its annotations explicitly report runner acquisition failure and macOS arm64
capacity constraints. GH Run Receptor retains the cancellation without assigning
a specific causal label; the native annotations provide the separate capacity
evidence. The initial receipt observes attempt 2 with seven successful cells and
the eighth queued. The later native receiving now accepts all eight required
cells. Original attempt-1 IDs and step execution timestamps bind the seven retained
successes to the inherited attempt-2 metadata; only macOS/Python 3.14 is a recovered
execution. It is not described as eight fresh runs. Central dispatches or retries
no suite. #9 owns current and subsequent main-head receiving.

### PharmacophoreMT source adoption accepted

Owner #69 is resolved with archived report and guard
`tests/test_chemical_domain_receiving.py`. Static inspection resolves its four
test functions; the actual candidate matrix includes the owner tests. Independent
native verification accepts required reporting and all eight Linux/macOS arm64
Python 3.11–3.14 test jobs, including dependency-route and interpreter/architecture
preflights. Attempt 2 of `41674239397` is successful. The cancelled attempt-1 cell
remains cancellation evidence, separately from its recovered successful execution.

Direct code integration `76f43ffa6663f4a3c85ef27c27d212d773d55442` and main
checkpoint `0485c176642b5adbef16f143cde259618c19f2f1` have exactly the candidate's
six tracked runtime/addon/support/test/tool/workflow trees. Their object IDs also
match the owner's published receipt. Generated Git versions and actual artifact
producers retain their own identities. The separate main CI `41688951342`, and
later product changes/heads, remain with #9; they are not relabeled as this source
candidate matrix. Installed Conda/public/platform acceptance remains #23/#10.

The XML suite-versus-case discrepancy has no owner explanation in the inspected
closed record. It is now an independent documentation follow-up,
[PharmacophoreMT #71](https://github.com/uibcdf/pharmacophoremt/issues/71), linked
to the unchanged published XML and earlier central checks. It requests an actual
accounting disposition from retained evidence; neither a new scientific suite nor
an unconfirmed provider diagnosis is imposed. #69's source acceptance remains
separate from this unresolved metadata clarification.

## Historical owner inventory — 2026-10-30

| Owner | Received observation | Remaining owner action |
| --- | --- | --- |
| MolSysViewer #269 | Owner publishes runtime `8aff97e` and fixture correction `ca7ebea`; local ordinary/addon receiving is reported. Exact later CI and source-pair runs fail. | Diagnose/correct or explicitly track hosted failures and return identified receiving evidence. |
| DockingMT #56 | Original owner source probe at `51b2232` against provider `9fb77c3` reports 27 failed / 7 passed; a scratch patch passes 24 selected cases. | Migrate four production graph calls, fixtures/snapshot schema and qualification routes; scratch work is not an owner-main correction. |
| PharmacophoreMT #69 | Pre-cutover 22-case old-provider baseline and target notice are recorded. | Receive SMARTS plus state/absence/component/axis/copy/codec boundaries on identified new sources. |
| TopoMT #100 | Original provider-owned source probe reports 81 passes without failures/errors/skips. | Review the bounded source result and identify any remaining engine/persistence/qualification scope. Early maturity and coverage deferral remain. |

Full identities, original comment references and separately measured native failure
metadata are retained in the [receiving inventory](../rollouts/chemical_domain_receiving_155_20261030.json).
Local scientific counts above are original owner reports, not new central executions.

## Initial native failure observations — 2026-10-30

Central coordination reads the exact migration blob, checks provider ancestry and
inspects current source/owner notices. GH Run Receptor and native stable-snapshot
acquisition independently confirm these terminal Viewer outcomes at
`ca7ebea60d530a7a0c65cb4d0ccea7b4288f3352`, attempt 1:

- CI `41138522008`: six Linux/macOS Python 3.12–3.14 jobs fail at `Run tests`;
  both 3.11 jobs pass and recovery/PR-only jobs skip.
- Source pair `41138522041`: all three Linux/macOS/Windows Python 3.14 jobs fail
  at `Run MolSysViewer Python tests`.

Those are verified failure boundaries, not a diagnosis. The existing local
development-provider/addon results retain their recorded sources and scope;
they do not establish hosted or installed/public success. The failures are
handed to Viewer #269 in comment `6535604196`. No central scientific run,
source installation, checkout/pin update or package operation was performed.

## What is measured and what is assumed — 2026-11-03

Central uses GH Run Receptor first, then stable native run/attempt/job acquisition
and required-step verification. Provider smoke `41670736932` binds #531 source
`0faf1584`; `41677348318` binds the separate #532 source `2e5c8b64`. Each required
native and bound-Viewer test step executes successfully. Owner-reported counts
and optional skips retain their scope; they are not independent central scientific
executions or a full platform/minor matrix.

DockingMT CI `41674495741` binds main `7870325c`, all four Linux Python
3.11–3.14 cells, quality/distribution jobs and actual measured coverage upload.
The immutable CI definition selects MolSysMT `00abb958` and Viewer `ca7ebea6`.
The separate private installed 1,381-pass result is an owning report, not a wheel
download or execution by central. Original wheel digests/producers remain fixed.
Successful upload does not claim processed Codecov percentage.

PharmacophoreMT's public compressed receiving is independently parsed and bound
as above. Original physical runtime execution, raw environment history and wheel
creation remain the owning team's evidence. Later successful candidate recovery,
the earlier cancelled attempt, main integration and its separate CI remain distinct. Primary clones, the shared
development environment and all #82 candidate prefixes are preserved.

## Alternatives and refuted paths

- Reintroducing a hidden Topology chemistry facade would reverse provider ownership.
- Namespace-only searches miss actual native/indirect consumers and do not replace receiving.
- Reusing an old public provider result does not qualify the identified development source.
- Local success cannot clear a later failed hosted matrix or qualify an installed artifact.

## Scope and exclusions

This issue owns cross-component source coordination. Provider/client scientific
fixes and tests remain local. No new compatibility floor, stable API, release,
platform admission or installed-package certificate is inferred.
Exact release/installed evidence stays in the existing component release owners.
Main integration is identified above; it is not a release or public compatibility
floor. The #82 installation/import cohort does not substitute for this scientific
contract receiving.
Primary branches, dirty work and the shared development prefix remain preserved.

## Acceptance criteria

- Identify the implemented provider source and its actual receiving specification.
- Receive explicit dispositions from all four client owners with exact sources,
  actual relevant checks and bounded remaining gaps/exceptions.
- Keep failure and deferred scientific/engine scopes with their owners; do not
  claim completed cutover or installed compatibility from source-only observations.
- Reconcile provider integration/final-gate state through MolSysMT #255 and retain
  installed/public qualification as a separate milestone.

## Local implementation issues

Provider: uibcdf/molsysmt#255. Clients: uibcdf/molsysviewer#269,
uibcdf/dockingmt#56, uibcdf/pharmacophoremt#69 and uibcdf/topomt#100.
MolSysMT #255 is closed with main integration identified. Its later #531/#532
fixes are also closed, with exact guards/source CI bound in the current receipt.
PharmacophoreMT #69 is source-resolved; #9 owns current main CI and #71 the open
XML accounting clarification. Public/installed boundaries remain in the clients'
existing distribution and release issues.

## Dependencies and risks

Providers and clients are under active development; a new source result needs its
own identities and controls. Preserve units, scientific definitions, state/structure
associations, unknown membership, stable maps and original qualified artifacts.
Generic policy or source probes cannot clear pending scientific or release evidence.

## Provenance

Initial review: 2026-10-30, named Linux Python 3.14.7 environment. Public immutable source blobs,
GitHub owner issues and native Actions run/attempt/jobs/steps were read; no scientific
suite was dispatched or replayed. The maintained JSON separates inspected source,
original owner execution and independently acquired native failure evidence.

Current refresh: 2026-11-03, named Linux Python 3.14.7 administrative interpreter;
the qualified isolated GHR installation is used for read-only reception. Public
Git objects, owning issue reports, compressed receipt/XML and native Actions
snapshots are inspected without new component test execution. The initial
`9fb77c3` migration guide (7,441 bytes, SHA-256
`c9a7dc076e78a97ee289e96d3effaf0ab69e4839ecc8aab5a75de5ee07426f23`)
and the October receipt retain their original historical scope.

## DockingMT private installed-addon receiving — 2026-11-03

A later bounded owner handoff under #47/#60 publishes `9f8b787213bf699c99eb2d6b37ede89769921315`.
The original private wheel producer is `376679c2fe77298eda7a80edd311335c2cfa205b`,
SHA-256 `aa5626e1ee7073a2df32fdce75cf10c132eeedffc807aa71a5421d1a55a9391e`.
Its six linked public evidence inputs bind by size/digest; all 62 nongenerated
reported payload hashes match producer Git objects. Runtime, addon, tests and
project metadata objects match the documentation checkpoint. Private wheel bytes,
raw execution outputs and installed filesystem were not acquired centrally.

Owner evidence reports normal non-editable Linux x86_64/Python 3.14.8 installation,
clean closure before/after **1,430 passing cases**, no failures/errors/skips,
63 unchanged installed payload files and 2,622 prefix-owned loaded modules.
Original MolSysMT `de7ffad2`, Viewer `ca7ebea6` and ArgDigest `3d1ec53` wheel
identities stay fixed. OpenMM 8.6.1 uses the explicitly recorded public wheel
variant, not the earlier Conda binary closure. The 328 unit-test warnings remain.

The companion's four later code cells exactly match the frozen source notebook;
its first cell checks ordinary-install/origin/provenance. The owner reports five
real-kernel cells, five frames/2,033 atoms, unchanged 33 original files, explicit
one-receptor/two-ligand preparation replay, and nine composition warnings. Zero
new search/map/energy/optimization/RMSD counts apply only to that notebook.
Neither rendered pixels/browser controls nor C6 is accepted. Maintainer interaction
remains deferred; provider follow-ups remain Viewer #291 and MolSysMT #521.

GHR first inspection and independent native identity/job/step checks verify
producer run 41699697539's quality, distribution and Linux 3.11/3.14 jobs. The
whole run still has 3.12/3.13 work in progress at inspection; new checkpoint CI
41708278656, policy 41708279096 and publication guard 41708279241 are queued.
No whole-matrix success is inferred. Current component owners track terminal
recovery, exact public dependencies/Conda/archive/platform admission and frontend
acceptance. Resource review is #50, 2026-11-10, under central #104.

This receives a bounded installed owner result alongside accepted source adoption;
it does not close #155, replace the earlier 1,381-case receipt, qualify public
bytes or dispatch science. [Separated receipt](../rollouts/docking_private_addon_receiving_155_45_20261103.json).

## MolSysViewer source adoption received — 2026-11-03

Closed owner #269 publishes `e7f7d55c6c1821fbaa9887785469335a1367ed03`.
Exact provider `d8ea626a0ab6dbd976d0e04ad9299019e4ae0a42` includes export repair
`2797c5425f5735568422325928520ae591c3676a`. GHR first inspection and independent
native verification bind original run 41690488611 and successful Linux recovery
41714550124, both workflow-dispatch attempt 1. Required original Windows/macOS
installation/audit/Rust/integration/Python/upload steps pass. Complete Linux
recovery also passes its scope, browser and notebook steps.

Four original/recovery ZIP digests and exact JUnit bytes match. Actual case
records give original Linux 3,347 passes / 25 skips, Windows/macOS 3,320 / 52 each,
and recovery Linux 3,358 / 25. All five copy controls execute without skip/failure
on each host. Original Linux remains failed in its browser fixture. Runtime is
unchanged between original `d72f93f7` and recovery `c1137ebb`; the sole package-path
delta declares the positive context-menu fixture's real chain membership. Loader/
copy guard bytes remain identical. The original recovery job log's SHA-256 also
matches, retaining its 14 Qt deselections, 102 installed Rust exports, minimum
image 2.5, three native-path/two integration checks, 44 core browser suites and
25 notebooks. Raw logs are not republished.

Successful original hosts are reused within that unchanged-runtime scope, not
relabeled as new executions at the recovery SHA. The original browser failure
and cancelled superseded recovery 41707479800 retain their conclusions. Earlier
pending fields in the owner receipt are superseded by its resolution/recovery.

Viewer joins DockingMT and PharmacophoreMT in source receiving; TopoMT #100
retains indirect-contract work and approved early-development deferrals. Newer
Viewer #291, #264 addon/GUI and canonical candidate/installed/public gates remain
separate. No new minimum, publication, scientific rerun, component edit or #82
switch occurs. [Independent receiving](../rollouts/viewer_chemical_source_receiving_155_20261103.json).

## Third-batch receiving — 2026-11-12

The original typed dependency correction at `0216c7d7158bed9762c37ec0d9b812ebbf70a040` now has independently verified native gate 41906939436, both jobs and required steps, recovering the former queued observation. The provider and three bounded client source dispositions retain their existing receipts. TopoMT #100 remains open with no completed owner receiving added; #155 stays partial. BindingMT #56 broader installed/public boundaries and original private/source-only artifacts remain separately owned. No registry edge, scientific kernel, dependency pin or source package is changed.

[Source/owner receiving](../rollouts/third_ten_receiving_20261112.json) and [original native proof](../rollouts/third_ten_native_20261112.json) retain identities and limits. Primary/human work, #82 pause and other explicit scientific/early-development deferrals remain preserved.
