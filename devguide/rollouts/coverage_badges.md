# Coverage badge adoption

Central ownership: uibcdf/molsyssuite#69. Normative rules: [repository_badges.md](../repository_badges.md#coverage-percentage-applicability-and-cadence).

## Measured inventory (2026-10-01)

All fifteen registered members and the suite root are included. GitHub confirms
`main` as each default branch. Exact inspected source SHAs, complete report SHAs,
commit timestamps, Codecov cache states and actual upload times/runs are retained
in [coverage_badges.json](coverage_badges.json). Percentages below are dated
measurements; README badges render the service dynamically. No test suite was
launched for this review. Backup workflows are excluded from active producers.

| Repository | Complete report observed | Native upload evidence | README / owned action |
| --- | --- | --- | --- |
| uibcdf/smonitor | 78.38% · `2e03716a94a3` | [36539959586](https://github.com/uibcdf/smonitor/actions/runs/36539959586) | existing live badge; cadence explanation pending; [uibcdf/molsyssuite#69](https://github.com/uibcdf/molsyssuite/issues/69) |
| uibcdf/argdigest | 92.53% · `6223e0124fcc` | [36640865049](https://github.com/uibcdf/argdigest/actions/runs/36640865049) | existing live badge; cadence explanation pending; [uibcdf/molsyssuite#69](https://github.com/uibcdf/molsyssuite/issues/69) |
| uibcdf/depdigest | 93.27% · `0da46d9ff31f` | [36788753059](https://github.com/uibcdf/depdigest/actions/runs/36788753059) | existing live badge; cadence explanation pending; [uibcdf/molsyssuite#69](https://github.com/uibcdf/molsyssuite/issues/69) |
| uibcdf/pyunitwizard | 90.23% · `c9f572c5061a` | [36538121889](https://github.com/uibcdf/pyunitwizard/actions/runs/36538121889) | existing live badge; cadence explanation pending; [uibcdf/molsyssuite#69](https://github.com/uibcdf/molsyssuite/issues/69) |
| uibcdf/pytest-receptor | No usable completed report observed | Unavailable / not observed | producer/evidence adoption pending; [uibcdf/pytest-receptor#12](https://github.com/uibcdf/pytest-receptor/issues/12) |
| uibcdf/gh-run-receptor | No usable completed report observed | Unavailable / not observed | producer/evidence adoption pending; [uibcdf/gh-run-receptor#57](https://github.com/uibcdf/gh-run-receptor/issues/57) |
| uibcdf/molsysmt | 78.79% · `b6c0e4f2a15e` | Unavailable / not observed | stale March evidence; maintainer-approved deferral; keep badge absent; [uibcdf/molsysmt#286](https://github.com/uibcdf/molsysmt/issues/286) |
| uibcdf/molsysviewer | 75.81% · `ca6a3cda9eef` | [36926313560](https://github.com/uibcdf/molsysviewer/actions/runs/36926313560) | recent report; README badge restoration pending; [uibcdf/molsyssuite#69](https://github.com/uibcdf/molsyssuite/issues/69) |
| uibcdf/topomt | No usable completed report observed | Unavailable / not observed | producer/evidence adoption pending; [uibcdf/topomt#81](https://github.com/uibcdf/topomt/issues/81) |
| uibcdf/pharmacophoremt | 38.99% · `98ecb459348a` | [36457546833](https://github.com/uibcdf/pharmacophoremt/actions/runs/36457546833), [36357376234](https://github.com/uibcdf/pharmacophoremt/actions/runs/36357376234) | recent report; README badge restoration pending; [uibcdf/molsyssuite#69](https://github.com/uibcdf/molsyssuite/issues/69) |
| uibcdf/elastnetmt | 60.97% · `956670796957` | [36459131786](https://github.com/uibcdf/elastnetmt/actions/runs/36459131786), [36357927495](https://github.com/uibcdf/elastnetmt/actions/runs/36357927495) | recent report; README badge restoration pending; [uibcdf/molsyssuite#69](https://github.com/uibcdf/molsyssuite/issues/69) |
| uibcdf/dockingmt | No usable completed report observed | Unavailable / not observed | producer/evidence adoption pending; [uibcdf/dockingmt#22](https://github.com/uibcdf/dockingmt/issues/22) |
| uibcdf/ackredit | No usable completed report observed | Unavailable / not observed | producer/evidence adoption pending; [uibcdf/ackredit#76](https://github.com/uibcdf/ackredit/issues/76) |
| uibcdf/lindelint | 55.13% · `dfb23cde031d` | [36701419960](https://github.com/uibcdf/lindelint/actions/runs/36701419960) | existing live badge; cadence explanation pending; [uibcdf/molsyssuite#69](https://github.com/uibcdf/molsyssuite/issues/69) |
| uibcdf/molsys-ai | No usable completed report observed | Unavailable / not observed | producer/evidence adoption pending; [uibcdf/molsys-ai#3](https://github.com/uibcdf/molsys-ai/issues/3) |
| uibcdf/molsyssuite | No usable completed report observed | Unavailable / not observed | producer/evidence adoption pending; [uibcdf/molsyssuite#69](https://github.com/uibcdf/molsyssuite/issues/69) |

## Evidence boundaries and cadence

The four support libraries publish from their existing routine Linux/Python 3.13
coverage route; their weekly full-matrix jobs do not necessarily upload coverage.
MolSysViewer uploads Python plus JavaScript unit coverage from its selected
Linux/Python 3.13 lane. PharmacophoreMT, ElastNetMT and LinDelINT retain their
existing full contributor/weekly/conditional-nightly routes and selected uploader.
A skipped push does not produce a new report. README explanations must name the
last-uploaded-report boundary rather than imply coverage of later HEAD.

For ElastNetMT, the successful Linux/Python 3.13 upload in the recorded run
coexists with failed older-minor jobs. Its percentage is valid for that report;
the overall workflow remains failure. No scientific failure was repaired here.

MolSysMT renders 80% from a skipped March 25 cache with inherited 79.88% totals;
the newest complete report observed is March 24 (78.79%). The maintainer approved
waiting for a recent owner-reviewed report, tracked in uibcdf/molsysmt#286.
Owner: dprada/LMMV. Review: 2026-10-31. Interim: badge absent and no full suite
forced by this rollout. Removal: recent complete default-branch report and actual
upload evidence under the component normal CI.

TopoMT has an uploader configured but public percentage is unknown and the
observed branch cache is pending. No report in this bounded scan is not proof of
never uploading. Ackredit public evidence returns HTTP 404; that is unavailable
evidence, not an applicability waiver.

## Applicability outside existing producers

Pytest Receptor and GH Run Receptor have tested executable code and are applicable;
their missing producer work is local. DockingMT and Ackredit likewise need owned
reporting review; early maturity alone is not non-applicability.

MolSys-AI is currently a specification-oriented subsystem with executable
governance scripts and reporting tests. Coverage of an unimplemented agent
runtime is not applicable; coverage of existing tooling is separately applicable
and pending under uibcdf/molsys-ai#3. Reassess runtime coverage when executable
agent behavior is implemented. MolSysSuite central tooling is also applicable;
its producer and README adoption remain under uibcdf/molsyssuite#69.

## Repeatable read-only operations

1. Run `python devtools/scripts/suite_status.py` before the member review; preserve
   dirty worktrees and inspect fetched refs or isolated checkouts.
2. Record actual default-branch source SHA and inspect only active workflow files.
3. Run `python devtools/scripts/coverage_audit.py --repository uibcdf/<name>`; retain
   its JSON, including errors. It does not judge freshness or scientific scope.
4. Match the complete report SHA to the native workflow and actual successful
   coverage upload step. Record upload completion time separately from commit time.
5. Review producer cadence and README scope, then generate the badge via
   `coverage_badge(repository, branch)` in the owning badge module.
6. Record missing producers, deferrals and non-applicability with the owning issue.
   Refresh dated evidence before claiming adoption; no package is published.
