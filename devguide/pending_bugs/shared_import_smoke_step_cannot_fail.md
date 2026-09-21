---
summary: Shared import smoke steps can hide a failed import behind a trailing echo.
issue: uibcdf/molsyssuite#33
status: active
opened: 2026-09-21
closed:
severity: high
verification: reproduced
area: [ci, testing, governance]
guard:
normative:
blocked_by: []
supersedes: []
---

# Shared import smoke steps can report success after a failed import

**Reported:** 2026-09-21, from five green Ackredit CI runs whose import step printed an
`AttributeError` for its missing `__version__`.
**Status:** Active; DepDigest is the validated pilot and the remaining affected members
still require measured rollout work.

## What

The shared multi-line import smoke step used by seven member repositories can return zero
after Python fails. The shell script closes a GitHub log group with `echo` after the
fallible import, and `bash -l {0}` does not enable fail-fast behavior. GitHub therefore
uses the successful final `echo` as the step result.

The initial inventory found sixteen affected steps across SMonitor, PyUnitWizard,
DepDigest, MolSysMT, MolSysViewer, ArgDigest and Pytest Receptor. Thirteen were the import
smoke step itself. DepDigest has since repaired and behaviorally tested both of its import
steps at `d82f387049acadaf414755dbcfa4ebb602d04f80`.

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
across Python 3.11--3.14 after the pilot repair. It proves one portable implementation;
it does not prove the other members have adopted it.

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

- DepDigest: pilot complete at `d82f387049acadaf414755dbcfa4ebb602d04f80`.
- Ackredit: `uibcdf/ackredit#11` owns its missing public version and local dead gate.
- Open component issues only when concrete migration work begins in the remaining six
  measured repositories.

## Dependencies and risks

Parsing arbitrary shell safely is out of scope for the first guard. Start with the exact
shared smoke-step shape and expand only with defensible syntax. A heuristic that claims to
validate every multi-line shell script would create another false assurance.

## Provenance

Evidence supplied by the issue reproduction and the DepDigest pilot on 2026-09-21. The
central triage used Python 3.13 and gh-run-receptor for the hosted pilot summary.
