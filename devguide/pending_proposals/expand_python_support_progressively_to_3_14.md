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
**Status:** active; the first cohort and evidence requirements are decided.
Pytest Receptor, GH Run Receptor, SMonitor, and DepDigest are admitted after independent
verification of their public Python 3.14 releases. ArgDigest is now admitted after
its public 0.13.0 release; PyUnitWizard is now admitted after its public 0.26.0
release and independently verified Python 3.14 package installation.

On 2026-09-24, the suite administrator explicitly authorized MolSysMT and
MolSysViewer to enter this transition under `uibcdf/molsysmt#237` and
`uibcdf/molsysviewer#93`. The component teams reported final-version
candidate sources `3eb5afd1de087f775b78d7fa45ad69cca3a02d43` for
MolSysMT 0.22.4 and `ec4c71e574d798b7c8675b7e7e983da878ce9889`
for MolSysViewer 0.23.4. Their isolated local full suites passed
10,225 tests (11 skips) and 2,112 tests (14 skips), respectively, with
12 workers; MolSysMT's fast release gates passed 13/13. The earlier
technical staged 0.22.3/0.23.3 pair passed 20/20 installed cells, but
that is not evidence for the final-version candidates. Those candidates
have not been built, uploaded, tagged or independently installed from their
claimed public channels. Both components are therefore `authorized`, not
`admitted`; the stable suite default remains unchanged. The transition-aware
gate must now require the target Python range and 3.14 CI for both member
callers, using only `policy-v1.4.11` until later releases supersede it.
MolSysViewer's existing PR policy run `36055805114` rejected its
older `policy-v1.4.6` caller against the target metadata; a new immutable
central release was needed before either component could repin and rerun.

That release is `policy-v1.4.11`, an annotated tag at central commit
`6b51af81d50a5cfbafc08113fa617b34a3ee73df`. The effective snapshot
remains MOLI `6a91433bd38582980d0781474be6a80c58f48886` plus that suite
tag. The offline governance validator, Ruff check and format check passed;
pytest-receptor reported 141/141 local tests passing. Hosted governance run
`36060463505` passed. After the canonical guide's 15 consumer copies were
synchronized and published, component-guide run `36061416552` passed 16/16
and vendored-guide run `36061420024` passed 1/1. Local implementation and
public-admission evidence remain owned by the two component issues.

ArgDigest 0.13.0 completed the public admission gates on 2026-09-22. Commit
`9880fa7b990fd0987ff0de715b665eb9e11c11b2` passed the hosted 12-cell
source matrix (`35695504353`) and shared policy gate (`35695504851`). The exact
`noarch` staged build `py_1` passed 12 clean installed-package cells on Linux,
macOS, and Windows with Python 3.11--3.14 (`35696336418`). GitHub Release
`0.13.0` is public; the release-triggered workflow (`35697325021`) verified the
staged route without rebuilding. Promotion (`35697373110`) moved the same file
to `uibcdf/noarch`, and an independent public channel query returned SHA-256
`273ae5053d0aaa2d207ec9a2c684588fe3da539219b1d91cdea3b1f8dd265007`.
A fresh public-channel Linux Python 3.14.7 environment imported ArgDigest
0.13.0, DepDigest 0.11.0, and SMonitor 0.16.0 and ran the ArgDigest CLI.
Zenodo record `22892326` independently confirms the 0.13.0 source snapshot,
version DOI `10.5281/zenodo.22892326`, and concept DOI
`10.5281/zenodo.22892325`; it does not archive the Conda artifact. These
facts authorize central `admitted` status and the corresponding public badge.

PyUnitWizard entered the transition as `authorized` on 2026-09-22 under
`uibcdf/pyunitwizard#78`. Its final 0.26.0 release commit
`026be28d9530077d57f92cbd5fd1755c0982c596` passed the hosted Linux/macOS
by Python 3.11–3.14 full-suite matrix (`35715344397`), release gates
(`35715344393`), and shared policy gate (`35715345024`). The exact `noarch`
candidate `pyunitwizard-0.26.0-py_1.tar.bz2` was built in staging
(`35715749149`) and passed eight clean installed-package cells plus the
receipt gate (`35716044649`). The GitHub Release `0.26.0` was published;
its release-triggered Conda workflow (`35716501517`) selected the staged
route and skipped rebuilding. Promotion (`35716642205`) copied the exact
candidate to `uibcdf/noarch`; the independent public channel query matched
SHA-256 `3689855787a82b7dc942c6b3a71f40733f4f2633c3509f10c12b45892e9ae1a9`.
A clean public-channel Linux Python 3.14.7 environment imported PyUnitWizard
0.26.0 with public SMonitor 0.16.0 and DepDigest 0.11.0 and passed a unit
conversion smoke test. A separate clean environment installed the immutable
Git tag using `pip --no-deps` over those public Conda dependencies and passed
the same version/API check. PyUnitWizard is therefore `admitted` for the
declared range; this evidence does not claim Windows CI or a PyPI distribution.
Zenodo verification is a separate release/archive check, not inferred from
the GitHub Release or Conda package.

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

