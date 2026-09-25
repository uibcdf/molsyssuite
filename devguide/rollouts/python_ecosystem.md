# Python ecosystem policy rollout

**Owners:** `uibcdf/moli#6` for the platform rule;
`uibcdf/molsyssuite#6` for member adoption.

**Effective snapshot:** MOLI `6a91433bd38582980d0781474be6a80c58f48886` plus
MolSysSuite `policy-v1.4.11`.

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

The support-library review is `partial`. DepDigest and SMonitor are runtime
dependencies with exercised integration paths. ArgDigest itself provides
argument validation. PyUnitWizard is an optional quantity adapter with tests,
but the existing Python 3.14 matrix uses the core environment without it. The
member issue must retain published-release evidence for that optional
integration on every claimed Python minor, or a bounded exception, before
claiming complete support-library adoption.

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

The support-library review is `partial`. SMonitor provides tested diagnostics;
DepDigest manages optional backend dependencies; PyUnitWizard owns the physical
quantity boundary. ArgDigest's optional PyUnitWizard adapter passes local
smoke and collective error-path tests, but it is absent from hosted test
environments. Its published integration across claimed Python minors is thus
unproven. The member issue also retains the decision about whether native
public argument checks need ArgDigest without creating a library cycle.
