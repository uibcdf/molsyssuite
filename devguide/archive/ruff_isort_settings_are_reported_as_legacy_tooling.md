---
summary: The conformance guard mistakes Ruff isort settings for legacy tooling.
issue: uibcdf/molsyssuite#9
status: resolved
opened: 2026-09-06
closed: 2026-09-06
severity: high
verification: reproduced
area: [governance, tooling, ci]
guard: tests/test_governance.py::RepositoryConformanceTests::test_ruff_isort_settings_are_not_legacy_isort_tooling
normative:
blocked_by: []
supersedes: []
---

# Ruff isort settings are reported as legacy tooling

**Reported:** 2026-09-06, during the ArgDigest policy rollout.
**Status:** Resolved in `bbb6c90`; the structural detector ships in policy 1.1.1.

## What

The `policy-v1.1.0` conformance guard emits `LEGACY_TOOL` for the legitimate Ruff table
`[tool.ruff.lint.isort]`. That table configures Ruff's built-in import sorter; it does not
activate or depend on the replaced `isort` package.

## How

`_legacy_tools()` searches the raw contents of `pyproject.toml` for tool names. The free
text match cannot distinguish `[tool.isort]` from `[tool.ruff.lint.isort]`.

Parse the TOML already loaded by the guard and exclude Ruff's own configuration subtree
from legacy-tool detection. Continue scanning all other project and tool configuration,
plus workflow and INI files, so actual legacy dependencies and `[tool.isort]` settings
remain findings.

## Why

ArgDigest needs `known-first-party = ["argdigest"]` to make import classification stable
when its generated, gitignored `_version.py` file is absent in a clean checkout. Policy
run `34062338487` rejected this valid configuration. The false positive can block any
member that uses Ruff's supported isort compatibility settings.

## What is measured and what is assumed

The regression fixture passes before the Ruff isort table is appended and returns exactly
one `LEGACY_TOOL` finding afterwards under `policy-v1.1.0`. With the structural fix, all
14 governance tests pass and a real ArgDigest audit has no findings.

## Scope and exclusions

This fix does not relax the ban on active Black, isort, or Flake8 configuration and
commands. It does not change the common Ruff rules or formatter behavior.

## Acceptance criteria

- Ruff's `[tool.ruff.lint.isort]` table produces no legacy-tool finding.
- A real `[tool.isort]` table still produces `LEGACY_TOOL`.
- All governance tests and the real ArgDigest audit pass.
- An immutable `policy-v1.1.1` tag contains the fix.

## Dependencies and risks

This bug blocks `uibcdf/argdigest#4` and the suite rollout `uibcdf/molsyssuite#6`.

## Resolution

The guard now removes only Ruff's configuration subtree from TOML legacy-tool scanning.
Actual `[tool.isort]` configuration remains a finding. All 14 governance tests pass and
the real ArgDigest audit conforms. The immutable fix is published as `policy-v1.1.1`.
