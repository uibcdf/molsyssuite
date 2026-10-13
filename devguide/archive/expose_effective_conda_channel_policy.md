---
summary: Report Conda channel evidence and decide an optional exclusive operation mode.
issue: uibcdf/molsyssuite#116
status: resolved
opened: 2026-10-10
closed: 2026-10-13
verification: measured
area: [governance, tooling, compatibility]
guard: tests/test_conda_environment_tools.py
normative: devguide/conda_environment_tools.md
blocked_by: []
supersedes: []
---

# Effective channel policy in shared environment operations

**Reported:** PharmacophoreMT's ordinary environment receiving under
uibcdf/pharmacophoremt#10 observed inherited channels.
**Status:** Accepted 2026-10-13 and implemented in the existing shared operator.
Configured inheritance stays the default; exclusive support is qualified only for
Mamba 2.9.0 Linux x86_64 creation. Consumer adoption remains separately owned.

## What

`conda_environment_tools.apply_environment` validates the owner's declared YAML,
sets `CONDA_CHANNEL_PRIORITY=strict` and invokes a checked `env create/update`.
Its result contains no declared/effective channel facts or inheritance policy.
Strict priority orders channels; it does not remove inherited channels.

The consumer's committed evidence at
`5aefc25e656114513a3955bffbe13bc564805523` records three actual environment
creations and public installed/context checks. Its YAML declares `uibcdf`, then
`conda-forge`; the manager also lists inherited `ambermd`. Every original archive
comes from the two declared channels, and separate exclusive dry solves reproduce
the same coordinates. These are original owner measurements, not new central
environment or scientific tests.

## How: accepted compatible contract

Extend the existing owned module rather than introduce another environment
operator. Keep generation and all owner YAML unchanged. The principal maintainer chose option 1 after reviewing both scopes:

1. **Evidence plus optional exclusivity (recommended):** add truthful channel
   reporting and opt-in `channel_policy="declared-only"`. Omission retains the
   existing configured inheritance behavior.
2. **Evidence only:** add reporting while deferring any new execution mode.

Both retain new-name/active-interpreter protection, exact source/context/Python
selection, manager errors, caller resources and private-manifest cleanup. Neither
changes a consumer pin or makes exclusivity a common admission/release requirement.
Scientific channels explicitly declared by an owner remain eligible.

### Reporting contract

Keep the existing result fields and add a bounded channel-evidence section:

- owner's literal ordered declared channels;
- selected inheritance policy, separately from requested strict priority;
- manager family/version and evidence method when verifiable;
- observed manager configuration, distinguished from the operation's effective
  solver channel list;
- effective channels with an explicit `observed`/`unknown` state and reason;
- exact reviewed invocation/input identity, with credential redaction.

Do not infer the effective list by concatenating YAML and configuration strings:
aliases, multichannels, configuration precedence, target context and caches need
manager-owned interpretation. A configuration snapshot is time-qualified
configuration evidence, not proof of the solver's actual invocation. Selected
package URLs, installed dependency closure, pip sources and public release
qualification remain separate facts.

For an unsupported/malformed/unavailable observation, preserve the existing
configured execution route and report `unknown`; do not create an unrelated
blocking gate. Required create/update failures still propagate. Query only the
needed configuration fields and avoid retaining credentials or raw global logs.

### Optional exclusive contract

The accepted implementation adds keyword-only `channel_policy` to the existing operation and a
matching CLI selector. The default is configured inheritance. `declared-only`
would restrict this operation's Conda solver channel inputs through a reviewed
manager adapter; it does not isolate all manager settings, pip indexes, caches
or previously installed packages, or certify artifact provenance.

Use a private execution manifest and the supported manager route, preserving
dependency/pip sections and owner inputs. The qualified route uses the standard YAML `nodefaults` sentinel
in the private execution manifest. Do not assume `--override-channels` works for every
`env create/update` command. A manager/version/operation that cannot enforce the
selected policy must refuse it before mutation, without falling back to inherited
channels. Unknown managers continue to use their existing configured route.

Qualification must establish both the requested channel restriction and truthful
receipt evidence. Supporting creation does not automatically qualify update;
supporting Mamba does not automatically qualify Micromamba or older versions.
Do not disable TLS or edit global configuration to make the mode pass.

