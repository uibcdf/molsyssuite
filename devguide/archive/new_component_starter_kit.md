---
summary: Provide a starter kit for new MolSysSuite components.
issue: uibcdf/molsyssuite#17
status: resolved
opened: 2026-09-07
closed: 2026-09-07
verification: reproduced
area: [governance, tooling]
guard: tests/test_governance.py::StarterKitTests
normative: devguide/new_component_starter_kit.md
blocked_by: []
supersedes: []
---

# Provide a starter kit for new MolSysSuite components

## What

New component repositories previously began from local convention or copied an existing
member. They therefore acquired suite policy later through coordinated migrations.

## How

MolSysSuite now carries a dependency-free generator and a versioned Python-library
template. Generation is allowed only after central registration and produces the common
Python range, Ruff baseline, CI matrix, ambassador guide, contributor routing and the
complete issue-backed developer-guide lifecycle.

## Why

The first policy rollout had to inspect and edit eleven repositories independently.
Making the accepted baseline executable moves that coordination cost to one reviewed
template and leaves only domain-specific design for the new component.

## Scope and exclusions

The initial kit covers the `python-library` profile. It does not prescribe scientific
validation, frontend tooling, release automation, dependencies or public API shape.
Those remain component-specific and may earn later profile templates.

## Decision

Accepted. `devguide/new_component_starter_kit.md` is the normative onboarding sequence;
`devtools/scripts/bootstrap_component.py` instantiates the tested template. Existing
repositories remain governed through explicit rollouts rather than automatic rewriting.
