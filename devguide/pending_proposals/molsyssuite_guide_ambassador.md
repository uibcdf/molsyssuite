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

## Rollout status — 2026-09-07

The canonical guide and byte-drift guard are published in `394779d`. Copies and root
`AGENTS.md` references are published in:

| Component | Commit |
| --- | --- |
| SMonitor | `72d9c5d` |
| ArgDigest | `db788d9` |
| DepDigest | `33c98d6` |
| pytest-receptor | `ca8f266` |
| gh-run-receptor | `f4c99f0` |
| MolSysMT | `79e9d66d9` |
| MolSysViewer | `6816e4c5` |
| PharmacophoreMT | `e60f829` |
| ElastNetMT | `6330da9` |
| PyUnitWizard | `f790544` |
| TopoMT | `1c991bf` |

All eleven registered components now carry the byte-identical guide and require it from
their root `AGENTS.md`. A central matrix workflow checks only this contract, independently
of unfinished Python/Ruff adoption, on relevant pushes, by manual dispatch, and weekly.
