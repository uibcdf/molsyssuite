---
summary: Complete delayed Zenodo ingestion handling after paired archives became public.
issue: uibcdf/molsyssuite#49
status: resolved
opened: 2026-09-25
closed: 2026-10-01
verification: measured
area: [governance, archival, ci]
guard: tests/test_zenodo_recovery.py
normative: devguide/zenodo_policy.md
blocked_by: []
supersedes: []
---

# Monitor delayed Zenodo ingestion

**Status:** Resolved. The common recovery contract and provider are published;
both initial consumers pass exact-tag and complete covered-release hosted checks.

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
- [x] Define the longer/resumable outer window, retry/final escalation threshold,
  and economical read-only recovery route from observed ingestion behavior.
- [x] Link component adoption evidence for that recovery contract.

## Local implementation issues

uibcdf/molsysmt#273 and uibcdf/molsysviewer#132 own the local recovery workflow
adoptions. The earlier #195/#82 references concern distribution/release constraints,
not ownership of these verification implementations. uibcdf/molsyssuite#24 owns
the accepted archival vocabulary.

## Implementation: 2026-10-01

The common contract now specifies a 72-hour operational outer window anchored
to original publication, nominal six-hour scheduled probes, a manual exact-tag
route and explicit pending/invalid/absent/unavailable meanings. The threshold is
a conservative maintainer intervention choice, not an inferred Zenodo SLA.

The central provider queries complete bounded release and concept-version lists
once per run, reuses `audit_zenodo.verify_record`, and retains sanitized exact
file evidence. Fixed adoption cutoffs keep overdue releases visible; neither
rolling lookbacks nor expiring artifacts own the recovery queue. Malformed or
truncated discovery is inconclusive. The workflow pins its own source identity
with the documented reusable-job context and installs no component runtime.

Thirteen focused semantic regressions cover the pending/72-hour boundary, late
recovery, unavailable-versus-absence distinction, immutable publication clock,
invalid and ambiguous records, file identity/checksums, fixed discovery and API
pagination. The initial test-first run could not import the missing provider;
all thirteen pass after implementation. Member publication and hosted evidence
are pending below; this record remains partial until that adoption is verified.

## Dependencies and risks

The accepted policy now settles the operational window and complete recovery
route. GitHub scheduling can be delayed or dropped; maintainers retain manual
follow-up and account-side investigation. Source archival verification remains
separate from scientific, Conda and npm release evidence.

## Provenance

2026-10-01, coordination host, Python 3.13.15. Bounded anonymous GETs for Records
22959294/22959304 and `audit_zenodo.verify_record` against the registered inventory
passed. Raw API responses stayed under /tmp; no account configuration, credential,
webhook receiver or raw delivery payload was accessed or committed.


## Resolution and measured adoption — 2026-10-01

