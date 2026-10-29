---
summary: Consolidate GHR product/tooling qualification with the shared installed runner.
issue: uibcdf/molsyssuite#144
status: active
opened: 2026-10-25
closed:
verification: inspected
area: [distribution, tooling, compatibility]
guard:
normative:
blocked_by: [uibcdf/gh-run-receptor#76]
supersedes: []
---

# Consolidated product, tooling and installed qualification

**Reported:** GHR installed Conda qualification, uibcdf/gh-run-receptor#60 / #72.
**Status:** Principal-maintainer structural direction accepted on 2026-10-29;
component implementation handed to uibcdf/gh-run-receptor#76. No refactoring or
new shared SDK contract is implemented or qualified by this handoff.

## What and why

The original full installed test selection imports repository administrative
helpers through devtools/tests names; some helpers derive repository inputs
from their original __file__. Isolated installed collection failed before the
tests could execute. Adding the whole producer root can substitute source GHR
for the exact installed artifact. Renaming/staging path-dependent helpers alone
can change their behavior.

GHR's qualified original-path equivalent already unblocked public 1.3.0.
Ordinary Conda installation works; the remaining need is a maintainable complete
product/tooling/integration architecture and coordinated receiving.

## Accepted direction and component handoff

The maintainer selected full refactoring rather than immediately generalizing
legacy import/path interception. The implementation owner is GHR; the complete
What/How/Why, inspected examples, original identities and acceptance checklist
are in [uibcdf/gh-run-receptor#76](https://github.com/uibcdf/gh-run-receptor/issues/76).
The human will commission that team; central coordination does not begin its
implementation or notify a separate channel.

The target combines:

1. Physical product/tool separation, preferably src/gh_run_receptor or a reviewed
   equivalent; preserve packaging, resources, versions, CLI and editable use.
2. Component-specific tool imports and explicit repository/manifest/fixture/output
   inputs; independently useful operations have contracts and tests. Development
   helpers do not become public runtime payload/dependencies just to collect tests.
3. A complete before/after assertion inventory: installed product, repository
   tooling and their integration. Classify by claim, preserve all applicable
   checks, and explain actual non-applicability. Separation cannot waive gates.
4. Composition through supported shared runner/import/support operations, with
   distinct immutable product/artifact/tool/qualification/provider identities.
   Verify installed origins before/after the applicable execution outside source.
5. Full replacement receiving on claimed platform/minor boundaries, followed by
   retirement of the active GHR-specific adapter. Historical qualified sources
   and files remain immutable; no required half is indefinitely deferred.

Existing internal push/checkpoint policies remain unchanged. The work does not
impose every full matrix on every internal push or on unrelated components.

## MolSysSuite ownership and acceptance

MolSysSuite receives the component's immutable design/implementation/test handoff
under #144. Reuse installed_noarch.py, installed_imports.py and the existing
installed_test_support.py profile when the refactored tools can use them. Any
remaining shared gap needs minimal consumer evidence, a reusable provider API,
regressions, compatible default behavior, owner notice and actual receiving.
Do not copy provider behavior into GHR or broaden legacy namespace access by
assumption. No new API/schema or universal layout rule is accepted here.

#144 remains active until the component and shared boundary are consolidated:
all previous checks have an explicit executed home; real installed identity is
preserved; necessary shared operations are received; the maintained route no
longer needs the local adapter; owner docs/receipts and applicable native gates
agree. A directory rename, documentation-only handoff or planned future provider
fix cannot close the whole coordination scope.

The existing publisher inventory identifies nine potential shared-noarch users:
ArgDigest, Pytest Receptor, GHR, TopoMT, PharmacophoreMT, ElastNetMT, DockingMT,
Ackredit and LinDelInt. Only GHR is the confirmed original-path helper case.
Recheck concrete calls before any shared-provider rollout; keep impact notice,
source adoption and installed artifact receiving separate. The handoff changes
no other member's guide, caller, package or workflow.

## Preserved original evidence

- Producer/source: run 40143062622, 5a48759a399a17a16d923851b32519983a836f5f.
- Original file: gh-run-receptor-1.3.0-py_0.tar.bz2, SHA256
  65f33b29dad70eb9e779f917e4c553d27effa4fddc2740a0260d259866746fd3.
- Original failed installed run 40143357716 remains failed.
- Qualified administrative source: 08b83a0e853aff5c563ad9b19d0ddffb15e030f8;
  twelve-cell installed run 40144989781 and same-file promotion 40145282787.
- Public-delivery record: uibcdf/molsyssuite#143. Historical helper recovery is
  valid history, not an instruction to rewrite the frozen producer.

A new development/qualification candidate retains its own identity and owner
authorization. This handoff selects no public version and authorizes no rebuild
of original bytes, tag move, upload, promotion or package retirement.

## Alternatives and decision history

The earlier proposed optional original-path profile is preserved in the
[immutable study](https://github.com/uibcdf/molsyssuite/blob/662a39e91819e6628a6bdad26fe9fbd1b7ee289e/devguide/pending_proposals/receive_path_sensitive_installed_helpers.md).
It was studied, not accepted or implemented. Centralizing that equivalent would
reduce duplication but make special import/path management a shared compatibility
surface. Keeping it local avoids immediate work but leaves that maintenance.

The principal maintainer instead selected structural refactoring and a complete
shared boundary, accepting the larger initial effort. src layout alone or test
classification alone is insufficient. Shipping administrative tools in the public
runtime package only to satisfy collection adds an unnecessary product contract.
Dropping tests, silently widening paths or rebuilding to obtain green is rejected.

GHR's detailed implementation choices remain owner work; a legitimate remaining
shared need returns to #144 with evidence. It is not silently postponed or treated
as already solved by this issue handoff.

## Scope and provenance

2026-10-29, central read-only source review and authorized issue handoff. Component
code, primary worktrees, shared environments, original artifacts and scientific
work are unchanged. No MolSysMT work or new scientific execution occurs. Earlier
study/native receiving limits retain their original sources. The common guard,
index update and exact central documentation CI are recorded in #144 closeout
comments; they do not qualify the proposed refactoring.
