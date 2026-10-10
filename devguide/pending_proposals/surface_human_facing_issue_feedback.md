---
summary: Adopt human-facing contributor issue feedback while the MolSys-AI pilot remains pending.
issue: uibcdf/molsyssuite#65
status: partial
opened: 2026-10-10
closed:
verification: inspected
area: [governance, working-instructions]
guard:
normative: devguide/working_instructions_policy.md
blocked_by: []
supersedes: []
---

# Human-facing issue feedback in contributor instructions

**Reported:** 2026-10-10, review of remaining central governance issues.
**Status:** The contributor instruction is accepted on 2026-10-10; central policy,
root instructions and the starter are updated. Member delivery is pending.
The full MolSys-AI objective remains open.

## What

Review whether the developer-instruction part of uibcdf/molsyssuite#65 can be
accepted before its scientist-facing pilot exists. The intended action is to
surface an actionable suspected defect, inconsistency, missing analysis or
improvement, including uncertain and nonblocking findings, and explicitly offer
its owning issue to the human collaborator. Existing authority, disclosure
restrictions and owner triage remain applicable.

## How

The current canonical guide already adopts the universal issue-feedback
commitment from MOLI. It requires an owning issue for actionable findings but
does not explicitly describe offering that issue during a human conversation.
The future human-facing workflow is expressly pending in
`devguide/working_instructions_policy.md`. This record proposes that instruction
step for a separate decision; it does not reinterpret the future objective as
already accepted.

Initial component-facing draft reviewed at `7e79574bc804a1d2802d81e85322bf2f380a5713`:

> During development, tests, scientific exploration and conversations, surface
> actionable suspected defects, inconsistencies, missing analyses and improvements,
> even when uncertain or nonblocking. State what was observed and what remains
> uncertain; identify the owning repository and check for an existing issue.
> When working with a human, explicitly offer to open or update that issue at a
> natural pause, and respect a declined or deferred report. File or update under
> the applicable authorization; existing authorization for the same work does
> not require another permission request. Keep confidential findings out of
> public issues and use the private security route when appropriate. Follow the
> canonical reporting and cross-component feedback routes.

If accepted, maintain the full common action in `MOLSYSSUITE_GUIDE.md` and the
reporting/instruction policy. Put a short actionable route in the central root
`AGENTS.md`, the versioned component starter, and each member's root instructions.
Reuse the current nested instruction routes and exception mechanism. The
registered guide synchronizer must distribute byte-identical canonical copies;
consumer copies must not be edited independently.

Before rollout, update the owning impact issue, identify all sixteen members
from `suite.toml`, and send the accepted text, immutable source and applicable
local checks to their owning adoption issues. Preserve concurrent component work.
An early-development member has the same reporting route; its scientific maturity
does not imply additional tests or a promise to implement every reported need.

The proposal's handling of a declined human report must be reconciled explicitly
with the universal reporting commitment in coordination with uibcdf/moli#34.
Existing authority to report ordinary authorized technical findings must remain
usable without a repeated approval step. Human review remains relevant for new
scientific disclosures, uncertain interpretation and confidential inputs.

## Why

A durable reporting rule can be followed mechanically while an uncertain or
nonblocking finding is still lost during a conversation. An explicit contributor
action would make that finding visible and correctly owned. It can be evaluated
without building MolSys-AI integrations or changing scientific suites.

## What is measured and what is assumed

Inspected on 2026-10-10:

- uibcdf/molsyssuite#65: open, no comments; includes contributor instructions and
  a later scientist-facing pilot as separate acceptance requirements.
- uibcdf/moli#34: open, no comments; the cross-platform contract is proposed.
- MOLI's already adopted reporting protocol at immutable commit
  `8056b7861ce9238d75a3b957322d839ccb6c7ca6`, read through GitHub's contents API.
- Central guide and policy at unchanged source
  `e1866466428bc021944f20674de9181f3e719b69`: ordinary reporting is adopted;
  the future human-facing workflow is pending.
