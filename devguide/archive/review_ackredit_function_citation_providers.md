---
summary: Review provisional dependency-free function declarations and explicit Ackredit observation before stable adoption.
issue: uibcdf/molsyssuite#97
status: resolved
opened: 2026-10-04
closed: 2026-10-08
verification: measured
area: [governance, compatibility, provenance]
guard:
normative: devguide/ackredit_client_policy.md
blocked_by: []
supersedes: []
---

# Review provisional function citation providers

## Current review — 2026-10-08

Provider-owned public promises have advanced beyond the earlier provisional
central decision: portable attribution remains >=0.9.0; accepted provider
signatures/interpretation are delivered from >=0.11.0; bounded recorder evidence
and standalone validation are delivered from >=0.12.0. General public 1.x awaits
separately qualified 1.0.0. This records the owner's decisions, not a new suite
requirement or automatic central stable adoption. The principal maintainer accepted the scoped optional disposition on 2026-10-08.
#97 resolves the accepted bounded review and guide coordination: all six copies
are delivered, ten exact-head administrative workflows are independently verified,
and owning handoffs are delivered. Runtime integration remains consumer-owned.
Earlier sections retain dated source, delivery and provisional-decision history.

## What

Ackredit implements a dependency-free module/function declaration protocol and
explicit `observe_calls(*modules)` context under uibcdf/ackredit#84 and #85.
The declaration schema `ackredit.provider@1` and observation API are provisional,
initially published in development source `536bd87ec395cf8abfd18a14c4d24dc71ad88980`.
The synthetic-fixture repair is `b67ea77981e8c68a8b0eb42b8814178cdd8d88e9`.
The latest independently reviewed receiving checkpoint is Ackredit
`1a5dd4566737f6195571b4cb421af6f01647c5f6` with PyUnitWizard
`33fec8a627505a4f5426babe87e8e85438105041`: eight installed cells, six
tests each. The prior `fc00a6cf` checkpoint is retained below. PyUnitWizard
accepts its bounded experimental pilot in `f34b111`; stable/shared adoption
remains deferred by the maintainer. These wheel identities remain development qualifications.
The corrected public Conda checkpoint is now independently reviewed below:
Ackredit 0.10.1 at `dd500842b6085111e01e62cfc243f68406eb8cc7`.
Public Ackredit 0.9.0 does not contain this API. No suite adoption is implied.

## How

Review the provider-owned schema, activation/entry semantics, restored exports,
failure diagnostics, concurrency, saved-reader fidelity and measured costs.
Reuse existing portable attribution rather than centralizing another renderer
or result schema. Candidate consumers derive from the six registered Ackredit
guide relationships; Sabueso separately consumes the portable contract. Direct
MOLI consumer review is uibcdf/moli#46. Real receiving owners choose integration
and scientific citations; central review concerns the shared compatibility
boundary and truthful adoption claims.

## Why

Offline declarations allow a producer to work with Ackredit absent. Explicit
entry observation can avoid crediting untaken calls discovered statically.
However, function entry alone neither proves successful scientific completion
nor identifies branches inside that function. Automatic adoption could assign
incorrect references or misstate support for aliases, native code or lazy modules.

## Inspected contract and its policy boundary

This describes the current `fc00a6cf` source. The earlier failed and repaired
synthetic checkpoints are retained in the dated evidence sections below.

- Declarations contain offline bibliography, original software/version and
  contextual use roles. Function attributes attach metadata without changing
  the producer callable. Declaration/import alone earns no credit.
- Application activation selects already imported ordinary modules. It changes
  selected module exports temporarily; observations are context-local and
  leases restore exports. Unrelated contexts may encounter a forwarding wrapper
  while another observer is active; zero cost or unchanged callable identity
  during active patching is not assumed.
- Synchronous entry and awaited coroutine execution record references. Untaken
  calls earn none; a failed scientific call can retain observed entry references.
  A host must distinguish invocation/partial provenance from completed results.
  Attach a scientific criterion only at the meaningful operation actually
  implementing it; inner-function branch selection remains consumer-owned.
- Ordinary modules with declared lazy PEP 562 exports are supported: explicit
  activation resolves only declared names. Producer loader side effects are
  not rolled back if validation fails. Custom module subclasses, pre-activation
  aliases, generators, descriptors, native internal calls and subprocesses
  remain outside the contract. A
  receiver must use supported qualified calls and report its unobserved scope.
