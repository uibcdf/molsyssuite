---
summary: Synchronize every vendored integration guide from the central registry.
issue: uibcdf/molsyssuite#21
status: resolved
opened: 2026-09-09
closed: 2026-09-12
verification: measured
area: [governance, tooling]
guard: tests/test_governance.py
normative: devguide/vendored_guides.md
blocked_by: []
supersedes: []
---

# Generalize vendored-guide synchronization from the central registry

**Reported:** Proposed during the PyUnitWizard stabilization work on 2026-09-09 after
observing that `sync_component_guide.py` only handles `MOLSYSSUITE_GUIDE.md`.
**Status:** Resolved and guarded by the governance test suite.

## What

Provide one MolSysSuite-owned command that checks or synchronizes every registered
integration guide, including SMonitor, DepDigest, ArgDigest, PyUnitWizard, and GH Run
Receptor guides, rather than special-casing only the suite ambassador.

## How

Derive canonical sources, destination filenames, and consumers from the existing
`[[guides]]` entries in `suite.toml`. Check by default, require `--write` for mutation,
allow exact guide and repository filters, and preflight all selected relationships before
writing. Write mode additionally compares source `HEAD` with remote `main`, rejects
uncommitted canonical content, and protects locally modified consumer copies. Retain
`sync_component_guide.py` as a compatibility entry point.

The executable belongs in MolSysSuite because the central registry owns distribution
topology. Each provider continues to own, review, and validate its canonical guide.

## Why

Duplicating synchronization code in every provider would create multiple partial views
of the same consumer graph and make registration drift likely. A central data-driven
tool turns the existing registry into the executable authority while preserving content
ownership at the provider.

## What is measured and what is assumed

Inspection on 2026-09-09 found six guide families already registered in `suite.toml`, a
generic cross-repository checker, and only one write tool specialized for
`MOLSYSSUITE_GUIDE.md`. It is assumed that ordinary coordinated work uses sibling
checkouts under one workspace, matching the existing cross-repository workflow.

The first real write trial exposed a stale local `gh-run-receptor` source checkout: its
local `origin/main` cache and `HEAD` were both at 0.19.0 while the remote and five
consumers were already at 0.19.1. No generated changes were committed. A subsequent
`git pull --ff-only` advanced the provider from `327f292` to `f6160e7`; this observation
caused remote-source and local-edit guards to become part of the implementation.

## Alternatives and refuted paths

- One synchronizer in every guide-owner repository was rejected because every owner
  would duplicate and potentially drift from the centrally governed consumer list.
- Moving canonical guide content into MolSysSuite was rejected because it would erase
  the provider's editorial and technical ownership.
- Extending only `sync_component_guide.py` without a new name was rejected because its
  established name and positional-target interface describe one special guide.

## Scope and exclusions

This applies to all relationships under `[[guides]]`. It does not clone repositories,
commit consumer changes, push branches, edit canonical content, or replace provider-side
content tests.

## Acceptance criteria

- A central command derives all relationships from `suite.toml`.
- Check mode is read-only and write mode produces byte-identical copies.
- Guide and repository selectors reject unknown values.
- A failed preflight produces no partial writes.
- Write mode rejects stale or unpublished canonical sources and locally edited copies.
- The normative guide documents ownership and the operating commands.
- The offline governance suite passes.

## Local implementation issues

None. Consumer repositories only need commits when a canonical guide has actually
changed; the synchronization mechanism itself is central.

## Dependencies and risks

The command intentionally refuses incomplete workspaces. Overwriting a legitimate local
edit is not supported because registered consumer copies are generated read-only files;
operators must review check-mode output before choosing `--write`.

## Provenance

Inspected from the MolSysSuite checkout on 2026-09-09 using Python 3.13 and the current
`main` registry and governance tests.

## Resolution

Resolved on 2026-09-12. `sync_vendored_guides.py` now derives every relationship from
`suite.toml`, supports guide and consumer filters, checks by default, and requires
`--write` for distribution. Write mode performs a complete structural preflight,
requires clean canonical files at the current remote `main`, and refuses to overwrite
locally modified consumer copies.

The implementation was exercised against the real sibling workspace. Its stale-source
guard rejected SMonitor commit `d4d29a0` after remote `main` had advanced to `b4f3e24`,
without modifying a consumer. After the provider update, it synchronized the remaining
PyUnitWizard copy of `SMONITOR_GUIDE.md`. The final registry audit reported all 52 copies
current and byte-identical. The offline governance suite provides the durable guard.
