---
summary: Report working-tree and upstream state across registered components.
issue: uibcdf/molsyssuite#20
status: resolved
opened: 2026-09-08
closed: 2026-09-12
verification: measured
area: [governance, tooling]
guard: tests/test_governance.py
normative: MOLSYSSUITE_GUIDE.md
blocked_by: []
supersedes: []
---

# A suite-wide working-tree status

**Reported:** Opened on 2026-09-08 after three cross-repository operations used stale
local state.
**Status:** Resolved and guarded by the governance test suite.

## What

Provide one command that reports uncommitted, unpushed, and unpulled state across every
registered component before coordinated work begins.

## How

`devtools/scripts/suite_status.py` derives repositories and stabilization cohorts from
`suite.toml`. It fetches each checkout, reads its porcelain worktree state, resolves its
upstream, and measures both sides of `HEAD...upstream`. Human and JSON output identify
repositories requiring attention; any such repository makes the command exit nonzero.

The command may update remote-tracking references through `git fetch`, but never changes
a worktree, index, local branch, stash, commit, or remote branch. `--no-fetch` provides an
explicit offline snapshot and `--repository` bounds inspection without duplicating the
registry.

## Why

Cross-component development is ordinary MolSysSuite work. A clean-looking checkout whose
remote-tracking reference is stale can cause false guide drift, duplicated commits, or a
downgrade from an old canonical source. Centralizing this check reduces that risk before
the next multi-repository rollout.

## What is measured and what is assumed

The first live run on 2026-09-12 fetched all twelve registered components. Ten were
current and clean. It reported exactly the two already known local changes:
`argdigest/devtools/conda-envs/=18` and `topomt/topomt/_version.py`. No worktree changed.

It is assumed that coordinated local work uses sibling checkouts under a common workspace,
matching the existing guide-synchronization workflow.

## Alternatives and refuted paths

- A script copied into every component was rejected because member inventory and cohort
  order are central facts.
- Reading cached `origin/main` without fetching was rejected because that exact approach
  had already produced false conclusions.
- Automatically pulling or stashing was rejected because status inspection must not alter
  contributor work.

## Scope and exclusions

The command inspects Git repository state. It does not run component tests, validate
MolSysSuite conformance, synchronize guides, install dependencies, or decide whether a
known local change should be kept.

## Acceptance criteria

- Repository selection and order come from `suite.toml`.
- Remote references are refreshed before reporting by default.
- Dirty, ahead, behind, missing, fetch-failed, and upstream-less states are explicit.
- Human and JSON output are available, with repository filters.
- Any repository requiring attention produces a nonzero exit status.
- The command never changes a component worktree.
- The guide ambassador tells component developers when and how to run it.

## Local implementation issues

None. This is central coordination tooling.

## Dependencies and risks

Default operation needs network access for `git fetch`. Explicit `--no-fetch` output is an
offline snapshot and must not be represented as current remote state.

## Provenance

Measured on 2026-09-12 with Python 3.13 from sibling checkouts under
`/home/liliana/repos@uibcdf`.

## Resolution

Resolved on 2026-09-12. `devtools/scripts/suite_status.py` now derives the registered
repositories and stabilization order from `suite.toml`, refreshes remote references by
default, and reports worktree, upstream, ahead, and behind state in human-readable or
JSON form without modifying component worktrees.

The command was exercised against all twelve registered sibling checkouts before and
after publishing the ambassador-guide update. It identified only the two pre-existing
local changes in ArgDigest and TopoMT and reported every other checkout current. The
canonical guide and all twelve synchronized copies now advertise the command; the
governance test suite is the durable guard.
