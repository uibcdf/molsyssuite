---
summary: Adopt owner-controlled temporary resource cleanup across suite members.
issue: uibcdf/molsyssuite#104
status: partial
opened: 2026-10-06
closed:
verification: inspected
area: [governance, tooling]
guard:
normative: devguide/temporary_resources.md
blocked_by: []
supersedes: []
---

# Temporary resource lifecycle and member adoption

**Reported:** Ackredit qualification inventory on 2026-10-06.
**Status:** Maintainer approved policy-v1.5.8 publication and sixteen-member
guide delivery. Tool lifecycle and retrospective owner reviews remain separate.

## What

The initial report measured 65.7 GiB in /tmp and 96% root-disk use. Disposable
environments/caches dominated several retained Ackredit resources. The principal
maintainer clarified that useful evidence may remain in /tmp, without relocation.
Resources must be removed when their usefulness ends.

## How

The accepted temporary_resources.md text applies to all registered members.
Publish the normative policy, canonical guide and root/starter instructions
under policy-v1.5.8, then deliver the registered copies.
Use existing registry/synchronizer for byte-identical guide delivery. Record
source delivery independently of applicable tool lifecycle and historical cleanup.
Prefer managed temporary directories and retain caller-owned outputs/environments.

## Why

Unowned obsolete outputs can exhaust the shared filesystem. Blanket age/prefix
cleanup can destroy active/human work. Shared policy establishes an owned lifecycle,
without a separate global cleaner or new mandatory scientific test gate.

## What is measured and what is assumed

The initial issue retains dated disk/resource measurements. On 2026-10-07, all
five specifically named example paths are absent; removal attribution is unknown.
The filesystem now reports 52% used/about 54 GiB available. This is a bounded
observation, not a complete /tmp inventory or a claim this task reclaimed space.
Shared tools use managed qualification fixtures/temporary manifests; the existing
Conda-tool failure-propagation/cleanup test protects the manifest lifecycle.
Hosted runner disposal and artifact retention are inspected, not newly executed.
Component-owned tools require separate review when applicable.

## Alternatives and refuted paths

No whole-machine temporary cleaner, compulsory evidence relocation, fixed-age
expiry or copied per-component cleanup framework. Reuse existing lifecycle tools;
report missing provider capabilities with concrete consumer evidence.

## Scope and exclusions

Policy, registry, canonical guide, contributor/starter instructions and maintained
sixteen-member rollout. No scientific dispatch, environment removal, existing
package reconstruction, credentials change or deletion of another session's work.
Publish policy-v1.5.8 for the new shared rule. Existing caller pins remain
compatible; this introduces no new blocking scientific or CI-pattern gate.

## Acceptance criteria

- Accepted policy states applicability, cleanup/retention and bounded exceptions.
- Deliver byte-identical guide copies from the registered canonical source.
- Keep tool inspection/executed cleanup and actual source delivery separate.
- Retrospective resources receive owner review; preserve active/needed evidence.
- Coordinate with uibcdf/moli#61 and leave incomplete owner reviews visible.

## Local implementation issues

The rollout identifies every registered guide consumer. Existing distribution/CI
owner issues receive the adoption handoff; new local defects belong with each
component. Ackredit supplies the initial resource case; MOLI #61 owns its platform
coordination. Temporarily private OpenCASTp retains #102's access decisions.

## Dependencies and risks

Primary clones may contain active work. Use isolated committed snapshots for guide
updates and only the canonical synchronizer. A guide delivery does not prove all
scientific/documentation/build tools comply. Needed temporary evidence is ordinary
retention; a missing lifecycle implementation has an owned bounded exception.

## Provenance

2026-10-07 Linux x86_64; molsyssuite@uibcdf_3.14, Python3.14.7.
Existing seven #82 conflicts and eligible local receptor origins unchanged.
No unrelated directories or environments are cleaned by the adoption record.

## Publication authorization — 2026-10-07

The principal maintainer approved publishing policy-v1.5.8 and delivering all
sixteen registered guide copies. The previous draft-only checkpoint is
bffffcd5fe478d3f62f2c49af9024a6c4bd6c84d. The prepared version transition,
agent instructions and Conda lifecycle tests pass: 156 existing tests and the
offline governance guard. Python 3.14.7 and the two local editable receptors
are verified; seven existing dependency conflicts remain tracked in #82.
Advance notices identify the same policy impact and the component review owner.
Publication and exact delivery evidence will be added to the rollout receipt.
Guide synchronization alone will not close the pending tool lifecycle reviews.
