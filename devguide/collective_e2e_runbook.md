# Collective E2E Runbook

This runbook defines the reproducible validation steps for collective criterion #2 and #3.

Date baseline: 2026-03-03

## Repository snapshots

- pyunitwizard: `48be457`
- smonitor: `f68c847`
- depdigest: `f217d78`
- argdigest: `9666502`
- molsyssuite (checklist baseline): `3e452d8`

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

- `devguide/collective_e2e_artifact_2026-03-03.md`

## Notes

- This runbook advances collective validation to `in progress`.
- Final collective `done` still requires explicit closure of finality criterion #2 and #3 in central checklist governance.
