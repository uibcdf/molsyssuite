---
summary: MolSysSuite becomes the authority for shared governance and reporting.
issue: uibcdf/molsyssuite#1
status: resolved
opened: 2026-09-06
closed: 2026-09-06
verification: inspected
area: [governance, reporting]
guard:
normative: devguide/reporting_protocol.md
blocked_by: []
supersedes: [uibcdf/molsysmt#156]
---

# MolSysSuite lacks a shared governance and reporting authority

**Reported:** 2026-09-06, after comparing coordination practices across the member
repositories.
**Status:** Resolved; the central protocol, ownership contract, registry and offline guard
are in place.

## What

Make `uibcdf/molsyssuite` the authority for policies and contracts shared by two or more
member repositories. Keep implementation decisions local and connect them to central
themes with stable issue references.

## How

Adopt the repository-independent reporting vocabulary already exercised by MolSysMT and
MolSysViewer. Add a machine-readable member registry, queue templates, generated indexes
and an offline validation gate. Introduce concrete Python and tooling standards later as
separate, independently decidable proposals.

## Why

MolSysSuite already holds collective checklists and E2E evidence, but it has no lifecycle
for shared decisions. The reporting vocabulary is duplicated in member repositories and
its ecosystem-wide future is tracked in MolSysMT rather than in the suite repository.

## What is measured and what is assumed

Inspected on 2026-09-06: the central issue board had no open or closed issues before this
record; the repository had no reporting protocol, issue templates or governance checks.
The suitability of the shared vocabulary is supported by its existing adoption in both a
scientific core library and a viewer.

## Alternatives and refuted paths

- Duplicating the whole protocol in every repository was rejected because prose drifts.
- A runtime Python package was rejected because governance must not enter member release
  dependency chains.
- Tracking all work centrally was rejected because it would hide component ownership.

## Scope and exclusions

This theme establishes governance, reporting and the initial eleven-member registry. It
does not yet change Python support, formatter/linter choices or member CI.

## Acceptance criteria

- A normative ownership and reporting protocol exists.
- The eleven current members and their profiles have one machine-readable registry.
- Pending records have generated indexes and an offline validator.
- CI executes the validator without network credentials.
- Agents and contributors are routed to the protocol.

Resolution will name the normative protocol and repository contract.

## Local implementation issues

None. Member adoption will be proposed and tracked after the central contract is stable.

## Dependencies and risks

The main risk is over-centralization. The repository contract therefore preserves local
ownership and makes shared rules profile-specific.

## Provenance

Repository inspection on 2026-09-06. Related prior proposal:
`uibcdf/molsysmt#156`.

## Resolution

Accepted on 2026-09-06. MolSysSuite now owns suite-wide governance while component-local
implementation remains local. The durable rules live in `devguide/reporting_protocol.md`
and `devguide/repository_contract.md`; `tests/test_governance.py` guards the registry and
offline validation path.
