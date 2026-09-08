---
summary: Vendored guides are rewritten by repository-specific Ruff configurations.
issue: uibcdf/molsyssuite#12
status: resolved
opened: 2026-09-06
closed: 2026-09-08
severity: high
verification: measured
area: [python, tooling, governance, ci]
guard: tests/test_governance.py::VendoredGuideSynchronizationTests
normative: devguide/vendored_guides.md
blocked_by: []
supersedes: []
---

# Vendored guides use the host Ruff configuration

**Reported:** 2026-09-06 from the ArgDigest and DepDigest Ruff rollout.
**Status:** Resolved; formatter ownership, explicit exclusions and byte-drift checks are
enforced by policy release 1.1.4.

## What

Ruff formats fenced Python in Markdown using the host repository's settings. A guide
copied byte-for-byte from another repository can therefore fail locally or be rewritten
and later reverted by synchronization.

## How

The collision is between two valid but incompatible invariants: exact synchronized
copies and host-wide formatting. Line width was initially involved, but TopoMT's single
quote setting reproduced the conflict even after snippet lines were shortened.

## Why

The suite currently carries six shared guides and dozens of copies. Local stopgaps do not
identify generated files or prove that copies still match their source.

## What is measured and what is assumed

The issue records Ruff 0.16.5 measurements at line lengths 88, 100 and 120 and a quote
style conflict in TopoMT. Current sibling checkout comparison on 2026-09-07 also found
stale SMonitor, DepDigest, ArgDigest and PyUnitWizard copies. It is assumed that every
registered consumer should receive the current canonical guide.

## Alternatives and refuted paths

- One suite-wide line length was rejected because quote style independently reproduces
  the conflict.
- Reformatting consumer copies was rejected because synchronization correctly reverts
  local changes.
- Excluding every Markdown file was rejected because it removes useful checks from
  repository-owned documentation.

## Scope and exclusions

This applies to registered root integration guides. Canonical sources, local developer
documentation, notebooks and generated non-guide artifacts keep their owning repository's
rules.

## Acceptance criteria

- [x] One normative policy assigns formatter ownership and an explicit Ruff exclusion.
- [x] Every guide and consumer is registered centrally.
- [x] Source and copies carry an unambiguous generated/read-only marker.
- [x] Offline tests cover exclusion, markers, missing copies and byte drift.
- [x] A central workflow checks the cross-repository inventory.
- [x] Current Ruff adopters and TopoMT use the rule without changing canonical sources.

## Local implementation issues

The guide rollout is coordinated by `uibcdf/molsyssuite#12`. The broader TopoMT policy
adoption exposed during verification continues in `uibcdf/topomt#16` under
`uibcdf/molsyssuite#6`.

## Dependencies and risks

Guide replacement may reveal intentional local edits. Such edits must be proposed at the
canonical source rather than preserved as untracked divergence.

## Resolution

Commit `79e814e` registered all six guides and their consumers, made
`devguide/vendored_guides.md` normative, extended the repository guard and starter kit,
and added the cross-repository byte comparison. Commit `8347947` removed a checkout-local
assumption from the test fixture and published immutable `policy-v1.1.4`.

All registered sources and copies matched in local verification. Central runs
`34212867390`, `34212867379`, and `34212867408` passed governance, ambassador-guide and
full vendored-guide checks respectively. ArgDigest, DepDigest, Pytest Receptor and GH Run
Receptor then passed the reusable 1.1.4 policy gate. TopoMT adopted the shared Python
range, Ruff target and explicit guide exclusions without making its remaining incubating
Ruff cleanup a blocker for this defect.
