# Python ecosystem policy rollout

**Owners:** `uibcdf/moli#6` for the platform rule;
`uibcdf/molsyssuite#6` for member adoption.

**Effective snapshot:** MOLI `15b38fbe17b6ee9fa9aac2a8e21b80d76a8da70f` plus
MolSysSuite `policy-v1.4.12`.

MOLI published the support-library and developer-tool policies on 2026-09-23.
Publication changes the inherited baseline; it does not establish member adoption.
At the initial checkpoint, all 14 registered Python members had `pending` reviews for
both policies in `suite.toml`. Some members already use particular libraries or
receptors, but no complete applicability review has yet been accepted under this
snapshot. This conservative state prevents guide delivery or an older CI run from
being mistaken for proof of adoption.

The live declared inventory is:

```bash
python devtools/scripts/python_ecosystem_status.py
```

The validator checks record coverage and evidence requirements without requiring
all members to be adopted. `--require-adopted` is the rollout completion gate.
Each review advances only with a member issue and linked evidence describing
applicable boundaries, non-applicability, implementation and tests, and any bounded
exception. Existing member migration issues may carry the review when their scope
matches; the suite issue remains the coordination record.

The separate guide-copy and policy-caller inventory remains under
`uibcdf/molsyssuite#34`. A policy caller that is current or compatible with
`policy-v1.4.11` does not prove adoption of either newly inherited policy.

## SMonitor support-library review

Under `uibcdf/smonitor#24` and `uibcdf/smonitor#29`, SMonitor's support-library
state is `adopted` under the effective MOLI bootstrap rule at `15b38fb`.
SMonitor is the diagnostic provider and fixed millisecond timing fields do not
create a PyUnitWizard boundary. Public configuration and event validation are
ArgDigest-shaped, and the optional `rich` backend is DepDigest-shaped. Both
providers require SMonitor at runtime, so the scoped structural
non-applicability rule keeps these bootstrap boundaries local while those
reverse edges exist. SMonitor's source dependency/import-order guard passed in
hosted QA `36233454261`; clean published Linux/Python 3.13 installation and
all six import orders passed with SMonitor 0.17.3, ArgDigest 0.13.0 and
DepDigest 0.11.1. A missing `rich` backend produced an actionable ImportError.
The previous bounded exception is removed from the inventory. Developer-tools
adoption remains independently evidenced.

## DepDigest member review

Under `uibcdf/depdigest#18`, DepDigest adopted the inherited developer-tools
policy in source commit `19a478ba5e2b99a65de71616d6a920f02866253f`.
Its canonical test requirements now pin published pytest-receptor 1.1.0, all
hosted pytest workflows use the `ci` profile, and the repository configures
rerun commands for `python -m pytest`. Local pytest-receptor passed 104 tests;
hosted routine CI `36063274018` passed with 103 tests and one skip and
confirmed the exact Conda package. The shared policy `36063275021`, full
12-cell Python/OS matrix `36063283769`, and three-cell Python 3.14 probe
`36063283598` passed. GH Run Receptor inspected all four runs.

The support-library review is `partial`. DepDigest already uses SMonitor for
missing-dependency and plugin-load diagnostics, with tests for signals and
emission failure. DepDigest itself implements optional-dependency handling;
there is no physical-quantity boundary for PyUnitWizard. ArgDigest depends on
DepDigest, while DepDigest exposes some public argument checks. Adding
ArgDigest here would create a runtime cycle, so the member issue owns a
bounded design decision before this review can be called complete.

## ArgDigest member review

Under `uibcdf/argdigest#20`, ArgDigest adopted the inherited developer-tools
policy in source commit `1d8e337726ee9647aa3a56671b5c6c7def063257`.
Both CI test environments now pin published pytest-receptor 1.1.0, all hosted
pytest workflows use the `ci` profile, and rerun commands match
`python -m pytest`. Local pytest-receptor passed 274 tests. Hosted routine CI
`36064688726` passed with 273 tests and one skip, confirming the exact Conda
package and profile. The shared policy `36064689045`, 12-cell Python/OS matrix
`36101321876`, and three-cell Python 3.14 probe `36101321962` passed. GH
Run Receptor inspected all four runs.

