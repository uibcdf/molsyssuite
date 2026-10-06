---
summary: Track exact-file delivery and consumer impact of Ackredit CFF name fidelity.
issue: uibcdf/molsyssuite#103
status: partial
opened: 2026-10-05
closed:
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
consumer impact and a future exact-file delivery; source completion alone
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

Provider source and future delivery coordination. Ackredit owns implementation,
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
- Future release and consumer receiving owners remain to be identified from the
  actual selected delivery; no new member implementation is prescribed now.

## Dependencies and risks

No next public candidate has been selected in the reviewed handoff. Public
0.10.1 does not gain this later correction from a successful source run.

## Provenance

2026-10-05, Linux, `molsyssuite@uibcdf_3.14`, Python 3.14.7, local editable
GH Run Receptor. Source and metadata administration only; existing shared
environment dependency conflicts remain deferred by the maintainer. Original
clones and package bytes are preserved. MOLI owns Recorda review separately
under uibcdf/moli#50; it is not a suite member or a consumer inferred here.
