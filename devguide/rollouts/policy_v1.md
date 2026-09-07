# MolSysSuite policy 1.0 rollout

**Issue:** `uibcdf/molsyssuite#6`
**Policy release:** `policy-v1.1.2`
**Started:** 2026-09-06
**Status:** Active.

## Acceptance

Every member registered in `suite.toml` must either pass:

```bash
python devtools/scripts/check_repository.py ../<member> --repository uibcdf/<member>
```

or carry a central exception naming its reason, issue and expiration condition.

Migration work is prioritized using the cohorts in `suite.toml`: the six wave-1
libraries first, receptor repositories as supporting infrastructure, and the three
incubating scientific tools only when they enter stabilization. Already completed
infrastructure adoption remains valid; incubating members do not block the wave-1
stabilization decision.

## Initial audit

Measured locally on 2026-09-06 with Python 3.13.15. Findings are stable audit codes, not
estimates of migration effort.

Corrected on 2026-09-06 by `uibcdf/molsyssuite#7`: the 1.0.0 guard did not inspect active
Ruff CI commands. This live matrix incorporates the corrected `RUFF_CI` results.

Corrected again by `uibcdf/molsyssuite#9`: the 1.1.0 guard confused Ruff's own isort
settings with the replaced standalone tool. Release 1.1.2 parses that configuration
structurally and preserves detection of actual legacy tooling. The intermediate immutable
1.1.1 tag is not usable because its reusable workflow checked out the prior policy release;
`uibcdf/molsyssuite#10` adds a regression for that self-reference.

| Member | Cohort | State | Local issue | Initial findings |
| --- | --- | --- | --- | --- |
| pytest-receptor | infrastructure | adopted | `uibcdf/pytest-receptor#2` | pass at `8985684`; policy run `34060234759`; full CI `34060234428`; 163 local tests and 9 skips |
| gh-run-receptor | infrastructure | adopted | `uibcdf/gh-run-receptor#22` | pass at `862e151`; policy run `34059932644`; 223 local tests |
| argdigest | wave 1 | adopted | `uibcdf/argdigest#4` | pass at `22ad5da`; policy run `34062887147`; CI `34062886826`; 222 local tests |
| depdigest | wave 1 | adopted | `uibcdf/depdigest#3` | pass at `58086ed`; policy run `34062887954`; 49 local tests |
| elastnetmt | incubating | deferred | — | `GOVERNANCE_POINTER`, `RUFF_CONFIG`, `RUFF_CI`, `LEGACY_TOOL` |
| molsysmt | wave 1 | pending | — | `GOVERNANCE_POINTER`, `RUFF_CONFIG`, `RUFF_CI`, `LEGACY_TOOL` |
| molsysviewer | wave 1 | pending | — | `GOVERNANCE_POINTER`, `PYTHON_RANGE`, `RUFF_CI`, `LEGACY_TOOL` |
| pharmacophoremt | incubating | deferred | — | `GOVERNANCE_POINTER`, `PYTHON_RANGE`, `PYTHON_CI`, `RUFF_CONFIG`, `RUFF_CI`, `LEGACY_TOOL` |
| pyunitwizard | wave 1 | pending | — | `GOVERNANCE_POINTER`, `RUFF_CONFIG`, `RUFF_CI`, `LEGACY_TOOL` |
| smonitor | wave 1 | pending | — | `GOVERNANCE_POINTER`, `PYTHON_RANGE`, `RUFF_CONFIG`, `RUFF_CI` |
| topomt | incubating | deferred | — | `GOVERNANCE_POINTER`, `PYTHON_RANGE`, `RUFF_CONFIG`, `RUFF_CI` |

## Rollout discipline

- Start with repositories already technically conforming to validate routing and workflow
  invocation.
- Open a local issue only when a concrete repository change starts.
- Keep formatting-only changes separate from behavioral fixes.
- Run each repository's existing tests before removing a legacy gate.
- Update this matrix from measured checker output, not from intent.
- Do not close the central issue when the first member passes.
