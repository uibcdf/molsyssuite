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

## Implementation checkpoint — 2026-09-19

The common policy is implemented locally and awaiting publication plus ambassador-guide
synchronization. The implementation adds:

- `devguide/zenodo_policy.md` as the normative ownership, evidence, DOI, security,
  release-verification and exception contract;
- required applicability for wave-1 and infrastructure components, with auxiliary and
  incubating components optional until stabilization or release preparation;
- a complete machine-readable inventory whose only `verified` entry is the independently
  rechecked gh-run-receptor 1.0.0 record; every unmeasured component remains `unknown`;
- an offline schema and coverage guard plus a scheduled/manual anonymous public audit;
- a component-facing route in `MOLSYSSUITE_GUIDE.md`.

The public audit rechecked version DOI `10.5281/zenodo.22849252`, concept DOI
`10.5281/zenodo.22843377`, and the exact 569,573-byte 1.0.0 source snapshot with its MD5
checksum. No account mutation, credential access, release publication or inferred archive
claim was performed.

## What

Define one suite-wide policy for Zenodo archival and DOI lifecycle. MolSysSuite should own
the common rules, applicability, account-side stewardship, evidence threshold, monitoring,
and exception process. Each component should remain responsible for release-specific
metadata, artifacts, workflows, tests, and evidence.

The policy must distinguish facts that are currently easy to conflate:

1. citation metadata exists in a repository;
2. the repository toggle is believed to be enabled in a connected Zenodo account;
3. a release-event webhook is observed without inspecting its credential-bearing
   configuration;
4. a GitHub Release was published after enablement;
5. a public Zenodo record with DOI and explicitly inventoried files was independently
   verified.

Only the fifth fact permits a component or suite surface to claim completed archival.
Even then, the claim must name its coverage: source preservation is not proof that GitHub
Release distributions were copied into Zenodo.

## How

Add an accepted normative document, provisionally `devguide/zenodo_policy.md`, and
register its applicability in `suite.toml`. The policy should assign responsibilities:

- **MolSysSuite governance:** decide which member profiles require archival, define
  metadata and DOI rules, maintain the collective inventory, audit drift, and approve
  bounded exceptions;
- **authorized Zenodo maintainers:** connect the UIBCDF account, synchronize repository
  visibility, enable eligible repositories, rotate a repository connection after any
  credential-bearing receiver URL is exposed, and inspect account-side ingestion failures;
- **component maintainers:** keep `CITATION.cff` and optional `.zenodo.json` consistent,
  publish verified releases, run the public record verifier, and retain exact-version
  evidence locally;
- **automation:** validate only public or repository-contained facts and never claim an
  account toggle, DOI, deposit, or file archive from a successful GitHub Release alone.

Account-side inspection must follow a least-disclosure rule. GitHub webhook responses can
contain a receiver URL with a credential in its query string. Routine checks may project
only non-secret facts such as whether one hook is active, whether it subscribes to the
`release` event, and when it was updated. Raw hook configuration, receiver URLs, tokens,
screenshots containing them, and unfiltered API responses must not enter logs, issues,
developer guides, or audit artifacts. If such a value is exposed, the authorized
maintainer disables the repository toggle, synchronizes or refreshes the integration, and
reenables it before the next release. A new active release hook is operational recovery
evidence; its secret value is deliberately not read back or compared.

Define concept DOI and version DOI use explicitly. Stable project badges, README citation,
and general documentation should normally use the concept DOI; an exact release record or
reproducibility statement may use its version DOI. Neither value may be invented, copied
from another component, or recorded before the public record proves it.

Define metadata precedence as well as consistency. Zenodo documents that `.zenodo.json`
takes precedence and `CITATION.cff` is ignored for ingestion when both exist. A component
that retains both must still validate their shared title, creators, ORCIDs, license, and
repository relation so GitHub-facing citation and Zenodo ingestion do not silently
diverge. The policy must link the upstream rule at
`https://help.zenodo.org/docs/github/describe-software/zenodo-json/`.

The authoritative registry should state applicability and durable identity without
putting credentials or personal account data in Git. Candidate fields include archival
mode (`required`, `optional`, or a documented exception), public concept DOI, and the
component issue responsible for adoption. Frequently changing evidence such as last
verified version, date, record URL, and failure state belongs in a generated or maintained
rollout/audit document rather than being confused with stable component identity.

The accepted workflow should cover:

1. metadata validation before a release;
2. safe repository enablement or connection rotation without exposing hook configuration;
3. draft-first GitHub release verification where the component supports it;
4. publication only after the component's own gates pass;
5. bounded waiting for asynchronous Zenodo ingestion;
6. read-only verification through the public Zenodo API;
7. distinct `verified`, `absent`, `invalid`, and temporarily unavailable states;
8. verification of the actual archived filenames, sizes, and checksums independently from
   the GitHub Release asset inventory;
9. incident ownership and bounded retry rules;
10. concept/version DOI publication only after verification;
11. periodic suite audit and removal or correction of stale DOI badges;
12. an exception with reason, issue, owner, and expiration condition when archival does
    not apply or cannot be completed.

