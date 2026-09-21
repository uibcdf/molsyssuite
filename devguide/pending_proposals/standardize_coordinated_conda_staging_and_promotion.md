---
summary: Standardize coordinated Conda staging and promotion across coupled components.
issue: uibcdf/molsyssuite#27
status: active
opened: 2026-09-19
closed:
verification: measured
area: [packaging, release, ci, governance]
guard:
normative:
blocked_by: []
supersedes: []
---

# Coordinated Conda staging should be a shared release contract

**Reported:** 2026-09-19, while reconciling the MolSysMT stabilization assessment with
MolSysViewer's request for an installable MolSysMT 0.22.0.
**Status:** Active proposal with MolSysMT/MolSysViewer as the measured pilot. The
two-route release contract below is under review; no shared policy or reusable workflow
has been accepted yet.

## What

Define one MolSysSuite contract for staging and promoting Conda releases when two or more
components must be tested together before either can safely reach the public channel.
The contract must separate shared release semantics from package-specific mechanics:
MolSysMT produces five native ABI3 artefacts, while MolSysViewer produces one
`noarch: python` artefact. They cannot use one literal build matrix, but they should not
independently reinvent candidate identity, staging labels, bootstrap exceptions,
evidence, promotion order or rollback.

The initial pilot is the mutual hard-dependency boundary between
`uibcdf/molsysmt#195` and `uibcdf/molsysviewer#82`/`#88`. Its output should be reusable
by later MolSysSuite components and clear enough to copy only when a reusable workflow
would erase a real package-topology difference.

## How

The proposed common contract has eight layers.

1. **Immutable candidate identity.** A staging dispatch names a full commit SHA, a stable
   three-part version and a non-negative build number. The checkout proves its SHA; an
   existing version tag must identify that SHA, while an untagged staging candidate may
   receive only a runner-local ephemeral tag for version derivation. Staging does not
   create or move a remote tag.
2. **State separation.** Manual candidate work uploads only to
   `uibcdf/label/staging`. A GitHub Release, after all exact-commit gates pass, is the only
   normal path to the public `main` label. A routine release with no staged candidate
   may build, test and upload once to `main`; a release with a staged candidate must
   promote the verified exact file instead. Routine push, pull-request and scheduled CI
   consume the public channel; candidate consumption is an explicit manual input.
3. **Narrow bootstrap exception.** A mutual package cycle may require the first producer
   to upload one staging build without its runtime test. The report must prove why the
   environment cannot exist yet and name the counterpart that closes the cycle. The
   counterpart must run its package test when its just-built artefact makes the cycle
   solvable. No public build may retain `--no-test`.
4. **Exact-pair validation.** The installed gate names both versions, all supported
   Python minors and all claimed platforms. It checks distribution provenance, versions,
   native extensions where present, required packaged resources and an explicit
   environment inventory. A source checkout or editable installation cannot satisfy it.
5. **Coordinate integrity.** Staging repair is additive: increment the build number
   rather than replacing bytes. If a release was staged, public publication promotes the
   already verified exact file by adding the target label; it does not rebuild, re-upload
   or use `--force`. Promotion names the full owner/package/version/subdir/filename
   identity and expected SHA-256, verifies both source and target registry state, and
   preserves the source label. If no candidate was staged, a direct release may build,
   test and upload its new coordinate to `main` exactly once after a fail-closed registry
   preflight. A version/build coordinate never denotes two byte sequences.
6. **Ordered promotion and rollback.** The dependency that lets the counterpart's public
   build solve is published first, followed immediately by the counterpart. Failures are
   contained by labels and replacement build numbers, not deletion or overwriting. The
   previous exact `conda list --explicit` remains available as rollback evidence.
7. **Structured evidence.** A reviewed release of
   `uibcdf/action-build-and-upload-conda-packages` emits its bounded producer evidence and
   an `if: always()` step retains it. GH Run Receptor is the first run-inspection path,
   using `conda` plus `expected_platforms` for native matrices and
   `package_kind: noarch` for noarch packages. GitHub conclusions and independent channel
   queries remain authoritative; a receptor report alone never authorizes publication.
8. **Profiled reuse.** Shared tooling should provide small, guarded units: candidate
   validation, exact checkout, staging/public state checks, evidence retention and
   conformance fixtures. Native/ABI3, noarch and pure metapackage profiles keep their
   distinct build mechanics. Publication tokens remain in the owning repository rather
   than moving into a central workflow merely to reduce YAML.

