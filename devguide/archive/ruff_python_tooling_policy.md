---
summary: Ruff becomes the common formatter, import sorter and linter for Python code.
issue: uibcdf/molsyssuite#4
status: resolved
opened: 2026-09-06
closed: 2026-09-06
verification: inspected
area: [python, tooling, ci]
guard:
normative: devguide/python_tooling_policy.md
blocked_by: []
supersedes: []
---

# Python quality tooling is duplicated across the suite

**Reported:** 2026-09-06, after comparing development tooling across member repositories.
**Status:** Resolved; the common baseline and migration boundary are normative.

## What

Use Ruff for Python formatting, import sorting and linting. Remove active Black, isort and
flake8 gates after each repository reaches equivalent green checks. Keep static type
checking repository-local rather than mandatory.

## How

Require a small rule baseline and common commands, while leaving source exclusions and
additional rules in each repository. Central policy defines the invariant; later audits
check it without distributing a runtime package.

## Why

Maintaining four overlapping tools across eleven repositories multiplies dependency,
configuration and CI work. Ruff covers the chosen responsibilities with one installation
and consistent commands.

## What is measured and what is assumed

The decision follows inspection of current member configurations and prior maintainer
discussion. Migration effort and repository-specific violations remain to be measured in
the rollout; this proposal does not claim that all members are already Ruff-clean.

## Alternatives and refuted paths

- Keeping Black, isort and flake8 as a universal stack was rejected as duplicated work.
- Making every Ruff option identical was rejected because source layouts differ.
- Requiring a type checker now was rejected because the suite does not yet have evidence
  that one common static gate pays for its maintenance cost.
- Treating ArgDigest as a type checker was rejected because it validates runtime calls and
  solves a different problem.

## Scope and exclusions

Applies to Python code in the `python-library` profile. JavaScript, notebooks, generated
files and domain-specific validation retain repository-specific tooling.

## Acceptance criteria

- Ruff's three responsibilities and baseline rule families are normative.
- Common check and formatting commands are specified.
- Black/isort/flake8 removal is gated on a green migration.
- Static type checking and local extensions have explicit status.
- The machine-readable policy matches the normative document.

## Local implementation issues

None yet. Pilot and rollout work will be tracked separately.

## Dependencies and risks

Enabling import ordering and formatting may produce large mechanical diffs. Those changes
must remain isolated from behavioral work and retain full test coverage.

## Resolution

Accepted on 2026-09-06. Ruff owns formatting, import sorting and linting for the
`python-library` profile; Pytest remains the test runner and type checking remains a local
choice. Black, isort and flake8 leave active gates only after a repository is green under
the Ruff replacement.
