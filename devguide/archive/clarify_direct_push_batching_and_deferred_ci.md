---
summary: Clarify conditional direct-push batching, scoped local checks and deferred CI evidence.
issue: uibcdf/molsyssuite#94
status: resolved
opened: 2026-10-04
closed: 2026-10-04
verification: inspected
area: [governance, ci, instructions]
guard:
normative: devguide/python_ci_policy.md
blocked_by: []
supersedes: []
---

# Direct-push decisions and scoped validation

## What

Make the already authorized internal-maintainer route affordable and explicit:
select informative local checks, keep several commits local when remote visibility
is unnecessary, consider a permitted interim skip, and keep final validation and
any outstanding full-suite debt visible. Avoid repeating unchanged local cases
merely because a note was committed. External PR and release evidence retain
their existing full-suite and exact-candidate requirements.

The requesting evidence is uibcdf/molsyssuite#94 and uibcdf/moli#44. MOLI's
published direct-component wording in `afba713` is context, not automatically
inherited member policy. MolSysSuite owns its decision and adoption.

## How — prepared wording

Before a direct push, decide whether collaboration, backup or current evidence
needs a remote checkpoint. Prefer several local commits and one meaningful push
when it does not. A marker is optional, never the default for every small commit.
Consider it only within an authorized member route, after the relevant local
checks, when the risk permits deferral and the existing recovery/exception owner
is explicit. Preserve daily full-matrix debt and the #39 rollout/deferred core
work; this clarification does not turn deferred scientific lanes on.

Normally finish with an unskipped checkpoint and inspect the applicable gates
on the actual head. If work stops with evidence missing, identify that head,
what remains untested, its owning issue and recovery/manual route. Skipped,
failed, cancelled or unexecuted tests are not passing evidence.

Select local checks by changed code, inputs and scope. Documentation/evidence
requires its reporting/index/link/guide checks; a scientific hypothesis needs
its informative local numerical cases and explicit limits; executable behavior,
dependencies, metadata, packaging or integration boundaries need the relevant
code/contract tests. PR/release full-suite obligations remain. Retain a completed
local result while its tested code, inputs and scope stay unchanged; repeat or
broaden when later changes, failures or unresolved questions make it insufficient.
A local result does not certify a different remote head or installed candidate.

Put the short lasting action in central root instructions, the canonical guide
and the starter. Replace the starter's unconditional full pytest before each
commit with explicit scoped local gates in that same change. Registered member
copies are delivered with `sync_vendored_guides.py`. Concrete local instruction
contradictions need linked owner adoption; runtime tools and scientific repairs
remain component-owned.

## Facts checked and ownership

[GitHub skip semantics](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/skip-workflow-runs)
were checked on 2026-10-04: commit markers suppress `push`/`pull_request`
workflows, not just expensive tests; required PR checks can remain pending.
Schedules and manual dispatch are separate events. Do not advise using a marker
on a required PR head or representing it as selective test suppression.

OpenCASTp root instructions and the official starter currently require full
pytest before any commit. That conflicts with a proposed docs-only scoped path
until the owning instructions change together. TopoMT has a different local rule:
lint/type before commits and pytest before PRs; review its actual text before
proposing an edit. The original active clones must be preserved. A guide copy,
owner notice and accepted local instruction change are distinct delivery states.

## Maintainer decision — accepted 2026-10-04

The maintainer accepted a clarification: the purpose is safe, executed CI for
publication and releases. A literal marker ban is not the shared condition.
An authorized manual route remains valid only when every mandatory gate has
executed and passed for the exact candidate and installed bytes/closure, retaining
the original producer identity and digest. No gate is waived and no recorded
file is rebuilt. Normally finish ordinary iteration with an unskipped checkpoint;
explicitly executed and verified manual exact-head gates are also valid.
Missing evidence and full-suite backlog stay visible and owner-linked.

The maintainer also requested a final MOLI issue explaining the delivered rule,
changes and reason, for consideration alongside uibcdf/moli#44. This is a
coordination handoff, not an automatic change to MOLI's accepted policy.

## Why

This makes internal iteration lighter while protecting integration and release
claims through executed evidence and reliable recovery. Unconditional full local
pytest, unconditional skips, duplicating unchanged checks and silently dropping
full-suite debt each lose a necessary distinction.

## Acceptance criteria