### Proposed two-route release decision

The shared contract should preserve the routine user action of publishing a stable
GitHub Release when no pre-public Conda candidate is required. Staging is a gate for a
release that needs installed-candidate, cross-package, cross-platform or other
pre-public evidence; it is not a mandatory extra upload for every patch release.

**Choose the route before tagging or publishing.** The release owner records the
decision and its evidence in the release checklist or an immutable release-plan record
associated with the candidate commit. The exact storage mechanism is a design task, not
permission for an unrecorded choice. Staging is required when at least one of these
conditions holds:

1. A release gate must run against an installable Conda artifact or an exact combination
   of component artifacts **before** any of them is visible on the public channel. This
   includes the MolSysMT--MolSysViewer dependency cycle and an ordered bootstrap.
2. The release changes claimed Python/platform support, native packaging, packaged
   resources, or dependency resolution in a way that requires a clean installed-package
   check that the ordinary build/test job cannot complete before its public upload.
3. A candidate file for the same version already exists under staging, or the version has
   ambiguous registry state. Build repairs use a higher build number; the public job
   must never reinterpret an older staged file as a fresh direct release.
4. A coupled or multi-artifact release requires the full set to pass as a unit before the
   first public label is added; per-job success is insufficient for that gate.

The direct route is allowed only when **none** of those conditions applies: dependencies
are already public and resolvable, the exact commit passed its ordinary CI and release
checks, the action tests every package it will upload, no pre-public installed-consumer
gate is required, and the target version is unoccupied in every relevant registry label.
Being a patch release or a pure-Python package does not alone grant the direct route;
conversely, being a MolSysSuite component does not alone mandate staging. If the release
owner cannot establish these facts, the conservative decision is staging or a paused
release, not an optimistic direct upload.

**Minimum decision evidence.** Before the tag or Release is published, a reviewed
release checklist or versioned plan names the intended `X.Y.Z` version, candidate
commit, chosen route, responsible maintainer, reason against the criteria above, and
the exact required CI/package/installed gates. A routine direct release needs no new
GitHub issue merely for choosing its route. The workflow retains a machine-readable
receipt bound to the final tag SHA that records the chosen route, passed gate/run IDs,
the time and result of the all-label registry preflight, package coordinates and
SHA-256 digests, and an independent public poststate query. A staged release additionally
records the expected digest for every source file, its staging label, installed-candidate
gate, and promotion receipt. The decision is reviewable before publication; the receipt
proves what actually happened afterward. Do not put secrets or raw credential-bearing
API responses in either record. The storage and schema of the pre-tag plan should be
chosen centrally before this proposal becomes normative.

- **Direct route, no staged candidate for this version.** The stable release event checks
  the exact tag/commit and required gates, confirms that the intended version has no
  existing staged or public files in any target subdirectory, then builds and tests the
  Conda package and uploads each new coordinate to `main` once. It never uses `--force`,
  retains producer evidence and independently checks the resulting public records.
  A registry query error, ambiguous existing version, or retry with an already occupied
  coordinate fails closed rather than guessing that a second upload is safe.
- **Staged route, candidate already uploaded.** The release tag must identify the tested
  candidate commit. The publisher names every exact staged build and SHA-256, verifies
  the required installed gates, and uses the shared `promote` Action to add `main` to
  those same bytes. The release event must not rebuild or upload that version. Until an
  immutable candidate manifest supports trustworthy automatic selection, an explicit
  promotion dispatch is safer than choosing the newest build or copying a whole label.

Both routes require stable `X.Y.Z` tags, the same no-overwrite rule, package tests,
bounded evidence, independent registry verification and version-scoped concurrency.
They differ only in whether a verified staged file already exists. The route must be
declared or mechanically proven before any registry mutation; absence of a staging
artifact is not itself evidence that a release has passed its normal scientific gates.

A release-event direct upload has a known non-atomicity: the GitHub Release becomes
public before the Conda job finishes. A failed job must be reported as an incomplete
release, never as a successful package publication. The central policy should decide
whether that bounded window is acceptable for routine independent packages or whether
draft-first publication should be required. This question does not justify silently
removing existing automatic Conda publication from every component.

The first design task is to compare three implementation shapes:

