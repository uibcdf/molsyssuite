# Quantity boundary adoption

Reviewed 2026-10-01 under uibcdf/molsyssuite#46 and uibcdf/molsyssuite#18.
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
| uibcdf/pyunitwizard#82 / uibcdf/pyunitwizard#83 | Record form and `QuantityRecord`/bundle exist; canonical guide marks API provisional. | Provider API promotion, HDF5 binding and published compatibility remain provider-owned. |
| uibcdf/molsysmt#240 | H5MSM quantity layout/reader migration remains open. | Component team owns scientific schema and migration, non-default policy and fresh-reader proof. |
| uibcdf/molsysviewer#96 | Closed. Current `viewer/scene.py` extracts box lengths to angstrom; `annotations.py` extracts world offsets to nm. `tests/test_units_under_a_user_policy.py` exists. | Historical 10x failure is not a current unresolved defect. Follow-up uibcdf/molsysviewer#98 is also closed with component-reported guards; that report explicitly does not claim immutable release qualification. |
| uibcdf/molsyssuite#18 | Four bridge baselines agree in inspected source. | Complete output classification and installed/import-order evidence remain pending, not another configuration rewrite. |

The superseded `serialization_contract_draft.md` is historical, not the current
provider format. ArgDigest passports/value certification remain refuted prior
art; quantity records preserve explicit units without certifying mutable live
objects. Existing schema owners do not independently redesign this provider API.

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