- Settle the checkpoint/publication wording without changing full PR/release gates.
- Publish scoped contributor actions in the normative policy, central instructions,
  canonical guide and versioned starter, preserving tested-result reuse boundaries.
- Reconcile concrete member-local contradictions through linked owner changes;
  record reviewed source commits, delivered guide hashes and evidence separately.
- Validate offline governance and relevant instruction/starter regressions.
- Preserve #39 rollout ownership, daily recovery and deferred core science work.

## Alternatives and limits

No new action, CI execution schema, mandatory test-count floor or scientific
implementation is proposed. Existing reusable guards and synchronization own
these operations. Admission/policy tags remain immutable. A guide wording change
alone does not claim a recovery workflow executed or a science suite passed.

## Provenance

Inspected central main `3ae32e74812762cdce73ef2e5bf78fcd724667e6`, current issue
comments and official GitHub documentation on 2026-10-04. Cross-member source
identities and owner adoption will be recorded after the decision and fresh
registered status scan. No new component scientific suite was executed.

## Delivery record

`devguide/rollouts/direct_push_instructions_94.json` records all sixteen consumers
from the registered canonical-guide inventory, reviewed source identities, owning
CI/governance issues and the eight concrete root-instruction contradictions.
Existing owning CI issues retain their broader implementation/qualification scope;
this delivery does not close them or change their recovery adoption states.
The central normative guard is the CI checkpoint section; existing starter and
instruction regressions (13 tests) and offline governance pass on Python 3.14.7.
No new scientific suite or mandatory semantic prose checker was introduced.

## Resolution — 2026-10-04

Accepted source `33474ecd05f8e9e89a288fa2e802e411cca14858` publishes the
normative checkpoint section, central working instruction, canonical guide,
scoped starter instruction and bootstrap guidance. The normative section
protects the decision: all mandatory PR/admission/release gates must execute;
authorized exact-head/exact-original-artifact manual qualification is valid;
local-result reuse cannot certify a changed head or closure. This clarification
requires no new machine policy version or existing workflow pin migration.

All sixteen registered canonical-guide consumers received SHA-256
`80ec36238f68c00ea660791a67d3ae2e7d5489e59ab60d4d908aee353792a02b` through
`sync_vendored_guides.py`. Eight source roots were reconciled in the same local
commits as their guide copies: OpenCASTp, DockingMT, Ackredit, LinDelInt,
TopoMT, PyUnitWizard, GH Run Receptor and MolSysMT. The pre-change facts above
are preserved as the inspected starting state, not current local requirements.
Only guides/root working instructions changed in consumers; implementation,
scientific tests, workflows, policy tags and artifact identities were preserved.
The sixteen immutable heads and before/after source identities are in
`devguide/rollouts/direct_push_instructions_94.json`.

Verification: the existing thirteen starter/instruction regressions and offline
central governance pass locally with Python 3.14.7; all member guide guards,
applicable standalone report-index checks and changed-line whitespace checks
pass. The minimal administrative interpreter was used for governance checks;
no scientific environment or suite qualification is inferred from it.
The source governance run [37187663012](https://github.com/uibcdf/molsyssuite/actions/runs/37187663012)
passed. Initial push guide audit
[37187663022](https://github.com/uibcdf/molsyssuite/actions/runs/37187663022)
failed before distribution and remains visible. After all consumer pushes,
manual audit [37187914475](https://github.com/uibcdf/molsyssuite/actions/runs/37187914475)
passed all seventeen jobs. This proves the shared guide/instruction route,
not scientific correctness or a full-matrix recovery watermark.

Owner handoffs were sent to each registered member's existing CI/governance
issue before distribution; delivery links and exact commits are in the rollout
receipt. Broader owner CI/recovery issues remain owned and are not closed by
this instruction delivery. Most documentation pushes conditionally deferred
automatic CI to the explicit shared governance audit; their full-suite debt is
not cleared. OpenCASTp, which does not yet implement skip recovery, and the
non-Python umbrella MolSys-AI used unskipped pushes. Original active clones and
their uncommitted work were preserved by using isolated local clones.

At the maintainer's request, [MOLI #45](https://github.com/uibcdf/moli/issues/45)
contains the final result, changes and rationale for review alongside MOLI #44.
MOLI owns that follow-up; this suite decision does not silently revise its
policy. Full CI rollout remains uibcdf/molsyssuite#39, and deferred core science
and general action/package-withdrawal work retain their existing owners/scope.