- a reusable candidate-preparation workflow plus local build jobs;
- a centrally versioned canonical template with machine-checked invariants; and
- a small composite validation Action used before and after local package Actions.

The result may combine them. Reuse is successful when it centralizes the decisions that
must agree, not when unrelated recipes are forced through one parameter-heavy workflow.

## Why

The MolSysMT/MolSysViewer cycle required several rounds of investigation before the safe
sequence was visible. Keeping that result only in two local workflows would make every
future component pay the same reasoning cost and would let the implementations drift:
one repository could publish directly to `main`, silently consume staging in normal CI,
skip both package tests, overwrite a validated coordinate, or treat a green build as
proof of registry publication.

The shared value is broader than this cycle. Exact candidate identity, non-overwriting
coordinates, explicit pre-release channels, evidence retention and independent registry
verification apply to every MolSysSuite Conda publisher. Central ownership lets one
review and one set of negative fixtures protect all adopters while local repositories
retain authority over scientific tests, recipes and release decisions.

## What is measured and what is assumed

Measured on 2026-09-19:

- MolSysMT run `33849332945`, commit
  `e5820d4794f8ce31a1f64e345c5edf9073ade975`, published build-2 ABI3 artefacts for
  `linux-64`, `linux-aarch64`, `osx-64`, `osx-arm64` and `win-64` to staging. Independent
  `conda search --subdir` queries found all five coordinates.
- A Linux dry-run with staging resolves MolSysMT 0.22.0 on Python 3.12 and fails on 3.13
  because its hard MolSysViewer dependency can find only old interpreter-specific public
  packages. This reproduces the cycle rather than inferring it from YAML.
- MolSysViewer commit `c7ec68fa` implements exact-SHA staging, separate build numbers,
  tested noarch publication and explicit staging inputs for its CI, E2E and notebook
  workflows. Its complete local suite passed 2,067 tests with 13 accepted skips under 12
  workers in 65.80 seconds; 16 distribution-contract tests, Ruff, developer-guide index
  validation and a build-0 noarch recipe render also passed. No package was uploaded.
- MolSysMT commit `664a948e1` removes the stale default MolSysViewer version from its
  five-platform by three-interpreter pair gate. Its workflow contract tests and
  developer-guide validator pass.
- The inspected Linux `py311` records for ArgDigest 0.12.1, DepDigest 0.10.0 and SMonitor
  0.13.0 are platform/interpreter-specific, not noarch; separate 3.12 and 3.13 records
  exist on that platform.
- Both repositories already carry exact GH Run Receptor rules: MolSysMT's installed-pair
  gate declares the five expected native platforms, and MolSysViewer's publisher declares
  `package_kind: noarch`.
- Pytest Receptor became an independent noarch reuse pilot at commit `f2ff0e3`. Its manual
  staging run `35528151054` accepted a full candidate SHA, runner-local version tag, and
  build number; uploaded only `pytest-receptor-1.1.0-py_0` to
  `uibcdf/label/staging`; retained the package Action's producer evidence; and was
  summarized by gh-run-receptor as `PASS`, `package=noarch`, one of one jobs, and one
  available artifact. A separate channel query and clean CPython 3.14.7 environment then
  verified the exact distribution, module version, installation path, Python constraint,
  and plugin entry point. No remote tag, GitHub Release, or public-channel artifact was
  created.
- The later Pytest Receptor 1.1.0 release exposed the missing promotion primitive. Release
  run `35532680623` rebuilt the exact `py_0` filename and Anaconda.org rejected its upload
  to `main` with HTTP 409 because that coordinate already existed under `staging`.
  gh-run-receptor correctly classified the run as failed and retained producer evidence.
  Neither `--force` nor promotion of the older candidate was accepted: the release tag
  included later documentation and therefore named a different source commit. Exact tag
  `14e996430fa2b3810ae68f8b7fed16298dc7733b` was instead rebuilt additively as `py_1` in
  staging by run `35533044229`; its public registry digest is
  `4b56e6fc7c24e3f01d771c989bd7ed4bac9cf40c05e22f831a0ffff8defcd7dc`, and a clean
  CPython 3.14.7 environment installed and loaded it successfully. Provider issue
  `uibcdf/action-build-and-upload-conda-packages#43` now owns a reusable exact-file,
  digest-verified label promotion path.
