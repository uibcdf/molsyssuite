---
summary: Migrate the six remaining Python components to 3.14
issue: uibcdf/molsyssuite#51
status: open
opened: 2026-09-26
closed:
verification: inspected
area: [python, compatibility, packaging, ci]
guard:
normative:
blocked_by: []
supersedes: []
---

# Migrate the six remaining Python components to 3.14

**Reported:** 2026-09-26, while constructing a Python 3.14 development environment
from the editable packages in the existing Python 3.13 environment.
**Status:** Open; source metadata has been inventoried, but compatibility and release
evidence remain component-owned.

## What

Complete the Python 3.14 transition for the registered Python packages that still
exclude that interpreter in their source metadata. This is the remaining-cohort
tracker under the phased suite rollout in `uibcdf/molsyssuite#29`, not a claim that
editing a version bound alone establishes support.

| Component | Source declaration inspected on 2026-09-26 |
| --- | --- |
| Ackredit | `pyproject.toml:10`: `>=3.11,<3.14` |
| DockingMT | `pyproject.toml:22`: `>=3.11,<3.14` |
| ElastNetMT | `pyproject.toml:21`: `>=3.11.0,<3.14.0` |
| LindeLint | `pyproject.toml:21`: `>=3.11.0,<3.14.0` |
| PharmacophoreMT | `pyproject.toml:21`: `>=3.11,<3.14` |
| TopoMT | `pyproject.toml:21`: `>=3.11,<3.14` |

## How

Each component owner should verify the Python 3.14 dependency chain, run the relevant
local and hosted tests, align package metadata, Conda recipes, CI, documentation and
release gates, and test a clean installed package. Native or upstream blockers need
explicit component issues and a bounded suite exception. Admit packages in dependency
order; do not use `--ignore-requires-python` to make the development environment appear
complete.

## Why

The new `molsyssuite@uibcdf_3.14` environment can legitimately install the already
compatible core pair and tooling in editable mode, but cannot reproduce all editable
members of the older 3.13 environment until these six move. A central remaining-cohort
tracker prevents the first successful pair from being mistaken for suite-wide coverage.

## What is measured and what is assumed

**Inspected:** The six `requires-python` fields above were read from fetched
`origin/main` refs after the suite status check. Several local checkouts lag those
refs, and PharmacophoreMT's local checkout still declares the older lower bound
`>=3.10.0`. The suite registry lists all six with `python-package` capability.
The other eight registered Python packages declare a range including 3.14.

**Not yet measured here:** Importability, full test results, Conda solves, native
extension availability, and public installed-package behavior for the six. Those
results belong to each component's implementation record.

## Alternatives and refuted paths

Forcing the six editable installs with `--ignore-requires-python` would bypass their
published contract and conceal compatibility failures. It is unsuitable as evidence.
No other migration strategy has been evaluated yet.

## Scope and exclusions

This central issue coordinates Ackredit, DockingMT, ElastNetMT, LindeLint,
PharmacophoreMT and TopoMT. Component-specific code, tests and release decisions remain
in their respective repositories. The already-admitted first cohort and the
MolSysMT--MolSysViewer pair are tracked by `uibcdf/molsyssuite#29` and their own issues.

## Acceptance criteria

- Each listed component has its own Python 3.14 compatibility evidence and an aligned
  declared package contract, or a documented, time-bounded exception linked from suite
  policy.
- Clean installed-package evidence and release provenance are recorded before a
  component is marked admitted.
- The suite registry and this tracker identify no unaccounted registered Python package
  still excluding 3.14.
- Closure names the normative suite policy or an automated registry/metadata audit
  that prevents a silent regression.

## Local implementation issues

To be opened by component owners as individual migration work is scoped.

## Dependencies and risks

No strict issue blocker is established yet. Native packages and optional scientific
dependencies may have different release paths; an editable source import alone does not
prove a distributable 3.14 package.

## Provenance

Source inspection on 2026-09-26 from fetched `origin/main` refs in
`/home/diego/repos@uibcdf`, host `nauta`;
the new development environment uses CPython 3.14.7. No runtime measurement for the six
is claimed by this report.
