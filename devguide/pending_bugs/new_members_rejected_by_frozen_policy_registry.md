---
summary: Published starter policy rejects newly admitted members from its frozen registry
issue: uibcdf/molsyssuite#73
status: open
opened: 2026-10-02
closed:
severity: medium
verification: reproduced
area: [governance, ci, admission]
guard:
normative:
blocked_by: []
supersedes: []
---

# Published policy rejects newly admitted members

## What

The official starter generates a policy-v1.5.2 reusable caller whose registry
snapshot does not contain members admitted afterward. OpenCASTp is registered
in current main but the published workflow rejects it as UNREGISTERED.

## How

At OpenCASTp c9a6f65ea6a7b76924f21df17c88830e745ca561,
https://github.com/uibcdf/opencastp/actions/runs/37055145913 attempt 1
fails in Check repository conformance with
`[UNREGISTERED] uibcdf/opencastp is not registered in suite.toml`.
The same member passes source conformance at central admission
271aa61856089dc583427dbefbef72c69bab41d3, and routine CI plus the
three-minor numerical/installed matrix pass independently.

## Why

A new component that follows the starter cannot complete its published policy
gate. Admission facts and immutable member engineering policy need an explicit
relationship. A new policy snapshot is one option; an admission-aware mechanism
is another. Do not mutate an existing public tag or silently make engineering
rules depend on mutable main.

## Interim exception

OpenCASTp #3 owns an enforced, dated admission-bootstrap route pinned to the
central admission/authorization commit recorded in its workflow, with conformance and the inherited
Ruff checks. The original caller is visibly disabled, not tolerated as a failed
executed gate. The suite registry records the exception until 2026-12-31.
The maintainer owns review. Re-enable the published route only after a released
admission-aware gate recognizes the member and passes actual hosted checks.
A source-level bootstrap is not proof of published policy adoption.

## Acceptance criteria

- New-member admission and published checker membership agree through an explicit reviewed mechanism.
- Preserve immutable policy semantics and a regression for the observed failure.
- Demonstrate the released gate in the affected consumer before removing its exception.

## Scope

Tracked under uibcdf/molsyssuite#73; membership admission is #70.
No existing member or public policy tag is changed by the interim consumer route.

## Follow-up — 2026-10-02

The maintainer also requested Python 3.14. Its authorization is component-owned
uibcdf/opencastp#5, so the consumer pin must include that transition record.
The originally observed UNREGISTERED failure remains unchanged; update the
immutable bootstrap pin from the source that actually carries both admission
and authorization, rather than modifying any historical public tag.
