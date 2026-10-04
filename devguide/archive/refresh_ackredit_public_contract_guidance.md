---
summary: Reconcile public Ackredit portable-contract status and verify six published canonical guides.
issue: uibcdf/molsyssuite#96
status: resolved
opened: 2026-10-04
closed: 2026-10-04
verification: measured
area: [governance, compatibility, provenance]
guard:
normative: devguide/ackredit_client_policy.md
blocked_by: []
supersedes: []
---

# Refresh public Ackredit contract guidance

## What

Provider correction uibcdf/ackredit#83 identifies the already public portable
contract in Ackredit 0.9.0. Six consumer guide copies and the central provider
paragraph still described that delivery as pending. The original accepted
client and registration decisions in uibcdf/molsyssuite#68 and #71 remain intact.

## How

The six canonical copies were published during the #51 admission follow-up
through `sync_vendored_guides.py`, using clean isolated clones. This issue
reuses those exact commits rather than repeating delivery. The central client
policy now identifies the released `ackredit>=0.9.0` portable API floor,
`ackredit.attribution@1`, `Attribution`, `capture` and `get_attribution`, with
the existing public-file qualification receipt. It retains client-owned result
schemas, optional integration, dependency checks and actual adoption evidence.

## Why

A pending-provider paragraph could lead a consumer to maintain an obsolete
workaround or confuse public API availability with its own migration. Guide
receipt does not establish runtime adoption or require every member to install
Ackredit. This is a factual correction to an accepted profile.

## What is measured and what is assumed

Canonical change: `148ffb4b02285c8d7bcf94f50eeacc3fd1b2e2e8`; guide SHA-256
`dab9d96a897f0e229837ffeda2a7277029a344cace6530a79ac55e5a90d3e529`.
The official six-copy check passes at inspected provider head
`536bd87ec395cf8abfd18a14c4d24dc71ad88980`; that later development source does
not change the canonical guide or the public 0.9.0 file. Read-only GitHub
commit/contents queries also verify each recipient guide at its immutable
remote-main head against the canonical digest.

Primary recheck: `devguide/rollouts/ackredit_guide_public_status_96.json`.
Original delivery and notices: the `public_attribution_guide_delivery` section
of `devguide/rollouts/ackredit_python314_admission_51.json`. That receipt keeps
exact consumer commits, source identity and initial/final audit outcomes.
No receiving runtime or scientific qualification is inferred from these checks.

## Alternatives and refuted paths

Republishing unchanged consumer copies is unnecessary. Reopening #68 or #71
would confuse an accepted profile with this later factual refresh. Their
historical records retain their original claims; this dated record supplies
the subsequent public status.

## Scope and exclusions

PyUnitWizard, MolSysMT, MolSysViewer, TopoMT, PharmacophoreMT and ElastNetMT
receive the canonical text. Original working files, including unrelated dirty
clones, remain preserved. No runtime implementation, installation extra,
dependency change, scientific suite, new release or archive replacement occurs.
The provisional function-provider API in #97 is separate and absent from the
qualified public 0.9.0 package.

## Acceptance criteria and outcome

Canonical source/hash, six published recipient commits and notices are retained;
the official checker and independent remote-content comparisons pass. The
central outdated provider paragraph is corrected. The normative client policy
preserves deferred loading, explicit application opt-in, detached provenance,
exceptions and client qualification requirements. This completes #96.

## Local implementation issues

uibcdf/ackredit#83 owns the resolved provider documentation correction.
Recipient handoffs are uibcdf/pyunitwizard#92, uibcdf/molsysmt#292,
uibcdf/molsysviewer#152, uibcdf/topomt#94, uibcdf/pharmacophoremt#19 and
uibcdf/elastnetmt#20. The TopoMT published-copy notice also used its existing
ecosystem issue uibcdf/topomt#91; #94 receives the explicit closure handoff.
Those issues retain any separately owned runtime adoption scope.

## Dependencies and risks

Public provider delivery is already qualified. A later guide revision requires
a fresh registered synchronization; this checkpoint certifies only its recorded
bytes and heads. No prerequisite remains for this factual refresh.

## Provenance

2026-10-04, Linux; administrative reader Python 3.14.7. Commands and immutable
remote recipient identities are in the primary recheck receipt. Original
public package and installed qualification remain in the admission receipt.
