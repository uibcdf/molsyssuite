# Collective V1 Checklist (UIBCDF Ecosystem)

This document defines the **interoperability, consistency, and robustness** requirements that `smonitor`, `depdigest`, `argdigest`, and `pyunitwizard` must fulfill for their 1.0 versions to be considered successful as a collective ecosystem.

---

## Writing Protocol (Mandatory)

Use the following rules when updating this checklist:

1. Keep each requirement checkbox as `[ ]` until **collective** validation is complete.
2. Do not mark `[x]` based only on one library's local completion.
3. Under each section, maintain a `Status note (YYYY-MM-DD)` with per-library progress.
4. Use this exact status vocabulary per library: `done locally`, `in progress`, `blocked`, `pending`.
5. Add blockers with short references (`issue`, `PR`, or commit) when status is `blocked`.
6. Mark a checkbox `[x]` only after cross-library E2E evidence is available.

Status note template:

```md
Status note (YYYY-MM-DD):
- smonitor: <done locally|in progress|blocked|pending> (<reference/short note>)
- depdigest: <done locally|in progress|blocked|pending> (<reference/short note>)
- argdigest: <done locally|in progress|blocked|pending> (<reference/short note>)
- pyunitwizard: <done locally|in progress|blocked|pending> (<reference/short note>)
- collective validation: <pending|in progress|done> (<evidence>)
```

---

## 🌐 Cross-Library Standards (Mandatory for all)

To ensure the end-user perceives a unified ecosystem, all 1.0 versions must share these patterns:

- [ ] **Unified Configuration**: Implement the automatic discovery pattern for `_*.py` files at the host package root identically (same precedence: `runtime > env > file`).
- [ ] **Native Instrumentation**: All critical public API functions must be decorated with `@smonitor.signal`.
- [ ] **Optional Dependencies**: No infrastructure library shall force the installation of heavy dependencies (e.g., `rich`, `beartype`, `pydantic`, `pint`) without using `depdigest` mechanisms.
- [ ] **AI-Agent Readiness**: All error and warning messages must include a stable code (`CODE`) and a machine-processable repair suggestion (`hint`).
- [ ] **Compatibility Matrix**: Explicitly define the minimum supported versions of sibling libraries.

Status note (2026-03-04):
- smonitor: in progress (`e0e1a8c`, collective pack + stabilization path active)
- depdigest: in progress (`ac6261c`, collective pack + 0.10.x stabilization)
- argdigest: done locally (`c543c1a`, `0.9.0` RC consolidation + collective pack)
- pyunitwizard: done locally (`9fd9b46`, post-RC stabilization window active)
- collective validation: in progress (shared `tests/e2e/test_collective_error_path.py` green in 4 repos; one-path proof refreshed in `devguide/collective_e2e_artifact_2026-03-04.md`)

---

## 🛠️ SMonitor 1.0: The "Communication Protocol"
*Role: Ensure the ecosystem's nervous system is stable and predictable.*

- [ ] **Event Schema Stability**: Lock the output JSON schema (Schema Version 1.0) so external tools can parse it without breaking.
- [ ] **Profile Consistency**: Guarantee that `user`, `dev`, `qa`, and `agent` profiles produce coherent outputs across all libraries using SMonitor.
- [ ] **Traceability Contract**: Define standard labels (`tags`) to identify "contract" failures (ArgDigest) or "infrastructure" failures (DepDigest).
- [ ] **Predictable Bundle Export**: The diagnostic export format (`bundle.json`) must be the source of truth for error reproduction across the ecosystem.

Status note (2026-03-04):
- smonitor: in progress (`e0e1a8c`, collective pack; schema/bundle locks still pending)
- depdigest: in progress (`ac6261c`, consumer-side alignment in progress)
- argdigest: in progress (`c543c1a`, consumer-side profile validation in progress)
- pyunitwizard: done locally (`9fd9b46`, profile/code-hint contracts validated in RC-close/stabilization evidence)
- collective validation: in progress (shared e2e green; cross-repo profile/tag evidence pending)

---

## 📦 DepDigest 1.0: The "Efficiency Architect"
*Role: Ensure ecosystem growth does not penalize performance.*

- [ ] **Ecosystem Audit**: The `depdigest audit` CLI must be able to detect soft-dependency leaks even within sibling libraries (`argdigest`, `pyunitwizard`).
- [ ] **SMonitor Integration**: Emit `DEBUG` level signals during dependency resolution to allow runtime performance audits.
- [ ] **`_depdigest.py` Standardization**: The dependency definition contract (hard/soft) must be flexible enough to be adopted by the entire ecosystem without ad-hoc extensions.
- [ ] **Zero-Cost Verification**: Confirm through tests that importing `depdigest` adds no more than 50ms to a host library's startup.

