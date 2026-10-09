---
summary: Coordinate opt-in scoped diagnostic capabilities and separate guide delivery from consumer qualification.
issue: uibcdf/molsyssuite#106
status: partial
opened: 2026-10-06
closed:
verification: measured
area: [governance, compatibility, diagnostics]
guard:
normative: devguide/cross_component_feedback.md
blocked_by: []
supersedes: []
---

# Scoped diagnostics and provider registration: receiving coordination

**Reported:** Recorda's direct MOLI consumer review exposed reusable provider limits;
DockingMT subsequently reproduced stale provider-guide copies.
**Status:** Public provider outcomes and canonical-guide delivery are recorded;
two bounded optional receiving dispositions are settled as of 2026-10-09;
nine remain owner-scoped and pending.

## What

Coordinate suite-member applicability, compatibility and handoffs for the additive
SMonitor registration/scoped-capture and ArgDigest instrumentation/pipeline APIs.
Recorda remains directly governed by MOLI. Provider implementation, release choices,
and each member's receiving/runtime selection retain their owning repositories.

The opening proposals are now delivered publicly: SMonitor 0.19.0 under
uibcdf/smonitor#35/#37/#38 and ArgDigest 0.15.0 under uibcdf/argdigest#29/#30/#31.
The original Recorda probes against SMonitor 0.18.0 / ArgDigest 0.14.0 describe earlier
limitations; they are not evidence that these later APIs are still unimplemented.

## How

Use the registered guide inventory and review issues in `suite.toml`. The review
identified eleven committed callers of `ensure_configured` in package initialization,
eleven SMonitor-guide consumers, and seven ArgDigest-guide consumers. The caller
inventory records source commits, paths, content digests and observed lines. Inspection
establishes helper use, not application-policy preservation for an arbitrary installed
provider or opt-in scoped-runtime adoption.

All eighteen committed copies differed from current canonical guides. The SMonitor
canonical guide additionally advertised the new registration/scoped promises while
identifying version 0.17.0. The owner repaired that misleading boundary in
uibcdf/smonitor#45: version 0.19.0, explicit public capability floor, earlier-provider
compatibility and bounded opt-in scope. ArgDigest's canonical guide already identifies
0.15.0 and the optional SMonitor 0.19.0 scoped capability requirement.

Advance impact notices precede provider publication/consumer rollout. The only source
change is SMonitor's canonical guide; the registered synchronizer delivers byte-identical
root copies in isolated clones. Reviewed caller pins, runtime source, dependency floors,
configuration, package files, publication workflows and primary clones remain as found.
The receipt records immutable provider/copy commits, guide digests, local checks,
executed exact-head native gates, concurrency reconciliation and owning notices.

## Why

A guide that associates new capabilities with an older provider can lead consumers to
rely on guarantees their declared lower bound does not supply. Stale copies also hide
available reusable capabilities. Delivery gives maintainers an actionable versioned
contract without selecting a migration for them or imposing a new suite-wide minimum.

## What is measured and what is assumed

The durable receipt is
`devguide/rollouts/scoped_diagnostics_guide_delivery_106_20261008.json`.

Existing original public-byte qualification is retained separately:

- SMonitor 0.19.0 build 1: source `f604b940ab281df4554869fdd24f796ea6d42c27`,
  SHA-256 `4b876b4993b1e2caeed40851402a931f3b245ed7c1916d9483d81bc90274e31c`,
  receipt `devguide/rollouts/smonitor_public_0_19_0_45_20261006.json`.
- ArgDigest 0.15.0 build 0: original source
  `57447cc4ec1f7ce85078f8a939892efd075bc919`, SHA-256
  `b0f22038a8ad1c888dca10adedaca0fa14d2383a685a97c0602b7ca05f29d6a1`,
  receipt `devguide/rollouts/argdigest_public_0_15_0_45_20261006.json`.
  The full installed matrix exercises scoped cases with public SMonitor 0.19.0;
  the separate NumPy-free core matrix preserves earlier supported provider floors.
  The additive operator profile under uibcdf/molsyssuite#92 records that evidence
  without replacing the older 0.14.0 profile or republishing bytes.

