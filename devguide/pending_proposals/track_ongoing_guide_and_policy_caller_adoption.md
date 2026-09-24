---
summary: Track ongoing guide and policy caller adoption across members.
issue: uibcdf/molsyssuite#34
status: active
opened: 2026-09-21
closed:
verification: measured
area: [governance, documentation, ci]
guard: .github/workflows/check-vendored-guides.yaml
normative: devguide/adoption_lifecycle.md
blocked_by: []
supersedes: []
---

# Track ongoing guide and policy caller adoption across members

**Reported:** 2026-09-21, after a canonical guide update and the policy 1.4.1 rollout.
**Status:** Active; `uibcdf/molsyssuite#35` is the first concrete guide rollout used to
exercise and refine the process. The current central release is `policy-v1.4.10`;
`policy-v1.4.6` remains the minimum release gate, subject to member-specific
compatibility checks. Older pins below are observations in consumers.

## What

MolSysSuite already registers canonical guides and consumer copies and checks byte
equality. It also checks versioned policy-workflow callers. Those checks detect
staleness, but neither turns a publication into assigned, reviewable adoption work
across all registered members. A guide-only edit and a new required policy release
are different events and should not be coupled mechanically.

## How

Maintain a central inventory of each consumer, canonical guide revision, current
copy, required policy release, caller pin, owner, exception, and next action. When a
canonical guide changes, identify affected consumers and prepare reviewable updates
or pull requests. When a new policy release is required, propose its caller-pin
change with any necessary migration and local validation. Keep component review and
CI before publication; direct main commits require authorization. The
existing drift and conformance guards should verify convergence and report actionable
remaining work.

The implementation is `devtools/scripts/adoption_status.py`. It emits independent
guide and policy records, supports text and JSON output, validates bounded exceptions,
and can fail a rollout check while any selected record is stale, missing or unavailable.

## Why

The current guard can remain red across the entire registry after central
publication, leaving maintainers to discover and coordinate updates manually.
An ongoing publication-to-adoption lifecycle prevents members from quietly keeping
obsolete instructions or an obsolete gate without making every prose change a
runtime-policy update.

## What is measured and what is assumed

On 2026-09-21, hosted MolSysSuite run
`35596834974` of `.github/workflows/check-vendored-guides.yaml` reported
`GUIDE_DRIFT` for `MOLSYSSUITE_GUIDE.md` in all 13 registered members and for
`GH_RUN_RECEPTOR_GUIDE.md` in MolSysViewer. The workflow already runs on relevant
central pushes, weekly schedule, and manual dispatch; it checks exact copies but
does not propose updates. The central repository checker enforces applicable
versioned policy caller pins. It is assumed that a reviewable cross-repository
proposal mechanism can be built with acceptable permissions; credential design
and rollout batching have not yet been decided.

On 2026-09-22, the central checkout was refreshed to `policy-v1.4.3`. Inspection of
published default branches found ArgDigest already on `policy-v1.4.3`, DockingMT on
`policy-v1.4.2`, and the remaining applicable members on `policy-v1.4.1`. These are
separate policy-adoption records; they do not invalidate the independently completed
Ackredit guide-copy rollout.

On 2026-09-22, PyUnitWizard's new Python 3.14 authorization exposed the
immutable-snapshot boundary: its first hosted policy run `35706813034`
executed the still-pinned `policy-v1.4.3`, whose registry did not yet contain
`uibcdf/pyunitwizard#78`, and rejected the target metadata with `PYTHON_RANGE`.
This is a necessary new policy release, not guide drift. Policy `1.4.4` adds
the authorized registry entry; PyUnitWizard is its first consumer. The live
inventory must retain every other stale caller as explicit adoption work
instead of treating the new tag as automatically adopted suite-wide.

