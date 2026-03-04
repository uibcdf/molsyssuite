# Collective E2E Artifact (2026-03-04)

Repository snapshots (validated run):
- pyunitwizard: `0.21.1-1-g9fd9b46` (`9fd9b46`)
- smonitor: `0.11.4-16-ge0e1a8c` (`e0e1a8c`)
- depdigest: `0.9.1-8-gac6261c` (`ac6261c`)
- argdigest: `0.9.0-9-gc543c1a` (`c543c1a`)
- molsyssuite: `2d78bfa`

## pyunitwizard
```bash
$ pytest -q tests/e2e/test_collective_error_path.py
.                                                                        [100%]
1 passed in 2.41s
```

## smonitor
```bash
$ pytest -q tests/e2e/test_collective_error_path.py
.                                                                        [100%]
```

## depdigest
```bash
$ pytest -q tests/e2e/test_collective_error_path.py
.                                                                        [100%]
1 passed in 2.53s
```

## argdigest
```bash
$ pytest -q tests/e2e/test_collective_error_path.py
.                                                                        [100%]
1 passed in 2.01s
```

## molsyssuite host check
```bash
$ smonitor --check
OK
```

## One-path proof for finality criterion #2

The shared E2E test (`tests/e2e/test_collective_error_path.py`) explicitly validates:

1. PyUnitWizard generates an invalid quantity path (`wrong_distance`).
2. ArgDigest raises `DigestValueError` in contract validation.
3. SMonitor captures a diagnostic event code prefixed with `ARG-` or `PUW-`.
4. DepDigest payload includes remediation install hints (`dependencies[*].install`) for `pint`.

This confirms the four-layer trace in a single reproducible path.

## Notes

- This artifact supersedes `devguide/collective_e2e_artifact_2026-03-03.md` as the latest validated snapshot.
- Collective finality remains pending until checklist-level closure is explicitly approved.
