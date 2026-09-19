---
summary: Govern Zenodo archival and DOI lifecycle across MolSysSuite.
issue: uibcdf/molsyssuite#24
status: active
opened: 2026-09-19
closed:
verification: measured
area: [governance, releases, citation, automation]
guard:
normative:
blocked_by: []
supersedes: []
---

# Governing Zenodo archival and DOI lifecycle across MolSysSuite

**Reported:** 2026-09-19, after enabling the Zenodo integration for gh-run-receptor and
recognizing that account ownership, DOI semantics, and archival claims affect every
publishing component.
**Status:** Active; component evidence exists, but MolSysSuite has no accepted common
policy, authoritative applicability registry, or collective audit.

## What

Define one suite-wide policy for Zenodo archival and DOI lifecycle. MolSysSuite should own
the common rules, applicability, account-side stewardship, evidence threshold, monitoring,
and exception process. Each component should remain responsible for release-specific
metadata, artifacts, workflows, tests, and evidence.

The policy must distinguish at least four facts that are currently easy to conflate:

1. citation metadata exists in a repository;
2. the repository toggle is believed to be enabled in a connected Zenodo account;
3. a GitHub Release was published after enablement;
4. a public Zenodo record with DOI and archived files was independently verified.

Only the fourth fact permits a component or suite surface to claim completed archival.

## How

Add an accepted normative document, provisionally `devguide/zenodo_policy.md`, and
register its applicability in `suite.toml`. The policy should assign responsibilities:

- **MolSysSuite governance:** decide which member profiles require archival, define
  metadata and DOI rules, maintain the collective inventory, audit drift, and approve
  bounded exceptions;
- **authorized Zenodo maintainers:** connect the UIBCDF account, synchronize repository
  visibility, enable eligible repositories, and inspect account-side ingestion failures;
- **component maintainers:** keep `CITATION.cff` and optional `.zenodo.json` consistent,
  publish verified releases, run the public record verifier, and retain exact-version
  evidence locally;
- **automation:** validate only public or repository-contained facts and never claim an
  account toggle, DOI, deposit, or file archive from a successful GitHub Release alone.

Define concept DOI and version DOI use explicitly. Stable project badges, README citation,
and general documentation should normally use the concept DOI; an exact release record or
reproducibility statement may use its version DOI. Neither value may be invented, copied
from another component, or recorded before the public record proves it.

The authoritative registry should state applicability and durable identity without
putting credentials or personal account data in Git. Candidate fields include archival
mode (`required`, `optional`, or a documented exception), public concept DOI, and the
component issue responsible for adoption. Frequently changing evidence such as last
verified version, date, record URL, and failure state belongs in a generated or maintained
rollout/audit document rather than being confused with stable component identity.

The accepted workflow should cover:

1. metadata validation before a release;
2. draft-first GitHub release verification where the component supports it;
3. publication only after the component's own gates pass;
4. bounded waiting for asynchronous Zenodo ingestion;
5. read-only verification through the public Zenodo API;
6. distinct `verified`, `absent`, `invalid`, and temporarily unavailable states;
7. incident ownership and retry rules;
8. concept/version DOI publication only after verification;
9. periodic suite audit and removal or correction of stale DOI badges;
10. an exception with reason, issue, owner, and expiration condition when archival does
    not apply or cannot be completed.

## Why

Zenodo account access and integration toggles span repositories and cannot be governed
truthfully by a component-local runbook. If each component invents its own convention,
MolSysSuite risks inconsistent creators and ORCIDs, version DOIs frozen into project
badges, silent missing deposits, unsupported assumptions about backfill, and green release
workflows that are mistaken for external archival.

Gh-run-receptor already demonstrates the correct separation of concerns: it has matching
citation metadata, verified GitHub Release assets, a bounded public verifier, and an
account-side handoff, yet its latest release is still publicly absent. That implementation
is useful evidence for a common policy but should not become the suite authority merely
because it encountered the problem first.

## What is measured and what is assumed

Measured on 2026-09-19:

- `suite.toml` contains no Zenodo, DOI, citation, or archival policy;
- no open or closed `uibcdf/molsyssuite` issue governs this theme;
- gh-run-receptor issue `uibcdf/gh-run-receptor#27` delivered and tested a local public
  verifier plus maintainer handoff;
