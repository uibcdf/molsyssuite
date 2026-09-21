---
summary: Admit Ackredit as an incubating MolSysSuite support library
issue: uibcdf/molsyssuite#28
status: resolved
opened: 2026-09-20
closed: 2026-09-21
verification: inspected
area: [governance, membership, integration]
guard: tests/test_governance.py::GovernanceTests::test_ackredit_is_registered_as_incubating_support_library
normative:
blocked_by: []
supersedes: []
---

# Admit Ackredit as an incubating MolSysSuite member

**Reported:** 2026-09-20 as FlowCite; the owner renamed the component Ackredit before
central registration. The final name and schema-version-2 classification are settled in
the comments of `uibcdf/molsyssuite#28`.
**Status:** Resolved; registration, local policy conformance and the exact member
classification are verified.

## What

Register `uibcdf/ackredit` as a primary, active, incubating support library with the
`python-package` capability and optional Zenodo archival. Ackredit records runtime
citations and acknowledgements for workflows. Its hosts must work when it is absent.
Incubating membership does not imply a stable public API, a release, Python 3.14 support,
or a stabilization-priority assignment.

## How

Add the member to `suite.toml`, include it as a consumer of the canonical MolSysSuite,
SMonitor and DepDigest guides it already uses and the GH Run Receptor guide for its
documented CI-inspection practice, and register its own
`standards/ACKREDIT_GUIDE.md` as the source of an integration guide with no consumers
until a host formally adopts it. Synchronize its suite guide and enforce the existing
component policy, including the Python 3.11--3.13 range, Ruff and badges. Add the
incubating, optional Zenodo entry with state `unknown` and a test that guards its
classification and registered guide relationships.

## Why

The repository already exists and has adopted the common baseline, but without a member
entry the central conformance guard reports `UNREGISTERED` and its integration guide has
no governing owner. Registration lets future hosts discover its optional-dependency
contract without confusing an unverified citation engine with a stabilized component.

## What is measured and what is assumed

**Inspected 2026-09-21:** `ackredit/pyproject.toml` declares Python `>=3.11,<3.14`,
SMonitor and DepDigest dependencies and a pure-Python package. Its README and AGENTS
describe an optional host integration. The two existing root integration-guide copies
match their canonical sources byte-for-byte. Its `standards/ACKREDIT_GUIDE.md` exists.
The existing central check initially reported `UNREGISTERED`; after the registry,
synchronized guides and canonical badges were updated,
`python -m devtools.scripts.check_repository /home/diego/repos@uibcdf/ackredit
--repository uibcdf/ackredit` accepted the checkout as conforming to policy 1.0.
The offline governance validator and all 79 central tests pass. Ackredit's 263 tests
pass in serial mode; a parallel run produced one isolated-test-passing failure in an
unrelated concurrent code change, so the admission does not claim xdist-clean tests.

**Unverified:** no Python 3.14 admission, PyPI or Conda release, Zenodo deposit, host
consumer, or stable public API is established by this central registration.

## Alternatives and refuted paths

- Retaining the old FlowCite name is rejected: it was changed before registration and
  only persists in the historical opening issue body; its later owner comments settle
  the name and classification.
- Reusing the superseded `profiles` registry field is rejected: schema version 2 requires
  separate role, membership, maturity, development mode and capability fields.
- Registering an actual host consumer for `ACKREDIT_GUIDE.md` before that host adopts it
  is rejected: it would invent a cross-repository contract and fail the byte-level gate.

## Scope and exclusions

This admits an incubating support library and its existing guide authority. It does not
add Ackredit to the Python 3.14 transition, stabilization priorities, any host runtime
dependencies, or the mandatory Zenodo cohort. The separate CI environment problem for
members depending on sibling libraries belongs to `uibcdf/molsyssuite#31`.

## Acceptance criteria

- The classification, guide owner and consumer relationships are guarded in
  `tests/test_governance.py`.
- The Ackredit checkout passes the central conformance check without altering unrelated
  work in its dirty tree.
- The Zenodo inventory and generated governance indexes include the new member.
- The central issue closes with a link to the archived record and the guard.

## Local implementation issues

Ackredit-specific CI and dependency-environment work is tracked in `uibcdf/ackredit#6`.

## Dependencies and risks

The older issue body describes FlowCite and an obsolete registry schema; later comments
are the authoritative corrected request. Existing Ackredit code has unrelated local
modifications and must remain untouched.

## Resolution

Ackredit is registered as a primary incubating support library with four consumed
canonical guides and an owned integration guide without invented host consumers.
The assertion named in `guard` reads the registry and fails if the member's
classification, guide ownership or consumers regress. Admission is not an approval
for Python 3.14, a release, or a stable product contract.

## Provenance

Central `suite.toml`, central conformance checker and the Ackredit checkout inspected
locally on 2026-09-21. No release or interpreter-compatibility test was inferred from
source inspection.