The support-library review is `adopted`. DepDigest and SMonitor are runtime
dependencies with exercised integration paths, and ArgDigest itself provides
argument validation. Source `d6dcebe` pins published PyUnitWizard 0.27.0 in
both hosted test environments and requires its import before pytest. Routine
CI `36335205697`, policy `36335206079`, and the 12/12 Linux, macOS, and Windows
matrix `36335240891` passed. Each matrix cell on Python 3.11–3.14 imported
PyUnitWizard 0.27.0 and passed 283 tests with one unrelated sibling-checkout
skip. GH Run Receptor inspected the exact-commit runs; the member record was
archived under `uibcdf/argdigest#20`.

## PyUnitWizard member review

Under `uibcdf/pyunitwizard#89`, PyUnitWizard adopted the inherited
developer-tools policy in source commit `c8cd85652d172fae7736154e0e37e24ee2c7825a`.
Its test, development, and release-gate environments pin published
pytest-receptor 1.1.0. Hosted pytest commands select the `ci` profile while
preserving their test selection, coverage, JUnit report, xdist, and release
gates. Local pytest-receptor passed 596 tests with eight skips. Hosted routine
CI `36102753740` passed with 622 tests and five skips, and its native log
confirmed the exact `uibcdf` Conda package and `ci` profile. The suite policy
run `36102754343` and six-job release gates `36102768017` passed. The
eight-cell Python/OS matrix `36102767731` passed. GH Run Receptor inspected
all four runs.

The support-library review remains `partial`. SMonitor provides tested
diagnostics; DepDigest manages optional backend dependencies; PyUnitWizard
owns the physical-quantity boundary. Source `00d4707` pins published ArgDigest
0.13.0 in the test, development, and release-gate environments. Routine CI
`36335377594`, policy `36335377971`, release gates `36335382518`, and the
eight-cell Linux/macOS matrix `36335382533` passed. Native logs confirmed the
published adapter import on Python 3.11–3.14. The member record under
`uibcdf/pyunitwizard#89` now holds that evidence. Its remaining decision is
whether native public argument checks should use ArgDigest or warrant a
bounded provider exception, with dependency and import-order analysis if a
reverse runtime edge is proposed.

## Pytest Receptor member review

Under `uibcdf/pytest-receptor#6`, both inherited reviews are `adopted`.
At an earlier checkpoint, source commit `e51fc6f` changed its hosted
eight-cell Python/pytest matrix from the `llm` to the `ci` profile in both
ordinary and distributed test commands. The earlier matrix `36024482632`
passed all eight test cells with the former profile. Local `--receptor=llm`
passed 172 tests with nine skips;
the exact-change matrix `36134742751` was pending at that checkpoint.
Subsequently, source `29516dd` passed all 11 hosted test cells in run
`36311551496` with the `ci` profile, serial and xdist testing, and a clean
wheel packaging job. Policy run `36311551788` passed. The provider's local
review resolved how the published-release pin applies to self-testing: its
own tests use the checkout.

The support-library review records PyUnitWizard as inapplicable because the
plugin has no physical-quantity boundary. The local adoption record documents
the decisions for passive optional pytest-plugin hooks and public option,
artifact, and diagnostic paths. Guards for options and artifact warnings live
in `tests/test_artifact.py`. No runtime library was added solely to change
the inventory state.

## MolSysMT member review

