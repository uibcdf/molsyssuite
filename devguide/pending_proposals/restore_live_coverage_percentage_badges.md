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
inventory are implemented. Recent reports support eight member README routes;
missing/stale producers remain owned follow-ups. MolSysMT's deferred full suite
is not run to manufacture a recent badge.

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

MolSysMT's missing badge initially suggested a simple README omission, but public
Codecov currently renders 80% from March's cached totals. Reintroducing that image
as current would be misleading. In contrast, MolSysViewer, PharmacophoreMT and
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
MolSys-AI, the unimplemented agent runtime has no meaningful runtime coverage;
its existing executable governance scripts/tests remain separately applicable.
MolSysSuite's own tested governance code is applicable but has no producer yet.

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
