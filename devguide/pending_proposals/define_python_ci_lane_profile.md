---
summary: Define observable CI lane coverage for Python package members.
issue: uibcdf/molsyssuite#39
status: active
opened: 2026-09-22
closed:
verification: inspected
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
direct pushes on 2026-09-28. The accepted
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

- On direct pushes, run a Linux test lane on Python 3.13, the routine
  development minor. Components with a demonstrably expensive scientific
  suite may use a bounded smoke suite, clearly labelled as such. Every PR
  runs the complete test suite on Linux 3.13; members may run a wider PR
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
