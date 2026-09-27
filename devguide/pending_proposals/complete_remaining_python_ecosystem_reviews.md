---
summary: Complete remaining Python ecosystem reviews after policy rollout.
issue: uibcdf/molsyssuite#56
status: open
opened: 2026-09-27
closed:
verification: inspected
area: [governance, tooling]
guard:
normative: devguide/python_ecosystem_policy.md
blocked_by: []
supersedes: []
---

# Complete remaining Python ecosystem reviews

## What

The initial member-policy rollout passes its conformance gate, but six registered
members had `pending` Python ecosystem reviews when this proposal opened. Their
review entries pointed to the initial rollout issue even though adoption of developer
tools and support libraries requires separate, member-specific evidence.

MolSysViewer's source review at `19dadc1a` is now recorded as `partial` for both
policies under `uibcdf/molsysviewer#110`. Five reviews remain `pending`.

## How

Review MolSysViewer, PharmacophoreMT, ElastNetMT, DockingMT, Ackredit, and Lindelint
under `devguide/python_ecosystem_policy.md`. Record applicable support libraries
and developer tools separately. Use member-local issues when implementation or
an exception is needed, and update the central inventory from measured evidence.

## Why

Keeping applicability reviews separate from the completed policy-caller rollout
prevents a green conformance run from being mistaken for adoption of every tool.

## Acceptance

Each of the six reviews has evidence and an accurate state, or a local issue and
explicit next action. No review entry points to closed rollout issue #6.
