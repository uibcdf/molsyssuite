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

**Reported:** 2026-09-24; initial source baseline 2026-10-01; registry and
PyUnitWizard, Ackredit and Pytest Receptor release evidence reconciled 2026-10-06.
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

The [dated rollout](../rollouts/python_distribution.md) preserves the initial 14 immutable
source identities, bounded audit results and component gaps, with dated updates
for the current 15-member Python inventory. The maintainer
authorized adapting the four legacy publishers now and migrating them to noarch
Python. See [the common route](../noarch_conda_workflow.md).

## Why

A passing general repository checker does not establish the entire distribution
contract. The source baseline finds omitted recipe requirements, weak environment
floors, unbounded recipe Python claims, outdated upload routes and artifact-specific
review gaps. Central policy ownership makes those adoption gaps visible without
assigning component scientific repairs to MolSysSuite.

## What is measured and what is assumed

All 14 initially inspected member snapshots pass the general repository checker.
The initial publisher-profile audit reported 26 findings in nine repositories,
three conforming publisher repositories and two with no publisher. Results are
bounded source observations, not installed-artifact evidence or a new defect
diagnosis for each custom workflow. Four delivered noarch migrations now have member-owned partial/partial/unknown
reviews in the initial delivery. As of 2026-10-06 the registry has 15 Python
reviews: seven partial and eight pending. PyUnitWizard advances to partial with
verified 0.28.1 evidence and member-owned uibcdf/pyunitwizard#114; no member is
newly marked adopted. Ackredit and Pytest Receptor also advance to partial with owned reviews
under uibcdf/ackredit#108 and uibcdf/pytest-receptor#38. Publication access
is confirmed only for these three observed authorized deliveries; the other
twelve access states remain unknown. See the
dated rollout for
full implementation identities and exact-source administrative runs.

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

The 15 currently registered `python-package` members, including OpenCASTp.
MolSys-AI is outside this Python distribution
inventory. The central metapackage profile remains uibcdf/molsyssuite#67.
Scientific algorithms, postponed full scientific execution reviews and new package
publication are outside this administrative work. Existing owner-run release
evidence may be inspected without authorizing another build or execution.

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
Noarch migration reviews: uibcdf/topomt#78, uibcdf/pharmacophoremt#10,
uibcdf/elastnetmt#18 and uibcdf/lindelint#13. Provider exact-file upload:
uibcdf/action-build-and-upload-conda-packages#45. A narrow or closed local issue
is not automatically whole-policy adoption.

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


## PyUnitWizard release reconciliation — 2026-10-06

Existing uibcdf/pyunitwizard#112 delivers public 0.28.1. The central read-only
review verifies its five exact-source gates (29 required jobs), all 30 installed
cells and source binding, producer and same-file promotion. The public label,
solver index and downloaded archive match the original digest and source;
all eight dependency-route hashes match. Source conformance and the publisher
contract checker pass. Old production dependency floors and absent test NumPy
are corrected in this candidate.

Receipt: [pyunitwizard_distribution_45_20261006.json](../rollouts/pyunitwizard_distribution_45_20261006.json).
The documented local publisher equivalent remains applicable; the generic
shared noarch operator is not used for this orchestration. Archived owner
receipts describe a fresh public install and complete closures. Central work
performs no new install, scientific execution, build or promotion.

Whole-policy adoption remains partial: uibcdf/pyunitwizard#114 owns the formal
review and maintained runnable dependency preflight/negative guards. One-time
negative results in a release receipt do not protect later metadata/route
changes. Identify an existing reusable local equivalent first. Current library
work and the provisional API scope retain their existing boundaries.


## Ackredit and Pytest Receptor reconciliation — 2026-10-06

The current sources pass general repository conformance. Public Ackredit 0.10.1
and Pytest Receptor 1.2.1 independently pass the shared read-only operator:
original producer/source/file binding, all eight Linux/macOS arm64 Python
3.11–3.14 installed cells and main-label/solver-index availability. Their original
source-gate evidence confirms 17 required jobs for Ackredit and 18 for Pytest
Receptor; those historical runs are not repeated here.
Downloaded Conda bytes pass the shared recipe/archive metadata, resources,
version and runtime-constraint checks. Ackredit's packaged citation names 0.10.1.
Pytest Receptor's public PyPI wheel and sdist separately match recorded hashes
and pass its existing release checker. This review runs administrative checks and performs no build, install, solve
or scientific test execution.

Receipts: [Ackredit](../rollouts/ackredit_distribution_45_20261006.json) and
[Pytest Receptor](../rollouts/pytest_receptor_distribution_45_20261006.json).
The original Pytest Receptor tag predates later canonical guide additions;
its historical latest-guide comparison fails, while current main passes.
Retain the historical result and original tag/bytes; it is not current guide drift.

Both member reviews are partial/partial with confirmed access bounded to
observed authorized delivery. Formal route review and maintained dependency
preflight/negative guards remain in uibcdf/ackredit#108 and
uibcdf/pytest-receptor#38. Existing recipe, packaging/resource and installation
page guards are retained; their narrower coverage does not protect all runtime
environment/source constraints. Source routes and build-only profiles must be
classified before introducing new operations; reuse maintained tools first.
Ackredit's ongoing 0.11.0 candidate and contract review remain separate from
this public 0.10.1 evidence. Pytest Receptor's self-test exception is preserved.
