---
summary: Recognize separate exact-upload calls without counting build-only qualification.
issue: uibcdf/molsyssuite#196
status: resolved
opened: 2026-11-13
closed: 2026-11-13
severity: medium
verification: reproduced
area: [governance, distribution]
guard: tests/test_python_distribution_status.py::PythonDistributionStatusTests::test_separate_exact_upload_is_a_publisher_in_committed_source
normative:
blocked_by: []
supersedes: []
---

# Separate Conda uploads were absent from the publisher inventory

**Reported:** During #87 owner receiving, 2026-11-12 Mexico City / 2026-11-13 UTC.
**Status:** Resolved in the source-only observer and its inventory validator.

## What

At SMonitor `f69d2d5e91be9d5f81dd48b123d00d0596e0a8ca`, the committed
publisher has two upload-disabled root builds and two separately inspected,
digest-bound `/upload@87c70b1443d5f22d738ee3ddf812bdbe0152f6c2` steps.
The unchanged production observer at `a3a829b8aede73fb07498358fde59855ec249b8c`
reports `no-conda-publisher-observed` and no calls. Its validator also lacks
the separate upload prefix. This would misrepresent an actual source adoption.

## How and why

The observer recognizes shared noarch jobs and combined root build/upload steps.
An upload-disabled build is correctly excluded, but no branch admits the actual
separate upload operation. Recognize the exact `/upload@` prefix independently
of root build flags and admit that prefix in validation. Preserve the existing
schema, committed-source boundary and classification vocabulary.

## Measurements and guard relevance

The new real-Git regression commits two upload steps, an upload-disabled build,
promotion and withdrawal in an actual workflow, plus an ignored nested backup.
It then replaces the uncommitted workflow with an empty document. The production
observer must still report exactly the two committed uploads and their source
commit; the production validator must accept that row. The same test fails before
the repair with the false-absence result and passes after it. Existing shared
caller, build-only, completeness and truthful-kind controls remain passing.

The selected distribution-status, release-contract and governance modules pass
174 tests with published Pytest Receptor 1.2.3 on Linux/Python 3.14.7. Exact
source/report/guard hashes, the original failure and selected JUnit digests are
retained in the [#87 receiving receipt](../rollouts/conda_owner_receiving_87_20261113.json).
The published closeout retains exact-source hosted acceptance and scratch retirement.

## Alternatives and scope

Keeping the old SMonitor row would leave a stale observation. Calling this
component publisher-free would convert an unsupported reader shape into false
absence. Counting upload-disabled root builds would misclassify qualification.
The additive upload branch represents the actual publishing entry point.

No component workflow, provider pin, package, credential, canonical guide or
scientific run changes. Promotion/withdrawal, nested backups and build-only
qualification remain excluded. Source presence establishes neither enabled
execution nor publication/readiness; suspended routes retain their owner state.

## Acceptance and local issues

The causal regression protects both observation and validation; eight received
#87 rows are refreshed with every other complete row preserved. Existing
SMonitor #58 needs no component correction: its source exposed this central bug.
The owner adoption and wider #87 acceptance remain separate.

## Provenance

Immutable fetched Git objects and complete owner issues/comments were inspected.
Primary/human work and #82 resources remain preserved. Only task-owned fixtures,
source evidence and the published receptor overlay are retired at closeout.