Annotated tag `policy-v1.4.4` was published at commit `ebdcf49`; PyUnitWizard
adopted it at `2dbd9bc` and its hosted policy run `35708012251` passed. The
local policy-only inventory immediately afterward reported PyUnitWizard
`current` and 13 other registered callers `stale` (most already predated
`1.4.3`). Those thirteen are still assigned adoption work, not failures of
PyUnitWizard's gate or evidence of suite-wide completion.

Policy `1.4.5` records PyUnitWizard's independently verified public 0.26.0
Python 3.14 release as `admitted`. Its caller and Python badge must adopt the
new immutable tag together; other members' older pins remain separately tracked
and are not silently migrated by this registration change.

On 2026-09-22, a bounded policy-caller rollout moved SMonitor, ArgDigest,
DepDigest, Pytest Receptor, GH Run Receptor, MolSysMT, MolSysViewer, TopoMT,
DockingMT, Ackredit and Lindelint to `policy-v1.4.5`. PyUnitWizard was already
current. GH Run Receptor confirmed successful hosted policy runs for ten newly
updated consumers: SMonitor `35723875418`, Pytest Receptor `35723876073`,
MolSysMT `35723875632`, MolSysViewer `35723875386`, DockingMT `35723875739`,
Ackredit `35723876067`, Lindelint `35723875847`, ArgDigest `35764236598`,
DepDigest `35764238121`, and GH Run Receptor `35764236974`.

TopoMT's caller is current, but hosted run `35723875941` failed its existing
full-repository Ruff gate with 603 findings. That repository-level migration is
already tracked by `uibcdf/topomt#16`; a current pin is not being presented as a
green adoption. PharmacophoreMT and ElastNetMT remain deliberately pinned to
`policy-v1.4.1` while their measured local migrations remain open as
`uibcdf/pharmacophoremt#3` and `uibcdf/elastnetmt#12`. The live policy inventory
therefore reports 12 current callers and two stale callers; the central rollout
remains active.

Policy `1.4.6` adds the sibling-dependency CI acquisition guard resolved in
`uibcdf/molsyssuite#31`. It was published at `182d484` and the central hosted
governance run `35783728127` passed. PyUnitWizard adopted the immutable caller at
`06566cf`; GH Run Receptor observed its hosted policy run `35783928343` pass.
The local policy-only inventory then reported one current caller (PyUnitWizard)
and thirteen stale callers. Ackredit's local checkout was twelve commits behind
its fetched default branch; both its local and fetched policy callers remained at
`1.4.5`. ArgDigest and TopoMT had unrelated local changes and were left untouched.
This is an adoption snapshot, not a claim that the new guard has proven every
component's environment can solve or install.

The next bounded rollout moved SMonitor (`f9e9ed4`), DepDigest (`073f105`),
MolSysMT (`44f4236b8`) and MolSysViewer (`8ed632ba`) to `policy-v1.4.6`.
The common offline checker passed for all four. GH Run Receptor confirmed green
hosted policy runs `35785458460`, `35785463600`, `35785483875` and
`35785476690`, respectively. MolSysMT used its required `[skip ci]` commit
convention, followed by an explicit `workflow_dispatch` of the policy gate.
Its legacy-tree full Ruff check still reports 576 existing findings, while the
critical-rule gate passes; `uibcdf/molsysmt#212` retains that separate debt.
The policy-only inventory now reports five current callers and nine stale ones.

The following bounded rollout moved ArgDigest (`52f5521`), Pytest Receptor
(`cfb4067`), GH Run Receptor (`fa90e46`) and Lindelint (`1a70034`) to
`policy-v1.4.6`. The common offline checker and hosted policy runs
`35788007089`, `35788656344`, `35788659548` and `35788666769` passed,
respectively. ArgDigest's unrelated untracked `devtools/conda-envs/=18` was
preserved. GH Run Receptor's local suite exposed an obsolete test assertion for
`policy-v1.3.0`; the same focused commit updated it to the adopted pin, after
which 451 tests and Ruff passed. Pytest Receptor ran 172 passing tests with nine
optional-plugin skips; Lindelint passed its five tests and Ruff gates. The
policy-only inventory now reports nine current callers and five stale ones:
Ackredit, DockingMT, TopoMT, PharmacophoreMT and ElastNetMT. Their separate
checkout and migration conditions are not erased by this caller rollout.

