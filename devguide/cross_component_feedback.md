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

This route applies when work in a member component needs a change in another
component or UIBCDF auxiliary provider. The repository owning the behavior also
owns the solution and its review:

1. For a nonurgent need without a ready fix, open or update the provider issue
   with the reproduction, consumer impact and required outcome. Its maintainers
   decide priority and implementation.
2. With a concrete proposed fix, submit a provider pull request for owner review
   and acceptance, linked to the owning issue and affected consumer work.
3. For urgent work performed by Diego (`dprada`) or Liliana (`LMMV`), or directly
   supervised by either, ask which route to use: direct push, pull request or
   issue. A direct commit and push to the other repository requires their
   explicit authorization before either action. Without it, use the issue or
   pull request route.

Explicit authorization already given for the same work remains valid; do not
ask again merely because the work reaches its next commit or repository within
the authorized scope. A new owner, scope or conflicting instruction needs its
own route decision. Urgency or shared UIBCDF membership alone grants no write
authority, and another contributor does not inherit a maintainer's authorization.

This contribution route does not replace an owning team's local review practice
or the accepted internal-maintainer direct-push and CI rules. Repository-local
development remains with its owner. Retain provider and consumer issue links;
use private reporting first for confidential or exploitable findings. A shared
provider change also needs the separate consumer-impact handoff below; owner
review of a fix does not substitute for that notice.

A bounded exception records the affected rule and repositories, owning issue,
reason, responsible maintainer, explicit route authorization, interim controls,
review/expiry date and removal condition. It does not authorize other work or
contributors, or weaken release and CI evidence requirements.

This adopts the owner contribution route in
[MOLI #41](https://github.com/uibcdf/moli/issues/41) for suite members under
[MolSysSuite #83](https://github.com/uibcdf/molsyssuite/issues/83).

## Shared-provider changes and consumer impact

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
