---
summary: Provide the native Rust toolchain inside the Linux development environment.
issue: uibcdf/molsyssuite#134
status: resolved
opened: 2026-10-24
closed: 2026-10-24
severity: medium
verification: measured
area: [development, tooling]
guard: tests/test_development_environment.py
normative:
blocked_by: []
supersedes: []
---

# Development environment omits its native build toolchain

**Reported:** 2026-10-24, creating the documented environment on a new Linux machine.
**Status:** Resolved; published implementation and fresh hosted bootstrap verified.

## What

MolSysMT editable installation fails with `can't find Rust compiler` after
creating `molsyssuite@uibcdf_3.14` from the maintained YAML. The recipe supplies
`setuptools-rust`, but no Rust/Cargo toolchain or compiler activation.

## How

The newly created Conda environment reports Python 3.14.9 and clean `pip check`.
Both `shutil.which('rustc')` and `shutil.which('cargo')` return `None` inside
`conda run`. The existing CI checks Cargo before creating the environment,
therefore accepting a compiler provided by its runner. MolSysMT's inspected
toolchain file requests Rust 1.97.1. The maintainer supplies a successful
Conda-forge Rust 1.97.1/native-linker inventory from another machine.

## Why

The shared development recipe should provide a reproducible bootstrap for a
new machine, including native compilation and linking. The same environment
is consumed by the reusable development operator, hosted integration probe
and unpublished developer-metapackage preparation.

## Scope and acceptance criteria

- Provide native tools and Python dependencies through public Conda packages,
  without a pip subsection or a rustup prerequisite.
- Verify active-prefix compiler/linker provenance and actual compile/run
  behavior after environment activation, before editable installation.
- Exercise a fresh solve/create and an isolated real MolSysMT editable build.
- Add regressions rejecting the original recipe and pre-creation CI check.
- Preserve the registered fourteen-member cohort and primary clones; retain
  exact evidence separately from scientific/release or whole-cohort claims.

## Measurements and resources

The baseline check uses the named environment's Python 3.14.9; the central
development module resolves to this checkout. Conda's telemetry plugins have
an independent compatibility failure, bypassed only for inspection with
`CONDA_NO_PLUGINS=true`; no base installation is changed.

Task-owned validation root: `/tmp/molsyssuite-native-env-20261024-OLhJKM`.
Owner: this task under uibcdf/molsyssuite#134. The disposable environment,
source copies, caches and raw receipts were removed after retaining bounded
verification evidence. Primary clones and the user-owned environment remain.

The mandatory suite-status fetch reports thirteen current clean clones;
Pytest Receptor (one commit), TopoMT (374) and MolSys-AI (58) are behind their
upstreams. Preserve these primary clones without updating them. TopoMT remains
outside the authorized development cohort.

## Local correction and verification — 2026-10-24

The recipe now declares `git`, `setuptools-rust>=1.13,<2` and
`rust_linux-64>=1.97.1,<2`. The activation package resolves matching Rust/Cargo,
standard libraries, GCC, binutils and sysroot through Conda-forge. The range
keeps the maintainer's known-working baseline and permits newer Rust 1.x.
The development operator's `toolchain` operation verifies active-prefix tool
origins and Conda records, then compiles and runs C and dependency-free Cargo
programs offline. Temporary sources, targets and Cargo cache are managed and
removed on failure as well as success. Shared installation runs this before
pip; CI now checks the toolchain after creating and activating the environment.

The existing metapackage recipe generator also accepts underscores in plain
Conda dependency names, preserving its channel/source restrictions. Its
existing recipe-propagation regression previously failed on `rust_linux-64`
and now passes. No metapackage is published.

Fresh creation with Micromamba 2.4.0 resolves 404 public Conda packages,
including Python 3.14.9, Rust/Cargo 1.99.0, GCC 16.2.0 and sysroot 2.39.
All fourteen isolated source copies install with
`--no-deps --no-build-isolation --editable`, pass dependency closure and actual
editable-origin imports, and load official Qt/WebEngine 6.11.2. MolSysMT and
ElastNetMT's Rust extensions also import directly. All fourteen primary source
commits and clean worktrees are rechecked unchanged.

Central checks: 540 unittest cases, 539 passed and one existing opt-in native
Mamba skip; 28 focused pytest cases and 41 subtests pass. Ruff check/format and
offline governance pass. The missing-tool regression rejects the original
recipe; companion tests reject host tools/incomplete provenance, enforce CI
ordering and protect temporary-cache cleanup when compilation fails.

The [bounded receipt](../rollouts/native_development_toolchain_134_20261024.json)
records exact candidate hashes, native Conda inputs, fourteen source identities,
extension hashes and verification limits. This is local source-development
evidence, without scientific-suite, GUI, public-package or hosted-CI claims.
Keep this issue active until the local fix is published and its applicable
hosted checks are received. The user-owned named environment is unchanged;
the guide supplies update/reactivation commands.

## Hosted bootstrap correction — 2026-10-24

Implementation `a985c12865c39a233cdfb4c4ec176d6fcf9a20be` is published.
Its first governance run `40132032799` executes the offline guard successfully,
then the real editable-version regression fails because the hosted interpreter
does not contain `setuptools.build_meta`. Local development had the backends
from Conda; the lightweight governance and PR-preflight environments must also
declare them for this test. Both workflow bootstraps now explicitly install
setuptools, versioningit 3.3.0 and wheel. The scientific/import qualification
and the original failed run remain separately identified. No user Conda
dependency is installed through pip by this CI-only correction.

## Resolution and hosted receiving — 2026-10-24

Implementation `a985c12865c39a233cdfb4c4ec176d6fcf9a20be` and its hosted-test
bootstrap correction `283607369c45bd77dc19638511338b0959b01d67` are published
on `main`. At the corrected exact source, governance/coverage run
[40132369611](https://github.com/uibcdf/molsyssuite/actions/runs/40132369611)
and fresh Linux development run
[40132369547](https://github.com/uibcdf/molsyssuite/actions/runs/40132369547)
pass. Native run/source/attempt identities, job conclusions and required
executed steps were independently verified with the existing gate verifier.
The fresh run creates the public-channel Conda environment, compiles and runs
the native toolchain probes, installs fourteen eligible editables, checks
dependency closure and verifies source imports and the official Qt runtime.
The first failed governance run remains recorded above, rather than being
relabeled as a successful checkpoint.

Final local code checks execute 544 unittest cases: 543 pass and one existing
opt-in native Mamba case is skipped. Ruff, offline governance and publisher
contract checks pass. The caller's now-updated named environment also passes
the C and offline Cargo compile/run probe; no dependency installation or
whole-workspace reinstall is performed by this delivery task.

The guard `tests/test_development_environment.py` rejects the original recipe
without the native activation package, host/incomplete tool provenance and
the original pre-creation CI ordering. Its compile-failure cases also protect
temporary-cache cleanup. These assertions exercise the reported missing
compiler mechanism rather than merely checking that a command exists.
The [hosted delivery receipt](../rollouts/development_delivery_134_135_20261024.json)
keeps exact hosted proof separate from the earlier local input receipt.
Scientific/release qualification and the eighteen-source compatibility work
under uibcdf/molsyssuite#135 retain their own scope.

## Related work

Previous bootstrap implementation: uibcdf/molsyssuite#52. Workspace scope:
uibcdf/molsyssuite#82. Component-native release qualification and scientific
work retain their existing owners.
