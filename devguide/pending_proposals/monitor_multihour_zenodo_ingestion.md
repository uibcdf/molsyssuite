---
summary: Complete delayed Zenodo ingestion handling after paired archives became public.
issue: uibcdf/molsyssuite#49
status: partial
opened: 2026-09-25
closed: 
verification: measured
area: [governance, archival, ci]
guard: 
normative: devguide/zenodo_policy.md
blocked_by: []
supersedes: []
---

# Monitor delayed Zenodo ingestion

**Status:** Partial. Both exact public source archives are verified; the common
longer/resumable recovery window remains to be settled.

## What

The 0.22.4 MolSysMT and 0.23.4 MolSysViewer releases exceeded their 900-second
Zenodo verification window. Initial empty queries and accepted webhook deliveries
were pending ingestion, not proof of permanent absence or failed package release.

## How

The registered public records are independently rechecked with the existing
`audit_zenodo.verify_record` contract, including repository/version identity,
public/open software metadata, distinct version/concept DOIs and exact file
names, sizes and checksums. Keep delayed-state policy and rerunnable read-only
verification separate from release mutation. No hook replay or manual deposit is
needed for these now-public snapshots.

## Why

A brief runner wait can report an archival failure while ingestion is still in
progress. A bounded recovery procedure should preserve truthful state without
occupying a hosted runner for hours or repeating accepted publication events.

## What is measured and what is assumed

On 2026-10-01 the anonymous Records API and existing semantic verifier matched:

| Repository/version | Record / version DOI | Concept DOI | Exact source file |
| --- | --- | --- | --- |
| uibcdf/molsysmt 0.22.4 | 22959294 / 10.5281/zenodo.22959294 | 10.5281/zenodo.1298752 | uibcdf/molsysmt-0.22.4.zip, 150833579 bytes, md5:9927d9511e5946eb708254d89d427d0d |
| uibcdf/molsysviewer 0.23.4 | 22959304 / 10.5281/zenodo.22959304 | 10.5281/zenodo.18072956 | uibcdf/molsysviewer-0.23.4.zip, 23694420 bytes, md5:2cfe76a5ea9ec2894964926db81c2609 |

Their record creation timestamps are 2026-09-25T12:36:35Z and 12:36:47Z,
about 87 minutes after the issue's recorded 11:09 UTC GitHub publication.
That observed pair delay is distinct from the maintainer's reports of other
multi-hour queues. Registered evidence has been `verified` since 2026-09-26;
no Conda/npm/wheel coverage is inferred from these source ZIPs.

## Alternatives and refuted paths

Blindly replaying accepted events risks duplicate account-side work. Holding a
hosted runner for a multi-hour wait is unnecessary when read-only recovery can
be dispatched or scheduled. A green Conda gate does not prove archival.

## Scope and exclusions

Shared delayed-state/recovery policy and exact-version archival follow-up. Core
scientific execution reviews remain deferred; package promotion is separate.

## Acceptance criteria

- [x] Independently verify both exact public source archives and DOI/file identity.
- [x] Record the verified inventory without treating the early absence as permanent.
- [ ] Define the longer/resumable outer window, retry/final escalation threshold,
  and economical read-only recovery route from observed ingestion behavior.
- [ ] Link component adoption evidence for that recovery contract.

## Local implementation issues

uibcdf/molsysmt#195 and uibcdf/molsysviewer#82 own exact release verification;
uibcdf/molsyssuite#24 owns the accepted archival vocabulary. Further local
workflow issues follow only after the common recovery mechanism is accepted.

## Dependencies and risks

The existing policy states bounded retries but does not settle the requested
multi-hour operational window. Keeping this proposal partial retains that work;
source archival verification alone is insufficient for its full closure.

## Provenance

2026-10-01, coordination host, Python 3.13.15. Bounded anonymous GETs for Records
22959294/22959304 and `audit_zenodo.verify_record` against the registered inventory
passed. Raw API responses stayed under /tmp; no account configuration, credential,
webhook receiver or raw delivery payload was accessed or committed.
