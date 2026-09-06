---
summary: Python libraries support 3.11 through 3.13 and develop on 3.13.
issue: uibcdf/molsyssuite#3
status: resolved
opened: 2026-09-06
closed: 2026-09-06
verification: inspected
area: [python, compatibility, ci]
guard:
normative: devguide/python_policy.md
blocked_by: []
supersedes: []
---

# MolSysSuite needs one Python support range

**Reported:** 2026-09-06, during the suite governance bootstrap.
**Status:** Resolved; the compatibility policy is normative and machine-readable.

## What

Python libraries support Python 3.11, 3.12 and 3.13, declare
`requires-python = ">=3.11,<3.14"`, and use Python 3.13 for routine development.

## How

Make the range and CI versions machine-readable in `suite.toml`, document what support
means, and migrate each differing repository through local work.

## Why

One range makes dependency choices, CI failures and release compatibility intelligible
across the suite. A common development version removes needless environmental variation.

## What is measured and what is assumed

The member repositories were previously inspected and found to carry differing Python
metadata and CI conventions. This proposal records the range explicitly agreed by the
maintainers; it does not claim that every member has completed migration.

## Alternatives and refuted paths

- Supporting only 3.13 was rejected because users need maintained older minors.
- Developing on every supported minor interchangeably was rejected because it provides no
  stable maintainer default.
- Allowing each member to choose independently was rejected because compatibility is a
  suite contract.

## Scope and exclusions

Applies to the `python-library` profile. Repository-specific dependency lanes and non-Python
toolchains remain local.

## Acceptance criteria

- The exact range, development version and required CI minors are normative.
- The same values exist in `suite.toml`.
- The policy distinguishes adoption from declaration and defines exceptions.

## Local implementation issues

None yet. They will be opened only for repositories that differ from the accepted policy.

## Dependencies and risks

Some member dependency sets may reveal blockers during rollout. Those become explicit,
time-bounded exceptions rather than changes to the common range.

## Resolution

Accepted on 2026-09-06. The supported range is `>=3.11,<3.14`, routine development uses
Python 3.13, and required CI covers 3.11, 3.12 and 3.13. Adoption by individual members is
tracked separately from this policy decision.