Ackredit's uibcdf/ackredit#119 handoff is bounded actual receiving evidence for the
selected public providers, original public Ackredit 0.11.0 and a separately installed
current-runtime wheel. Its original sources/environments/three receiving guards remain
in that owner issue and the dated #106 comment; it is not a fresh qualification of
every later main commit, every suite member or another release. DockingMT's
uibcdf/dockingmt#42 evidence is a local unpublished source composition, explicitly
separate from scoped-policy adoption and its hosted/public receiving obligations.

Local checks cover current conformance and each component's report/index controls.
SMonitor's actual reporting selector executes 111 tests with one existing skip; an
initial nonexistent guessed selector executed no tests and was replaced by the actual
`tests/test_devguide_reports.py`. Consumer reporting checks execute 215 tests in total.
MolSysMT's checks validate developer/archive/API/evidence registry structure and do not
execute scientific evidence tests. Native policy checks independently verify the exact
commits, workflow identities, attempts, required jobs and executed steps. Backlog-only
probes additionally assert that scientific matrix jobs were skipped. Guide-only interim
skip commits use the authorized manual gate route; administrative success does not
clear pending full-suite debt.

## Compatibility and member action

Detailed diagnostic defaults and native diagnostic/error identities remain available.
A consumer relying on application-policy-preserving setup, declaration-only registration
or scoped capture selects the documented public capability floor and tests its chosen
use. An earlier supported provider retains its released behavior; merely copying the
guide does not extend that provider's guarantees. Explicit restrictive ArgDigest capture
on an unavailable provider fails safely rather than silently weakening the policy.

Each owner decides whether/when to adopt. If selected, record its provider/file/source
identity and test import order, application-policy preservation, configured catalog and
explicit-audience rendering where used, scope precedence/owned payload suppression,
retained pipelines/contracts and native exception/cause identity as applicable. Scope
covers documented owned capture paths, not arbitrary third-party code or all user
formatting. No global redaction guarantee or new common dependency floor is introduced.

## Alternatives and refuted paths

Editing consumer copies bypasses canonical ownership and was not used. Changing all
runtime minima, bootstrap policies or activating scopes would require component decisions
and receiving proof beyond a guide delivery. Administrative gates cannot substitute for
that proof. Rebuilding public artifacts would invalidate the original exact-byte evidence
and was not needed. Earlier ArgDigest profile bindings remain historical identities.

## Scope and exclusions

