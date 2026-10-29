---
summary: Assess optional original-path administrative helpers for installed package tests.
issue: uibcdf/molsyssuite#144
status: open
opened: 2026-10-25
closed:
verification: inspected
area: [distribution, tooling, compatibility]
guard:
normative:
blocked_by: []
supersedes: []
---

# Original-path administrative helpers in installed qualification

**Reported:** GH Run Receptor installed Conda receiving, uibcdf/gh-run-receptor#60 / #72.
**Status:** Study complete; optional shared contract proposed, not accepted or implemented.

## What

The existing shared unshipped-support @1 profile stages a declared helper package
under a dedicated namespace. It intentionally rejects legacy devtools/tests names.
Some administrative tests derive repository inputs from their original __file__;
renaming or relocating those helpers changes their meaning. The original GHR
candidate collection failed before its declared tests could run.

GHR already has a reviewed owner-equivalent operation that qualifies its original
file. All twelve installed cells and same-byte publication are reported under
#143/#144. No release is currently blocked on implementing a new shared API.
The remaining provider question is whether to receive the independently useful
original-path operation in the shared SDK, reducing a qualified local equivalent.

## Inspected evidence

- Producer source 5a48759a399a17a16d923851b32519983a836f5f, run 40143062622.
- File gh-run-receptor-1.3.0-py_0.tar.bz2, SHA256
  65f33b29dad70eb9e779f917e4c553d27effa4fddc2740a0260d259866746fd3.
- Original installed collection failure 40143357716 remains failed.
- Owner-equivalent installed_test_helpers.py is inspected at administrative
  qualification source 08b83a0e853aff5c563ad9b19d0ddffb15e030f8.
- Original successful twelve-cell qualification 40144989781 and promotion
  40145282787 remain owner evidence in this study, not independently rerun here.
- Existing shared owners are installed_test_support.py, installed_noarch.py,
  installed_imports.py and noarch_conda.py. Support @1 stages copies; its serial
  provenance hooks and exact-file guards remain useful existing operations.

The equivalent binds reviewed devtools/tests namespaces at original paths and
checks loaded helper origins/hashes. Its controlled sys.path list blocks and
records two legacy source-root insertion attempts. This is trusted owner test
code, not a hostile-code sandbox. Its fixed namespaces and consumer orchestration
are local choices to generalize deliberately, not copy unchanged into every repo.

## Proposed compatible implementation

Add an explicit optional original-path administrative helper profile to the
shared installed-test runner. Keep current @1 and undeclared/default behavior.
Retain the producer's immutable test selection and source/file identities.
A reviewed qualification-side descriptor permits this capability for an existing
candidate without modifying the producer snapshot or rebuilding its archive.
The descriptor is itself tied to an immutable qualification commit and digest;
its exact schema/CLI names are implementation work after this decision.

The proposed descriptor names the original candidate SHA, qualification SHA,
provider SHA, rationale, selected nonruntime namespace roots and the complete
committed Python file/hash inventory. Artifact/run identity remains separate
context and is independently verified by the existing exact-file workflow.
No automatic discovery or blanket exposure of a checkout is accepted.

Required controls:

1. Verify exact producer checkout and declared committed paths/bytes; reject
   symlinks, untracked Python aliases, traversal, case collisions and oversized
   declarations. Preserve original helper __file__ and sibling reads.
2. Reject runtime, stdlib, pytest and SDK/tool namespace collisions, including
   preloaded/resolvable ownership. Execute this profile in a fresh isolated
   interpreter with the SDK's own imports distinct from consumer devtools.
3. Never add the producer/runtime source root to sys.path. Block and report the
   reviewed legacy insertion attempts; fail if isolation/bindings are replaced.
   Existing installed runtime/resource checks run before/after helper binding
   and the unchanged tests. This is provenance checking, not hostile isolation.
4. Audit loaded helper locations and original bytes on success and failure.
   Retire only owned bindings and restore owned path state; preserve caller or
   foreign modules and expose validation/cleanup failures with original errors.
5. Keep serial in-process execution and existing nonempty test-selection rules.
   Retain a bounded success/failure receipt with source/qualification/provider,
   original file/digest, loaded modules, blocked attempts and cleanup outcome.
6. Make descriptor absence preserve current behavior; reject conflicting support
   profiles rather than silently weakening @1 or choosing another namespace.

The operation belongs in its shared provider with its own contract and tests;
the installed workflow calls it. Consumer-specific selection/qualification
choices stay local. A reviewed GHR pilot precedes removing its equivalent.

## Alternatives and refuted paths

- Keep the existing qualified GHR equivalent: lowest immediate change, with
  explicit owner/review/removal condition, at the cost of local maintenance.
- Extend shared support optionally (recommended): reuse the existing installed
  runner/provenance operations and qualify the original-path operation once.
- Adding the producer root to PYTHONPATH, dropping administrative tests,
  relocating path-sensitive helpers or rebuilding to obtain green breaks the
  required qualification identity or scope and is rejected.

## Applicability, consumers and notices

This is an optional qualification capability for genuine original-path
administrative tests, not a mandatory component convention. GHR is the concrete
receiver; other components need no helper declaration or automatic caller bump.

The maintained conda_publishers.json inventory currently records shared-noarch
publication consumers ArgDigest, Pytest Receptor, GH Run Receptor, TopoMT,
PharmacophoreMT, ElastNetMT, DockingMT, Ackredit and LinDelInt. This is a potential
shared-provider impact set, not proof that nine installed callers need this helper
mode. Recheck actual recorded calls and helper users before a provider rollout.
Use #144 as the impact issue; hand the proposed immutable provider revision,
compatibility/default evidence and adoption criteria to concrete affected owners
before publication/adoption. Keep notices, source adoption and installed receiving
separate. No guide/caller/policy pin is changed by this study.

## Acceptance criteria if implementation is selected

- Accept/document the opt-in contract and owner SDK API; preserve existing @1
  byte/origin/namespace/cleanup controls and all undeclared/default tests.
- Add meaningful fresh-process tests for real original-path sibling reads,
  immutable bytes/paths, collisions, root-insertion blocking, failure cleanup,
  preserved caller modules and unchanged installed-runtime origin before/after.
- Exercise the full original GHR selection against its registered unchanged
  artifact using a separately reviewed qualification workflow. Existing original
  producer/source/file/digest remain fixed; no package rebuild/public mutation.
- Qualify all claimed Linux/macOS arm64/Windows and Python 3.11–3.14 cells before
  retiring the local equivalent. Earlier failed/native/public receipts stay intact.
- Notify/adopt through the registered owning issues; record an accepted shared
  guard or an explicit decision to retain the bounded local equivalent.

## Owner follow-up and exclusions

GHR #60/#72 retains the local equivalent and its 2026-11-07 review target until
shared receiving passes. Earlier successful publication does not itself settle
this provider-interface proposal. MolSysSuite owns the shared API decision.
No MolSysMT work, scientific suite/model execution, new package, publication,
new Action, automatic component rollout or shared-environment repair is requested.

## Provenance

2026-10-29, Linux, named molsyssuite@uibcdf_3.14 Python 3.14.7; local receptor
origins verified. Twelve known inherited dependency findings are preserved.
Inspection uses committed source objects and existing issue/native receipts;
no consumer source or scientific environment is mutated by this study.
