# Quantity boundary adoption

Baseline reviewed 2026-10-01 under uibcdf/molsyssuite#46 and uibcdf/molsyssuite#18;
provider MVP and owner closures reconciled 2026-10-05; public-provider availability
and the sixteen-member review routes refreshed 2026-10-22 below.
The shared [contract](../quantity_boundaries.md) governs applicability and
exceptions. Provider guidance, source adoption, scientific migration and public
installed compatibility are separate evidence claims.

## Shared baseline source inspection

All four `_pyunitwizard.py` bridges declare the same units and guard policy
initialization with `has_active_policy()`. This corrects the stale central claim
that PharmacophoreMT still configured the kernel unconditionally. Inspected:

| Member | Immutable source | Finding |
| --- | --- | --- |
| uibcdf/molsysmt | `97ab4789470a04aa83be6cc76d4676b2387426e5` | Shared baseline and protected initialization present. |
| uibcdf/molsysviewer | `deeb1d3db3d3041bf9a3714933f5e9a669516761` | Shared baseline and protected initialization present. |
| uibcdf/topomt | `793c3199689bd080356658ecb48e1be38f3c5e01` | Shared baseline and protected initialization present. |
| uibcdf/pharmacophoremt | `6a0221968536e440951b33d6021176245eff7c81` | Shared baseline and protected initialization present. |

The baseline is nm, ps, K, mole, dalton, e, kJ/mol, kJ/(mol*nm),
kJ/(mol*nm**2) and radians. Existing guards are
`tests/cross_repo/test_unit_policy_authority.py` in MolSysMT and MolSysViewer;
this review inspected their subprocess checks, not a complete installed/minor
matrix. Scientific suites were not rerun.

## Cases and provider maturity

| Owner | Current inspected state | Remaining ownership |
| --- | --- | --- |
| uibcdf/pyunitwizard#82 / uibcdf/pyunitwizard#83 | Closed for delivered homogeneous record/bundle MVP and design. Public 0.28.1 has separately qualified installed profiles; APIs and qrec/0.3 formats remain provisional. | Explicit stable promotion remains pending. HDF5/CF provider work is closed under uibcdf/pyunitwizard#101 / uibcdf/pyunitwizard#108; consumer migration is separate. |
| uibcdf/molsysmt#240 | Closed by its owner for legacy H5MSM unit declaration/read validation. Current published source retains unit validation and dedicated guards. This is not QuantityRecord codec adoption. | Future codec/schema migration and fresh-reader proof remain component-owned; the optional provider HDF5 capability is available under closed uibcdf/pyunitwizard#101. |
| uibcdf/molsysviewer#96 | Closed. Current `viewer/scene.py` extracts box lengths to angstrom; `annotations.py` extracts world offsets to nm. `tests/test_units_under_a_user_policy.py` exists. | Historical 10x failure is not a current unresolved defect. Follow-up uibcdf/molsysviewer#98 is also closed with component-reported guards; that report explicitly does not claim immutable release qualification. |
| uibcdf/molsyssuite#18 | Four bridge baselines agree in inspected source. | Complete output classification and installed/import-order evidence remain pending, not another configuration rewrite. |

The superseded `serialization_contract_draft.md` is historical, not the current
provider format. ArgDigest passports/value certification remain refuted prior
art; quantity records preserve explicit units without certifying mutable live
objects. Existing schema owners do not independently redesign this provider API.

## Delivered provider and receiving evidence — 2026-10-05

PyUnitWizard's owner-closed MVP/design/integrity issues #82/#83/#100 remain
separate from stable API or public-package admission. Qualified runtime
`fc062598fb968988acb493cd2e6ef2f2537c3423` has an independently inspected
eight-cell Linux/macOS Python 3.11–3.14 full matrix, 701 passed/14 skips per
cell, and successful release gates. Closure source
`426e2fd409d22adca757df163da8d67b01185499` has separate routine CI.
Owner-local installed development-wheel evidence uses mapped public providers
over existing scientific dependencies; it is not a fresh Conda solve.

| Receiving owner | Evidence and limit |
| --- | --- |
| uibcdf/sabueso#32 | Closed; owner-reported negotiated quantity columns, bundle verification and JSON/SQLite guards at `4b98b84`. No current installed public compatibility or whole suite is requalified centrally. |
| uibcdf/topomt#56 | Published sealed DFND input at `bfbd28f8c3d25a438c7b3d1e526097dd56f63d3c` has the recorded SHA-256 and exactly matches the provider's three copied records. Its owner-local canary reads under metre policy and converts explicitly to nm, refusing a wrong field. This is a bounded input boundary, not blanket TopoMT adoption or scientific algorithm qualification. |

The formats `qrec/0.3` and `qrec-bundle/0.3` stay provisional. At that early MVP
checkpoint the provider extensions #101–#106 and active OpenFF integration had
separate owners; the later completed HDF5/CF and publication handoffs are
reconciled below. Historical source qualification is not a new public install.
Unpublished work is not counted as delivered adoption.

Primary receipt:
`quantity_provider_reconciliation_46_20261005.json`.
Scientific/schema implementation and explicit provider promotion remain with
their owners; uibcdf/molsyssuite#46 stays partial for member adoption.

## Public provider and current owner review — 2026-10-22

PyUnitWizard uibcdf/pyunitwizard#101 and uibcdf/pyunitwizard#108 are closed for
optional `pyunitwizard.storage.hdf5.write/read` and bounded CF/UDUNITS tools.
The binding is a provisional whole-array `qrec-hdf5/0.1` snapshot over unchanged
`qrec/0.3` records. Readers declare field/unit/kind and explicit temperature
semantics; guards refuse changed values/units/metadata, dtype/shape changes,
missing manifests and raw appends. Append/streaming/crash/concurrent-writer
guarantees, full-CF/calendar validation and consumer schema migration are outside
that delivered scope. Tagged layout, Arrow/Parquet, Zarr, verified append and
translation-hub proposals remain open under uibcdf/pyunitwizard#102,
uibcdf/pyunitwizard#103, uibcdf/pyunitwizard#104, uibcdf/pyunitwizard#105 and
uibcdf/pyunitwizard#106.

