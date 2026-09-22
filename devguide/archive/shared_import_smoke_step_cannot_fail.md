---
summary: Shared import smoke steps can hide a failed import behind a trailing echo.
issue: uibcdf/molsyssuite#33
status: resolved
opened: 2026-09-21
closed: 2026-09-22
severity: high
verification: reproduced
area: [ci, testing, governance]
guard: tests/test_governance.py::RepositoryConformanceTests::test_import_smoke_step_cannot_hide_failure_behind_trailing_logging
normative:
blocked_by: []
supersedes: []
---

# Shared import smoke steps can report success after a failed import

**Reported:** 2026-09-21, from five green Ackredit CI runs whose import step printed an
`AttributeError` for its missing `__version__`.
**Status:** Resolved; all measured steps are fail-fast, the shared guard is active, and
the rollout has behavioral and hosted cross-runner evidence.

## What

The shared multi-line import smoke step used by seven member repositories can return zero
after Python fails. The shell script closes a GitHub log group with `echo` after the
fallible import, and `bash -l {0}` does not enable fail-fast behavior. GitHub therefore
uses the successful final `echo` as the step result.

The initial inventory found sixteen affected steps across SMonitor, PyUnitWizard,
DepDigest, MolSysMT, MolSysViewer, ArgDigest and Pytest Receptor. Thirteen were the import
smoke step itself. After the DepDigest pilot and other concurrent work, the accepted
central checker measured twelve remaining import steps in six repositories: three each in
SMonitor and PyUnitWizard, one in DepDigest, two each in MolSysMT and MolSysViewer, and one
in ArgDigest. Pytest Receptor no longer contained the measured unsafe shape.

## How

Adopt an explicit fail-fast shell contract for fallible multi-line workflow steps. The
DepDigest pilot uses `set -euo pipefail` inside each script and a regression test that
substitutes an import exiting with status 17, executes the actual workflow script and
requires that status to escape before the trailing group-closing `echo`.

The central policy must detect the unsafe shared shape so a new member cannot reintroduce
it. Component tests may remain where they protect repository-specific shell execution,
including Git Bash selection on Windows.

## Why

A smoke test that cannot fail provides false evidence for package installation, import
outside the source tree and public version exposure. Its failure direction is silent: a
green job gives maintainers no reason to inspect the traceback.

## What is measured and what is assumed

Reproduced in isolation with `bash -l -c`: a missing Python module followed by `echo`
returns zero. Ackredit runs `35572342317`, `35573426452`, `35574083301`, `35574868257`
and `35575394649` all concluded success while printing the missing-version traceback.

DepDigest hosted run `35645517041` passes all twelve jobs on Ubuntu, macOS and Windows
across Python 3.11--3.14 after repairing its CI and full-matrix steps. Its documentation
workflow still contained the unsafe step when the central checker was introduced, so the
pilot was portable evidence rather than complete repository adoption.

The central guard landed in `dcd3e7a`. The twelve remaining steps were then migrated with
the same fail-fast preamble, EXIT trap and direct `python -c` invocation in SMonitor
`0b2b1af`, PyUnitWizard `c32afa1`, DepDigest `42649aa`, MolSysMT `284038cfc`, MolSysViewer
`2c022507` and ArgDigest `f1953d1`. A mutation of each actual workflow script replaced its
import with `SystemExit(17)`; all twelve returned 17 and still closed the GitHub log group.
The checker subsequently reported no `WORKFLOW_FAIL_FAST` finding in any of the seven
originally measured repositories.

Hosted execution covers every runner family used by the repaired workflows. SMonitor run
`35662669121` completed the repaired import step successfully in all twelve Ubuntu, macOS
and Windows jobs before four Windows jobs failed later in their test step. PyUnitWizard
run `35662674539` completed it in six Ubuntu and macOS jobs. ArgDigest run `35662685342`
completed it in six Ubuntu and macOS jobs before later test failures, and DepDigest pilot
run `35645517041` was green across its complete twelve-job matrix. The non-successful
overall conclusions are not presented as success; the named import-step conclusions are
the bounded evidence relevant here.

Fresh workflow dispatches for MolSysMT (`35770751279`) and MolSysViewer (`35770751369`)
failed in `setup-micromamba` before reaching the repaired import step. They therefore add
no import evidence and do not contradict the direct mutation evidence. Current hosted
policy runs `35723875632` and `35723875386` independently confirm that the central guard
accepts the published MolSysMT and MolSysViewer workflow shapes.

## Alternatives and refuted paths

- Rely on the final command being fallible: rejected because harmless logging changes can
  silently disable the check again.
- Fix only the import line: rejected because the same shell semantics affect other
  fallible commands in multi-line steps.
- Copy DepDigest's entire test mechanically: rejected because Windows shell discovery and
  workflow layouts are repository-specific; the central rule should guard the common
  unsafe property.

## Scope and exclusions

This issue owns fail-fast semantics for shared workflow steps and the coordinated rollout
to the seven measured members. Environment construction and installation of sibling
dependencies belong to `uibcdf/molsyssuite#31`.

## Acceptance criteria

- The central checker rejects an affected multi-line smoke step that can hide failure.
- Every affected member either adopts fail-fast behavior or has an explicit central
  exception with an expiration condition.
- Each repaired import smoke step has behavioral evidence that a failed import makes the
  script and job fail before a trailing log command.
- Hosted evidence covers the supported runner families used by each repaired workflow.

## Local implementation issues

The uniform six-repository rollout is owned centrally by this issue; no local exception
or component-specific decision was needed. Ackredit issue `uibcdf/ackredit#11` separately
owns its missing public version and the local gate that first exposed the shared defect.

## Dependencies and risks

Parsing arbitrary shell safely is out of scope for the first guard. Start with the exact
shared smoke-step shape and expand only with defensible syntax. A heuristic that claims to
validate every multi-line shell script would create another false assurance.

## Provenance

Evidence supplied by the issue reproduction and the DepDigest pilot on 2026-09-21. The
central triage used Python 3.13 and gh-run-receptor for the hosted pilot summary.
