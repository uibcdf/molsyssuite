# Repository ownership contract

This document is normative for deciding where MolSysSuite work is tracked.

## Governance hierarchy

MolSysSuite is a first-class MOLI component with delegated internal governance.

MOLI owns platform-wide contracts and the shared engineering baseline. MolSysSuite owns modeling-ecosystem governance and may add stricter domain profiles without weakening inherited MOLI policy.

## Central MolSysSuite ownership

`uibcdf/molsyssuite` owns a theme when its acceptance changes a modeling-domain policy, compatibility contract, admission/classification rule, collective validation, or integration shared by two or more MolSysSuite members.

Examples include member dependency topology, suite-specific acquisition routes, collective E2E, member classification, component labels, and modeling-ecosystem rollouts.

## MOLI ownership

A theme belongs to `uibcdf/moli` when it changes a contract between MolSysSuite and another MOLI component or changes the platform-wide engineering baseline.

Examples include the baseline Python range, common Ruff/pytest contract, public release-version semantics, and Scientific Context ↔ MolSysSuite interoperability.

MolSysSuite may own rollout/admission state for its members while MOLI owns the underlying baseline.

## Component ownership

A member repository owns a defect or proposal confined to that component. A defect in a shared dependency remains with the repository that can fix it; downstream manifestations link rather than duplicate analysis.

## Coordinated implementation

A central issue may require local implementation issues. The central record owns rationale and collective acceptance; local records own code, tests, and component-specific evidence.

## Reporting lifecycle

MolSysSuite retains its mature issue-backed reporting lifecycle, which is compatible with and may be stricter than the MOLI universal lifecycle.

Every queued report has an owning GitHub issue. Meaningful resolved history is archived rather than deleted.

## Applicability and exceptions

Governance has four layers:

1. MOLI platform/scientific governance;
2. MOLI shared engineering policy;
3. MolSysSuite modeling-domain governance and inherited-policy profiles;
4. repository-local rules.

An exception must be explicit, tracked, justified, and time-bounded. The authoritative MolSysSuite member/capability registry remains `suite.toml`.
