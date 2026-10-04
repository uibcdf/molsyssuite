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
