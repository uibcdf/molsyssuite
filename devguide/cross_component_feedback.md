# Cross-component feedback and shared stewardship

This document is normative for every MolSysSuite repository. All components are UIBCDF
team developments, so contributors share responsibility for improving the ecosystem,
not only the repository in which they happen to be working.

## The responsibility

When work in one component exposes a missing, limiting, unsafe, or unnecessarily costly
capability in another component, the contributor reports the need to the repository that
owns that capability. For example, a MolSysViewer developer who needs behavior that
SMonitor does not provide opens or updates a SMonitor issue with the consumer evidence.

Provider ownership determines where the change is decided and implemented. It does not
end the discovering contributor's responsibility to communicate what was learned.

## The handoff

The provider report includes:

- **What:** the capability or limitation observed from the consumer;
- **How:** a minimal reproduction, measurement, or concrete integration path;
- **Why:** user, scientific, maintenance, or operability impact;
- the consuming repository and local issue or report, when one exists;
- the required outcome or constraint, separated from a prescribed implementation.

The consumer cross-links the provider issue from any local workaround, blocked report,
test exemption, or follow-up. If several components need the same change or the decision
alters a shared contract, open a central `uibcdf/molsyssuite` issue as well and link the
provider implementation.

## Workarounds are temporary evidence

A local workaround may unblock development, but it does not replace the provider report.
Document why it exists, the owning issue, the condition for removal, and any behavioral
difference it introduces. Do not silently copy or fork a sibling's functionality into
the consumer.

## Triage is collaborative, delivery is prioritized

The provider maintainers acknowledge and triage the ecosystem need, verify ownership,
and state whether it is accepted, blocked, deferred, or out of scope. Filing an issue is
not an immediate delivery promise. Prioritization follows impact, release risk, and the
active initiatives in `suite.toml`; an incubating consumer may reveal a valid provider
improvement without causing it to preempt the current stabilization priorities.

If the request does not belong in the named provider, close or transfer it with an
explicit owner and stable cross-link. Do not let it disappear between repositories.

## Contributing a fix to another repository

Diego clarified the working routes on 2026-11-17:

| Destination | Working route |
| --- | --- |
| The repository currently owning the work | Commit and push directly through its normal internal-maintainer and CI route. |
| Another repository under `github.com/uibcdf` | Open or update its owning issue, or submit a concrete fix as a linked PR for owner review. |
| A third-party repository outside `github.com/uibcdf` | Obtain prior explicit permission before creating or publishing an issue or PR, including a remote draft. |

An internal UIBCDF issue or PR within the authorized task does not require an
extra publication-permission question merely because its destination is another
repository. Use an issue when there is no ready fix; use a PR for a reviewable
patch. The owning maintainers decide priority, review and integration. Do not
pause to ask for a direct-push exception to this ordinary issue/PR route.

Existing explicit authorization for the same work retains its scope. It does
not transfer ownership of another component, authorize merging its PR, or grant
third-party publication permission. Keep confidential findings on their private
reporting route. Retain provider and consumer issue links; a provider PR does
not replace a required shared-provider impact notice.

