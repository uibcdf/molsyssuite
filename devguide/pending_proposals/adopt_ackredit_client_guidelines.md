---
summary: Adopt optional lazy attribution guidance from the real MolSysMT interaction pilot.
issue: uibcdf/molsyssuite#68
status: active
opened: 2026-10-01
closed:
verification: inspected
area: [governance, compatibility, provenance]
guard:
normative:
blocked_by: []
supersedes: []
---

# Ackredit client guidance from the interaction pilot

## What

Review and adopt shared guidance for components integrating optional scientific
runtime attribution. MolSysMT interactions are the first real client under
uibcdf/molsysmt#27. Ackredit owns its API and canonical integration guide under
uibcdf/ackredit#75. MolSysSuite owns common applicability and synchronization.

## How

The proposed profile is concrete below. If accepted, add it to the suite ecosystem
policy and the provider-owned `standards/ACKREDIT_GUIDE.md`, then distribute that
canonical guide with `sync_vendored_guides.py`. Keep the current tested eager/demo
examples available with explicit applicability; do not edit consumer copies or
merge the scientific pilot branch as part of this governance change.

## Why

The current Ackredit guide's optional shim imports the provider immediately and
recommends registration in the host's `__init__`. The pilot defers provider loading
and registration, contributes to the application's current session, and preserves
a detached bibliography in each scientific result. The two profiles need an
explicit applicability boundary before distributing a common client rule.

## Evidence and its limits

Inspected client: `e21f03d9992b87af2cc9285211adee888462be41`, published on
`review/interaction-attribution-20261001` in MolSysMT. Its `_ackredit.py` uses the
public provider registration, scope and explicit tracking API and catalog warnings
for provider failures. It does not read a private provider registry or implement
a bibliography renderer. The pilot record reports 511 interaction/control tests,
310 overlapping attribution/diagnostic tests, 63 doctests and four executed
notebooks. These selections were not rerun by this governance review. The measured
provider was an editable, dirty 0.8 development version; these results do not
certify a published installation route or different provider revision.

The pilot tests assert actual provider observations, reused references in two
individual results, enclosing scopes, evaluated-empty results, absence/failure,
fresh-process lazy import and saved-result reading without new credit. Inspect
`tests/interactions/test_scientific_attribution.py` at that SHA for the evidence.
Its `molsysmt.scientific_attribution@1` payload remains a component-owned schema.
It is not silently promoted into an Ackredit or suite interchange format.

Provider canonical guide inspected at
`048ac0c612d5bd5537a350aa36316da63b45e609` (guide-only suite synchronization
on the previously inspected provider source). It recommends eager loading and
includes advanced hooks/persistence examples. The portable capture/export/import
API requested by uibcdf/ackredit#75 remains open. Current journals contain item IDs;
session differencing loses reused references and isolated sessions do not imply
parent propagation. Do not invent supported API names or an installation extra.

## Proposed common profile

This is a proposal awaiting the maintainer's choice, not a new accepted rule.
Applicability: new or changed optional attribution boundaries for scientific
methods/results in a MolSysSuite member. Utilities with no such boundary record
non-applicability; an installed package does not earn scientific credit by itself.

1. Keep declarations offline in host-owned constants and verify bibliographic
   fields against the original work. Defer provider imports and registration until
   the attribution boundary is actually requested. Importing the host does not
   load Ackredit, enable hooks or perform network/filesystem work.
2. Credit the scientific branch actually reached. Distinguish criterion,
   adapted reference implementation and executed software in the result context;
   a referenced implementation is not an executed dependency. Track once per
   calculation or meaningful child operation, never per pair/frame/occurrence.
3. Complete evaluated-empty analyses retain their actual provenance. A failed
   operation cannot claim successful completion; independently completed child
   operations may retain their own credit. Method definitions remain host-owned.
4. Applications own workflow sessions. A component contributes to the current
   session instead of replacing it with an isolated private session. Individual
   result references are not inferred by subtracting deduplicated session IDs.
5. Saved results carry detached bibliography and original producer versions,
   including works reused by multiple results. Reading or forwarding a result
   preserves those facts and does not claim another scientific calculation.
6. Provider absence preserves the scientific result and its host-owned detached
   provenance. A broken provider emits a catalog diagnostic and preserves a
   completed result; it must not silently claim successful tracking. Do not
   swallow the scientific function's own exception as a provider failure.
7. Libraries do not enable import hooks, auto tracking, DOI enrichment, journals
   or reminders automatically. Applications may explicitly choose provider
   features when their documented capabilities match the intended workflow.
8. Test with a real provider and assert actual tracking, plus two results reusing
   a reference, an enclosing workflow, evaluated-empty results, genuine absence,
   provider failure, detached ownership and a fresh reader with original versions.
   An installed flag or mocked success alone cannot prove integration.
9. Verify provider version floors and published dependency closure for each
   claimed client Python minor. Do not narrow MolSysMT/Viewer support to force an
   optional provider into every environment. Editable-source pilot evidence does
   not authorize a public optional extra or published compatibility claim.
10. Ackredit owns portable capture/export/import and provider guide examples.
    Until its supported contract is agreed, the bounded host adapter uses only
    supported public operations and keeps the result schema/scientific declarations
    local. Do not centralize the pilot schema or pretend journals export full
    portable bibliography. Provider adoption and member adoption remain separate.

A special integration needing different initialization or session semantics needs
a member-owned reviewed exception naming the rule, reason, interim controls,
owner, expiry and removal condition under the suite ecosystem policy. Third-party
hosts and existing eager/demo examples remain documented provider profiles; the
proposed optional MolSysSuite profile does not rewrite their implementation.

## Decision to consult

- **Adopt the bounded lazy client profile now:** document the rules and provider
  boundary, synchronize the canonical guide, and leave portable API implementation
  and public distribution with their owning Ackredit issues. This is recommended
  because the real pilot already supplies concrete consumer evidence.
- **Wait for the portable provider contract:** keep current guidance and the pilot
  as provisional evidence until uibcdf/ackredit#75 settles capture/export/import,
  then accept and synchronize a complete provider-backed profile.

Neither choice authorizes scientific branch merges, public package publication or
blanket attribution dependencies in all components.

## Acceptance criteria

- The maintainer selects the profile timing and its applicability.
- Suite policy and provider canonical guide state compatible lazy/session/result
  rules with a documented exception mechanism and no unsupported API promise.
- Canonical guide is synchronized through the registered route, with existing
  eager/demo profile applicability and tested examples preserved.
- Records separate reported pilot measurements, actual provider capabilities,
  publication/compatibility evidence and member runtime adoption.
- Offline governance and the relevant guide/profile administrative checks pass.

## Scope and exclusions

Shared client guidance and canonical provider-guide adoption. Scientific detector
implementation, merges of the interaction pilot, whole-library instrumentation,
portable provider API implementation and new public releases remain with their
owning component work. The authorized following blocks remain #59, #46/#18 and
#52, in that order; this decision precedes further block work.
