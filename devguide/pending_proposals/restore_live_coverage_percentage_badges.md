---
summary: Restore truthful live coverage percentages and track every repository's reporting scope.
issue: uibcdf/molsyssuite#69
status: partial
opened: 2026-10-01
closed:
verification: measured
area: [governance, ci, documentation, coverage]
guard: tests/test_coverage_audit.py
normative: devguide/repository_badges.md
blocked_by: []
supersedes: []
---

# Live coverage percentages with owned evidence

**Reported:** 2026-10-01 in uibcdf/molsyssuite#69.
**Status:** Partial; the shared contract, public evidence probe and complete
inventory are implemented. All fifteen member guides and eleven coverage README
updates (ten members plus the suite root) are pushed;
missing/stale producers remain owned follow-ups. MolSysMT's explicitly approved
single Linux/Python 3.13 report is generated and published; independent Codecov
processing and its live badge remain pending, as recorded below.

## What

Applicable member READMEs should display their own live Codecov coverage
percentage, backed by a recent accepted default-branch report. Assess all fifteen
registered members and MolSysSuite itself, including auxiliary tools and the
specification-oriented MolSys-AI subsystem. Keep age, code/language scope and
CI health explicit rather than equating a percentage with a scientific pass.

## How

Extend the existing badge owner, `devtools/scripts/repository_badges.py`, with
public snippet generation and checks for existing Codecov identity/project
links and unsafe/static images. Add `devtools/scripts/coverage_audit.py` as a
bounded, read-only public evidence operation; its contract is documented in
`devguide/repository_badges.md`. Keep Codecov branch cache, explicitly complete
report, commit timestamp, native upload time and actual CI conclusions separate.

The normative coverage contract requires percentages where meaningful reporting
is maintained, states applicability and exceptions, preserves existing CI/skip
policies and has no common minimum percentage. The starter kit carries the same
conditional adoption instructions without inventing a project or upload.

## Why

MolSysMT's missing badge initially suggested a simple README omission, but the
initial public Codecov inspection rendered 80% from March's cached totals.
Reintroducing that image as current would be misleading. MolSysViewer, PharmacophoreMT and
ElastNetMT have recent complete reports and executed successful uploads; their
missing badges can be repaired without new scientific execution. Auxiliary tools
also have tested code and must not disappear from the review.

## What is measured and what is assumed

Read-only inspection on 2026-10-01 fetched every registered remote and examined
immutable `origin/main` sources, active top-level workflow files, public GitHub
default-branch metadata, Codecov v2 branch/commit responses and rendered SVGs.
The inventory retains exact source/report SHAs and native upload runs in
`devguide/rollouts/coverage_badges.md` and its JSON receipt. No component test
suite was run by this audit. Historical backup workflows are not active producers.

Eight members have recent complete reports and matching successful native uploads.
ElastNetMT's Linux/Python 3.13 upload succeeds while other matrix cells fail; both
facts remain visible. MolSysMT's public branch cache is `skipped` with inherited
79.88% totals from March 25; the newest complete report observed is March 24,
78.79%. Neither is current evidence for October's active source.

No complete report observed in a bounded scan is not proof of never uploading;
HTTP 404/network failure is unavailable evidence, not non-applicability. For
MolSys-AI, runtime code is owned by its internal Server/Client/Agent repositories rather
than this umbrella; existing executable governance scripts/tests remain separately
applicable. Absence of runtime in the umbrella does not imply it is unimplemented
in its internal repositories.
MolSysSuite's tested governance code was initially missing its producer; the
approved implementation and accepted hosted report are recorded below.

## Alternatives and refuted paths

- Restore every numeric SVG immediately: rejected because cached skipped-commit
  totals can be old, as demonstrated by MolSysMT.
- Require a full suite for each internal push to keep the percentage current:
  rejected because it conflicts with the accepted direct/skip workflow and is
  unnecessary for explaining report cadence.
- Declare developer tools or early components non-applicable automatically:
  rejected; executable scope and tests determine meaningfulness.
- Add a suite-wide coverage floor: outside this badge contract. Percentage
  alone neither qualifies scientific correctness nor repairs a failing matrix.

## Scope and exclusions

The central issue owns shared README evidence and rollout coordination. Components
own their producers, code selections, supported language/platform claims, service
access and scientific repairs. Package publication and full scientific
qualification remain separate. Existing badged members gain cadence explanations;
new badges are added only where independent evidence supports them.

## Acceptance criteria