This coordination does not alter unit authority/interchange (uibcdf/molsyssuite#18/#46),
previous ArgDigest 0.14.0 receiving (uibcdf/molsyssuite#98), broad action v2.3.0 adoption
(#87), internal direct-push policies, scientific algorithms, browser tests or package
publication. Direct MOLI/Recorda notices use uibcdf/moli#62 and uibcdf/recorda#2.

## Acceptance and remaining ownership

Completed: provider public outcomes reconciled, inspected member caller/guide inventory,
misleading canonical version repaired by its owner, current guides delivered through the
registered tool, applicable administrative evidence and actionable immutable handoffs.

The issue remains partial for receiver dispositions not yet recorded. Optional adoption
is not required simply to make this issue green. Each registered owner issue can record
adopted, deferred with reason/review, or not applicable, and retain receiving proof for an
actually selected path. Central coordination may close when those scoped dispositions
are explicit; it must not claim every member migrated from guide delivery alone.

Local receiving homes: uibcdf/argdigest#20, uibcdf/depdigest#18,
uibcdf/pyunitwizard#89, uibcdf/molsysmt#244, uibcdf/molsysviewer#110,
uibcdf/topomt#56, uibcdf/pharmacophoremt#6, uibcdf/elastnetmt#14,
uibcdf/lindelint#9, uibcdf/ackredit#72 and uibcdf/dockingmt#19.
Closed historical qualifications remain closed; a guide notice does not reopen them.
The existing receiving/compatibility owner can choose a separate local issue for a new
implementation without transferring component code to the central repository.

## Provenance and resource lifecycle

Review/delivery: 2026-10-08, Linux x86_64, qualified `molsyssuite@uibcdf_3.14`,
Python 3.14.7, eligible local receptor import origins retained. Accepted workspace
conflicts remain under uibcdf/molsyssuite#82; no dependency solve is performed here.
Primary clones and the caller-owned environment are preserved. The task-owned isolated
source/consumer clones and generated caches are removed after immutable receipt and
handoffs; any failure or specifically retained resource is reported at closeout.

## Bounded receiver dispositions — 2026-10-09

The eleven receivers are taken from the registered SMonitor/ArgDigest guide
inventories. All owning issues were read again. Their latest guide notices
remain delivery evidence; closed older reviews do not establish a new scoped
outcome. Two established owner outcomes now have explicit receiving dispositions:

| Receiver | Disposition | Evidence and boundary |
| --- | --- | --- |
| ArgDigest | Adopted for its optional owned capture/pipeline paths | uibcdf/argdigest#29/#30/#31; public 0.15.0's original twelve installed cells require scoped cases with SMonitor 0.19.0, while twelve minimal-core cells preserve lower-provider behavior/refusal. Original independent #45/#92 receipts retained. |
| Ackredit | Adopted for the selected optional receiving paths | uibcdf/ackredit#119; original public Ackredit 0.11.0 and a separate unpublished normally installed runtime wheel, Linux x86_64/Python 3.14.8. |

ArgDigest's actual capture/argument-selection/core guard sources were inspected
at original public producer `57447cc4ec1f7ce85078f8a939892efd075bc919`.
The published archive digest, original installed run 37525789576 and core run
37525794773 remain those independently reviewed under #45/#92. This review
uses that existing qualification; it does not dispatch tests, requalify a later
main, activate restrictive defaults or impose a new floor on other consumers.

Ackredit's original checkpoint is
`eb9f52f1ec9f0425e1a7549f4dc615ecb6235a1b`. Its three original isolated
receiving guards run against the untouched public Ackredit interpreter and
the separate runtime wheel. They retain configured application-policy identity,
idempotent catalog/provider registration, explicit-audience rendering, owned
capture suppression, active normalization/argument/binding refusals, original
native exception/cause identity and exact independent saved readers. Its
candidate file/identity maps agree before and after testing. The original local
370-case outcome retains the initial restricted-network build failure and the
unchanged one-case recovery; it is not rewritten as one uninterrupted green run.

Read-only native verification independently confirms Ackredit's original
CI 37530510968 against the exact source, workflow, push event, attempt, seven
actual jobs and required executed steps. That confirms original source CI;
it does not reproduce the local public probes or infer that optional cases
execute without skips in every routine cell. Pipeline-only selection remains
fixture-only and Ackredit's runtime defaults/dependency floors are unchanged.
Explicitly supplied metadata and arbitrary third-party code are outside the
owned-capture guarantee. No broader platform/minor/performance claim follows.

**Two settled / nine pending:** DepDigest, PyUnitWizard, MolSysMT, MolSysViewer,
TopoMT, PharmacophoreMT, ElastNetMT, LinDelINT and DockingMT still need an explicit
owner-selected applicability/receiving disposition. Existing actionable guide
handoffs remain their review route; no duplicate reminder or new issue is needed
for an unanswered notice. MolSysMT/Viewer deferrals and early-component maturity
are preserved. No consumer activation or scientific test is requested centrally.

Receipt: [diagnostic_receiving_dispositions_98_106_20261009.json](../rollouts/diagnostic_receiving_dispositions_98_106_20261009.json).
Broad ecosystem adoption statuses, original public artifact receipts and prior
guide deliveries are unchanged. Task resources are only small issue/evidence
snapshots; retire them after durable publication, exact central CI and focused
owning/coordination handoffs. No primary clone or shared environment is changed.
