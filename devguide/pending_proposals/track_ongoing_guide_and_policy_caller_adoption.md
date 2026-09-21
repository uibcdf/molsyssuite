---
summary: Track ongoing guide and policy caller adoption across members.
issue: uibcdf/molsyssuite#34
status: active
opened: 2026-09-21
closed:
verification: measured
area: [governance, documentation, ci]
guard:
normative:
blocked_by: []
supersedes: []
---

# Track ongoing guide and policy caller adoption across members

**Reported:** 2026-09-21, after a canonical guide update and policy 1.4.1 rollout.
**Status:** Active; `uibcdf/molsyssuite#35` is the first concrete guide rollout used to
exercise and refine the process.

## What

MolSysSuite already registers canonical guides and consumer copies and checks byte
equality. It also checks versioned policy-workflow callers. Those checks detect
staleness, but neither turns a publication into assigned, reviewable adoption work
across all registered members. A guide-only edit and a new required policy release
are different events and should not be coupled mechanically.

## How

Maintain a central inventory of each consumer, canonical guide revision, current
copy, required policy release, caller pin, owner, exception, and next action. When a
canonical guide changes, identify affected consumers and prepare reviewable updates
or pull requests. When a new policy release is required, propose its caller-pin
change with any necessary migration and local validation. Keep component review and
CI before merge; do not push or auto-merge silently into member repositories. The
existing drift and conformance guards should verify convergence and report actionable
remaining work.

## Why

The current guard can remain red across the entire registry after central
publication, leaving maintainers to discover and coordinate updates manually.
An ongoing publication-to-adoption lifecycle prevents members from quietly keeping
obsolete instructions or an obsolete gate without making every prose change a
runtime-policy update.

## What is measured and what is assumed

On 2026-09-21, hosted MolSysSuite run
`35596834974` of `.github/workflows/check-vendored-guides.yaml` reported
`GUIDE_DRIFT` for `MOLSYSSUITE_GUIDE.md` in all 13 registered members and for
`GH_RUN_RECEPTOR_GUIDE.md` in MolSysViewer. The workflow already runs on relevant
central pushes, weekly schedule, and manual dispatch; it checks exact copies but
does not propose updates. The central repository checker enforces applicable
versioned policy caller pins. It is assumed that a reviewable cross-repository
proposal mechanism can be built with acceptable permissions; credential design
and rollout batching have not yet been decided.

## Alternatives and refuted paths

- Automatically rewrite and push each member workflow for every guide edit: rejected
  because guide content and versioned policy behavior change independently and
  member maintainers need local validation.
- Keep only the red central detector: insufficient because it identifies drift but
  does not assign or complete adoption.
- Use unpinned policy callers: rejected because it would make policy behavior change
  without a reviewable member commit.

## Scope and exclusions

This applies to registered MolSysSuite members and canonical integration guides.
It owns ongoing adoption after central publication. The initial policy-1.0 rollout
remains `uibcdf/molsyssuite#6`; vendored ownership and drift semantics were settled
under `uibcdf/molsyssuite#12`. It does not change component-specific release gates
or require automatic merging.

## Acceptance criteria

- The central inventory distinguishes guide copy drift from policy caller pin drift.
- Each canonical guide or required policy-release change yields reviewable, assigned
  member adoption work or an explicit, expiring exception.
- Central guards identify the affected member, expected source or version, and next
  action, and converge to green after adoption.
- A guide-only edit does not force a caller-pin bump; a required policy release
  cannot be called fully adopted while applicable members are stale or unexcepted.
- A normative operational procedure and an automated guard protect this lifecycle.

## Local implementation issues

`uibcdf/molsyssuite#35` is the first central rollout case. Open member issues only where
migration needs component-specific work.

## Dependencies and risks

Cross-repository write permissions must be narrowly scoped if automation proposes
pull requests. The process must tolerate members with concurrent work and avoid
making a permanently failing guard into accepted background noise.

## Provenance

GitHub Actions run `35596834974` on 2026-09-21, using the central
`check-vendored-guides.yaml` workflow. The inspected local source was the
MolSysSuite checkout on Linux; no Python runtime claim is involved.
