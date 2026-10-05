# Quantity boundary adoption

Baseline reviewed 2026-10-01 under uibcdf/molsyssuite#46 and uibcdf/molsyssuite#18;
provider MVP and owner closures reconciled 2026-10-05 below.
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
| uibcdf/pyunitwizard#82 / uibcdf/pyunitwizard#83 | Closed for delivered homogeneous record/bundle MVP and design. APIs and qrec/0.3 formats remain provisional. | Explicit provider promotion and new public compatibility remain pending; HDF5 binding has separate owner uibcdf/pyunitwizard#101. |
| uibcdf/molsysmt#240 | Closed by its owner for legacy H5MSM unit declaration/read validation. This is not QuantityRecord codec adoption. | Future codec/schema migration and fresh-reader proof remain component-owned; provider HDF5 capability is uibcdf/pyunitwizard#101. |
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

The formats `qrec/0.3` and `qrec-bundle/0.3` stay provisional. Deferred provider
extensions have owning issues #101–#106, including #101 for HDF5/CF binding.
The principal maintainer reports that OpenFF integration is active; central
review waits for its team's completed handoff. This reconciliation does not
certify that integration, force an optional dependency or distribute a new guide.
Unpublished PharmacophoreMT work is not counted as delivered adoption.

Primary receipt:
`quantity_provider_reconciliation_46_20261005.json`.
Scientific/schema implementation and explicit provider promotion remain with
their owners; uibcdf/molsyssuite#46 stays partial for member adoption.

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

## Completion boundary

The shared rules and registered guide route are delivered. None of the inventory
rows grants a blanket exception or claims a newly executed scientific gate. Future
applicable changes need their actual focused boundary guard and provider closure;
existing schema/provider constraints need reviewed member-owned exceptions with
owner, interim controls, expiry and removal condition. Internal direct pushes
retain the accepted lightweight CI route. Full scientific repairs remain local.