- The shared contract states applicability, percentage format, ordering, cadence,
  unavailable/stale evidence and bounded exceptions.
- All registered members and the central repository have explicit inventory
  outcomes and component-owned missing-report work; no silent exclusions.
- Every applicable maintained producer has its own live README percentage backed
  by a recent accepted report and actual upload evidence, with scope/cadence text.
- The starter kit and relevant offline shape checks preserve the contract;
  service evidence remains a separate read-only networked operation.
- Missing reporting and the approved MolSysMT deferral are resolved or have
  accepted bounded exceptions before the rollout is described as complete.

## Local implementation issues

Owning identities and interim actions are listed in the coverage rollout.
MolSysMT's deferred report is uibcdf/molsysmt#286; TopoMT's missing accepted
report is uibcdf/topomt#81. Developer-tool and remaining producer follow-ups
stay with their repositories. The suite's central producer remains part of #69.
Companion platform coordination is uibcdf/moli#35.

## Dependencies and risks

A workflow upload step can succeed without proving that a new service report was
accepted; inspect both source-linked surfaces. Codecov branch caches may inherit
totals onto skipped commits. The public probe is bounded and cannot establish
scientific scope, cadence adherence or latest-HEAD coverage by itself. Ordinary
service outages must not be turned into passing evidence or non-applicability.

## Maintainer decision (2026-10-01)

The principal maintainer chose to wait for a recent MolSysMT report and register
the pending work. The interim README keeps its badge absent, with owner dprada/LMMV
and review on 2026-10-31. Removal condition: the owning team obtains a reviewed
recent default-branch report through its normal CI and can verify its actual
upload. This review date does not authorize a forced full-suite run.

## Guard relevance

`tests/test_coverage_audit.py` collectively guards the failure mechanism: skipped
cached totals cannot qualify as a completed report; zero coverage remains valid;
invalid percentages/source SHAs/timestamps fail; an unknown SVG cannot pass;
foreign/static/token-bearing images are rejected; and bounded missing/unavailable
responses do not become a passing or non-applicable result. Fixture tests exercise
the public-service adapter contract independently of network availability.

## Provenance

2026-10-01, host nauta, administrative Python 3.13 environment. Source/API audit
receipts identify observation times and every inspected SHA. The public probe
was also exercised successfully against MolSysViewer's existing report. This is
administrative evidence, not a new scientific or package-release qualification.

## Delivery and checks (2026-10-01)

Central source `9516239` implements the contract, public probe, badge generator,
starter guidance and initial measured inventory. All fifteen guide copies and
eight README updates were subsequently synchronized and pushed, with exact
member delivery SHAs in the rollout JSON. Three missing live badges were restored;
five existing badges gained scope/cadence text. The changes are documentation only
in member repositories and use `[skip ci]` under the accepted internal workflow.

Central offline governance and eighteen focused public-probe/badge/starter tests
passed. Ruff passes for the changed Python operations. Fourteen member offline
repository guards passed. MolSys-AI's pre-existing missing identity/policy/license
badges are separately owned in uibcdf/molsys-ai#4; its reporting/index checks passed.
This work does not claim new scientific execution, complete rollout adoption or
an accepted report for the pending producers.

## Approved producer implementation (2026-10-01)

The maintainer authorized producers for MolSysSuite, Pytest Receptor and GH Run
Receptor using their existing tests. The three workflows now measure declared
administrative/package scope and retain XML, with separate trusted-main OIDC
publishers. No scientific member suite is invoked. Local central execution
passed 268 existing tests and exported XML; two publisher-boundary guards were
then added and passed. Hosted execution and service acceptance remain pending.

## Hosted publisher correction (2026-10-01)

The first hosted publisher failed before sending a report because v5.5.1 fetched
an unavailable OpenPGP key. Tests and XML generation succeeded. The producer now
uses the official v7.1.1 commit, whose wrapper fetches the current `codecovsecops`
key. Signature checking remains enabled. Acceptance is still independently
required; the initial failure is not counted as an upload.

## Accepted hosted evidence (2026-10-01)