Policy deviations retain their documented owner, reason, controls, review/expiry
and removal condition. Ordinary authorized UIBCDF issues and PRs need no such
permission exception. Historical adoption is tracked in
[MolSysSuite #83](https://github.com/uibcdf/molsyssuite/issues/83) and
[MolI #41](https://github.com/uibcdf/moli/issues/41); their original dated records
remain history, while this maintained section carries the clarified route.

## Agents' external-publication authorization

Agents developing any MolSysSuite member must obtain prior explicit permission
from **Diego Prada Gracia** or **Liliana Marisol Moreno Vargas** before creating
or publishing an issue or pull request in a third-party repository outside
`https://github.com/uibcdf`. A remotely
created draft PR is an external write too. This accepted human instruction is
tracked in [MolSysSuite #159](https://github.com/uibcdf/molsyssuite/issues/159)
and [MolI #80](https://github.com/uibcdf/moli/issues/80); MolI owns platform-wide
adoption and MolSysSuite owns member guidance and distribution.

Investigate through read-only routes and prepare a reviewable local/internal
finding or patch. Identify the destination, proposed action and material to
disclose before asking one of those humans for permission. If permission is
absent, keep the report internal and hand it to the human, who may submit it.
The duty to report a finding is fulfilled through this authorized handoff while
external publication awaits permission; it is not an instruction to post anyway.

Existing explicit authorization for the same repository/action/content scope
persists without another permission round. Broader disclosure, another action
or a new destination requires its own authorization. Generic instructions to
report bugs, contribute or work autonomously, credentials, read access, working
with a principal maintainer and internal direct-push permission do not constitute
destination-specific external permission. Never bypass the boundary through
outside forks, other agents, accounts, tools or automation.

Internal UIBCDF issues and PRs within the authorized task need no extra
publication-permission round. Owner review and contribution rules still apply;
this grants no direct push or merge into another owner's repository. Read-only
research and local drafting remain possible. Confidential or exploitable details
retain their private reporting controls, including during the permission request.
No policy exception or ordinary feedback obligation substitutes for the required
human permission.

## Shared-provider changes and consumer impact

Every component release and package-publication event also follows the separate
[central event-notice rule](release_notifications.md), even without known impact.
That closeout notice does not replace the advance impact handoff defined below.

This rule applies when a developer or agent changes a shared auxiliary library,
reusable workflow, development/publication action or canonical integration guide
and a consumer effect is plausible. Examples include SMonitor, PyUnitWizard,
ArgDigest, DepDigest, Ackredit, Pytest Receptor, GH Run Receptor, the Conda
build/upload action and the Sphinx-to-Pages action. Public APIs, serialized
records, defaults, dependency or Python constraints, diagnostics, workflow
inputs/outputs and release behavior are relevant effects. Private implementation
changes without plausible consumer impact remain provider-local.

The provider retains its implementation, tests, issue and release ownership.
Open or update a linked MolSysSuite impact issue for adoption affecting suite
members. When direct MOLI components or a platform contract are affected, use
the MOLI route as well; when both domains have distinct work, cross-link one
issue in each. A single consumer-local finding stays in provider and consumer
issues until broader impact becomes plausible. This adopts the platform
[shared-provider notice rule](https://github.com/uibcdf/moli/blob/main/devguide/governance/cross_component_feedback.md#changes-to-shared-auxiliary-providers)
for suite members under the decision in [MolSysSuite #79](https://github.com/uibcdf/molsyssuite/issues/79).

Record provider identity and old/new immutable versions or commits, affected and
candidate consumers, old/new observable behavior, compatibility and release
effects, migration or fallback, evidence and unknowns, and owners of follow-up
work. Give notice before publishing the provider change or starting consumer
rollout when impact is foreseeable; report a later discovery promptly. Reuse
the existing issue for the same independently closable theme. Subsequent commits
within that tracked change update its evidence and handoff rather than creating
a notice per commit.

Identify members from `suite.toml`. Use the registered guide relationships,
dependency graph and maintained publisher inventory to identify known consumers.
Record where a list is incomplete and distinguish a candidate consumer from a
verified user. For Conda publication use
`python devtools/scripts/python_distribution_status.py --publisher-kind shared-noarch`
and recheck recorded calls before rollout.

Send the actionable handoff to each affected member's existing owner issue, or
open an owner issue when concrete adoption has no existing home. Record exact
notice links, reviewed caller/version commits, relevant installed or runtime
evidence, and deferred work separately. Guide synchronization, notice delivery,
source adoption and tested/public artifacts are different states. Close the
central coordination issue only when its declared coordination criteria are met.

Internal maintainer direct pushes and the accepted brief/full CI lanes continue
under their [existing policy](python_ci_policy.md). Consumer release decisions
and scientific failures remain component-owned. The impact record coordinates
work; it adds no central preapproval gate for ordinary provider development.
Confidential or exploitable details use the private reporting route first.

A bounded exception identifies the affected rule/consumer, owner issue, reason,
responsible maintainer, interim controls, expiry/review date and removal condition.
A deferred consumer adoption can remain tracked without delaying an independent
provider release when the compatibility contract and owner decision allow it.
