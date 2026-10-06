# Coverage badge adoption

Central ownership: uibcdf/molsyssuite#69. Normative rules: [repository_badges.md](../repository_badges.md#coverage-percentage-applicability-and-cadence).

## Measured inventory (2026-10-01; MolSysMT refreshed 2026-10-02)

The initial inventory includes all fifteen members registered on 2026-10-01 and
the suite root. OpenCASTp was appended on 2026-10-02 following its admission; the
inventory now covers all sixteen registered members and the suite root. GitHub confirms
`main` as each inspected default branch. Exact inspected source SHAs, complete report SHAs,
commit timestamps, Codecov cache states and actual upload times/runs are retained
in [coverage_badges.json](coverage_badges.json). Percentages below are dated
measurements; README badges render the service dynamically. The initial read-only audit launched no test suite. The three approved
producer executions below subsequently reuse tool/admin tests without launching
a scientific consumer suite. The later explicitly authorized MolSysMT refresh is
a separate execution, recorded below. Backup workflows are excluded from active producers.

| Repository | Complete report observed | Native upload evidence | README / owned action |
| --- | --- | --- | --- |
| uibcdf/smonitor | 78.38% · `2e03716a94a3` | [36539959586](https://github.com/uibcdf/smonitor/actions/runs/36539959586) | live percentage and cadence explanation delivered; [uibcdf/molsyssuite#69](https://github.com/uibcdf/molsyssuite/issues/69) |
| uibcdf/argdigest | 92.53% · `6223e0124fcc` | [36640865049](https://github.com/uibcdf/argdigest/actions/runs/36640865049) | live percentage and cadence explanation delivered; [uibcdf/molsyssuite#69](https://github.com/uibcdf/molsyssuite/issues/69) |
| uibcdf/depdigest | 93.27% · `0da46d9ff31f` | [36788753059](https://github.com/uibcdf/depdigest/actions/runs/36788753059) | live percentage and cadence explanation delivered; [uibcdf/molsyssuite#69](https://github.com/uibcdf/molsyssuite/issues/69) |
| uibcdf/pyunitwizard | 90.23% · `c9f572c5061a` | [36538121889](https://github.com/uibcdf/pyunitwizard/actions/runs/36538121889) | live percentage and cadence explanation delivered; [uibcdf/molsyssuite#69](https://github.com/uibcdf/molsyssuite/issues/69) |
| uibcdf/pytest-receptor | 79.73% · `b75be9c46b1e` | [36935901442](https://github.com/uibcdf/pytest-receptor/actions/runs/36935901442) | live percentage and scope/cadence explanation delivered; [uibcdf/pytest-receptor#12](https://github.com/uibcdf/pytest-receptor/issues/12) |
| uibcdf/gh-run-receptor | 78.95% · `da225de8e1a5` | [36935965052](https://github.com/uibcdf/gh-run-receptor/actions/runs/36935965052) | live percentage and scope/cadence explanation delivered; [uibcdf/gh-run-receptor#57](https://github.com/uibcdf/gh-run-receptor/issues/57) |
| uibcdf/molsysmt | New XML: 86.02% lines / 71.34% branches; complete Codecov report pending | [36939842865](https://github.com/uibcdf/molsysmt/actions/runs/36939842865), upload succeeded while tests failed | report and scope/cadence delivered; live badge withheld pending service acceptance; [uibcdf/molsysmt#286](https://github.com/uibcdf/molsysmt/issues/286) |
| uibcdf/molsysviewer | 75.81% · `ca6a3cda9eef` | [36926313560](https://github.com/uibcdf/molsysviewer/actions/runs/36926313560) | live percentage and scope/cadence explanation delivered; [uibcdf/molsyssuite#69](https://github.com/uibcdf/molsyssuite/issues/69) |
| uibcdf/topomt | No usable completed report observed | Unavailable / not observed | producer/evidence adoption pending; [uibcdf/topomt#81](https://github.com/uibcdf/topomt/issues/81) |
| uibcdf/pharmacophoremt | 38.99% · `98ecb459348a` | [36457546833](https://github.com/uibcdf/pharmacophoremt/actions/runs/36457546833), [36357376234](https://github.com/uibcdf/pharmacophoremt/actions/runs/36357376234) | live percentage and scope/cadence explanation delivered; [uibcdf/molsyssuite#69](https://github.com/uibcdf/molsyssuite/issues/69) |
| uibcdf/elastnetmt | 60.97% · `956670796957` | [36459131786](https://github.com/uibcdf/elastnetmt/actions/runs/36459131786), [36357927495](https://github.com/uibcdf/elastnetmt/actions/runs/36357927495) | live percentage and scope/cadence explanation delivered; [uibcdf/molsyssuite#69](https://github.com/uibcdf/molsyssuite/issues/69) |
| uibcdf/dockingmt | No usable completed report observed | Unavailable / not observed | producer/evidence adoption pending; [uibcdf/dockingmt#22](https://github.com/uibcdf/dockingmt/issues/22) |
| uibcdf/ackredit | 90.59% · `991084a4d0be` (2026-10-04 update; SVG 91%) | [37188364728](https://github.com/uibcdf/ackredit/actions/runs/37188364728) | live percentage and installed runtime scope/weekly-manual cadence delivered; [uibcdf/ackredit#76](https://github.com/uibcdf/ackredit/issues/76) closed |
| uibcdf/lindelint | 55.13% · `dfb23cde031d` | [36701419960](https://github.com/uibcdf/lindelint/actions/runs/36701419960) | live percentage and cadence explanation delivered; [uibcdf/molsyssuite#69](https://github.com/uibcdf/molsyssuite/issues/69) |
| uibcdf/molsys-ai | No usable completed report observed | Unavailable / not observed | producer/evidence adoption pending; [uibcdf/molsys-ai#3](https://github.com/uibcdf/molsys-ai/issues/3) |
| uibcdf/opencastp | Pending meaningful producer/report at `6303af503182` | Test CI exists; no coverage producer/upload | meaningful producer/scope and accepted-report evidence pending; [uibcdf/opencastp#3](https://github.com/uibcdf/opencastp/issues/3) |
| uibcdf/molsyssuite | 57.91% · `1eed48d97939` (2026-10-06; SVG 58%) | [37421121401](https://github.com/uibcdf/molsyssuite/actions/runs/37421121401) | live percentage and scope/cadence explanation delivered; [uibcdf/molsyssuite#69](https://github.com/uibcdf/molsyssuite/issues/69) |

## Evidence boundaries and cadence

OpenCASTp's row was refreshed from the initial README-only snapshot to the team's
published `6303af5` source under uibcdf/molsyssuite#70/#72. Numerical coverage is
applicable, but no meaningful producer/upload or service-level report is claimed.
Its four required guide copies are registered and byte-identical in that source;
its active checkout was not changed. The original fifteen-member
guide delivery and five remaining follow-ups below are historical measurements;
OpenCASTp adds a sixth producer/evidence follow-up under uibcdf/opencastp#3.

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

The initial MolSysMT inspection rendered 80% from a skipped March 25 cache with
inherited 79.88% totals. The subsequent authorized refresh generated and
transported current XML, but at the dated October 2 observation Codecov still
has no complete report for its SHA and the live SVG has no numeric percentage.
The newest complete service report still observed is March 24 (78.79%), retained
as historical evidence. uibcdf/molsysmt#286 stays partial for service acceptance.
Owner: dprada/LMMV. Review: 2026-10-31. Interim: badge absent; retained XML and
measured local report available. Removal: independent complete default-branch
report for the actual uploader SHA and live numeric SVG. No additional scientific
execution is authorized by the service-pending state.

TopoMT has an uploader configured but public percentage is unknown and the
observed branch cache is pending. No report in this bounded scan is not proof of
never uploading. Ackredit public evidence returns HTTP 404; that is unavailable
evidence, not an applicability waiver.

## Applicability outside existing producers

Pytest Receptor and GH Run Receptor have tested executable code and are applicable;
their approved producers and accepted reports are now delivered below. DockingMT and Ackredit likewise need owned
reporting review; early maturity alone is not non-applicability.

MolSys-AI is currently a specification-oriented subsystem with executable
governance scripts and reporting tests. Runtime code is owned by its internal
Server/Client/Agent repositories; a runtime percentage is not applicable to this
umbrella checkout. Coverage of existing tooling is separately applicable
and pending under uibcdf/molsys-ai#3. Reassess scope when executable responsibilities move; this inspection does not
establish the implementation state of its child repositories. MolSysSuite central tooling is also applicable;
its producer and README adoption are now delivered under uibcdf/molsyssuite#69.

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
| uibcdf/pytest-receptor | `3b0e07c3afff7b283efa7254bc251a3b8670005c` | yes; accepted producer report |
| uibcdf/gh-run-receptor | `1f378f2ccd0e8cf8c0d4cbb73431c712611955b1` | yes; accepted producer report |
| uibcdf/molsysmt | `2ad135d645a6b2a033a90015d42c88d8570305a2` | scope/procedure and measured report; badge still pending |
| uibcdf/molsysviewer | `f2b148722e32e2f83bc690e51e6aa622b2e31294` | yes |
| uibcdf/topomt | `e8dfdd239391707d2de56e154d99ee483156c2cf` | no; owned pending evidence/scope |
| uibcdf/pharmacophoremt | `228355a70a691c7594244189a3bed4acc437c8c2` | yes |
| uibcdf/elastnetmt | `e1b3bbe859cff203665e8630091c55fe1ad064a3` | yes |
| uibcdf/dockingmt | `12f06dcde6c62a4e0fb6d2ac45daf2479dd59500` | no; owned pending evidence/scope |
| uibcdf/ackredit | `2e9f5091a449b8c01ffaf11a46d3d51cefd211bb` | no; owned pending evidence/scope |
| uibcdf/lindelint | `26fdb4891d28627c29644014d9151ac126354d98` | yes |
| uibcdf/molsys-ai | `ed0347d7e38011075a944e3bead1e3ffe24286ff` | no; owned pending evidence/scope |

## Approved producer delivery (2026-10-01)

The maintainer approved implementing the MolSysSuite, Pytest Receptor and GH Run
Receptor producers using their existing tests. All three exact-source hosted
workflows succeeded, retained XML and uploaded through separate trusted-main OIDC
jobs. Independent Codecov API checks confirm complete reports for those same
commits, and each live SVG renders a numeric percentage. XML upload time remains
separate from source commit time in the JSON receipt.

| Repository | Measured scope | Existing test evidence | Accepted source |
| --- | --- | --- | --- |
| uibcdf/molsyssuite | `devtools/scripts`; parent process only | 270 administrative unittest tests | `a4cee98a30fa5ec553760ebb1d4e4bb71c2318f0` |
| uibcdf/pytest-receptor | `pytest_receptor`; parent process only | 200 serial tests; all eight serial/distributed matrix cells also passed | `b75be9c46b1e5bd42994b3fad619fd8481b09896` |
| uibcdf/gh-run-receptor | `gh_run_receptor`; parent process only | 465 package tests | `da225de8e1a574b5f4b3469f6b89a03548632e7f` |

Initial publishers failed before upload while Codecov action v5.5.1 tried to
fetch an unavailable verification key. All three now pin verified official
v7.1.1, which uses the current key source; signature validation remains enabled.
This evidence qualifies the declared tool/admin report scope. It does not add a
common coverage floor, measure every supported platform, combine child processes
or run deferred scientific suites.

Pytest Receptor and GH Run Receptor archive their producer records and close
uibcdf/pytest-receptor#12 and uibcdf/gh-run-receptor#57 after README delivery. The
suite now has accepted evidence for ten members plus its own tooling. The five
remaining repository follow-ups are MolSysMT (service acceptance pending), TopoMT,
DockingMT, Ackredit and the MolSys-AI umbrella's separate tooling scope. #69 stays
partial. The shared guide remains unchanged by producer implementation.

## MolSysMT authorized refresh (2026-10-01)

The maintainer explicitly authorized a complete Linux/Python 3.13 refresh after
prioritizing MolSysMT and MolSysViewer. The initial waiting decision remains a
historical checkpoint; [36939842865](https://github.com/uibcdf/molsysmt/actions/runs/36939842865) executed on `98e0d7832026df1f03320003d47ab9c4a6df2188` through the
existing workflow's explicit manual selector. The normal/default Linux matrix
remains three interpreters. A complete report may be uploaded after completed
pytest exit 1, while the actual CI failure remains visible; abort/collection
errors cannot publish. Artifact retention and uploader identity are checked
independently of scientific pass claims. Independent service acceptance remains
pending, with measured results below.

### MolSysMT measured result (2026-10-02)

Native logs and retained XML independently establish 10,298 passed, 4 failed,
2 skipped and 40 deselected in 2,338.79 seconds. The scientific truth gate passed
54 cases; the package job/workflow correctly remain failed. XML measures 63,586
of 73,923 Python lines (86.02%) and 15,152 of 21,240 branches (71.34%) across 2,470
files. These XML values are not an accepted Codecov project percentage and do
not include Rust execution or the declared coverage exclusions.

The retained report and area breakdown are published by MolSysMT documentation
source `2ad135d645a6b2a033a90015d42c88d8570305a2` under
[uibcdf/molsysmt#286](https://github.com/uibcdf/molsysmt/issues/286). The three
unit-policy failures remain related to uibcdf/molsysmt#244 and
uibcdf/molsyssuite#18; the converter-table failure stays component-owned. No
scientific assertion or dependency pin was changed to obtain coverage.

The actual coverage upload succeeded at `2026-10-01T23:58:11Z`. At
`2026-10-02T06:47:07.185353+00:00`, the public branch cache identifies the correct
source but has null state/totals; the independent commit has no processed report,
and the uploads API lists coverage as `started`. Test-results ingestion is
separately processed. The live SVG is nonnumeric. Transport success therefore
cannot restore the percentage badge or close the owner issue. Existing XML is
available for 14 days; a future transport repair can reuse it without treating
this pending service state as authorization to repeat the scientific suite.

The earlier public-service check at `2026-10-02T07:13:43.715728+00:00`
returned the same incomplete correct-source state, no numeric SVG, and March
as the newest complete report. The JSON retains both observations.


## MolSysMT automatic publisher and bounded replays (2026-10-02)

MolSysMT now automatically calls a separate reusable OIDC publisher after the
weekly/conditional-nightly/full-manual test job group. Like the three tool/admin
producers, routine publication submits only the selected XML without a flag.
Completed failed suites with successfully retained XML can be measured, but
remain failed. An unrelated publisher failure cannot force an already successful
three-minor scientific matrix to run again; publisher-only replay and the failed
single-lane measurement cannot pay matrix debt.

The owner-local implementation is pushed through
`e28d37d143af50ee0e2d3513104a73c0cae91167`; the maintained diagnostic record is
pushed in `e6f70c6c92bb560ff8dbda0b9cf94a70657f5b00`. These are publisher/documentation
sources, not newly measured coverage. All replays preserve measured source
`98e0d7832026df1f03320003d47ab9c4a6df2188` and XML digest
`9615b46264936cd8c80d2618919ab53f666b1f217b2a9223eaba0affe7726f3d`.

| Replay | Transport | Native upload ended (UTC) | Independently processed report |
| --- | --- | --- | --- |
| [36979661341](https://github.com/uibcdf/molsysmt/actions/runs/36979661341) | token, original flag | 2026-10-02 07:39:38 | not observed |
| [36980687004](https://github.com/uibcdf/molsysmt/actions/runs/36980687004) | OIDC, original flag | 2026-10-02 07:51:03 | not observed |
| [36985514288](https://github.com/uibcdf/molsysmt/actions/runs/36985514288) | OIDC, unflagged | 2026-10-02 08:42:33 | not observed |
| [36987144451](https://github.com/uibcdf/molsysmt/actions/runs/36987144451) | OIDC, unflagged, legacy endpoint | 2026-10-02 08:59:48 | not observed |

All four native publisher runs succeed and transmit the unchanged XML for its
original source without running tests. The legacy input is an explicit
compatibility probe, default false; routine publication keeps the current
endpoint. At `2026-10-02T09:03:55.181766+00:00` the independent API still has
null source state/totals, a nonnumeric SVG and March's latest complete report.
Four modern coverage uploads remain `started`; JUnit is separately processed.
The successful legacy queue request has no new exposed row in the public uploads
listing, so it is not counted as a listed fifth coverage upload. The maintainer's
authenticated UI confirms `Missing Head Report`, without a processing error.

The processing cause remains unidentified. Owner-local records contain the
source/artifact/digest, native runs, transport differences and service receipts
needed for provider diagnostics, without signed URLs or credentials. No further
identical replay or scientific execution follows from this pending state.
Thirty-three focused component provenance and suite/debt tests pass, along with
Ruff, actionlint, local devguide/index and the central repository conformance guard.
The live badge remains withheld; uibcdf/molsysmt#286 and uibcdf/molsyssuite#69
remain partial, with the same five owner-local follow-ups.

The final check at `2026-10-02T09:08:49.011548+00:00` confirms the same null
correct-source report, nonnumeric SVG and March's latest complete report; its
full receipt is retained as `last_service_check` in the JSON inventory.


## Ackredit accepted runtime report — 2026-10-04

The component completed uibcdf/ackredit#76 in
`04015022d0e13a33ce6631bdc10d62ea10aefa74`; this central review independently
accepts producer `991084a4d0be3fddbc0f2f79a87818b3a8f0ad18` from manual run
[37188364728](https://github.com/uibcdf/ackredit/actions/runs/37188364728).
Both installed-measurement and separate trusted-main OIDC upload jobs passed.
The exact native artifact ZIP digest and retained XML SHA-256 were verified;
all sixty-one module identities match the producer source, with seven empty
modules and fifty-four nonempty files. XML and public Codecov agree on 2,010
lines / 1,821 hits: 90.597% XML, 90.59% service and 91% rounded numeric SVG.
Receipt: [`ackredit_runtime_coverage_69.json`](ackredit_runtime_coverage_69.json).

The scope is installed parent-process runtime Python, excluding only generated
version constants within the package. Third-party code, subprocesses and
developer tools are outside the percentage; uncovered optional adapter paths
remain in the denominator. Hosted tests report 1,552 passed and seven skips
for absent optional system/developer tools, not a zero-skip result. The first
accepted upload is manual; weekly Monday 06:43 UTC is configured, not yet
claimed observed here. No extra suite runs on internal pushes or PRs, no
coverage floor, scientific correctness, full matrix or new public package claim
is added. Report source, later README head, native upload time and service
commit timestamp remain distinct. The initial pending receipt above is dated
history, superseded for Ackredit by this explicit follow-up.


## Central recovery accepted — 2026-10-06

The normal unskipped checkpoint `1eed48d979399a5619b100afb172b0a3ebdd63e6`
passes [37421121401](https://github.com/uibcdf/molsyssuite/actions/runs/37421121401):
337 administrative tests, offline governance, Conda controls and retained XML.
The separate publisher succeeds through the unchanged official CLI download,
GPG signature (fingerprint `27034E7FDB850E0BBC2C62FF806BB28AED779869`) and
checksum verification. No workflow or verification replacement was needed.

The independent exact-commit API now reports **complete**, correct `main`/SHA
identity and **57.91%**; the live SVG reads **58%**. This supersedes the earlier
pending-processing observation and resolves the central transport/processing
recovery. Receipt: [molsyssuite_coverage_recovery_69_20261006.json](molsyssuite_coverage_recovery_69_20261006.json).
Retained artifact 11393106645 has native ZIP digest
`sha256:e698720f856906c9e4e90326f0ce1d3eadaa1f92b26a104f8d3a93074d6ba0e9`;
XML SHA-256 is `6e11c92654b318d4268cc51211bc5cf93db6490c5fafd695111207ca83dc7189`.

Codecov counts 3,116 fully covered lines and 409 partial lines out of 5,380.
Their sum matches the XML's 3,525 covered lines; the XML line rate (65.52%)
includes those partial branch lines and is not the service's percentage.
This is the new checkpoint's report, not a replay of the earlier failed source.
No additional tests or publisher replay were dispatched for this reconciliation.
#69 remains partial for the independently owned component reports, including
uibcdf/molsysmt#286; their dated pending evidence and scientific deferral are
not cleared by the central success.
