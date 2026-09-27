---
summary: Complete remaining Python ecosystem reviews after policy rollout.
issue: uibcdf/molsyssuite#56
status: resolved
opened: 2026-09-27
closed: 2026-09-27
verification: inspected
area: [governance, tooling]
guard: tests/test_python_ecosystem_status.py::test_remaining_review_cohort_has_member_evidence
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

MolSysViewer's source review at `19dadc1a` is recorded as `partial` for both
policies under `uibcdf/molsysviewer#110`. PharmacophoreMT's review at
`7df2496b` records support libraries as `partial` and developer tools as
`adopted` under `uibcdf/pharmacophoremt#6`. The other four have now been
reviewed: ElastNetMT is `partial`/`partial` under `uibcdf/elastnetmt#14`,
DockingMT is `partial`/`partial` under `uibcdf/dockingmt#19`, Ackredit is
`adopted`/`partial` under `uibcdf/ackredit#72`, and LinDelInt is
`partial`/`partial` under `uibcdf/lindelint#9`. Each pair lists support
libraries first and developer tools second. No original review remains
`pending`; member issues retain the concrete next actions.

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

## Resolution

The six original review entries now have independent support-library and
developer-tool states, evidence, and member-owned issues in `suite.toml`.
MolSysViewer and PharmacophoreMT were recorded first; ElastNetMT, DockingMT,
Ackredit, and LinDelInt followed. The member issues listed above retain the
implementation work behind partial states. TopoMT is a separate pending review
under `uibcdf/topomt#16` and was outside this six-member cohort.

The named guard verifies that all six remain non-pending, carry evidence for
both policy areas, and point to their owning member issues. The governance
validator and the full central test suite passed after the records reached
`main`. This report is archived because its inventory-review outcome is done;
member adoption work stays open in the corresponding repositories.

## Correction — 2026-09-27

The TopoMT status above described the separate review at the time this
six-member report closed. TopoMT was subsequently reviewed under
`uibcdf/topomt#56`: support libraries are `partial` and developer tools are
`adopted`. Its former review reference `uibcdf/topomt#16` now tracks Python
matrix evidence before support or release claims.
