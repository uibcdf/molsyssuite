---
summary: Route quantity interchange to PyUnitWizard and track actual member adoption.
issue: uibcdf/molsyssuite#46
status: partial
opened: 2026-09-24
closed:
verification: inspected
area: [units, compatibility, governance]
guard:
normative:
blocked_by: []
supersedes: []
---

# Quantity interchange adoption

## What

One provider owns quantity interchange: uibcdf/pyunitwizard#83 (design) and
uibcdf/pyunitwizard#82 (implementation). Members retain scientific schema ownership.

## How

The common contract is `devguide/quantity_boundaries.md`. It requires explicit
units at interchange boundaries, a real non-default-policy regression, explicit
conversion for fixed-unit wire protocols and reviewed bounded exceptions.
The registered PyUnitWizard guide already documents the provisional record API;
do not copy the superseded serialization draft or invent new supported names.

## Why

Unit policy cannot determine how an independent reader interprets an unlabelled
magnitude. A frontend/file assuming nanometers can misread a user angstrom policy.
The historical Viewer failure is resolved locally; H5MSM schema migration remains
under uibcdf/molsysmt#240. See `devguide/rollouts/quantity_boundaries.md` for current
source evidence and remaining ownership.

## What was refuted

Guide delivery does not establish codec adoption. A provisional provider API does
not authorize ambiguous numbers. This work does not restore ArgDigest passports
or value certification, or turn a client schema into a shared quantity format.

## Scope and exclusions

Shared governance, routing, applicability and evidence inventory. Provider API
promotion and scientific storage/frontend migrations stay with their teams.

## Acceptance criteria

- Canonical guidance routes design and implementation to the provider.
- Applicable members own non-default-policy guards at their actual boundaries.
- Codec/provider compatibility, schema migration and public claims are evidenced
  per member, or carry a reviewed exception preserving unit integrity.
- Inventory distinguishes resolved cases from outstanding migration and API work.

Current state: shared rules and routing delivered; complete member adoption and
provider promotion remain pending. Do not close this coordinated adoption issue
merely because the guide is synchronized.

Delivered 2026-10-01: the common boundary summary was synchronized and pushed
to all 15 registered members; all registered guide copies match their sources.
Offline governance passed. This delivery does not close outstanding member
scientific migrations or promote the provisional provider API.
