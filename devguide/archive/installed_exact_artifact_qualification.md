---
summary: Qualify registered noarch bytes through a corrected workflow without changing producer identity.
issue: uibcdf/molsyssuite#88
status: resolved
opened: 2026-10-03
closed: 2026-10-03
severity: high
verification: reproduced
area: [distribution, tooling, ci]
guard: tests/test_installed_noarch.py
normative: devguide/noarch_conda_workflow.md
blocked_by: []
supersedes: []
---

# Installed exact-file qualification and source binding

## What

Pytest Receptor's installed run `37136496168` fails all eight cells because
strict channel priority excludes its newer staging MatchSpec behind the older
public package. A corrected qualification wrapper also has a different native
head from the original producer; their identities must remain distinguishable.
Ackredit's related four-step preparation mismatch is uibcdf/molsyssuite#89.

## How

Reviewed owner PR #91 verifies the archive digest and inspected runtime
requirements, solves dependencies through ordinary strict public channels at
the cell's exact prefix/Python minor, then installs the exact staging URL.
The existing installed file/resource/import and final provenance checks remain.

Preparation checks out the original candidate and binds its source/file/hash,
full declared matrix, native qualification head, run and attempt in
`molsyssuite.installed-source@1`. A different reviewed qualification SHA must be
explicitly supplied to promotion; the verifier checks native jobs, complete
executed steps and the bounded attempt-qualified binding artifact including
its native ZIP digest. Same-source callers remain compatible. Promotion checks
out the original producer, independently verifies its existing source gates,
and adds a public label to the same tested file through the existing provider.

PR #90 supplies the regression reading the real workflow's fourth provenance
step, compatibility with the exact legacy three-step list, and negative lists.
Both proposal histories are preserved by central integration.

## Additional measured launch defect

PR #91 source `3350615eee8c95903aca916e42789ecbdcc1f8ef` repairs direct helper
launch under safe-path mode. Native receiving run `37148090965` then installs
and verifies the exact Pytest Receptor file on all eight cells, but its native
conclusion remains failure: 210 tests pass and the reporting-protocol test
cannot import `devguide_reports` from its administrative script's directory.
Inherited `PYTHONSAFEPATH=1` causes that independent child-process failure.
Ackredit's unchanged reporting-protocol test reproduces the same failure;
launching the parent with `python -P` without exporting that environment
variable passes the same test.

The shared launch uses `python -P` in the primary scientific interpreter,
importlib collection, and before/after installed-origin guards. Administrative
children retain access to their own reviewed helper directory. A regression
executes the real published launch from a neutral directory with an installed
distribution, a shadow source package and an administrative child script. It
fails on inherited safe-path mode and passes after correction while requiring
safe-path mode and installed origins in the scientific interpreter.

All 286 central tests pass locally on Python 3.14.7. The first hosted integration
run `37150226815` fails this native pytest regression because that administrative
job did not install pytest. Its bootstrap now explicitly installs the bounded
pytest runtime used by the regression; fixture science is not a component suite.
The accepted immutable source and final native result are recorded in the
owning issue before receiving adoption.

## Exact existing candidates

| Owner | Producer source | Registered file | SHA-256 |
| --- | --- | --- | --- |
| uibcdf/ackredit#22 | `598abf993a2409c025de5e912acd7eb45a257ebd` | `noarch/ackredit-0.9.0-py_0.tar.bz2` | `37661090f6ad19a74b8155d8a4d4b4a068c9099f4ceba0743b3abfe887e97fe1` |
| uibcdf/pytest-receptor#32 | `6c4686c55ee5e004160ba4c36a499ff7e5c8a64b` | `noarch/pytest-receptor-1.2.1-py_0.tar.bz2` | `77bf3694bc903f606d4323b88e3bb3aea9628618036b53073f5a5dbd5dbc73cb` |

Successful staging producers are `37136075066` and `37136074225` respectively.
Staging evidence remains distinct from installed qualification and public
delivery. Sabueso's unchanged receiving integration passes on Linux 3.11–3.14
against the exact Ackredit staging file, as recorded in uibcdf/sabueso#108.

## Acceptance and evidence limits

- Reject mismatched source, native run/attempt, file/digest or matrix bindings.
- Install the exact candidate while keeping dependency priority strict and public.
- Retain all four provenance/scientific steps and unchanged component tests.
- Pass central regressions/governance and publish an immutable accepted workflow.
- Complete all eight declared Linux/macOS-arm64 Python 3.11–3.14 installed cells
  before a component promotes its candidate.

Central source validation alone does not certify those hosted installed cells.
The component owns any scientific failure and the final qualified release.
No package rebuild/replacement is part of this correction. General action
v2.3.0 adoption and withdrawal remain deferred and outside this work.

## Coordination

Shared delivery is uibcdf/molsyssuite#78; Ackredit delivery is
uibcdf/ackredit#22 and its receiver is uibcdf/sabueso#108. Registered shared
publisher consumers are Pytest Receptor, Ackredit, TopoMT, PharmacophoreMT,
ElastNetMT and Lindelint. Owner notices identify old/new immutable sources,
qualification adoption and evidence separately. Existing build/upload/promotion
provider pins and internal-push CI controls are preserved.


## Resolution — 2026-10-03

Accepted immutable source `c3e2b9b3dabf3d1c65349c389a23048957bea21a` directly
integrates PR #90/#91. Its 286 central tests and native governance
`37151428556` pass. The module guard protects exact public dependency solving
and staging URL installation, original/corrected identities, descriptor
alignment, and the actual safe-path launch including administrative children.
The actual-launch regression failed before the process-argument correction.

Pytest Receptor's exact-file run `37148738757` independently passes all eight
cells, with unchanged producer `6c4686c55ee5e004160ba4c36a499ff7e5c8a64b`,
file/digest and separate qualification head
`98e2cf35b24896891b3d95a684facb5c0212c48d`. Its reviewed local equivalent
retains the original test tools and frozen selection; it provides installed
evidence for the real older-main/new-staging case. Public delivery stays with
uibcdf/pytest-receptor#32.

Ackredit's accepted thin caller at
`92871148a762ea4b4786a64d13afd66a5b0bf8e7` uses the accepted shared workflow.
Native `37152044426` passes all eight cells plus prepare against the existing
producer/file/digest recorded above. Promotion `37152421084` then successfully
checks the bounded native artifact and ZIP digest, original source gates,
all declared jobs and four executed required steps before adding the public
label to the same file. Independent public label and solver-index checks pass.
Its retained `molsyssuite.installed-matrix@1` receipt explicitly keeps original
candidate and separate qualification head. No registered archive is rebuilt,
replaced or reuploaded.

The owning issues of all six registered consumers receive the accepted source,
exact adoption/receipt contract and evidence limits. Detailed receipts and
notice URLs are in `devguide/rollouts/installed_noarch_88_89.json`; the concrete
caller handoff is `devguide/rollouts/installed_noarch_88_89.md`. Component
scientific/release work, Windows claims, v2.3.0 and withdrawal remain separate.