- `devtools/scripts/agent_instructions.py`: already checks root/nested instruction
  routes and registered exceptions; it deliberately does not judge instruction
  prose. This proposal requires no new checker, Action or runtime feature.
- `devtools/templates/python_component/AGENTS.md`: already provides ordinary
  reporting and durable instruction routes, without the proposed explicit offer.

No new scientist-facing behavior, notification service, component adoption,
scientific verification or accepted policy is inferred from those inspections.

## Alternatives and refuted paths

1. **Accept this instruction step now, after review.** Reuse existing routes and
   distribute it through ordinary governance adoption. Keep the pilot pending.
2. **Wait for the scientist-facing contract and pilot.** Retain current universal
   reporting and leave the proposed conversational instruction unadopted.

Neither alternative needs a new reporting Action, another instruction lifecycle,
automatic public scientific disclosure or repeated permission for authorized work.

## Scope and exclusions

The proposed instruction applies to MolSysSuite and its sixteen registered members
for contributor and agent work. Platform-wide acceptance belongs to MOLI.

The MolSys-AI / MolSysViewer pilot, UI integration, opt-in subscriptions, verified
fix notifications and automatic task retry remain future owner work. No package,
dependency floor, release, scientific suite or publication gate changes here.

## Acceptance criteria

For the bounded instruction step:

- A reviewed decision accepts or defers the proposed action and explains the
  relationship between human review and existing reporting authorization.
- If accepted, maintained policy and root/starter routes agree; shared-provider
  notice precedes registered guide delivery and member adoption.
- Local adoption checks verify instruction routes and canonical guide identity;
  notice delivery is recorded separately from accepted member adoption.
- Applicable reporting/index/governance checks pass; scientific tests are not
  invoked solely for instruction prose.

Closing uibcdf/molsyssuite#65 still requires its full pilot acceptance criteria,
including privacy/deduplication, correct ownership and opt-in notification only
after a usable verified fix. Completing this step alone cannot close that issue.

## Local implementation issues

None opened by this draft. Open or reuse member adoption issues only after the
shared instruction decision and impact handoff. Future pilot implementation
issues remain in their owning components.

## Dependencies and risks

The cross-platform human-facing contract is coordinated in uibcdf/moli#34.
It does not block preparing or reviewing this draft. Publication of a policy
change requires the new instruction decision; the existing universal reporting
rule remains in force. Avoid interpreting a suspected finding as a proven
scientific defect or promising a release merely because an issue exists.

## Provenance

Review date: 2026-10-10, Linux workspace. Metadata was inspected with `gh issue
view` and `gh api`; canonical source, starter and checker were read locally.
Qualified interpreter: `molsyssuite@uibcdf_3.14`, Python 3.14.7; editable receptor
imports resolve to their participating local clones. The seven previously accepted
dependency-closure findings under uibcdf/molsyssuite#82 remain unchanged. They
do not constitute a new clean-closure claim or invalidate this prose inspection.

## Accepted instruction decision, 2026-10-10

The principal developer accepted **"Adoptar la instrucción ahora"**, including
member guides/instructions and preservation of existing reporting authority.
The scientist-facing pilot and notifications remain pending. The initial draft's
447 central tests and coverage upload pass in native run 38032654499; that evidence
validates the draft commit rather than this later accepted provider change.

The accepted canonical text makes the authority boundary explicit: respect a
declined/deferred human disclosure, retain only an authorized sanitized disposition,
and do not publish the human's confidential material without authority. The
ordinary universal reporting obligation remains due for otherwise authorized
findings. This is a member contributor rule; uibcdf/moli#34 owns platform-wide
acceptance and future product integration. No new runtime or test requirement
is created.

Updated maintained surfaces are `MOLSYSSUITE_GUIDE.md`, `AGENTS.md`, the versioned
Python-component root instruction template, `devguide/reporting_protocol.md` and
`devguide/working_instructions_policy.md`. Local route and canonical guide checks
will establish member instruction delivery separately from future product behavior.
Advance owning impact/adoption notices precede provider publication and rollout.
