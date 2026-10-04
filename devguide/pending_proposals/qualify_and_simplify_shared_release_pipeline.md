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
