---
summary: Centralize a Python 3.14 development environment for MolSysSuite
issue: uibcdf/molsyssuite#52
status: resolved
opened: 2026-09-26
closed: 2026-10-01
verification: measured
area: [python, development, packaging, coordination]
guard: tests/test_development_environment.py
normative: devtools/conda-envs/README.md
blocked_by: []
supersedes: []
---

# Centralize a Python 3.14 development environment for MolSysSuite

**Reported:** 2026-09-26, after a host-local Python 3.14 development environment
was assembled for MolSysMT and MolSysViewer.
**Status:** Resolved on 2026-10-01 with the maintainer-approved scope of the
eight-member eligible Linux development base, verified by fresh hosted creation
and editable/runtime checks. The six-member Python 3.14 migration remains open
in uibcdf/molsyssuite#51.

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

The clean hosted development probe is now implemented and passing. It detects
recipe, source-metadata, dependency and basic runtime drift. Broader scientific
and viewer behavior stays with component qualification; newly eligible members
join through the registered transition. `uibcdf/molsyssuite#51` tracks the six members
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

**Not established:** Tests for all optional integrations or every registered
component. Independent clean Linux creation is now established by the hosted
run below; it is not a full scientific or GUI-rendering certificate.
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
their owning repositories. The central Qt lane is an official conda-forge
solution installed and checked on both the developer host and a fresh hosted
Linux runner; package release and native-platform gates
remain separate.

## Acceptance criteria

2026-10-01 administrative delivery: the reusable environment profile derives the
eight eligible editables from the registered transition and distinguishes six
publicly admitted tools/support libraries from the authorized MolSysMT/Viewer
pair. It rejects hidden channels, historical Qt forks and incompatible source
metadata. The new Linux workflow creates an uncached environment, installs the
eligible cohort without changing the Conda solution, runs `pip check`, verifies
editable import origins and loads the official Qt/WebEngine libraries. It retains
source and Conda receipts even on failure. Hosted execution now passed as detailed
below; it does not claim full scientific or GUI qualification.

- The recipe creates the named environment from a fresh checkout on Linux-64, without
  relying on undocumented machine-specific paths.
- Each eligible component installs in editable mode with `pip check` and verified
  source imports; representative component tests remain dated local evidence.
  Newly eligible members join the maintained set through the registered transition.
- All eight currently eligible Python components are included. The six remaining
  migrations are tracked in uibcdf/molsyssuite#51 under uibcdf/molsyssuite#29;
  incompatible metadata is rejected rather than overridden or implicitly exempted.
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


## Fresh hosted verification (2026-10-01)

Native run [36925121745](https://github.com/uibcdf/molsyssuite/actions/runs/36925121745)
passed at environment/tool/workflow source
`b1b8486f3b6de88de31c52305e4806a41dde69fc`. Every named creation, editable-install,
`pip check`, runtime-origin/Qt and evidence-retention step executed successfully.
The environment was created without an environment or download cache on a fresh
GitHub Linux runner, independently of the original developer host.

Downloaded artifact `linux-py314-development-36925121745-1` contains `profile.json`,
`source-inventory.json`, `editable-inventory.json`, `runtime.json` and
`conda-packages.json`. Their cohort and source SHA maps agree. All eight source
checkouts were clean before and after editable builds. The loaded interpreter
is Python 3.14.7; `pyside6`, `qt6-main`, `qt6-webengine` and `qt6-positioning` are
6.11.2 from public conda-forge Linux-64 URLs, without the historical UIBCDF forks.
The package imports originate in the selected editables, and distribution metadata
records editable installation.

| Editable member | Checked source SHA | Source version observed |
| --- | --- | --- |
| uibcdf/pytest-receptor | `ab3b7791d2826d1916c83be3debad663f9c17958` | `1.2.0+22.gab3b779` |
| uibcdf/gh-run-receptor | `c4b76db4d68c90d966e7161fbc075b9ac5d52de2` | `1.1.1+48.gc4b76db` |
| uibcdf/smonitor | `6a98d1e550859fb58dc3eb72ac3cb001dea421e5` | `0.18.0+21.g6a98d1e` |
| uibcdf/depdigest | `e323d412f3333b6a977248184a65e81a08c6c241` | `0.12.0+11.ge323d41` |
| uibcdf/argdigest | `43385bb662b5ce06e5266c6e330f82891f094284` | `0.13.0+52.g43385bb` |
| uibcdf/pyunitwizard | `7278ad466f3eec7abff8490b4365080d0816497c` | `0.27.0+34.g7278ad4` |
| uibcdf/molsysmt | `be76a2b6193c4ed9f72a40c8e17de01011508a4f` | `0.22.4+57.gbe76a2b6` |
| uibcdf/molsysviewer | `015b8884cbecf082492922cc6f0433f751d1f86a` | `0.23.4+67.g015b888` |

Six support/tool members are publicly admitted; the MolSysMT/Viewer pair is
source-authorized. This fresh development proof does not grant public admission,
a full scientific pass, Qt visible-window/rendering qualification or new release
approval. Previously reported focused component tests remain dated local evidence;
they were not rerun by this environment probe. Offline administration passed 261
tests; Ruff and the new workflow's actionlint checks passed.

## Accepted closure scope (2026-10-01)

The maintainer approved closing uibcdf/molsyssuite#52 as the reproducible
eight-member eligible Linux base. This accepted scope replaces the earlier local
checklist requiring every registered member or a bounded exception. The delivered
environment is usable now; component migration and admission retain their own
owners rather than blocking the environment's closure.

uibcdf/molsyssuite#51 remains open for Ackredit, DockingMT, ElastNetMT, LindeLint,
PharmacophoreMT and TopoMT. uibcdf/molsyssuite#29 continues to own phased admission.
Closing this environment proposal grants no metadata override, exception, public
Python 3.14 admission or scientific qualification. The profile derives its cohort
from the registered transition so newly eligible members join its checks.

The durable guard is `tests/test_development_environment.py`, a locally runnable
module whose five tests collectively protect the environment contract: eligibility
and admission distinctions, rejection of incompatible source metadata and hidden
channels/forks, coherent official Qt pins, and installation flags with propagated
failures. These assertions exercise mechanisms that could otherwise make the
shared profile misleading or unreproducible. The hosted workflow complements this
offline guard with fresh channel resolution, actual installation and runtime
evidence; its successful run is recorded above.
