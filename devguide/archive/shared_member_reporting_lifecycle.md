---
summary: Require the issue-backed devguide lifecycle in every member repository.
issue: uibcdf/molsyssuite#11
status: resolved
opened: 2026-09-07
closed: 2026-09-07
verification: inspected
area: [governance, reporting]
guard: tests/test_governance.py::GovernanceTests::test_reporting_lifecycle_is_a_universal_policy
normative: devguide/reporting_protocol.md
blocked_by: []
supersedes: []
---

# Shared member reporting lifecycle

## What

Make the issue-backed developer-guide lifecycle a universal MolSysSuite rule. Every
member must keep queued bug and proposal reports tied to owning GitHub issues, preserve
resolved records, and make their status discoverable and verifiable.

## How

Adopt the repository-independent semantics proven by MolSysMT and MolSysViewer: stable
issue identity, common open and closed states, front matter, issue-first filing, durable
closure evidence, archive-not-delete history, generated indexes, and offline validation.
Allow local folder layouts, extra metadata, and automation so mature repositories do not
have to discard useful internal practices.

Roll out the local surface separately from accepting the semantic contract. Enforcement
must not be added to the shared repository conformance gate until member repositories
have had a tracked migration path; otherwise accepting a policy would break unrelated
Ruff and Python checks immediately.

The rollout is ordered by the registry cohorts. `uibcdf/molsyssuite#13` first covers
SMonitor, ArgDigest, DepDigest, PyUnitWizard, MolSysMT, and MolSysViewer. The receptor
repositories remain supporting infrastructure. TopoMT, PharmacophoreMT, and ElastNetMT
are incubating and do not block the first stabilization outcome.

## Why

The existing central protocol governed central reports well but did not state clearly
that every member repository had to implement the same lifecycle. That gap permits
issues and developer-guide reports to drift and makes completed reasoning disappear or
become hard to find.

## Acceptance criteria

- `suite.toml` declares reporting as a universal repository policy.
- The normative protocol assigns local and central issue ownership unambiguously.
- Common queue, metadata, status, synchronization, archive, index, and validation
  semantics are explicit.
- Established local archive layouts remain valid through documented mappings.
- Adoption and later enforcement are tracked without breaking current shared gates.
