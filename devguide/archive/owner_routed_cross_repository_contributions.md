---
summary: Adopt the owner-routed contribution policy for changes to another repository.
issue: uibcdf/molsyssuite#83
status: resolved
opened: 2026-10-03
closed: 2026-10-03
verification: inspected
area: [governance]
guard:
normative: devguide/cross_component_feedback.md
blocked_by: []
supersedes: []
---

# Owner-routed cross-repository contributions

**Reported:** 2026-10-03 through uibcdf/molsyssuite#83 and uibcdf/moli#41.
**Status:** Resolved; accepted route published and delivered to all sixteen members.

## What

Make the contribution route explicit when a member developer needs a change in
another component or auxiliary provider. Preserve owner-local development,
existing explicit route authorization and the separate shared-provider notice.

## How

The normative cross-component feedback policy defines the issue, owner-reviewed
PR and authorized urgent direct-push routes. The canonical member guide, root
instructions and new-component starter link that policy. Existing authorization
for the same scope persists; other contributors do not inherit it. A tracked,
bounded exception has an owner, authorization, controls and exit condition.

Synchronize all registered member copies using `sync_vendored_guides.py` in
isolated checkouts at fetched current main. Record exact source and delivery
commits, guide audit evidence and the return handoff to MOLI #41. Do not edit
consumer guide copies manually or move immutable engineering-policy tags.

## Why

Provider ownership needs both an implementation review route and consumer
feedback. The earlier #79 notice rule covers consumer impact; it does not tell
a contributor how to propose a fix in a different owner's repository. MOLI
has adopted that route; MolSysSuite owns corresponding member guidance.

## What is measured and what is assumed

Inspection of current policy, guide and starter confirms that they describe
reporting and impact notices without the complete contribution route. GitHub
issue reads confirm MOLI's published policy and the suite-owned adoption request.
The maintainer authorized proceeding with #83 while retaining this session's
explicit direct-commit/push route. Guide delivery is not implementation or
scientific runtime qualification in a consuming component.

## Alternatives and refuted paths

- Applying the route to owner-local development would remove legitimate local
  practices outside this issue's scope.
- Asking again for each commit would contradict existing scoped authorization.
- Treating a provider PR as a consumer notice would omit the separate impact
  handoff accepted in #79.
- Updating a released policy tag would change its immutable meaning. This is
  maintained contributor guidance, not a changed Python/CI policy snapshot.

## Scope and exclusions

All repositories registered as canonical member-guide consumers are affected.
Auxiliary providers follow the route when contributing to another owner; their
own implementation and review remain theirs. Direct MOLI components are under
MOLI #41. Scientific code, release workflows, credentials and suite execution
are outside this documentation adoption.

## Acceptance criteria

- Normative policy states applicability, the three routes, scoped authorization,
  owner-local boundaries, impact notices and bounded exceptions.
- Root, canonical guide and starter expose the accepted lasting action.
- All registered member guide copies are identical and audited, with exact
  delivery commits recorded.
- Governance validation passes and the settled outcome is returned to MOLI #41.

## Local implementation issues

Member changes are canonical guide delivery only, tracked by
uibcdf/molsyssuite#83. Any later provider implementation change retains its own
owning issue and accepted review route.

## Dependencies and risks

Active member work is preserved using isolated clones and ordinary pushes with
concurrent changes reconciled before publication. No force pushes or original
dirty-worktree updates are permitted.

## Provenance

2026-10-03, Linux coordination workspace. Policy inspection and GitHub issue
reads; runtime execution and package publication are not claimed. Verification
commands and exact guide-delivery receipts are appended at resolution.

## Resolution — 2026-10-03

Canonical source `c23dfb7bf95818fbc6a3765c87516232da9461f7` publishes the
normative route, root instructions, canonical member summary and starter. The
registered synchronizer delivered byte-identical copies in sixteen guide-only
commits; per-member guide and root-instruction checks pass. Exact bases, delivery
commits, guide digest, audit runs and evidence limits are recorded in
`devguide/rollouts/cross_repository_contributions_83.json`.

Local administrative validation: `python devtools/scripts/validate_governance.py`
and six existing unittest targets (the `StarterKitTests` class and the feedback,
component-guide and starter-policy assertions in `GovernanceTests`) pass on
Python 3.13.15. This local interpreter is not claimed as the routine 3.14
development baseline. Exact-source native governance
[37135810290](https://github.com/uibcdf/molsyssuite/actions/runs/37135810290)
passes on Python 3.14, including the existing governance tests and publication
contract checks.

After member pushes, native component-guide audit
[37135810272](https://github.com/uibcdf/molsyssuite/actions/runs/37135810272)
passes all seventeen jobs, and the complete registered vendored-guide audit
[37135810234](https://github.com/uibcdf/molsyssuite/actions/runs/37135810234)
passes. Initial audit attempts ran before copy delivery and failed on drift;
post-delivery reruns pass, with original attempts retained in GitHub.

The documented route preserves the explicit direct-push authorization for this
work without requiring repeated confirmation. It creates no general authorization
for other contributors and changes no owner-local CI or release gate. Policy
`policy-v1.5.4` still resolves to its original commit
`e459ea0e8ac6aa8017e17a2f171c50d122b9e0b7`. Original dirty worktrees were
preserved, no scientific suites were launched, and no package mutation occurred.

MOLI #41 receives the adopted source, member delivery and verification handoff;
its direct-component implementation and closure remain MOLI-owned. Closure of
this issue is protected by the normative route in
`devguide/cross_component_feedback.md`. Existing guide/starter validators protect
delivery and discoverability; they do not replace owner review of policy meaning.