The operational state vocabulary should be explicit: `unknown`, `enabled_reported`,
`webhook_observed`, `release_published`, `ingestion_pending`, `verified`, `absent`,
`invalid`, and `temporarily_unavailable`. The first four are observations, not archival
claims. `absent` after publication may be a transient ingestion state and therefore needs
a bounded retry schedule; it must not be silently converted into either `verified` or a
permanent failure.

## Why

Zenodo account access and integration toggles span repositories and cannot be governed
truthfully by a component-local runbook. If each component invents its own convention,
MolSysSuite risks inconsistent creators and ORCIDs, version DOIs frozen into project
badges, silent missing deposits, unsupported assumptions about backfill, and green release
workflows that are mistaken for external archival.

Gh-run-receptor now demonstrates the complete separation of concerns: matching citation
metadata, independently verified GitHub Release distributions, safe account-side
reenablement, a bounded public verifier, and a positive Zenodo record. The pilot also
shows that the Zenodo archive and GitHub Release asset sets differ. That implementation is
useful evidence for a common policy but should not become the suite authority merely
because it encountered and completed the path first.

## What is measured and what is assumed

Measured on 2026-09-19 before the positive pilot:

- `suite.toml` contains no Zenodo, DOI, citation, or archival policy;
- no open or closed `uibcdf/molsyssuite` issue governs this theme;
- gh-run-receptor issue `uibcdf/gh-run-receptor#27` delivered and tested a local public
  verifier plus maintainer handoff;
- gh-run-receptor 0.21.1 is a published GitHub Release with verified assets;
- a fresh anonymous Zenodo API query, evaluated by that repository's semantic verifier,
  returned `Zenodo archive: ABSENT — 0.21.1`;
- a maintainer reports that the gh-run-receptor repository toggle has now been enabled.

Measured later on 2026-09-19 during the positive pilot:

- the repository connection was disabled, synchronized or refreshed, and reenabled after
  a credential-bearing receiver URL had appeared in an unfiltered maintainer query;
- a least-disclosure GitHub query observed one active `release` webhook with a fresh
  update time without requesting or printing its configuration;
- gh-run-receptor tag `0.22.0` resolves to
  `cbe269fcddfbcaaa6c5a691817221eca011935a8`;
- five exact-tag gates passed, followed by draft-first release run `35435957227`;
- independent public verification matched the wheel, source distribution, and checksum
  manifest in the GitHub Release, and an installed downloaded wheel reported 0.22.0;
- Zenodo verification run `35436181206` passed through the anonymous records API;
- the verified version DOI is `10.5281/zenodo.22843378` and the stable concept DOI is
  `10.5281/zenodo.22843377`;
- the Zenodo record contains one 535,405-byte source snapshot,
  `uibcdf/gh-run-receptor-0.22.0.zip`, while the GitHub Release separately contains the
  wheel, source distribution, and `SHA256SUMS`.

The toggle itself remains account-side mutable state. The active hook observation proves
that GitHub had a release delivery route at that time, not that Zenodo ingested a release.
The public Zenodo record is the positive archival proof. Prior releases remain unassumed
and were not backfilled as part of this pilot.

It is not yet measured which other MolSysSuite members have enabled integrations, concept
DOIs, valid metadata, archived files, or current badges. That inventory is acceptance
work, not an assumption in this proposal.

## Alternatives and refuted paths

- Keeping the policy only in gh-run-receptor is rejected because account governance,
  citation semantics, and applicability span multiple components.
- Treating a successful GitHub Release or a valid `.zenodo.json` as archival proof is
  rejected; gh-run-receptor supplies a real counterexample.
- Reading or retaining a complete webhook response to prove enablement is rejected because
  receiver configuration can contain a credential-bearing URL; a bounded field projection
  is sufficient for operational diagnosis.
- Treating a Zenodo source snapshot as proof that wheels, Conda packages, checksum
  manifests, or other GitHub Release assets were archived is rejected by the 0.22.0 pilot.
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
- Define the least-disclosure webhook inspection and connection-rotation procedure.
- Define archive-coverage vocabulary that distinguishes source snapshots from release
  distributions and validates the observed file inventory.
- Inventory every registered member without silently changing it; record `verified`,
  `absent`, `not_applicable`, `unknown`, or an explicit exception with evidence date.
- Retain the gh-run-receptor 0.22.0 positive pilot as evidence while requiring the accepted
  policy and collective audit to generalize rather than copy its repository-local code.
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

The first positive pilot is complete. The remaining work is policy acceptance, collective
inventory, registry design, offline guards, audit behavior, and component-specific
remediation discovered by that inventory.

Central policy must not overclaim authority over external service availability. Zenodo can
delay ingestion, change API behavior, or expose account-side errors only to authorized
maintainers. The policy needs a temporary-unavailable state and bounded retries rather
than turning every service delay into false component failure.

## Provenance

Inspection ran on 2026-09-19 from the MolSysSuite workspace on Linux with Python 3.13.14
and GitHub CLI 2.93.0. `python devtools/scripts/suite_status.py` found 11 of 12 registered
repositories current and clean; the only unrelated state is the preserved untracked
`topomt/sandbox/smoke_test.ipynb`. The positive Zenodo query was anonymous and read-only.
The webhook follow-up projected only non-secret status fields; no credential value was
copied into this report.
