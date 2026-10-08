---
summary: Track exact-file delivery and consumer impact of Ackredit CFF name fidelity.
issue: uibcdf/molsyssuite#103
status: resolved
opened: 2026-10-05
closed: 2026-10-08
verification: measured
area: [governance, compatibility, provenance, distribution]
guard:
normative: devguide/cross_component_feedback.md
blocked_by: []
supersedes: []
---

# Ackredit CFF name delivery

## What

Ackredit's CFF parser and CSL exporter previously lost explicit entity/person
identity, including names containing commas, single-component names, suffixes
and particles. The provider resolves uibcdf/ackredit#98 at immutable source
`46b2635b17f47e03e18ab576016ace94b7e6461b`. MolSysSuite #103 coordinates
consumer impact and exact-file delivery; source completion alone
does not complete that delivery.

## How

The provider preserves bounded original author/editor metadata alongside existing
human-readable strings. Export uses those hints only while they still match
the current list; explicit replacements and typed preferred-work ownership
remain authoritative. Identifiers remain saved metadata. No new dependency,
portable schema identifier or mandatory client minimum is introduced.

## Why

CFF name identity can reach exported citations used by suite components. The
registered Ackredit guide clients are PyUnitWizard, MolSysMT, MolSysViewer,
TopoMT, PharmacophoreMT and ElastNetMT; actual use of affected CFF cases is
unknown. Sabueso is a separate MOLI consumer. Candidate consumers, notice,
adoption and installed/public evidence must remain distinct.

## What is measured and what is assumed

On 2026-10-05, central read-only source inspection verifies four runtime hashes
and the 22-case regression module against the provider's committed receipt.
That receipt reports normal installed baseline failures (17 failed, five passed)
and candidate success (22 passed), plus 1,815 local source tests passing.
Those owner-local results were inspected, not rerun centrally; its development
candidate is bound to the delivered files, without claiming a release version.

Local editable GH Run Receptor reads existing CI 37301497881 at the delivered
source: seven successful jobs, including executed successful test steps on
Linux Python 3.11–3.14 and macOS Python 3.14. Metadata does not establish
an eight-cell installed release matrix or the local counts above. The selected
owner guard follows discovery/capture through producer-free, network-blocked
saved CSL reading; its assertions directly preserve entity/person and suffix
identity. Central source-hash comparison binds that guard to the repaired files.

Primary receipt: `devguide/rollouts/ackredit_cff_source_review_103_20261005.json`.
The previously verified public 0.10.1 file remains a separate historical
checkpoint in `devguide/rollouts/ackredit_011_public_pipeline_92_97_20261005.json`.

## Alternatives and refuted paths

Punctuation guessing cannot recover identity already supplied by CFF. An
original-name hint cannot override an explicit list replacement. Do not infer
CSL particle dropping semantics or unsupported identifier fields. No further
implementation alternative is decided centrally.

## Scope and exclusions

Provider source and existing delivery coordination. Ackredit owns implementation,
release selection and exact-candidate qualification. PyUnitWizard #111 and the
provisional observation/evidence APIs under MolSysSuite #97 remain independent.
No client source, guide rollout, dependency migration, package publication or
component test dispatch is performed here.

## Acceptance criteria

- Preserve the baseline, repaired source, relevant guard and source evidence.
- Record the future owner's selected version/commit/file/digest and executed
  required installed qualification before asserting public delivery.
- Deliver actionable release/compatibility notices to affected owning consumer
  issues from the registered inventories; retain unknown actual CFF use and
  owner receiving review/adoption/deferral separately.
- Reconcile these declared outcomes under the normative shared-provider notice
  rule before closing central coordination.

## Local implementation issues

- uibcdf/ackredit#98: resolved source correction and owner regression guard.
- uibcdf/ackredit#107 and uibcdf/ackredit#127: delivered exact public releases.
- Consumer notice/receiving owners are recorded in the resolution below.

## Dependencies and risks

The initial source-only handoff had no selected public candidate. Public 0.10.1
does not gain this later correction from a successful source run. The qualified
additive deliveries below retain new file coordinates and original bytes.

## Provenance

2026-10-05, Linux, `molsyssuite@uibcdf_3.14`, Python 3.14.7, local editable
GH Run Receptor. Source and metadata administration only; existing shared
environment dependency conflicts remain deferred by the maintainer. Original
clones and package bytes are preserved. MOLI owns Recorda review separately
under uibcdf/moli#50; it is not a suite member or a consumer inferred here.

## Resolution — 2026-10-08

