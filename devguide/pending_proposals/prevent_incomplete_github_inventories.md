---
summary: Prevent false remote audit conclusions from incomplete GitHub inventories.
issue: uibcdf/molsyssuite#171
status: active
opened: 2026-11-12
closed:
verification: reproduced
area: [governance, tooling]
guard: tests/test_github_inventory.py
normative: devguide/reporting_protocol.md
blocked_by: []
supersedes: []
---

# Complete acquisition before remote absence decisions

**Reported:** Diego requested suite engineering review after MolSysMT #587's
500-issue cap falsely lost valid old records. MolI #85 owns direct components.
**Status:** Central fixes/guards pass; complete source review, owner handoffs,
canonical instruction delivery and published native receiving are in progress.

## What

Acquisition scope and presentation limits were conflated. The existing MolSysMT
issue-pagination correction and already paginated MolSysViewer reader are
preserved. This review finds a central 1,000-label cap hiding a later deviation
and a release watcher accepting zero observed pages before possible creation.
Both new consumer guards fail on the original central source and pass after
the shared reader is used. Two component label readers still cap at 200;
controlled 201-label transports reproduce their false missing-label results.
Actual current boards are not alleged to exceed that cap.

## How

Read immutable published script/instruction sources for all seventeen registered
members, preserving primary dirty/ahead/behind work. Distinguish actual absence
audits from point reads, bounded exploratory queries, conservative CI fallback
and historical readiness notes. Inspect existing reusable routes before adding
code. MolSysMT/Viewer provide qualified issue-specific owner implementations;
the central watcher has native pagination but needs completeness validation.

Central `github_inventory.acquire_inventory` owns the reusable native acquisition
contract for two actual central consumers. Validate all returned pages and
resource identities, normalize states, exclude PRs by key presence and refuse
failed/zero-page/malformed/duplicate/over-bound evidence. Keep mutation and
interpretation in each consumer. The reporting protocol and canonical member
guide carry the lasting human/agent action; delivery uses the registered sync tool.

## Why

False absence can create duplicate issues, block valid labels or invalidate
existing records. Raising a silent cap defers the defect. Complete acquisition
and bounded summaries serve different purposes and should remain separate.

## Measurements and limits

The central guards reproduce both original failures and pass with the shared
reader. The selected inventory/watcher/label suite passes nineteen tests with
published Pytest Receptor 1.2.3. Native resource traversal and direct known-issue
readbacks, reviewed member sources, owner issues and actual delivered commits
will be retained in the closeout receipt. No component scientific test is run.

The source search covers tracked administrative/script/text extensions and
instructions at seventeen exact commits. It is a bounded source review, not
proof of every dynamic call path or an ecosystem scientific certificate.
PeptideMT's first lazy blob read timed out; only the subsequent bounded bulk
acquisition and completed scan qualify that member's source inspection.

## Alternatives and refuted paths

- Raising the old numeric cap retains false absence and is rejected.
- Importing private MolSysMT/Viewer reconciler helpers would invert ownership;
  preserve their qualified record adapters and expose the shared administrative
  operation centrally for its two real central consumers.
- Search-index results or capped connector responses remain exploratory. Use a
  complete native scope or record unknown instead of inventing an empty board.
- Refactoring every bounded CI search is unnecessary: a conservative positive
  witness/fallback is different from an exhaustive absence assertion.

## Scope and exclusions

Suite administrative tools, member engineering source/instruction review and
normal canonical-guide delivery. Component implementation fixes and scientific
qualification stay with their teams. MolI #85 stays independently owned. No
package/policy release, mandatory scientific matrix, environment switch, broad
repository cleanup or silent client dependency/SDK pin update is commissioned.

## Acceptance criteria

- Complete declared acquisition or explicit unknown; no false empty/absence or
  duplicate-prone mutation after failure. Meaningful later-page/state/PR/empty/
  malformed/bound transport guards and both actual central consumers pass.
- All seventeen source reviews have immutable scope, findings and dispositions.
  Concrete component defects have owning follow-ups; prior fixes remain closed.
- The accepted common action is published and all registered guide copies are
  byte-verified, separately from implementation adoption and instruction defects.
- Exact final central native evidence, owner notices and scoped resource cleanup
  are retained. Index/offline governance and relevant quality checks pass.

## Local implementation issues

MolSysMT #724 and GH Run Receptor #85 own their label-cap fixes. Earlier MolSysMT #587
and MolSysViewer #264 do not certify those distinct operations or every member.
Their exact new issue identities and receiving are recorded at closeout.

## Publication checkpoint

Publish the locally qualified canonical guide and central implementation as an
incremental `[skip ci]` source, deliver the registered generated copies, then
perform the final exact-source central governance and applicable byte/instruction/
label checkpoint. The Mamba native acquisition operation is unchanged; this
reader change qualifies its inventory/notification boundary through focused
transport and existing watcher tests, without repeating native environment solves.
Member guide-only commits retain their owner cadence; no member workflow is
manually dispatched for this administrative delivery.

## Dependencies and risks

Native complete traversal is not transactional freezing. Dynamic changes,
permissions, malformed data and resource bounds remain explicit. Refuse unknown
evidence; do not delete records. Member implementations and direct MolI adoption
remain outside the central receiving closure.

## Provenance

2026-11-12; named Linux/Python 3.14.7 environment, published Pytest Receptor 1.2.3
in an isolated target. Twelve inherited pip findings and the #82 pause remain.
Temporary clones use immutable published sources; primary work is preserved.
