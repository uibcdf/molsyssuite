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
for legacy H5MSM unit validation; it is not codec adoption. The optional HDF5
provider binding is delivered under closed uibcdf/pyunitwizard#101; scientific
schema decisions and actual migration remain with consumers.
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

## Public provider availability reconciled — 2026-10-22

Live provider issues uibcdf/pyunitwizard#101 and uibcdf/pyunitwizard#108 are
closed for provisional verified HDF5 snapshots and bounded CF physical-unit tools. The new binding is
`qrec-hdf5/0.1`, over unchanged qrec/0.3 records; it requires reader expectations
and explicit temperature meaning and refuses raw edits, missing/conflicting
metadata and appends. It does not deliver streaming/appends, crash recovery,
full-CF/calendar conformance or a MolSysMT H5MSM migration. Independent
extensions uibcdf/pyunitwizard#102, uibcdf/pyunitwizard#103,
uibcdf/pyunitwizard#104, uibcdf/pyunitwizard#105 and uibcdf/pyunitwizard#106 remain open.

Completed publication uibcdf/pyunitwizard#112 and existing independent #45/#39
receipts qualify original public 0.28.1 source `25a4bc2468da4ef3af2a638c0bf068becf2acfb4`,
archive SHA-256 `d4654faf93ed4181bf331f7d382379e78f02784f71f678ad19d0ac43d8062cc6`
and thirty original installed cells: baseline/storage/prepared each on
Linux/macOS arm64 Python 3.11–3.14, OpenFF on 3.12–3.14. Fresh source inspection
confirms selected API/test/user-contract bytes and the original release receipt
retain their qualified identities. This reuses evidence; no science or public
installation was repeated. The previous OpenFF waiting statement no longer
applies to that completed published profile, while future integration remains
separately owned. Publication does not promote provisional APIs or formats.

All existing owner review homes and specific legacy/Viewer/Sabueso cases were
refreshed. No new broad codec-acceptance claim follows from ecosystem issue
closure. MolSysMT's published source retains legacy unit validation; Viewer's
published source retains explicit fixed-unit conversions and relevant guards.
The inventory now includes all sixteen registered members, adding the missing
OpenCASTp route with applicability pending and private issue metadata only.
All eight registered PyUnitWizard guide copies match their canonical source.

The [normalized receipt](../rollouts/quantity_provider_refresh_46_20261022.json)
retains source/blob/hash bindings, existing native/public proof provenance,
guard addressability by inspection, owner states and limits. No canonical
contract, guide distribution, registry/adoption state, dependency floor,
workflow/pin, scientific suite or package operation changes. #46 remains partial
for actual member boundary adoption and explicit provider promotion. Existing
scientific, early-maturity and Qt waiting decisions remain unchanged.


## Public 0.29.0 receiving — 2026-10-30

The version-specific central reception #132 independently verifies the original
0.29.0 source, separate qualifier, six source/control profiles, thirty installed
cells plus producer verification, exact native binding artifact and unchanged
public Conda bytes, title/tag/source and publication/docs steps. The six profiles
contain 29 source/release jobs plus policy conformance. All eight registered
canonical guide copies already match the published hash; no redistribution or
new client minimum is needed. The inspected current direct/optional declarations
retain owner-controlled bounds; they do not certify execution of an affected path.

This supersedes the dated pending-provider/public-0.28.1 statements above for
#102–#106 and #125–#127. Their source delivery and 0.29.0 publication do not
promote provisional record/storage/dialect APIs or scientific schemas. The four
translator corrections in central #127 are included in the release source;
nine registered candidate consumers received scoped owner handoffs. #127 stays
partial for actual affected-path dispositions. No broad scientific matrix,
consumer migration, dependency-floor change or stable-API decision is made here.

[Receiving receipt](../rollouts/pyunitwizard_0_29_0_receiving_132_20261030.json)
and [translator handoffs](../rollouts/pyunitwizard_translator_handoffs_127_20261030.json).
PeptideMT is now the seventeenth registered member; its quantity applicability
follows its own review under uibcdf/peptidemt#6, not the historical sixteen-member
inventory. The guide and actual scientific boundaries remain separate evidence.
