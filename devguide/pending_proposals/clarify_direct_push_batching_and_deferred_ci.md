---
summary: Clarify conditional direct-push batching, scoped local checks and deferred CI evidence.
issue: uibcdf/molsyssuite#94
status: active
opened: 2026-10-04
closed:
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

## Maintainer decision pending

The issue requests a blanket prohibition on markers for candidates/publication.
Existing shared release operations deliberately support explicit manual
qualification of the exact original producer and immutable existing bytes,
including administrative recovery. A marker does not suppress manual dispatch.
Adding a literal marker ban would be a new common restriction beyond requiring
executed complete exact-candidate evidence.

Recommended: normally use the unskipped checkpoint; retain an explicit manual
route that verifies all required gates on the exact head/candidate and leaves
outstanding debt visible. Never waive PR/release gates or silently mark a skipped
run green. Alternative: additionally require a final unskipped push and ban
markers on release/publication commits even when all exact-candidate evidence
was independently obtained through the authorized manual route. The maintainer
must choose before that new normative condition or consumer instructions ship.

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