- The Pytest Receptor pilot passed promotion run `35571349099` with the reusable action
  `v2.2.2`. Earlier attempts `35534760532` and `35568720075` failed safely on the
  Anaconda `/channels/` endpoint's `api:read` requirement, without changing the public
  label. The provider instead reads the public `/release/` metadata with ambient
  credentials explicitly discarded, reserves the upload token for one exact label write,
  and checks the public poststate. Hosted action run `35570832180` passed all three jobs.
  Independent public Conda metadata found the exact staged SHA-256 of
  `pytest-receptor-1.1.0-py_1.tar.bz2` on `uibcdf/noarch`, and a fresh Python 3.14.7
  environment resolved and loaded the exact build from the public channel. This validates
  exact-file promotion for one noarch publisher; native ABI3 matrices and the coupled
  MolSysMT/MolSysViewer release remain separate pending gates.
- SMonitor independently reproduced the same coordinate collision on release 0.16.0:
  release-triggered upload run `35587726937` received HTTP 409 after a `py_0` file had
  already been uploaded to staging. Its exact release-commit `py_1` candidate from
  staging run `35587197005` had SHA-256
  `a7f0ea073786354695c606e89959e67fcd4afc910a42683bba00955eb17163d7`.
  SMonitor removed the second-upload release path in commit `6ac5c73` and adopted the
  shared `promote@v2.2.2` Action. Promotion run `35589475337` passed; an independent
  public-channel query returned the same `smonitor-0.16.0-py_1.tar.bz2` SHA-256, and a
  fresh Linux Python 3.14.7 environment installed that exact public build and loaded
  its module and CLI. Local recovery is tracked by `uibcdf/smonitor#19`. This is a second
  noarch publisher proof, not evidence for native ABI3 promotion or the coupled pair.
- The 0.16.0 recovery also exposed an overcorrection: SMonitor's current Conda build
  workflow has only `workflow_dispatch`, and its promotion workflow is also manual.
  Publishing a routine future `0.17.0` GitHub Release would therefore not start any
  Conda upload. That preserves safety for staged candidates but unintentionally removes
  the previous automatic direct-release path. DepDigest still combines staging dispatch
  with a release-triggered fresh build/upload, reproducing the collision risk when both
  use build 0; ArgDigest still has a release-triggered direct uploader. Neither existing
  implementation is yet the proposed guarded two-route contract.

