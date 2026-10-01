---
summary: Adopt durable working-instruction lifecycle and scoped routes in every member.
issue: uibcdf/molsyssuite#66
status: active
opened: 2026-10-01
closed:
verification: inspected
area: [governance, onboarding, tooling]
guard: tests/test_agent_instructions.py
normative: devguide/working_instructions_policy.md
blocked_by: []
supersedes: []
---

# Durable working instructions across MolSysSuite members

**Reported:** 2026-10-01 in the suite counterpart of MOLI#20.
**Status:** Starter routes exist; normative member policy and existing-member
adoption are being completed under this issue.

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