The Architecture 1.0 ambassador-guide update was published in MolSysSuite as
`7ab6a35` and synchronized to all 14 registered component copies of
`MOLSYSSUITE_GUIDE.md`. Five stale `ACKREDIT_GUIDE.md` copies were synchronized
in the same guide-only batch, using their Ackredit-owned canonical source.
The local byte-equality check and guide-only adoption inventory now pass for
every registered copy; the manually dispatched hosted guide workflow
`35795393294` also passed. This is guide adoption only: the policy inventory still
has nine current callers and the same five stale callers listed above. The
MolSysMT guide commit was rebased over two unrelated concurrent documentation
commits and published without overwriting them. Unrelated local changes in
ArgDigest and TopoMT were left untouched.

Ackredit (`7990bb1`) and DockingMT (`cfdc8fa`) then adopted the immutable
`policy-v1.4.6` caller. Both passed the central offline conformance checker and
their hosted policy runs (`35823050823` and `35823050325`). Ackredit passed
1,382 local tests and hosted CI run `35823050350`; one local wheel-build test
was skipped because its isolated build environment was unavailable. DockingMT's
four governance tests passed after updating an obsolete pinned-version assertion.
Its product CI run `35823049829` failed because the source-installed scientific
stack lacked the optional `Bio` module; the same failure was present in the
pre-adoption run `35795373825`. DockingMT resolved that separate defect under
`uibcdf/dockingmt#11` by adding Biopython to its committed Conda test
environment. Hosted CI run `35823963841` then passed all three Python test
lanes and quality; policy run `35823964246` also passed. Local integration
tests still expose a MolSysViewer addon mismatch, which is not claimed to be
repaired by the caller or CI-dependency changes. The live policy inventory now
reports 11 current callers and three stale callers:
TopoMT, PharmacophoreMT and ElastNetMT, each with a local migration issue.

On 2026-09-23, central `policy-v1.4.9` moved the general Python, CI, Ruff and
release-version values to the immutable MOLI commit recorded in `suite.toml`.
This is a central policy publication, not a member rollout: the required member
caller remains `policy-v1.4.6`. After fetching every registered checkout, the
live inventory reported all 77 guide relationships current and 11 of 14 Python
policy callers current against that required release. TopoMT still calls
`policy-v1.4.5`; PharmacophoreMT and ElastNetMT still call `policy-v1.4.1`.
The central governance validator and 132 tests passed against the pinned MOLI
snapshot. The new offline repository checker found no findings in eight of the
14 Python members; three transition members were flagged only because their
existing `1.4.6` caller is not a transition-compatible `1.4.9` snapshot, and
the three previously tracked local migrations retain their findings. These
offline observations do not prove hosted `1.4.9` adoption in any member.

The follow-up inventory correction separates the central release from caller
compatibility. Under `policy-v1.4.9`, eight existing `1.4.6` callers are
compatible and six are not currently admitted by the combined release and
member-specific Ruff CI rules. The latter six are ArgDigest, DepDigest,
GH Run Receptor, TopoMT, PharmacophoreMT and ElastNetMT. The first three are
transition members whose `1.4.6` caller does not supply the required Ruff CI
coverage and whose local workflows do not provide both Ruff commands.
`policy-v1.4.7` remains excluded even though its version number exceeds the
`1.4.6` release-gate minimum. This replaces the earlier equality-based
11-of-14 adoption count; it does not claim new member deployments.

