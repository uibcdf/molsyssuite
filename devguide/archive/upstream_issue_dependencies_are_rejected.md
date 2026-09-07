---
summary: Report dependency fields reject valid upstream GitHub issues.
issue: uibcdf/molsyssuite#14
status: resolved
opened: 2026-09-07
closed: 2026-09-07
severity: medium
verification: reproduced
area: [governance, reporting]
guard: tests/test_governance.py::GovernanceTests::test_report_dependencies_may_reference_upstream_github_issues
normative: devguide/reporting_protocol.md
blocked_by: []
supersedes: []
---

# Upstream issue dependencies are rejected

## What

The shared report schema permits only `uibcdf/<repo>#<number>` in `blocked_by` and
`supersedes`. It cannot represent an upstream GitHub dependency.

## How

SMonitor's catalog-warning report is blocked on `pytest-dev/pytest-xdist#1372`. The
current expression rejects that stable GitHub identity even though report ownership
itself correctly remains in `uibcdf/smonitor`.

## Why

The limitation forces a false status, an empty dependency field, or an ad hoc prose-only
link. All three weaken synchronization between the issue and developer-guide record.

## Acceptance criteria

- Owning report issues remain restricted to the appropriate MolSysSuite repository.
- Dependency fields accept `<owner>/<repository>#<positive integer>` GitHub identities.
- The normative protocol distinguishes ownership from external dependency references.

## Resolution

Dependency references now accept stable GitHub issue identities from any owner while
the owning report issue remains restricted to its MolSysSuite repository. The regression
uses SMonitor's real pytest-xdist blocker.
