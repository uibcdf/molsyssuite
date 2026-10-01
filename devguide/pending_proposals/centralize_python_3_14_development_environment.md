---
summary: Centralize a Python 3.14 development environment for MolSysSuite
issue: uibcdf/molsyssuite#52
status: active
opened: 2026-09-26
closed:
verification: inspected
area: [python, development, packaging, coordination]
guard:
normative:
blocked_by: []
supersedes: []
---

# Centralize a Python 3.14 development environment for MolSysSuite

**Reported:** 2026-09-26, after a host-local Python 3.14 development environment
was assembled for MolSysMT and MolSysViewer.
**Status:** Active; an initial opt-in Conda recipe and editable-install guide exist,
but the recipe is not yet a complete Linux suite development contract.

## What

Maintain a discoverable Conda/Mamba recipe named `molsyssuite@uibcdf_3.14` in this
repository for the common third-party dependency base, with separate guidance for
editable MolSysSuite checkouts. The primary developers work on Linux, so Linux-64 is
the intended development platform and macOS/Windows are not gates for this recipe.
This is an environment definition, not a new Git repository.
It must never be presented as proof that every member has been admitted to Python 3.14.

## How

The recipe is `devtools/conda-envs/molsyssuite-dev-py314.yaml` plus the neighboring
`README.md`. It uses public `uibcdf` and `conda-forge` channels and now pins the
coherent official `pyside6`, `qt6-webengine`, and `qt6-positioning` 6.11.2 stack.
The guide installs the eight currently eligible component checkouts with
`pip --no-deps --no-build-isolation -e`, verifies package metadata and imports,
and retains the former UIBCDF 6.10.1 lane only as a separate rollback recipe.

The next increments should make the recipe reproducible in clean CI environments,
define update/pinning policy, check representative science and viewer behavior, and
add each newly admitted component. `uibcdf/molsyssuite#51` tracks the six members
whose current metadata still excludes 3.14. The phased support policy and admission
remain under `uibcdf/molsyssuite#29`.

## Why

One developer host now has a working Python 3.14.7 base with the MolSysMT and
MolSysViewer source pair, eight editable MolSysSuite packages, and official
Qt 6.11.2 from conda-forge. That experience should not remain a machine-specific
command or be rediscovered independently by each component team. The existing
shared development recipe targets Python 3.12; replacing it prematurely would
lose an established path.

## What is measured and what is assumed

**Measured locally on Linux x86-64:** The host-local environment created on
2026-09-26 resolved Python 3.14.7, `qt6-main=6.10.1`, and five aligned local UIBCDF
Qt packages. Eight compatible source checkouts installed in editable mode;
`python -m pip check` reported no broken requirements. Selected MolSysMT tests passed
16/16 and selected MolSysViewer integration/Qt tests passed 14/14 with at most 12
workers. This validates the source of the recipe, not a fresh creation from the new
YAML on another Linux host.

The new YAML itself passed a Linux-64 dry-run solve with Conda 26.5.3,
`conda env create --file devtools/conda-envs/molsyssuite-dev-py314.yaml
--prefix /tmp/molsyssuite-py314-dry-run --dry-run --offline --solver libmamba
--json`, using cached `uibcdf` and `conda-forge` metadata. This produced a resolved
package list and exited 0; no environment was created. It does not establish a clean
download/install on a second Linux host.
An independent `mamba env create --dry-run --offline --file
devtools/conda-envs/molsyssuite-dev-py314.yaml --prefix
/tmp/molsyssuite-py314-mamba-probe --json` also exited 0 with `success: true` and
`dry_run: true` using cached metadata. This confirms that both environment-file
frontends accept and resolve the initial Linux profile, not that either installed it.