Under `uibcdf/molsysmt#244`, MolSysMT's developer-tools review is `partial`.
Source commit `de9e9c91966d587fba9072a2a14e00406a31618f` updated the Conda
test pin from pytest-receptor 0.6.0 to published 1.1.0, added the same exact
release to the development environment, and added it to the standalone
data-integrity workflow. That workflow now uses `--receptor=ci` while keeping
the curated test selection. Other active hosted pytest commands already used
the `ci` profile and the repository already configured rerun commands for
`python -m pytest`. Local targeted receptor tests passed 92 cases. The
exact-commit data-integrity run `36105299656` and developer-guide run
`36105299549` passed; the former confirmed the published PyPI version and
profile. The smoke run `36105275404` was cancelled. Weekly `36105275495`
failed in all three Python cells, and the six-cell full matrix `36105299602`
failed in all six cells. Every failed job reached pytest and reported the same
three shared unit-policy assertions in
`tests/cross_repo/test_unit_policy_authority.py`: import order changes the
policy and a later MolSysViewer import resets the user's unit choice. The
matrix log confirms the published Conda receptor 1.1.0 and its truthful
`FAIL exit=1` report. A separate earlier revision `8d58581` passed the
matrix with newer controlled source revisions. GH Run Receptor inspected
these runs. MolSysMT later merged candidate `89ceda0ad` into `main`, changing
the controlled sources and Python 3.14 metadata. The failed runs above
describe the preceding `de9e9c9` revision. On the merged checkout, the
MolSysSuite repository checker and six focused unit-policy tests pass locally.
Candidate `e28ceb9ea` also passed the six-cell full matrix in run
`36120923064`, but that branch predates the receptor 1.1.0 pins. Exact-main
run `36132035176` tests the integrated revision `6a334cc3e` with controlled
MolSysViewer commit `cf427942d0b08a1c5c60f262c6a6b33f248d6f8b`.
Its first macOS/Python 3.11 cell stopped during editable installation because
the runner's Rust 1.97.1 toolchain lacked `rustc`; pytest did not start in that
cell. Five test cells were still running at this checkpoint. Developer-tool
adoption remains `partial` pending a successful integrated gate.

The support-library review is also `partial`. MolSysMT declares and uses
ArgDigest, DepDigest, SMonitor, and PyUnitWizard; targeted argument, dependency,
diagnostic, and quantity tests pass. The member issue retains the full
public-boundary audit and related open integration work, while the authorized
Python 3.14 transition remains separately tracked in `uibcdf/molsysmt#237`.
These partial states will advance only with exact-commit hosted evidence and
the remaining member decisions.

## MolSysViewer member review

Under `uibcdf/molsysviewer#110`, both policy reviews are `partial` after source
inspection at `19dadc1a`. MolSysViewer declares all four support libraries and
has representative integration tests for argument digestion, optional
dependencies, diagnostics, and quantities. Six emitted SMonitor codes still
lack message templates (`uibcdf/molsysviewer#107`), so diagnostic integration
cannot yet be claimed complete. The member review also retains the public
quantity and argument-boundary decisions.

The main CI test environment does not pin Pytest Receptor and its pytest
commands do not select the `ci` profile. The Python 3.14 source-pair workflow
does select that profile, but its receptor dependency is unpinned. GH Run
Receptor has a workflow profile configuration; the member review still needs
published-version and first-inspection evidence. The local issue owns the
implementation and test decisions; the central inventory tracks the two
independent adoption states.

## TopoMT member review

Under `uibcdf/topomt#56`, support-library adoption is `partial` and
developer-tool adoption is `adopted` at source `015cb48`. TopoMT declares
ArgDigest, DepDigest, SMonitor, and PyUnitWizard. Public argument and quantity
paths are present, and the shared unit defaults are set only when no policy
is active. SMonitor's catalog still cannot render its authored diagnostics
(`uibcdf/topomt#15`), and the AlphaSpace2 optional backend boundary needs
member review before full support-library adoption.

