# Collective E2E Runbook

This runbook defines the reproducible validation steps for collective criterion #2 and #3.

Date baseline: 2026-03-04

## Repository snapshots

- pyunitwizard: `0.21.1-1-g9fd9b46` (head `9fd9b46`)
- smonitor: `0.11.4-16-ge0e1a8c` (head `e0e1a8c`)
- depdigest: `0.9.1-8-gac6261c` (head `ac6261c`)
- argdigest: `0.9.0-9-gc543c1a` (head `c543c1a`)
- molsyssuite (checklist baseline): `2d78bfa`

## Objective

Validate, with reproducible commands, that:

1. Shared cross-repo E2E error-path scenario is green in all four libraries.
2. `smonitor --check` succeeds from host repository context (`molsyssuite`).

## Commands

Run from each repository root:

```bash
# pyunitwizard
pytest -q tests/e2e/test_collective_error_path.py

# smonitor
pytest -q tests/e2e/test_collective_error_path.py

# depdigest
pytest -q tests/e2e/test_collective_error_path.py

# argdigest
pytest -q tests/e2e/test_collective_error_path.py
```

Run from host repository root:

```bash
# molsyssuite
smonitor --check
```

## Expected results

- All four `pytest` commands return exit code `0` and show one passing test.
- `smonitor --check` returns `OK` with exit code `0`.

## Artifact

Recorded execution output is stored in:

- `devguide/collective_e2e_artifact_2026-03-04.md`

## Notes

- This runbook keeps collective validation in `in progress` until the finality
  criteria in the central checklist are explicitly closed.
- Shared E2E tests already assert the one-path chain:
  `PyUnitWizard invalid quantity -> ArgDigest DigestValueError -> SMonitor event code (ARG-/PUW-) -> DepDigest install hints in payload`.
