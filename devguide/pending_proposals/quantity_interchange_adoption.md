---
summary: Route quantity interchange to PyUnitWizard and track actual member adoption.
issue: uibcdf/molsyssuite#46
status: partial
opened: 2026-09-24
closed:
verification: measured
area: [units, compatibility, governance]
guard:
normative:
blocked_by: []
supersedes: []
---

# Quantity interchange adoption

## What

One provider owns quantity interchange: uibcdf/pyunitwizard#83 (design) and
uibcdf/pyunitwizard#82 (implementation). Members retain scientific schema ownership.

## How

The common contract is `devguide/quantity_boundaries.md`. It requires explicit
units at interchange boundaries, a real non-default-policy regression, explicit
conversion for fixed-unit wire protocols and reviewed bounded exceptions.
The registered PyUnitWizard guide already documents the provisional record API;
do not copy the superseded serialization draft or invent new supported names.

## Why

Unit policy cannot determine how an independent reader interprets an unlabelled
magnitude. A frontend/file assuming nanometers can misread a user angstrom policy.
The historical Viewer failure is resolved locally. MolSysMT #240 is also closed
for legacy H5MSM unit validation; it is not codec adoption. Future HDF5 binding
belongs to uibcdf/pyunitwizard#101 and scientific schema decisions to consumers.
See `devguide/rollouts/quantity_boundaries.md` for evidence and remaining ownership.

## What was refuted

Guide delivery does not establish codec adoption. A provisional provider API does
not authorize ambiguous numbers. This work does not restore ArgDigest passports
or value certification, or turn a client schema into a shared quantity format.

## Scope and exclusions

Shared governance, routing, applicability and evidence inventory. Provider API
promotion and scientific storage/frontend migrations stay with their teams.

## Acceptance criteria

- Canonical guidance routes design and implementation to the provider.
- Applicable members own non-default-policy guards at their actual boundaries.
- Codec/provider compatibility, schema migration and public claims are evidenced
  per member, or carry a reviewed exception preserving unit integrity.
- Inventory distinguishes resolved cases from outstanding migration and API work.

Current state: shared rules and routing delivered; complete member adoption and
provider promotion remain pending. Do not close this coordinated adoption issue
merely because the guide is synchronized.

Delivered 2026-10-01: the common boundary summary was synchronized and pushed
to all 15 registered members; all registered guide copies match their sources.
Offline governance passed. This delivery does not close outstanding member
scientific migrations or promote the provisional provider API.


## Delivered MVP reconciliation — 2026-10-05

PyUnitWizard #82/#83 resolve the homogeneous QuantityRecord/Bundle MVP and
design record at `426e2fd409d22adca757df163da8d67b01185499`; #100 resolves
write reactivation behind the seal at runtime source
`fc062598fb968988acb493cd2e6ef2f2537c3423`. The source-qualified full matrix
37237982579 executes eight Linux/macOS Python 3.11–3.14 cells with **701
passed/14 skips each**, independently confirmed through native logs. Release
gates 37237984869 execute six successful jobs; the archival-source routine CI
37238940812 passes separately. The owner-local 706/12 result, normally
installed development wheel's 63/1 record selection and three later consumer
canaries retain their distinct scopes; no fresh solve or public package is
inferred from mapped scientific dependencies or source-wheel qualification.

The provider's frozen-vector, tamper and write-reactivation guards are
addressable and relevant by inspection. Original TopoMT sealed DFND input at
`bfbd28f8c3d25a438c7b3d1e526097dd56f63d3c` matches its recorded digest and
the provider's three copied records exactly. The owning canary reads them
under metre policy with explicit angstrom-to-nanometre conversion and refuses
a wrong field. This does not qualify TopoMT algorithms. Closed Sabueso #32
retains its owner-reported negotiated-column/bundle receiving evidence.

MolSysMT #240 is corrected in the central inventory: its team closed legacy
H5MSM declaration/read validation, not adoption of this codec. HDF5/CF binding,
tagged records, Arrow/Parquet, Zarr, verified appends and translation-hub work
have independent provider owners #101–#106. No consumer source or scientific
suite is changed by this reconciliation.

**QuantityRecord/Bundle and qrec/0.3 formats remain provisional** under the
provider's explicit maturity decision. Implementation closure does not mean
stable promotion, a new public artifact or full member adoption. The principal
maintainer reports active OpenFF integration; central review of that integration
is deferred until its team's completed handoff. Earlier snapshots are not
current adoption certification. #46 stays partial for actual member adoption
and explicit provider promotion.

Receipt: `devguide/rollouts/quantity_provider_reconciliation_46_20261005.json`.
Inspected provider snapshot: `a8120de403f1c2742bbe68257eaf3adae54f6a92`.
Canonical guide distribution remains separate; no new component dependency,
mandatory optional backend, format promotion or scientific execution follows.