Implementation commit `b78fa9d30d46ce5607999cdecae85cf6c03f5fcd` supplies the
accepted policy and initial provider. Final provider `2cc2d9bfe80f14a981d40bc109ecdf2af39b693b` adds
the unindexable-version evidence correction. The new regression failed before
that fix and passes afterward. All fourteen focused regressions pass. A
controlled change of the outer window to 15 minutes makes the pending-state
regression fail, directly protecting the original false-absence mechanism.
The initial complete central suite passed 177 tests; final hosted governance
[36843000280](https://github.com/uibcdf/molsyssuite/actions/runs/36843000280)
passed on the hardened provider. Changed Python Ruff lint/format and offline
governance passed before publication. Test addressability and relevance are
both recorded: this module exercises states, exact deadlines, late recovery,
immutable publication time, malformed identity/files and complete discovery.

Direct anonymous probes found the paired exact public records. Final hosted
evidence below independently matches the registered record IDs, version/concept
DOIs and exact source ZIP names, sizes and checksums. Native logs also prove
the hardened provider source identity and actual successful probe step; job
success alone is not used as proof of archival.

| Consumer | Route | Hosted run | Exact caller source |
| --- | --- | --- | --- |
| uibcdf/molsysmt | exact | [36843304931](https://github.com/uibcdf/molsysmt/actions/runs/36843304931) PASS | `3dfdd51ee8f841eec3940cd161b988c98aae1e16` |
| uibcdf/molsysmt | scan | [36843305017](https://github.com/uibcdf/molsysmt/actions/runs/36843305017) PASS | `3dfdd51ee8f841eec3940cd161b988c98aae1e16` |
| uibcdf/molsysviewer | exact | [36843304681](https://github.com/uibcdf/molsysviewer/actions/runs/36843304681) PASS | `a3dc5f768dd1e020913cdd4d3d0355aeab5af20b` |
| uibcdf/molsysviewer | scan | [36843306658](https://github.com/uibcdf/molsysviewer/actions/runs/36843306658) PASS | `a3dc5f768dd1e020913cdd4d3d0355aeab5af20b` |

Local adoption issues uibcdf/molsysmt#273 and uibcdf/molsysviewer#132 are
resolved with permanent records and the local normative citation contract.
Final member evidence commits are `3e5aea30fdfb9afda3a842573567974f7efa33e6` and
`e66762449ea30180c0e1b39b1276f09b0aa3451c`. MolSysMT's devguide validator and
MolSysViewer's reporting checks passed (125 tests before archival, 123 after
its queue/archive parameter inventory changed); its generated index passes.
The attempted unittest discovery of the Viewer pytest module collected zero
tests and is not counted as verification; the actual pytest reporting run is.
No scientific runtime or execution review was performed.

### Common guide distribution

All fifteen member guides were distributed with `sync_vendored_guides.py`
from committed canonical source. Guide SHA256:
`234ba072047b5f08c796526e4652a21f4456fa6440b5fd2f7f05fecf3668d000`.
Initial automatic guide audits 36840421458 and 36840421626 ran before consumer
distribution and failed. Final post-distribution
[component audit 36841479884](https://github.com/uibcdf/molsyssuite/actions/runs/36841479884)
and [vendored audit 36841479725](https://github.com/uibcdf/molsyssuite/actions/runs/36841479725)
pass, including every member. Subsequent consumer changes are provider pin,
local normative documentation and archived evidence; guide bytes and root
contributor routes remain unchanged. No consumer guide was edited manually.

| Member | Guide publication commit |
| --- | --- |
| uibcdf/smonitor | `8c053fd244ce28f1fe7c47220697d73d9b749438` |
| uibcdf/argdigest | `ffb5d2c1f1e3a98fdd188911cc240cf1c036f58a` |
| uibcdf/depdigest | `bfbdf9fb116c70ba1d2582961291b36bd5cc3fe6` |
| uibcdf/pyunitwizard | `b87040ed70735e97258668300542180f0e0c6ffe` |
| uibcdf/pytest-receptor | `e51ee7d8425bae21a78f0985f0a960346d0dea26` |
| uibcdf/gh-run-receptor | `c0ea07aba87f87f4e2c54dd72773fa8b1acf2a8b` |
| uibcdf/molsysmt | `f09ed3b4c73a8ecdd0cf2341a62ec450dbadcc7d` |
| uibcdf/molsysviewer | `cfb5def953fc148362a7de4640e39fae10ebf9d1` |
| uibcdf/topomt | `b119103cffb7c515bda938fc5d5899313b41a489` |
| uibcdf/pharmacophoremt | `9cbec4ab806e5f9fa96219ef9eef9dd9967a75a6` |
| uibcdf/elastnetmt | `290db1c798407f5062055de6f7e0fff1e3579e0e` |
| uibcdf/dockingmt | `4ab0688d24fff5a8daddf645a9e77d23a6b08642` |
| uibcdf/ackredit | `c4e0d60228824bf5ad2b3b80ff1d48ad6bc85115` |
| uibcdf/lindelint | `a512dc68a2e4e824c17fdb66abcb8afccf2bba96` |
| uibcdf/molsys-ai | `9544a8fa54ec2423b9076f7a54e3d0337c3f6a60` |

### Outcome and limits

All acceptance criteria are met for the common contract and two initial
consumers. Other required members adopt this prospective recovery contract
before their next applicable public release; they are not claimed to have
changed workflows already. Equivalent implementations and exceptions are
documented in the common policy. Retained legacy one-off component helpers
are historical diagnostics; current sign-off uses explicit common-provider
verified evidence, never a green pending job.

The observed records preserve source snapshots only. No package promotion,
webhook replay, account mutation, manual deposit, release publication or new
scientific CI requirement occurred. Direct commits/pushes were authorized by
the principal maintainer; skipped component commits retain their existing
nightly recovery responsibilities. Original member worktrees remain intact.
