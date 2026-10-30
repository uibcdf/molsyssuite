---
summary: Require human permission before agents publish external issues or pull requests.
issue: uibcdf/molsyssuite#159
status: active
opened: 2026-10-30
closed:
verification: inspected
area: [governance]
guard:
normative: devguide/cross_component_feedback.md
blocked_by: []
supersedes: []
---

# Agent authorization for external issues and pull requests

**Reported:** Explicit principal-maintainer instruction on 2026-10-30.
**Status:** Accepted instruction; canonical publication and registered delivery in progress.

## What

Agents need prior explicit permission from Diego Prada Gracia or Liliana Marisol
Moreno Vargas before creating/publishing issues or PRs outside MolI's scope or
repositories owned by us, in particular outside github.com/uibcdf. Remote drafts
count. Ordinary internal reporting, read-only research and local preparation
retain their normal authorized routes.

## How

Clarify the existing cross-component contribution and reporting policies, the
canonical MOLSYSSUITE_GUIDE.md and the official starter's reporting route. The
root mandatory guide delegation remains the common entry; no duplicate rule is
needed in each AGENTS.md. Publish the canonical source first and use only the
registered synchronizer for all seventeen member copies. Preserve primary/dirty
clones using task-owned temporary clones. Keep original and delivered identities,
structural checks and native executed-step evidence separate.

## Why

A universal feedback duty must not be read as permission to post outside our
organization/platform. The external Conda hook handoff under #139 is a concrete
example. Credentials and internal direct-push permission do not authorize that
external publication. MolI #80 owns platform/direct-component adoption separately.

## What is measured and what is assumed

The existing feedback, contribution, reporting and generated instruction routes
were inspected. The official generator copies the canonical guide and mandatory
entry; the local reporting template now explicitly routes the same boundary.
No external issue/PR is created. Delivery and checks are recorded after execution.

## Alternatives and refuted paths

Repeating the rule in seventeen root instruction files would create competing
common sources. Use the established canonical guide and mandatory delegation.
Generic authorization or an outside fork cannot substitute for human permission.

## Scope and exclusions

All registered suite members, including auxiliary/incubating/subsystem members.
No component implementation, scientific suite, policy-tag bump, executable pin,
release, shared-environment change or MolI direct-member rollout is required.

## Acceptance criteria

- Normative reporting/contribution guidance and starter convey the named approvers
  and scoped prior-permission boundary, without a conflicting feedback fallback.
- All registered members have received byte-identical canonical guidance, or a
  bounded owning deferral/exception; record source/delivery/checks separately.
- Reconcile central issue and maintained checkpoint, with MolI #80 handoff.

## Local implementation issues

MolI-wide guide/template adoption: uibcdf/moli#80. Member work is central-owned
canonical distribution under uibcdf/molsyssuite#159, not scientific implementation.

## Dependencies and risks

Preserve concurrent owner changes and private repository evidence. Missing native
job-step metadata must remain unverified, even when a run reports success.

## Provenance

2026-10-30, Linux development host; named molsyssuite@uibcdf_3.14 environment.
Selected governance/generation checks and delivery receipts follow below.

Local canonical checks: Python 3.14.7 in the named shared environment;
`python -m pytest --receptor=llm tests/test_agent_instructions.py` passes 15
existing instruction tests. The existing `StarterKitTests` and
`VendoredGuideSynchronizationTests` pass 18 tests, including generation, byte
identity, stale canonical-source rejection and preservation of modified copies.
The offline governance validator and regenerated indexes pass. These checks
qualify instruction routing/distribution mechanisms, not scientific behavior.
