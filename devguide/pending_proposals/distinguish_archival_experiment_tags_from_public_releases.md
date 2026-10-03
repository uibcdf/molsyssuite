---
summary: Distinguish archival experiment tags from public component releases.
issue: uibcdf/molsyssuite#84
status: open
opened: 2026-10-03
closed:
verification: measured
area: [governance, releases]
guard:
normative:
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

The maintainer requested an explanation on 2026-10-03. Approval of the namespace
is pending. The existing tag is neither deleted nor moved. Published
`policy-v1.5.4` remains immutable; its failed result is retained. A later policy
release and caller rollout are needed if the shared rule changes. No scientific
code, scientific tests or public package release is involved.

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
