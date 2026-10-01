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

## 2026-10-01 completed governance adoption

Contract provider: `2a63a15d67d2e72724b6349e89f9f026b25e860f`.
Its native governance run 36864814948 passed. All 15 registered members received
the byte-identical canonical guide through `sync_vendored_guides.py`; guide SHA256:
`c8c5af5de21e7974ab64e9256be8e56de3bf67b53fe5fa54812858fa0e212236`.
Native component-guide audit 36866426306 and vendored-guide audit 36866430137
passed after delivery. Earlier audits 36864818260/36864814906 detected the
pre-distribution gap; they were not waived.

| Member | Delivered guide commit |
| --- | --- |
| SMonitor | `91a80981405b83f5fc9c4b9b11640db153a5b4e5` |
| ArgDigest | `9ee927c9256c34aeff7cc929fc0e4c1f269b5723` |
| DepDigest | `86fe1087f540d33a86a277936f4e46acfa27a886` |
| PyUnitWizard | `66e35d3ca896bf3ed7e76ff9e53dd5c49bf447e3` |
| Pytest-Receptor | `5448ca31a1df03130d8a0a9eb7a367bed798f81b` |
| GH-Run-Receptor | `293e2ca0746322ae9c76d854f805c55f77f1935f` |
| MolSysMT | `30711dd41fff0f13815d725cb18871b17274ee73` |
| MolSysViewer | `1a7f20e66a5f2aeef1979c5c96f23e70fb241830` |
| TopoMT | `ad388afe169dbcda982d582675eea01f4bf3c5b4` |
| PharmacophoreMT | `54d0029c3e4e1f9729c81b9c1c3af925d5f6e9ac` |
| ElastNetMT | `b9e3ab29a34ab69006d68df8dff62f31792c93a3` |
| DockingMT | `d0cc7d254a40d515375112fc751b5f77ee03bb86` |
| Ackredit | `10f1a30bf423aa680d8f49726172e0cec3517ce5` |
| LinDelINT | `fa1f37a241e1daf30e7596cc4e97a903fd98aa57` |
| MolSys-AI | `95bc2805e590cb68212b21189a6352451ad4b590` |

MT, Viewer and DepDigest also adopted the pinned lightweight shared conformance
workflow. Native runs 36866412845, 36866417706 and 36866422530 respectively
passed. This is administrative publisher conformance, not a full scientific suite.

### Installed-matrix evidence instead of fixed job counts

Provider `778c918b37a1c2c2fa03ed387a000bff0edf1b3d` adds a read-only common
composite, descriptor and seven regression tests. It verifies exact source,
workflow, pair title, successful attempt, complete named cells, mandatory successful
installed-evidence steps and absence of a rerun race. Native governance run
36867833977 passed. MT commit `8195ef2e0` and Viewer commit `3db82d02` replace
their incompatible fixed job counts (17 and 21) with this provider, retaining
independent receipts before promotion. Their current descriptors both require
four platforms and four Python minors; historical five-platform evidence keeps
its own explicit descriptor.

Read-only native provider run 36870288683 and consumer runs 36870400939 (MT)
and 36870406262 (Viewer) passed against existing staged-pair run 36121427459,
source `e28ceb9ea0de0cc86bc370e5aff1e96c4cc71c69`, twenty installed cells.
No scientific gate was rerun. The first provider probe 36867834546 correctly
rejected a descriptor naming the current installation step: the historical run
used "Install the staged package pair". The corrected historical descriptor
matches that source; future promotion still checks "Install the selected package
pair" from the current workflow. No rejection was converted into a pass by
weakening the expected evidence.

The public-file verifier, native installed matrix and publication receipts prove
different claims. Viewer run 36860171883 remains an overall failure despite its
successful public-file job: its historical Windows launcher defect remains
uibcdf/molsysviewer#101 / uibcdf/molsyssuite#47. The central metapackage exception
remains uibcdf/molsyssuite#67. New publications and the deferred scientific
execution reviews are outside this completed governance adoption.
