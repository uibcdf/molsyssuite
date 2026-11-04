---
summary: Adopt the reviewed Conda v2.3.0 provider without coupling source delivery to publication.
issue: uibcdf/molsyssuite#87
status: partial
opened: 2026-10-03
closed:
verification: measured
area: [governance, distribution, compatibility]
guard: tests/test_conda_release_contract.py
normative: devguide/noarch_conda_workflow.md
blocked_by: []
supersedes: []
---

# Conda provider v2.3.0 adoption

**Reported:** Provider release 2026-10-03; human resumed adoption 2026-11-03.
**Status:** Partial. Shared source is reviewed and updated; component adoption
and owner confirmations remain separate work.

## DockingMT owner receiving and original central CI — 2026-11-04

The explicit owner completion in DockingMT #47 / central #87 is now received.
At published `8dbcab39f2b2a5defde25309146a747826e3d62a`, build/exact-upload,
promotion and publication-governance wrappers change only their full central
reference to `95f693be10c9205ab9b912cb53453710a207bf45`. Ten manifest records
and six shared file hashes match; triggers, inputs, permissions and secret
mappings remain identical. The initial installed helper retained `2d320484`.

That initial retention is now historical: the later owner-completed private
whole-suite/support receiving at `ea9b30256799112313b91d12467448aae1e526d9`
also adopts the delivered installed helper, changing only its central reference.
Nine installed-support manifest records and the three actual shared support
implementation hashes bind. The owner reports 1,450 installed cases, distinct
test/helper source `3bf7abf5` and original wheel producer `50d8e33f`; all private
execution/payload/process outcomes remain owner-produced evidence, not centrally
rerun or independently downloaded private artifacts. The later `07fc2692`
source-mapping repair preserves the original full receipt/manifest bytes; its
record hashes bind. This does not qualify a staged Conda file, public dependency
closure, another platform/minor or an actual release. The SDK stays `738fe8dd`.

The current fetched publisher and installed-wrapper bytes match these adopted
wrappers. Only DockingMT's publisher inventory row is refreshed; the explicit
partial-refresh note preserves other rows' older observations. No other owner
adoption is inferred. [Receiving/source/limits](../rollouts/dockingmt_conda_adoption_87_20261104.json).

Reporting limit: initial handoff/readiness prose says 29 administrative tests,
while its bound control JSON says 34. Both remain unreconciled owner-reported
totals; no raw administrative test log/JUnit was acquired and no count is
accepted centrally. The discrepancy is nonblocking for the exact reference-only
source proof and stays with the owner; no new scientific run is requested.

Original central source CI is independently accepted: run `41739439697`, exact
`95f693be10c9205ab9b912cb53453710a207bf45`, push/attempt 1, passes both jobs and
all required steps after GHR/stable native verification. Its bound log records
564 central unittest cases and 27 Conda contract tests as ok.
[Native proof](../rollouts/conda_provider_native_87_20261104.json).
This supersedes the earlier queued observation, not later-head CI, Codecov
processing or component publication/installed/scientific gates.

This DockingMT receiving and central source CI slice is complete. #87 remains
partial for other owner confirmations; their implementations, releases and
qualification stay with component teams. No member code, scientific tests,
environment, package, credential or withdrawal operation is changed here.

## What and why

Consolidate the separately repaired build and exact-upload operations and the
older promotion operation on immutable provider
`87c70b1443d5f22d738ee3ddf812bdbe0152f6c2` (v2.3.0). The original deferral is
superseded by the new human instruction for this adoption only. Withdrawal is
outside scope. Coordinate platform-direct consumers through uibcdf/moli#42.

## Reviewed operations

| Operation | Previous shared source | Review and applicable limit |
| --- | --- | --- |
| Build without upload | `8da628d9b393e184c3bf3722708b19dcfbf7ef0a` | Active Conda executable correction retained. Conversion rejects `.conda` before conversion/removal. Shared noarch remains host-only, `upload: false`, no conversion, `.tar.bz2`. |
| Exact upload | `1aa2011f902a1a9d533564572245bb29f6862e86` | Execution script identical; action change is author metadata. Login shell, sealed bytes, coordinate absence, original candidate/digest, single unforced write and bounded receipts retained. |
| Promotion | `8a1f203c2cfe51acd63de7452117b4b6e9d609f4` | Shared typed-coordinate/label validation rejects incomplete, duplicate or contradictory inventories. Inputs pass through environment variables; exact digest, installed gate, staging/main and independent public verification retained. |
| Central combined metapackages | `8a1f203c2cfe51acd63de7452117b4b6e9d609f4` | Same reviewed build implementation; no conversion or force. This source update does not resume #67 or supply its missing plans. |

