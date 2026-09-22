---
summary: Register and distribute the Pytest Receptor consumer guide.
issue: uibcdf/molsyssuite#37
status: active
opened: 2026-09-22
closed:
verification: measured
area: [governance, documentation, testing]
guard:
normative:
blocked_by: []
supersedes: []
---

# Register and distribute the Pytest Receptor consumer guide

**Reported:** 2026-09-22 after the provider guide was requested in
`uibcdf/pytest-receptor#5`.
**Status:** Active. The provider blocker is resolved and the central registry rollout is
being implemented.

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