## Why

This prevents an ordered YAML from being mistaken for exclusive resolution and
keeps host-specific configuration effects visible. It offers reproducible channel
selection when needed while preserving specialized component requirements and
ordinary development behavior. Publication still needs actual exact-candidate,
installed and public evidence under its existing owner contracts.

## Preparation measurements (before implementation)

2026-10-13, Linux, qualified Python 3.14.7 with the two editable receptor origins
verified; the seven accepted local closure conflicts remain uibcdf/molsyssuite#82.
Actual installed manager versions are Conda 26.7.1 and Mamba 2.9.0; Micromamba
is unavailable. Managers use their own runtime, separately from the development
interpreter. No solver installation, shared-environment update or science ran.

The [bounded probe receipt](../rollouts/channel_policy_proposal_116_20261013.json)
retains actual metadata-only local-channel dry-run outcomes and limitations:

- Mamba configured mode finds a control package available only in its inherited
  local channel. Adding YAML `nodefaults` rejects that negative control; a package
  available in the declared channel passes. No target prefix is created.
- Conda `env create` rejects `--override-channels` as an unknown argument. The
  documented command and local help agree; Mamba creation accepts that option.
- Local offline Conda probes do not qualify exclusivity: their initial positive
  control cannot solve with an empty cache; after file-only metadata priming all
  three cases return success, including the exclusion negative. Effective solver
  inputs/package provenance were not acquired for that result. Retain it as
  inconclusive evidence, not a passing restriction or an asserted Conda defect.
- The initial custom `controlled.condarc` was ignored by both clients. Explicit
  configuration controls identify accepted `.condarc`/`.yaml` inputs and verify
  loading before the subsequent probes. The initial failures remain in the receipt.
- Controlled RC/config/cache/repodata/solver scratch are retired through managed
  contexts after child exit. Unrelated configuration values/logs are not retained.

The initial proposal qualified no exclusive adapter, SDK runner contract, update
route, Mac/Windows result, Micromamba result, public solve or installed package.
The subsequent native qualification below supplies the bounded non-offline creation
and cache/provenance controls. Existing consumer qualification remains valid.

## Primary documentation

