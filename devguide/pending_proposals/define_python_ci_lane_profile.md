---
summary: Define observable CI lane coverage for Python package members.
issue: uibcdf/molsyssuite#39
status: active
opened: 2026-09-22
closed:
verification: measured
area: [ci, python, governance]
guard:
normative: devguide/python_ci_policy.md
blocked_by: []
supersedes: []
---

# Define the Python CI lane profile

**Reported:** 2026-09-22 by Ackredit after its first supported-minor and
experimental-minor CI lanes exposed gaps in the shared contract.
**Status:** Active rollout. The suite maintainer chose a Python 3.13 push/PR
default and a weekly full supported-minor matrix on 2026-09-23, then required
the complete test suite on PRs and conditional daily recovery of skipped
direct pushes on 2026-09-28. On 2026-10-02 the maintainer moved routine local
development and the push/PR default to Python 3.14, while retaining older
supported minors in the full matrix. The accepted
normative target, registry minimum, starter-kit workflow, read-only workflow
inventory and per-member review records exist. Member-specific claims,
enforcement and rollout remain pending.

## What

Define what CI evidence a registered `python-package` must produce for each
supported Python minor, when that evidence must run, and which additional
operating systems the component claims. Keep this CI contract separate from
`role`, `membership`, `maturity` and `development-mode`, which classify real
repositories rather than their workflow topology.

The existing Python policy requires Linux lanes for every supported minor but
does not specify push, pull-request or scheduled triggers. The current
`PYTHON_CI` checker only finds version literals anywhere in workflow text; a
release or documentation workflow can therefore satisfy it without a test job.
The new checker must reason about active test jobs and observable outcomes.

## How

### Agreed default, pending implementation

- On direct pushes, run a Linux test lane on Python 3.14, the routine
  development minor. Components with a demonstrably expensive scientific
  suite may use a bounded smoke suite, clearly labelled as such. Every PR
  runs the complete test suite on Linux 3.14; members may run a wider PR
  matrix. The direct-push exception for named internal maintainers does not
  require a full suite after each commit.
- When a member permits CI-skip markers on direct pushes, run a conditional
  full Linux matrix daily for skipped commits since the last successful,
  executed full matrix. A missed or failed run leaves the backlog due, and
  history uncertainty triggers the full suite. PRs cannot bypass their full
  check with a skip marker.
- At least weekly, run the complete required suite on Linux for every supported
  Python minor. Before adding a new minor to metadata or publishing a release,
  verify a green full matrix for the exact candidate commit, through schedule
  or manual dispatch. A new scheduled lane does not count until a manual
  dispatch has passed; a configured cron is not executed evidence.
- Record non-Linux platform coverage explicitly. A `noarch` artifact is not
  evidence that code and its dependency stack work on macOS or Windows.
  A platform claimed by a component needs a gating representative lane and a
  regular full supported-minor matrix, or an explicit tracked exception. Do
  not force all three operating systems merely from `python-package` or
  `noarch` status.
- Require an initial green manual dispatch whenever a new scheduled matrix or
  platform is introduced. A cron entry is a promise of future evidence, not
  evidence that the lane has already run. Stagger schedules rather than
  requiring every member to start at the top of the same hour.
- Use a separate, explicitly invoked feasibility workflow for an unsupported
  Python minor. Its failed run remains visibly failed, but it is not a required
  branch check or support claim. Do not count `continue-on-error` jobs as
  passing evidence; a green workflow can contain a failed experimental job.
  Admission moves the minor into the required lanes with the metadata change.

### Implementation slices

1. Represent the suite-wide minimum under a dedicated CI policy in
   `suite.toml`, not as a new member `role` or maturity. The normative text
   belongs in a linked CI policy, and the starter-kit template must use the
   accepted shape. Per-member CI mode/platform claims and exceptions are
   still to be reviewed and registered during rollout.
2. Build a read-only inventory that parses configured workflow events, jobs and
   expanded static matrices. The first slice reports `(event, OS, Python,
   direct pytest command, gating, conditions)` and unresolved values. It does
   not yet infer test level (smoke versus full), executed runs or outcomes.
   Workflow names, comments, release steps and isolated version literals are
   not test evidence. A later checker needs explicit or otherwise validated
   test-level semantics before enforcing the complete-matrix requirement.
3. Test the parser against real repository patterns and adversarial fixtures:
   a version mentioned only in comments, a scheduled-only lane, an excluded
   matrix cell, an experimental `continue-on-error` failure, and a job skipped
   by `if` or path filters must not count as a required push/PR test lane.
4. After reviewing inventory and member-specific migration cost, make the versioned shared
   policy workflow enforce the agreed minimum. Roll out caller pins under
   `uibcdf/molsyssuite#34`; do not silently rewrite member workflows.

## Why

Ackredit had promised Python 3.11–3.13 while its push CI originally ran only
3.13 (`uibcdf/ackredit#63`). Its first non-blocking 3.14 job failed in the
Conda solver before pytest but the overall run was green
(`uibcdf/ackredit#64`). These are different failures: missing coverage and
false interpretation of attempted transition evidence. A common CI contract
must make both visible without making every repository use identical YAML.

## What is measured and what is assumed

**Source inspection on 2026-09-23, Linux development checkout:**

| Member or group | Push/PR test evidence | Scheduled or separate evidence |
| --- | --- | --- |
| SMonitor, DepDigest, ArgDigest | Linux 3.13 | Weekly Linux/macOS/Windows 3.11–3.14 |
| PyUnitWizard | Linux 3.13 | Weekly Linux/macOS 3.11–3.14 |
| MolSysMT | Linux 3.13 smoke | Weekly full Linux 3.11–3.13 |
| MolSysViewer | Linux/macOS 3.11–3.13 | The same workflow also schedules a matrix |
| Pytest Receptor | Linux 3.11–3.14, with pytest 8 and 9 | Platform-specific release evidence is separate |
| Ackredit | Linux 3.11–3.13 and macOS 3.13; 3.14 experimental | Weekly Linux/macOS 3.11–3.13 plus experimental 3.14 |

The observations come from each repository's `.github/workflows/` files, not
from an assertion that every scheduled lane has executed successfully. In
particular, Ackredit had to dispatch its newly added scheduled matrix by hand
before the next cron. The current checker uses `_version_is_present` over the
concatenated workflow text; it does not bind a version to a trigger, job or
test command.

**Complete static inventory on 2026-09-23:** all 14 registered Python members
were checked against their current local `main` after fetching their remotes.
This table describes configured direct pytest cells, not passing hosted jobs,
full-suite semantics, or an established platform-support claim. The scheduled
matrix column only reports configured cells; cron frequency, completion and
initial manual dispatch still need verification.

| Member | Configured push/PR Linux 3.13 test | Configured scheduled Linux matrix | Review needed |
| --- | --- | --- | --- |
| SMonitor | Yes: an unfiltered QA suite and a conditional, path-filtered CI lane | 3.11–3.14 | Review which gate represents the required suite and hosted results. |
| ArgDigest, DepDigest | Yes, conditional and path-filtered | 3.11–3.14 | Review filters and hosted results. |
| PyUnitWizard | Yes, conditional and path-filtered | 3.11–3.14 | Review filters and hosted results. |
| MolSysMT | Yes, smoke and data-integrity lanes, path-filtered | 3.11–3.13 | Link the bounded-smoke justification and full-suite evidence. |
| MolSysViewer | Yes, conditional and path-filtered | 3.11–3.13 | Review skip-CI conditions, filters and hosted results. |
| Pytest Receptor | Yes, 3.11–3.14 on push/PR | None | Add a weekly full matrix or tracked exception. |
| gh-run-receptor | No; compatibility tests are dispatch-only | None | Add a routine 3.13 gate and weekly full matrix. |
| TopoMT | Yes, path-filtered | 3.11–3.13 | Review filters; preserve unrelated dirty worktree. |
| PharmacophoreMT | No; package tests use 3.10–3.12 | 3.10–3.12 | Align the supported range and test 3.13. |
| ElastNetMT | No package-suite lane; a separate 3.13 contract test exists | Package suite on 3.10–3.12 | Align package-suite coverage with the supported range. |
| DockingMT | Yes, 3.11–3.13 on push/PR | None | Add a scheduled full matrix or tracked exception. |
| Ackredit | Yes, 3.11–3.13; 3.14 is non-gating | 3.11–3.13; 3.14 is non-gating | Keep experimental 3.14 separate; verify full-suite semantics. |
| Lindelint | Yes, 3.11–3.13 | 3.11–3.13 | Verify hosted full-suite results. |

At this 2026-09-23 snapshot, the first migration target was gh-run-receptor's
missing routine and scheduled lanes, followed by Pytest Receptor and
DockingMT's missing scheduled lanes. The
early-stage ElastNetMT and PharmacophoreMT range mismatches should be handled
as component-owned migration work rather than treated as evidence that the
common policy is already satisfied. A central offline gate must not turn this
static survey into a compliance verdict before it can resolve conditions,
test level and hosted outcomes.

At that snapshot, GH Run Receptor's `compatibility.yml` was deliberately dispatch-only,
and its repository test asserts that it has no push, pull-request or schedule
trigger. Its migration therefore needed a separately reviewable routine/weekly
test workflow or an explicit local decision to change that contract. The
component owns the workflow, its test-level claim and hosted validation; the
central issue tracks the common acceptance criteria.

The inventory is `devtools/scripts/ci_lane_inventory.py`. Run
`python devtools/scripts/ci_lane_inventory.py .. --json` from the central
checkout to inspect all registered Python members, or add
`--repository uibcdf/<member>` to focus on one. It parsed all 14 local Python
members on 2026-09-23. These are static observations only: an unresolved
expression is reported as `unknown`; a direct pytest command is not proof of
its execution, its completeness or a successful outcome. The inventory flags
conditional jobs and test steps, path and ref filters (including tag-only
pushes), and tolerated job or test-step failures. It does not yet interpret
wrapper scripts, reusable workflows, dependency setup, test-level semantics or
hosted run results, so it cannot be used as an admission or policy gate.

The next local parser slice resolves simple `github.event_name` conditions for
each configured event. `event_eligible=true` means the direct pytest step and
its job are enabled by the event condition; `false` means the condition excludes
that event; `null` means another condition remains unresolved. The `conditional`
field now marks that unresolved case. This avoids counting a schedule-only job
as a push test merely because both triggers occur in the same workflow. It does
not clear path/ref filters, prove that a hosted job ran, or classify smoke versus
full tests. In the 2026-09-23 local inventory, GH Run Receptor had no direct Linux
3.13 push/PR pytest candidate, while SMonitor and MolSysMT retained unresolved
conditions on some test jobs. The accepted policy remains in phased adoption;
this inventory change does not activate a conformance gate.

**Review-registry slice on 2026-09-27:** `suite.toml` now has one
`[[python-ci-reviews]]` record for each of the 14 Python members. At introduction,
every record started `pending`, with routine test level and platform claims explicitly
unreviewed; this preserves the difference between configured workflow cells
and supported or passing lanes. `devtools/scripts/python_ci_status.py` reports
the review state and validates future partial, adopted and bounded-exception
records. `validate_governance.py` rejects missing records, unsupported claims,
unsubstantiated adoption and expired exceptions. No member workflow or shared
repository conformance gate changed in this slice. Next, review hosted routine
and full runs with each member, record test level and support claims, and only
then enable a versioned lane checker for reviewed members.

The central hosted governance run `36353113617` for commit `0328552`
passed, as did the component-guide, vendored-guide, Zenodo and issue-label
audits on that commit. This verifies the new registry guard and central
documentation in CI; it does not establish passing member test lanes.

