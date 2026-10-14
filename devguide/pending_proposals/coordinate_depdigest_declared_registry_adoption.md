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
**Status:** Partial: public 0.14.0 registry, 0.15.0 adapter-inspection and 0.15.1
bounded concurrent-reader identities verified. Current guide deliveries pass
exact-source manual governance; hosted step evidence is tracked in #118.
MolSysMT receiving remains owner-scoped and pending.

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
stay local. Ackredit's separate grouped discovery assessment under
uibcdf/depdigest#31 is now closed: retain standard-library fresh queries, without
a new DepDigest API, persistent cache or dependency floor. Existing component science
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
- uibcdf/depdigest#36: optional adapter-inspection implementation, closed.
- uibcdf/depdigest#37: public 0.15.0 delivery, closed.
- uibcdf/depdigest#31: completed Ackredit discovery/freshness assessment;
  consumer uibcdf/ackredit#117 closed, existing standard-library owner retained.

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


## Admitted adapter inspection and current guide delivery — 2026-10-13

Public DepDigest 0.15.0 adds explicit `DeclaredRegistry(load_policy="adapter")`
at tag/candidate `01d83c7b176a2b6cdcbdb42d33f3060f2eda5af7`. Original file
`noarch/depdigest-0.15.0-py_0.tar.bz2` has SHA-256
`5b888794367e7cd2fd24eac23471b1d26bcbbdfe4d2a14cf77a53f104a110d98`.
The base registry floor remains >=0.14.0; selecting the adapter policy requires
>=0.15.0. Existing strict/`LazyRegistry` behavior requires no automatic upgrade.

The explicit policy permits loading requested importable Python adapter metadata
without its optional engine. Current visibility still hides absent-engine adapters
in restricted mode, including cached ones; all-capability mode can inspect metadata.
Identity, failure provenance/caching/retry/refresh and execution guards remain.
Importability is not engine availability, conversion/scientific parity or speed.
Host catalogue/aliases/converter validation and actual execution remain local.

Independent receiving reacquires twelve source cells in 38415352585, attempt 2,
source/tag policy 38415275687/38417378234, original producer 38416272276 and
both attempt-qualified ZIP receipts, thirteen-job installed run 38416982119,
and promotion 38417506809 with both the promotion receipt and checked route.
The initial source attempt's pre-test micromamba download failure is retained;
no candidate or package repair is inferred from the successful same-source rerun.
The installed gate is twelve smoke/contract cells, not full installed pytest.
The immutable annotated tag, public main solver/index and downloaded archive
match the original digest; all fourteen inventoried resource hashes match the
owner's normalized release receipt. Fresh public installation and source-snapshot
DOI verification remain separately attributed to the provider's original evidence;
they are not rerun or upgraded to consumer qualification centrally.

The initial local reader assumed one promotion JSON, while the committed
workflow bundles promotion plus checked route. The review verifies both explicit
members and their candidate/gate bindings; no provider fix or artifact mutation
was needed. A concurrent provider advance was incorporated only in the clean
scratch clone, with unchanged canonical guide bytes and a repeated source preflight.

Ten existing owning notices were updated before rollout. Canonical source
`69f152b22c5a8fe9c9890ea1ee1fbee76512a9c2` is delivered through the registered
synchronizer. Each delivery changes solely `DEPDIGEST_GUIDE.md`, passes local
index/conformance/whitespace checks and exact-source manual policy. Viewer also
executes its metadata audit. Documentary conditional skips retain scientific debt;
no runtime/floor/fixed-pin edits, scientific or installed dispatch, release decision,
package operation or shared environment change occurred.

