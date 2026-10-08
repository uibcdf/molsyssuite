---
summary: Qualify shared release tools independently and reduce manual evidence reconciliation.
issue: uibcdf/molsyssuite#92
status: partial
opened: 2026-10-03
closed:
verification: measured
area: [distribution, tooling, ci]
guard: tests/test_noarch_release.py
normative:
blocked_by: []
supersedes: []
---

# Independently qualified publication with a short operator path

## What and why

Ackredit and Pytest Receptor exposed shared publisher defects while preparing
ordinary releases: Conda executable/plugin selection (#78/#80), staging
selection under strict priority (#88), descriptor step mismatch (#89), and
administrative subprocess imports under inherited safe-path settings (#88/#91).
Those fixes and the original exact-byte deliveries are complete. The shared
pipeline still needs independent representative qualification and a simpler
operator path before claiming reduced release effort. Platform scope is
uibcdf/moli#43; this issue owns suite engineering.

## Implemented operator capability

`devtools/scripts/noarch_release.py` reads the original producer's native job
facts and attempt-qualified receipt ZIP, checks its native digest and binds
source preflight, inspected file and verified upload. It derives original
candidate, version, filename and archive digest without manual transcription.
The original producer checkout can differ from the native wrapper head.

It reuses recipe/plan validation, installed descriptors, native matrix verification
and independent public verification. `_release_artifacts.py` owns bounded JSON
artifact acquisition and is also used by the installed-source binding reader.
The optional reviewed qualification commit remains explicit. Existing staged
wrappers, source gates, component tests and publication authority keep their
current contracts; the new tool only prepares arguments for those wrappers.

Current registry facts are checked before preparing the next operation. An
already-public file requires its existing installed evidence and produces a
public verification receipt with no dispatch command. Uncertain evidence,
changed hashes, dirty producer clones, mutable caller pins, missing forwarded
inputs, moved workflow refs and mixed native attempts stop the handoff.

The entry point and normal/recovery paths are documented in
`devguide/noarch_release_operations.md`. Consumer discovery remains the maintained
publisher inventory, not an ad hoc repository search. New workflow pins or
forced consumer adoption are not required to use this administrative capability.

## Measurements and limits

`devguide/rollouts/release_pipeline_92.json` contains nine explicitly selected
historical Pytest Receptor publication/installed runs: five failed and four
succeeded. This is a bounded sample, not the complete release inventory. Native
creation/update intervals include execution and GitHub coordination; they do
not measure human work, operator steps or all source-CI costs.

The tool independently rechecks Ackredit 0.9.0 and Pytest Receptor 1.2.1 against
their original producer artifacts, full existing installed matrices and public
label/index hashes. Both archives now carry the public label. These read-only
checks do not recreate a staging-only file masked by an older public package,
perform a fresh dependency solve, execute science or constitute independent
qualification of all provider execution environments.

Local verification uses Python 3.14.7 and Ruff 0.16.5. Regression tests cover
changed digests/sources/attempts, skipped builds, ambiguous receipts, safe-path
launch outside source, command identities and preventing duplicate publication.
The pre-existing exact-install and actual published scientific-launch
regressions remain in `tests/test_installed_noarch.py`.

## Remaining acceptance

- Exercise the operator path on a later ordinary release and record run count,
  operator steps and elapsed/active effort before selecting improvement targets
  or claiming reduced effort. No measured human-hours total is available yet.

The issue remains partial until these criteria are met. Receipt checks and a
green administrative suite do not substitute for those remaining observations.

## Scope and alternatives

No changes to scientific APIs, internal push CI, Windows support, mandatory
dependency adoption, action v2.3.0 rollout (#87) or package withdrawal. Calling
the existing tested workflows keeps their release controls in their owning
tools; rebuilding staged bytes or copying publisher logic into members would
discard the successful immutable recovery contract.

Related owners: uibcdf/ackredit#22, uibcdf/pytest-receptor#32,
uibcdf/topomt#78, uibcdf/pharmacophoremt#10, uibcdf/elastnetmt#18,
uibcdf/lindelint#13; notices and usage remain separate from caller adoption.


## Independent provider qualification — 2026-10-03

`devtools/scripts/qualify_noarch_install.py` freezes two local channel catalogs
from verified real public metadata/bytes: Pytest Receptor 1.2.0 at higher
priority and 1.2.1 in the staged catalog. It installs the older file, confirms
that the newer staged entry is visible, and requires the actual Conda solver
to reject named candidate selection under strict priority. It then calls the
unchanged exact installer: real public dependency solve followed by the real
registered 1.2.1 staging URL, SHA verification, installed provenance/resources
and an outside-source plugin smoke. The current real files both carry main;
the visibility conflict is a reproducible frozen fixture, not a claim of a
current staging-only release.

`.github/workflows/qualify-noarch-install.yaml` runs this case manually on all
eight Linux/macOS-arm64 × Python 3.11–3.14 cells with the actual login-shell
and `python -P` helper controls, plus the existing published-launch/child-import
regressions. It has contents-read permission only, no registry secret and no
push trigger. Original producer source remains pinned. Native results must
be recorded before marking independent installed qualification complete.


The isolated Linux/Python 3.14.7 case now passes with Conda 26.7.1. It checks
that Conda actually loads the frozen YAML configuration, observes the candidate
in the lower-priority catalog, and records `LibMambaUnsatisfiableError` for
named selection. The fixture configuration is then restored before calling
the unchanged corrected installer through ordinary real public channels and
the exact staging URL. Installed digest/origin/resource checks and the real
plugin smoke pass. This is a local installation-tool qualification, not an
eight-cell hosted or ordinary-release effort claim. Primary local receipt and
explicit pending native scope: `devguide/rollouts/noarch_install_qualification_92.json`.


Native run [37159007278](https://github.com/uibcdf/molsyssuite/actions/runs/37159007278)
at immutable provider `da485db244e2b9039e5302962eeb5fd4f5cd8868` passed all eight
Linux/macOS-arm64 × Python 3.11–3.14 cells. Each native artifact ZIP digest
was independently checked; all eight primary installation receipts retain the
original producer, exact archive digest, rejected named solve and verified
installed origin. The workflow also passed the actual launcher/administrative
child regressions. `devguide/rollouts/noarch_install_qualification_92.json`
now records these native facts and primary receipts. The independent provider
qualification criterion is met; the later ordinary-release operator/effort
comparison remains pending. No measured effort reduction is claimed.


## Later-release observation — 2026-10-04

A bounded native check after the 2026-10-03T22:56:58Z checkpoint found no
new producer runs in the registered shared-noarch staging wrappers of Pytest
Receptor, Ackredit, TopoMT, PharmacophoreMT, ElastNetMT and LinDelINT. This
is a workflow/date-bounded observation, not a claim about every release route.
DepDigest 0.13.0 completed uibcdf/depdigest#29 meanwhile; its local-provider
publisher is a different route and its public delivery does not qualify the
shared administrative operator or establish a comparable operator-effort
measurement. No extra release or suite is dispatched to manufacture a sample.

Receipt: `devguide/rollouts/release_pipeline_92_followup_20261004.json`.
#92 remains partial for the next comparable ordinary shared-operator release.
Use the existing recording checklist in `devguide/noarch_release_operations.md`
to retain steps, runs/retries, timestamps and separately measured active effort
at that time. No reduction target or retrospective human-time total is invented.

## First later release: ArgDigest 0.14.0 — 2026-10-04

The provider completed a real public release after the prior checkpoint.
`devguide/rollouts/release_pipeline_92_argdigest_014.json` preserves seven
explicit episode runs: two build/staging attempts, two full installed attempts,
one minimal-core matrix, one release-triggered route and one promotion.
Two fail; the remaining five succeed. The release-triggered build job is
intentionally skipped and is not a second artifact production.

The first build fails because Conda rejects simultaneous `build.sh` and
`build/script`; both upload steps are skipped. Its recipe correction precedes
the final original producer. The first installed run passes Linux/macOS but
four Windows cells fail while installing administrative tools, before artifact
installation (`WinError 2`). The owning correction #99/#100 is merged and
qualified in the second twelve-cell installed run. Source, qualification
revision and unchanged file digest remain distinct; no recovery rebuild occurs.

For the aligned producer/full-installed/promotion stages, the historical
Pytest Receptor sample has eight runs/five failures; ArgDigest has five/two.
The broader stored episodes have nine and seven runs respectively. Scope
differs: ArgDigest has twelve platform/minor cells, an independent minimal-core
gate and component-specific recipe work; the older installed sample has eight
cells and different failures. These raw observations are not a controlled
improvement measure. The ArgDigest creation/update envelope is 85 minutes,
7 seconds; it includes queues and coordination. Operator steps and active
human effort were not measured and remain null.

The existing read-only operator independently reports `public-verified` for
the original source and exact public file, with no dispatch or mutation.
That post-publication use does not establish an ordinary end-to-end generic
operator route. ArgDigest's promoter additionally requires `core_run_id` for
its independent core gate; the standard adapter cannot generate that evidence.

This exposed reproduced central defect `uibcdf/molsyssuite#101`: the old
caller subset check accepts an incomplete generated dispatch. The correction
rejects extra required inputs before emitting any command, names the missing
fields and retains the existing reviewed adapter/local route. Required defaults
are not silently selected. Optional extras and read-only public verification
remain supported. The targeted regression fails before the fix; all fourteen
operator tests pass afterward, and the actual immutable ArgDigest caller now
rejects missing `core_run_id`. Seven candidate publisher owners receive notice
before publication; operator use is verified only for the three recorded
post-publication users. No member caller, policy pin, core gate or artifact is
changed. The common operator doc states this boundary.

#92 remains partial for a reviewed complete operator route and separately
measured operator-step/active-effort comparison. Further adapters require
their own input/evidence contracts; neither a helper default nor consumer
publication permits bypassing a special gate. No new scientific execution,
package operation or general provider v2.3.0 rollout is initiated.

## Additional-gate design — prepared decision history

The actual immutable ArgDigest promotion caller at
`be39e899f3b9fef2d4ce705799ae19770f41f769` explains why simply allowing
arbitrary extra inputs would be insufficient. `core_run_id` is consumed by
the local `release` job, which checks the public release and the exact
minimal-core matrix. The shared `promote` job depends on `release` and forwards
only the existing standard inputs. An extra gate input must therefore be
reviewed together with the job that consumes it and the promotion dependency;
it cannot be treated as another shared-workflow parameter.

The existing owner operation is
`devtools/conda-build/verify_core_release.py::validate_run` in ArgDigest. It
checks exact producer source, digest-bearing title, workflow, run attempt,
complete matrix membership and the executed successful core step. The owner
keeps the scientific lower-bound/NumPy-free test selection and its promotion
guard. MolSysSuite owns administrative orchestration and shared evidence
primitives. No scientific test implementation should be copied centrally.

Two concrete delivery choices are available:

| Choice | Scope | Consequence |
| --- | --- | --- |
| Optional shared gate profiles (recommended) | Extend the existing `noarch_release.py` operator with explicitly reviewed, source-bound profiles for additional gate inputs, starting with ArgDigest. | Supports complete handoffs for special component gates while retaining the component's own enforcement before promotion. |
| Retain local preparation routes | Keep the standard operator's #101 rejection and ArgDigest's existing tested promotion route. | Current publication remains usable; special input reconciliation remains local/manual and #92's complete-route work stays pending. |

If the shared extension is chosen, its bounded contract should provide:

- Explicit input names and run identities, with no arbitrary extra arguments
  or implicit selection of required defaults. Components with no extra gates
  keep their standard route.
- An immutable reviewed profile binding the caller, input-consuming guard,
  promotion dependency and owner verification sources. Source drift produces
  an unverified handoff with no command until receiving review.
- Read-only acquisition of the complete native run/attempt/jobs/steps and
  producer/file identity. Reuse central acquisition/identity primitives and
  the provider-owned evidence contract. Missing, wrong-file, wrong-source,
  skipped, failed or incomplete gate evidence produces no command.
- A distinction between standard fields forwarded to the shared promoter and
  additional fields consumed by the component's prior guard. Reject a caller
  which no longer keeps that guard as a promotion dependency.
- Receipts retaining original producer, separate administrative qualification,
  exact archive digest, additional gate identities and reviewed profile source.
  The operator remains read-only; its preparation is not publication authority.
- Provider-owned reacquisition and validation before the actual mutation.
  Central preflight does not replace an independently executed promotion guard,
  scientific gate, full installed matrix or uncertainty-recovery route.
- Regression coverage for invalid/missing gate evidence, source/attempt drift,
  removed promotion dependency and unchanged standard/read-only public routes.
  Use existing archived bytes and native metadata for a bounded adapter review;
  do not create a release or repeat scientific tests to manufacture evidence.

The proposed extension applies only to opt-in reviewed operator profiles. It
adds no universal component gate, new internal-push requirement or compulsory
provider pin migration. A component with a special route can retain its local
equivalent. Notify the seven inventoried shared-publisher candidates before
publishing an implementation; source adoption and a future measured ordinary
release remain distinct follow-up evidence. No extension/profile is accepted
or implemented by this proposal checkpoint.

## Accepted optional profiles and implemented adapter — 2026-10-04

The maintainer selects **optional shared gate profiles**. The alternatives above
retain their predecision history. No universal gate, compulsory migration or
per-push scientific suite is adopted.

The existing `noarch_release.py` now offers `--gate-profile`, explicit
`--gate-run INPUT=RUN_ID` and an optional reviewed catalog. The first profile
binds ArgDigest's core caller/guard/verification inputs by exact Git-blob hashes.
It preserves the prior local promotion dependency and component-owned science;
central code reads native evidence through existing reusable acquisition/job
primitives. Exact digest-bearing title, producer source, workflow/event, complete
expected matrix, executed steps and stable attempt are required before a
command can be prepared. Generic unprofiled required inputs still fail as #101
requires; existing standard and read-only public routes remain available.

ArgDigest's `main`-only promotion guard revealed that installed qualification
and promoter source must remain distinct. `--promotion-sha` names the reviewed
caller revision selected by the dispatch ref; `--qualification-sha` retains the
installed evidence revision. Both differ from the original producer when
needed. The profile checks its caller hashes at promoter source and its core
workflow/verification inputs at producer source. Moving a ref or choosing an
unsupported caller ref produces no command.

The real archived-byte checkpoint independently verifies public ArgDigest
0.14.0 with original producer `0fa776af2d271065c60727c28480b20c3ce09aee`,
installed qualification `be39e899f3b9fef2d4ce705799ae19770f41f769`, promoter
source `42b2f93346fdcd1573ade66a3f82a1717a496184` and existing core run
`37211211381`. All twelve required core jobs/steps pass; the original file
SHA-256 and full installed matrix remain bound. State is `public-verified`,
`next_command` is null and no mutation occurred. No scientific run, fresh
installation or promotion was dispatched for this review.

Thirty focused operator/profile/matrix tests pass, including failed/skipped,
wrong-file/source/workflow/event/attempt, incomplete/extra matrix, source drift,
removed/tolerated guard, input overwrite, missing inputs, rerun, forbidden ref,
separate promotion/installed identities and unchanged public no-repeat behavior.
Ruff and offline governance checks pass. Primary receipt:
`devguide/rollouts/release_gate_profiles_92_20261004.json`; maintained use and
profile contract: `devguide/noarch_release_operations.md`.

#92 remains partial for owner receiving outcomes and a later ordinary release
using the complete preparation route with separately measured operator steps
and active effort. The actual checkpoint above is post-publication read-only
verification. No success of a new promotion or measured effort reduction is
claimed. The seven shared-publisher candidates receive the new operator
contract before its implementation is published; member workflow/pin/dependency
adoption remains their own choice.


## Ackredit 0.10.0 ordinary publication observation — 2026-10-04

Ackredit #93 delivers another real shared-noarch release: original producer
`16c356d54f245db8dd7fd6aaab72200df9a96e7d`, archive
`ackredit-0.10.0-py_0.tar.bz2`, SHA-256
`2ed4841af32eaee603574b185a644fc16c9473497ad15a732788d6630b9cedc3`.
Staging 37237182299, eight-cell installed matrix 37237527349, eight-cell
real PyUnitWizard receiving 37237527141 and exact-file promotion 37237913352
all succeed. Native promotion steps reacquire source/installed gates, add the
public label without rebuilding and verify registry/index. The annotated tag
0.10.0 resolves to the original producer.

The existing central operator independently returns `public-verified` with
original source/file/digest, staging/main labels, no next command and no
mutation. Downloaded public bytes match that exact SHA-256. Separately, all
ten receiving artifact ZIP digests match GitHub metadata; the immutable
Ackredit `qualification_bundle.py summarize` reconstructs the same native
aggregate with public Pytest Receptor 1.2.1. Each of eight Linux/macOS arm64
Python 3.11–3.14 cells executes six tests (48 total), no skips/deselections,
and binds the same Conda file before and after science. Only the PyUnitWizard
producer and original 0.9.0 fallback are wheel-built in this profile. No
component execution or release operation is dispatched centrally.

This explicitly selected episode has four successful runs, zero observed
failures; its aligned staging/installed/promotion subset has three runs. Its
12 minute 18 second creation/update envelope includes queues and parallel
receiving work, excludes source CI and later correction, and does not measure
active operator effort. Operator use/steps/active time remain unreported;
post-publication central verification does not establish ordinary end-to-end
operator adoption or a controlled effort improvement. Owner recording is
requested under the existing checklist, without retrospective estimates.

Native source matrix cells report 1,702 passed/seven skips; installed cells
report 1,635 passed/eight skips for the declared tests directory outside source.
Both results are retained; their collection difference is not silently equated
and the owner is asked to clarify scope. Zero-skip real receiving is a third,
six-test-per-cell scope. Source/policy/installation/receiving evidence remain
distinct from scientific coverage or a guarantee over every future release.

A later owner audit exposes stale self-citation metadata, independently
confirmed inside the digest-verified public archive: CFF version 0.9.0/date
2026-10-03, distribution/runtime 0.10.0. Ackredit #94 owns the preparation
and semantic-gate correction; the shared publisher correctly preserved its
inputs. Ackredit #93 prepares additive 0.10.1, retaining original 0.10.0
bytes and tag. The owner asks receivers to wait for corrected exact-file
qualification/public handoff before selecting the new checkpoint. Existing
portable >=0.9.0 usage remains usable; no consumer floor or source edit is
required by this observation.

Primary receipt:
`devguide/rollouts/ackredit_010_public_pipeline_92_97_20261004.json`.
#92 remains partial for the measured ordinary operator route and steps/effort.
#97 separately retains the principal maintainer's decision to keep the APIs
provisional. No new shared gate, policy pin, withdrawal, overwrite, rebuild,
retagging, guide rollout or fresh central runtime qualification follows.


### Later owner correction checkpoint — 2026-10-05

Ackredit #93 now reports staged 0.10.1 at
`dd500842b6085111e01e62cfc243f68406eb8cc7`, SHA-256
`26e75a0780ad4e6abc2de55df90b29b4a2aa4e510d6b50fa54a5812ad929228e`,
with installed 37268949725 and real receiving 37268949118 passing. These
are new owner-reported inputs, not independently qualified by the preceding
0.10.0 review. Its final public clean-installation/tag handoff and central
exact-file review remain distinct pending work. Provisional classification
continues through any corrected delivery until explicitly decided otherwise.


## Additive Ackredit 0.10.1 delivery review — 2026-10-05

The corrected delivery is complete under owning Ackredit #93/#94, closed
at `f71d242705b4b65302fb3eecb0659207d56c47dd`. Independent central review
binds producer `dd500842b6085111e01e62cfc243f68406eb8cc7`, archive
`ackredit-0.10.1-py_0.tar.bz2` and SHA-256
`26e75a0780ad4e6abc2de55df90b29b4a2aa4e510d6b50fa54a5812ad929228e`.
The existing operator returns `public-verified` without mutation or dispatch;
public downloaded bytes, solver index, labels and original-producer tag agree.
Packaged CFF now matches version 0.10.1/date 2026-10-04 and both producer
copies. The provider's relevant source/installed guards repair its semantic
preparation omission. The shared publisher correctly preserves bytes.

The selected four-run staging/installed/receiving/promotion episode
37268654191/37268949725/37268949118/37269544505 has four successes, zero
observed failures; the aligned publication subset has three runs. Native
creation/update envelope is **13m11s**, including queues and parallel receiving,
excluding source CI, clean public installation and final owner closure. This
is not measured human effort or a controlled comparison with prior episodes.
Operator use before dispatch, actual manual steps and measured active time
are still unreported. The existing owner recording request remains pending;
central post-publication verification does not prove end-to-end adoption.

Native source matrix 37268372798 has 1,708 passed/seven skips per cell;
installed matrix has 1,641 passed/eight skips per cell. Owner clarification
of collection differences is still pending, without treating them as a proven
defect. Independent verification of ten receiving ZIPs and provider-owned
summary proves a third scope: eight cells/six tests each, 48 total, no skips,
with identical Conda identity before/after science. Owner-retained fresh
public Linux/Python 3.14.7 installation and 56 public Sabueso receiving tests
are inspected separately and not repeated centrally.

Receipt: `devguide/rollouts/ackredit_011_public_pipeline_92_97_20261005.json`.
Original 0.10.0 bytes, tag and limited evidence remain intact. #92 stays
partial for ordinary operator use/steps/effort; #97 separately keeps the APIs
provisional. No additional policy gate, rebuild, withdrawal, consumer minimum
or scientific execution follows from this read-only reconciliation.


## Additive ArgDigest 0.15.0 profile qualification — 2026-10-08

The maintenance need reported from #45 is complete. Existing `argdigest-core`
remains byte-for-byte preserved for the 0.14.0 review; opt-in
`argdigest-core-v2` adds original 0.15.0 producer
`57447cc4ec1f7ce85078f8a939892efd075bc919` and reviewed guard source
`15b1921b6bbe1b4bf4abcb091e91f51d74927325`. Exactly one of five bound inputs
changes: `core_runtime_probe.py` retains all earlier assertions and adds explicit
pipeline and lower-bound restrictive-capture refusal checks using the public
DigestConfig/DigestError API. Current reviewed guard/source inputs are identical
to those at the original producer. No component code is imported or changed.

The historical profile actually rejects the changed producer before native
acquisition (`additional-gate source drift: devtools/conda-build/core_runtime_probe.py`).
The new profile runs through the actual shared `prepare_handoff` operation:
original producer 37524900085, full installed 37525789576 and all twelve core
jobs in 37525794773 are independently verified with native source/workflow/title/
attempt/job/required-step evidence. Exact current public metadata/index/hash
agree with original `argdigest-0.15.0-py_0.tar.bz2`, SHA-256
`b0f22038a8ad1c888dca10adedaca0fa14d2383a685a97c0602b7ca05f29d6a1`.
Outcome: **public-verified, next_command null, mutation_performed false**.
No matrix or package operation is dispatched, rerun, rebuilt or promoted.

The profile keeps the component's required core_run_id and nonoptional local
guard before publication; original source/file/installed identity bindings,
complete twelve-cell matrix, native digest-bearing title and executed core
steps remain mandatory. Unknown or moved source inputs still fail closed. Both
profiles remain explicitly selected and repository-scoped; no default/migration
or other consumer change is introduced. The actual revised optional profile is
protected by `tests/test_noarch_gate_profiles.py::AdditionalGateTests::test_reviewed_profile_revision_preserves_the_legacy_source_binding`:
selection fails before addition; afterwards its tests protect historical source
binding, changed probe, unchanged other inputs/gates and repository isolation.
All 21 focused profile/operator tests and Ruff/offline checks pass.

Advance notices reach #92 and uibcdf/argdigest#31 before publication. Operations
guidance selects v2 for the reviewed 0.15.0 inputs and retains the historical
choice; future drift still needs source review rather than blind hash refresh.
[Durable source/native/operator receipt](../rollouts/argdigest_core_profile_v2_92_20261008.json).
#92 remains partial for ordinary end-to-end operator use, actual manual steps
and separately measured active human effort. This post-publication qualification
is not that owner measurement or proof of effort reduction. Action-v2.3.0
adoption remains separate under #87; public release and consumer adoption under
#45/#98/#106 keep their own identities and owners.
