---
summary: Expand Python support progressively to 3.14 across eligible components
issue: uibcdf/molsyssuite#29
status: active
opened: 2026-09-20
closed:
verification: inspected
area: [python, compatibility, packaging, ci]
guard:
normative:
blocked_by: []
supersedes: []
---

# Expand Python support progressively to 3.14 across eligible components

**Reported:** 2026-09-20, while preparing new stable Conda releases for the support
libraries needed by the coordinated MolSysMT--MolSysViewer release.
**Status:** active; the first cohort and evidence requirements are decided. Pytest
Pytest Receptor and GH Run Receptor are admitted after independent verification of their
public Python 3.14 releases. The four support-library dependencies remain unadmitted.

## What

Begin a progressive expansion from Python `>=3.11,<3.14` to `>=3.11,<3.15`. The first
cohort is the pure-Python dependency chain SMonitor, DepDigest, ArgDigest, and
PyUnitWizard. Pytest Receptor and GH Run Receptor are enabling infrastructure in the same
rollout: the former must be able to run the 3.14 evidence and the latter must be able to
inspect its hosted workflows. A component joins the supported 3.14 set only after its own
runtime, dependencies, CI, package metadata, and clean installation have been demonstrated.

The current suite-wide range remains normative while this evidence is collected. The
proposal must define an explicit transitional representation before any component
advertises 3.14; an experimental CI lane alone is not a support claim.

## How

1. Establish Python 3.14 evidence for Pytest Receptor and GH Run Receptor, then add
   non-claiming Python 3.14 evidence lanes to the first-cohort repositories and run their
   complete required suites in dependency order.
2. Verify Conda/Python dependency resolution independently of source checkouts, including
   installed version identity and CLI/import smoke tests.
3. Amend `devguide/python_policy.md` and `suite.toml` with a machine-readable phased
   adoption mechanism. It must distinguish the default supported range, components that
   have earned 3.14 support, and temporary exceptions with tracking issues and expiration
   conditions.
4. Update metadata, required CI, recipes, documentation, and minor release notes together
   in each admitted component.
5. Publish the pure-Python chain in dependency order. Components with native extensions
   or native optional stacks are assessed separately and must not inherit a support claim
   from the pure-Python cohort.

## Why

The four first-cohort projects are already being prepared for new minor releases and are
the dependency foundation of MolSysMT and MolSysViewer. Testing Python 3.14 now avoids
publishing fresh packages with an immediately stale upper bound. Central coordination
prevents one component from admitting an interpreter that its required dependencies or
the suite's conformance policy still reject.

## What is measured and what is assumed

**Inspected:** all four first-cohort projects declare no compiled extension in their own
package. Their current metadata and shared policy still cap Python below 3.14. SMonitor is
dependency-free; DepDigest depends on SMonitor; ArgDigest depends on both plus NumPy; and
PyUnitWizard depends on SMonitor, DepDigest, NumPy, and Pint. This determines the rollout
order but does not prove Python 3.14 compatibility.

**Measured:** Python 3.14 is available from conda-forge. The first SMonitor feasibility
environment on 2026-09-20 did not reach collection because the exploratory Conda tool set
could not resolve its requested `build` package. This is environment-specification
evidence, not a SMonitor compatibility result. Pytest Receptor currently declares
`>=3.11,<3.14`, so using it for a 3.14 probe requires explicit experimental installation
until its own support has been demonstrated.

On 2026-09-20 Pytest Receptor passed 172 tests locally on CPython 3.14.7 with
pytest 9.1.1 and pytest-xdist 3.8.0 using 12 workers. Hosted run `35509547575` then passed
all 11 jobs, including Python 3.14 with both pytest 8 and pytest 9. This authorizes its
local contract migration under `uibcdf/pytest-receptor#3`; it is not admitted until the
metadata, package checks, documentation, and clean installation agree.

Pytest Receptor completed those admission gates later on 2026-09-20. Commit `3b88958`
aligned metadata, classifiers, the Python/pytest matrix, the Conda recipe, release checks,
documentation, and release notes; hosted run `35512512809` passed all 11 jobs. Commit
`f2ff0e3` then adopted the shared noarch staging pattern. Conda run `35528151054` passed
and retained producer evidence; gh-run-receptor reported one successful noarch package
job and one available artifact. Independent channel inspection found
`pytest-receptor-1.1.0-py_0` on `uibcdf/label/staging`, and a clean CPython 3.14.7
environment installed it from that channel, imported version `1.1.0` from
`site-packages`, reported `Requires-Python: <3.15,>=3.11`, and loaded the receptor CLI.
This evidence authorizes promotion, but it does not publish a stable `1.1.0` release.
The registry retained Pytest Receptor as `authorized` while its immutable GitHub/PyPI
release and public `uibcdf` promotion were pending. This stricter boundary prevents a
source branch or staging label from being mistaken for delivered support.

