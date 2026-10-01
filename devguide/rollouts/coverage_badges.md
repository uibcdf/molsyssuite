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
| uibcdf/smonitor | 78.38% · `2e03716a94a3` | [36539959586](https://github.com/uibcdf/smonitor/actions/runs/36539959586) | live percentage and cadence explanation delivered; [uibcdf/molsyssuite#69](https://github.com/uibcdf/molsyssuite/issues/69) |
| uibcdf/argdigest | 92.53% · `6223e0124fcc` | [36640865049](https://github.com/uibcdf/argdigest/actions/runs/36640865049) | live percentage and cadence explanation delivered; [uibcdf/molsyssuite#69](https://github.com/uibcdf/molsyssuite/issues/69) |
| uibcdf/depdigest | 93.27% · `0da46d9ff31f` | [36788753059](https://github.com/uibcdf/depdigest/actions/runs/36788753059) | live percentage and cadence explanation delivered; [uibcdf/molsyssuite#69](https://github.com/uibcdf/molsyssuite/issues/69) |
| uibcdf/pyunitwizard | 90.23% · `c9f572c5061a` | [36538121889](https://github.com/uibcdf/pyunitwizard/actions/runs/36538121889) | live percentage and cadence explanation delivered; [uibcdf/molsyssuite#69](https://github.com/uibcdf/molsyssuite/issues/69) |
| uibcdf/pytest-receptor | No usable completed report observed | Unavailable / not observed | producer/evidence adoption pending; [uibcdf/pytest-receptor#12](https://github.com/uibcdf/pytest-receptor/issues/12) |
| uibcdf/gh-run-receptor | No usable completed report observed | Unavailable / not observed | producer/evidence adoption pending; [uibcdf/gh-run-receptor#57](https://github.com/uibcdf/gh-run-receptor/issues/57) |
| uibcdf/molsysmt | 78.79% · `b6c0e4f2a15e` | Unavailable / not observed | stale March evidence; maintainer-approved deferral; keep badge absent; [uibcdf/molsysmt#286](https://github.com/uibcdf/molsysmt/issues/286) |
| uibcdf/molsysviewer | 75.81% · `ca6a3cda9eef` | [36926313560](https://github.com/uibcdf/molsysviewer/actions/runs/36926313560) | live percentage and scope/cadence explanation delivered; [uibcdf/molsyssuite#69](https://github.com/uibcdf/molsyssuite/issues/69) |
| uibcdf/topomt | No usable completed report observed | Unavailable / not observed | producer/evidence adoption pending; [uibcdf/topomt#81](https://github.com/uibcdf/topomt/issues/81) |
| uibcdf/pharmacophoremt | 38.99% · `98ecb459348a` | [36457546833](https://github.com/uibcdf/pharmacophoremt/actions/runs/36457546833), [36357376234](https://github.com/uibcdf/pharmacophoremt/actions/runs/36357376234) | live percentage and scope/cadence explanation delivered; [uibcdf/molsyssuite#69](https://github.com/uibcdf/molsyssuite/issues/69) |
| uibcdf/elastnetmt | 60.97% · `956670796957` | [36459131786](https://github.com/uibcdf/elastnetmt/actions/runs/36459131786), [36357927495](https://github.com/uibcdf/elastnetmt/actions/runs/36357927495) | live percentage and scope/cadence explanation delivered; [uibcdf/molsyssuite#69](https://github.com/uibcdf/molsyssuite/issues/69) |
| uibcdf/dockingmt | No usable completed report observed | Unavailable / not observed | producer/evidence adoption pending; [uibcdf/dockingmt#22](https://github.com/uibcdf/dockingmt/issues/22) |
| uibcdf/ackredit | No usable completed report observed | Unavailable / not observed | producer/evidence adoption pending; [uibcdf/ackredit#76](https://github.com/uibcdf/ackredit/issues/76) |
| uibcdf/lindelint | 55.13% · `dfb23cde031d` | [36701419960](https://github.com/uibcdf/lindelint/actions/runs/36701419960) | live percentage and cadence explanation delivered; [uibcdf/molsyssuite#69](https://github.com/uibcdf/molsyssuite/issues/69) |
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
governance scripts and reporting tests. Runtime code is owned by its internal
Server/Client/Agent repositories; a runtime percentage is not applicable to this
umbrella checkout. Coverage of existing tooling is separately applicable
and pending under uibcdf/molsys-ai#3. Reassess scope when executable responsibilities move; this inspection does not
establish the implementation state of its child repositories. MolSysSuite central tooling is also applicable;
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

## Delivery (2026-10-01)

The canonical member guide from central source `9516239` was synchronized with
`sync_vendored_guides.py` and pushed to all fifteen members. Eight README updates
were pushed: new live percentages for MolSysViewer, PharmacophoreMT and ElastNetMT,
and cadence/scope explanations for those three plus the five previously badged
members. Delivery SHAs are distinct from inspected/report SHAs in the JSON receipt.
These documentation-only direct commits use `[skip ci]`; none changes a test
selection, upload workflow, package coordinate or scientific implementation.

Fourteen Python-member offline repository guards passed. MolSys-AI's separate
pre-existing identity/policy/license baseline omissions remain under
uibcdf/molsys-ai#4; its local reporting/index guard passed. A synchronized guide
is not a claim that every component policy or scientific matrix passes.

| Member | Pushed documentation SHA | Coverage README updated |
| --- | --- | --- |
| uibcdf/smonitor | `bfae8ab35b06a68377bde57ce73770d69fb85484` | yes |
| uibcdf/argdigest | `458b7950661e753f1e60990be070f8d28ebe5cba` | yes |
| uibcdf/depdigest | `2d56ef4330e36ddba421c344acf5dab0f0221c7a` | yes |
| uibcdf/pyunitwizard | `2ffe1885675f47c76af03c08e51bc889a5e99a05` | yes |
| uibcdf/pytest-receptor | `910ffa4911feb33832c1540942de7d123ec1b9e1` | no; owned pending evidence/scope |
| uibcdf/gh-run-receptor | `5ffe8c7eaf7095cf664b7643340fab78f442bcdd` | no; owned pending evidence/scope |
| uibcdf/molsysmt | `bc4a7c67a03800db2137dee93002791e02c1acac` | no; owned pending evidence/scope |
| uibcdf/molsysviewer | `f2b148722e32e2f83bc690e51e6aa622b2e31294` | yes |
| uibcdf/topomt | `e8dfdd239391707d2de56e154d99ee483156c2cf` | no; owned pending evidence/scope |
| uibcdf/pharmacophoremt | `228355a70a691c7594244189a3bed4acc437c8c2` | yes |
| uibcdf/elastnetmt | `e1b3bbe859cff203665e8630091c55fe1ad064a3` | yes |
| uibcdf/dockingmt | `12f06dcde6c62a4e0fb6d2ac45daf2479dd59500` | no; owned pending evidence/scope |
| uibcdf/ackredit | `2e9f5091a449b8c01ffaf11a46d3d51cefd211bb` | no; owned pending evidence/scope |
| uibcdf/lindelint | `26fdb4891d28627c29644014d9151ac126354d98` | yes |
| uibcdf/molsys-ai | `ed0347d7e38011075a944e3bead1e3ffe24286ff` | no; owned pending evidence/scope |
