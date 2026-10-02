---
summary: Audit OpenCASTp governance and route pending implementation to its owners.
issue: uibcdf/molsyssuite#72
status: resolved
opened: 2026-10-02
closed: 2026-10-02
verification: measured
area: [governance, ecosystem, admission]
guard: tests/test_governance.py::GovernanceTests::test_opencastp_admission_preserves_review_ownership_and_bounded_claims
normative: devguide/repository_contract.md
blocked_by: []
supersedes: []
---

# OpenCASTp auxiliary-member governance audit

**Reported:** 2026-10-02; follow-up to uibcdf/molsyssuite#70.
**Status:** Resolved. Dated audit, actual source conformance, hosted bounded-bootstrap
evidence and owner-local follow-ups are recorded. Scientific/distribution/coverage
qualification and the permanent policy mechanism continue in their owning issues.

## What

Audit the auxiliary member without exempting it from suite rules or disrupting active
scientific development. Keep its independently usable numerical API separate from
TopoMT's molecular preparation and Topography adapter. This audit records evidence and
ownership; it does not implement or judge unresolved numerical behavior.

## How

Inspect the exact published source, run the read-only component checker, validate an
isolated official starter reference, and register explicit pending reviews. Reuse existing
component issues for scientific, provenance and CI work; add only the missing repository
baseline and consumer-transition handoffs.

## Dated audit (2026-10-02)

Initial public snapshot: `163b27d22594fface4edcdaf069f78cee4c3b80b` (minimal README).
The actively developed team then published `c9a6f65ea6a7b76924f21df17c88830e745ca561`.
The table below reflects that newer exact-source archive; initial findings are retained
in the receipt as history. No scientific conclusions are independently qualified here.

| Requirement | State | Evidence and next owning issue |
| --- | --- | --- |
| Central identity, classification, guide registration and inventories | adopted | `suite.toml`, central README/receipts; uibcdf/molsyssuite#70 |
| Independent numerical owner / TopoMT adapter transition | partial | Component architecture and public API boundary; uibcdf/opencastp#1 and uibcdf/topomt#90; adapter pending |
| Official scaffold and published repository baseline | adopted | Component #1 checkpoint and `c9a6f65` adoption commit; exact published source passes the central checker; uibcdf/opencastp#4 handoff satisfied |
| Canonical member/provider guides and root/nested instructions | adopted | Four registered guide copies are byte-identical; `AGENTS.md` and `devguide/AGENTS.md` contain the required routes |
| Report queues, template, archive, indexes and offline reporting gate | adopted | Published source includes the local lifecycle; its index/validator check passes |
| README identity, maturity, policy, purpose and ownership | adopted | Component README agrees with auxiliary/incubating classification and distinguishes current capabilities from future plans |
| License file / source rights | partial | MIT file and third-party notices published; imported-source provenance/public distribution still uibcdf/opencastp#2 |
| Python metadata, Ruff, versioning, manifests and Conda environments | adopted | Current baseline metadata; Ruff lint and all 39 formatting checks pass; manifest graph agrees. This does not qualify installed runtime/platform support |
| Support-library applicability and dependency decisions | partial | PyUnitWizard declared and observed; owner-local pending ArgDigest/optional-backend applicability decisions under uibcdf/opencastp#2; registry review pending |
| Receptors and routine/full CI design | partial | Published pin `pytest-receptor==1.1.0`, `ci` profile, GH Run Receptor guide/profile, unfiltered routine and full lanes; hosted qualification remains uibcdf/opencastp#3 |
| Hosted policy conformance | excepted | Initial run 37055145913 failed `UNREGISTERED`. Later source `762db29` uses the approved deadline-enforced source pin; run 37058867837 executes conformance/Ruff successfully. Exception through 2026-12-31 under uibcdf/opencastp#3; permanent mechanism uibcdf/molsyssuite#73 |
| Supported-minor/platform and external-PR evidence | partial | The maintainer admitted component-specific Python 3.14 after recorded Linux four-minor installed/scientific evidence under uibcdf/opencastp#5 (central 2707ef9). CI review is partial/full with no public OS claims; external PR/coverage work remains uibcdf/opencastp#3 |
| Conda-first distribution, exact installed artifacts and controlled publication | pending | Component explicitly withholds public installation claims; registry recipe pending/access unknown; uibcdf/opencastp#2. Decide noarch from the actual delivered payload, including future native code |
| Documentation deployment and public release claims | pending | Documentation/source and local build claims exist; public qualification remains uibcdf/opencastp#2; no release/deployment evidence adopted centrally |
| Meaningful accepted coverage and README percentage | pending | Numerical coverage applicable; CI has no coverage producer/upload yet and README claims no percentage; uibcdf/opencastp#3 |
| Optional Zenodo archival | pending | Inventory `unknown`; no DOI verification or required archival claim; uibcdf/opencastp#2 |
| Inputs, geometry, units, tolerances, reference validation and limits | partial | Component scientific status and extraction manifest record owner-local evidence; broader qualification stays uibcdf/opencastp#1/#2 and is not rerun or diagnosed centrally |
| Optional-provider absence and adapter/result preservation | pending | uibcdf/topomt#90; existing semantic contract uibcdf/topomt#63; DFND ownership unchanged |
| Temporary engine coexistence | excepted | Component architecture and uibcdf/opencastp#1 retain TopoMT code by maintainer instruction, with review by 2026-12-31; future removal requires an explicit later instruction and qualified adapter |
| Rust/GPU capability delivery | pending | Only Python backend implemented according to component documentation; future capabilities are not registered as delivered; uibcdf/opencastp#1 |

