# GitHub Discussions for MolSysSuite components

Accepted under uibcdf/molsyssuite#120 for MolSysSuite and every registered member,
including incubating, auxiliary and governed-subsystem repositories. This adopts
the platform baseline in [MolI #23](https://github.com/uibcdf/moli/issues/23) and
its [published policy](https://github.com/uibcdf/moli/blob/5ad9aea3e55e943fea82b0e0365c0648fd7d6783/devguide/governance/github_discussions.md).
The suite owns member policy, future-repository guidance and measured adoption.

## Activation, purpose and ownership

Enable Discussions during onboarding and retain it even when activity is low.
Use the repository that owns the subject: member-specific usage stays with that
member, shared suite questions with MolSysSuite, platform-wide questions with
MolI. Link an existing thread rather than starting parallel conversations.

The repository's maintainers own triage until they delegate it to a named
maintainer or maintained team. Missing delegation is work to assign, not an
exemption from activation. There is no response-time promise. Record category
purpose, accountable owner and durable destination; the defaults below apply
to the common categories. Record purposeful local extensions in owner guidance.

## Common categories and local extensions

| Name / slug | GitHub format | Purpose and durable destination |
| --- | --- | --- |
| Announcements / `announcements` | Announcement | Maintainer updates linking an already recorded release, contract or policy. The owning release/decision record remains authoritative. |
| Q&A / `q-a` | Question and answer | Usage and interpretation questions. Mark useful answers; route actionable findings to owning issues and lasting clarifications to maintained documentation. |
| Ideas / `ideas` | Open-ended discussion | Early conversations without concrete actionable work. Once work is actionable, use an owning issue; record decisions in that issue or a named versioned record. |

Keep all three even when empty. Adapt descriptions, examples and forms to the
component without changing the common names, slugs or formats. Extra categories
need a purpose, owner and destination. An additional intake category also needs
a form and documented disposition/conversion rules. Existing specialized
categories are reviewed locally, not silently deleted by central rollout.

Retire unused defaults such as General, Polls and Show and tell only after
checking their contents and preserving useful threads, decisions and links in
an appropriate destination. Preserve discussion history and stable references;
configuration conformity is no reason to delete conversations.

## From a thread to durable work

Actionable suspected defects, missing capabilities and concrete improvements
belong in owning issues even when uncertain or nonblocking. Ideas must not
become a queue bypassing [the reporting duty](reporting_protocol.md).

At triage or conclusion, find/open/update the owning issue or versioned record.
Record accepted/deferred/rejected decisions with date and reason, and a concrete
revisit trigger for deferral. Link the original thread from the durable record
and the destination back from the thread. Mark answered or close when useful,
explaining the disposition. A short usage answer needs no new issue unless it
exposes actionable work or a lasting change. A discussion, vote or closure alone
does not accept a shared contract or prove implementation.

Keep public discussions within the same disclosure limits as public issues.
Use sanitized examples and private reporting where required. Reading or
summarizing a thread does not authorize posting, subscriptions, disclosure,
notifications, runtime integration or scientific implementation. Existing task
authorization and the normal owner review/release routes remain applicable.

## Observation, adoption and exceptions

Keep desired policy, published contributor guidance and observed GitHub settings
separate. Record the repository, observer/date, activation, common category
names/slugs/descriptions, Q&A answerability, actual formats, content-preservation
review, local owner/extensions and any form rendering. Name presence alone does
not establish format. An API readback cannot certify UI-only settings.

The maintained rollout inventory names each member's receiving state and owning
follow-up. An immutable central source commit identifies this published policy;
no network-dependent Python gate, mandatory new manifest schema or blanket
Python caller upgrade is introduced. Source checks do not configure GitHub.

An inaccessible API/editor or justified special condition needs a bounded
owner issue with affected setting/scope, reason, responsible maintainer,
interim communication route, review/expiry and removal condition. The inventory
retains missing evidence as pending/excepted, never as verified. Incubating
status or empty categories alone are not exemptions.
