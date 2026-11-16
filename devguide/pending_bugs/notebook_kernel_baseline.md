---
summary: Qualify the corrected notebook kernel baseline without mutating the paused prefix.
issue: uibcdf/molsyssuite#200
status: active
opened: 2026-11-15
closed:
severity: high
verification: measured
area: [development, notebooks]
guard: tests/test_development_environment.py::DevelopmentEnvironmentTests::test_notebook_baseline_refuses_missing_or_pre_740_kernel
normative: devguide/development_workspace.md
blocked_by: []
supersedes: []
---

# Corrected notebook kernel baseline

## What and why

MolSysViewer #396 receives its actual application guard on ipykernel 7.4.0 after
independent native shell/comm stalls with 7.3.0. Upstream ipython/ipykernel#1529
is merged and its source is consistent with that owner observation. The common
recipe previously admitted a missing/unbounded/older kernel. Similar symptoms
do not assign MolSysMT #615 the same cause.

## How and causal guard

Require ipykernel>=7.4.0 in the recipe and profile validator. The regression fails
on all three missing/unbounded/7.3 floor mutations before the fix; fourteen
profile tests pass afterward. A separate public-channel workflow checks a clean
notebook closure and actual execution/comm interleaving independently of private
source acquisition. The probe verifies the selected interpreter/module origins,
cycle/phase correlation, bounded replies and owned kernel retirement; no product
deadline changes. Ruff lint and formatting pass.

## Measurements and limits

The [receipt](../rollouts/notebook_baseline_200_20261115.json) records 62 clean
conda-forge packages, original ipykernel 7.4.0 archive/hash, successful pip closure,
and thirty cycles/sixty correlated replies on Linux/Python 3.14.10. Both native
attempts pass; the final maximum reply is below 0.04 seconds. The full updated
recipe resolves against public channels; this is a solver plan, not a complete
installation. An initial native env dry-run produced only specifications and is
not counted as a solve. Administrative tests use retained Python 3.14.7 and
published Pytest Receptor 1.2.3 in a task overlay. GHR's unavailable PyPI route
is replaced by independently hash-verified published Conda 1.5.0, not an editable.

## Acceptance and owner follow-up

Receive the recipe/profile guard, actual hosted native-kernel workflow and exact
central governance before closure. Hand the baseline, identities and limits to
MolSysMT and MolSysViewer. Preserve #82's shared-prefix pause and #175's separate
replacement/owner-transition route; the old kernel and live sessions remain.
This bounded central correction does not certify the complete editable workspace,
scientific suites, browser/Qt behavior or other platforms. Component acceptance
and eventual shared transition remain separately owned.

Owner routes are uibcdf/molsysmt#765 and existing uibcdf/molsysviewer#396.
MolSysMT complete inventory (eight pages, 683 issues) contains no matching
notebook-baseline implementation; unrelated closed #590 is preserved. The
166-case development/workspace/read-access/governance selection passes.
