---
summary: Migrate the six remaining Python components to 3.14
issue: uibcdf/molsyssuite#51
status: active
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
**Status:** Active; the six required source contracts now include Python 3.14.
Qualification and public delivery remain component-owned; see the dated checkpoints.

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

Ackredit adoption is owned by uibcdf/ackredit#80, also needed by Sabueso's
required dependency closure under uibcdf/sabueso#108. The other component
owners retain their own implementation and scientific qualification work.

## Universal requirement decision — 2026-10-02

The maintainer explicitly requires Python 3.14 support from every registered
Python component now. The common required range is `>=3.11,<3.15`, with four
required full CI minors; development remains Python 3.13. Initial-cohort
membership no longer controls applicability. The common guide conveys this
to all members. Adoption remains measured separately from the requirement,
and pending migration cannot create a delivered-support badge or public
artifact claim.

Ackredit's root instructions still explicitly denied authorization and its
metadata capped Python below 3.14 at source `6420407`. Its successful earlier
two-platform feasibility run `36693052801` is source evidence, not ordinary
installed/public delivery: the old workflow used `--ignore-requires-python`.
The suite authorizes its migration under #80, requiring normal installation,
required 3.14 CI, coherent environments/recipe/instructions, and delivery
evidence before admission. The common gate and starter require four minors;
the regression
`tests/test_governance.py::GovernanceTests::test_every_python_member_requires_314_without_inheriting_admission`
checks universal applicability without promoting an unqualified badge.

## Qualified Ackredit source and guide delivery — 2026-10-02

Immutable `policy-v1.5.3` at central `4010595` publishes the universal
requirement and includes the admitted OpenCASTp registry entry. All 16 member
copies of the canonical guide are synchronized and pushed through the central
tool. Active original checkouts remain preserved; MolSysMT/MolSysViewer receive
only the guide, with scientific suites still deferred.

Ackredit source `e4a006a6931f3fb5f97be5b09767c144dfb35662` passes ordinary
routine CI `37073478950`, shared policy `37073479396`, and full Linux/macOS
arm64 Python 3.11–3.14 matrix `37074118479`. Native evidence confirms all eight
normal install, off-checkout import, interpreter/architecture and full test
steps executed successfully. Local isolated Python 3.13 regression passes
1,530 tests. Its seventh strict required PR check is Linux 3.14, with the
existing internal bypass preserved. Recovery probe `37075039313` recognizes
the four-minor source watermark with zero pending skips and omits heavy jobs.

Ackredit remains `authorized`: public portable-API delivery and independent
consumer installation are still pending under #80/#22/#75. DockingMT,
ElastNetMT, LinDelINT, PharmacophoreMT and TopoMT still have source declarations
excluding 3.14; their mandatory adoption remains open in this tracker and is
not certified by the new guide. Full machine receipts and source observations
are in `devguide/rollouts/python314_required_adoption.json`.
Platform coordination is raised in uibcdf/moli#37.

After documentary push `16b9598 [skip ci]`, native GitHub confirms the
administrator route bypasses the seven required checks. Brief probe
`37075787493` detects exactly one pending skipped commit since `e4a006a`;
probe mode intentionally omits heavy jobs and leaves nightly recovery due.
This is evidence of debt retention, not a successful recovery-suite claim.

## Remaining source contracts and measured qualification — 2026-10-03

The five remaining migrations are published through direct commits on `main`,
using isolated source clones and preserving original worktrees and concurrent
DockingMT development. Their package metadata, full CI, contributor instructions,
applicable noarch recipes and installed-candidate gates now cover Python
3.11–3.14. All call immutable `policy-v1.5.3`; every policy run passes. Existing
older-minor dependency routes are retained; new 3.14 lanes use exact reviewed
provider revisions whose metadata admits that interpreter. No Requires-Python
override, scientific expectation change or public package upload is used.

| Owner | Measured source evidence | Remaining qualification |
| --- | --- | --- |
| uibcdf/lindelint#14 | `bf3fc3a`, CI [37105584626](https://github.com/uibcdf/lindelint/actions/runs/37105584626): all eight Linux/macOS ARM cells pass | Public candidate/channel delivery under uibcdf/lindelint#13 |
| uibcdf/elastnetmt#19 | `062d634`, CI [37106324494](https://github.com/uibcdf/elastnetmt/actions/runs/37106324494): governance and all four 3.13/3.14 cells pass | Known trajectory failures in four older-minor cells under uibcdf/elastnetmt#14 and uibcdf/elastnetmt#17; public delivery under uibcdf/elastnetmt#18 |
| uibcdf/pharmacophoremt#23 | `9c67ee2`, CI [37105628282](https://github.com/uibcdf/pharmacophoremt/actions/runs/37105628282): governance and all eight cells pass | Public noarch delivery and independent installation |
| uibcdf/dockingmt#30 | `ff64d84`, CI [37107875583](https://github.com/uibcdf/dockingmt/actions/runs/37107875583): four Linux minors pass; `0c48cf7`, full [37108673271](https://github.com/uibcdf/dockingmt/actions/runs/37108673271): six cells pass including macOS ARM 3.13/3.14 and required Vina | Public delivery and independent installation |
| uibcdf/topomt#16 | `e1d2fee`, CI [37105640084](https://github.com/uibcdf/topomt/actions/runs/37105640084): 3.14 ordinary installation/import succeeds on both platforms; Linux full tests report 2,003 passes and seven failures | One packaging guard corrected locally at `3fddc22`; six scientific failures remain with the component team; no passing matrix or feasibility admission |