The release candidate `14e996430fa2b3810ae68f8b7fed16298dc7733b` passed the
complete 11-job hosted matrix in run `35532366589`, including both Python 3.14/pytest
cells. Release `1.1.0` was published on GitHub and PyPI; PyPI publication run
`35532680937` succeeded and a clean CPython 3.14.7 wheel installation confirmed the
version, supported interpreter range, installed path, and pytest entry point. Conda
promotion run `35571349099` published the separately tested exact-tag build `py_1`
without rebuilding or replacing it. Independent public `uibcdf/noarch` metadata reported
SHA-256 `4b56e6fc7c24e3f01d771c989bd7ed4bac9cf40c05e22f831a0ffff8defcd7dc`.
A new CPython 3.14.7 Conda environment sourced exclusively from public `uibcdf` and
conda-forge installed `pytest-receptor=1.1.0=py_1`, imported installed version `1.1.0`,
reported `Requires-Python: <3.15,>=3.11`, and loaded the pytest plugin. Pytest Receptor
therefore became the first `admitted` member of this Python 3.14 rollout on 2026-09-21.

GH Run Receptor then passed its first transition feasibility gate under
`uibcdf/gh-run-receptor#49`. A clean clone of commit `61d9a4e` installed into a new
CPython 3.14.7 environment with the existing metadata override required for an
unclaimed interpreter. Its complete suite passed 443 tests with 12 workers in 2.73
seconds using pytest 9.1.1, pytest-xdist 3.8.0, and the staged pytest-receptor 1.1.0.
The project has no runtime Python dependencies, and the current development dependencies
resolved on 3.14. The final release commit
`d4a639b5a9eb3ce5a72daa407b42f8fe8e69b285` passed the full twelve-cell
Ubuntu/macOS/Windows by Python 3.11--3.14 compatibility matrix in run `35573910621`.
All 445 local tests passed with 12 workers after making a security ZIP fixture's xdist
collection IDs deterministic. The draft-first GitHub Release 1.1.0 was published in run
`35574071616`; the three public assets were independently downloaded, and
`sha256sum -c SHA256SUMS` verified both wheel and sdist. A new CPython 3.14.7 environment
installed the public wheel, imported version 1.1.0 from `site-packages`, reported
`Requires-Python: <3.15,>=3.11`, and executed the console command. The GitHub CLI
extension, pinned to 1.1.0 in an isolated XDG directory, resolved the exact release
commit and reported version 1.1.0 using that Python environment. Canonical installation
guidance, documentation and the public badge now state the delivered range. GH Run
Receptor is therefore also `admitted`; it does not claim PyPI or Conda distribution.

**Assumed pending measurement:** supported runners and Conda dependencies exist for the
required first-cohort matrix. Every such assumption must be replaced by retained command
or hosted-run evidence before a repository changes its support metadata.

## Alternatives and refuted paths

- Changing the global range immediately was rejected: MolSysMT has a native ABI3
  extension and other components have native dependency stacks that have not been tested
  on 3.14.
- Letting components change independently was rejected by the existing Python policy and
  would make the shared conformance gate contradict their metadata.
- Waiting until every MolSysSuite member supports 3.14 was rejected: pure-Python support
  libraries can provide value earlier if the transition and exceptions are explicit.
- Treating a successful import as support was rejected: the complete required suite,
  packaging metadata, dependency resolution, and clean installation are all part of the
  existing definition of support.

## Scope and exclusions

The first implementation cohort is SMonitor, DepDigest, ArgDigest, and PyUnitWizard, with
Pytest Receptor and GH Run Receptor as enabling infrastructure. MolSysMT, MolSysViewer,
and incubating/native components remain at the current range until their own issues provide
evidence. This proposal does not drop Python 3.11, change the routine development
interpreter, or declare Python 3.14 support merely because a package is `noarch`.

## Acceptance criteria

- The central Python policy defines the transitional adoption and exception model.
- `suite.toml` represents it and the offline governance validator enforces it.
- Each first-cohort and enabling component has a local implementation issue and retained
  Python 3.14 test and clean-package evidence.
- Each admitted component updates metadata, CI, Conda recipe where applicable,
  user/developer documentation, and release notes in one coordinated change; publishes
  an immutable release to every claimed package channel; and passes independent clean
  Python 3.14 installation checks against those public artifacts.
- The dependency chain is published and independently installable on Python 3.14 in
  dependency order.
- Components outside the admitted cohort continue to state the narrower range explicitly.
- A follow-up decision records when the default suite-wide range can become
  `>=3.11,<3.15` without exceptions.

The eventual durable guard belongs in the central governance tests; the normative record
will be `devguide/python_policy.md`.

## Local implementation issues

Local issues will be opened after each repository's first Python 3.14 feasibility run;
failed feasibility remains useful evidence and must not be converted into a support
claim.

## Dependencies and risks

The main risks are unavailable native transitive dependencies, a noarch package silently
admitting an untested interpreter, and a central rule that reports universal support while
only a cohort has passed. The phased model must fail closed on all three.

## Provenance

Source and policy inspection on 2026-09-20. No Python 3.14 execution evidence is attached
at filing time.