Status note (2026-03-04):
- smonitor: in progress (`e0e1a8c`, traceability integration path pending collective E2E)
- depdigest: in progress (`ac6261c`, 0.10.x stabilization + collective pack)
- argdigest: done locally (`c543c1a`, consumer integration path validated)
- pyunitwizard: done locally (`9fd9b46`, hard/soft policy checks validated and release-gates fix validated)
- collective validation: in progress (shared e2e green; `depdigest audit` + import-cost budget evidence pending)

---

## 🧪 ArgDigest 1.0: The "Frontier Orchestrator"
*Role: Validate that component integration is seamless and robust.*

- [ ] **Transparent Orchestration**: Demonstrate it can use `depdigest` to load validators and `pyunitwizard` for units without the user configuring anything beyond a `_argdigest.py`.
- [ ] **Unit Error Mapping**: `pyunitwizard` conversion failures must be captured and re-emitted as ArgDigest contract errors with full caller context.
- [ ] **Inspection Cache**: Implement efficient cache management for `inspect.signature` so massive use of `@arg_digest` does not degrade the performance of main simulation loops.
- [ ] **SMonitor Profile Validation**: Ensure that in the `user` profile, validation errors are friendly, while in `dev`, they include the full digestion trace.

Status note (2026-03-04):
- smonitor: in progress (`e0e1a8c`, profile parity evidence pending cross-repo E2E)
- depdigest: in progress (`ac6261c`, remediation-hint path pending collective E2E)
- argdigest: done locally (`c543c1a`, `0.9.0` RC + collective pack)
- pyunitwizard: done locally (`9fd9b46`, argdigest integration smoke validated in current evidence)
- collective validation: in progress (shared e2e green; full 4-layer closure still pending)

---

## 📏 PyUnitWizard 1.0: The "Quantity Standard"
*Role: Provide an immovable physical foundation for ecosystem data.*

- [ ] **Isolated Kernel**: The unit kernel must be immune to changes in underlying libraries (`pint`, `unyt`) once initialized.
- [ ] **Exception Translation**: All third-party library exceptions must map to an internal PyUnitWizard hierarchy with SMonitor codes.
- [ ] **Fundamental Unit Lock**: Lock the definition of fundamental units (`[L]`, `[M]`, `[T]`, etc.) to ensure long-term data serialization compatibility.
- [ ] **Performance Benchmarking**: Guarantee that the overhead of converting between forms is not the bottleneck in high-frequency APIs (e.g., atom selection).

Status note (2026-03-04):
- smonitor: in progress (`e0e1a8c`, consumer-side alignment documented)
- depdigest: in progress (`ac6261c`, consumer-side alignment documented)
- argdigest: in progress (`c543c1a`, consumer-side error mapping validated)
- pyunitwizard: done locally (`9fd9b46`, kernel/exception/fundamental/perf contracts validated)
- collective validation: in progress (shared e2e green; collective finality criteria still open)

## Cross-Repo E2E Evidence (2026-03-04)

- `pyunitwizard` (`0.21.1-1-g9fd9b46`): `pytest -q tests/e2e/test_collective_error_path.py` -> pass
- `smonitor` (`0.11.4-16-ge0e1a8c`): `pytest -q tests/e2e/test_collective_error_path.py` -> pass
- `depdigest` (`0.9.1-8-gac6261c`): `pytest -q tests/e2e/test_collective_error_path.py` -> pass
- `argdigest` (`0.9.0-9-gc543c1a`): `pytest -q tests/e2e/test_collective_error_path.py` -> pass
- `molsyssuite`: `smonitor --check` -> `OK`

Evidence artifacts:
- runbook: `devguide/collective_e2e_runbook.md`
- latest captured output: `devguide/collective_e2e_artifact_2026-03-04.md`
- historical captured output: `devguide/collective_e2e_artifact_2026-03-03.md`

Pending for collective `done`:
- finality criterion #1: all four libraries reach tag version `>= 1.0.0`.
- finality criterion #2 and #3: explicit collective closure approval with linked evidence trace and host-level all-layer validation sign-off.

---

## 🏁 Collective Finality Criterion
The ecosystem will be considered to have reached version 1.0 when:
1. All four libraries are at version `>= 1.0.0`.
2. An error triggered at the unit layer (`pyunitwizard`) is reported by the API layer (`argdigest`) in an `smonitor` log with the corresponding `depdigest` installation hint, automatically.
3. The `smonitor --check` command in a host library (e.g., MolSysMT) validates the health of all four layers simultaneously.