**2026-09-27 canonical migration on the same Linux host:** A fresh prefix
created from the Qt-pinned YAML resolved Python 3.14.7 and official
`pyside6`, `qt6-main`, `qt6-webengine`, and `qt6-positioning` 6.11.2, all from
conda-forge, with none of the five UIBCDF Qt/PySide packages. After eight
editable installs, `python -m pip check` reported no broken requirements.
Viewer's standalone and Qt transport files passed 54 tests with two expected
graphical/GPU skips; its distribution/movie files passed 63 tests with one
expected skip after adding `python-build` and `imageio` to the recipe. The
MolSysMT–Viewer integration directory passed 116 tests. The shared
`molsyssuite@uibcdf_3.14` prefix was then migrated from the five local
UIBCDF packages to official Qt 6.11.2. It passed the same 54-case Qt selection,
the same 63-case distribution/movie selection, the 116-case integration
directory, a real Xvfb window smoke, and an Xvfb/SwiftShader full-render
smoke. This is Linux-host evidence, not visible-window or native macOS/Windows
certification.

One full Viewer-suite run in the fresh prefix before the recipe/test correction
yielded 2,132 passed, 17 skipped, and three failures: missing `python-build`,
missing `imageio`, and a test expecting `macos-latest` after the workflow was
pinned to `macos-15` for arm64. The affected files passed after those fixes;
the complete suite was not rerun, following Viewer's one-full-run discipline.
Do not report this as a green full-suite run.
The final YAML, including those two test dependencies, passed a separate
offline dry-run solve; the fresh prefix received them through a targeted
Conda install before the affected tests were repeated.

**Inspected:** The existing `molsyssuite-dev.yaml` pins Python 3.12 and includes
AmberTools and a broader optional stack. The six remaining components in
`uibcdf/molsyssuite#51` exclude Python 3.14 in fetched `origin/main` metadata.

**Not established:** A clean, independent YAML-based installation on a second Linux
host; tests for all optional integrations or every registered component.
macOS and Windows are outside this development-environment
issue's acceptance scope; package release gates retain their own platform policies.

## Alternatives and refuted paths

Replacing the Python 3.12 recipe now would erase a usable older profile while the
3.14 transition remains incomplete. Embedding an absolute local Qt channel in the
portable YAML would make it fail on every other host. Installing packages that still
declare `python<3.14` with a metadata override would conceal their migration work.

## Scope and exclusions

The initial environment serves compatible MolSysSuite Python components in local
development. It does not publish packages, update the stable suite Python baseline,
or grant component admission. Component-specific dependencies and fixes remain with
their owning repositories. The central Qt lane is now an official conda-forge
solve tested on this Linux host; package release and native-platform gates
remain separate.

## Acceptance criteria

2026-10-01 administrative delivery: the reusable environment profile derives the
eight eligible editables from the registered transition and distinguishes six
publicly admitted tools/support libraries from the authorized MolSysMT/Viewer
pair. It rejects hidden channels, historical Qt forks and incompatible source
metadata. The new Linux workflow creates an uncached environment, installs the
eligible cohort without changing the Conda solution, runs `pip check`, verifies
editable import origins and loads the official Qt/WebEngine libraries. It retains
source and Conda receipts even on failure. Hosted execution is pending; do not
claim a second-host creation or full scientific/GUI qualification yet.

- The recipe creates the named environment from a fresh checkout on Linux-64, without
  relying on undocumented machine-specific paths.
- Each eligible component can be installed in editable mode with `pip check` and
  representative local tests; newly admitted members join the maintained set.
- Every registered Python component is covered or has a bounded exception linked to
  its owner issue.
- The Qt/PySide route is reproducible from conda-forge without a hidden local
  channel or a required UIBCDF fork; an explicitly separate rollback remains.
- A CI or equivalent automated guard detects stale channel/package constraints.

## Local implementation issues

The initial recipe is central. Component migrations are tracked by
`uibcdf/molsyssuite#51` and their component-owned follow-up issues.

## Dependencies and risks

The recipe depends on public Conda channel continuity and a Rust/Cargo toolchain for
the editable MolSysMT build. Optional scientific packages can create solver pressure;
the environment should remain usable for core development if one optional integration
is temporarily unavailable.

## Provenance

Inspection and local environment measurements on 2026-09-26, Linux x86-64,
CPython 3.14.7. The exact validation commands and initial package selections are in
`devtools/conda-envs/README.md` and the accompanying YAML.
