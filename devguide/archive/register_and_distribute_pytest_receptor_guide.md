---
summary: Register and distribute the Pytest Receptor consumer guide.
issue: uibcdf/molsyssuite#37
status: resolved
opened: 2026-09-22
closed: 2026-09-22
verification: measured
area: [governance, documentation, testing]
guard: tests/test_governance.py::GovernanceTests::test_pytest_receptor_guide_targets_measured_consumers
normative: devguide/vendored_guides.md
blocked_by: []
supersedes: []
---

# Register and distribute the Pytest Receptor consumer guide

**Reported:** 2026-09-22 after the provider guide was requested in
`uibcdf/pytest-receptor#5`.
**Status:** Resolved on 2026-09-22. The provider contract, exact consumer registry,
consumer copies and hosted central guard are complete.

## What

Register `PYTEST_RECEPTOR_GUIDE.md` in the central vendored-guide inventory and distribute
byte-identical read-only copies only to MolSysSuite repositories with durable Pytest
Receptor use.

## How

Use the canonical provider source at
`uibcdf/pytest-receptor:standards/PYTEST_RECEPTOR_GUIDE.md`. Derive the consumer set from
development dependencies, workflow commands and maintained contributor instructions.
Synchronize through `sync_vendored_guides.py`, require each consumer `AGENTS.md` to route
developers to the root copy, and exclude the generated prose through each repository's
existing Ruff vendored-guide configuration.

## Why

Developers already use Pytest Receptor across multiple components, but operational
knowledge is split between provider documentation and consumer-local notes. A canonical
visible contract prevents stale or divergent instructions while preserving the provider
as content owner.

## What is measured and what is assumed

On 2026-09-22, repository-wide inspection found durable use in SMonitor, ArgDigest,
DepDigest, PyUnitWizard, MolSysMT, MolSysViewer, GH Run Receptor, DockingMT and Ackredit.
Evidence included declared test dependencies, `--receptor` CI invocations and maintained
developer commands. TopoMT, PharmacophoreMT, ElastNetMT and Lindelint showed no equivalent
use and are excluded.

Provider issue `uibcdf/pytest-receptor#5` is resolved. Canonical commit `5765e6c` passed
172 local tests, focused guide guards and Ruff. Hosted provider tests run `35719841057`
passed 11/11 jobs and policy run `35719841348` passed 1/1.

## Acceptance criteria

- The exact nine-consumer boundary is registered and guarded centrally.
- All copies equal the provider source byte for byte.
- Every consumer `AGENTS.md` requires the root guide and Ruff excludes that exact path.
- Provider, consumer and central guide guards pass after publication.
- The provider issue owns content; this issue owns registry and adoption evidence.

## Scope and exclusions

This issue does not change Pytest Receptor behavior or require non-users to adopt it. A
consumer-local dependency or workflow deficiency discovered during rollout remains local
work rather than silently expanding this guide-only change.

## Provenance

Provider issue, canonical source and hosted runs plus searches of registered repositories'
workflows, environments, package metadata and maintained developer documentation on
2026-09-22.

## Resolution evidence

Provider commit `5765e6c` introduced the canonical contract. Central preflight then
correctly rejected its provider-specific header before writing any consumer file;
provider correction `4f552d4` adopted the existing universal marker and passed 11/11
hosted test jobs plus the 1/1 policy job. The archived provider record retains a dated
correction rather than hiding the initial mismatch.

Central commit `0dba9db` registered the exact nine-consumer boundary and its guard. The
canonical SHA-256 is
`9a036c6b9c5a80993dc1de4c5b5471f8d9b9cc8574917c793f03f9dffbde3137`; every published
root copy matches it byte for byte. Consumer commits are SMonitor `2221365`, ArgDigest
`32d8c59`, DepDigest `6a63a2e`, PyUnitWizard `d77aeb2`, MolSysMT `7e293f4a8`, MolSysViewer
`98df7c61`, GH Run Receptor `176323f`, DockingMT `6b994aa`, and Ackredit `6e2d2cf`.

Each consumer routes developers from `AGENTS.md` and excludes the exact generated root
path in Ruff. The central conformance audit reported no guide-specific findings; unrelated
release-policy and pre-existing Ruff findings remain tracked by their owning work.
Vendored-guide run `35720822728` attempt 2 passed its single job after cloning and checking
the published repositories. GH Run Receptor independently summarized the rerun as PASS.
