---
summary: The conformance guard accepts dormant Ruff configuration without CI gates.
issue: uibcdf/molsyssuite#7
status: resolved
opened: 2026-09-06
closed: 2026-09-06
severity: high
verification: reproduced
area: [governance, tooling, ci]
guard: tests/test_governance.py::RepositoryConformanceTests::test_ruff_configuration_without_active_ci_gates_is_not_conforming
normative:
blocked_by: []
supersedes: []
---

# The conformance guard ignores Ruff CI gates

**Reported:** 2026-09-06, while preparing the ArgDigest and DepDigest rollout.
**Status:** Resolved; the corrected guard requires both Ruff CI commands.

## What

`policy-v1.0.0` reports a Python member as conforming when `pyproject.toml` carries the
required Ruff configuration but no workflow runs `ruff check` or
`ruff format --check`.

## How

`check_repository._ruff_conforms()` validates configuration only. `_workflow_text()` is
already available for Python-version and legacy-tool checks, but no assertion consumes it
for the two required Ruff commands.

This allowed `gh-run-receptor` to pass the pilot guard despite having no active Ruff CI
job. The local adoption issue `uibcdf/gh-run-receptor#22` was reopened.

## Why

The accepted tooling policy requires active lint and format checks. A dormant configuration
does not prevent drift, so a false green result invalidates the central rollout evidence.
Severity is high because the guard is the enforcement mechanism for eleven repositories.

## What is measured and what is assumed

Reproduced with a fixture containing the complete Ruff baseline and Python matrix but no
Ruff workflow commands. Before the fix it returns no findings; the required result is
`RUFF_CI`.

## Alternatives and refuted paths

- Treating configuration as sufficient was refuted by the real gh-run-receptor result.
- Running Ruff inside the central workflow was rejected for this fix because it would need
  to know every repository's source exclusions and installation environment. The member's
  own workflow remains responsible for its gate.

## Scope and exclusions

This bug checks that active workflow text contains both required commands. It does not
prove that a historical run succeeded; GitHub branch protection and run status carry that
evidence.

## Acceptance criteria

- The regression fixture fails before and passes after the implementation.
- Missing either command produces one stable `RUFF_CI` finding naming what is absent.
- Other independent findings remain visible.
- A new immutable `policy-v1.0.1` tag contains the corrected guard.

## Dependencies and risks

Static workflow inspection can be fooled by commented commands. This patch improves the
contract materially without adding a YAML dependency; execution evidence is still required
during adoption.

## Resolution

Fixed in `2fadc28`. The guard emits `RUFF_CI` when an active workflow lacks either
`ruff check` or `ruff format --check`, while preserving all other findings. The regression
fixture reproduces dormant configuration explicitly. The corrected reusable workflow is
pinned as `policy-v1.0.1`.