SMonitor, the first support-library dependency, passed a source-tree feasibility run on
Linux CPython 3.14.7 at commit `7b10cb9db537c3ea7a531283bdebcb6624f092bc`:
461 tests passed, one was skipped, and the cross-library test passed with NumPy 2.5.3
and Pint 0.26.1 installed in the temporary test environment. The first two attempts
missed those test dependencies, not a SMonitor runtime requirement. Local issue
`uibcdf/smonitor#17` and its developer report retain the measurement and the staged,
hosted, public-artifact, and clean-install gates. The later exact release commit
`7daac74c6641e6003df8bbcc6cca91709ec891b9` passed all twelve hosted Linux,
macOS, and Windows by Python 3.11--3.14 cells in run `35587196946`. Its verified
`noarch: python` staged build `0.16.0-py_1` was promoted without rebuilding by the
shared Action in run `35589475337`. Independent public `uibcdf/noarch` metadata found
the same SHA-256,
`a7f0ea073786354695c606e89959e67fcd4afc910a42683bba00955eb17163d7`.
A fresh Linux Python 3.14.7 Conda environment installed the exact public build from
`uibcdf` and `conda-forge`, imported SMonitor 0.16.0 from `site-packages`, and ran its
CLI. GitHub Release 0.16.0 and the separately checked Zenodo source snapshot are public.
SMonitor is therefore `admitted` on 2026-09-21. This does not claim a separate clean
installed-package run on macOS or Windows; hosted source compatibility covered those
platforms, and the same noarch artifact is served to each.

DepDigest began its transition under `uibcdf/depdigest#14` on 2026-09-21. Its early
source feasibility run `35595697428` passed on Ubuntu, macOS, and Windows and justified
`authorized` status only. The final release commit
`d5b259a0f4ab00756858869061604fd64d561850` passed the required twelve-cell
Python 3.11--3.14 source matrix in run `35664438560` and the suite policy in run
`35664438912`. Staging run `35664759083` built the single noarch
`depdigest-0.11.0-py_2.tar.bz2` artifact; its producer receipt and an independent
staging query agree on SHA-256
`b6ba665d9125f49506b7e4231e6065f164d3b643117a22288b44baafceff270f`.
Run `35665346654` passed the producer check and all twelve clean installed-package
cells on Linux, macOS, and Windows, verifying the exact artifact, public SMonitor,
off-checkout import, and CLI. Published ArgDigest 0.12.1 also passed a Linux/Python
3.13 consumer smoke against this staged artifact. ArgDigest itself still limits
Python to below 3.14; its transition is next, not silently inherited.

The immutable GitHub Release 0.11.0 is public. Promotion run `35665723593` added
the public Conda label to the tested `py_2` file without rebuilding; an independent
public registry query matched the same SHA-256. A fresh Linux/Python 3.14.7 environment
resolved DepDigest 0.11.0 build `py_2` and SMonitor 0.16.0 build `py_1` solely from
public `uibcdf` and conda-forge, imported the installed version outside the source
checkout, and ran the CLI. Zenodo independently archived the source snapshot as version
DOI `10.5281/zenodo.22884369`; the public record and downloaded file checksum were
verified under `uibcdf/depdigest#11`. DepDigest is therefore `admitted` for Python
3.14. This does not change the suite-wide default or claim archival of Conda files.

ArgDigest opened `uibcdf/argdigest#13` and tested public DepDigest 0.11.0 and
SMonitor 0.16.0 in a clean Linux Python 3.14.7 environment. Its development
checkout passed 224 tests with seven optional PyUnitWizard skips after fixing
an undefined optional-import sentinel and a stale badge-color test. The first
hosted attempt failed only because a clean checkout had no generated
`argdigest/_version.py`; installing the development source explicitly corrected
the preparation. At commit `4fdbf19d386bbf476455d35c9988bf00624873e1`,
hosted non-claiming feasibility run `35668756549` passed on Ubuntu, macOS, and
Windows. GH Run Receptor reported 3/3 success, and the independent GitHub query
confirmed the exact SHA and each job conclusion. At that point ArgDigest was
`authorized`; its later public admission and remaining evidence are recorded
above. Seven optional PyUnitWizard
tests skipped in the local 3.14 environment; no claim is made for that optional
integration before PyUnitWizard's own transition. Ackredit likewise remains
outside the transition until consumer evidence.

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

The first implementation cohort was SMonitor, DepDigest, ArgDigest, and PyUnitWizard, with
Pytest Receptor and GH Run Receptor as enabling infrastructure. MolSysMT and
MolSysViewer subsequently entered as `authorized`; they cannot claim the target
range publicly until admitted. Other incubating/native components remain at the
current range until their own issues provide evidence. This proposal does not
drop Python 3.11, change the routine development
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