**First member review on 2026-09-27:** GH Run Receptor is now recorded as
`adopted` under `uibcdf/gh-run-receptor#52`; the other 13 entries remain
pending. At source `fc681a2`, `python-routine.yml` has an unfiltered,
non-tolerated full-suite Linux 3.13 job for pushes and pull requests.
The [recent push run](https://github.com/uibcdf/gh-run-receptor/actions/runs/36333697901)
passed at `b0e04d3`. `python-weekly.yml` has Tuesday schedule and manual
dispatch for Python 3.11–3.14 on Linux, macOS and Windows. The
[first manual matrix](https://github.com/uibcdf/gh-run-receptor/actions/runs/35907790354)
and a [later manual matrix](https://github.com/uibcdf/gh-run-receptor/actions/runs/36032624692)
each passed all 12 jobs, including the full pytest step. Hosted logs for the
later matrix identify the macOS runner image as `macos-26-arm64`. The
[exact-tag compatibility run](https://github.com/uibcdf/gh-run-receptor/actions/runs/35573910621)
at `d4a639b` passed all 12 jobs, including wheel build, installation and an
outside-checkout command smoke test; its macOS logs also identify
`macos-26-arm64`. The component's README claims these three OS platforms.
The Tuesday schedule has not yet elapsed since the new workflow was added;
the initial green manual dispatch supplies the policy's required first-run
evidence. Future scheduled and release-candidate outcomes must be reviewed
on their own commits. This member review does not activate the shared checker.

The next workflow target, Pytest Receptor, still has a full Python 3.11–3.14
push/PR matrix but no scheduled matrix in its fetched default branch on
2026-09-27. Its local reporting queues also lack the template, generated
index and offline validator required before a new member implementation
proposal can complete the common issue/devguide lifecycle. The separate
governance rollout is tracked in `uibcdf/molsyssuite#60`; the CI lane need
remains in this issue. Neither finding is a scientific test failure.

**Core-member review on 2026-09-28:** MolSysMT and MolSysViewer remain
`pending` in `suite.toml`. Their workflow structure is compatible with the
accepted target, but configured jobs and past green runs do not establish
adoption for the current candidate.

| Member | Observed source and hosted evidence | Review needed before adoption |
| --- | --- | --- |
| MolSysMT | Source `1de623fc6` configures a Linux 3.13 smoke lane for push/PR, a Monday full Linux 3.11–3.13 lane, and a manual full Linux/macOS arm64 3.11–3.13 candidate matrix. `AGENTS.md` instructs commits to include `[skip ci]` unless told otherwise; the smoke job also skips such commits, and path filters suppress documentation-only runs. This is already tracked as `uibcdf/molsysmt#185`. The [2026-09-25 weekly manual run](https://github.com/uibcdf/molsysmt/actions/runs/36105275495) failed its full pytest step on all three minors at `de9e9c9`. The [earlier full matrix](https://github.com/uibcdf/molsysmt/actions/runs/36120923064) passed six test cells at `e28ceb9`, but the [later candidate matrix](https://github.com/uibcdf/molsysmt/actions/runs/36132035176) failed macOS 3.11 before pytest at `6a334cc`. | Restore an observable routine push/PR signal under `#185`; document the bounded smoke omissions and its full-suite route in a member issue; obtain passing full Linux evidence for the current candidate. Review the public macOS arm64 claim and its recurring lane separately from the manual release matrix. Keep scientific assertions with the component team. |
| MolSysViewer | Source `09d04296` configures Linux/macOS `macos-15` Python 3.11–3.13 test jobs on push/PR, Monday schedule and manual dispatch. Its push/PR paths ignore documentation and YAML files, and `[skip ci]` can skip test jobs. The [2026-09-28 push run](https://github.com/uibcdf/molsysviewer/actions/runs/36389782757) passed the six pytest jobs and the Qt job at `7a19f7e`; the [2026-09-27 manual run](https://github.com/uibcdf/molsysviewer/actions/runs/36338541516) passed six pytest jobs at `19dadc1`. The current source commit is a later documentation commit with `[skip ci]`. | Review the deliberate filters and skip conditions against the routine gate; confirm support claims and exact-candidate installed-package evidence. The next Monday trigger had not yet occurred at this review, so a configured schedule is not recorded as a passed scheduled run. |

The contract permits MolSysMT's bounded smoke lane and MolSysViewer's wider
routine matrix. Do not activate the shared conformance checker for these
members based on this source survey: first record member-owned exceptions or
migrations and passing hosted evidence for the actual lanes. Neither member
is marked adopted merely because a historical run passed.

**Contributor-route amendment on 2026-09-28:** the two MolSysMT maintainers,
Diego (`dprada`) and Liliana (`LMMV`), may continue direct pushes without a
complete suite after each commit. They prefer a short smoke test but may
intentionally skip it during rapid iteration. The component-owned control
under `uibcdf/molsysmt#185` is a conditional full Linux matrix shortly after
midnight in `America/Mexico_City`. It must examine skipped commits since the
last successful *executed* full matrix, so a missed schedule or red run never
erases the debt. Every PR requires the complete suite on the routine Python
minor; MolSysMT chooses its existing six-cell Linux/macOS matrix for PRs.
The weekly full matrix and exact release-candidate gate remain separate.
This amendment changes the earlier push/PR smoke default without claiming
that MolSysMT or any other pending member has completed adoption.

**MolSysMT implementation review on 2026-09-28:** direct-push smoke now
selects four test files; its [hosted run](https://github.com/uibcdf/molsysmt/actions/runs/36403598162)
passed 13 tests in the pytest step. The
[manual full Linux run](https://github.com/uibcdf/molsysmt/actions/runs/36403213916)
executed pytest on 3.11, 3.12 and 3.13 and failed in all three cells with four
failures each. Three cross-component unit-policy assertions already failed
in the [preceding full run](https://github.com/uibcdf/molsysmt/actions/runs/36105275495);
the fourth reports a stale converter table. Those assertions remain with the
component team. The
[hosted backlog probe](https://github.com/uibcdf/molsysmt/actions/runs/36426806753)
ran the detector, found skipped commits without a valid full-matrix
watermark, chose to run the full matrix, and skipped the heavy jobs because
the dispatch was diagnostic. GitHub's actual midnight schedule and the
required PR check have yet to execute. MolSysMT is therefore recorded as
`partial`, with public platform claims still unreviewed.

The MolSysMT backlog detector was then corrected to inspect completed branch
runs directly and to credit successful executed manual `ci-full.yaml` matrices
as well as weekly runs. Its
[hosted probe](https://github.com/uibcdf/molsysmt/actions/runs/36478302828)
at `3deb36aff` recognized the
[green manual matrix](https://github.com/uibcdf/molsysmt/actions/runs/31781216880)
at `38ab61f` and counted 378 skipped commits afterward. The debt therefore
remains due; the diagnostic did not run the heavy jobs. The current
[smoke](https://github.com/uibcdf/molsysmt/actions/runs/36478296550),
[policy](https://github.com/uibcdf/molsysmt/actions/runs/36478297404) and
[Ruff](https://github.com/uibcdf/molsysmt/actions/runs/36478296564) gates pass.

**MolSysViewer implementation review on 2026-09-28:** its
[scheduled six-cell matrix](https://github.com/uibcdf/molsysviewer/actions/runs/36455949357)
passed at `6f49013`, and the
[full push matrix](https://github.com/uibcdf/molsysviewer/actions/runs/36476235643),
[core E2E](https://github.com/uibcdf/molsysviewer/actions/runs/36476235487)
and policy gate passed at `500c556`. `uibcdf/molsysviewer#116` removed PR
path and title/branch skip conditions, configured stable `PR full suite` and
`Core E2E` checks, and enabled branch protection that requires both for PRs
while administrator direct pushes remain available. A deliberately skipped
direct push at `ad43571` was detected as one pending commit by the
[CI backlog probe](https://github.com/uibcdf/molsysviewer/actions/runs/36477025996)
and independently by the
[E2E backlog probe](https://github.com/uibcdf/molsysviewer/actions/runs/36477036433).
Both probes omitted heavy jobs as designed. The first real nightly run, a
hosted PR aggregate and platform-claim review remain; MolSysViewer is
recorded as `partial`, and the skipped candidate is not counted as green.

**SMonitor implementation review on 2026-09-28:** `uibcdf/smonitor#33`
removed PR path and title/branch skip conditions from its full Linux 3.13 CI.
Its `main` branch now requires three strict checks: the primary test job,
`qa`, and `collective-e2e`; administrators `dprada` and `LMMV` retain direct
pushes. The [weekly twelve-cell matrix](https://github.com/uibcdf/smonitor/actions/runs/36457179148)
passed at `fc042c4`; [CI](https://github.com/uibcdf/smonitor/actions/runs/36483279101),
[QA and E2E](https://github.com/uibcdf/smonitor/actions/runs/36483279046),
and [policy](https://github.com/uibcdf/smonitor/actions/runs/36483280197)
passed at `709ecfd`. A [zero-debt probe](https://github.com/uibcdf/smonitor/actions/runs/36483329864)
recognized the executed weekly matrix as its watermark and skipped the heavy
jobs. A direct push with `[skip ci]` at `69bb1a3` bypassed the required PR
checks as intended; a [second probe](https://github.com/uibcdf/smonitor/actions/runs/36484514827)
found exactly one pending skipped commit and again omitted matrix jobs because
it was diagnostic. A [manual full matrix](https://github.com/uibcdf/smonitor/actions/runs/36485266297)
then passed all twelve jobs at `534367f`; the
[following probe](https://github.com/uibcdf/smonitor/actions/runs/36485441346)
recognized that run as the new executed watermark and found zero pending
skipped commits. The actual daily schedule, a hosted PR and platform claims
remain unreviewed, so the central review stays `partial`.

**ArgDigest implementation review on 2026-09-29:** `uibcdf/argdigest#21`
removed PR path and title/branch skip conditions from its full Linux 3.13 CI.
Its `main` branch requires the stable test job with strict checks;
administrators `dprada` and `LMMV` retain direct pushes. The
[weekly twelve-cell matrix](https://github.com/uibcdf/argdigest/actions/runs/36455538074)
passed at `ca537d2`, and [routine CI](https://github.com/uibcdf/argdigest/actions/runs/36531091052)
and [policy](https://github.com/uibcdf/argdigest/actions/runs/36531091809)
passed at `d1df25b`. A [zero-debt probe](https://github.com/uibcdf/argdigest/actions/runs/36531106522)
recognized the executed weekly matrix as its watermark and omitted matrix
jobs. A deliberately skipped direct push at `8a34746` bypassed the required
PR check as intended; a [second probe](https://github.com/uibcdf/argdigest/actions/runs/36531382436)
found exactly one pending skipped commit and omitted heavy jobs because it was
diagnostic. GitHub did not show the 00:37 scheduled run in the observed window,
so a [manual full matrix](https://github.com/uibcdf/argdigest/actions/runs/36532458998)
passed all twelve jobs at `9bb0a8e`. The
[following probe](https://github.com/uibcdf/argdigest/actions/runs/36532645259)
recognized that run as the new executed watermark and found zero pending
skipped commits. The actual daily schedule, a hosted PR and platform claims
remain unreviewed, so ArgDigest stays `partial`.

**DepDigest implementation review on 2026-09-29:** `uibcdf/depdigest#21`
removed PR path and title/branch skip conditions from its full Linux 3.13 CI.
Its `main` branch now requires the stable test job with strict checks;
administrators `dprada` and `LMMV` retain direct pushes. The
[weekly twelve-cell matrix](https://github.com/uibcdf/depdigest/actions/runs/36455844421)
passed at `0353087`, and [routine CI](https://github.com/uibcdf/depdigest/actions/runs/36533588363)
and [policy](https://github.com/uibcdf/depdigest/actions/runs/36533589077)
passed at `e6dfa7c`. A [zero-debt probe](https://github.com/uibcdf/depdigest/actions/runs/36534534264)
recognized the executed weekly matrix as its watermark and omitted matrix
jobs. A deliberately skipped direct push at `d779cfa` bypassed the required
PR check as intended; a [second probe](https://github.com/uibcdf/depdigest/actions/runs/36534652166)
found exactly one pending skipped commit and again omitted heavy jobs because
it was diagnostic. A [manual full matrix](https://github.com/uibcdf/depdigest/actions/runs/36534834729)
then passed all twelve jobs at `80e021e`. The
[following probe](https://github.com/uibcdf/depdigest/actions/runs/36534985790)
recognized that run as the new executed watermark and found zero pending
skipped commits. The actual daily schedule, hosted PR execution and platform
claims remain unreviewed, so DepDigest stays `partial`.

**PyUnitWizard implementation review on 2026-09-29:** `uibcdf/pyunitwizard#91`
removed PR path and title/branch skip conditions from its full Linux 3.13 CI.
`main` requires the stable test check with strict status; the only current
collaborators, administrators `dprada` and `LMMV`, retain direct pushes. The
[weekly eight-cell matrix](https://github.com/uibcdf/pyunitwizard/actions/runs/36457307824)
passed at `4ffe2f1`, and [routine CI](https://github.com/uibcdf/pyunitwizard/actions/runs/36536757396)
and [policy](https://github.com/uibcdf/pyunitwizard/actions/runs/36536758336)
passed at `4b7f5ed`. A [zero-debt probe](https://github.com/uibcdf/pyunitwizard/actions/runs/36536772026)
recognized the weekly matrix. A deliberately skipped push at `cdccfa8`
bypassed the required check. Its
[first probe](https://github.com/uibcdf/pyunitwizard/actions/runs/36537194515)
exposed an old run listing from GitHub's `branch=main` filter; the detector
now lists current runs and filters their `head_branch` itself. The
[corrected probe](https://github.com/uibcdf/pyunitwizard/actions/runs/36538129589)
found exactly one skipped commit. A
[manual matrix](https://github.com/uibcdf/pyunitwizard/actions/runs/36538496360)
executed all eight jobs at `8dc7f63`, but Linux 3.13 failed one component
test with `LibraryWithoutParserError` for `openmm.unit`; the
[following probe](https://github.com/uibcdf/pyunitwizard/actions/runs/36539355874)
confirmed the skipped commit remains due. The component team owns that test
failure. The daily schedule, hosted PR and platform claims remain unreviewed,
so PyUnitWizard is `partial`.

**Detector correction and actual daily evidence on 2026-09-29:** the
PyUnitWizard review exposed an old workflow-run listing returned by GitHub's
`branch=main` API filter. SMonitor reproduced the same discrepancy.
The detectors in PyUnitWizard, SMonitor, ArgDigest and DepDigest now list
runs without that filter and check `head_branch=main` locally, together with
commit ancestry and executed Linux test steps. Their focused regressions
reject a green feature-branch run as a watermark.

SMonitor's [corrected probe](https://github.com/uibcdf/smonitor/actions/runs/36539973071)
at `2e03716` retained `534367f` as the full watermark with zero debt.
Its [actual daily schedule](https://github.com/uibcdf/smonitor/actions/runs/36571010365)
ran the detector, found zero debt and omitted the matrix.
ArgDigest's [actual daily schedule](https://github.com/uibcdf/argdigest/actions/runs/36573874803)
passed twelve test jobs at `417ab9e`, but the previous detector triggered
it after losing the green watermark and counting 68 historical skipped
commits. Its [corrected probe](https://github.com/uibcdf/argdigest/actions/runs/36640897094)
at `6223e01` recognized that scheduled matrix and found zero debt.
DepDigest's [corrected probe](https://github.com/uibcdf/depdigest/actions/runs/36640913043)
at `166e9c9` retained `80e021e` as its full watermark with zero debt.
Routine CI and policy checks passed on both corrected sources; SMonitor's
QA and collective E2E also passed. Heavy jobs were omitted by all corrected
diagnostic probes. SMonitor and ArgDigest now have actual daily-trigger
evidence; their hosted PR and platform reviews still remain. DepDigest and
PyUnitWizard have no observed actual daily run yet. All four reviews remain
`partial`.

**Pytest Receptor implementation review on 2026-09-30:**
`uibcdf/pytest-receptor#11` preserves the existing unfiltered push/PR Tests
matrix across Linux Python 3.11–3.14 and pytest 8/9. At `608b230`,
[Tests](https://github.com/uibcdf/pytest-receptor/actions/runs/36644241696)
passed all eleven jobs, executing both serial and distributed suites in
each of the eight compatibility cells. Reporting governance and suite
policy also passed. The new weekly/manual workflow runs those eight cells
plus two macOS arm64 Python 3.13 representatives, one per pytest major.
Its daily conditional route is staggered at 01:07 in `America/Mexico_City`.
Unlike a quick push lane, a green Tests push is a valid full Linux watermark:
all required Python/pytest pairs must execute both suites successfully.

The deliberate `[skip ci]` push `a7f3b0e` was accepted through the internal
admin bypass. The [debt probe](https://github.com/uibcdf/pytest-receptor/actions/runs/36644755285)
found exactly one pending skipped commit since full Tests at `608b230` and
omitted heavy jobs. The [first manual full matrix](https://github.com/uibcdf/pytest-receptor/actions/runs/36644802980)
passed all ten cells at `a7f3b0e`, including executed serial/distributed
suites and assertions for architecture and pytest major. The
[recovery probe](https://github.com/uibcdf/pytest-receptor/actions/runs/36678939997)
then recognized that commit as the new full watermark and found zero debt.
Actual daily cron execution, hosted PR execution and published platform
claims remain unreviewed, so the registry records `partial`.
The final evidence record is committed at `67bf827`; its
[Tests](https://github.com/uibcdf/pytest-receptor/actions/runs/36682626592),
[reporting governance](https://github.com/uibcdf/pytest-receptor/actions/runs/36682626545)
and [suite policy](https://github.com/uibcdf/pytest-receptor/actions/runs/36682627369)
all passed after the direct push.

**Explicit PR protection correction on 2026-09-30:** inspection of the six
previously reviewed members found strict required status checks and admin
bypass, but `required_pull_request_reviews=null`. Required checks alone do
not establish the agreed external PR route. SMonitor, ArgDigest, DepDigest,
PyUnitWizard, MolSysMT and MolSysViewer now explicitly require PRs with
`required_approving_review_count=0`, using GitHub's
[review-protection API](https://docs.github.com/en/rest/branches/branch-protection#update-pull-request-review-protection).
This adds the PR route without adding mandatory reviewers. Pytest Receptor
received that setting in its initial rollout. A fresh protection read
confirmed all seven have a non-null PR rule, zero mandatory approvals,
their existing strict checks, and `enforce_admins=false`. The internal
maintainers retain direct pushes. Earlier descriptions of required checks
should not be read as evidence that the explicit PR requirement already
existed before this correction. No hosted external PR was created to test
enforcement, and the postponed MolSysMT/MolSysViewer execution reviews
remain postponed.

**DockingMT implementation review on 2026-09-30:** `uibcdf/dockingmt#21`
preserves its unfiltered full Linux Python 3.11–3.13 push/PR matrix and
the scientific sibling commits already fixed in its Conda/source route.
The new periodic workflow follows the starter-kit matrix structure with
that existing dependency-driven variation, tracked by
`uibcdf/molsyssuite#31`. It adds weekly Tuesday 09:17 UTC and manual
coverage on all three Linux minors plus macOS arm64 Python 3.13, with
interpreter, architecture and Vina import assertions. Daily recovery is
staggered at 01:19 `America/Mexico_City`.

At `1dd86ec`, [CI](https://github.com/uibcdf/dockingmt/actions/runs/36685744582)
passed all four quality/full-suite jobs and the
[suite policy](https://github.com/uibcdf/dockingmt/actions/runs/36685745455)
passed. The [initial probe](https://github.com/uibcdf/dockingmt/actions/runs/36685765426)
recognized executed full push CI at `ac91b22`, found zero debt and omitted
heavy jobs. `main` now requires explicit PRs with zero mandatory approvals
and all four strict quality/test checks, with admin bypass for the only
current collaborators, `dprada` and `LMMV`.
The deliberately skipped documentation push `d74aaa1` was accepted with
explicit PR/check bypass notices. Its
[debt probe](https://github.com/uibcdf/dockingmt/actions/runs/36686660142)
found exactly one skipped commit since the executed green full push
matrix at `1dd86ec` and omitted heavy jobs. The
[initial manual matrix](https://github.com/uibcdf/dockingmt/actions/runs/36686938454)
passed all four test cells at `d74aaa1`, including executed interpreter,
architecture and Vina assertions and the full pytest step in every job.
GH Run Receptor preserved GitHub's success; native job/step evidence
separately verified coverage. The decision job was intentionally skipped
for the unconditional manual matrix. The
[recovery probe](https://github.com/uibcdf/dockingmt/actions/runs/36687546093)
recognized `d74aaa1` as the new full watermark, found zero skipped commits
and omitted heavy jobs. Actual daily cron execution, hosted PR enforcement
and publication platform claims remain unreviewed; the registry records
`partial`.
The component's final evidence record is committed at `0420d43` under the
same open local issue; the deployment used direct pushes to `main`.

**Ackredit implementation review on 2026-09-30:** `uibcdf/ackredit#74`
preserves full supported Python 3.11–3.13 Linux push/PR coverage and a
macOS arm64 3.13 routine lane. The existing weekly Linux/macOS matrix now
contains only the six supported cells. Unsupported 3.14 moved from tolerated
cells inside required workflows to a separate dispatch-only feasibility
workflow whose failure remains visible. `requires-python` and suite
admission are unchanged. Explicit `macos-15` runners and full/feasibility
architecture assertions establish which architecture actually executes.
Weekly coverage is staggered at Monday 05:23 UTC; conditional daily
recovery is at 01:31 `America/Mexico_City`.

At `2bb6967`, [CI](https://github.com/uibcdf/ackredit/actions/runs/36692957081)
passed all six mandatory Ruff/documentation/supported-test jobs, and
[suite policy](https://github.com/uibcdf/ackredit/actions/runs/36692957976)
passed. The [initial probe](https://github.com/uibcdf/ackredit/actions/runs/36693051220)
recognized that executed full CI commit, found zero debt and omitted heavy
jobs. The [separate manual 3.14 feasibility run](https://github.com/uibcdf/ackredit/actions/runs/36693052801)
passed Linux and macOS arm64 cells, including executed tests and architecture
assertions; this supplies exploratory evidence and does not admit 3.14.
The updated workflow guards reject unsupported or tolerated required cells,
manual-only feasibility guards preserve failure visibility, and environment
guards retain the existing solver/install contract checks.

Protected `main` now requires explicit PRs with zero mandatory approvals
and the six strict supported checks. Administrators `dprada` and `LMMV`,
the only current collaborators, retain direct pushes. Documentation push
`abce1b0` deliberately skipped CI and was accepted with explicit PR/check
bypass notices. The [debt probe](https://github.com/uibcdf/ackredit/actions/runs/36694080410)
found exactly one skipped commit since full CI at `2bb6967` and omitted
heavy jobs. The [required manual full matrix](https://github.com/uibcdf/ackredit/actions/runs/36694709030)
passed all six Linux/macOS supported cells at `abce1b0`, including executed
interpreter/architecture assertions and full pytest steps. The decision job
was intentionally skipped for the unconditional manual run. GH Run
Receptor preserved GitHub's success, and native job/step evidence verified
all six cells. The [recovery probe](https://github.com/uibcdf/ackredit/actions/runs/36695131397)
recognized `abce1b0` as the new full watermark, found zero skipped commits
and omitted heavy jobs. Actual daily execution, hosted PR enforcement and
publication platform claims remain unreviewed, so the registry records
`partial`.

The component's final evidence record is committed at `bf24c28` under
`uibcdf/ackredit#74`; implementation and evidence used direct pushes to `main`.

The [previous weekly run](https://github.com/uibcdf/ackredit/actions/runs/36415326167)
at `7233f67` failed macOS 3.13 in the component performance test
`test_crediting_one_more_caller_costs_the_same_at_ten_thousand`:
0.7 microseconds per call against no callers became 2.4 against 5,000.
That result remains visible; this routing rollout preserves the runtime and
performance assertions. A later green run does not erase the old failure.

**LinDelINT implementation review on 2026-09-30:** `uibcdf/lindelint#12`
owns the local full-CI routes and skipped-push recovery. Source `78ddc30`
preserves the existing complete six-cell Python 3.11–3.13 Linux/macOS matrix,
its wheel/import gates, distributed pytest selection, Ruff and independent
reporting job. The existing weekly Monday 09:00 UTC route stays unconditional;
manual dispatch runs the same full matrix. Daily recovery is staggered at
01:43 `America/Mexico_City`. The macOS runner is pinned to `macos-15`, with
arm64 and interpreter-minor assertions before tests. No scientific code or
assertions changed.

Main protection now explicitly requires PRs with zero mandatory approvals
and seven strict supported checks. Current collaborator API lists only
`dprada` and `LMMV`, both administrators retaining direct pushes. The
implementation push reported bypass of the PR rule and all seven checks.
[Routine CI](https://github.com/uibcdf/lindelint/actions/runs/36700139663)
passed reporting and all six complete matrix cells; native steps confirm the
interpreter/architecture assertions and full tests actually ran in each.
[Suite policy](https://github.com/uibcdf/lindelint/actions/runs/36700140495)
passed. GH Run Receptor 1.0.0 preserved the successful conclusion.
The [initial probe](https://github.com/uibcdf/lindelint/actions/runs/36700190976)
found zero debt since baseline `ed588ab`, ran independent reporting and
omitted the six heavy jobs. Probe success is never accepted as a full
watermark. The detector accepts only successful ancestral main
push/schedule/manual runs with every supported Linux test step executed;
uncertain evidence runs the full matrix.

The documentation-only skipped push `81c45be` bypassed the PR rule and seven
checks. The [debt probe](https://github.com/uibcdf/lindelint/actions/runs/36700480542)
detected exactly one pending skipped commit since full CI at `78ddc30` and
omitted heavy jobs. [Complete manual CI](https://github.com/uibcdf/lindelint/actions/runs/36700581051)
at the skipped `81c45be` head passed reporting and all six supported
Linux/macOS cells. Native evidence confirmed both full tests and
interpreter/architecture assertions executed successfully in every cell; its
decision job was intentionally skipped for unconditional manual execution.
The [recovery probe](https://github.com/uibcdf/lindelint/actions/runs/36700906324)
recognized `81c45be` as the full watermark, found zero debt and omitted heavy
jobs. No ordinary full push intervened to clear the skipped debt.

Local Python 3.13.15 with NumPy 2.4.6, SciPy 1.18.0 and Numba 0.67.0 passed
12/12 tests, Ruff, reporting/index guards and central component conformance.
Actual daily execution, hosted external-PR enforcement and publication
platform claims remain unreviewed; existing scientific findings
`uibcdf/lindelint#7` and `uibcdf/lindelint#8` remain component-owned, with
ecosystem adoption separately tracked in `uibcdf/lindelint#9`. The CI review
and local issue remain partial/open.

**Concurrent guide publication observed during final validation:** central
commit `bcbcbce` passed governance, Zenodo, component-label and component-guide
audits. Its [vendored-guide audit](https://github.com/uibcdf/molsyssuite/actions/runs/36701423229)
failed because DepDigest published a new canonical `DEPDIGEST_GUIDE.md` in
`08f8263`, with provider integration record `4de4c0a`, during this review.
Native logs identify ten consumers awaiting distribution: ArgDigest,
PyUnitWizard, MolSysMT, MolSysViewer, TopoMT, PharmacophoreMT, ElastNetMT,
LinDelINT, Ackredit and DockingMT. The inspected diff documents optional
executable engines and explicit installer routes; it is separate from this
CI rollout. Publication and consumer adoption are already owned by
`uibcdf/molsyssuite#62` and `uibcdf/depdigest#22`, whose acceptance includes
canonical-guide synchronization and provider release. The failed audit stays
visible; passing LinDelINT CI does not establish guide synchronization or
optional-engine runtime adoption. Distribute the accepted source through
`sync_vendored_guides.py`, preserving active component worktrees and deferred
scientific reviews.

**Guide-distribution follow-up on 2026-09-30:** `uibcdf/molsyssuite#63`
resolved the concurrent DepDigest guide drift. The canonical guide at
`4de4c0a` was distributed byte-identically to all ten consumers through the
registered synchronizer, using isolated current checkouts and documentation-only
direct pushes. The [shared hosted audit](https://github.com/uibcdf/molsyssuite/actions/runs/36705001882)
passed against remote-main checkouts; the distribution record and consumer
commit table are archived centrally. The failure at `36701423229` is retained
as historical evidence. Parent `uibcdf/molsyssuite#62` remains open, and guide
synchronization does not claim consumer runtime adoption. Documentation pushes
used the authorized skip-CI route; existing recovery controls retain debt
until complete coverage succeeds.

**TopoMT implementation review on 2026-09-30:** `uibcdf/topomt#58`
owns local contributor full-CI routes and skipped-push recovery. Source
`100bc49` (routing implementation `8bd0a83`) removes documentation exclusions
from PRs and preserves the complete supported six-cell Python 3.11–3.13
Linux/macOS scientific pytest selection, minor-specific Conda environments,
controlled suite source revisions and separately tested MolSysMT source pin.
macOS is pinned to `macos-15` with interpreter/arm64 assertions before tests.
Weekly Monday 09:00 UTC/manual complete execution remains unconditional;
daily conditional recovery is staggered at 01:55 `America/Mexico_City`.
An independent report/debt/PR-route job selects only administrative modules
with `--noconftest`, avoiding scientific fixture imports for that job. Full
scientific jobs keep their original conftest and collection.

Main was unprotected at initial inspection. It now explicitly requires PRs
with zero mandatory approvals and eight strict Ruff/governance/supported
complete checks. Fresh collaborator API lists only `dprada` and `LMMV`, both
administrators retaining direct pushes. Internal implementation pushes used
`[skip ci]`; GitHub reported bypass of the PR rule and all eight checks.
Concurrent component work advanced main to `c5b6588` before the first push.
The unpublished governance commit was rebased over it; the component's
provider/provenance/AlphaSpace2 changes are preserved. No scientific code,
assertion, dependency pin or support-range change belongs to this review.

The PR-route regression first failed because old PR configuration ignored
Markdown/docs. Seven administrative tests now pass locally; Ruff, reporting
indexes, central conformance and scoped mypy also pass. The
[baseline full CI](https://github.com/uibcdf/topomt/actions/runs/36700609235)
at `507e347` failed all six actual scientific test jobs; Linux 3.11 reported
88 failed, 716 passed, 69 skipped and five xfailed in 816.90 seconds; Linux
3.12 reported the same counts in 1847.47 seconds. Missing fpocket is one of
nine grouped causes. Scientific matrix readiness remains separately owned
by `uibcdf/topomt#16`; optional-engine work remains with
`uibcdf/topomt#56`, `uibcdf/topomt#53` and `uibcdf/molsyssuite#62`.

The [first probe](https://github.com/uibcdf/topomt/actions/runs/36715825226)
at `47683f5` found no eligible executed green full matrix and reported
39 skipped commits, omitting heavy jobs. Its independent governance bootstrap
failed because the scientific Conda pin `pytest-receptor=0.6.0` does not exist
on PyPI. Correction `100bc49` uses exact published `1.0.0` for this new pip job
only; the component's scientific Conda `0.6.0` pins remain unchanged. This
correction adds no common mandatory upgrade. The
[corrected probe](https://github.com/uibcdf/topomt/actions/runs/36716167067)
passed reporting/CI governance and the detector, reported 40 pending skipped
commits after the extra skipped correction, and omitted heavy jobs. Native
steps confirmed both report-index validation and the seven administrative
tests actually succeeded. Probe success did not clear debt or supply a
scientific full watermark. [Ruff](https://github.com/uibcdf/topomt/actions/runs/36716171200)
and [suite policy](https://github.com/uibcdf/topomt/actions/runs/36716176543)
passed at the corrected source.

The final ordinary documentation push at `b6c8b9a` triggered
[Ruff](https://github.com/uibcdf/topomt/actions/runs/36717343437) and
[suite policy](https://github.com/uibcdf/topomt/actions/runs/36717343905),
both successful. Its [probe](https://github.com/uibcdf/topomt/actions/runs/36717343316)
also passed the actual reporting and CI-governance steps and retained all
40 skipped commits with no eligible full watermark. Thus an ordinary commit
after skipped pushes and another successful administrative probe did not erase
the backlog. GH Run Receptor preserved the probe's success with the heavy
matrix intentionally omitted; native detector logs provide the debt evidence.

[Complete manual CI](https://github.com/uibcdf/topomt/actions/runs/36716726423)
was dispatched at `100bc49`; all six cells are running and Linux's three
interpreter assertions passed before their actual scientific test steps began.
The overall result is still pending; native job/step metadata already shows
failures in the actual Run tests steps on Linux 3.11/3.13 and macOS 3.11.
These failures do not establish a successful full watermark. This review
records execution without diagnosing or repairing component scientific
failures. Actual daily execution, hosted external-PR enforcement and
publication-platform claims remain unreviewed. Keep the local issue and
registry review partial. Failed/unexecuted coverage, PRs, other branches and
successful probes cannot clear skipped debt; missing evidence runs complete
coverage rather than assuming cleanliness.

**PharmacophoreMT implementation review on 2026-09-30:**
`uibcdf/pharmacophoremt#9` owns contributor governance and skipped-push
recovery. Source `efc27e3`, with partial record revision `4e856ea`, preserves
unfiltered complete push/PR Python 3.11–3.13 coverage on Linux/macOS, each
minor-specific Conda environment, controlled suite source revisions and the
separately tested MolSysMT source pin. macOS is pinned to `macos-15` with
interpreter/arm64 assertions. The existing independent Reporting governance
job keeps its standard-library report/index validation and adds backlog/route
guards with independent pip tools; only that bootstrap uses published
pytest-receptor `1.0.0`, preserving scientific Conda `0.6.0` pins. No scientific
code, assertions, source pin, support range or collection is changed.

Main was unprotected. It now explicitly requires PRs with zero mandatory
approvals and eight strict checks: existing Reporting governance, existing
`policy / conformance` (including Ruff), and all six supported scientific jobs.
Fresh collaborator evidence lists only `dprada`/`LMMV` as administrators;
GitHub observed their PR/check bypass on both internal skipped pushes.
Weekly Monday 09:00 UTC/manual complete execution remains unconditional;
daily conditional recovery is staggered at 02:07 `America/Mexico_City`.
Failed/unexecuted complete coverage cannot clear skipped debt; API/history
uncertainty or a failed decision job runs full coverage.

The route regression failed on the old dispatch without a probe input and
passed after implementation. Eight local administrative tests, the required
three standard-library reporting tests, Ruff over 135 files, generated
indexes and central conformance passed. GH Run Receptor preserved success for
[weekly baseline](https://github.com/uibcdf/pharmacophoremt/actions/runs/36457546833)
at `98ecb45`; native evidence confirms all six actual scientific Run tests
steps and reporting passed. This is historical execution, not new publication
or installed-artifact evidence. Existing ecosystem adoption and SMonitor
rendering defects remain separately owned by `uibcdf/pharmacophoremt#6` and
`uibcdf/pharmacophoremt#2`.

The [initial probe](https://github.com/uibcdf/pharmacophoremt/actions/runs/36764937398)
at `efc27e3` passed reporting/index/backlog/route steps, recognized the `98ecb45`
executed full watermark and found exactly two pending skips: `d0215fa` (guide
distribution) and `efc27e3` (implementation). Heavy jobs were omitted; successful
administrative execution retained that debt.
[Suite policy](https://github.com/uibcdf/pharmacophoremt/actions/runs/36764942903)
passed at the same source. Record revision `4e856ea` adds one further authorized
skipped documentation commit. Its
[probe](https://github.com/uibcdf/pharmacophoremt/actions/runs/36765380849)
passed governance/detector and retained exactly three pending skips; native
logs demonstrate successful probes do not erase debt.
[Final policy](https://github.com/uibcdf/pharmacophoremt/actions/runs/36765390157)
also passed. The
[manual complete matrix](https://github.com/uibcdf/pharmacophoremt/actions/runs/36765385366)
passed Reporting governance and all six supported cells at `4e856ea`.
Native evidence confirms actual full pytest steps and interpreter/arm64
assertions succeeded in each; the decision job was intentionally skipped for
unconditional execution. GH Run Receptor preserved success. The
[recovery probe](https://github.com/uibcdf/pharmacophoremt/actions/runs/36768440174)
passed reporting/governance and the detector, recognized executed complete
`4e856ea` as its new watermark and reported zero skipped commits while omitting
heavy jobs. The three previously observed skipped commits were cleared only
after successful complete coverage. Native detector logs verify the change;
GH Run Receptor preserved success. Keep adoption partial until actual daily
recovery, hosted external-PR execution and separate publication-platform
claims are reviewed. Final execution evidence is recorded in the owning issue
and this central record without adding another skipped component commit.

**ElastNetMT implementation review on 2026-09-30:** `uibcdf/elastnetmt#17`
owns contributor governance and skipped-push recovery. Final guard/record
source `9f47e1f`, routing `c68f662` and collection correction `71f1179` preserve
unfiltered complete push/PR Linux/macOS Python 3.11–3.13 tests, minor-specific
Conda environments and controlled suite revisions. The tested MolSysMT source
replacement remains **limited to Python 3.13**; older minors retain their
original Conda source. The full plain pytest command and inconsistent
scientific Pytest Receptor adoption remain separately owned by
`uibcdf/elastnetmt#14`. macOS is pinned to `macos-15` with interpreter/arm64
assertions. Independent Reporting governance retains its standard-library
checks and adds administrative guards with independent pip receptor `1.0.0`.

Main previously had basic protection without required PRs or status checks.
It now explicitly requires PRs with zero mandatory approvals and nine strict
checks: Reporting governance, `policy / conformance` (including Ruff), six
supported scientific jobs and the existing specialized add-on `contract`.
Fresh collaborator evidence lists `dprada`/`LMMV` as administrators retaining
observed PR/check bypass; `isandom` keeps existing maintain access and uses PR.
No access role is changed. Weekly Monday 09:00 UTC/manual complete CI and the
unfiltered separate MolSysViewer contract stay intact. Conditional daily
recovery is staggered at 02:19 `America/Mexico_City`.

The new route regression failed before a probe input existed. Eight local
administrative tests, three required standard-library reporting tests, Ruff
over 59 files, indexes and central conformance pass. The
[weekly baseline](https://github.com/uibcdf/elastnetmt/actions/runs/36459131786)
at `9566707` failed the four actual Python 3.11/3.12 scientific jobs and passed
both Python 3.13 jobs and reporting. Native baseline Linux 3.11 logs confirm
the known trajectory LinDelINT auto-engine/CuPy error already owned by
`uibcdf/elastnetmt#14` and `uibcdf/lindelint#8`.

The [initial probe](https://github.com/uibcdf/elastnetmt/actions/runs/36775315293)
at `c68f662` passed reporting/index/CI guards and detector, recognized executed
full `a47c067` and retained five skips, omitting heavy jobs.
[Initial policy](https://github.com/uibcdf/elastnetmt/actions/runs/36775320115)
passed. The [specialized contract](https://github.com/uibcdf/elastnetmt/actions/runs/36775325575)
passed its actual add-on verification at `c68f662`. Skipped record `3d2c59b`
added one more debt: its [probe](https://github.com/uibcdf/elastnetmt/actions/runs/36775593546)
retained six skips and its
[policy](https://github.com/uibcdf/elastnetmt/actions/runs/36775602474) passed.

The [first complete manual CI](https://github.com/uibcdf/elastnetmt/actions/runs/36775597556)
at `3d2c59b` exposed a **local governance regression**: the new YAML route
guard imported PyYAML during scientific collection on older minors, whose
existing environments lack it. All four Python 3.11/3.12 jobs failed collection;
both Python 3.13 jobs and independent governance passed. GH Run Receptor
identified missing `yaml`. These four failures belong to this implementation,
not the baseline provider error; retain and correct that distinction.

Correction `71f1179` moves this administrative-only guard to
`devtools/tests/test_ci_routes.py`, explicitly selected by governance with its
existing PyYAML bootstrap. The original scientific `testpaths=["tests"]`,
full command, environments, source pins, existing test modules and assertions
are preserved. No test is skipped. The final guard also verifies administrative
isolation and keeps that path out of scientific execution. The
[corrected probe](https://github.com/uibcdf/elastnetmt/actions/runs/36776675464)
passed and retained seven skips; [corrected policy](https://github.com/uibcdf/elastnetmt/actions/runs/36776680458)
passed. The [repeated complete manual CI](https://github.com/uibcdf/elastnetmt/actions/runs/36776671299)
at `71f1179` restored collection: both Python 3.13 scientific jobs and
Reporting governance passed; the four older-minor jobs failed their actual
scientific test steps. All six interpreter/arm64 assertions succeeded. Native
logs from all four older-minor jobs confirm the pre-existing trajectory
CuPy/auto-engine failure; Linux 3.11 also shows all four debt tests passed. GH Run Receptor
preserved overall failure; no full success or scientific remediation is claimed.
Final source `9f47e1f` adds only administrative guard/record changes. Its
[probe](https://github.com/uibcdf/elastnetmt/actions/runs/36777411290)
passed actual reporting/CI guards and detector, retained eight skipped commits
since older full `a47c067` and omitted heavy jobs after failed complete coverage.
[Final policy](https://github.com/uibcdf/elastnetmt/actions/runs/36777416876)
passed. Thus neither the local collection regression nor the corrected
scientific failure discharged skipped debt. Actual daily recovery, hosted
external PRs and installed-artifact/platform claims are unreviewed. Keep #17
and registry adoption partial.

This completes the initial recorded CI review of the existing registered
Python members: none remains pending, with one adopted and thirteen partial.
This is review coverage, not completed adoption. Scientific failures, postponed
core reviews, actual scheduled/PR observations and platform/release evidence
remain visible under their owning issues. The invalid-adoption regression now
constructs unreviewed evidence independently of live pending entries, so it
continues protecting the contract after the final initial review advances.

GitHub documents that scheduled runs occur on the default branch and may be
delayed or dropped at busy times, especially at the start of an hour. GitHub
also documents that `continue-on-error` can let a workflow succeed while an
individual matrix job fails. `uibcdf/gh-run-receptor#51` remains open because
its compact LLM report can omit that tolerated failure from a `PASS` summary.
These facts support initial dispatch verification and a separate failing
feasibility workflow for transition evidence.

**Remaining assumptions:** weekly full Linux matrices can be added to members
that currently lack them without an unsolved dependency stack, and the
development-minor gate is affordable in every repository. Hosted duration and
dependency resolution must be measured before changing a member workflow.

## Alternatives and refuted paths

- Run every supported Linux minor on every push/PR: faster attribution of a
  version-specific regression, but multiplies routine CI jobs, especially in
  scientific repositories. The suite maintainer chose the 3.13-plus-weekly
  default instead. The residual detection delay is explicit and is mitigated
  by initial dispatch and exact-candidate full-matrix checks before releases.
- Require Linux/macOS/Windows for every pure-Python or `noarch` package:
  rejected as a default inference. Packaging architecture does not prove OS
  behavior or dependency availability; Ackredit's POSIX journal is a concrete
  counterexample to treating platforms as interchangeable.
- Count any version literal in any workflow as coverage: rejected because the
  existing checker cannot prove that tests run on that version.
- Put experimental minors in a `continue-on-error` cell of required CI:
  rejected as the canonical evidence path after `uibcdf/ackredit#64`.
- Require the same cron minute across the suite: rejected because a shared
  schedule time adds no contract value and GitHub warns of top-of-hour load.

## Scope and exclusions

This policy applies to registered `python-package` members. It defines CI
evidence, not package publication, Conda promotion, Python admission, or a
guarantee that a green workflow proves scientific correctness. Specialized
GPU, GUI, ABI and installed-artifact gates remain component-owned unless a
separate common rule accepts them.

## Acceptance criteria

- A normative CI-lane contract states trigger, supported-minor, test-level,
  platform, experimental-minor and exception semantics.
- `suite.toml` identifies the common minimum and any justified member-specific
  CI mode/platform claim without modifying member classification fields.
- An offline checker distinguishes required lanes from workflow text that
  merely mentions the expected versions, with focused regression tests.
- Starter-kit workflows and participating members follow the contract or
  carry a tracked exception with an expiry condition.
- A newly introduced scheduled lane is dispatched and inspected before it is
  treated as evidence; hosted policy and member CI runs confirm the rollout.

The accepted normative target is `devguide/python_ci_policy.md`, with its
minimum recorded in `suite.toml`. The future enforcement guard belongs in
the versioned `check_repository.py` policy gate; the registry and starter-kit
shape are guarded locally by `tests/test_python_ci_policy.py`.

## Local implementation issues

`uibcdf/ackredit#63`, `uibcdf/ackredit#64` and `uibcdf/ackredit#71`
supply resolved consumer evidence.
`uibcdf/gh-run-receptor#52` owns the first concrete routine/weekly CI migration.
Open further member issues only when a concrete workflow migration is assigned;
the central issue owns the common decision.

## Dependencies and risks

The agreed baseline and a truthful workflow parser are prerequisites to
enforcement. A checker that treats YAML as an unstructured string, ignores
`if`/filters, or counts tolerated failures as evidence would make the new rule
look stronger than it is. Additional runner minutes and native dependency
availability must be measured per cohort before a required policy release.
Weekly-only coverage of older minors deliberately accepts up to a week's
detection delay between full runs.

## Provenance

Inspected local registered checkouts and the central checker on 2026-09-23
under the Python 3.13 development environment on Linux. Issue evidence comes
from `uibcdf/ackredit#63`, `uibcdf/ackredit#64`, `uibcdf/ackredit#71`
and `uibcdf/gh-run-receptor#51`.
GitHub Actions schedule and matrix semantics were checked against GitHub's
official workflow and event documentation on the same date.
The 3.13 push/PR plus weekly-full default was chosen by the suite maintainer
on 2026-09-23 after comparison with all-minor push/PR coverage.

## Published routine baseline — 2026-10-03

The maintainer explicitly authorized publication and adoption of policy-v1.5.4.
Its immutable source is e459ea0e8ac6aa8017e17a2f171c50d122b9e0b7. All sixteen
registered guide consumers received the byte-identical canonical summary, and
all fifteen Python callers now select this published release. Native guide
audit 37123018170 and manifest audit 37123019881 pass across the full registry.
The latter also confirms the observed Viewer development extra relationship
for Pytest Receptor after the dependency inventory was corrected.

[Machine receipts](../rollouts/policy154_routine_adoption.json) retain exact
commits, run/job outcomes, scopes, protection-name updates and limits. Fourteen
member policy gates pass; MolSysMT fails RELEASE_TAG for an archival experiment
marker. That independent namespace decision is uibcdf/molsyssuite#84, not a
Python or scientific defect. No tag was moved or deleted, and 1.5.4 is immutable.

SMonitor, ArgDigest, DepDigest, PyUnitWizard and GH Run Receptor pass their full
Linux routine suites on 3.14. Ackredit passes its retained four-minor Linux
matrix, macOS ARM 3.14, Ruff and documentation build. Pytest Receptor passes
its Linux Python/pytest matrix, routine auxiliary jobs, coverage publication and
manual ten-cell weekly matrix including macOS ARM 3.14. OpenCASTp passes its
manual four-minor installed/full matrix; its push-only routine interpreter is
configured as 3.14, not claimed executed by that manual dispatch. Its normal
published caller passes and its admission-bootstrap exception is retired.

LinDelINT, ElastNetMT, PharmacophoreMT and TopoMT pass independent administrative
governance/debt probes on 3.14, with scientific jobs intentionally omitted.
ElastNetMT, PharmacophoreMT and TopoMT required an updated administrative
Pytest Receptor pin because 1.0.0 rejects Python 3.14; the actual failed
results remain history. Existing scientific matrices retain every minor.

MolSysMT and MolSysViewer receive the caller and guide without launching their
deferred scientific suites. Their older rich development/scientific routine
routes remain explicit temporary migrations under uibcdf/molsysmt#237 and
uibcdf/molsysviewer#93, owned by their teams and reviewed by 2026-12-31. Exit
requires current-closure review, configured 3.14 routine/full lanes and passing
exact-source tests. Viewer metadata-only auditing already passes on 3.14.

Required PR check names were updated where the routine/governance interpreter
changed; strict checks, unrelated check identities, application bindings and
administrator direct pushes are preserved. Recovery still uses the complete
supported matrix as its watermark: a passing routine job or probe does not
discharge skipped debt by itself. Source/package/platform certification, real
PR and scheduled observations, and later CI-pattern enforcement remain the
tracked rollout scope; no global completed-adoption claim is made.


## Central reconciliation of owner evidence — 2026-10-04

DepDigest and Ackredit now have adopted CI-routing reviews in `suite.toml`.
The earlier partial reviews above remain dated history. Independent review
used GH Run Receptor first, native run/job/step identities and bounded detector
/architecture facts, current classic branch protection and unchanged current
CI/detector source. The safe receipt is
`devguide/rollouts/ci_reconciliation_39_20261004.json`. No new component suite,
package operation or branch-protection mutation was performed.

DepDigest's actual scheduled twelve-cell recovery found one pending skip; its
real Markdown-only PR executed Linux/Python 3.14 despite skip-like title/branch.
Twelve installed resource/CLI smoke cells support reviewed Linux/macOS arm64/
Windows claims. Historical macOS source output is 135 passed, one optional
sibling-integration skip; this is not proof of that collective boundary.

Ackredit's actual recovery and PR retain their then-supported three-minor
scope. Current four-minor source matrix passes eight Linux/macOS arm64 cells;
its qualification branch is not a main watermark. Current seven protected
checks include 3.14 and keep the internal administrator route. The unchanged
current routing and bounded backlog guards reject incomplete, three-minor,
probe, PR, feature-branch and failed watermarks; source inspection together
with observed historical execution establishes route adoption. No current
four-minor scheduled-recovery or PR run is manufactured or claimed. The
scheduled zero-debt job omits tests intentionally, and is not a watermark.
Native macOS full/push test output includes seven skips, so the owner's
separate zero-skip local result is not represented as hosted evidence.
The original 0.9.0 installed eight-cell qualification and same-byte promotion
remain separately recorded under #88/#89 and the component #22/#80.

`adopted` here describes the CI contract and reviewed platforms; it does not
certify every later source commit, optional integration, release or public
closure. Three members are now adopted; twelve remain partial. The central
CI-pattern enforcement target and suite rollout remain open in #39.
MolSysMT/MolSysViewer scientific deferrals are unchanged.

## Further independent reconciliation — 2026-10-04

ArgDigest's provider review uibcdf/argdigest#21 is closed with new observations.
Central review independently inspects published GH Run Receptor metadata for:

- actual PR run [37201939802](https://github.com/uibcdf/argdigest/actions/runs/37201939802),
  on the skip-like `fix/skip-ci-pyunitwizard-import` branch;
- documentation-only PR checkpoint
  [37202605038](https://github.com/uibcdf/argdigest/actions/runs/37202605038);
- actual scheduled recovery
  [37203404180](https://github.com/uibcdf/argdigest/actions/runs/37203404180)
  at `91543cfc638ef81d6daf1028296c4561af3554cb`.

Both PRs execute the required Linux/Python 3.14 `Run tests` step. The scheduled
run executes all twelve supported Linux/macOS/Windows × Python 3.11–3.14
test steps. These are passing executed jobs, not a probe's empty matrix.
Current routine/full workflow, backlog detector and backlog tests are
byte-identical to the scheduled main source. Current classic protection keeps
the strict named Python 3.14 PR check, bound to its existing application, and
does not enforce it on administrators' authorized direct pushes. This review
performs no new dispatch, tests, package operation or protection mutation.

The historical PR-observation gap is resolved. ArgDigest remains partial in
the central registry pending its distinct public/installed platform-claim
review; no new public artifact or later skip-debt clearance follows from these
source runs. Three reviews remain adopted and twelve partial. Exact source
hashes, safe protection fields and job/step identities are in
`devguide/rollouts/argdigest_ci_review_39_20261004.json`.

The refreshed existing static inventory covers all fifteen Python members and
913 event/job/matrix observations. Eleven members have an observed gating
direct pytest PR cell on Linux/Python 3.14 without unresolved/excluding
conditions in that event. This is configured evidence, not a full-suite or
complete-policy verdict. Reusable workflows, wrappers, dependency acquisition,
test-level semantics, required-check binding and actual hosted execution still
need their receiving profiles/evidence. The receipt retains the command,
inventory digest, member set and this limit.

## Prepared next enforcement decision — not adopted

The existing common minimum is accepted; the unresolved choice is how to
introduce its automated checker without treating an unrecognized valid
component workflow as a missing test or a scientific failure as governance
adoption evidence. Keep the owning reusable workflow parser/inventory and
registry review modules as the implementation surface.

| Delivery option | Concrete scope | Consequence |
| --- | --- | --- |
| Informational pilot first (recommended) | Resolve workflow profiles for the three reviewed components (GH Run Receptor, DepDigest, Ackredit), with adversarial fixtures and explicit `unknown` findings; emit a report. | Measures false positives and owner-specific full/smoke semantics before any new mandatory caller release. |
| Blocking gate for reviewed components | Publish a new immutable policy after qualifying those profiles; enforce only its explicitly registered adopters with the existing exception mechanism. | Introduces a new required check in those repositories and needs owner rollout/verification immediately. |

Both options preserve the existing direct-maintainer route, full PR requirement,
conditional recovery/weekly/manual semantics, independent publication gates
and component-owned special conditions. MolSysMT/MolSysViewer scientific
deferrals and early scientific-component debt remain visible. No uniform YAML,
new per-push scientific suite or opaque-wrapper rejection is adopted here.

The pilot's profiles must bind configured event, workflow/job, interpreter,
test selection and gating/condition semantics to reviewed source and hosted
evidence. Adversarial coverage must reject comment-only versions, matrix
exclusions, tolerated failures, skipped/filtered PR routes and probe/routine
watermarks while retaining valid smoke exceptions and reusable/wrapped routes
as reviewed or explicitly unresolved. A later compulsory rollout needs its
own immutable policy source, impact notice and exact caller evidence.

The maintainer is consulted on this delivery choice before implementation.

## Accepted informational pilot — 2026-10-04

The maintainer chooses the informational pilot first. The two options above
retain the decision history; no blocking gate was adopted.

`python_ci_status.py --pilot WORKSPACE` and its reusable `inspect_pilot`
operation now read three source-bound workflow profiles in
`devtools/ci_pilot_profiles.toml`, using the existing CI inventory parser.
The command reader gains bounded coverage-module pytest recognition for GH
Run Receptor's actual full-suite producer; arbitrary wrappers remain unknown.
Hash drift invalidates reviewed selection. Normal review/status behavior and
required CI/caller versions remain unchanged; no pilot workflow is added.

The first report is `devguide/rollouts/ci_pilot_39_20261004.json`. All three
profiles match their inputs: GH Run Receptor has eleven configured target
cells, DepDigest two configured/nine conditional and Ackredit three configured/
eight conditional. The conditions remain visible because schedule/probe/backlog
contexts are not yet automatically resolved. No job run, passing watermark,
whole-policy adoption or publication qualification follows from these counts.

The tool contract, profile maintenance and remaining inference limits are in
`devguide/ci_pilot.md`. Thirty-one focused pilot/inventory/CI-policy tests pass,
including adversarial coverage for excluded minors, version comments, tolerated
and skipped tests, filters, opaque/dynamic routes and changed selection inputs.
`tests/test_ci_pilot.py` protects the informational boundary and smoke/full
separation. The receipt states the compatible administrative Conda/Python 3.14
environment and its bounded exception; no scientific suite or member mutation
was performed.

Remaining #39 scope: owner-reviewed scheduled/input/reusable semantics,
independent evidence for outstanding member reviews and an explicit later
decision/versioned rollout before mandatory enforcement.

## Informational routing follow-up — 2026-10-04

The pilot's published source `474d5ae5bea16cadbfc6f79723eada0712925b21`
passes hosted governance `37214106604`, including all 318 central tests and
coverage publication. Delivery to the three owner reviews is complete; no
receiving reply had arrived when this follow-up began. No owner approval or
new execution is inferred from notice delivery.

The owning CI inventory module now provides `condition_outcome` and
`inspect_event_routes`. They add configured cron/manual-default/boolean-input
predicate scenarios to the informational report, preserving aggregate lane
states and ordinary inventory behavior. DepDigest and Ackredit distinguish
weekly full selection, manual full selection and manual debt probes. Daily
recovery remains unknown without detector result/output facts. Known true
predicates are never successful jobs, implicit dependency success or cleared
debt. Source input drift invalidates each scenario's selection review.

The latest Ackredit source advanced two commits to `d3fd892` during inspection;
its CI profile inputs remain byte-identical. That establishes only unchanged
configured selection/routing, not passing current runtime code or new tests.
Concurrent central Windows qualification corrections were fast-forwarded and
preserved before this work. Original component clones were not modified.

`tests/test_ci_event_routes.py` protects absent detector facts, fail-safe
detector failure, successful zero-debt suppression, typed probe defaults,
missing inputs, literal/reference separation, unsupported expressions and the
separation between predicates and execution. Together with the relevant
existing pilot/inventory/CI-policy tests, 39 focused tests pass on the verified
administrative Python 3.14 interpreter. The existing bounded environment scope
is retained; no scientific suite or component CI dispatch was performed.

Receipt: `devguide/rollouts/ci_pilot_routes_39_20261004.json`; contract and limits:
`devguide/ci_pilot.md`. Owner receiving feedback, external execution/dependency
facts, outstanding broader reviews and any mandatory rollout remain pending.

## ArgDigest platform reconciliation and pilot refresh — 2026-10-04

The remaining ArgDigest platform observation gap is resolved by its existing
public 0.14.0 delivery, independently reconciled under #98. Original producer
`0fa776af2d271065c60727c28480b20c3ce09aee` and file SHA-256
`983dca0f6bd0944d81fb1efc01e1dfa5c951e95abac6e7a0a08a13b7370d3b9e`
remain bound to
[installed run 37213239915](https://github.com/uibcdf/argdigest/actions/runs/37213239915)
and its separate administrative qualification
`be39e899f3b9fef2d4ce705799ae19770f41f769`.
Published GH Run Receptor 1.2.0/native metadata confirm thirteen successful
jobs, including all twelve Linux/macOS arm64/Windows × Python 3.11–3.14
cells. Each executes exact installation, installed-resource validation, the
selected complete test directory outside source and final provenance checks.

The native macOS/Python 3.14 log identifies `macos-15-arm64` and Conda
`osx-arm64`; it reports 302 passed, one skip because sibling repositories are
unavailable. This supports the reviewed installed platform claim while
leaving that optional collective integration unqualified. No zero-skip result
or future package qualification is inferred.

Current main source `42b2f93346fdcd1573ade66a3f82a1717a496184` retains the
previously reviewed routing/detector/guard hashes and the producer's runtime,
test and Python metadata inputs. Current strict Python 3.14 PR protection,
its existing Actions application binding and administrator direct pushes were
rechecked without mutation. Combined with the earlier real PR and actual
scheduled recovery evidence, this completes ArgDigest's CI contract review.
Its `suite.toml` entry is now **adopted**, with Linux/macOS/Windows claims and
the common macOS-arm64 limit. Four members are adopted; eleven remain partial.
Later skipped debt, optional integrations and #98 consumer adoption remain
separate; the installed qualification branch is not a main recovery watermark.

The existing informational pilot was rerun against fresh immutable main sources
for its three authorized members. All reviewed profile inputs still match:
GH Run Receptor `f1a5901`, DepDigest `0568f9a`, Ackredit `de209ca`.
Ackredit's newer reporting work does not change these routine/full-selection
inputs; this match makes no runtime/receiving claim about its new features.
The owner issues retain central delivery notices, with no new receiving reply
observed at this checkpoint. Conditional/unknown daily detector facts remain
visible. No profile cohort, mandatory checker, workflow, dependency or policy
version changes.

Primary receipt:
`devguide/rollouts/ci_reconciliation_39_argdigest_platforms_20261004.json`.
The earlier dated partial reviews remain history. #39 stays open for owner
feedback, remaining member reviews and a separately accepted versioned rollout
before CI-pattern enforcement.


## Informational pilot refresh — 2026-10-05

Read-only inspection of fetched immutable main sources confirms all three
existing profile input sets still match: GH Run Receptor
`f1a5901ae9543d4d79dd184e694c05b7eb2a901f`, DepDigest
`0568f9aba397ed5495adb350ba0f90899d6bdb8b`, Ackredit
`6f8f361fc11143d7507ba9ff6c7aee75a7a4ac6e`. The owning pilot issues still
have no new receiving response. No enforcement or cohort expansion is adopted.

Original local clones are not the same evidence source: the DepDigest clone is
76 commits behind and produces an invalidated input review. The current fetched
source matches the profile. This is a source-selection distinction, without
updating that clone or clearing runtime/dependency/test debt. Ackredit's newer
provider evidence work remains independent of unchanged CI profile inputs.

## Fresh informational pilot reconciliation — 2026-10-07

Read only immutable origin/main snapshots from the existing registered clones;
primary worktrees remain untouched. DepDigest df72daec and GH Run Receptor
ec42d211 retain identical reviewed inputs. Ackredit 1342f0f2 changes only
CI.yaml: three pinned dependency-parser/preflight steps are added to the quality
job. After removing exactly those three additions, the complete YAML structure
matches the previously reviewed document, including science/events/matrix and
recovery. Metadata, full matrix, backlog detector and environment hashes match.
The one reviewed CI input hash and immutable source identities are reconciled;
no automatic acceptance of unrelated input drift or new pilot member occurs.

Before reconciliation, Ackredit's stale hash makes its eleven lanes unknown.
After explicit review, all three profiles match their committed inputs: GH Run
Receptor eleven configured; DepDigest two configured/nine conditional; Ackredit
three configured/eight conditional. Conditional branches/detector facts remain
conditional. These are source observations, not executed-test/compliance/debt
verdicts. Existing adoption states and scientific deferrals are unchanged.

Managed snapshot fixtures are removed after receipt acquisition. No component
workflow, gate, Python claim, dependency, protection, release or science dispatch
is changed. Receipt: devguide/rollouts/ci_pilot_reconciliation_39_20261007.json.
Owning feedback and an explicit later mandatory-rollout decision remain separate.

Current three owner issues (#52/#21/#74) are closed for their original CI
adoption scope. Recent comments retain prior pilot notices and separate
publication/source reviews; they do not authorize mandatory enforcement or
clear other members. No interpretation feedback is silently inferred from
closed status. Exact receiving comments are registered in the receipt.


## Reviewed Viewer transition caller registration — 2026-10-08

The principal maintainer authorized correction of the central caller discrepancy
exposed during #97. At current committed Viewer source
`0abad175bf97c77908c09a008e27055fec8eac80`, the latest central checker reproduces
`[RUFF_CI] active workflow commands missing: ruff format --check`. The unchanged
caller is `policy-v1.5.7`; the component's explicit transition list only registers
`policy-v1.5.4`. Recognizing an executed historical quality gate remains distinct
from admitting Python support or certifying a complete scientific suite.

The frozen policy is `f1ae1a043720e33493024d8afcab1e45375e42a2`. Immutable
workflow/source review confirms Python 3.14, Ruff 0.16.5 and mandatory lint/import
and formatting operations; the changes from reviewed 1.5.4 add optional immutable
admission handling and its exclusions, retaining the quality gates. Current
[Viewer policy 37787547140](https://github.com/uibcdf/molsysviewer/actions/runs/37787547140)
independently verifies exact source/workflow/event/attempt, both jobs and required
executed conformance/lint/format/dependency-metadata steps. No component science
or browser run is dispatched by this correction.

Register reviewed 1.5.7 in the existing transition-compatible catalogue and the
Viewer-specific allowed list, retaining its 1.5.4 route. This repairs data in the
owning registry rather than changing the checker algorithm or accepting every
ordinary historical pin. Other explicit component restrictions remain unchanged;
the six members inheriting the catalogue may recognize the reviewed capability
if deliberately selected. An inventory of all sixteen committed actual callers
shows **only Viewer changes from stale to compatible**; the other fifteen retain
their current state. Their configured pins and component worktrees are unchanged.

A new actual-registry regression fails before the correction; the component
isolation control already passes. After correction, 58 focused conformance,
adoption and transition tests pass, including rejection of moving/unreviewed
Viewer pins and 1.5.7 for other explicitly restricted components. The actual Viewer
source passes the latest central checker, with the prior failure retained in the
receipt. Ruff lint/format and the offline governance guard pass. Durable guard:
`tests/test_governance.py::RepositoryConformanceTests::test_viewer_reviewed_transition_caller_supplies_ruff_without_local_commands`.

Advance notices are delivered to this issue and uibcdf/molsysviewer#93 before
publication. Evidence and complete current-caller comparison:
[transition_caller_registration_39_20261008.json](../rollouts/transition_caller_registration_39_20261008.json).
Current policy registration, unchanged frozen policy rules, source qualification,
public artifacts and scientific debt remain separate. No policy release/tag,
component caller/dependency, admission, badge or source requirement changes.
#39 remains active for its CI-routing/pilot/enforcement rollout; this registration
correction does not close the broader proposal or Viewer #93.


## Actual PR/recovery evidence and portable preflight — 2026-10-09

Fresh immutable main input review reruns the existing informational pilot for
GH Run Receptor `4a89d19`, DepDigest `f7c8625` and Ackredit `593440b`.
All profile inputs still match: respectively 11 configured; 2 configured/9
conditional; 3 configured/8 conditional. No new owner interpretation response
is found. Profiles, cohort, test-level interpretation, required gates and
mandatory-enforcement decisions are unchanged. Source scenarios do not qualify
execution or clear skipped-commit debt.

The prior Pytest Receptor PR/schedule observation gaps are now resolved by
independent verification of existing original executions, without dispatch:

- PR Tests 37126514411, source `7851421c7e5385e030f900d100a9766f88045e82`,
  verifies eleven mandatory jobs: Linux Python 3.11–3.14/pytest8–9 serial and
  distributed suites, lint, benchmarks and packaging. Its default-branch coverage
  job is inapplicable/skipped and is not counted as executed evidence.
- Scheduled recovery 37943286303 at current source
  `5fe7d98f4a4a6f7f2bca1f250427ad48178c73a2` verifies the executed detector
  and all ten serial/distributed cells: eight supported Linux pairs and two
  macOS arm64 routine-Python3.14 representatives. This matches the current
  weekly routine-minor non-Linux contract; it is not an all-minor macOS
  scheduled claim or a calculation of later skip debt.
- Fresh native protection retains eleven strict checks, explicit PR requirements,
  disabled force pushes/deletion and administrator direct-push bypass. The
  PR-to-current YAML delta adds only three pinned lint preflight operations and
  `needs: lint` on test/benchmark/packaging; removing exactly those additions
  makes complete YAML equal. Current CI/full-matrix/detector inputs are identical
  to independently qualified distribution source `9220984`, Tests 37472499238.
- Original public 1.2.1 Conda producer/file/digest and eight Linux/macOS arm64
  installed cells under #93/#45 retain their independently reviewed scope.
  No new installed qualification or Windows claim is introduced.

This completes the existing uibcdf/pytest-receptor#11 CI review for Linux/macOS
arm64. Registry totals become **five adopted / ten partial**. Owner source,
pins, protection and workflows are not edited; routing adoption does not
certify a changed release, arbitrary later code or collective consumer science.

SMonitor also has existing actual PR evidence: CI 37154925144 and QA 37154925156
at `e5355b78ce2e349e8376fe458b73a78a0116ddac` independently execute all three
current protected checks, complete/default/strict suites, collective path and
wheel/CLI smoke. Fresh strict protection/admin bypass is unchanged. Its latest
scheduled run 37935661439 passes four Linux and four macOS test cells but fails
all four Windows preflights before tests. It stays **partial**; this failed run
cannot become a full watermark. Original public 0.19.0 artifact qualification
remains separate.

Shared source discovery incorrectly compares native Windows backslashes with
portable slash-separated route identities. Reproduced audit guard and additive
correction belong to **uibcdf/molsyssuite#112**; actual SDK adoption and native
Windows preflight evidence belong to **uibcdf/smonitor#46**. The new regression
fails before and passes after, retaining refusal of an extra environment and
changed workflow digest; 46 focused dependency checks pass. Twelve registered
client/candidate notices precede provider publication, without mandatory migration
or scientific dispatch. Provider availability is not consumer recovery.

Receipt: [ci_receiving_and_portable_routes_39_112_20261009.json](../rollouts/ci_receiving_and_portable_routes_39_112_20261009.json).
Original dated records remain. MolSysMT/Viewer and early scientific work stay
with their teams; workspace #82 and private OpenCASTp #102 remain unchanged.
#39 stays active for ten remaining reviews, receiving interpretations and a
separate later enforcement decision. No PR creation or new suite dispatch.


Initial hosted checkpoint — Source `738e6f3` native 37991689637 runs 447
central tests; only the existing live-registry test fails because it still
expects Pytest Receptor `partial`. Windows discovery regression and all other
tests pass. Coverage upload is skipped; that commit is not delivered as an
accepted SDK. Correct the assertion for the evidence-backed adopted review and
explicit Linux/macOS claim, retaining all other member expectations. Final
exact-head native governance is verified before accepted-provider handoff.


## Native Windows preflight receiving — 2026-10-09

Deliberate SMonitor adoption under uibcdf/smonitor#46 uses accepted shared SDK
`6d6172d` for all eight paired preflight checkouts. Only those refs and seven
reviewed workflow hashes change; @2 inventory, declared/installed constraints,
source/test selections, matrices, recovery and publication gates remain.
Independent resource/publication/installed-verifier pins keep their reviewed SDK.

First receiving source `b16b032` clears portable discovery, but native full matrix
37994715796 fails all four Windows exact workflow hashes before tests: Git
`core.autocrlf=true` converts LF blobs to CRLF. Source `57bcf31` fixes the owning
checkout contract with `.github/workflows/* text eol=lf`, retaining the actual
shared hash checks. An actual Git regression fails before and passes after;
a paired-SDK/hash guard covers all callers. Local adoption has 149 passing
contract checks plus an existing report skip; thirteen focused distribution
checks and archival reporting controls pass.

Independent native verification of full matrix 37995139887 binds source
`57bcf31cc0508fba7f877a5eecc4ec8dd5d725bd`, normal manual event, workflow,
attempt and all twelve Linux/macOS arm64/Windows Python3.11–3.14 executed
preflight/install/import/lint/test cells. The detector is inapplicable/skipped
for that normal manual event; it is not counted as an executed test gate.
Routine CI 37995139308, both QA jobs 37995139461 and policy 37995140043
independently pass exact-source required steps. Current strict three-check
PR protection and administrator direct pushes stay unchanged; the earlier
actual PR observations remain and the reviewed full selections/conditions are
preserved. Representative routine-minor cells have 656 passed/five ordinary
skips; macOS runner evidence identifies arm64.

This completes the SMonitor routing review for all three claimed platforms:
**six adopted / nine partial**. Its later record-only archival head retains
identical executable/CI/metadata/dependency inputs and gets its own applicable
policy/QA checks. That reuse does not qualify a changed release candidate or
assert a full matrix ran on the archival head. Original failed schedule
37935661439 and first receiving failure 37994715796 stay failed; neither
clears debt. Public 0.19.0 source/file/digest and original installed matrix
remain untouched.

GH Run Receptor's installed editable source `f1a5901` omitted the explicit
preflight rejection before generic exit 1. Native fallback recovered the
diagnostic; incoming provider feedback is uibcdf/gh-run-receptor#64.
No provider-code fix or latest-remote behavior is assumed from that report.

Receipt: [smonitor_portable_preflight_receiving_39_46_20261009.json](../rollouts/smonitor_portable_preflight_receiving_39_46_20261009.json).
The existing informational pilot, cohort and separate enforcement decision stay
unchanged. #39 remains active for nine reviews and receiving interpretations;
MolSysMT/Viewer and early scientific work stay with their teams.

Final archival head `8484983` independently verifies its applicable policy
37995542858 and QA 37995542241. Probe-only 37995542767 executes the detector,
recognizes the actual full source `57bcf31` as its watermark and observes zero
skipped commits at that head. Its full-test job is intentionally skipped; this
probe adds no full-suite or exact-candidate evidence and says nothing about
later skipped commits. The two prior failed matrices never become watermarks.

## LinDelINT actual daily receiving — 2026-10-09

Independent original-run acquisition resolves the daily observation gap in
`uibcdf/lindelint#12`. Actual schedule 37945882859 at
`a2443ca9f87a0b744451301a4103a7a210b50959` verifies all ten executed required
jobs: backlog detection, reporting/distribution controls and eight complete
Linux/macOS arm64 Python 3.11–3.14 source cells. The detector found two
documentary skipped commits after full source `1a65d75` and requested the full
matrix; every installation, dependency, wheel, import, interpreter/architecture,
test and Ruff gate passes. Both 3.14 representative logs report 13 passed.

Actual historical PR 36347750244 at
`8cc2fa960db27395ce2d40ed88285a72140c4e93` verifies six then-configured
Linux/macOS Python 3.11–3.13 jobs. Actor `LMMV` is an administrator; this
does not observe an external contribution, a current eight-cell PR or the old
macOS architecture. Current PR routing remains unfiltered and its six common
suite operations are identical; the later 3.14/arm64/preflight additions have
the separately executed daily evidence above. Fresh protection retains nine
strict full/reporting checks, explicit zero-approval PR requirements and
administrator direct pushes by `dprada` and `LMMV`.

The current workflow/detector/test/metadata inputs match qualified source
`c4418a7`; later changes contain only synchronized guides and records. Owner
checkpoint `8c23a218102c83daa13a30f2740525273af05f74` changes one pending
record, passes three local reporting tests/index checks and receives exact-head
manual policy verification 37997418930. It does not execute or clear its
documentary skip through administrative checks; unchanged daily/weekly/manual
full recovery remains owned in #12.

The review stays **partial** for current complete PR observation and independent
public distribution/platform qualification under `uibcdf/lindelint#14`.
Historical public 0.2.0 availability and future noarch targets do not admit a
new delivered 3.14 artifact. No workflow, pin, protection, support badge,
scientific implementation, release or artifact operation changes. Totals remain
**six adopted / nine partial**, with the pilot and later enforcement decision
unchanged. Receipt:
[lindelint_ci_receiving_39_20261009.json](../rollouts/lindelint_ci_receiving_39_20261009.json).

## PharmacophoreMT source and daily receiving — 2026-10-09

At current source `95487103a4ad5e97971c93ae97bc85484872705c`, original push
CI 37977232408 independently verifies Reporting governance and all eight
Linux/macOS arm64 Python 3.11–3.14 source cells. Actual dependency/Git-context
preflight, installation, import, interpreter/architecture and full tests pass;
both routine-minor representatives report 626 passed. Its daily/probe-only
detector is inapplicable/skipped and does not count as executed recovery.
Exact-source policy 37977233095 and Conda controls 37977233061 also pass:
eleven executed required source/administrative jobs, without a new dispatch.

Actual daily schedule 37950055123 at `2132fa0` verifies the detector and
Reporting governance; its log observes zero skipped commits since full source
`2132fa0` and intentionally omits the matrix. This resolves the actual daily
observation gap, not a new full run or a claim about later debt.

PR 37578072679 at `7326f47` stays **cancelled** overall. Selected-job native
verification observes eight then-configured full source cells and reporting
success; that PR predates current dependency controls. Those job observations
cannot turn its cancelled workflow into an accepted complete PR or watermark.
An accepted current PR and installed/public platform claims remain pending
under `uibcdf/pharmacophoremt#9` / #10 / #23.

Fresh protection retains ten strict checks (eight source, reporting, policy),
explicit zero-approval PRs and administrator direct pushes for dprada/LMMV.
Since helper adoption `448e47e`, the sole full workflow delta adds independent
evidence-archive reporting tests; the corresponding registered hash is reviewed.
No matrix, trigger, scientific selection, SDK or recovery change is introduced.
The owner removes delivered #108 from its distribution record's active blockers,
retaining source-free environment/public delivery gaps and historical provenance.

Both reviews stay partial; CI totals remain **six adopted / nine partial**.
The informational pilot and later enforcement decision are unchanged. Receipt:
[pharmacophoremt_ci_receiving_39_45_20261009.json](../rollouts/pharmacophoremt_ci_receiving_39_45_20261009.json).


## PyUnitWizard independent CI acceptance — 2026-10-09

The owner closed `uibcdf/pyunitwizard#91` on 2026-10-04. Central receiving
now accepts its CI contract as **adopted**, with reviewed Linux and macOS
arm64 claims. Windows and macOS Intel remain outside those claims.

Actual documentation-only PR #97 passed the required Linux 3.14 full suite
in 37230026063: 676 passed / 22 documented skips. Its skip-like branch/title
did not bypass the unfiltered PR lane. The API requested source is
`6120b8f9f5e3bc4de91b9b4402a96f68a2350649`; native checkout tested synthetic
integration `1b638227e183d186251318201950bb6eca8fd6e3`. This observes PR
integration and does not substitute for exact-candidate release qualification.

Actual daily 37011806773 detected six skips and executed all eight supported
Linux/macOS minor cells. Probe 37230605443 later recognized the successful
`71de829` full watermark with zero debt and intentionally omitted tests.
Current actual daily 37939979875 at `a2bed779` detects one skip and passes
all eight Linux/macOS 3.11–3.14 cells, including current dependency preflight.
Both 3.14 representatives report 791 passed / 19 skips; macOS identifies
`osx-arm64`. Scheduled execution delays are observable, not a delivery guarantee.
Historical failed full 36538496360 and its retained debt remain failed evidence;
scientific repairs belong to owner #95/#96. A probe never clears full-suite debt.

Routine full 37692655957 at `08b3107` passes 791 / 19. All executable, test,
workflow, metadata and environment inputs match current `a2bed779`; only three
synchronized guides differ. Exact-current policy 37795024942 passes. Reviewed
PR/recovery triggers, matrix, conditions and suite/import/install/style/detector
commands are unchanged since the original routing qualification; later SDK
preflight has executed current evidence. Fresh protection requires strict Linux
3.14 PR tests, while administrator direct pushes by dprada/LMMV remain available.
The owner recovery guard is `tests/test_ci_backlog.py`.

Original public 0.28.1 bytes retain source `25a4bc2`, producer 37307676226 and
SHA-256 `d4654faf93ed4181bf331f7d382379e78f02784f71f678ad19d0ac43d8062cc6`.
Independent receiving rechecks installed 37308199459: the original source/file
binding and all 30 native profile cells. Baseline/storage/prepared cover
Linux/macOS 3.11–3.14; OpenFF retains its reasoned 3.12–3.14 scope. The prior
public snapshot and owner-reported clean public installation are reused with
their original limits; no new central public installation or release occurs.
This does not certify future OpenFF changes or new artifacts.

No component file, workflow, pin, protection, badge, scientific selection or
release operation changes. The central regression assertion now expects this
reviewed state and its two platform claims. Totals become **seven adopted /
eight partial**. The informational pilot and later enforcement decision remain
unchanged; central #39 stays open for its other member reviews. Receipt:
[pyunitwizard_ci_receiving_39_20261009.json](../rollouts/pyunitwizard_ci_receiving_39_20261009.json).
