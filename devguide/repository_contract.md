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