- gh-run-receptor 0.21.1 is a published GitHub Release with verified assets;
- a fresh anonymous Zenodo API query, evaluated by that repository's semantic verifier,
  returned `Zenodo archive: ABSENT — 0.21.1`;
- a maintainer reports that the gh-run-receptor repository toggle has now been enabled.

The reported toggle state cannot be independently read from GitHub or the anonymous
Zenodo records API. The next GitHub Release published after enablement is therefore the
first suitable positive test; prior releases are not assumed to be backfilled.

It is not yet measured which other MolSysSuite members have enabled integrations, concept
DOIs, valid metadata, archived files, or current badges. That inventory is acceptance
work, not an assumption in this proposal.

## Alternatives and refuted paths

- Keeping the policy only in gh-run-receptor is rejected because account governance,
  citation semantics, and applicability span multiple components.
- Treating a successful GitHub Release or a valid `.zenodo.json` as archival proof is
  rejected; gh-run-receptor supplies a real counterexample.
- Storing credentials, access tokens, personal account identifiers, or mutable Zenodo
  account state in `suite.toml` is rejected.
- Using a version DOI in a permanent project badge is rejected because it freezes one
  historical release instead of following the project concept.
- Assuming that enabling a repository retroactively archives old releases is rejected
  until measured for the actual integration.
- Requiring every incubating repository to mint a DOI immediately is rejected as an
  unreviewed applicability decision; policy profiles and explicit exceptions must decide.
- Centralizing component release implementation in MolSysSuite is rejected. Shared policy
  and audit are central; release code and evidence remain with the component that can
  test and repair them.

## Scope and exclusions

The proposal applies potentially to all registered repositories, with final applicability
decided by profile and publication status. It governs Zenodo release archival, citation
metadata consistency, DOI presentation, monitoring, and exceptions.

It does not grant account access, automate login, store secrets, publish the next
gh-run-receptor release, change scientific authorship, decide a suite-level DOI for an
aggregate MolSysSuite product, or replace repository-specific release gates. Those are
separate decisions or component work.

## Acceptance criteria

- Publish one normative central Zenodo/DOI policy with explicit applicability and
  exception semantics.
- Register the accepted policy in `suite.toml` with an existing normative path and central
  issue.
- Define MolSysSuite, account-maintainer, component-maintainer, and automation ownership.
- Define concept DOI versus version DOI use and prohibit unverified DOI claims.
- Define minimum metadata consistency, pre-release validation, post-release verification,
  retry, and incident rules.
- Inventory every registered member without silently changing it; record `verified`,
  `absent`, `not_applicable`, `unknown`, or an explicit exception with evidence date.
- Prove the path with at least one release published after confirmed enablement and verify
  its public DOI plus archived files.
- Add an offline governance guard for stable registry semantics and a bounded authenticated
  or public audit for external facts.
- Route the policy from `MOLSYSSUITE_GUIDE.md` and identify any component-local adoption
  issues actually required.
- Record a rollout that distinguishes policy adoption from successful archive ingestion.

## Local implementation issues

- `uibcdf/gh-run-receptor#27` — resolved local verifier and maintainer handoff; supplies
  the first negative evidence and candidate positive pilot.

Do not create issues in every component until the inventory identifies a concrete local
change. Future component issues should own only metadata, workflow, badge, or release
remediation in that repository.

## Dependencies and risks

The first positive pilot depends on a new gh-run-receptor GitHub Release after the reported
Zenodo enablement and on Zenodo's asynchronous processing. That dependency does not block
drafting and accepting the common policy or auditing existing component state.

Central policy must not overclaim authority over external service availability. Zenodo can
delay ingestion, change API behavior, or expose account-side errors only to authorized
maintainers. The policy needs a temporary-unavailable state and bounded retries rather
than turning every service delay into false component failure.

## Provenance

Inspection ran on 2026-09-19 from the MolSysSuite workspace on Linux with Python 3.13.14
and GitHub CLI 2.93.0. `python devtools/scripts/suite_status.py` found 11 of 12 registered
repositories current and clean; the only unrelated state is the preserved untracked
`topomt/sandbox/smoke_test.ipynb`. The Zenodo query was anonymous and read-only; its
temporary response was deleted after verification.
