---
summary: Review provisional dependency-free function declarations and explicit Ackredit observation before stable adoption.
issue: uibcdf/molsyssuite#97
status: partial
opened: 2026-10-04
closed:
verification: inspected
area: [governance, compatibility, provenance]
guard:
normative:
blocked_by: []
supersedes: []
---

# Review provisional function citation providers

## What

Ackredit implements a dependency-free module/function declaration protocol and
explicit `observe_calls(*modules)` context under uibcdf/ackredit#84 and #85.
The declaration schema `ackredit.provider@1` and observation API are provisional,
initially published in development source `536bd87ec395cf8abfd18a14c4d24dc71ad88980`.
The repaired candidate is `b67ea77981e8c68a8b0eb42b8814178cdd8d88e9`;
its installed fixture and hosted gates now pass as reviewed below.
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
- Pre-activation aliases, generators, descriptors, custom/lazy module subclasses,
  native internal calls and subprocesses are outside the first contract. A
  receiver must use supported qualified calls and report its unobserved scope.
- Invalid/conflicting declarations fail before activation with ACKREDIT-E012.
  Attribution failure or export rebinding uses ACKREDIT-W019; original scientific
  results/exceptions are preserved under ordinary warning handling. A consumer's
  explicit warnings-as-errors configuration needs its own failure-policy review.
- The candidate reuses sessions, scope, captures, detached bibliography and
  registry checks. Existing public portable schema and coarse hooks retain
  distinct contracts. Original-version fidelity and reused references are
  inspected in tests, not newly certified in a real receiving component here.

These boundaries fit review under the existing optional client profile:
`devguide/ackredit_client_policy.md` already allows explicit application opt-in
and requires client-owned references, absence/failure behavior and actual
receiving evidence. It does not authorize enabling observers on library import,
mandating Ackredit or treating this provisional schema as a common requirement.
No new normative rule is adopted by this review.

## What is measured and what is assumed

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
fixture environment; uibcdf/ackredit#85 owns measured overhead. No specific
suite consumer pilot has been chosen. uibcdf/moli#46 owns its direct receiving
scope without transferring platform authority to MolSysSuite.

## Dependencies and risks

The repaired candidate has exact-head hosted installation/reader evidence.
Missing real producer/receiving review and a stable-promotion decision keep
#97 partial. A later source change needs its own exact-head inspection. Do not reuse public 0.9.0 qualification
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

#97 remains partial for a concrete producer/receiving review and a maintainer
decision before stable shared adoption. `observe_calls` / `ackredit.provider@1`
remain provisional; public Ackredit 0.9.0 and its portable floor are unchanged.
The existing optional client policy and function-entry/failure/alias scope
recorded above still apply. Direct MOLI receiving review remains uibcdf/moli#46.
