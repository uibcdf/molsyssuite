---
summary: Coordinate optional DeclaredRegistry admission, guide delivery and MolSysMT receiving.
issue: uibcdf/molsyssuite#115
status: partial
opened: 2026-10-10
closed:
verification: measured
area: [governance, compatibility, distribution]
guard:
normative: devguide/cross_component_feedback.md
blocked_by: [uibcdf/molsysmt#382]
supersedes: []
---

# DepDigest declaration-based registry receiving

**Reported:** 2026-10-10 by DepDigest, following ElastNetMT's first-use evidence.
**Status:** Partial: public provider admission and all ten guide deliveries
verified; MolSysMT receiving remains owner-scoped and pending.

## What

Coordinate the additive `DeclaredRegistry` interface owned by DepDigest under
uibcdf/depdigest#34 and uibcdf/depdigest#35. MolSysMT owns its catalogue/alias wiring, argument and
converter validation, scientific parity and performance under
uibcdf/molsysmt#382. The motivating observations belong to uibcdf/elastnetmt#26.

## How

Use the ten `DEPDIGEST_GUIDE.md` consumers registered in `suite.toml`, the
existing synchronizer, original provider receipts and shared native/public/
archive verifiers. Give actionable owning notices before guide rollout; record
source, delivery, optional API adoption and installed artifacts separately.

Public DepDigest 0.14.0 admits this interface. A component selecting it declares
DepDigest >=0.14.0 after its own receiving review. Existing `LazyRegistry`
callers retain their supported provider floors and need no automatic migration.
Source experiments identify an exact immutable provider revision.

## Why

The previous first-access scan loads eligible adapters even for one known form.
Declarations let metadata inspection enumerate known identities and value lookup
load the requested implementation. That shared capability belongs to DepDigest;
catalogue parsing and scientific conversion remain host-owned. Guide delivery
makes the admitted capability available without selecting an adoption for hosts.

## What is measured and what is assumed

Original public version/tag: 0.14.0 at
`affd73ef04070a9bf492173c0db615292a73e5d1`. Original file:
`noarch/depdigest-0.14.0-py_0.tar.bz2`, SHA-256
`3622a95cfb45871c3eed2709b38fc3f5b683b8b73555c1d91253b4b7080737d5`.
Provider closeout and canonical guide source:
`1b746ece24587e920e49ea20f2bfebde7c3efc24`.

Independent read-only receiving on 2026-10-13 verifies:

- Twelve mandatory source cells in run 38059326760 and policy 38059299168
  against the original candidate/workflows and executed declared steps. The
  manual source run's inapplicable nightly detector is skipped; this does not
  establish skipped-commit recovery or zero backlog.
- Original producer 38059892340, attempt-qualified ZIP digests and both route/
  producer receipts, using the unchanged provider receipt verifier.
- All twelve installed smoke cells and producer preparation in 38060431615,
  with exact source/title/current attempt and required executed steps.
- Same-file staging-to-main promotion 38063846322 and its original receipt,
  public tag/release, current main label/solver index and downloaded archive.
  The shared archive verifier confirms embedded identity/version, declared
  dependency bounds, Python payload and required resources including registry.py.

The original hosted source result retains 234 passed / 5 optional sibling-
workspace skips; local 239/0 and the provider's clean public Linux installation
are owner measurements, not repeated centrally. Installed smoke is not full
installed pytest. These results prove provider delivery and selective-loading
contracts, not a MolSysMT conversion-parity result or consumer speedup.

The durable receiving/delivery receipt is
`devguide/rollouts/depdigest_declared_registry_115_20261013.json`.

## Alternatives and refuted paths

- Treating the older public 0.13.0 as providing this API would admit a missing
  capability; the floor applies only to clients selecting the new interface.
- Copying a private registry into MolSysMT would bypass provider ownership.
- Rebuilding or rerunning a published candidate would replace original evidence.
- Guide equality alone cannot establish API use or consumer scientific parity.

## Scope and exclusions

Provider admission reconciliation, registered guide delivery and owner handoffs
are central work. Consumer source/defaults/dependency floors and release choices
stay local. Ackredit's grouped entry-point discovery/freshness request remains
uibcdf/depdigest#31; this feature does not resolve it. Existing component science
deferrals, early maturity, full-suite debt, policy tags and package files retain
their existing scope.

## Acceptance criteria

1. Admit the public provider only with exact source/file and executed original
   source/installed/public evidence: verified.
2. Deliver the canonical versioned guide through the registered synchronizer
   and record actionable notices and exact delivery/check commits: complete.
3. Record MolSysMT's explicit owner receiving/adoption outcome under
   uibcdf/molsysmt#382;
   leave its scientific parity and performance interpretation with its team:
   pending. Other guide recipients remain optional candidate users.

The existing shared-provider notice contract is the durable normative guard.
Keep #115 partial until the declared coordination conditions are met.

## Local implementation issues

- uibcdf/depdigest#34: declaration-based registry source implementation, closed.
- uibcdf/depdigest#35: original public 0.14.0 delivery, closed.
- uibcdf/molsysmt#382: concrete consumer receiving, open.
- uibcdf/elastnetmt#26: motivating first-use evidence and owned native integration.
- uibcdf/depdigest#31: separate Ackredit discovery/freshness capability, open.

## Dependencies and risks

MolSysMT receiving remains a tracked dependency. Dynamic overrides, visibility,
failures/retries, metadata freshness and explicit undeclared discovery follow
the published provider contract; enumeration and materialization differ.
Synchronous loading supplies no new concurrency guarantee. A source or guide
copy does not qualify later candidate artifacts or a default runtime migration.

## Provenance

2026-10-13; qualified Linux Python 3.14.7 interpreter with both local receptor
origins verified. Seven accepted local dependency conflicts remain visible under
uibcdf/molsyssuite#82. Original native runs and artifacts are acquired without
new scientific/installed dispatches. Ten isolated consumer clones preserve
primary worktrees; task-owned temporary sources, archive and metadata are removed
after durable receipt, applicable governance gates and owning handoffs.

## Registered guide delivery — 2026-10-13

All ten notices precede rollout. The existing synchronizer produced byte-identical
root copies in isolated clones. All local report/index and central conformance
checks pass. Each focused guide-only commit used the conditional internal skip
with explicit manual exact-head policy qualification; no administrative result
clears scientific backlog. MolSysViewer also executes its dependency metadata
audit. The original public provider and all member dependency/runtime files
retain their identities.

| Consumer | Delivery commit | Exact manual policy |
| --- | --- | --- |
| uibcdf/argdigest | `b9dc46c6306db09b788ed17921d2d81f151d16ac` | [run 38369956094](https://github.com/uibcdf/argdigest/actions/runs/38369956094) |
| uibcdf/pyunitwizard | `f117e5b36083d063517334337f060c3a439819ca` | [run 38369972708](https://github.com/uibcdf/pyunitwizard/actions/runs/38369972708) |
| uibcdf/molsysmt | `e134bd104c93bf0fa3a43516e737d16314d76e05` | [run 38370243983](https://github.com/uibcdf/molsysmt/actions/runs/38370243983) |
| uibcdf/molsysviewer | `ef52674a5857fca6541b69c0e84713ef02992de6` | [run 38370256022](https://github.com/uibcdf/molsysviewer/actions/runs/38370256022) |
| uibcdf/topomt | `f1ca466ae2e1f7e416726ae80d53221dca71b289` | [run 38370266815](https://github.com/uibcdf/topomt/actions/runs/38370266815) |
| uibcdf/pharmacophoremt | `7b346dd6e3285270c76c372d699e2e7a9239e966` | [run 38370277927](https://github.com/uibcdf/pharmacophoremt/actions/runs/38370277927) |
| uibcdf/elastnetmt | `b944d050ff6b9f56bd9b8f993461c26c52cf2b7c` | [run 38370289216](https://github.com/uibcdf/elastnetmt/actions/runs/38370289216) |
| uibcdf/lindelint | `86f8f953df56bcf8b74f947b2954e93407d8bd28` | [run 38370300712](https://github.com/uibcdf/lindelint/actions/runs/38370300712) |
| uibcdf/ackredit | `430afefeabd97d8346d7d44eb3ce18cafe2dc77a` | [run 38370311263](https://github.com/uibcdf/ackredit/actions/runs/38370311263) |
| uibcdf/dockingmt | `415d61c69ab34943579c52bb073626952c8c6a8e` | [run 38370321393](https://github.com/uibcdf/dockingmt/actions/runs/38370321393) |

HTTPS push authentication was corrected only in the scratch clone. MolSysMT
advanced concurrently; only the unpublished guide commit was rebased over its
new native fixes, then rechecked and pushed without force. Primary clones and
caller-owned environment/resources were not edited.

Ten delivered guides expose an optional admitted capability. They do not
establish ten runtime users or a MolSysMT speedup; #115 stays partial for
uibcdf/molsysmt#382. Ackredit grouped discovery remains a separate request.

## Coordination closeout — 2026-10-13

All ten owning handoffs now include their exact copy/check commits and the
central receipt. Published checkpoint `c5d9da7f9375b71ac467743b837dce5f16f49b22`
passes exact central CI 38371030578, independently acquired for source, push
event, current attempt, complete job inventory and every declared step.

The task-owned eleven isolated sources, downloaded original archive and
metadata/scripts are removed after namespace ownership, exact-head/clean-state
and completed-operation checks. No cleanup failure. Durable source/digest/run/
notice evidence stays in the central receipt; caller resources remain outside
this removal. The central issue remains partial for the explicit MolSysMT
receiving condition.
