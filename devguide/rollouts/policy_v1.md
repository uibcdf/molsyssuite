# MolSysSuite policy 1.0 rollout

**Issue:** `uibcdf/molsyssuite#6`
**Policy release:** `policy-v1.0.0`
**Started:** 2026-09-06
**Status:** Active.

## Acceptance

Every member registered in `suite.toml` must either pass:

```bash
python devtools/scripts/check_repository.py ../<member> --repository uibcdf/<member>
```

or carry a central exception naming its reason, issue and expiration condition.

## Initial audit

Measured locally on 2026-09-06 with Python 3.13.15. Findings are stable audit codes, not
estimates of migration effort.

| Member | State | Local issue | Initial findings |
| --- | --- | --- | --- |
| pytest-receptor | adopted | `uibcdf/pytest-receptor#2` | pass at `bda0ddb`; policy run `34053874479`; full CI `34053874063` |
| gh-run-receptor | adopted | `uibcdf/gh-run-receptor#22` | pass at `6af4030`; policy run `34053873977` |
| argdigest | pending | — | `GOVERNANCE_POINTER`, `RUFF_CONFIG` |
| depdigest | pending | — | `GOVERNANCE_POINTER`, `RUFF_CONFIG` |
| elastnetmt | pending | — | `GOVERNANCE_POINTER`, `RUFF_CONFIG`, `LEGACY_TOOL` |
| molsysmt | pending | — | `GOVERNANCE_POINTER`, `RUFF_CONFIG`, `LEGACY_TOOL` |
| molsysviewer | pending | — | `GOVERNANCE_POINTER`, `PYTHON_RANGE`, `LEGACY_TOOL` |
| pharmacophoremt | pending | — | `GOVERNANCE_POINTER`, `PYTHON_RANGE`, `PYTHON_CI`, `RUFF_CONFIG`, `LEGACY_TOOL` |
| pyunitwizard | pending | — | `GOVERNANCE_POINTER`, `RUFF_CONFIG`, `LEGACY_TOOL` |
| smonitor | pending | — | `GOVERNANCE_POINTER`, `PYTHON_RANGE`, `RUFF_CONFIG` |
| topomt | pending | — | `GOVERNANCE_POINTER`, `PYTHON_RANGE`, `RUFF_CONFIG` |

## Rollout discipline

- Start with repositories already technically conforming to validate routing and workflow
  invocation.
- Open a local issue only when a concrete repository change starts.
- Keep formatting-only changes separate from behavioral fixes.
- Run each repository's existing tests before removing a legacy gate.
- Update this matrix from measured checker output, not from intent.
- Do not close the central issue when the first member passes.
