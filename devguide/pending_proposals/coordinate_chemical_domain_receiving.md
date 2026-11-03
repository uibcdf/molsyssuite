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
bound to successful smoke gates. Client source receiving is mixed; PharmacophoreMT
has an owning CI recovery in progress. Installed/public qualification remains
separately owned. Current observations are dated 2026-11-03.

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
| MolSysViewer #269 | Adapted `ca7ebea6` has owner-reported ordinary/addon source receiving. The provider's verified #531/#532 smoke executes its bound addon tier at that Viewer pin. | Return the disposition of current complete ordinary/source-pair routes and their earlier failed runs. A bound provider addon tier is not a full Viewer or installed/public certificate. |
| DockingMT #56 | Main-source checkpoint `7870325c` selects provider `00abb958`. All seven exact CI jobs and required source/ordinary-install/context/closure/test/upload steps pass; owner reports 1,381 passes per Linux minor and a new complete private Linux/3.14 installed result of 1,381 passes. | Public package/minimum and complete installed/platform qualification remain #30/#47. Preserve the private wheels' original producers and earlier failed/narrow installed history. |
| PharmacophoreMT #69 | Consumer `7e5b5a5` against provider `0faf1584` publishes 1,009 passing source case records and 110 installed local-wheel cases. Digest/XML/source checks bind the 22 original controls and all four unchanged typed CCD cases. #531 no longer blocks it. | #9 owns the eight-cell source matrix recovery and subsequent deliberate main integration. Attempt 1 has seven passing test jobs and a zero-step capacity cancellation; attempt 2 retains seven successful cells and queues the eighth at observation. #23/#10 retain installed/public delivery. Clarify the XML counter discrepancy below. |
| TopoMT #100 | The original bounded 81-pass owner result remains the latest receiving disposition. | Owning indirect/engine/persistence review remains; preserve early-maturity and coverage deferrals. No new full suite is imposed by this refresh. |

The [current separated receipt](../rollouts/chemical_domain_receiving_155_20261103.json)
retains exact commits, native gates, source objects and owner-report boundaries.
Central did not execute these component tests, rebuild wheels or alter pins.

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
the discrepancy remains explicit for owning clarification. No extra seventeen
passes, skips or failures are inferred, and full collection/completeness is not
independently certified from that counter.

Native attempt 1 of `41674239397` ends in failure with seven successful test jobs
and cancelled macOS arm64/Python 3.14 job `126050438777`, which has zero steps.
Its annotations explicitly report runner acquisition failure and macOS arm64
capacity constraints. GH Run Receptor retains the cancellation without assigning
a specific causal label; the native annotations provide the separate capacity
evidence. The owner's attempt 2 is observed at the same source, with seven
successful cell records and macOS/Python 3.14 queued. This is not eight-cell
acceptance. Central does not dispatch, cancel, retry or integrate its scientific
work; #9 owns recovery.

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
creation remain the owning team's evidence. Its new pending native attempt and
the earlier cancelled attempt remain distinct. Primary clones, the shared
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
PharmacophoreMT #9 owns current CI recovery; public/installed boundaries remain
in the clients' existing distribution and release issues.

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
