# Release and package-publication notices

## Applicability and ownership

Accepted by Diego on 2026-10-23 under uibcdf/molsyssuite#129, this rule applies
prospectively to every registered member, including auxiliary, incubating and
subsystem repositories when they release a component or publish a package.

| Releasing or publishing repository | Required central notice |
| --- | --- |
| Member registered in MolSysSuite | `uibcdf/molsyssuite` |
| MolI component outside MolSysSuite membership | `uibcdf/moli`, through the separately owned uibcdf/moli#75 adoption |

MolSysSuite itself is a MolI component at the platform boundary. Its internal
`policy-vX.Y.Z` snapshots keep their own policy-release process; they do not
become component package releases. Historical `archive/` preservation tags and
ordinary development tags are not releases merely because they exist.

## Required events and timing

Open a **release-specific central GitHub issue** whenever the component:

- makes a new release, including a declared source/tag-only release or a
  GitHub Release with no published installable package;
- publishes a new package version, build or distribution route, even without
  a new GitHub Release. Identify staging and public channels separately.

The release owner records the event as part of its release/publication closeout,
as soon as its actual outcome is known. Do not wait for every later artifact
before reporting an already completed source release. If that component/version
already has a central release-notice issue, update it with each later package,
build or channel event and its evidence rather than opening a duplicate.
An existing central release-specific issue qualifies only if it carries the
required event information; a generic umbrella or an unrelated provider issue
alone does not. Link the local owning release/publication issue.

A failed publication attempt is not a published package. Retain its failure and
pending state in the owning work and any existing notice. This rule does not
require retrospective notices for every historical version; an older delivery
needed by current coordination may be reported with its original dated evidence.

## Minimum notice

Use [the notice template](templates/release_notice.md). Include:

1. Component repository, local owning issue, event kind/date and exact version.
2. Immutable source commit, tag target and release URL when present. State
   explicitly when the release has no published package.
3. For actual packages: channel/index and label, subdirectory/platform, exact
   filename/version/build, SHA-256, producer and public/installed verification
   receipts with their source, platform/minor scope, result and limits. Mark
   unavailable evidence pending; do not turn an upload into a public-install
   or compatibility claim.
4. Relevant old/new dependency contracts, source pins, generated/vendored guides,
   ecosystem packages and known consumers; distinguish observed impact from
   candidates or unknowns. Name the follow-up owner or a reviewed not-applicable
   disposition. A notice is required even when no consumer impact is known.

The central team triages the reported facts, cross-links ongoing work and tracks
the applicable tag/pin, constraint, guide, package and consumer-receiving updates.
Those are separately reviewed actions, not automatic consequences of the notice.
Closing a notification requires recording that disposition and any remaining
owning issues; it does not certify unrelated scientific or future-release scope.

## Relationship to other release controls

This is a reporting obligation, **not a new central permission gate** before a
component release. The component retains its release authority, existing exact
candidate/artifact gates and immutable tags/files. Reporting never authorizes
moving a published tag, replacing a package, selecting new dependency floors,
updating consumer pins or rerunning science automatically.

The separate [shared-provider impact notice](cross_component_feedback.md#shared-provider-changes-and-consumer-impact)
remains due **before** publication/rollout when impact is foreseeable. A release
notice can link that issue but cannot replace its advance timing or affected-owner
handoffs. Cross-link a MolI issue when distinct platform/direct-component work is
also required; membership routing does not require duplicating every notice.

## Instructions, delivery and exceptions

Each member's root `AGENTS.md` explicitly states this release/publication action
and routes to `MOLSYSSUITE_GUIDE.md#release-and-package-publication-notices`.
The canonical guide and versioned starter carry the same route. Distribute guide
copies only through the registered synchronizer. Instruction/guide checks prove
delivery and routing, not that a future event has been reported or qualified.

A bounded exception records the affected repository/event, owning issue,
responsible maintainer, reason, interim reporting route, review/expiry date and
removal condition. A missing credential or inaccessible issue tracker requires
an owned maintainer handoff; it does not silently waive the notice. Use private
reporting for confidential or exploitable details and publish only an authorized
sanitized coordination record. Never put credentials in the notice.
