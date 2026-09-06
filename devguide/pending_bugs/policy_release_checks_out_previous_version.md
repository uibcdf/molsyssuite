---
summary: Policy 1.1.1 checks out the previous policy version internally.
issue: uibcdf/molsyssuite#10
status: open
opened: 2026-09-06
closed:
severity: high
verification: reproduced
area: [governance, tooling, ci]
guard: tests/test_governance.py::RepositoryConformanceTests::test_reusable_workflow_checks_out_its_declared_policy_release
normative:
blocked_by: []
supersedes: []
---

# Policy 1.1.1 checks out the previous version internally

**Reported:** 2026-09-06, while updating adopted repositories after fixing the Ruff isort
false positive.
**Status:** Open; the regression and policy 1.1.2 correction are prepared locally.

## What

The reusable workflow published at `policy-v1.1.1` checks out `policy-v1.1.0` before it
runs the conformance script. Callers therefore select the new workflow shell but execute
the old checker.

## How

The internal `actions/checkout` reference was not advanced when the release value in
`suite.toml` changed. Add a regression that reads both files and requires exact equality.
Publish a new immutable release rather than moving the defective tag.

## Why

ArgDigest, DepDigest, and gh-run-receptor policy runs `34062648951`, `34062650978`, and
`34062650359` failed through the stale checker. Pytest-receptor happened to pass, but it
also executed the wrong policy and therefore cannot validate the release.

## Acceptance criteria

- The reusable workflow's internal checkout ref equals `governance.policy-release`.
- The regression fails for 1.1.1 and passes for the corrected release.
- All governance tests pass.
- Immutable tag `policy-v1.1.2` is published and member callers use it.

## Dependencies and risks

This blocks the active rollout `uibcdf/molsyssuite#6`. The defective 1.1.1 tag remains
immutable and is documented as unusable.
