---
summary: Require cross-component improvement feedback and shared stewardship.
issue: uibcdf/molsyssuite#15
status: resolved
opened: 2026-09-07
closed: 2026-09-07
verification: inspected
area: [governance, collaboration]
guard: tests/test_governance.py::GovernanceTests::test_cross_component_feedback_is_a_universal_policy
normative: devguide/cross_component_feedback.md
blocked_by: []
supersedes: []
---

# Cross-component improvement feedback

## What

Make reporting a sibling component's limitation an explicit contributor responsibility,
not an optional courtesy.

## How

Define a provider-owned, consumer-evidenced handoff and require cross-links for local
workarounds. Separate reporting and triage from promises about implementation priority.

## Why

All MolSysSuite components are UIBCDF team developments. Keeping a provider limitation
only inside consumer code fragments the suite and deprives the provider of actionable
integration evidence.

## Resolution

The normative policy now assigns responsibility to both sides of the handoff and keeps
prioritization compatible with stabilization cohorts.