LinDelINT, ElastNetMT, PharmacophoreMT and DockingMT now have measured new-minor
feasibility and are `authorized` in the registry. TopoMT remains outside that
qualification table until its scientific evidence passes. All five still have
pending public admission; their badges retain the previous claim. Authorization
does not erase ElastNetMT's older-minor failures or qualify public dependencies.
MolSysMT/MolSysViewer code and scientific suites remain untouched by this work.

Existing matrix and metadata guards were aligned to the new contract. Actionlint
also reproduced malformed test-results expressions in four workflows; each full
condition is now one expression, retaining only Linux/Python 3.13 publication.
DockingMT's installed metadata check compares parsed specifier sets to handle
Setuptools' equivalent ordering. TopoMT's packaging guard uses the public
`packaging` requirement parser to compare names rather than versioned strings.
These corrections change administrative checks, not scientific behavior.

Strict required PR checks now include Linux/macOS ARM 3.14 where the full matrix
already protects PRs; DockingMT adds Linux 3.14 to its existing Linux PR route.
The previous checks and administrator direct-push bypass are preserved. Recovery
regressions reject a successful historical three-minor matrix as a four-minor
watermark. Native brief probes all pass and omit scientific jobs:

| Component | Probe | Watermark and retained skipped commits |
| --- | --- | --- |
| LinDelINT | [37109918242](https://github.com/uibcdf/lindelint/actions/runs/37109918242) | `bf3fc3a`; one pending skip |
| ElastNetMT | [37109920569](https://github.com/uibcdf/elastnetmt/actions/runs/37109920569) | No passing four-minor watermark; 52 historical skips remain pending |
| PharmacophoreMT | [37109922747](https://github.com/uibcdf/pharmacophoremt/actions/runs/37109922747) | `9c67ee2`; one pending skip |
| DockingMT | [37109949389](https://github.com/uibcdf/dockingmt/actions/runs/37109949389) | `0c48cf7`; one pending skip |
| TopoMT | [37109925282](https://github.com/uibcdf/topomt/actions/runs/37109925282) | No passing four-minor watermark; 57 historical skips remain pending |

Each probe decides that full recovery is due; probe success is neither an
executed recovery suite nor a passing scientific matrix. Nightly recovery remains
due. Machine receipts and checkpoint source SHAs are in
`devguide/rollouts/python314_remaining_source_adoption.json`, superseding the
old-cap observations dated 2026-10-02 in the earlier delivery receipt.
The central guard passes all 272 unit tests and the changed Python files pass
Ruff lint and format checks. This coordination issue remains open for delivery
and the component-owned blockers above.

## Dependencies and risks

No strict issue blocker is established yet. Native packages and optional scientific
dependencies may have different release paths; an editable source import alone does not
prove a distributable 3.14 package.

## Provenance

Source inspection on 2026-09-26 from fetched `origin/main` refs in
`/home/diego/repos@uibcdf`, host `nauta`;
the new development environment uses CPython 3.14.7. No runtime measurement for the six
is claimed by this report.

## Concurrent routine-interpreter decision — 2026-10-03

While publishing this checkpoint, remote commit
`5a90853d4ac147f7b831cfc37f9f5defd87c190a` introduced `policy-v1.5.4`
and Python 3.14 as the routine local/push/PR interpreter under
uibcdf/molsyssuite#39. That accepted source change is preserved by rebase.
The observations above qualify the exact recorded `policy-v1.5.3` sources;
their routine-3.13 wording describes that earlier snapshot, not the new
current baseline. Four-minor evidence remains valid at its recorded SHAs.

Native remote inspection found no published `policy-v1.5.4` tag at this
checkpoint. Publishing that new immutable policy and distributing its revised
guide/callers requires coordination with the concurrent change. The five
component callers and delivered guides observed here remain at 1.5.3; do not
claim completion of the new 1.5.4 rollout from these receipts. Public Python
admission and scientific blockers remain independent of that publication.

## Subsequent policy publication — 2026-10-03

The maintainer approved the newer routine baseline. Policy-v1.5.4 is now
published at immutable e459ea0, with all sixteen guide consumers and fifteen
Python callers updated. Exact deployment and routine/admin verification are
in [the subsequent receipt](../rollouts/policy154_routine_adoption.json), owned
by uibcdf/molsyssuite#39. Fourteen policy gates pass; MolSysMT's independent
archive-tag rejection is tracked as uibcdf/molsyssuite#84 pending a decision.

The earlier 1.5.3 source measurements above remain scoped to their recorded
commits and closures. They do not certify later concurrent scientific commits
or public artifact/channel delivery. No scientific suite of MolSysMT or
MolSysViewer is launched; their older routine routes remain bounded and visible
under uibcdf/molsysmt#237 and uibcdf/molsysviewer#93. The component-owned public
delivery and remaining scientific qualification gates keep #51 open.
