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
**Status:** Four of five initial targets fully adopted. Pytest Receptor's new
machinery is adopted, with a bounded identity exception for seventeen
pre-protocol resolved documents under `uibcdf/pytest-receptor#10`.

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

**LinDelInt adopted on 2026-09-27:** local issue
`uibcdf/lindelint#11` is closed with its record retained in the member's
archive. Commits `10aa0c8` and `ed588ab` added the template, generated
indexes, offline validator, documented wheel-guard profile and independent
reporting-governance job while preserving historical issue identities
`uibcdf/lindelint#6`, `uibcdf/lindelint#7` and `uibcdf/lindelint#9`.
Local index validation, three reporting tests, eight repository
tests and Ruff lint/format passed. On the archived-record commit `ed588ab`,
[hosted CI](https://github.com/uibcdf/lindelint/actions/runs/36356653703)
and the [MolSysSuite policy gate](https://github.com/uibcdf/lindelint/actions/runs/36356654032)
both passed. The CI run includes the dedicated reporting job; its scientific
matrix passed too, but that is not the basis for reporting adoption.

**PharmacophoreMT adopted on 2026-09-27:** local issue
`uibcdf/pharmacophoremt#8` is closed and archived. Commits `59aaef1` and
`98ecb45` added local guidance, template, offline validator, generated
indexes and an independent reporting-governance job while preserving the
active `#6` review and archived `#5` defect. The local index check, three
reporting tests and Ruff checks passed. On the exact archived-record commit,
[hosted CI](https://github.com/uibcdf/pharmacophoremt/actions/runs/36357376234)
and the [MolSysSuite policy gate](https://github.com/uibcdf/pharmacophoremt/actions/runs/36357376668)
both passed, including the dedicated governance job.

**ElastNetMT adopted on 2026-09-27:** local issue
`uibcdf/elastnetmt#16` is closed and archived. Commits `9ecc8f0` and
`9566707` added the missing bug queue and archive, template, offline
validator, generated indexes and independent reporting-governance job while
preserving the active `#14` review. The local index check, three reporting
tests and Ruff checks passed. On the exact archived-record commit, the
Reporting governance job passed in
[hosted CI](https://github.com/uibcdf/elastnetmt/actions/runs/36357927495),
and the [MolSysSuite policy gate](https://github.com/uibcdf/elastnetmt/actions/runs/36357927792)
passed. The overall CI workflow failed in scientific Python 3.11/3.12 cells;
that existing component and provider work remains under
`uibcdf/elastnetmt#14` and `uibcdf/lindelint#8`. The failed scientific cells
do not invalidate the separately passing reporting guard.

**MolSys-AI adopted on 2026-09-28:** the umbrella's local issue
`uibcdf/molsys-ai#2` is closed and archived. Commits `805a2cc` and `8ad5403`
completed its existing template, added generated indexes and an offline
validator, and introduced an independent reporting-governance workflow.
The exact archived-record
[hosted run](https://github.com/uibcdf/molsys-ai/actions/runs/36386362706)
passed. The umbrella gained no Python-package or scientific CI claim.
Its pre-existing resource-data examples still fail the separate
`scripts/validate_resources.py` check; this reporting adoption did not
change those files.

**Pytest Receptor machinery adopted on 2026-09-28, historical exception
open:** local implementation issue `uibcdf/pytest-receptor#8` is closed and
archived after commits `3226957`, `5e202f7` and `a4ea33a`. The active
CI-annotations proposal now has issue `uibcdf/pytest-receptor#9`; modern
archived reports `#4`, `#5` and `#6` retain their identities. The template,
generated queue and archive indexes, offline validator and independent
reporting workflow pass locally and in exact-commit
[hosted governance](https://github.com/uibcdf/pytest-receptor/actions/runs/36390398872)
and [MolSysSuite policy](https://github.com/uibcdf/pytest-receptor/actions/runs/36390399488).
Seventeen pre-protocol resolved records remain byte-preserved and indexed as
legacy register evidence. They do not yet all have GitHub issue identities;
`uibcdf/pytest-receptor#10` owns their bounded manifest and a 2026-12-31
review. The local guard rejects new issue-less reports and an expired review.
This historical identity exception is the remaining adoption debt in #60.

| Initial audit target | Reporting rollout state | Local issue |
| --- | --- | --- |
| Pytest Receptor | Machinery adopted; 17 legacy identities excepted pending review | `uibcdf/pytest-receptor#8`, `uibcdf/pytest-receptor#10` |
| PharmacophoreMT | Adopted; archive and hosted guard verified | `uibcdf/pharmacophoremt#8` |
| ElastNetMT | Adopted; archive and hosted guard verified; scientific CI red separately | `uibcdf/elastnetmt#16` |
| LinDelInt | Adopted; archive and hosted guard verified | `uibcdf/lindelint#11` |
| MolSys-AI | Adopted; hosted reporting guard verified | `uibcdf/molsys-ai#2` |

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

Completed local implementation issues: `uibcdf/lindelint#11`,
`uibcdf/pharmacophoremt#8`, `uibcdf/elastnetmt#16`,
`uibcdf/molsys-ai#2` and `uibcdf/pytest-receptor#8`. Pytest Receptor's
historical exception remains under `uibcdf/pytest-receptor#10`; its old
CI-annotations proposal now has `uibcdf/pytest-receptor#9`.

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
