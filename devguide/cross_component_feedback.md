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
stabilization cohorts in `suite.toml`; an incubating consumer may reveal a valid provider
improvement without causing it to preempt wave-1 stability work.

If the request does not belong in the named provider, close or transfer it with an
explicit owner and stable cross-link. Do not let it disappear between repositories.