Public availability is already independently reviewed under #45/#39:
`pyunitwizard-0.28.1-py_0.tar.bz2`, SHA-256
`d4654faf93ed4181bf331f7d382379e78f02784f71f678ad19d0ac43d8062cc6`,
original source `25a4bc2468da4ef3af2a638c0bf068becf2acfb4`, producer
37307676226 and installed qualification 37308199459. All thirty original
Linux/macOS arm64 installed cells retain their qualified closures: baseline,
storage and prepared profiles each cover Python 3.11–3.14; optional OpenFF has
six cells on 3.12–3.14. The earlier OpenFF waiting statement is superseded only
for that completed published handoff and its original closure. No future backend
qualification, new minimum or mandatory optional dependency follows.

Fresh inspection at provider `a2d7e38f6d8dc8f4072cc19b09a8cacddf77899a`
confirms the selected HDF5/CF APIs, guards and user-contract files match the
public candidate exactly. The original release receipt still matches its
previous central digest. The eight registered canonical-guide consumers match
the current provider bytes; this receiving needs no guide distribution.
Existing public/native evidence is reused, with no new solve, installation,
scientific test run or claim about current registry availability.

All fifteen existing member review issues were inspected; MolSys-AI's route is
this central issue. OpenCASTp adds the previously omitted sixteenth inventory
row, with owner applicability still pending and private issue metadata only.
Broad ecosystem closures do not establish new codec adoption. Current published
MolSysMT retains its legacy H5MSM resolver and tests; Viewer retains explicit
angstrom box/nanometer offset extraction and non-default/scalar-unit guards.
Those are inspected source facts, not newly executed suites or blanket output
classification. The earlier Sabueso/TopoMT bounded evidence retains its scope.

Receipt: [quantity_provider_refresh_46_20261022.json](quantity_provider_refresh_46_20261022.json).
Provider APIs/formats remain provisional, consumer acceptance remains separately
owned, and #46 remains partial. Scientific/Qt/early-development deferrals stay
in force.

## Member boundary inventory

Applicability below is a review route, not a claim that every member has a wire
format or needs an added runtime dependency. Existing ecosystem review issues
own detailed API evidence and can split concrete scientific/storage work locally.

| Member | Review route | Applicability / next evidence |
| --- | --- | --- |
| uibcdf/smonitor | uibcdf/smonitor#24 | No scientific quantity interchange identified in the utility/subsystem contract; record non-applicability unless a boundary is introduced. |
| uibcdf/argdigest | uibcdf/argdigest#20 | Optional unit-aware validation; no standalone scientific persistence format is inferred. |
| uibcdf/depdigest | uibcdf/depdigest#18 | No scientific quantity interchange identified in the utility/subsystem contract; record non-applicability unless a boundary is introduced. |
| uibcdf/pyunitwizard | uibcdf/pyunitwizard#89 | Provider of unit authority and codec; does not infer consumer adoption. |
| uibcdf/pytest-receptor | uibcdf/pytest-receptor#6 | No scientific quantity interchange identified in the utility/subsystem contract; record non-applicability unless a boundary is introduced. |
| uibcdf/gh-run-receptor | uibcdf/gh-run-receptor#55 | No scientific quantity interchange identified in the utility/subsystem contract; record non-applicability unless a boundary is introduced. |
| uibcdf/molsysmt | uibcdf/molsysmt#244 | Quantity-producing consumer; actual persistence/wire and public output classification review remains component-owned. |
| uibcdf/molsysviewer | uibcdf/molsysviewer#110 | Quantity-producing consumer; actual persistence/wire and public output classification review remains component-owned. |
| uibcdf/topomt | uibcdf/topomt#56 | Quantity-producing consumer; actual persistence/wire and public output classification review remains component-owned. |
| uibcdf/pharmacophoremt | uibcdf/pharmacophoremt#6 | Quantity-producing consumer; actual persistence/wire and public output classification review remains component-owned. |
| uibcdf/elastnetmt | uibcdf/elastnetmt#14 | Quantity-producing consumer; actual persistence/wire and public output classification review remains component-owned. |
| uibcdf/dockingmt | uibcdf/dockingmt#19 | Quantity-producing consumer; actual persistence/wire and public output classification review remains component-owned. |
| uibcdf/ackredit | uibcdf/ackredit#72 | No scientific quantity interchange identified in the utility/subsystem contract; record non-applicability unless a boundary is introduced. |
| uibcdf/lindelint | uibcdf/lindelint#9 | Quantity-producing consumer; actual persistence/wire and public output classification review remains component-owned. |
| uibcdf/molsys-ai | uibcdf/molsyssuite#46 | No scientific quantity interchange identified in the utility/subsystem contract; record non-applicability unless a boundary is introduced. |
| uibcdf/opencastp | uibcdf/opencastp#2 | Applicability and actual quantity boundaries remain owner-reviewed; no codec adoption or non-applicability is inferred. Private issue state only was refreshed centrally. |

## Completion boundary

The shared rules and registered guide route are delivered. None of the inventory
rows grants a blanket exception or claims a newly executed scientific gate. Future
applicable changes need their actual focused boundary guard and provider closure;
existing schema/provider constraints need reviewed member-owned exceptions with
owner, interim controls, expiry and removal condition. Internal direct pushes
retain the accepted lightweight CI route. Full scientific repairs remain local.
