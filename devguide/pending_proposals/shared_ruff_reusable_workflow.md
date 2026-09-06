---
summary: The reusable policy workflow owns the common Ruff gate and version pin.
issue: uibcdf/molsyssuite#8
status: active
opened: 2026-09-06
closed:
verification: measured
area: [governance, tooling, ci]
guard:
normative:
blocked_by: []
supersedes: []
---

# Local Ruff jobs would duplicate the common policy

**Reported:** 2026-09-06, during the first policy rollout.
**Status:** Active; failing tests define recognition of the new shared gate release.

## What

Run `ruff check` and `ruff format --check` inside the reusable MolSysSuite policy workflow,
using one centrally pinned Ruff version. Keep member installation and tests local.

## How

The reusable workflow checks out the caller and the pinned policy implementation, installs
only Ruff, runs the read-only conformance audit, then applies both quality checks to the
caller while excluding the temporary policy checkout. The auditor recognizes the exact
policy release carrying this behavior as an active Ruff gate.

## Why

Eleven local jobs would repeat the same setup, commands and version pin. Ruff can inspect a
checkout without installing the member, so this is a genuinely common responsibility that
can be centralized without knowing repository dependency environments.

## What is measured and what is assumed

`pytest-receptor` passed Ruff check and format check locally with Ruff 0.16.5. The current
`gh-run-receptor` checkout passes lint but requires a one-time formatting migration; that
work remains local.

## Alternatives and refuted paths

- A copied local job was rejected as avoidable workflow duplication.
- Installing and testing members centrally was rejected because their dependency and test
  environments differ.
- Treating every `policy-v1.*` caller as equivalent was rejected because releases 1.0.0
  and 1.0.1 do not execute Ruff.

## Scope and exclusions

The shared workflow owns Ruff installation and the two common checks. Each `pyproject.toml`
still owns paths, exclusions, line length and additional rules. Pytest remains local.

## Acceptance criteria

- Tests distinguish the exact shared gate release from older policy tags.
- Ruff 0.16.5 is machine-readable as the policy version.
- The shared workflow runs lint and format without installing the member.
- The temporary policy checkout is excluded from member linting.
- `policy-v1.1.0` is immutable and usable by callers.

## Dependencies and risks

A Ruff update can change formatting. It therefore produces a new policy release and is
tested centrally before member callers update.
