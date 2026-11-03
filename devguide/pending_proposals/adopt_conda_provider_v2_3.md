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

## Acceptance and next action

- Shared source, immutable release and applicable original qualifications reviewed.
- Current registry-derived consumers identified and central pins/contracts checked.
- Deliver the exact central commit, compatibility notes and checks to member owner
  issues and MolI #42. Record notice separately from acceptance.
- Receive explicit **Review completed** responses with source, affected scopes,
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
