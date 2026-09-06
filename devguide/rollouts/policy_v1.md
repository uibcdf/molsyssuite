# MolSysSuite policy 1.0 rollout

**Issue:** `uibcdf/molsyssuite#6`
**Policy release:** `policy-v1.1.0`
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

Corrected on 2026-09-06 by `uibcdf/molsyssuite#7`: the 1.0.0 guard did not inspect active
Ruff CI commands. This live matrix incorporates the corrected `RUFF_CI` results.

| Member | State | Local issue | Initial findings |
| --- | --- | --- | --- |
| pytest-receptor | adopted | `uibcdf/pytest-receptor#2` | pass at `8985684`; policy run `34060234759`; full CI `34060234428`; 163 local tests and 9 skips |
| gh-run-receptor | adopted | `uibcdf/gh-run-receptor#22` | pass at `862e151`; policy run `34059932644`; 223 local tests |
| argdigest | pending | — | `GOVERNANCE_POINTER`, `RUFF_CONFIG`, `RUFF_CI` |
| depdigest | adopted | `uibcdf/depdigest#3` | pass at `107aa92`; policy run `34061109678`; CI `34061109432`; 49 local tests |
| elastnetmt | pending | — | `GOVERNANCE_POINTER`, `RUFF_CONFIG`, `RUFF_CI`, `LEGACY_TOOL` |
| molsysmt | pending | — | `GOVERNANCE_POINTER`, `RUFF_CONFIG`, `RUFF_CI`, `LEGACY_TOOL` |
| molsysviewer | pending | — | `GOVERNANCE_POINTER`, `PYTHON_RANGE`, `RUFF_CI`, `LEGACY_TOOL` |
| pharmacophoremt | pending | — | `GOVERNANCE_POINTER`, `PYTHON_RANGE`, `PYTHON_CI`, `RUFF_CONFIG`, `RUFF_CI`, `LEGACY_TOOL` |
| pyunitwizard | pending | — | `GOVERNANCE_POINTER`, `RUFF_CONFIG`, `RUFF_CI`, `LEGACY_TOOL` |
| smonitor | pending | — | `GOVERNANCE_POINTER`, `PYTHON_RANGE`, `RUFF_CONFIG`, `RUFF_CI` |
| topomt | pending | — | `GOVERNANCE_POINTER`, `PYTHON_RANGE`, `RUFF_CONFIG`, `RUFF_CI` |

## Rollout discipline

- Start with repositories already technically conforming to validate routing and workflow
  invocation.
- Open a local issue only when a concrete repository change starts.
- Keep formatting-only changes separate from behavioral fixes.
- Run each repository's existing tests before removing a legacy gate.
- Update this matrix from measured checker output, not from intent.
- Do not close the central issue when the first member passes.
