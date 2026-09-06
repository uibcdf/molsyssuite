# Reporting protocol

This document is normative. It governs `pending_bugs/`, `pending_proposals/`, `archive/`
and their relationship with the `uibcdf/molsyssuite` issue board.

It adopts the repository-independent vocabulary proven in MolSysMT and MolSysViewer.
Repository-specific validators, labels and queue layouts may differ; the meanings below
must not.

## The rule

**If a suite-wide theme deserves a pending document, it deserves a central issue.**

The two records have different jobs:

| Record | Holds | Changes |
| --- | --- | --- |
| developer-guide document | analysis, measurements, alternatives and refuted paths | continuously |
| GitHub issue | state and settled facts needed outside the repository | at opening and closing |

One independently closable theme has one central issue and one or more documents. Plans,
inventories and meeting notes do not enter a queue until split into closable themes.

## Identity and ownership

The issue reference is the stable identity. Cross-repository references use
`uibcdf/<repo>#<number>`, never a path into a sibling's developer guide.

Use [`repository_contract.md`](repository_contract.md) to decide whether a theme is
central or local. A central decision may link local implementation issues; it does not
absorb their implementation analysis.

## Front matter

Every queued or archived report starts with:

```yaml
---
summary: One line describing the theme.
issue: uibcdf/molsyssuite#1
status: open
opened: 2026-09-06
closed:
severity: medium
verification: asserted
area: [governance]
guard:
normative:
blocked_by: []
supersedes: []
---
```

`severity` is required only for bugs and is one of `critical`, `high`, `medium`, `low`.

Statuses are:

- open set: `open`, `active`, `blocked`, `partial`;
- closed set: `resolved`, `withdrawn`, `superseded`.

Verification describes the report's diagnosis, not the maturity of a feature:

- `reproduced`: executed and failed as described;
- `measured`: supported by recorded measurements and their command;
- `inspected`: verified by reading source or configuration;
- `upstream`: confirmed to originate outside the suite repository;
- `asserted`: believed but not yet checked.

Domain-specific evidence vocabularies remain local. A viewer, scientific library and CI
receiver do not prove their capabilities in the same way.

## Filing

1. Open the issue first to obtain its number.
2. Copy `templates/report.md` into the appropriate queue and fill its front matter.
3. Write the expanded What / How / Why analysis and acceptance criteria.
4. Regenerate the queue indexes.
5. Commit the issue and document references together; do not leave a cross-session gap.

The opening issue is telegraphic:

```text
What — the observed defect or proposed outcome
How — reproduction or implementation outline
Why — impact and evidence
Record — devguide/pending_.../<name>.md
```

Incoming issues may remain without a document while awaiting triage. Every queued
document must have an issue; not every issue must acquire a document.

## Closing

A resolved theme requires the outcome, its record and one durable guard:

- a test or automated check named by `guard`; or
- a normative document named by `normative` when the outcome is a policy.

Set `status` and `closed`, move the record to `archive/`, regenerate the index, and close
the issue with the decision or fix, user-visible consequence, guard or normative record,
and archived record path.

**Archive, never delete.** In an open document, correct a false claim in place. In an
archived document, append a dated correction and do not edit the original claim.

## Labels

- kind, exactly one: `bug`, `proposal`, `enhancement`, `documentation`;
- state, zero or one: `in-progress`, `blocked`, `partial`;
- triage: `needs-triage` for reports not yet attended.

No state label means open and unstarted. GitHub's closed state represents completion; a
separate `done` label is unnecessary.

## Security

An exploitable finding is not opened as a public issue. Report it through a private
GitHub security advisory. The public protocol resumes after a fix can be disclosed.

## Automated checks

Run locally:

```bash
python devtools/scripts/devguide_index.py
python devtools/scripts/validate_governance.py
```

The validator is deliberately offline. Board-state synchronization requires GitHub
credentials and remains a separate concern.