## Why

Explicit dated evidence prevents a bare repository, a generated reference, or a passing
administrative check from being mistaken for an adopted component or validated CASTp
reconstruction. Each pending responsibility has a stable owner outside the central audit.

## What is measured and what is assumed

[opencastp_admission.json](../rollouts/opencastp_admission.json) records the exact source,
eight initial findings, the newer published-source checks, generation and reference checks. The published tree
was fetched read-only. No unpushed scientific work was inspected or overwritten, no
scientific suite was launched, and no Codecov/Zenodo result was inferred from absence of
workflow files. Future API shape and Rust/GPU delivery remain component decisions.

## Alternatives and refuted paths

Closing #72 merely because the central registry or starter reference passes would
misrepresent actual component adoption. Reimplementing engine or adapter behavior in
MolSysSuite would violate component ownership. Both paths are excluded.

## Scope and exclusions

Governance admission, compatibility boundaries and issue-backed maintenance only.
Scientific implementation and diagnosis remain with OpenCASTp/TopoMT developers.
MolSysMT and MolSysViewer checks remain deferred and were not touched.

## Acceptance criteria

- Keep this dated adopted/partial/pending table and exact evidence, with an owning
  issue for each actionable gap.
- Verify the actual published bootstrap with the suite conformance and component
  reporting checks; reconcile registry reviews and README claims with that evidence.
- Record bounded, approved exceptions where needed rather than treating incubation
  as a waiver. The tracked owner-local coexistence exception above does not authorize deletion or waive other requirements.
- Preserve component-local follow-up ownership and independent API/adapter boundaries.
- Close after the published baseline and applicable hosted gate, including an approved
  bounded exception, can be checked and the handoff is complete; unresolved scientific
  work and permanent policy repair continue in their owning issues.

## Local implementation issues

uibcdf/opencastp#4 received the repository-baseline handoff, now verified in published source. Existing uibcdf/opencastp#1,
uibcdf/opencastp#2 and uibcdf/opencastp#3 retain their respective implementation scopes.
uibcdf/topomt#90 owns the consumer transition and cross-links uibcdf/topomt#63.

## Dependencies and risks

Active component work may be ahead of the inspected published snapshot. Reinspect
its new source before editing or claiming adoption. Pending scientific work does not
require all incubating CI lanes to pass before recording governance progress.

## Provenance

2026-10-02; Linux development workspace; Python 3.13.15. GitHub tree inspected at the
exact SHA using native read-only API calls. Reference generated using the inherited
`362d440` generator/template plus this central admission. All active worktrees preserved.

## Final checkpoint and resolution — 2026-10-02

The component team subsequently published `762db29693f030ac61baa423de0371993ad6a454`.
Its actual source passes component conformance, reporting/index validation, the
focused reporting test, Ruff (40 files), and four guide-byte comparisons. The
Python 3.14 authorization in central `a801b4a` and subsequent component-specific
admission in `2707ef9` are preserved. The component team records the installed
four-minor scientific evidence; no common baseline or other member state is changed
by this audit.

Hosted policy run [37058867837](https://github.com/uibcdf/opencastp/actions/runs/37058867837)
passes the mandatory deadline, exact immutable checker identity, conformance,
lint and format steps. Its published-policy job has no executed steps and is
skipped explicitly. The accepted bootstrap exception has an owning #3 issue,
2026-12-31 expiry and removal after a released admission-aware gate is qualified
under central #73. Green bootstrap does not mean adopted published policy.

The audit is complete: requirements have dated adopted/partial/pending/excepted
states, exact source/gate receipts, bounded exception conditions and owning
follow-ups. The listed guard preserves the conservative identity/review contract
and prevents unreviewed support/publication claims during admission. It does not
claim to protect or independently validate the scientific numerical engine.

OpenCASTp #1/#2/#3/#5 and TopoMT #90 remain the implementation owners. No
scientific bug is diagnosed or fixed centrally, no scientific suite is launched,
and no active component source checkout is modified by this audit.

### Preserved concurrent qualification

Central `2707ef9` subsequently archives #70 and admits the component-specific
3.14 transition from the team's installed/scientific lane evidence. This audit
retains that accepted state and its CI-review update. Current admission evidence
is not reverted to the earlier authorization/pending-CI snapshot. Broader
scientific validation, source rights, public distribution, coverage and permanent
published-policy repair retain their existing owning issues.

### Final promoted-source check — 2026-10-02

After member-specific admission, the older `762db29` snapshot retains its initial
three-minor badge and no longer represents current badge conformance. That is
historical evidence, not an instruction to reverse promotion. The team publishes
`6303af50318286476fac949015f9800e90c917ca` with the admitted four-minor badge and
bootstrap pin `2707ef9`. This actual promoted source passes current component
conformance, reporting/index and its focused regression, Ruff (42 files), four
guide-byte comparisons and the manifest graph. Native run
[37061097124](https://github.com/uibcdf/opencastp/actions/runs/37061097124) passes
the deadline, exact checker identity, conformance and Ruff steps; the old
published caller remains explicitly skipped. The bounded exception and #73
removal conditions are preserved. No scientific suite is rerun by this audit.

### Subsequent scientific ownership handoff — 2026-10-02

The live issue board also contains uibcdf/opencastp#6, "Establish complete measured
CASTp3 and CASTpFold equivalence". This new scientific proposal belongs to the
component developers. The governance audit records that owner-local follow-up;
it does not assess parity or implement the numerical work. Component #4 and #5
are already closed by the team for the baseline and Python 3.14 qualification.
