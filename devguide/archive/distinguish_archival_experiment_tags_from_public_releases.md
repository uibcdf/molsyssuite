---
summary: Distinguish archival experiment tags from public component releases.
issue: uibcdf/molsyssuite#84
status: resolved
opened: 2026-10-03
closed: 2026-10-04
verification: measured
area: [governance, releases]
guard: tests/test_governance.py::RepositoryConformanceTests::test_archival_tag_is_preserved_and_accepted_with_capable_gate
normative: devguide/release_version_policy.md
blocked_by: []
supersedes: []
---

# Archival experiment tags and public releases

## What

The published component checker enumerates all Git tags and treats every
noncanonical tag outside the historical inventory as an invalid public release.
MolSysMT policy-v1.5.4 run [37122589266](https://github.com/uibcdf/molsysmt/actions/runs/37122589266)
fails `RELEASE_TAG` for `archive/rust-c1-spike-20261002`.

The annotated tag object `6456293bb980e32b15b885c5b38a344af4cafd03` points to
`87317ba766e8d99e6b5129e25eebb83ffb089c0d`. Diego Prada created it on
2026-10-02 with the message: “Preserve the nonproduction Rust C1 packaging
experiment before branch retirement”. The active Interactions implementation
record explicitly requests preserving that tip before deleting its unmerged
experiment branch. This is archive intent, not an installable-version claim.

## How

Propose a reserved `archive/` tag namespace with no publication meaning. Public
release tags, package versions and GitHub Release versions retain canonical
`X.Y.Z`. Inspect existing public publisher triggers and version parsers before
adding an exemption: an archive tag must not trigger public package publication,
create release-version evidence or bypass an actual public-release check.

The existing reusable operation is the release-tag check in
`devtools/scripts/check_repository.py`; any accepted extension belongs there
and in the shared release policy, with focused regression tests. Component
publishers retain their own applicability and exact-candidate gates.

## Why

Branch retirement can preserve experimental history without presenting it as
a production release. Rejecting all archival markers conflates two uses of Git
tags; ignoring all noncanonical tags would weaken the public-version contract.
The proposal applies to registered repositories and requires a defined namespace
and publication boundary rather than a MolSysMT-only silent bypass.

## Decision and scope

The maintainer requested an explanation on 2026-10-03 and accepted the reserved
namespace on 2026-10-04. This work neither deletes nor moves the existing tag; the refreshed remote later shows it absent. Published
`policy-v1.5.4` remains immutable; its failed result is retained. The new immutable policy
release and caller rollout described below implement the accepted rule. No scientific
code, scientific tests or public package release is involved.

The accepted implementation is published as `policy-v1.5.7`: the repository
checker accepts only the reserved nonempty `archive/` prefix as archive identity,
retains exact public/metadata version checks and requires a capable caller where
archive tags exist. The common guide states its purpose/owner record and explicit
nonpublication meaning. Other members retain compatible callers, including
Ackredit's admitted 1.5.6 snapshot; no universal caller migration is required.

The trigger review found `tags: ["*"]` in the starter and MolSysMT. GitHub's
documented wildcard semantics exclude `/` for `*`; `**` includes it. The starter
now uses `**`, and `ARCHIVE_TAG_TRIGGER` validates an unconditional capable
caller covering all tag pushes. This extends the existing CI inventory's reusable
workflow reader instead of introducing another parser or Action. The new reusable
policy workflow installs its administrative PyYAML dependency before conformance.
MolSysMT's caller/trigger rollout and sixteen canonical guide copies follow the
published immutable snapshot. No archival tag needs to be recreated.

The new preservation regression failed on the original checker with exactly
`RELEASE_TAG`, before the fix; it passes afterward and verifies the temporary fixture
annotated tag object is unchanged. Negative checks retain other invalid Git tags,
reject archived project versions, older/filtered/conditional callers and archive
publication plans before acquiring source gates or registry permission.

The maintainer also requested evaluating the rule at MOLI. The linked platform
proposal uibcdf/moli#47 delivers the accepted suite rule, implementation/evidence
and remaining platform decision, preserving independent governance authority.

## Acceptance criteria

- Decide whether archival tags are an accepted shared capability.
- Define their namespace and explicit nonpublication semantics.
- Protect public `X.Y.Z` validation and archive/public trigger separation with
  regression tests that reproduce the observed checker failure.
- Publish any changed shared policy as a new immutable release, then inspect
  exact-source component conformance and relevant publisher guards.

## Provenance

Inspected the native failed job, GitHub annotated-tag API and MolSysMT's active
implementation record on 2026-10-03. Python 3.14.7 runs the hosted policy gate.
The failure precedes Ruff and does not diagnose scientific compatibility.

## Current reference and publication review — 2026-10-04

The refreshed remote query for MolSysMT archive refs returns no entries. Its
original failed run/tag object/experiment commit remain historical evidence;
this work does not recreate or move a reference. Its current source conforms
before rollout because no archive tag is fetched. The new caller/trigger will
prepare future use, while the real annotated Git fixture proves classification
and preservation independently. No actual tag-push event is manufactured.

Publisher evidence is retained in `devguide/rollouts/archive_tags_84.json`.
The review derives seventeen repository rows from the maintained owning
publisher inventory operation and rechecks committed Conda calls at fetched
heads. Publication wrappers do not subscribe to tag pushes. Local shell guards
reject archive release names and accept a canonical control in temporary Git
fixtures; shared frozen validators reject archive plans. MolSysSuite itself
remains blocked by missing reviewed plans under #67; that failure is not
archive-specific public qualification. No publisher pin or release route is
changed. Other distribution routes remain owner-reviewed before enabling the
capability; a Conda inventory is not a certificate for every publication route.


## Resolution and delivery — 2026-10-04

`policy-v1.5.7` is published at
`f1ae1a043720e33493024d8afcab1e45375e42a2`; its annotated tag object is
`0f89d1cb94e131f438673a8525f270ee05e9da48`. Previous policy tags remain
unchanged. The native central governance run
[37207648859](https://github.com/uibcdf/molsyssuite/actions/runs/37207648859)
and named Linux/Python 3.14 development workspace run
[37207648757](https://github.com/uibcdf/molsyssuite/actions/runs/37207648757)
pass on that exact source. All 308 local administrative tests passed.

The official guide synchronizer distributed and verified all sixteen copies.
The primary receipt records each immutable delivery commit and the guide digest.
The initial guide audits correctly failed before distribution; the native
component-guide audit
[37208088175](https://github.com/uibcdf/molsyssuite/actions/runs/37208088175)
and global vendored-guide audit
[37208088164](https://github.com/uibcdf/molsyssuite/actions/runs/37208088164)
both pass on attempt 2, preserving the initial history.

MolSysMT adopts the capable caller and all-tag filter at
`1945498ff1caf36be14d3b8a364fa02482b042d6`. Its explicitly dispatched
administrative policy run
[37208585357](https://github.com/uibcdf/molsysmt/actions/runs/37208585357)
passes on that exact commit, including parser installation, conformance and
full-tree Ruff checks. No scientific suite was dispatched. The caller inventory
passes with one current feature adopter and fourteen compatible callers
(Ackredit at 1.5.6, thirteen at 1.5.4). The feature is available without forcing
those repositories to migrate immediately.

Guard relevance: the named real annotated Git regression reproduced the
specific `RELEASE_TAG` failure before the fix; after the fix it checks accepted
classification and unchanged fixture tag identity. Its negative companions
exercise unsupported/filtered callers and retain unrelated invalid-tag failures.
The normative release policy protects the archive/public meaning separately
from actual scientific or installed-artifact qualification. Current MolSysMT
archive refs are absent, so this is configuration and fixture evidence for
future use, not a newly manufactured remote tag event.

The maintainer's requested platform escalation is recorded in
[uibcdf/moli#47](https://github.com/uibcdf/moli/issues/47). MOLI's applicability,
implementation and adoption decision remain independent; they do not block
the completed suite policy or duplicate its member governance. The receipt
`devguide/rollouts/archive_tags_84.json` holds publisher review, notices,
immutable publication/delivery identities, native evidence and limits.