- Invalid/conflicting declarations fail before activation with ACKREDIT-E012.
  Attribution failure or export rebinding uses ACKREDIT-W019; original scientific
  results/exceptions are preserved under ordinary warning handling. A consumer's
  explicit warnings-as-errors configuration needs its own failure-policy review.
- The candidate reuses sessions, scope, captures, detached bibliography and
  registry checks. Existing public portable schema and coarse hooks retain
  distinct contracts. Original-version fidelity, reused references and detached
  reading now have a real installed PyUnitWizard receiving checkpoint.
- Provisional `prepare_credit` validates and detaches a fixed explicit use,
  credits nothing during preparation, and writes to current sessions/captures
  on invocation. It rejects replaced/deleted bibliography with ACKREDIT-E010.
  The host owns the completion criterion, call scope and attribution-failure
  handling. PyUnitWizard feature-detects this API and retains the released
  `register_item` / `track_item` fallback when it is absent.

These boundaries fit review under the existing optional client profile:
`devguide/ackredit_client_policy.md` already allows explicit application opt-in
and requires client-owned references, absence/failure behavior and actual
receiving evidence. It does not authorize enabling observers on library import,
mandating Ackredit or treating this provisional schema as a common requirement.
No new normative rule is adopted by this review.

## Initial synthetic checkpoint — historical evidence

Inspected provider sources: `ackredit/core/providers.py`, the public declaration
guide, `tests/test_function_providers.py` and the committed overhead receipt at
the immutable candidate above. The installed fixture test builds Ackredit and
a dependency-free synthetic producer, blocks Ackredit during producer use,
then reads saved attribution with the producer blocked. This is useful provider
evidence but not a real scientific consumer adoption or a public candidate
publication. The reported 1,617 local tests and microsecond timings remain
provider-owned measurements; they were not rerun or generalized here.

Independent installed GH Run Receptor 1.2.0/native review finds exact-candidate
CI 37203629536 failed: Linux/Python 3.13, Linux/Python 3.14 and macOS-arm64/
Python 3.14 each fail the normal-installation fixture at line 421, reporting
`BackendUnavailable: Cannot import 'setuptools.build_meta'`. Each failing
cell records 1,608 passed and seven skipped. The fixture uses
`--no-build-isolation`; both source projects declare that backend. The failure
is observed during installation, before its capture/reader assertions.
Linux/Python 3.11 and 3.12, Ruff and docs pass. Policy 37203629838 and
publication guard 37203629820 pass separately; they do not establish the
failed receiving assertions. Missing `build` is also an observed optional
skip, not the demonstrated cause of that install failure.

The source/test environment need is handed to uibcdf/ackredit#84; central
coordination does not repair the provider or weaken its installation assertion.
Primary native review: `devguide/rollouts/ackredit_function_provider_review_97.json`.
Public 0.9.0's separately qualified package remains unchanged.

## Alternatives and refuted paths

No mandatory observer, interpreter-wide profiling, dependency floor, consumer
rollout or new attribution schema is centrally accepted. The released portable
API and explicit tracking remain the public fallback. No performance guarantee
or stable protocol follows from a synthetic timing or a green policy gate.

## Acceptance criteria

- Retain the provider's immutable declaration, compatibility and release scope.
- Obtain actual installation/reader evidence in the declared candidate lanes;
  resolve the reported provider environment failure without bypassing assertions.
- Obtain a concrete producer and receiver review covering scientific reference
  ownership, supported call paths, failure semantics and relevant overhead.
- Record exact source/package identities and receiving outcomes separately;
  consult the maintainer before any new common requirement or stable adoption.
- Deliver a registered guide change through its existing impact/synchronization
  route only if the provider promotes a consumer-facing contract.

## Scope and exclusions

This is a central review and provider handoff. No six-consumer dependency bump,
code patch, scientific suite, public build or package replacement is performed.
#96's public portable-guide refresh is independently complete. Scientific
implementation and citation choices remain with receiving teams; MolSysMT and
MolSysViewer deferred scientific reviews remain deferred.

## Local implementation issues

uibcdf/ackredit#84 owns declaration/observer implementation and its installed
fixture environment; uibcdf/ackredit#85 owns measured overhead and #87 owns
prepared explicit credit. uibcdf/pyunitwizard#94 owns the concrete receiving
pilot. uibcdf/moli#46 owns its direct receiving
scope without transferring platform authority to MolSysSuite.

## Dependencies and risks