The [Anaconda label documentation](https://www.anaconda.com/docs/tools/anaconda-org/maintainer-guide/labels)
confirms that a non-`main` label hides a file from routine resolution and that labels
can be added to make that file public. The
[GitHub release-event documentation](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#release)
confirms that a release-triggered workflow starts after the release activity; it cannot
make Conda publication an atomic prerequisite of the already public GitHub Release.

Assumed, pending the pilot execution: the MolSysViewer staging build can reproduce the
previous local `build_against_staging.sh` result on GitHub and close the cycle without
`--no-test`; and the complete installed-pair matrix will then solve on every target. The
Pytest Receptor and SMonitor pilots replace the earlier assumption about reuse by other
publishers: the shared noarch pattern transferred without inheriting
MolSysMT/MolSysViewer-specific names, although a central conformance unit is still
pending.

## Alternatives and refuted paths

- **Publish MolSysMT directly to the public channel to unblock MolSysViewer.** Rejected:
  it turns the consumer green by distributing the producer before the pair is validated.
- **Lower MolSysViewer's MolSysMT floor.** Rejected: 0.22.0 introduces an import-time API
  that MolSysViewer requires; the lower environment would solve and fail on import.
- **Put staging permanently ahead of the public channel.** Rejected: routine CI would
  silently test mutable pre-release dependencies and a green result would cease to
  describe the supported installation path.
- **Use `--no-test` on both sides of the cycle.** Rejected: the second package is present
  in its own conda-build test channel and can close the solver loop. Extending the
  exception would remove the first available installed-package proof.
- **Make one identical reusable build workflow.** Rejected as a goal: native ABI3,
  noarch and metapackage publishers expose different meaningful matrices. Common
  semantics and reusable units are preferable to a universal workflow full of inert
  inputs.
- **Leave the solution local because only two repositories need it today.** Rejected:
  exact identity, state separation, evidence and coordinate integrity already apply to
  every package publisher, and the central repository itself still has an unpinned
  publication Action and no structured producer evidence.
- **Move or recreate the existing MolSysViewer 0.22.0/0.23.0 tags.** Rejected: those tags
  predate the packaging fixes and immutable release identities must not be rewritten.
- **Rebuild a staged coordinate and upload it to another label.** Rejected by measured
  Anaconda.org behavior: labels do not create a separate file identity, so the second
  upload conflicts. `--force` would replace bytes rather than prove promotion and is
  forbidden. An exact digest-verified label addition is the required operation.
- **Require staging for every routine release.** Rejected as a universal rule under
  evaluation: it adds a manual publication step even when the ordinary release job can
  build and test the only package before its first upload, and it regresses SMonitor's
  expected release workflow. It remains mandatory when the pre-public gates above apply.
- **Always rebuild automatically on GitHub Release.** Rejected: a previously staged
  coordinate collides or distributes bytes different from those already tested. An
  ambiguous staged version must stop with an actionable promotion path.

## Scope and exclusions

The initial applicability profile is a MolSysSuite component that publishes a Conda
package, plus any component participating in a coordinated dependency window. Wave-1
MolSysMT and MolSysViewer are the pilot; the central MolSysSuite metapackages are an
immediate conformance case. Other members adopt only after their package topology is
classified.

Excluded: choosing the next MolSysViewer version, authorizing any tag or Release,
changing scientific compatibility, replacing component release gates, PyPI/npm/Zenodo
publication, Anaconda credentials, and claiming that a successful upload command proves
the external channel state.

## Acceptance criteria

- A normative central document defines candidate identity, staging/public state,
  bootstrap eligibility, exact-pair validation, coordinate immutability, promotion,
  rollback and evidence requirements.
- Applicability profiles cover at least native/ABI3 and noarch packages; a component can
  determine which rules apply without repository-name exceptions.
- The design chooses and versions the reusable workflow, canonical-template and/or
  composite-validation units. Shared units contain no component-specific package names
  and do not centralize publication secrets.
- Negative fixtures fail when a public path contains `--no-test`, a manual path uploads
  to `main`, candidate identity is mutable, staging becomes a routine-CI default,
  producer evidence can disappear after failure, or a native matrix omits a required
  platform.
- The shared release checklist makes the pre-tag staging decision explicit, with
  objective mandatory triggers and a documented direct-route eligibility test. Negative
  fixtures reject a direct release when a same-version staged file exists, registry
  preflight is inconclusive, a required installed-candidate gate is unmet, or a retry
  would overwrite a coordinate. A routine no-staging release retains its automatic
  build/test/upload behavior and independently proves the public poststate.
- MolSysMT and MolSysViewer complete the exact staged-pair pilot and record receptor plus
  independent channel evidence without treating either alone as publication proof.
- The central MolSysSuite Conda publisher either adopts the accepted contract or records
  a time-bounded profile exception; it no longer floats a package Action branch.
- At least one additional component evaluates the shared unit or template and reports
  whether it removes local decision duplication without obscuring its package topology.
- The component-facing guide routes Conda publishers to the normative policy, and the
  repository conformance gate checks every objectively enforceable invariant.

The future normative record and conformance fixtures will close this proposal; completing
only the two-component pilot is not sufficient.

## Local implementation issues

- `uibcdf/molsysmt#195` — native ABI3 producer and exact installed-pair matrix.
- `uibcdf/molsysviewer#82` — release decision for the existing tags and future candidate.
- `uibcdf/molsysviewer#88` — hosted gates blocked at the shared dependency boundary.

Open component issues only where adoption requires a concrete local change. Do not file
one in every registered repository pre-emptively.

## Dependencies and risks

The central design is not blocked by the current release window; the pilot's final
evidence depends on the linked component issues. Main risks are over-generalizing from
one cycle, putting credentials into central automation, masking package topology behind
generic inputs, and letting a shared validator check YAML form rather than release
intent. Mutation-style negative fixtures must demonstrate that each gate rejects the
unsafe behavior it names.

## Provenance

Measured 2026-09-19 from clean synchronized `main` checkouts of MolSysMT and MolSysViewer,
Conda 26.5.3/conda-build 26.5.0 on Linux x86-64, live UIBCDF staging and public channel
metadata, GitHub issue/release/workflow state, and gh-run-receptor 1.0.0's canonical
client guide. No tag, GitHub Release or new package artifact was created while drafting
this proposal.
