---
summary: The documented direct suite status command fails during imports.
issue: uibcdf/molsyssuite#44
status: resolved
opened: 2026-09-23
closed: 2026-09-26
severity: medium
verification: reproduced
area: [governance, tooling]
guard: tests/test_governance.py::SuiteStatusTests::test_documented_direct_entrypoint_ignores_foreign_devtools_package
normative:
blocked_by: []
supersedes: []
---

# Direct suite status invocation fails during imports

**Reported:** 2026-09-23 in the documented cross-repository status entrypoint.
**Status:** Resolved.

## What

`python devtools/scripts/suite_status.py --help` raises an import error before
displaying help when another `devtools` namespace is present in the Python environment.
The module invocation works. The directly documented governance validator has the same
failure mode in this checkout.

## How

Direct execution puts `devtools/scripts` on `sys.path`, but not necessarily the
repository root. `suite_status.py` imports `check_repository.py` only to load the policy.
That module imports `devtools.scripts` through the environment's namespace, where this
checkout's modules can be absent. Its fallback then encounters another failing nested
import. The validator has the same root-path problem in its direct entrypoint.

## Why

The prescribed preflight for coordinated component work and the mandatory offline
governance guard cannot be run as documented in affected developer environments.

## What is measured and what is assumed

On 2026-09-26, both `python devtools/scripts/suite_status.py --help` and
`python devtools/scripts/validate_governance.py` failed with `ImportError` from the
`devtools.scripts` namespace. Their module invocations succeeded. A subprocess test
with a foreign `devtools` package reproduces the status command failure.

## Alternatives and refuted paths

Changing the documentation to require module execution would leave existing direct
callers and the checked-in CI command broken. Changing every nested import is broader
than needed. The status command can load its registry from `moli_policy.py` directly;
the validator can put the local root on its import path before loading its helpers.

## Scope and exclusions

This repair covers the two documented direct commands. It does not change how Git
status is measured, fetch behavior, member ordering, or policy values.

## Acceptance criteria

- Direct `suite_status.py --help` works with a foreign `devtools` package importable.
- Direct governance validation succeeds with a foreign `devtools` namespace present.
- A targeted subprocess regression protects the reported status command failure.
- The offline governance guard and local tests pass.

## Local implementation issues

None; both commands belong to this repository.

## Dependencies and risks

No external dependency changes. The validator still depends on the pinned MOLI checkout
as specified by `suite.toml`.

## Provenance

Reproduced on host `nauta`, Python 3.13.14, on 2026-09-26 from the MolSysSuite root.
The commands above use this checkout and its existing Python environment.

## Resolution

`suite_status.py` now imports the registry loader directly from its local policy module
when run as a file, avoiding the unrelated nested imports. The governance validator
adds this checkout to its import path before loading helpers in direct mode.

The regression runs the documented status entrypoint with a foreign `devtools` package
on `PYTHONPATH`; it would fail during import before the repair. A second subprocess check
exercises the documented validator entrypoint with a foreign namespace. The direct
status command also produced a bounded, read-only JSON snapshot for SMonitor.
`python -m pytest -q tests` passed all 142 tests and 16 subtests, and
`python devtools/scripts/validate_governance.py` passed.
