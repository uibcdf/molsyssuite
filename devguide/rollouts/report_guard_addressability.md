# Report guard addressability rollout

**Issue:** `uibcdf/molsyssuite#26`

**Policy:** `devguide/reporting_protocol.md`

**Started:** 2026-09-19

**Status:** Completed on 2026-09-20.

## Scope

This rollout applies the shared `guard` contract to the six stabilization wave-1
members: SMonitor, ArgDigest, DepDigest, PyUnitWizard, MolSysMT and MolSysViewer.
Infrastructure, auxiliary and incubating repositories remain governed by the common
semantic rule, but do not define completion of this rollout.

## Acceptance

For reports resolved on or after 2026-09-20, the default Python profile accepts one safe
pytest module, function or class-method selector under `tests/` or `devtools/tests/`.
Validators reject missing files, missing nodes, parameter IDs, unsafe paths, globs,
comma-separated targets and command text. Historical records are not invalidated.

The mechanical check proves addressability only. The closing report must explain why the
selected assertion protects the reported failure mechanism; reviewers remain responsible
for that relevance judgement. A non-pytest guard first needs a bounded local profile that
fixes its runner, roots, syntax and resolution check.

## Adoption matrix

| Member | State | Local issue | Commit | Local guard |
| --- | --- | --- | --- | --- |
| smonitor | adopted | `uibcdf/smonitor#15` | `e39d070` | `tests/test_devguide_reports.py` |
| argdigest | adopted | `uibcdf/argdigest#12` | `cb5349e` | `tests/test_reporting_protocol.py` |
| depdigest | adopted | `uibcdf/depdigest#12` | `30a4671` | `tests/test_reporting_protocol.py` |
| pyunitwizard | adopted | `uibcdf/pyunitwizard#75` | `d0c688d` | `tests/test_reporting_protocol.py` |
| molsysmt | adopted | `uibcdf/molsysmt#197` | `05d0a3b37` | `devtools/tests/test_validate_devguide.py::test_a_guard_with_a_missing_node_is_refused` |
| molsysviewer | adopted | `uibcdf/molsysviewer#90` | `5c7537dc` | `tests/test_reporting_protocol.py` |

Every issue is closed with its implementation and verification evidence. MolSysMT's
report is archived because it owned the originating defect; the other local issues were
bounded adoption tasks and did not create duplicate devguide reports.

## Verification

Each repository passed its focused reporting-protocol suite, Ruff lint, Ruff formatting
check and `git diff --check` before publication. MolSysMT additionally passed
`python devtools/scripts/validate_devguide.py`. Central conformance passed 64 tests before
the member rollout began and is rerun when this record closes.

The synchronized `MOLSYSSUITE_GUIDE.md` in each wave-1 commit carries the prospective
date, safe selector forms, historical policy and addressability-versus-relevance boundary.
This rollout records semantic adoption; it does not claim that automation can establish
causal relevance.
