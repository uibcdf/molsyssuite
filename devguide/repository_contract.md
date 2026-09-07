# Repository ownership contract

This document is normative for deciding where MolSysSuite work is tracked.

## Central ownership

`uibcdf/molsyssuite` owns a theme when its acceptance changes a policy, compatibility
contract, release procedure or integration shared by two or more member repositories.
It also owns defects in suite-level automation and collective acceptance tests.

Examples include supported Python versions, common development tools, reporting
vocabulary, cross-component interfaces and coordinated release requirements.

## Component ownership

A member repository owns a defect or proposal whose acceptance and implementation are
confined to that component. A defect in a shared dependency remains with the repository
that can fix it; downstream manifestations link to that issue instead of duplicating its
analysis.

## Coordinated implementation

A central issue may require local implementation issues. The central record owns the
rationale, suite-wide acceptance criteria and adoption state. Each local record owns its
code, tests and component-specific evidence. They cross-reference one another using
`uibcdf/<repo>#<number>`.

The central issue closes only when its collective acceptance criteria are met. Finishing
the first component does not close a suite-wide decision.

Do not open an implementation issue in every member repository automatically. Create one
only where a concrete local change is required.

## Shared stewardship

Ownership is not isolation. Contributors who discover a provider limitation while
developing a consumer follow [`cross_component_feedback.md`](cross_component_feedback.md):
they file actionable evidence in the provider repository and cross-link any consumer
workaround or blocked work. Provider maintainers own triage and implementation priority;
the discovering contributor owns a clear handoff.

## Required reporting lifecycle

Every member repository follows the issue-backed lifecycle defined by
[`reporting_protocol.md`](reporting_protocol.md), irrespective of whether work is owned
centrally or locally. The central repository owns the common vocabulary and minimum
contract. Each member owns its issues, reports, archive, local path mapping, indexes,
validator and board synchronization for component work.

Member repositories may keep established layouts and stricter workflows. Compatibility
is semantic: common statuses and issue identity must retain their meaning, while a local
archive may be flat, typed, or use a documented established name.

## Applicability and exceptions

Common policy has three layers:

1. a small universal governance core;
2. profile rules, such as those for a Python library or scientific component;
3. repository-local rules and tools.

Every shared rule must name the profiles to which it applies. A repository may deviate
only through a documented exception that states the reason, expiration condition and
tracking issue. An exception is visible debt, not a silent fork of the policy.

The authoritative member and profile registry is `suite.toml`. Human-readable lists must
be generated from it or clearly marked as non-authoritative.
