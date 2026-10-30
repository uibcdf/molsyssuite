# Reporting protocol

This repository implements the common issue-backed lifecycle defined by
`uibcdf/molsyssuite` in its `devguide/reporting_protocol.md`.

## Identity and ownership

Component-local work uses `__REPOSITORY__#<number>`. Suite-wide rules and coordinated
changes use `uibcdf/molsyssuite`. Open the owning issue before creating a queued record.
Every queued document has an issue, although an incoming issue may await triage without
a document.

Agents follow the mandatory guide's
[external-publication authorization rule](../MOLSYSSUITE_GUIDE.md#human-approval-for-external-issues-and-pull-requests).
Before creating/publishing an issue or PR outside MolI's scope or in repositories
not owned by us, in particular outside `github.com/uibcdf`, obtain explicit
permission from Diego Prada Gracia or Liliana Marisol Moreno Vargas. A remote
draft PR counts. Without permission, prepare a reviewable internal finding for
the human. The issue-first lifecycle and generic feedback duty do not authorize
external publication; existing explicit authorization remains valid in its scope.

## Local paths

- `pending_bugs/`: open defects;
- `pending_proposals/`: open proposals;
- `archive/`: all resolved, withdrawn and superseded records.

Every report starts from `templates/report.md`. The issue holds public state; the
document holds analysis, measurements, alternatives and refuted paths.

## Closing

Set a closed status and date, name a durable test in `guard` or policy in `normative`,
move the record to `archive/`, regenerate indexes and close the issue with the outcome
and archived path. Archive, never delete. Append corrections to archived records rather
than rewriting their history.

## Offline checks

```bash
python devtools/devguide_index.py
python devtools/devguide_index.py --check
python -m pytest --receptor=llm tests/test_reporting_protocol.py
```
