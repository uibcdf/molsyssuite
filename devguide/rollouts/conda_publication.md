# Conda publication contract adoption

Coordination: uibcdf/molsyssuite#27. Shared verifier incident:
uibcdf/molsyssuite#48. Normative rules:
[`conda_publication_policy.md`](../conda_publication_policy.md).

## Measured profiles and preserved evidence

| Consumer/profile | Measured evidence | Adoption and remaining scope |
| --- | --- | --- |
| MolSysMT, native ABI3 | Public pair matrix 36129993869, 20/20 historical cells; public inventory 36850953842; consumer verifier 36860167904 | Common verifier 399d33a; four current artifact/test platforms remain local; five historical artifacts remain independently addressable. Lightweight shared publication gate adoption is recorded below. |
| MolSysViewer, noarch Python | Same historical pair; public verifier job 36860171883 | Common verifier 399d33a adopted. The same workflow's separate Windows launcher job failed for historical 0.23.4-py_5; Viewer#101 / MolSysSuite#47 remain open. |
| DepDigest, noarch Python | Staged matrix/promotion 36230598357; direct 0.11.2 release 36233613024 with exact-source matrix 36233298114 and all-label absence; common verifier 36860269789 | Actual third consumer of the common verifier. Its tested local route validator remains supported; it is not replaced with a scientific-component workflow. |
| SMonitor, noarch Python | Exact-file additive promotion 35589475337; local route correction SMonitor#20 | Existing local validator is a compatibility reference. Common-provider rollout remains prospective for changed release work. |
| Central metapackages | Source inspection of two legacy recipes and old publisher | Publisher pin, one-file topology, manual staging, route preflight, producer receipts and independent verifier are implemented. Full profile remains excepted under #67; no package publication was exercised. |

The administrative conformance gate and versioned transition validator do not
replace native scientific or installed-artifact evidence. Existing exact-source
release pilots remain dated evidence; no fresh scientific suites or publications
were required for governance acceptance. Compact/native/public claims stay separate.

## Central metapackage exception

- Owner: uibcdf/molsyssuite#67; maintainers dprada/LMMV.
- Affected rules: current per-package pre-tag plans and installed dependency/
  capability evidence for `molsyssuite` and `molsyssuite-dev`.
- Rationale: both historical recipes still declare calendar version `2026.02.0`;
  neither has a current reviewed release plan or measured metapackage matrix.
  Reusing component science gates would not validate this profile.
- Interim behavior: the publisher rejects a missing/nonconforming plan, mismatched
  recipe/tag/build identity, unavailable native gate or inconclusive/occupied
  registry. Manual builds are staging-only. `policy-v*` governance releases do
  not publish Conda packages. Each package builds once; no noarch conversion matrix.
- Review/expiry: 2026-12-31; no new public metapackage release is covered by this
  exception without the required profile evidence.
- Removal: reviewed matching plans/recipes, clean installed dependency/capability
  gates for the claimed matrix, then an explicitly authorized package candidate
  exercising the guarded route. This work creates no package-release authorization.

The exception is a visible incomplete profile, not a passing release claim.

## MolSysMT first-producer bootstrap

The current 0.22.4 staged plan records the hard-dependency cycle and installed-pair
gate; its staging build retains the existing `--no-test` bootstrap. The public
build never uses it, and exact installed-pair success remains mandatory before
promotion. Evidence and scope are the historical MolSysMT#195 and this central
policy's measured pilot. Responsible role: component maintainers. Review deadline:
before any new candidate/version decision, and no later than 2026-12-31.
Changing that plan must replace this historical bootstrap decision with an
issue-backed candidate-specific exception or restore normal staging recipe tests.
This entry does not waive testing for arbitrary future versions.

## Other member release work

All registered members receive the policy route through the canonical guide.
Classify the artifact topology and inspect local publication invariants before
changing a release pipeline. A member without Conda publication records
non-applicability. Existing custom publishers keep local profiles and must supply
a tested equivalent guard or a dated exception before an affected new release.
Guide delivery alone does not prove publisher adoption.
