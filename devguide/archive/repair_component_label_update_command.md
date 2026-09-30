---
summary: Repair stale component labels with the supported GitHub CLI command.
issue: uibcdf/molsyssuite#64
status: resolved
opened: 2026-09-30
closed: 2026-09-30
severity: medium
verification: reproduced
area: [governance, tooling]
guard: tests/test_governance.py::ComponentIssueLabelTests::test_stale_repair_uses_supported_cli_without_recreating_the_label
normative:
blocked_by: []
supersedes: []
---

# Repair stale component-label updates

## What

The canonical component-label synchronizer detects stale metadata correctly
but its write route emits unsupported `gh label update`. Reproduced on
2026-09-30 with `python devtools/scripts/component_issue_labels.py
--repository topomt --component molsysmt --write`; GitHub CLI rejected the
command's color flag and listed create/edit/list as the supported operations.
Central label audit 36770725771 failed on stale TopoMT component:molsysmt.

## How

Keep the internal create/update action vocabulary. Translate update to the
GitHub CLI's edit subcommand at the execution boundary; create remains create.
Preserve repository, label identity, canonical color and description. Editing
the existing label preserves its issue assignments; no delete/recreate occurs.

## Why

The documented governance repair must work as well as its read-only audit.
This blocked the final central checks for uibcdf/pharmacophoremt#9 even though
its complete six-cell CI and skipped-debt recovery had succeeded.

## What is measured and what is assumed

The original write command exited 2 with `unknown flag: --color` because
`update` is not a supported label subcommand. A new regression generated real
stale/missing actions through analysis and captured their external commands;
it failed before the repair on label/update versus label/edit. Hosted audit
attempts 1 and 2 both retained failure before repair. No component scientific
code or policy meaning is changed.

## Alternatives and refuted paths

Creating or deleting/recreating an existing label would obscure its identity
and issue relationships. Calling edit directly outside the canonical tool
would leave the documented repair broken. Fix the shared execution boundary.

## Scope and exclusions

The existing central component-label tool and its regression only. The stale
known TopoMT label is repaired through this tool; unregistered/self labels
remain review-only and are not automatically changed.

## Acceptance criteria

- A stale label emits edit and a missing requested label emits create.
- Both operations preserve canonical metadata and owning repository.
- The documented write command repairs the observed label.
- The hosted read-only audit succeeds after repair.

## Provenance

2026-09-30; Python 3.13; local GitHub CLI and hosted Ubuntu audit.
Original audit: https://github.com/uibcdf/molsyssuite/actions/runs/36770725771.
Durable guard: the named command-boundary regression above, which failed
against the original implementation and passes after mapping update to edit.

## Resolution on 2026-09-30

The update action now emits `gh label edit`; the create action still emits
`gh label create`. All five component-label tests pass, including the new
regression that failed against the original execution boundary. Ruff lint
and formatting pass. Local provenance is Python 3.13.15 and GitHub CLI 2.100.0.

The documented write command was rerun against TopoMT and reported
`CURRENT labels uibcdf/topomt`, proving the canonical color/description were
restored without recreating the label. Hosted audit 36770725771 retained
failure for attempts 1 and 2; attempt 3 succeeded after that repair. The
read-only audit implementation is unchanged. The regression protects the
observed failure because it produces a real stale-label action through
analysis and rejects its unsupported CLI subcommand while verifying metadata
and the separate create route. No policy or scientific behavior changes.
