---
summary: Restore MolSysSuite authority over governance of its members
issue: uibcdf/molsyssuite#53
status: resolved
opened: 2026-09-26
closed: 2026-09-27
verification: inspected
area: [governance, tooling, releases]
guard: tests/test_suite_policy.py
normative: devguide/repository_contract.md
blocked_by: []
supersedes: []
---

# Restore MolSysSuite authority over governance of its members

**Reported:** 2026-09-26, during review of the MOLI–MolSysSuite boundary.
**Status:** Resolved on 2026-09-27. Ongoing policy-caller adoption is tracked
separately in `uibcdf/molsyssuite#34`.

## What

MolSysSuite, as one MOLI component, remains accountable for platform contracts.
MolSysSuite governs its own members. The suite registry, policy documents and
versioned checks become the sole normative source for member Python, CI, Ruff,
support-library, developer-tool, distribution, release, badge and archival rules.

## How

Move the values currently derived from a pinned MOLI commit into `suite.toml` at
their existing effective settings. Replace the runtime MOLI policy loader with
a local suite loader. Update the canonical member guide, starter kit,
conformance workflow, validators and tests. Keep the MOLI commit reference only
as context for the suite's platform obligations. Publish a new suite policy
release and synchronize member guide copies through the established rollout.

## Why

The previous loader made MOLI the effective authority for member-level values,
although MolSysSuite already owned member admission, adoption and enforcement.
Local authority lets one suite decision change a member rule and preserves
reproducibility through suite policy releases. Platform contracts remain visible
at the suite boundary.

## What is measured and what is assumed

**Inspected on 2026-09-26:** `moli_policy.py` supplied nine member policies from
a pinned MOLI `moli.toml`; the suite had no local Ruff, Python, CI, distribution
or release-version values. Member reviews and guide consumers were already
registered in `suite.toml`. Two unrelated Pytest Receptor review edits were
present locally and preserved before this transition.

**Assumed pending member rollout:** existing member callers can continue using
their compatible policy releases while the new suite release is distributed.
Each member's observed guide and caller state must be checked; a central edit
alone does not establish member adoption.

## Alternatives and refuted paths

- Keeping automatic transitive MOLI inheritance was rejected because MOLI would
  still own the effective member values.
- Removing MOLI platform obligations was rejected because MolSysSuite remains a
  MOLI component with cross-component contracts and scientific duties.

## Scope and exclusions

This changes governance authority, not member implementations or public package
version numbers. Historical policy releases and recorded exceptions remain
immutable. Source providers still own their software and issue boards.

## Acceptance criteria

- MOLI and MolSysSuite registries and guides state the same ownership boundary.
- Suite member policy values are locally defined and validated without a MOLI checkout.
- The new suite policy release passes governance and member-checker tests.
- Canonical guide copies and relevant callers have a recorded rollout state.
- The preserved Pytest Receptor review edits are restored without entering the
  governance transition commit.

## Local implementation issues

Open a member issue only where a concrete guide or caller change is needed;
track the collective inventory in `uibcdf/molsyssuite#34` and this issue.

## Dependencies and risks

The transition needs a published suite policy tag before a member can call it.
Prematurely requiring that tag would break CI. Guide synchronization can be
staged separately from caller adoption. A MOLI scientific quantity contract
must remain binding at the suite boundary throughout the transition.

## Resolution and verification

Resolved by `52ee96d` and `cf3f3b2`, published as immutable
`policy-v1.5.0`. `suite.toml` and `devtools/scripts/suite_policy.py` now own
member policy values; MOLI remains the source for platform obligations. The
canonical guide was synchronized to all 15 registered members and three
contradictory `AGENTS.md` routes were corrected. The local suite policy tests
passed (148 tests at closure), and hosted governance and guide audits passed
in runs `36279831659`, `36280689653` and `36280689562`.

The normative ownership boundary is `devguide/repository_contract.md`. The
relevant regression guard is `tests/test_suite_policy.py`, which rejects
delegated member values and verifies that changes to the MOLI revision do not
change suite member values. Existing compatible member workflow pins remain
effective; their individual adoption is tracked by `uibcdf/molsyssuite#34`.

## Provenance

Inspection date: 2026-09-26. Sources: `moli.toml`, `suite.toml`,
`devtools/scripts/moli_policy.py` at MolSysSuite `eb265c3`, and the active
MolSysSuite member guide. No runtime package measurement was needed for this
governance ownership decision.
