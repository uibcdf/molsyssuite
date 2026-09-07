---
summary: Publish MOLSYSSUITE_GUIDE.md as the suite ambassador in every component.
issue: uibcdf/molsyssuite#16
status: active
opened: 2026-09-07
closed:
verification: inspected
area: [governance, documentation]
guard: tests/test_governance.py::GovernanceTests::test_component_guide_is_a_universal_policy
normative: MOLSYSSUITE_GUIDE.md
blocked_by: []
supersedes: []
---

# MolSysSuite guide ambassador

## What

Place a synchronized `MOLSYSSUITE_GUIDE.md` at the root of every component and require
contributors to read it through the component's root `AGENTS.md`.

## How

Keep one canonical, concise operational guide in `uibcdf/molsyssuite`; mark component
copies generated and read-only; compare them byte-for-byte in the central conformance
guard; and route detailed questions to complete central normative documents.

## Why

Governance that exists only in the central repository is easy to miss during ordinary
component work. The local ambassador makes suite membership and shared stewardship
visible without copying the entire developer guide into every repository.

## Acceptance criteria

- The guide covers ownership, reporting, shared stewardship, common tooling, cohorts,
  and when to consult the central repository.
- `suite.toml` declares it a universal policy.
- The conformance guard detects a missing, modified, or unreferenced copy.
- Every registered component receives the exact copy and references it from `AGENTS.md`.
- Vendored-guide formatting and drift behavior is consistent with `uibcdf/molsyssuite#12`.
