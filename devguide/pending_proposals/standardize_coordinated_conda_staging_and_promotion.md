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
**Status:** Active proposal with MolSysMT/MolSysViewer as the measured pilot; no shared
policy or reusable workflow is accepted yet.

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
   normal path to the public `main` label. Routine push, pull-request and scheduled CI
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
   rather than replacing bytes. Public builds use a distinct coordinate or promote the
   already verified bytes according to a documented strategy. A version/build coordinate
   never denotes two byte sequences.
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

Assumed, pending the pilot execution: the MolSysViewer staging build can reproduce the
previous local `build_against_staging.sh` result on GitHub and close the cycle without
`--no-test`; and the complete installed-pair matrix will then solve on every target. The
Pytest Receptor pilot replaces the earlier assumption about reuse by another publisher:
the shared noarch pattern transferred without inheriting MolSysMT/MolSysViewer-specific
names, although a central conformance unit is still pending.

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
