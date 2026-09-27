---
summary: Complete the shared reporting lifecycle in remaining suite members.
issue: uibcdf/molsyssuite#60
status: active
opened: 2026-09-27
closed:
verification: inspected
area: [governance, reporting, rollout]
guard:
normative: devguide/reporting_protocol.md
blocked_by: []
supersedes: []
---

# Complete the shared reporting lifecycle in remaining members

**Reported:** 2026-09-27, during the member review for the Python CI lane
profile in `uibcdf/molsyssuite#39`.
**Status:** Active inventory; local implementations and hosted validation remain.

## What

Bring every registered member outside the stabilization wave of
`uibcdf/molsyssuite#13` into the reporting lifecycle accepted by
`uibcdf/molsyssuite#11`. Preserve repository-specific queue layouts while
requiring issue identity, permanent resolution records, a report template,
generated index, offline validator and contributor guidance. Early development
and unrelated scientific CI failures do not remove these governance duties.

## How

Review each member's effective local machinery and historical queued records,
then open local issues for concrete missing pieces. Use each member's issue
first, followed by its developer-guide report. Migrate active records to stable
issue identities without deleting historical analysis, add the local guard and
regenerate indexes. Verify the offline guard and inspect hosted governance runs
separately from product CI. Record member adoption and bounded exceptions here.

## Why

The shared reporting protocol says every member must be able to file, triage
and close issues with an addressable record. The six-member stabilization wave
was explicitly scoped; supporting tools and incubating members remained
outside it. A later TopoMT adoption demonstrates the local route, but does not
establish the state of the other repositories. Missing lifecycle machinery
makes cross-component CI and compatibility work difficult to track and close.

## What is measured and what is assumed

**Inspected on 2026-09-27:** `suite_status.py` fetched the 15 registered
component remotes without changing their worktrees. Read-only `git ls-tree`
inspection of each `origin/main` found no obvious report template, generated
index or offline reporting validator in Pytest Receptor, PharmacophoreMT,
ElastNetMT and Lindelint. MolSys-AI has a report template, but no apparent
generated index or offline validator. Pytest Receptor retains pending and
resolved queues with a local historical register, so migration must preserve
those records rather than discard them. TopoMT's `uibcdf/topomt#54` adoption
has its local template, index and validator. The six wave-one members are
covered by the recorded `uibcdf/molsyssuite#13` outcome; GH Run Receptor,
DockingMT and Ackredit have visible local lifecycle machinery.

These are source-tree observations, not claims that every historical record is
valid or that no differently named local equivalent exists. The next step is
to run each member's documented command, inspect its actual rules and validate
the queue against GitHub issue state.

## Alternatives and refuted paths

- Reopen the completed stabilization-wave issue: rejected because its six
  repositories met its stated scope; this is separately closable rollout work.
- Treat incubating scientific components as exempt: rejected because the
  reporting protocol applies to every member and provides bounded exceptions.
- Infer adoption from queue directory names alone: rejected because template,
  index, validation and issue-state synchronization also matter.

## Scope and exclusions

Initial audit targets are `uibcdf/pytest-receptor`,
`uibcdf/pharmacophoremt`, `uibcdf/elastnetmt`, `uibcdf/lindelint` and
`uibcdf/molsys-ai`. Any other member found nonconforming during execution is
included by the common rule. This work concerns governance records and guards,
not whether a scientific component's test suite passes or its models are
correct. Local implementations remain owned by each member.

## Acceptance criteria

- Every registered member has a documented equivalent for each required local
  surface of `devguide/reporting_protocol.md`, or a complete bounded exception.
- Queued reports have owning GitHub issues and valid local metadata; resolved
  records remain archived with their closure decisions and guards or normative
  documents.
- Each member's offline validator and index check pass; its contributor guide
  explains filing and closure. Hosted governance evidence is inspected without
  counting unrelated product CI failures as a reporting failure.
- The central rollout inventory names the member issue, commit and verification
  state, and `uibcdf/molsyssuite#60` closes only after every entry is resolved
  or excepted.

The normative contract is `devguide/reporting_protocol.md`. Member-specific
validators are the guards for their own local machinery.

## Local implementation issues

Open an issue in a member after confirming its exact missing surfaces. Link
each issue here and in the central issue; no local issue is inferred from the
static path inventory alone.

## Dependencies and risks

Existing queues may contain historical documents without issue identities.
Classify archival context separately from active reports and preserve it.
Issue-state synchronization needs authenticated GitHub inspection, while the
offline guard must remain useful without network access.

## Provenance

Inspection date: 2026-09-27. Host: the MolSysSuite Linux development checkout.
Commands: `python devtools/scripts/suite_status.py` and `git -C ../<member>
ls-tree -r --name-only origin/main` for all 15 registered members. This is a
configuration audit; no Python runtime or package version was measured.