[36935888570](https://github.com/uibcdf/molsyssuite/actions/runs/36935888570) completed successfully for source `a4cee98a30fa5ec553760ebb1d4e4bb71c2318f0`.
It executed 270 administrative unittest tests, exported and retained XML, and executed a successful OIDC
upload. The independent public API observed `state=complete` for the same source
at `2026-10-01T22:36:16.788578+00:00` with 56.83%
Codecov coverage; the live SVG renders 57%.
The source commit timestamp is separate from the upload completion time
`2026-10-01T22:35:13Z`. The README now carries the live percentage and measured
scope/cadence. This does not qualify any scientific consumer or a new release.

## Current rollout state

The three approved producers and live badges are delivered with exact-source
complete service reports and successful native uploads. Developer-tool owning
issues #12 and #57 have resolved local records, tests/normative guidance and
README scope/cadence. The suite has accepted coverage evidence for ten members
plus its own administration. Five repository follow-ups remain; the rollout is
partial. The initial read-only audit and later authorized test executions are
separate evidence stages.

## MolSysMT single refresh authorization (2026-10-01)

The maintainer now prioritizes MolSysMT and MolSysViewer and explicitly chose one
complete MolSysMT Linux/Python 3.13 execution. This supersedes the earlier waiting
decision for this invocation only. Source `98e0d7832026df1f03320003d47ab9c4a6df2188` implements an explicit manual
selector in the existing weekly workflow and preserves normal/default matrix
scope. It retains completed-suite XML on pytest exit 0/1 while failed tests still
fail CI; aborted/invalid sessions cannot upload. Ten focused governance tests,
dependency/source audit, developer-guide validation, actionlint and the suite
repository guard pass.

[36939842865](https://github.com/uibcdf/molsysmt/actions/runs/36939842865) executed that exact source, with only the requested
interpreter. Its measured report is now published, while independent service
acceptance and live-badge adoption remain pending. No release or passing
full-matrix claim follows from this invocation.

## MolSysMT report delivered; service acceptance pending (2026-10-02)

The authorized complete Linux/Python 3.13 suite finished with real pytest exit 1:
10,298 passed, 4 failed, 2 skipped and 40 deselected. Its prior scientific gate
passed 54 cases. Retained `coverage.xml` and `junit.xml` confirm a complete
measurement, with 86.02% Python line coverage and 71.34% branch coverage under
unchanged exclusions; Rust execution is not instrumented. The selected job and
workflow correctly remain failed. Native retention and upload succeeded; the
upload completed at `2026-10-01T23:58:11Z` for the tested source.

Independent API observation at `2026-10-02T06:47:07.185353+00:00` does not yet
establish processing: correct-source branch-cache state/totals are null, coverage
upload is `started`, and the SVG has no numeric percentage. March's report is
still the latest explicitly complete service result observed. The new XML
measurement must not be substituted for an accepted Codecov project percentage.

MolSysMT direct documentation commit `2ad135d645a6b2a033a90015d42c88d8570305a2`
publishes the measured area breakdown, exact tests and artifact identity under
uibcdf/molsysmt#286 and explains report scope/cadence in README. The badge stays
absent and #286 stays partial. Ten focused component guards pass; local guide,
Ruff and central offline repository validation pass. The existing unit-policy
follow-ups retain the three repeated boundary failures; component conversion
contracts retain the fourth. Neither service acceptance nor a full-matrix pass
is invented. #69 remains partial with its same five owner-local follow-ups.

The earlier public-service check at `2026-10-02T07:13:43.715728+00:00`
returned the same incomplete correct-source state, no numeric SVG, and March
as the newest complete report. The JSON retains both observations.


## MolSysMT automatic publisher and bounded replays (2026-10-02)

The authorized follow-up delivers a separate reusable OIDC publisher that is
called automatically after the weekly/conditional-nightly/full-manual test job
group. Routine publication sends the complete selected XML without a flag, like
the three new tool/admin producers. Artifact-only replay preserves the measured
SHA/XML and does not run tests. An unrelated publisher failure cannot require
an already successful scientific matrix to run again; scientific failures and
publisher-only replays still cannot clear matrix debt. Thirty-three focused
component tests and the local workflow/governance checks pass.

Implementation is pushed through `e28d37d143af50ee0e2d3513104a73c0cae91167`;
the diagnostic record is pushed in `e6f70c6c92bb560ff8dbda0b9cf94a70657f5b00`.
Four bounded retained-XML replays test token, OIDC, unflagged and legacy transport.
All native publishers succeed, but the independent API and authenticated UI still
provide no processed head report. The cause remains unidentified; provider
diagnostics require evidence beyond successful transport or Missing Head Report.
The [rollout receipt](../rollouts/coverage_badges.md#molsysmt-automatic-publisher-and-bounded-replays-2026-10-02)
records the individual runs, timestamps and source/artifact identities; detailed
analysis remains owned by uibcdf/molsysmt#286. The live badge is withheld and
#69 remains partial with the same five owner-local follow-ups.