The provider's first corrected public delivery is Ackredit **0.11.0**,
`ackredit-0.11.0-py_0.tar.bz2`, source
`85deae594e65b2fd443d6ca9a7347eb2bda537e1`, SHA-256
`df8963ca2d286f50b19eb778e95c54c5ebb79c12fb55a6504e7c23daf5717d4f`.
Central independent review verifies its original producer native receipt ZIP/digest,
all four required original source gates, eight complete installed cells in
[37429662858](https://github.com/uibcdf/ackredit/actions/runs/37429662858),
public main label/solver index and actual downloaded file digest. Its four repaired
runtime files and original CFF regression module are byte-identical to the fix.
Source-to-shipped hashes match. Original promotion receipt and native artifact
[37430816845](https://github.com/uibcdf/ackredit/actions/runs/37430816845)
verify staging-to-main promotion of these same bytes.

Ackredit subsequently delivered **0.12.0** under uibcdf/ackredit#127:
`ackredit-0.12.0-py_0.tar.bz2`, source
`6f4dbf39996a7185b8aaff7c52b9daeb167a100a`, SHA-256
`160b452c2b9de3b44bc6c6e2f4bd8c47e44b1d2779b620f63048231708a1d4aa`.
The same bounded independent review verifies original producer receipts, four
required source gates, eight installed cells in
[37588182382](https://github.com/uibcdf/ackredit/actions/runs/37588182382),
public availability/download digest, shipped source hashes and same-byte
[promotion 37599450602](https://github.com/uibcdf/ackredit/actions/runs/37599450602).
The original CFF regression module is unchanged; name/CSL exporters have later
bibliographic repairs and are bound to this candidate, not falsely described as
byte-identical to the original fix. Both installed contracts select all `tests`
without a CFF exclusion and execute the required installed/provenance steps.
The full-source dispatch omits only its auxiliary backlog detector; all eight
required test jobs execute. Other source gates verify exact job inventories.
Windows is outside these existing owner claims.

The public checks use the existing read-only shared release operator and archive
inspector. No package construction, upload, promotion, scientific suite or new
qualification dispatch occurs. Owner-reported real PyUnitWizard receiving
(72 mandatory tests/eight cells without skips) and clean public runtime outcomes
remain separately attributed; this central review does not repeat them or
certify every guide client's runtime.

The impact issue is updated and all six registered guide clients receive an
exact-version/source/file/digest handoff through their existing owning issues:

| Consumer | Notice / owner route | Receiving disposition |
| --- | --- | --- |
| uibcdf/pyunitwizard | [uibcdf/pyunitwizard#94](https://github.com/uibcdf/pyunitwizard/issues/94#issuecomment-6057607953) | Notice delivered; actual affected CFF use/adoption remains owner-reviewed. |
| uibcdf/molsysmt | [uibcdf/molsysmt#292](https://github.com/uibcdf/molsysmt/issues/292#issuecomment-6057608494) | Notice delivered; actual affected CFF use/adoption remains owner-reviewed. |
| uibcdf/molsysviewer | [uibcdf/molsysviewer#152](https://github.com/uibcdf/molsysviewer/issues/152#issuecomment-6057608910) | Notice delivered; actual affected CFF use/adoption remains owner-reviewed. |
| uibcdf/topomt | [uibcdf/topomt#94](https://github.com/uibcdf/topomt/issues/94#issuecomment-6057609335) | Notice delivered; actual affected CFF use/adoption remains owner-reviewed. |
| uibcdf/pharmacophoremt | [uibcdf/pharmacophoremt#19](https://github.com/uibcdf/pharmacophoremt/issues/19#issuecomment-6057609824) | Notice delivered; actual affected CFF use/adoption remains owner-reviewed. |
| uibcdf/elastnetmt | [uibcdf/elastnetmt#20](https://github.com/uibcdf/elastnetmt/issues/20#issuecomment-6057610331) | Notice delivered; actual affected CFF use/adoption remains owner-reviewed. |

The list derives from registered guide consumers, cross-checked against the
maintained dependency graph and immutable current source snapshots. Only the
guide relationship is established for Viewer/TopoMT/ElastNetMT here. Existing
closed attribution/guide outcomes are preserved; notices do not reopen them or
claim current runtime adoption. Concrete receiving defects or future migrations
belong to consumer-owned issues linked to this record. Active MolSysMT #292 and
PharmacophoreMT #19 retain their runtime adoption ownership. Unknown actual
CFF use, future review and tested provider artifacts remain separate states.

This completes #103's declared exact-file delivery and consumer-impact notice
coordination. It does not mandate a client upgrade, new minimum, guide rollout
or scientific full suite, or certify the broader 0.12.0 contracts. Those remain
under provider #127, central #97 and consumer owners. Notices recommend reviewing
the current public release when selecting an upgrade; 0.11.0 records first
corrected delivery rather than a downgrade instruction. No portable schema or
shared policy is changed. The enduring handoff/ownership guard is the normative
`devguide/cross_component_feedback.md` rule.

Full identities, source/shipped hashes, executed gates, original native artifact
digests, notices and limitations:
[ackredit_cff_delivery_103_20261008.json](../rollouts/ackredit_cff_delivery_103_20261008.json).
The historical source receipt remains intact. Caller environment and original
clones are preserved; task-owned source/archive fixtures are removed at closeout.
