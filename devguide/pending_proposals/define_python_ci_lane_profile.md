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
default and a weekly full supported-minor matrix on 2026-09-23. The accepted
normative target, registry minimum, starter-kit workflow and read-only workflow
inventory exist. Member-specific claims, enforcement and rollout remain pending.

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

- On push and pull request, run a gating Linux test lane on Python 3.13, the
  routine development minor. Conventional libraries run their required suite;
  components with a demonstrably expensive scientific suite may use a bounded
  smoke suite, clearly labelled as such. Members may run additional supported
  minors on each push, but that is not the suite-wide default.
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

The first migration targets are gh-run-receptor's missing routine and scheduled
lanes, then Pytest Receptor and DockingMT's missing scheduled lane. The
early-stage ElastNetMT and PharmacophoreMT range mismatches should be handled
as component-owned migration work rather than treated as evidence that the
common policy is already satisfied. A central offline gate must not turn this
static survey into a compliance verdict before it can resolve conditions,
test level and hosted outcomes.

The first inventory slice is `devtools/scripts/ci_lane_inventory.py`. Run
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
Open new member issues only when a concrete workflow migration is assigned;
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
