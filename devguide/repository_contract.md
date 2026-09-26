# Repository ownership contract

This document is normative for deciding where MolSysSuite work is tracked.

## Governance hierarchy

MolSysSuite is a first-class MOLI component with delegated internal governance.

MOLI governs MolSysSuite as a platform component. MolSysSuite owns the normative rules for its registered members, including their engineering baseline.

## Central MolSysSuite ownership

`uibcdf/molsyssuite` owns a theme when its acceptance changes a modeling-domain policy, compatibility contract, admission/classification rule, collective validation, or integration shared by two or more MolSysSuite members.

Examples include member dependency topology, suite-specific acquisition routes, collective E2E, member classification, component labels, and modeling-ecosystem rollouts.

## MOLI ownership

A theme belongs to `uibcdf/moli` when it changes a contract between MolSysSuite and another MOLI component or a platform obligation of MolSysSuite itself.

Examples include scientific quantity integrity, issue feedback, visibility and provenance boundaries, and Scientific Context ↔ MolSysSuite interoperability. The Python range, Ruff/pytest gate and release-version rules of suite members belong to MolSysSuite.

MolSysSuite owns both normative member policy and its rollout/admission state. It remains accountable for the platform contracts it owes as a MOLI component.

## Component ownership

A member repository owns a defect or proposal confined to that component. A defect in a shared dependency remains with the repository that can fix it; downstream manifestations link rather than duplicate analysis.

## Coordinated implementation

A central issue may require local implementation issues. The central record owns rationale and collective acceptance; local records own code, tests, and component-specific evidence.

## Reporting lifecycle

MolSysSuite retains its mature issue-backed reporting lifecycle, which is compatible with and may be stricter than the MOLI universal lifecycle.

Every queued report has an owning GitHub issue. Meaningful resolved history is archived rather than deleted.

## Applicability and exceptions

Governance has three ownership layers:

1. MOLI platform/scientific contracts binding MolSysSuite as a component;
2. MolSysSuite engineering, modeling-domain and member-adoption policy;
3. repository-local implementation rules.

An exception must be explicit, tracked, justified, and time-bounded. The authoritative MolSysSuite member/capability registry remains `suite.toml`.
