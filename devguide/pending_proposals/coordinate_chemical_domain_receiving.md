---
summary: Coordinate owner receiving of the independent ChemicalStates source model.
issue: uibcdf/molsyssuite#155
status: partial
opened: 2026-10-29
closed:
verification: inspected
area: [compatibility, governance, molecular-modeling]
guard:
normative: devguide/cross_component_feedback.md
blocked_by: []
supersedes: []
---

# Independent chemical-domain receiving

**Reported:** MolSysMT's maintainer-approved pre-1.0 migration under #255.
**Status:** Development implementation identified; client source receiving is mixed
and installed/public qualification remains separately owned.

## What

Coordinate MolSysViewer, DockingMT, PharmacophoreMT and TopoMT receiving of
MolSysMT's independent ChemicalStates model. Topology retains stable inventory;
state-local bonds, assignments and components belong to ChemicalStates. Molecular
implementation stays with MolSysMT; visualization, docking, pharmacophore and
topography behavior stays with the respective client owners.

## How

The provider's coherent implementation is `7b983af32ac4efcc3adb7c4c0617a38957ecc41e`
on `dev/chemical-states-separation-255`. The later inspected checkpoint
`9fb77c3583b44dda31c0466348369de137301df9` is three commits ahead, with explicit
runtime, test and documentation corrections. Read the provider's immutable
[migration guide](https://github.com/uibcdf/molsysmt/blob/9fb77c3583b44dda31c0466348369de137301df9/devguide/chemical_states_migration.md)
and core specification instead of duplicating a changing provider specification here.
The downloaded guide is 7,441 bytes, SHA-256
`c9a7dc076e78a97ee289e96d3effaf0ab69e4839ecc8aab5a75de5ee07426f23`.

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

## Current owner inventory — 2026-10-30

| Owner | Received observation | Remaining owner action |
| --- | --- | --- |
| MolSysViewer #269 | Owner publishes runtime `8aff97e` and fixture correction `ca7ebea`; local ordinary/addon receiving is reported. Exact later CI and source-pair runs fail. | Diagnose/correct or explicitly track hosted failures and return identified receiving evidence. |
| DockingMT #56 | Original owner source probe at `51b2232` against provider `9fb77c3` reports 27 failed / 7 passed; a scratch patch passes 24 selected cases. | Migrate four production graph calls, fixtures/snapshot schema and qualification routes; scratch work is not an owner-main correction. |
| PharmacophoreMT #69 | Pre-cutover 22-case old-provider baseline and target notice are recorded. | Receive SMARTS plus state/absence/component/axis/copy/codec boundaries on identified new sources. |
| TopoMT #100 | Original provider-owned source probe reports 81 passes without failures/errors/skips. | Review the bounded source result and identify any remaining engine/persistence/qualification scope. Early maturity and coverage deferral remain. |

Full identities, original comment references and separately measured native failure
metadata are retained in the [receiving inventory](../rollouts/chemical_domain_receiving_155_20261030.json).
Local scientific counts above are original owner reports, not new central executions.

## What is measured and what is assumed

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

## Alternatives and refuted paths

- Reintroducing a hidden Topology chemistry facade would reverse provider ownership.
- Namespace-only searches miss actual native/indirect consumers and do not replace receiving.
- Reusing an old public provider result does not qualify the identified development source.
- Local success cannot clear a later failed hosted matrix or qualify an installed artifact.

## Scope and exclusions

This issue owns cross-component source coordination. Provider/client scientific
fixes and tests remain local. No new compatibility floor, stable API, main
integration, release, platform admission or installed-package certificate is inferred.
Exact release/installed evidence stays in the existing component release owners.
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
MolSysMT #255's original issue text still says post-1.0; its owner should reconcile
that historical text with the maintainer-approved pre-1.0 implementation record.

## Dependencies and risks

Providers and clients are under active development; a new source result needs its
own identities and controls. Preserve units, scientific definitions, state/structure
associations, unknown membership, stable maps and original qualified artifacts.
Generic policy or source probes cannot clear pending scientific or release evidence.

## Provenance

2026-10-30, named Linux Python 3.14.7 environment. Public immutable source blobs,
GitHub owner issues and native Actions run/attempt/jobs/steps were read; no scientific
suite was dispatched or replayed. The maintained JSON separates inspected source,
original owner execution and independently acquired native failure evidence.