Both maintained CI test environments pin published Pytest Receptor `0.6.0`,
and the pytest route selects `--receptor=ci`. Published GH Run Receptor
`1.0.0` inspected exact-source CI `36311638015`, policy `36311638223`, and
Ruff `36311638009`. Policy and Ruff passed. CI failed six of six test jobs
with `ModuleNotFoundError: alphaspace2`; the receptor reported the failure
truthfully, so this is not passing matrix or release evidence. The Python
matrix gate stays in `uibcdf/topomt#16`, while the ecosystem adoption work
stays in the member review issue.

## PharmacophoreMT member review

Under `uibcdf/pharmacophoremt#6`, the support-library review is `partial` at
source `7df2496b`. Public modeling paths use ArgDigest, SMonitor, and
PyUnitWizard. SMonitor is imported directly but absent from package runtime
dependencies, and its catalog mapping still prevents authored diagnostics
from rendering (`uibcdf/pharmacophoremt#2`). A DepDigest configuration exists,
but an optional MolSysViewer path imports the viewer directly. The member
review owns the user-facing dependency and boundary tests needed next.

The developer-tool review is `adopted` on exact hosted evidence. Both test
environments pin published Pytest Receptor `0.6.0`, and the six-cell CI matrix
uses `--receptor=ci`; run `36310571253` passed all six cells at the inspected
source. Published GH Run Receptor `1.0.0` first inspected that run and the
successful suite-policy run `36310571699`. The member issue retains the
commands and the independent policy decisions.

## ElastNetMT member review

Under `uibcdf/elastnetmt#14`, both reviews are `partial` at source `6705363`.
All four support libraries are declared and used, but import unconditionally
resets PyUnitWizard defaults. Exact-source CI `36311638612` failed four of six
trajectory cells because LinDelInt's auto engine raised a missing-CuPy error;
provider issue `uibcdf/lindelint#8` carries the consumer evidence. Suite-policy
run `36311638884` passed. GH Run Receptor `1.0.0` inspected the runs, and
native failed logs identified the traceback. Python 3.11/3.12 test environments
omit Pytest Receptor and the workflow invokes plain pytest. The member record
holds the policy-boundary and tool-migration steps.

## DockingMT member review

Under `uibcdf/dockingmt#19`, both reviews are `partial` at source `9c5d56a`.
DepDigest, SMonitor, and PyUnitWizard have runtime paths and tests. ArgDigest
is configured but has no package call sites; public argument applicability
needs an explicit decision and focused tests. CI `36310576692` passed 4/4
with `--receptor=ci`, and suite-policy `36310577050` passed; GH Run Receptor
`1.0.0` inspected both. The test environment and extra leave `pytest-receptor`
unpinned, so the developer-tool claim awaits an exact published pin and
hosted version evidence.

## Ackredit member review

Under `uibcdf/ackredit#72`, support-library adoption is `adopted` at source
`8877943`. ArgDigest, DepDigest, and SMonitor are declared and exercised by
argument, optional dependency, and diagnostic tests; PyUnitWizard has no
physical-quantity boundary in this citation/provenance component. Prior issues
`uibcdf/ackredit#6` and `uibcdf/ackredit#62` record the integrations. The
developer-tool review is `partial`: CI `36310576715` passed 7/7 with
`--receptor=ci`, suite-policy `36310577022` passed, and GH Run Receptor
`1.0.0` inspected both, but maintained Conda environments leave
`pytest-receptor` unpinned.

## LinDelInt member review

Under `uibcdf/lindelint#9`, both reviews are `partial` at source `437a306`.
The package declares all four support libraries, but import resets shared
PyUnitWizard defaults and the auto-engine missing-CuPy path lacks a usable
fallback (`uibcdf/lindelint#8`). Own CI `36310576811` passed 6/6 and
suite-policy `36310577229` passed; GH Run Receptor `1.0.0` inspected both.
The maintained test environment has no Pytest Receptor pin, and CI invokes
plain pytest. The member record specifies the boundary tests and CI changes.
