---
summary: Adopt exact version-only GitHub Release titles and deliver the rule to every suite member.
issue: uibcdf/molsyssuite#119
status: active
opened: 2026-10-20
closed:
verification: inspected
area: [governance, releases, documentation]
guard:
normative: devguide/release_version_policy.md
blocked_by: []
supersedes: []
---

# Version-only GitHub Release titles

**Reported:** 2026-10-20 after comparing Sabueso and the registered suite releases.
**Status:** Maintainer decision accepted; canonical guidance and sixteen-member
instruction delivery are in progress. MOLI direct-component adoption is separate.

## What

Public component GitHub Release titles/names are exactly their canonical `X.Y.Z`
versions, matching the GitHub Release tag and package/project version. Project
names, prefixes, subtitles and comments belong outside the title. Descriptions
remain in the release body/notes. The maintainer explicitly accepted this rule
for MolSysSuite and MOLI and authorized both owning issues and suite delivery.

## How

Extend the normative release policy and canonical component guide, add the lasting
release-preparation action to root instructions and versioned starter materials,
and deliver the canonical guide through the registered synchronizer. All sixteen
members receive root `AGENTS.md` guidance plus a short local developer-guide entry
linked to the canonical rule. Preserve local instructions and unrelated work.
Notify existing owning governance reviews before rollout. MOLI #68 owns the
corresponding platform/direct-component guidance, including Sabueso.

## Why

GitHub's `name` and `tag_name` fields are independent. Sabueso 0.14.0 has a
descriptive name while retaining canonical tag 0.14.0. Recent suite releases use
bare versions, name+version and descriptive titles, including DepDigest 0.15.0.
The existing parser governs tag/package identities but not the visible title.
The accepted rule gives the release list one consistent, concise format.

## What is measured and what is assumed

The current `suite.toml` inventory and normative release policy match central
remote main. Read-only GitHub CLI queries inspected up to three current releases
for each of sixteen members and twelve Sabueso releases. Sabueso remains directly
MOLI-governed. A release title is not a package version or artifact identity.
Instruction delivery does not certify a later release or historical title edits.

## Alternatives and refuted paths

- Name+version repeats repository context; the maintainer selected version only.
- Descriptive titles preserve multiple presentation styles; descriptions fit in
  the existing body/notes field.
- Retagging or rebuilding changes identities unrelated to this presentation rule.
- Updating frozen policy tags/callers is unnecessary for this documentary action;
  their machine checks do not acquire or validate GitHub's separate title field.

## Scope and exclusions

All sixteen current registered components, including incubating/auxiliary members
and the MolSys-AI subsystem, plus future Python starters. Existing separately
governed policy-release/archive namespaces retain their meanings. This delivery
does not change release metadata, package dependencies, scientific code, artifacts,
caller pins or scientific/full-suite debt. Historical metadata remains owner work.

## Acceptance criteria

- Publish the normative rule, canonical summary, central root action and starter.
- Deliver byte-identical guide copies and root AGENTS/local devguide actions to
  every registered member, retaining immutable sources and owning notices.
- Execute applicable documentary/governance checks and inspect exact-head hosted
  administrative gates or retain a precise recovery owner.
- Record MOLI #68 as its separate platform/direct-component implementation home.

The normative release policy is the closure guard for the accepted instruction.
Scientific suites and a new common API/mandatory network gate are not introduced.

## Local implementation issues

Platform/direct-component adoption: uibcdf/moli#68. Member notices use existing
registered governance review homes; no duplicate component proposal is needed
for this centrally accepted instruction delivery.

## Dependencies and risks

An instruction cannot retroactively certify title compliance or qualify releases.
The existing documented bounded exception mechanism applies. Preserve concurrent
owner commits and uncommitted work; use isolated delivery clones when necessary.

## Provenance

2026-10-20, Linux, named `molsyssuite@uibcdf_3.14` Python 3.14.7. Read-only
suite-status acquisition precedes cross-repository work. Receptor editable origins
are verified; existing shared-workspace dependency findings remain visible and
the environment is preserved. Exact delivery and administrative receipts follow
under `devguide/rollouts/` before closeout.

## Advance handoff and local checks — 2026-10-20

All sixteen registered members have received an actionable advance notice in
their existing owning governance reviews. The
[delivery receipt](../rollouts/release_title_instruction_delivery_119_20261020.json)
records their original remote sources, notice links and separate pending delivery
states. Root/canonical policy and future starter instructions are prepared;
offline governance, whitespace and thirteen existing instruction/starter tests
with twelve subtests pass in the named Python environment. No scientific test,
release title edit or runtime environment change was performed.
