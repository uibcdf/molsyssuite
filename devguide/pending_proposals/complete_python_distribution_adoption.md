---
summary: Complete evidence-backed member adoption of the suite distribution policy.
issue: uibcdf/molsyssuite#45
status: partial
opened: 2026-09-24
closed:
verification: inspected
area: [governance, distribution, compatibility]
guard: tests/test_python_distribution_status.py
normative: devguide/python_distribution_policy.md
blocked_by: []
supersedes: []
---

# Python distribution member adoption

**Reported:** 2026-09-24; current ownership and source baseline reviewed 2026-10-01.
**Status:** Partial. Accepted suite policy, inventory validator and onboarding exist;
member-owned route adoption and publication-readiness evidence remain incomplete.

## What

Complete and record adoption of the accepted distribution contract in every
registered Python component, with truthful route applicability and bounded exceptions.

## How

Use `suite.toml`'s separate adoption, CI/recipe and publication-access fields.
Inspect required metadata, maintained recipes, runtime environments and source
routes; review local early/negative dependency checks, generated resources for
each claimed artifact, immutable publication and independent public poststate.
Record member-owned implementation/evidence rather than equating synchronized
guides with adoption. Reuse the existing repository and publication checkers.

The [dated rollout](../rollouts/python_distribution.md) contains the 14 immutable
source identities, bounded audit results, component gaps and the proposed handling
of the four legacy publishers. The maintainer must choose that operational path
before their publication events are changed.

## Why

A passing general repository checker does not establish the entire distribution
contract. The source baseline finds omitted recipe requirements, weak environment
floors, unbounded recipe Python claims, outdated upload routes and artifact-specific
review gaps. Central policy ownership makes those adoption gaps visible without
assigning component scientific repairs to MolSysSuite.

## What is measured and what is assumed

All 14 current inspected member snapshots pass the general repository checker.
The existing publisher-profile audit reports 26 findings in nine repositories,
three conforming publisher repositories and two with no publisher. Results are
bounded source observations, not installed-artifact evidence or a new defect
diagnosis for each custom workflow. The committed inventory currently lists all
14 reviews as pending/pending/unknown.

Viewer#106 reports a completed working-tree audit, but that implementation is
absent from the inspected remote-main SHA. Its closure is recorded as incoming
evidence rather than silently credited to the inspected tree.

## Alternatives and refuted paths

- Updating a MOLI pin alone is no longer member adoption. MolSysSuite owns the
  member rules; the original issue's inheritance description is historical.
- Passing guide or general source checks is insufficient route evidence.
- Rebuilding an artifact cannot substitute for exact-file label promotion.
- Requiring full scientific runs for ordinary internal development pushes would
  contradict the accepted phased CI policy and the user's current work scope.
- Conda publication is not inferred for components documenting other supported
  routes or only source development.

## Scope and exclusions

The 14 `python-package` members. MolSys-AI is outside this Python distribution
inventory. The central metapackage profile remains uibcdf/molsyssuite#67.
Scientific algorithms, postponed full scientific execution reviews and package
publication are outside this initial administrative audit.

## Acceptance criteria

- Member-facing policy and starter contract remain consistent with the suite-owned
  registry and reference the platform credential procedure once settled.
- Every Python member has a member-owned evidence-backed review of its actual
  dependency, CI, recipe, artifact and claimed public routes, or a bounded exception.
- Access stays unknown until verified without exposing credentials; neither access
  nor public availability is inferred from configuration.
- Offline governance and relevant hosted administrative checks pass.
- Complete adoption is assessed with
  `python devtools/scripts/python_distribution_status.py --require-adopted`.

The registered guard protects inventory coverage and prevents unsupported adopted
states; it does not prove component dependency or artifact correctness.

## Local implementation issues

Current relevant bounded local themes: uibcdf/molsysmt#245,
uibcdf/molsysviewer#101, uibcdf/molsysviewer#106 and uibcdf/ackredit#22.
Whole-policy member reviews will be opened or reused after the publisher handling
choice; a narrow or closed local issue is not automatically complete adoption.

## Dependencies and risks

uibcdf/moli#8 owns the unresolved credential/access contract; unknown access does
not prevent an honest pre-publication review under the existing policy.
uibcdf/molsyssuite#47 tracks remaining installed Windows launcher evidence.
uibcdf/molsyssuite#59 owns the forward macOS support boundary.
Do not conflate these incomplete themes with a successful public installation.

## Provenance

2026-10-01; Linux, Python 3.13.15; central audit source
`bf3f06165f34ae542f830db57bf35519831224a0`.
Full member identities and repeatable commands are in the rollout record.

