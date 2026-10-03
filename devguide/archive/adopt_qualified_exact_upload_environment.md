---
summary: Adopt the fully qualified exact-upload provider in shared noarch publishers.
issue: uibcdf/molsyssuite#86
status: resolved
opened: 2026-10-03
closed: 2026-10-03
verification: measured
area: [governance, packaging, ci]
guard: tests/test_conda_release_contract.py::CondaReleaseContractTests::test_shared_noarch_build_uses_qualified_active_environment_provider
normative: devguide/noarch_conda_workflow.md
blocked_by: []
supersedes: []
---

# Qualified exact-upload environment adoption

**Reported:** 2026-10-03, provider closure handoff and maintainer review.
**Status:** Resolved; the qualified shared source is published, hosted checks pass,
all six consumer callers and notices are delivered, and provider/platform feedback
is recorded. Actual component delivery remains tracked separately under #78.

## What

The shared publisher's separate upload subaction selects non-login Bash, losing
the named environment's publishing client. Ackredit producer 37127293886 and
Pytest Receptor producer 37127152850 pass real build, recipe tests and archive
inspection, then fail at exact upload. Provider issue
uibcdf/action-build-and-upload-conda-packages#48 owns the repaired behavior;
uibcdf/molsyssuite#86 owns central adoption and handoff, linked to the existing
consumer coordination uibcdf/molsyssuite#78 and platform uibcdf/moli#38.

## How

Integrate the existing uibcdf/molsyssuite#85 with current main, then select the
more completely qualified provider source
`1aa2011f902a1a9d533564572245bb29f6862e86` for both exact-upload steps. Its parent
`6f65ba66d1afff74ded8442c3c3ee6448a5f3a60` implements the shell/diagnostic fix;
the newer source adds complete-composite qualification. The qualified build
and promotion sources and all existing release, byte, resource, installed and
independent verification controls remain under their accepted contracts.

Publish the immutable central source and identify shared consumers from the
registered publisher inventory. Preserve active team work using fetched isolated
clones, update applicable thin build callers and deliver exact handoffs to their
existing publication issues. Record commits, notices and actual artifact evidence
separately. No new pull request is needed.

## Why

The same shared operation failed in two independent consumers. Provider-local
repair requires central pin adoption before other member callers can use it.
Changing a developer's interpreter or reinstalling local dependencies cannot
repair the hosted composite shell. This is ecosystem tooling, not a scientific
component defect or a new release-policy decision.

## What is measured and what is assumed

Provider source and native run 37129463375 were inspected on 2026-10-03. Its
head is exactly `1aa2011f902a1a9d533564572245bb29f6862e86`; all five jobs pass:
the offline contract plus actual composite executions in named Linux/macOS
Conda environments for success and client failure. Verification checks sealed
bytes, identity/digest, one client call, public poststate, failure diagnostics,
original-candidate preservation and no retries. Client and registry are simulated.
Neither actual package publication nor Windows composite execution is inferred.

The central regression first fails against PR #85's earlier `6f65ba6...` pin,
then passes after selecting the fully qualified source. It protects the reviewed
immutable adoption and preserved single-file build/upload shape; provider tests
own the executable shell/client regression. These two evidence scopes differ.

## Alternatives and refuted paths

Using the implementation-only source loses the later full-composite evidence.
Replacing the build or promotion pin merely to align hashes would change unrelated
qualified operations. Repeating an uncertain upload, forcing an occupied coordinate
or skipping recipe/installed checks would violate the existing publication contract.

## Scope and exclusions

This central issue covers provider review, immutable pin adoption, workflow
guards and consumer handoff. Actual staged/public component delivery remains in
uibcdf/molsyssuite#78 and member issues. Scientific failures remain component-owned;
no new platform claim, public release or registry retry is authorized by closure.

## Acceptance criteria

- Publish the reviewed immutable exact-upload source in both shared steps.
- Pass offline governance, publication-contract tests and hosted central checks.
- Record the central source and affected member caller adoption/notice receipts.
- Return central acceptance to the provider/platform owning issues.
- Retain actual component artifact evidence separately in #78 and member issues.

## Local implementation issues

The six shared publisher owners are uibcdf/ackredit#22,
uibcdf/pytest-receptor#32, uibcdf/topomt#78, uibcdf/pharmacophoremt#10,
uibcdf/elastnetmt#18 and uibcdf/lindelint#13. uibcdf/ackredit#75,
uibcdf/ackredit#80 and uibcdf/sabueso#108 retain their portable contract and receiving-consumer delivery.

## Dependencies and risks

Consumer teams may advance while adoption is prepared. Fetch before editing and
record the actual committed caller. Fresh all-label coordinate reads and native
exact-source gates remain necessary before any later upload; an old absence
observation is not a new mutation permission.

## Provenance

Provider commit diff and native job/step JSON inspected through GitHub on
2026-10-03. Central regression first executed with local Python 3.13.15; central
hosted governance uses Python 3.14. Integration and rollout measurements are
appended below as they complete.

## Integration and delivery — 2026-10-03

Existing PR #85 is directly integrated at
`2fb344525ca0eea817dc24a518f4a6bf26e311cf` with the fully qualified upload source.
The merge retains the original prepared commit in its history and records the
newer review result in the final source. Native central governance
[37130795870](https://github.com/uibcdf/molsyssuite/actions/runs/37130795870)
passes at that exact source on Python 3.14, with the actual governance tests and
publication-control checks executed. The existing pin regression failed against
#85's earlier source before the update; all 24 publication-contract tests, Ruff
and offline governance pass locally on Python 3.13.15. A local Python 3.14
interpreter was unavailable; hosted 3.14 execution supplies that validation.

All six registered shared publisher consumers were fetched in isolated clones,
received a focused direct caller commit and were notified in their existing
publication issues before those commits were pushed. The only component edit
is its immutable build/publish workflow reference. Each passes the administrative
publication conformance check; no scientific suite, registry mutation or public
release was triggered by this rollout. Original dirty checkouts and active team
work were preserved. All exact commits, old/new references and notices are in
`devguide/rollouts/exact_upload_adoption_86.json`; the maintained publisher
inventory reflects all six adopted calls and passes its read-only drift check.

The central acceptance and consumer handoff were returned to
[uibcdf/action-build-and-upload-conda-packages#48](https://github.com/uibcdf/action-build-and-upload-conda-packages/issues/48#issuecomment-5970323043)
and [uibcdf/moli#38](https://github.com/uibcdf/moli/issues/38#issuecomment-5970337601).
Provider qualification, central acceptance, consumer source adoption and actual
component publication remain separate facts. The last remains in #78 and member
issues; it is not a missing criterion for this completed provider adoption.