| Consumer | Current guide commit | Exact manual policy |
| --- | --- | --- |
| uibcdf/argdigest | `fd746072f4ea98350d85d9aad1affba79c698b1b` | [run 38424516279](https://github.com/uibcdf/argdigest/actions/runs/38424516279) |
| uibcdf/pyunitwizard | `3813efb3c1f156d313a94fa49ff03e20300745ec` | [run 38424528906](https://github.com/uibcdf/pyunitwizard/actions/runs/38424528906) |
| uibcdf/molsysmt | `216ba5c6fdce98b586fdae4773aa06f6ab8003fb` | [run 38424542825](https://github.com/uibcdf/molsysmt/actions/runs/38424542825) |
| uibcdf/molsysviewer | `76c8cee1b2f00821820e05975609262844b27224` | [run 38424554069](https://github.com/uibcdf/molsysviewer/actions/runs/38424554069) |
| uibcdf/topomt | `06da0f5947c2ee21f011b8eb5d62260aeec1cb0d` | [run 38424565936](https://github.com/uibcdf/topomt/actions/runs/38424565936) |
| uibcdf/pharmacophoremt | `944a78cac28028b8f0e3167558802cb67dca5808` | [run 38424577511](https://github.com/uibcdf/pharmacophoremt/actions/runs/38424577511) |
| uibcdf/elastnetmt | `d83ff0c5c03f6cecd38a01d37b014fe32044951e` | [run 38424592166](https://github.com/uibcdf/elastnetmt/actions/runs/38424592166) |
| uibcdf/lindelint | `d34db8a56e35e25c770d6cb62cbe3111c6a36391` | [run 38424606190](https://github.com/uibcdf/lindelint/actions/runs/38424606190) |
| uibcdf/ackredit | `e124bd5dea82d2d340ae496db8c9abe2b8f3ff36` | [run 38424619129](https://github.com/uibcdf/ackredit/actions/runs/38424619129) |
| uibcdf/dockingmt | `32669322d034ea3e86d1e428f10a27f74c44123c` | [run 38424631596](https://github.com/uibcdf/dockingmt/actions/runs/38424631596) |

The current [adapter receiving receipt](../rollouts/depdigest_adapter_registry_115_20261013.json)
retains provider/source/file/run identities and all ten current copies. The original
0.14.0 receiving/delivery receipt and archive bytes remain unchanged; the earlier
copy table is historical. MolSysMT uibcdf/molsysmt#382 remains open for its own
adoption/conversion/scientific/performance disposition.

Separately, uibcdf/depdigest#31 and uibcdf/ackredit#117 are closed after the provider
assessment at `5744450a0778eb2d801cabd95d61ccda092a823b`: retain
`importlib.metadata.entry_points` with fresh independent first-demand/reload queries.
A simultaneous native snapshot may batch demands only without intervening registration.
No faster single-demand contract, persistent cache, new runtime API or dependency
floor is selected. The owner measurement and compatibility guards keep their scope.
DepDigest's closed resource review uibcdf/depdigest#33 is reconciled independently
under uibcdf/molsyssuite#104; guide delivery does not prove resource compliance.

### 0.15.0 coordination closeout

Published receiving/resource checkpoint
`ead8e5366ddab5e36c2a7c00e89a43cc55f01aea` passes exact central CI
38426337134, independently verified for source, push event, workflow/current
attempt, both jobs and every declared executed step. Ten current handoffs now
carry their copy/policy evidence and immutable central receipt links. #115 remains
partial for the unchanged uibcdf/molsysmt#382 receiving criterion.

After durable publication, completed gates and handoffs, the task's exact root
was removed: eleven clean expected-head clones, the original downloaded file
and task metadata. Explicit top-level inventory and UID checks covered 15718
paths; symlink targets were not followed and no cleanup error occurred. Primary
clones, shared environment, caller/human work and original release evidence remain
outside that disposal. The current receipt retains proof and retirement state.

## Public concurrent-reader capability — 0.15.1, 2026-10-13

DepDigest #39 is closed by its owner. Stable annotated tag/release identifies
`13cc73780a7cb645546ae3f396177f98b86a8792`; public
`noarch/depdigest-0.15.1-py_0.tar.bz2`, SHA-256
`2765c692de4e6aacff4197c4226ebb42ec1f0df9edb27e92f196ef1390cb1850`.
Independent native review verifies twelve source cells in 38459369859 and
policy 38459370795, original staged producer 38461660471, the thirteen-job
exact-file installed smoke 38462313607 and same-file promoter 38462737850.
Original route/distribution/promotion/public JSON artifact ZIP digests, tag/main
solver identity and downloaded archive match. Sixteen non-generated runtime
Python files match the original candidate. Local-publisher inspection uses its
immutable project bounds and resource inventory; it does not claim adoption of
the shared release-plan schema or a full installed pytest suite.

From >=0.15.1, overlapping declared value requests serialize within one registry,
sharing one initialization/value/failure while preserving genuine recursion
refusal, strict/adapter behavior, visibility and selective loading. Independent
mutation/discovery/retry/refresh/configuration needs external coordination;
initializers must not wait for another thread needing that registry. Arbitrary
cyclic interactions and consumer throughput/scientific parity are outside scope.
`LazyRegistry` and original 0.14.0/0.15.0 identities remain unchanged. A client
using older APIs need not change its floor merely because this version exists.

All ten registered DepDigest copies now match canonical 0.15.1 bytes, delivered
with SMonitor 0.20.0 through twenty-one registered relationships and eleven
guide-only commits. Owning advance notices retain source/copy hashes and the
chosen capability floors. Current copy commits pass exact-source manual checks
using their immutable policy versions and Ruff 0.16.5, including Viewer's
metadata audit. Hosted success with absent step arrays is explicitly unverified
under uibcdf/molsyssuite#118; no native executed-step success is fabricated.

[Current public receiving/delivery receipt](../rollouts/providers_public_guides_106_115_20261013.json).
MolSysMT #382 retains adoption, conversion/scientific parity and performance.
No consumer floor/pin/runtime change, scientific dispatch, build, promotion or
shared-environment update was made. The issue remains partial for its unchanged
owner receiving criterion.

## Prior guide/native evidence recovered — 2026-10-14

The eleven original joint SMonitor 0.20.0/DepDigest 0.15.1 guide-delivery runs
now expose complete executed steps and independently pass exact
source/workflow/event/attempt verification, including Viewer's metadata audit.
The two central governance runs and original SMonitor 0.20.0 promoter also
recover under #118. This supersedes the earlier current-unverified native limit;
original dated snapshots/manual administrative controls remain retained.
No guide copy, DepDigest artifact/floor or MolSysMT adoption changed. #115 stays
partial for MolSysMT #382. [Recovery receipt](../rollouts/native_evidence_recovery_118_20261014.json).
