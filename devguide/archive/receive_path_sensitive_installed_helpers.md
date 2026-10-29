---
summary: Consolidate GHR product/tooling qualification with the shared installed runner.
issue: uibcdf/molsyssuite#144
status: resolved
opened: 2026-10-25
closed: 2026-10-29
verification: measured
area: [distribution, tooling, compatibility]
guard: tests/test_noarch_conda.py::NoarchCondaTests::test_src_source_paths_do_not_change_installed_archive_coordinates
normative:
blocked_by: []
supersedes: []
---

# Consolidated product, tooling and installed qualification

**Reported:** GHR installed Conda qualification, uibcdf/gh-run-receptor#60 / #72.
**Status:** Resolved on 2026-10-29. GHR #76 and shared provider #157 are
implemented and independently received. The initial handoff/history below is
preserved; the completed acceptance and exact evidence supersede its pending
implementation statements. Public 1.4.0 receiving is coordinated in #158.


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


## Concrete provider requirement during GHR implementation — 2026-10-29

GHR #76 reproduced that the current noarch source/resource/freeze operations
assume installed and source paths are identical. A src layout cannot pass.
The provider change supplies bounded source_root (`.` default or `src`) for
source-only resource/version lookup, preserving installed coordinates and
rejecting alias/missing/unsupported/mismatched inputs. Support @1 also refuses
src runtime payload renamed as helpers. Explicit --plan selection on the
installed CLI composes nonpublishing candidates without editing historical plans.

This is a reusable source-layout/input correction, not a generalized legacy-path
import API. No component/provider implementation is copied. The change is
prepared in a task-owned checkout from 56fe192; owner review, committed-source
provider provenance checks and complete GHR native receiving remain required.
The first local provider run has 52 passing tests and one expected dirty-source
binding rejection; the guard is retained and must pass against committed input.
No dirty run is qualification, and component packaging/tests remain separately owned.


The component's authorized nonpublishing same-file experiment also exposed that
the existing install/verify operations force a staging URL even after accepting a
local Path. The opt-in local-file origin reuses all digest, dependency, prefix,
resource and launcher operations while making the local URI/claim explicit.
This avoids publication solely to exercise a refactor. Staging remains the default
and public promotion gates are unchanged. Provider tests cover local success,
wrong URI/digest, pre-subprocess rejection and default staging rejection.


## Completed acceptance — 2026-10-29

The delivered owner architecture uses `src/gh_run_receptor` for runtime and
17 unshipped `gh_run_receptor_tools` modules with explicit inputs. Packaging
discovery, resources, versions, CLI, extension and Action routes remain owned
and guarded by GHR. The active original-path adapter is retired at
`7e483d7d8499956cfea0fd33ae37615daa7daacb`; the maintained installed workflow
calls the shared runner and support @1 directly. No generalized legacy-path
namespace API or new Action was introduced.

Independent AST inspection matched all original assertion expressions and
parameterization for all 437 baseline functions at
`15758c330f369c39f9a920eb4d7c164c007a2ccf`: 435 remain active; two adapter-specific
functions (16 parameterized cases) retain explicit retirement and successor or
non-applicability evidence in the owner inventory. The private producer's
333 product/integration functions and executable product/tool/recipe/resource
inputs are unchanged at adapter retirement; its README changed as documented.
Current 1.4.0 source has 446 classified functions: 314 product, 111 tooling,
21 integration. The owner inventory guard independently passes against this
committed source; classification is not a waiver of source/tooling gates.

Native receiving independently verifies original private run 40935956394,
12 cells × 638 tests, its original file SHA-256 and all six JSON records per cell
against native artifact ZIP digests. The intentionally skipped build reuses
the original private producer; it is not counted as a new passing build.
Retirement source matrix 40937173648 executes the complete source/tooling/
integration suite on all twelve boundaries. Final public 1.4.0 uses a distinct
source/file: matrix 40953626384 executes 650 tests in each of twelve cells, with
before/after installed provenance, seven shared-support checks and all 17
helper files removed after use. Exact-tag source/wheel and Action matrices,
final complete source suite, strict docs, policy, Conda controls and public
promotion are independently bound to their own recorded immutable sources.

Shared provider `fee3bd875e68778844c0fffc2aba26b6cea02cd6`, accepted through #157
at `31613c2322eab767fb316c5737bf4f56cba48d6d`, supplies bounded optional `source_root`
and exact local-file qualification. Its relevant runner files are byte-identical
between reviewed and merged input. All 57 affected local tests pass; exact
provider native governance/coverage 40920603151 passes. The default flat layout,
staging origin and publication gates retain their earlier behavior.

The local guard names the regression that verifies src source lookup while
preserving installed archive coordinates—the concrete shared failure exposed
by GHR. Companion central modules protect local URI/digest refusal, default
staging behavior and refusal to stage src runtime as helpers. Owner guards
`tests/test_installed_qualification.py`,
`tests/test_installed_qualification_workflow.py` and
`tests/test_tool_inputs.py::test_inventory_refuses_removed_assertions_and_unclassified_tests`
protect actual installed origins, direct shared composition, complete assertion
accounting and visible failures. Their source is in the immutable owner handoff;
central guard addressability alone is not the component acceptance proof.

The [durable receiving receipt](../rollouts/gh_run_receptor_1_4_0_receiving_158_20261029.json)
retains native run/attempt/job identities, digest-bound per-cell records, full
source/qualification/provider/file distinctions, original assertion review and
public-byte verification. Both original failed attempts and historical public
1.3.0 sources/files retain their conclusions and bytes. No scientific waiver,
new universal src requirement or automatic provider/caller migration applies
to other members. Original artifacts were not rebuilt by central receiving.