All six central operation bindings accept the existing inputs and outputs. No
workflow trigger, secret mapping, gate, science matrix, receipt identity or
release authorization changes. `mambabuild` and `overwrite` remain deprecated
v2 compatibility inputs; omit unneeded inputs and do not replace overwrite with
force. Removing them in v3 requires a separate provider adoption. Conversion is
not native cross-compilation. Native/ABI3/local publication profiles require
their owners' operation-specific review; they do not switch to noarch by this task.

## Measured evidence and limits

The [receipt](../rollouts/conda_provider_adoption_87_20261103.json) binds the public
tag, provider execution files, all six central bindings and complete successful
native inventories after actual GHR inspection:

- `37131330687`: final-source unit and Linux/Windows multiple-variant qualification.
- `37131330690`: final-source active named/base Conda environment qualification.
- `37131330794`: final-source offline upload/promotion/label contract tests in six
  hosted jobs. Its actual composite exercise is withdrawal, which is excluded
  from suite adoption; this is not a hosted promotion execution claim.
- `37131178734`: earlier `038915ba6768666eb6cca3605290128c7e277592`
  exact-upload composite, success/write-failure on Linux/macOS. All eight
  execution, fixture, workflow and test files are byte-identical at the target.

The relevant provider tests execute from an independent immutable copy with
Python 3.14.7 and an isolated tool venv; counts and versions are in the receipt.
Registry transports are offline fixtures. An exploratory full provider run also
encountered the excluded withdrawal composite's venv-launcher limitation; no
withdrawal acceptance or universal full-provider pass is claimed. The normal
shared prefix lacks the Anaconda client and is unchanged.

The central contract guard protects inspection before exact upload and installed
verification before promotion, exact candidate/digest binding and separate public
verification. Existing negative route/force/rebuild/gate tests remain relevant.
These administrative checks do not qualify a member's installed or scientific
behavior, publish packages or clear historical candidate failures.

## Consumer inventory and owner work

The refreshed [publisher inventory](../rollouts/conda_publishers.json) identifies
nine shared-noarch callers, five local member publishers and the central
combined publisher. Three members have no publisher observed. A recorded caller
may be suspended or historical; source classification does not certify readiness.
Published immutable component sources are inspected without updating or editing
their active local clones. TopoMT and PeptideMT worktree changes are preserved.

Teams own their caller updates and review confirmations. Shared-noarch consumers
pin the delivered **MolSysSuite commit**, not the external action SHA. Review
publish and promotion separately; keep installed/operator helper references and
component-specific gates compatible. Local publishers pin the external provider
only after reviewing their actual build/format/conversion/upload/evidence path.
Never retrofit an old producer receipt or rebuild an existing staged/public file
to make this adoption green. Any future release retains #78/#45 requirements.
Delivery destinations and resulting comments/issues are recorded in the receipt.
Published central source is `95f693be10c9205ab9b912cb53453710a207bf45`.
All fourteen advance and immutable-delivery notices are sent: SMonitor #58,
ArgDigest #45, DepDigest #46, PyUnitWizard #136, Pytest Receptor #50,
GH Run Receptor #80, MolSysMT #544, MolSysViewer #293, TopoMT #78,
PharmacophoreMT #10, ElastNetMT #18, DockingMT #47, Ackredit #139 and LinDelINT #19.
The four reused distribution routes are TopoMT, PharmacophoreMT,
ElastNetMT and DockingMT; the other ten have independent new owner issues.
All are open at delivery inspection. MolI #42 receives the same reviewed source
for its distinct direct consumers. No component adoption is inferred from notice.

Eighty-four central test nodes and 59 unittest subtests pass; the JUnit suite
counter includes both while it contains 84 testcase elements. Controlled
upload-before-inspection and promotion-before-installed mutations each fail the
new order guard. Ruff/format, offline governance and publication controls pass.
Original central source run `41739439697` is queued at observation; GHR and a
stable native snapshot bind its source/event/workflow/attempt, not executed success.

## Acceptance and next action

- [x] Shared source, immutable release and applicable original qualifications reviewed.
- [x] Current registry-derived consumers identified and central pins/contracts checked.
- [x] Exact central commit, compatibility notes and checks delivered to member owner
  issues and MolI #42; notice retained separately from acceptance.
- [ ] Receive explicit **Review completed** responses with source, affected scopes,
  adopted commit/evidence or justified owner deferral and reassessment trigger.

Keep #87 partial while component-owned applicable caller adoption/disposition is
pending. No forced release, full scientific suite per internal push, new maturity
deadline, package withdrawal or shared-environment replacement is required.

## Alternatives and provenance

A blind replacement in every active component clone would bypass owner-specific
profiles and active work. Keeping the old central pins would leave the resumed
adoption unimplemented. The selected route delivers the reviewed shared source
and explicit owner tasks. Host: Linux; routine named shared Python 3.14.7;
provider fixtures use a task-owned venv, not an updated routine environment.
