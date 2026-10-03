---
summary: Qualify registered noarch bytes through a corrected workflow without changing producer identity.
issue: uibcdf/molsyssuite#88
status: active
opened: 2026-10-03
closed:
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