The current development candidate has exact-head hosted real-producer
installation/reader evidence. A maintainer decision and provider-owned
stable contract/release handoff keep #97 partial. A later source change needs
its own exact-head inspection. Do not reuse public 0.9.0 qualification
for this unreleased API or force a consumer to import a private provider engine.

## Provenance

2026-10-04, Linux; administrative Python 3.14.7. The installed public reader is
GH Run Receptor 1.2.0. Metadata was inspected before native failed-step logs;
CI lanes are reported from their actual job/step identities. No local runtime
test or scientific matrix was executed by this central review.


## Independently reviewed repair — 2026-10-04

The provider's corrected checkpoint is
`b67ea77981e8c68a8b0eb42b8814178cdd8d88e9`. Published GH Run Receptor
1.2.0 inspected all three exact-head gates first and reports PASS with
sufficient metadata. Native GitHub jobs/steps corroborate the source CI:
[37204993017](https://github.com/uibcdf/ackredit/actions/runs/37204993017)
passes all seven jobs (Linux/Python 3.11–3.14, macOS arm64/Python 3.14,
Ruff and strict documentation). Every five test cells executes package
installation, installed smoke and `Run tests`; the source selects the complete
test directory outside the checkout. The required producer/reader fixture is
not skipped or marked optional. Policy
[37204993413](https://github.com/uibcdf/ackredit/actions/runs/37204993413)
and publication guard
[37204993439](https://github.com/uibcdf/ackredit/actions/runs/37204993439)
pass on the same immutable candidate.

The inspected repair builds the fixture through a fresh minimal virtual
environment, explicitly checks that Versioningit is absent there, and allows
normal pip build isolation to acquire each project's declared backend.
It removes the failing `--no-build-isolation` dependency on incidental runtime
tooling. The provider implementation hash is unchanged; assertions for the
dependency-free producer, off-checkout consumer and producer-blocked saved
reader remain. The original three failed install cases and their source
identity are retained as historical evidence in the receipt.

This resolves the provider-fixture environment limitation reported by central
review. It proves the synthetic receiving contract on the observed candidate
lanes, with the hosted suite's existing optional-tool skips retained. The
provider's separately reported 1,617 zero-skip local tests and timings remain
provider-owned measurements. No new local runtime tests, component scientific
suite, public package or six-consumer rollout was initiated.

At this synthetic checkpoint, #97 remained partial for a concrete
producer/receiving review and a maintainer decision before stable shared
adoption. `observe_calls` / `ackredit.provider@1`
remain provisional; public Ackredit 0.9.0 and its portable floor are unchanged.
The existing optional client policy and function-entry/failure/alias scope
recorded above still apply. Direct MOLI receiving review remains uibcdf/moli#46.

## Independently reviewed real receiving checkpoint — 2026-10-04

Ackredit delivered an installed PyUnitWizard pilot in
[37217520167](https://github.com/uibcdf/ackredit/actions/runs/37217520167).
GH Run Receptor 1.2.0 and native metadata agree on the exact Ackredit producer
`fc00a6cf1e2426ab7d7662fa3e9a1e3b09472306`, attempt 1, and all ten successful
jobs: one wheel builder, eight receiving cells and one aggregate reader.

Central review downloaded all ten native artifact ZIPs and checked their
SHA-256 against GitHub's artifact digests. It then reused the provider's
immutable `devtools/qualification_bundle.py summarize` operation with public
Pytest Receptor 1.2.1 in an administrative Linux/Python 3.14.7 environment.
The operation independently verifies the wheel manifest and every shipped
package-file digest, exact matrix membership, completed event integrity and
five passing tests per cell. Its result equals the uploaded native aggregate.
No Ackredit/PyUnitWizard candidate was imported locally and no component tests
were rerun by central review.

| Package role | Immutable source | Wheel SHA-256 |
| --- | --- | --- |
| Ackredit candidate | `fc00a6cf1e2426ab7d7662fa3e9a1e3b09472306` | `6d71199ab22aac8c00918ba4cd8ea050639109403556613161074668edc9408d` |
| PyUnitWizard producer | `33fec8a627505a4f5426babe87e8e85438105041` | `9797dc35439b601e5a7c71bed963b49afab47a1bfd9cecb2ad9e348b2593dfba` |
| Released-API source baseline | `598abf993a2409c025de5e912acd7eb45a257ebd` | `019ec0e360d511b2c639c5776d25702a1d36941a80eb48c13ca4f732a543e1ab` |

Linux and macOS arm64 each cover Python 3.11–3.14: **eight cells, 40 passed,
zero skipped, deselected, failed, incomplete, xfailed or xpassed tests**.
The reviewed gate assertions cover installed resources/origins, actual Pint
and unyt calculations, reused references, original versions, scientific-use
roles, public-function/backend parentage, no-op and failure boundaries,
producer-blocked saved reading, provider absence and released-API fallback.
The fallback wheel is built from original 0.9.0 source; it is not the public
Conda archive and does not replace that archive's separate qualification.
This receiving matrix makes no Windows claim.

The concrete integration keeps entry observation separate from completed
backend credit. A failed/no-op public conversion may retain its PyUnitWizard
entry reference, while its backend receives credit only after a successful
dispatch. PyUnitWizard owns those references, roles and scientific criteria.
Its selected qualified calls and lazy declared exports are the reviewed scope;
cached parse returns, direct adapters and other backends remain outside it.
Attribution errors are diagnosed after the scientific callable returns;
explicit warnings-as-errors remains an application-owned choice.

Exact producer ordinary CI
[37217509058](https://github.com/uibcdf/ackredit/actions/runs/37217509058)
also passes seven jobs. The later documentation/receipt commit
`136b5d6fb2751659dcfd5cacd68b30e82157c881` passes its own seven-job CI
[37218150874](https://github.com/uibcdf/ackredit/actions/runs/37218150874);
inspection confirms its nine changed files concern documentation, receipts
and issue archive only. It is not substituted for the wheel producer.
The owner's 1,655-test local run and warmed overhead measurements remain
owner measurements; central artifact review does not independently repeat
them or establish a universal cost guarantee.

Primary central receipt:
`devguide/rollouts/ackredit_function_receiving_review_97_20261004.json`.
The provider's durable allowlisted receipt is
[function_provider_matrix_2026-10-04.json](https://github.com/uibcdf/ackredit/blob/136b5d6fb2751659dcfd5cacd68b30e82157c881/devtools/receipts/function_provider_matrix_2026-10-04.json).
Raw scientific captures and environment ZIPs remain outside this repository.

The concrete installed pilot requirement is now satisfied for these immutable
development candidates. #97 remains partial for the maintainer's decision
about stabilizing the bounded optional contract and its provider-owned
contract/release handoff. No observer obligation, common dependency floor,
member dependency bump or registered guide rollout follows from this receipt.
If stability is accepted, first obtain Ackredit's accepted contract/version
and PyUnitWizard's receiving adoption outcome; distribute any resulting shared
guide change through the existing impact inventory and synchronization route.

### Later provider notice — historical pending checkpoint

The subsequent
[provider notice](https://github.com/uibcdf/molsyssuite/issues/97#issuecomment-5982959583)
announces Ackredit #89/#90/#91: an explicit `workflow` report, detached
format-plugin inputs and iterative provenance rendering. The planned receiving
extension retains the same PyUnitWizard source. No qualified Ackredit producer
or artifact identities are supplied in that notice. This review does not apply
the `fc00a6cf` wheel's result to those later changes. Their new report/reader
assertions, compatibility limits and exact package evidence remain provider-owned
pending work at that checkpoint. The dated reconciliation below now reviews
the delivered report/reader extension and changed provider; stability remains
a separate decision.


## Changed-provider and receiving closure reconciliation — 2026-10-04

The provider fixes equivalent tuple/list bibliography registration in
uibcdf/ackredit#92 while preserving raw registered values, detached comparison
and original normalized portable output. Changed runtime producer
`1a5dd4566737f6195571b4cb421af6f01647c5f6` supplies wheel SHA-256
`4c1d65477af8a09f66873c119b40c9228e6e678a79e360a2e4c0fd4644080604`.
The prepared contract at `40f930a852e3fe4517ba0a6d32d7dabc8624d285`
retains this runtime and qualification code; it is not the wheel producer.

Independent published GH Run Receptor/native metadata confirm exact-source
CI [37230213187](https://github.com/uibcdf/ackredit/actions/runs/37230213187)
and installed receiving
[37230225286](https://github.com/uibcdf/ackredit/actions/runs/37230225286).
Central review downloads all ten native ZIPs, verifies their native SHA-256,
and reuses the immutable provider-owned `qualification_bundle.py summarize`
with public Pytest Receptor 1.2.1. The independent aggregate equals the hosted
aggregate and owner package identities: **eight Linux/macOS arm64 × Python
3.11–3.14 cells, six tests each, 48 total**, no skips/deselections/failures or
incomplete events. This is reading retained evidence; no candidate is imported
or component test dispatched locally.

The added real workflow-report guard pre-registers tuple authors through the
public API, then preserves normalized originals, references, roles, versions
and pipeline parentage in saved reading with producer imports and network
blocked. Function entry remains distinct from completed backend execution;
provider absence and original 0.9.0 source-wheel fallback remain. The older
and newer bundles build receiver/fallback wheels separately: same source pins
do not imply identical wheel bytes. No public Conda file is replaced.

uibcdf/pyunitwizard#94 is resolved for experimental receiving at
`f34b111baee0eacf7c6c97f62e7143fcfdc2b9e7`. Two added numerical/citation
cases cover `conversion_factor` and `standardize`; their assertions require
actual numerical outputs and original software DOI/version/role. Existing
attribution bridge, declarations, citation metadata and guards match the hosted
receiver through scientific source `ef85201`; final runtime Python and
metadata remain unchanged. The named owner regression is
`tests/integration/test_function_citation_provider.py::test_normally_installed_consumer_outside_checkout`.

Owner-local current-source receiving reports 712 passed/one covered NaN/JSON
skip and 27 installed tests/one deliberate build-from-checkout deselection,
with that guard exercised in the full source suite. Normally installed wheel
and mapped public ArgDigest files are distinguished; no fresh local Conda solve
or complete current hosted experimental matrix is inferred. Raw overhead is
owner evidence, not repeated centrally. Final ordinary CI
[37236634394](https://github.com/uibcdf/pyunitwizard/actions/runs/37236634394)
independently executes **699 passed/14 skipped** on Linux/Python 3.14; its
scope is distinct from the local experimental-provider run. Final policy
[37236634877](https://github.com/uibcdf/pyunitwizard/actions/runs/37236634877)
passes separately. Ackredit source CI has five executed test cells, each
1,691 passed/seven optional-tool skips; those skips are separate from the
zero-skip installed receiving matrix.

Primary reconciliation:
`devguide/rollouts/ackredit_function_receiving_reconciliation_97_20261004.json`.
The concrete experimental receiving item is settled. #97 remains partial for
the principal maintainer's decision about bounded stable guarantees, schema
compatibility and API classification, together with provider/direct-MOLI
handoff. Ackredit #93 prepares authorized **provisional** 0.10.0 delivery:
its future exact Conda file/source/installed/receiving/public evidence will be
reviewed separately. Release preparation does not accept stability and is
not blocked by inventing a central preapproval gate. No mandatory observer,
client floor, stable promotion, registered guide distribution or public
artifact qualification follows from this source-wheel review.


## Principal-maintainer decision — retain provisional status, 2026-10-04

The principal maintainer explicitly chooses to keep `observe_calls`,
`prepare_credit` and `ackredit.provider@1` provisional. The completed
PyUnitWizard #94 experimental pilot remains accepted within its reviewed
scope. No stable interpretation/compatibility commitment, shared requirement,
new minimum or six-component rollout is accepted by this decision.

Ackredit #93's separately authorized provisional 0.10.0 delivery may continue
through its existing exact-file/source/installed/public gates. Independently
reviewing its installed Conda bytes is the next evidence checkpoint; that
review will not automatically change provisional classification. Revisit
stability only through an explicit later maintainer decision and the owning
Ackredit #84/#87, MolSysSuite #97 and direct MOLI #46 handoff. #97 remains
partial for the deferred stable-contract/adoption decision.


## Provisional Conda delivery and known CFF limitation — 2026-10-04

Ackredit 0.10.0 has now been promoted from original producer
`16c356d54f245db8dd7fd6aaab72200df9a96e7d`. The central read-only operator
verifies public metadata/index and downloaded bytes for archive
`ackredit-0.10.0-py_0.tar.bz2`, SHA-256
`2ed4841af32eaee603574b185a644fc16c9473497ad15a732788d6630b9cedc3`.
The exact Conda receiving matrix 37237527141 has eight cells/six tests each,
48 total with no skips, and preserves the same file identity before and
after science; native ZIPs and the independently reconstructed summary match.
This satisfies an exact Conda evidence checkpoint, not stable API adoption.

Subsequent Ackredit #94 reports stale self-citation CFF version 0.9.0 in this
0.10.0 package, independently confirmed by central archive inspection. The
provider owns semantic preparation/gate corrections and additive 0.10.1
under Ackredit #93/#94; original bytes/tag are preserved. Wait for that
corrected file and its complete installed/receiving/public handoff before
selecting the new receiving checkpoint. The released 0.9.0 portable fallback
remains available. Public install reported by the provider is separate from
central file/evidence reading; it was not repeated here.

The principal-maintainer decision above remains: observer/prepared-credit
APIs and provider interpretation **stay provisional**, including through a
later corrected release. No automatic stabilization, mandatory adoption,
client floor or guide rollout follows from successful package gates.
Shared release-tool observations and remaining effort evidence belong to #92;
primary receipt is `devguide/rollouts/ackredit_010_public_pipeline_92_97_20261004.json`.


### Later owner correction checkpoint — 2026-10-05

Ackredit #93 now reports staged 0.10.1 at
`dd500842b6085111e01e62cfc243f68406eb8cc7`, SHA-256
`26e75a0780ad4e6abc2de55df90b29b4a2aa4e510d6b50fa54a5812ad929228e`,
with installed 37268949725 and real receiving 37268949118 passing. These
are new owner-reported inputs, not independently qualified by the preceding
0.10.0 review. Its final public clean-installation/tag handoff and central
exact-file review remain distinct pending work. Provisional classification
continues through any corrected delivery until explicitly decided otherwise.


## Corrected public checkpoint independently reviewed — 2026-10-05

Ackredit #93/#94 are closed by their owner at delivery-record commit
`f71d242705b4b65302fb3eecb0659207d56c47dd`. Central review now verifies
original producer `dd500842b6085111e01e62cfc243f68406eb8cc7`, public
`ackredit-0.10.1-py_0.tar.bz2`, SHA-256
`26e75a0780ad4e6abc2de55df90b29b4a2aa4e510d6b50fa54a5812ad929228e`.
The existing shared operator returns `public-verified`, staging/main labels,
no command and no mutation. Downloaded public bytes match; annotated tag
0.10.1 points to the original producer. Packaged CFF version 0.10.1/date
2026-10-04 matches both producer CFF copies and distribution metadata.
Original 0.10.0 evidence and its limitation remain preserved.

Native staging 37268654191, installed 37268949725, real PyUnitWizard
receiving 37268949118 and promotion 37269544505 all succeed. Ten native
receiving ZIP digests independently verify. The immutable provider-owned
`qualification_bundle.py summarize`, with public Pytest Receptor 1.2.1,
reconstructs the uploaded aggregate and the owner's base cell identities.
All eight Linux/macOS arm64 × Python 3.11–3.14 cells execute six tests each,
48 total, zero skips/deselections/incomplete events, binding the original
Conda file before and after science. Receiver/fallback wheels remain separate
identities. No candidate import or component test is repeated centrally.

The owning regression binds both CFF copies to the committed release plan;
its companion explicitly rejects discovered CFF 0.9.0 against exact runtime
0.10.1. The installed smoke calls that verifier. Relevance is inspected and
the owner retains the original failures; this review adds no shared semantic
gate. Fresh public Linux/Python 3.14.7 installation, CLI, `pip check` and
56 unchanged public Sabueso 0.12.0 receiving tests are inspected owner
evidence, distinct from central file/native-artifact verification.

Receipt: `devguide/rollouts/ackredit_011_public_pipeline_92_97_20261005.json`.
This settles the corrected public evidence checkpoint. **The APIs and
`ackredit.provider@1` remain provisional** by the explicit maintainer decision.
#97 stays partial for deferred stable-contract/adoption decisions; no new
consumer floor, mandatory integration or guide distribution follows.


## Later bounded-evidence advance notice — 2026-10-05

The provider reports new experimental work under uibcdf/ackredit#105 after
`d7120eb270d016b8b01360b7c5a8512141baf775`; advance notice is
[the #97 handoff](https://github.com/uibcdf/molsyssuite/issues/97#issuecomment-6003466879).
Proposed `capture(..., record_evidence=True)` and detached `.evidence` collect
bounded facts from explicitly activated provider observers: selected direct
exports, field sources in retained declarations and diagnosed recording gaps.
The default capture and original portable attribution are intended to retain
their contracts. A selected boundary is not invocation, completion, discovery,
import-origin or instrumentation-completeness evidence.

This is an owner proposal with qualification underway, not an independently
qualified new candidate. Real PyUnitWizard receiving and producer-free saved
reading remain provider-owned acceptance work. Existing observer/prepared/evidence
APIs and `ackredit.provider@1` retain the maintainer's provisional classification;
no canonical-guide rollout, mandatory client adoption or new public artifact
is inferred. The separate delivered CFF/CSL name correction is coordinated in
uibcdf/molsyssuite#103 and does not stabilize these APIs.

## Public 0.12.0 receiving independently reconstructed — 2026-10-08

Reuse the exact immutable file/source/installed/public/same-byte promotion
qualification in
[ackredit_cff_delivery_103_20261008.json](../rollouts/ackredit_cff_delivery_103_20261008.json)
without repeating package gates. For the separate real receiving route, local
editable GH Run Receptor and the shared native verifier agree on
[37588186298](https://github.com/uibcdf/ackredit/actions/runs/37588186298):
original source `6f4dbf39996a7185b8aaff7c52b9daeb167a100a`, dispatch,
attempt 1, exact ten-job inventory and executed required builder/receiving/
aggregate steps. Central review independently downloads all ten original native
ZIPs and verifies their GitHub artifact digests and source/run bindings.

The immutable provider-owned `devtools/qualification_bundle.py summarize`
(SHA-256 `925e13ae84be39d321d6f0c3cb48f81db25db746316e82124b14a7e88d1c4914`)
uses local editable Pytest Receptor to reconstruct the original uploaded
aggregate exactly: **eight cells, nine mandatory tests each, 72 passes, no
skips/deselections/incomplete streams**. Candidate Conda identities match before
and after science. Producer is installed PyUnitWizard source
`0e422d06b0af56e4dd2b43cafd00f059221eb405`; its original released fallback
and saved-reader artifacts remain distinct. Saved/provider evidence and workflow
reader/report files are retained by the owning aggregate contract. This is the
original hosted execution, not a new component suite or six-client certificate.

The principal provider decisions are recorded in Ackredit decisions 17/18/21/23
and owner issues #84/#87/#107/#114/#125/#127. The current canonical guide has
SHA-256 `6353892d552eab79973cecec5f8e3c8c31e146416e1cb481786e21cd3fcbf99d`;
all six registered consumer snapshots still carry the older portable-only guide
SHA-256 `dab9d96a897f0e229837ffeda2a7277029a344cace6530a79ac55e5a90d3e529`.
Source promises, exact public delivery, guide copies and actual consumer adoption
are recorded separately. Detailed receipt:
[ackredit_public_contract_review_97_20261008.json](../rollouts/ackredit_public_contract_review_97_20261008.json).

## Accepted scoped central disposition — 2026-10-08

The prior central provisional decision must not be changed merely because a
release is green. The provider has since recorded an explicit scoped acceptance
and qualified public delivery. Accepted outcome: register those bounded public
promises for **optional use** in the existing client profile and distribute the
current canonical integration guide through the registered synchronizer.

| Capability chosen by a consumer | Reviewed public promise | Suite consequence |
| --- | --- | --- |
| Existing portable attribution | >=0.9.0 | Existing floor and client obligations retained. |
| `prepare_credit`, `observe_calls`, `ackredit.provider@1` interpretation | >=0.11.0 | Optional published compatibility route; 0.10.x keeps its original provisional classification. |
| Recorder evidence and `validate_provider` | >=0.12.0 | Optional bounded contracts; 0.11.0 evidence remains provisional and lacks the standalone validator export. |
| General public 1.x stability | Future qualified 1.0.0 | Not delivered or accepted as a suite-wide promise here. |

Accepted client-profile clarification:

> Members choosing function-provider or prepared-credit features may use the
> provider's qualified public compatibility promise from Ackredit >=0.11.0.
> Bounded recorder evidence and standalone validation require >=0.12.0 when that
> public promise is needed. These identify optional feature capability, not a
> mandatory dependency or upgrade for all members. The portable >=0.9.0 route
> remains available. Application activation is explicit; library import enables
> no observers. Observed entry/declaration/validation is not successful scientific
> completion or complete instrumentation. Hosts own scientific reference choices,
> supported call paths, failure policy, original saved records and actual receiving
> qualification. Keep released fallback behavior where that is a claimed client
> compatibility route. Follow the canonical guide's versioned meanings and
> exclusions. Provider, guide delivery and client adoption remain separate; no
> general public 1.x promise follows from this review.

Implementation adds that clarification to
`devguide/ackredit_client_policy.md`, synchronize/publish the current
`ACKREDIT_GUIDE.md` in its six registered clients through preserved isolated
clones, verify exact-source administrative gates and send source/guide/outcome
handoffs to owning issues and MOLI #46. No shared guide is edited by hand; no
component dependency/code, release, tag or scientific suite is changed.
The earlier provisional disposition is superseded only for these explicitly
accepted optional public promises. Historical artifacts retain their original
classification; no general 1.x or mandatory client adoption is accepted.


## Resolution and guide deliveries — 2026-10-08

The principal maintainer explicitly accepted the scoped central registration after
provider-owned decisions and qualified public delivery. The normative guard is
[ackredit_client_policy.md](../ackredit_client_policy.md), section “Optional
function-provider and evidence contracts”: public capability floors and bounded
semantics, explicit application opt-in, original records, real receiving ownership
and exclusions remain explicit. This is the policy decision requested by #97;
ordinary guide/admin checks do not certify a component's scientific integration.
General public 1.x remains a future provider qualification; historical provisional
0.10.x and original 0.11.0 evidence keep their original scope.

The registered synchronizer delivered the canonical guide from Ackredit
`b319e7f868301d01a3325a37a1937da9267aa737`, SHA-256
`6353892d552eab79973cecec5f8e3c8c31e146416e1cb481786e21cd3fcbf99d`.
All six published copies match. Direct guide-only commits retain authorized
scientific/browser deferrals; native manual gates prove exact commit, workflow,
attempt, job inventory and required executed steps. Probe inputs omit science;
backlog detection does not clear full-suite debt.

| Consumer | Immutable guide commit | Verified administrative runs |
| --- | --- | --- |
| uibcdf/pyunitwizard | `4e4eefad58f12778f31e9ec3f81f53193750d567` | [37786048337](https://github.com/uibcdf/pyunitwizard/actions/runs/37786048337) |
| uibcdf/molsysmt | `f74a0f9dd0c364b3905f1031d5e89413be27d88b` | [37786197390](https://github.com/uibcdf/molsysmt/actions/runs/37786197390), [37786205682](https://github.com/uibcdf/molsysmt/actions/runs/37786205682) |
| uibcdf/molsysviewer | `a07a20556c9621f0f56884dcad3cf0103062ae7c` | [37786225766](https://github.com/uibcdf/molsysviewer/actions/runs/37786225766) |
| uibcdf/topomt | `efd9b9633f7c47185af26117ca4f3314af8c542e` | [37786245236](https://github.com/uibcdf/topomt/actions/runs/37786245236), [37786253103](https://github.com/uibcdf/topomt/actions/runs/37786253103) |
| uibcdf/pharmacophoremt | `8fdf03f0e007c80746455962503c6d2634f17559` | [37786271588](https://github.com/uibcdf/pharmacophoremt/actions/runs/37786271588), [37786279254](https://github.com/uibcdf/pharmacophoremt/actions/runs/37786279254) |
| uibcdf/elastnetmt | `1b7e1912f146ec429b445f6935831dcb8a0c42ab` | [37786297474](https://github.com/uibcdf/elastnetmt/actions/runs/37786297474), [37786305180](https://github.com/uibcdf/elastnetmt/actions/runs/37786305180) |

Local Python 3.14 checks execute the applicable reporting/index/conformance
surface (PyUnitWizard 9 reporting tests, Viewer 178, TopoMT 2,
PharmacophoreMT 3, ElastNetMT 3; MolSysMT's four structural validators pass).
Viewer's latest central checker retains a preexisting transition-caller finding:
its authorized transition only lists policy-v1.5.4 while its unchanged caller is
policy-v1.5.7. That actual pinned policy passes locally and natively, including
executed Ruff formatting and metadata audit. The latest finding is not hidden
or qualified as a pass; follow-up and evidence are delivered to
uibcdf/molsyssuite#39 and uibcdf/molsysviewer#93. No caller or transition rule is
changed in this documentation delivery.

Each of the six existing owning issues has an advance notice and final handoff.
Ackredit #127, direct MOLI #46 and Sabueso #108 receive the scoped contracts,
exact consumer commits and native gate links. The durable review receipt records
all notice URLs, local results, source/guide/adoption distinctions and primary
clone preservation. No component source/dependency, public bytes, tag, release or
caller-owned environment is changed. The original receiving qualification remains
pinned to its original producers, not generalized to six clients or Windows.

The bounded shared review/decision/guide coordination is complete. Optional
functional adoption stays in consumer issues; no requirement to adopt or upgrade
Ackredit is introduced. Original records and qualified release receipts remain
unchanged. Task-owned clones, downloaded ZIPs, caches and helpers are removed
at closeout once durable receipts and handoffs are committed; primary clones,
active work and the shared development environment remain preserved.