On 2026-09-23, MOLI published its Python ecosystem policies at
`888902eb2ccc482c62c6f75da9d8f0bf9bb56442`. MolSysSuite inherited that
exact revision in commit `7aec9c3` and immutable `policy-v1.4.10`. The central
validator and 138 tests passed; the new member review inventory records all 14
Python members as `pending` for support libraries and developer tools. This is
separate from guide and policy-caller adoption. The new canonical
`MOLSYSSUITE_GUIDE.md` was synchronized to all 15 registered consumers using
`sync_vendored_guides.py`, with one guide-only commit per repository. The local
guide inventory and the repeated hosted vendored-guide and component-guide
audits (`35929003666`, `35929003606`, attempt 2) passed. Initial hosted attempts
ran before member publication and failed on expected guide drift. The live
policy-caller inventory now shows 13 compatible older releases and one stale
caller: TopoMT remains on `policy-v1.4.5` under `uibcdf/topomt#16`. Compatibility
does not establish adoption of the newly inherited ecosystem policies; those
reviews advance only with member evidence or a bounded exception. The platform
handoff and remaining member work were reported to `uibcdf/moli#6`.

On 2026-09-24, ElastNetMT's source dependency repair passed hosted CI
`35961592607` and policy `35961592959`; its migration issue
`uibcdf/elastnetmt#12` was closed. PharmacophoreMT repaired the ERalpha
scientific defect under `uibcdf/pharmacophoremt#5`, archived its guard, and
closed that issue and migration issue `uibcdf/pharmacophoremt#3` after local
pytest-receptor passed 23 tests and hosted CI `35988945532` passed all six
jobs with policy `35988946765` green. TopoMT published its complete Ruff
baseline and `policy-v1.4.10` caller at `0fd4cd5`; hosted Ruff
`35990324990` and policy `35990325527` passed. Its full local test run and
an isolated run of the previous commit both yielded exactly 672 passed,
82 failed, 61 skipped and five expected failures, with the same nine failure
groups. These preexisting product and environment failures keep
`uibcdf/topomt#16` open pending a green full CI matrix. The policy inventory
therefore has one current caller (TopoMT), 13 compatible callers, and no
inadmissible pins. All 14 separate Python ecosystem reviews remain pending;
the closed ElastNetMT and PharmacophoreMT migration issues no longer serve
as review owners, so their pending review records point to
`uibcdf/molsyssuite#6`. Concurrent new canonical-guide changes at `7e51830`
have their own copy rollout and are not counted as complete here.

## Alternatives and refuted paths

- Automatically rewrite and push each member workflow for every guide edit: rejected
  because guide content and versioned policy behavior change independently and
  member maintainers need local validation.
- Keep only the red central detector: insufficient because it identifies drift but
  does not assign or complete adoption.
- Use unpinned policy callers: rejected because it would make policy behavior change
  without a reviewable member commit.

## Scope and exclusions

This applies to registered MolSysSuite members and canonical integration guides.
It owns ongoing adoption after central publication. The initial policy-1.0 rollout
remains `uibcdf/molsyssuite#6`; vendored ownership and drift semantics were settled
under `uibcdf/molsyssuite#12`. It does not change component-specific release gates
or require automatic merging.

## Acceptance criteria

- The central inventory distinguishes guide copy drift from policy caller pin drift.
- Each canonical guide or required policy-release change yields reviewable, assigned
  member adoption work or an explicit, expiring exception.
- Central guards identify the affected member, expected source or version, and next
  action, and converge to green after adoption.
- A guide-only edit does not force a caller-pin bump; a required policy release
  cannot be called fully adopted while applicable members are stale or unexcepted.
- A normative operational procedure and an automated guard protect this lifecycle.

## Local implementation issues

`uibcdf/molsyssuite#35` is the first central rollout case. Open member issues only where
migration needs component-specific work.

## Dependencies and risks

Cross-repository write permissions must be narrowly scoped if automation proposes
pull requests. The process must tolerate members with concurrent work and avoid
making a permanently failing guard into accepted background noise.

## Provenance

GitHub Actions run `35596834974` on 2026-09-21, using the central
`check-vendored-guides.yaml` workflow. The inspected local source was the
MolSysSuite checkout on Linux; no Python runtime claim is involved.