- [Conda environment YAML specification](https://conda.org/learn/specifications/exchange/environment-yml/):
  configured channels are appended unless `nodefaults` is present.
- [Conda env create](https://docs.conda.io/projects/conda/en/stable/commands/env/create.html):
  command options differ from general `conda create`.
- [Mamba configuration](https://mamba.readthedocs.io/en/stable/user_guide/configuration.html):
  configuration sources and sequence merging are manager-owned.

The upstream historical mamba-org/mamba#3841 concerns configuration-file
`nodefaults`/precedence. It does not establish failure of the current YAML route;
the local Mamba 2.9 control above is narrower, actual evidence.

## Alternatives and refuted paths

- Making exclusivity the new default would change compatible callers and could
  remove specialized channels without owner review.
- Editing the user's `.condarc`, replacing all manager configuration or translating
  YAML into a partial `conda create` command can change unrelated/pip semantics.
- Treating priority, observed package URLs or an empty-cache failure as proof of
  exclusive solver inputs confuses distinct evidence.
- Guessing an unobserved list or silently downgrading an unsupported exclusive
  request makes the receipt misleading.

## Scope and exclusions

Shared operator/receipt design, relevant administrative manager controls and an
immutable qualified provider handoff are in scope. No scientific implementation,
new common CI gate, consumer runtime/floor/pin rollout, package/release, old
qualification invalidation or caller/global environment cleanup is proposed.

## Acceptance criteria

1. Principal maintainer selects reporting-only or reporting plus optional exclusivity.
2. Existing operations retain compatibility and truthful bounded evidence;
   unsupported observations return explicit unknowns.
3. If selected, exclusive adapters are qualified by actual relevant manager routes,
   positive/negative controls, caches and update semantics before being enabled.
4. Extend `tests/test_conda_environment_tools.py` with meaningful regressions for
   policy/evidence, refusal before mutation, preserved inputs/pip/source contexts,
   manager errors and cleanup. Existing unrelated tests are not closure proof.
5. Publish a qualified immutable shared revision and deliver an actionable owning
   handoff. Consumer adoption/installed/public evidence remain separate.

## Local implementation issues / consumer inventory

- uibcdf/pharmacophoremt#10: actual adopter of shared environment SDK
  `8f00e6d9de943b6e4710ea62936e2ebea00fad24`; its wrapper forwards to the provider.
- uibcdf/pharmacophoremt#23: public component admission stays local.
- uibcdf/elastnetmt#18, uibcdf/lindelint#13 and uibcdf/topomt#78: registered
  candidate reuse from the #108 receiving inventory, not verified API adopters.

The provider implementation is complete; no consumer pin or candidate-consumer
rollout has started.
Owner notice before an accepted implementation rollout follows the existing
shared-provider rule; the impact issue here is already open.

## Dependencies and risks

The selected scope and bounded native-manager qualification are explicit.
Effective channel observation may remain unknown for unsupported versions or
configuration shapes. Availability of a special channel is component-owned;
successful restriction does not establish reproducible package bytes or science.

## Provenance

Source inspected at central `49026bb0a1635721f10cb64d5707eee3ff73b312`;
consumer source and original evidence inspected read-only after `suite_status.py`.
Prototype fixtures use private local repodata and managed scratch only. Those initial prototype receipts retain their original bytes. The accepted operator
and its maintained guide now implement the selected scope.

## Resolution — 2026-10-13

The principal maintainer accepted evidence plus optional exclusivity. Public
`observe_channels` provides reusable bounded version/configuration observation;
`apply_environment` adds `channel_evidence` and keyword-only `channel_policy`,
with the matching CLI selector. Existing result fields and default argv/source
selection remain compatible. Effective solver inputs stay explicitly unknown;
configuration is a timestamped snapshot, never a guessed resolved channel list.
Nonliteral locations are redacted, and unavailable observations remain nonblocking.

The exclusive adapter is admitted only for Mamba 2.9.0 Linux x86_64 `create`.
It inserts `nodefaults` into the private execution manifest and refuses unsupported
manager/version/architecture/platform/update routes before any mutation. It does
not duplicate an owner sentinel or alter pip/source requirements. Scientific
channels explicitly declared by an owner remain eligible. This is no new common
CI, scientific, admission or publication gate.

[Executed native receipt](../rollouts/channel_policy_qualification_116_20261013.json)
records actual SDK/manager creation over local HTTP metadata and real synthetic
archives, selected installed record hashes and provider/test file digests:

1. Exclusive cold cache rejects archives present only in the inherited channel.
2. Default configured mode installs four archives from that inherited channel.
3. Exclusive warm cache still refuses those inherited-only inputs.
4. Identical bytes served from an explicitly declared additional channel install
   under the exclusive route, with all four installed URLs and SHA-256 verified.

The synthetic Python record has no interpreter. This is transaction/channel
qualification, not real component Python, public-channel or scientific evidence.
A preliminary fixture omitted mandatory reviewed channels and was rejected before
creation; a repeated directory creation was corrected. Attempts to use `env remove`
for the synthetic Python fixture encountered its absent interpreter during native
pip inspection. Final retirement uses managed private directory cleanup followed
by native inventory pruning of absent fixture registrations, checked explicitly.
All private prefixes/cache/server/scratch and registrations are retired; caller
environments and owner input bytes are preserved. Initial proposal failures and
inconclusive Conda controls remain in their original receipt.

The offline regression module protects configured fallback, redaction/unknowns,
unsupported refusal before mutation, source/pip preservation, owner sentinel
identity, cleanup and manager errors. The native regression uses the actual public
SDK and manager calls and asserts inherited-only rejection against the paired
configured positive, so dropping the sentinel would break the exclusion control.
Native selection is opt-in and skipped without an explicit manager; a hosted skip
does not expand qualification.

Notice before publication:
[shared acceptance](https://github.com/uibcdf/molsyssuite/issues/116#issuecomment-6150705871),
[actual consumer handoff](https://github.com/uibcdf/pharmacophoremt/issues/10#issuecomment-6150706387).
The immutable provider revision and independently verified hosted checkpoint are
recorded in the closing issue and receiving handoff. Source adoption, actual owner
environments, installed/public package acceptance and science remain separate;
the actual consumer retains its old qualified SDK until its owner chooses to adopt.
