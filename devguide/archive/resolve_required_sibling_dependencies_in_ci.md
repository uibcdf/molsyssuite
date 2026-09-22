---
summary: Require a CI acquisition route for direct MolSysSuite dependencies.
issue: uibcdf/molsyssuite#31
status: resolved
opened: 2026-09-22
closed: 2026-09-22
verification: measured
area: [ci, dependencies, governance]
guard: tests/test_governance.py::StarterKitTests::test_generated_pip_lane_reports_a_new_required_suite_dependency
normative: devguide/ci_dependency_resolution.md
blocked_by: []
supersedes: []
---

# Resolve required sibling dependencies in CI

**Reported:** 2026-09-21 by the Ackredit consumer after its generated pip lane ceased
to be installable when SMonitor and DepDigest became required dependencies.
**Status:** Resolved in `policy-v1.4.6`; caller adoption is tracked separately by
`uibcdf/molsyssuite#34`.

## What

The starter kit generates a pip-only CI lane. A new component can follow it exactly,
then add a required suite dependency that is absent from PyPI. Its first hosted CI
cannot acquire that dependency, while the old conformance checker still reports success.

## How

The checker detects registered distribution names in `project.dependencies`. If any
are present, it requires a workflow to use `setup-micromamba` with a committed
`devtools/conda-envs/` file or full-commit source routes for every sibling. The
starter-kit instructions identify the transition point and the normative document
defines the repository-owned choices.

## Why

This turns a known first-push failure into a local finding while preserving each
component's authority over its actual environment files and test workflow.

## What is measured and what is assumed

The generated template runs `pip install -e '.[test]'` against the configured index.
A regression test adds `SMonitor>=0.16.0` to that generated shape: the old checker
returned no finding; the new checker reports `SIBLING_CI_ROUTE`. Tests also accept a
committed Conda route and a full-SHA source route. A local audit of all fourteen
registered components produced no new `SIBLING_CI_ROUTE` findings.

This structural check cannot prove that a Conda solver finds compatible artifacts or
that a source install succeeds. Hosted installation and import remain required evidence.

## Alternatives and refuted paths

- Generate Conda CI for every new repository: adds environment maintenance when no
  sibling is required and still cannot know whether a future dependency has a
  published artifact for each Python version.
- Require Conda exclusively: excludes a pinned source route needed before publication.
- Accept a floating Git branch: makes a CI result difficult to reproduce.

## Scope and exclusions

This governs required suite dependencies in `project.dependencies`. Optional extras,
release staging (`uibcdf/molsyssuite#27`) and the graph inventory
(`uibcdf/molsyssuite#30`) retain their own ownership.

## Acceptance criteria

- The pip-only starter lane yields an offline finding after a required sibling is added.
- The checker accepts committed Conda and immutable source routes.
- The starter guide and policy registry describe the rule and its limits.
- An immutable policy release runs the checker for adopted members.

## Resolution

The named guard failed against the old checker when the generated starter lane gained
SMonitor as a required dependency. It passes with `SIBLING_CI_ROUTE` in the new checker.
The accepted Conda and full-SHA source routes, floating source rejection, and inert
comment rejection have independent tests in the same module. Local tests and governance
validation passed before publishing `policy-v1.4.6`. The offline guard remains a
structural test, not a substitute for hosted installation and imports.

## Local implementation issues

Ackredit's historical migration is `uibcdf/ackredit#6`; no additional component
migration was found in the local audit.

## Dependencies and risks

The route check is intentionally structural. It must not be described as proof of
solver readiness, package availability or test coverage.

## Provenance

Inspected on 2026-09-22 in the MolSysSuite checkout with Python 3.13 and Ruff 0.16.5.
