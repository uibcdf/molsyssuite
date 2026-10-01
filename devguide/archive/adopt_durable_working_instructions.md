---
summary: Adopt durable working-instruction lifecycle and scoped routes in every member.
issue: uibcdf/molsyssuite#66
status: resolved
opened: 2026-10-01
closed: 2026-10-01
verification: inspected
area: [governance, onboarding, tooling]
guard: tests/test_agent_instructions.py
normative: devguide/working_instructions_policy.md
blocked_by: []
supersedes: []
---

# Durable working instructions across MolSysSuite members

**Reported:** 2026-10-01 in the suite counterpart of MOLI#20.
**Status:** Resolved: normative member policy, starter validation and all 15
existing member instruction routes are implemented and independently checked.

## What

Make accepted durable contributor actions discoverable in correctly scoped
AGENTS.md files, without turning every technical finding into another rule.

## How

Register a suite-owned policy, preserve local instructions, add thin canonical
routes at root and devguide scope, and reuse one mechanical checker for central
governance, generated components and the hosted member-guide inventory. Deliver
the canonical summary through the registered guide sync tool.

## Why

The starter path was fixed in 430b4b3/8b36a1f, but existing members do not yet
share instruction placement and route validation. Shared knowledge needs an
explicit reviewed owner and applicability rather than duplicated defect history.

## What is measured and what is assumed

An isolated, fetched-main inventory finds root AGENTS.md in all 15 members;
devguide/AGENTS.md exists in GH Run Receptor, MolSysMT and MolSysViewer. Three
members use different guide landing layouts; local reporting protocols remain
the authority for queue/archive paths. File presence is not semantic correctness.

## Alternatives and refuted paths

Do not regenerate existing root files from the starter or require one archive
layout. Do not require a separate instruction issue for each defect or infer
member adoption from upstream MOLI closure.

## Scope and exclusions

All registered members, including MolSys-AI. Product/scientific conventions and
future scientist notification behavior (#65) stay with their respective owners.

## Acceptance criteria

- Registered normative placement, feedback and exception rules.
- Generated member passes the same active-route checks without manual repair.
- Existing member instruction files preserved and required routes adopted, or
  complete bounded exceptions with owning issues.
- Hosted 15-member administrative audit and central governance pass.

## Local implementation issues

This central issue owns shared route delivery. Distinct local work or exceptions
need their own owner; no component scientific implementation is changed.

## Dependencies and risks

Mechanical routes cannot establish instruction quality; relevance is reviewed.
Preserve existing local work and specialized nested instructions during rollout.

## Provenance

2026-10-01, Linux, Python 3.13; fetched isolated member main checkouts, suite
status, root/nested instructions and starter source inspected. Original component
worktrees, including ArgDigest and TopoMT local changes, are preserved.

## Resolution, 2026-10-01

Provider 406e45e76b57e857372d6712a44ca2d40f413152 registers the member-owned
normative rule and one reusable route checker. Its ten regression tests reject
missing files, hidden or misplaced routes, missing local targets, unregistered
claims and malformed, duplicate or expired exceptions. Generation and hosted
audits call that provider; the three starter tests and all 224 administrative
tests pass. These assertions protect route delivery, not instruction semantics.

All 15 members received root and nested routes and byte-identical canonical
guidance; original specialized instructions were retained. Local index gates
passed, including MolSys-AI's equivalent layout, and MolSysMT's developer-guide
validator passed. Native governance 36873854500, member-guide audit 36874496180
and vendored-guide audit 36874500880 passed. Sources and delivered commits are
recorded in devguide/rollouts/working_instructions.md. No exception is required.

The shared route rollout is owned by this central issue; no distinct local
scientific implementation or publisher change was needed. Upstream MOLI#20
acceptance did not substitute for member adoption. #65 remains the owner of
future scientist-facing reporting/notification behavior. No policy-caller bump,
scientific rerun or package publication was performed.
