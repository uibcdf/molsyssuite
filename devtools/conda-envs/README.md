# MolSysSuite development environments

The default [Python 3.14 recipe](molsyssuite-dev-py314.yaml) creates
`molsyssuite@uibcdf_3.14`, a Linux development base for MolSysMT, MolSysViewer, and
the MolSysSuite support and developer tools eligible for Python 3.14 development.
Use it for routine local work on those members. Members still blocked on 3.14
use a tracked temporary migration environment until their normal dependency
closure and tests work; see `uibcdf/molsyssuite#51`.
Six support/tool members are publicly admitted; MolSysMT and MolSysViewer are
authorized for the transition, which is distinct from public admission. The main
developers use Linux; macOS and Windows are not acceptance gates for this environment.
It is not an installed-package release gate or a suite-wide support claim. The older
`molsyssuite-dev.yaml` remains a separate Python
3.12 profile; `molsyssuite.yaml` is for published component packages, not editable
development.

From this repository, create the environment with Conda or Mamba:

```bash
conda env create --file devtools/conda-envs/molsyssuite-dev-py314.yaml
conda activate 'molsyssuite@uibcdf_3.14'
```

If your Conda installation has multiple environment directories, pass an explicit
`--prefix /absolute/path/to/envs/molsyssuite@uibcdf_3.14` to `conda env create` and activate
that same path. Mamba accepts the same environment file. The recipe uses only `uibcdf`
and `conda-forge`; its matching `pyside6`, `qt6-webengine`, and `qt6-positioning`
6.11.2 packages come from conda-forge. Do not install the retained UIBCDF
Qt/PySide family into the same environment.
The YAML resolved in Linux-64 dry runs with Conda 26.5.3 and Mamba using cached channel
metadata on 2026-09-26. On 2026-09-27, a fresh environment built from the
Qt-pinned recipe on this Linux host passed editable-install, dependency,
WebEngine transport, and MolSysMT–Viewer integration checks. The migrated
shared environment also passed Xvfb/SwiftShader render checks. The final
recipe, including two test dependencies discovered during validation, passed
an offline dry-run solve. On 2026-10-01, hosted run
[36925121745](https://github.com/uibcdf/molsyssuite/actions/runs/36925121745)
created the environment without caches on a fresh GitHub Linux runner: Python
3.14.7, all eight clean editable sources, successful `pip check`, verified import
origins and loaded official Qt/WebEngine 6.11.2. Its retained receipts name every
source SHA. This is development feasibility, not a full scientific/GUI or public
release qualification.

If an existing environment still contains the UIBCDF Qt/PySide family, do not
assume `conda env update` removes it: its package names are distinct from the
official ones. Prefer creating a fresh environment from this YAML. To migrate
an existing environment, remove the five UIBCDF packages deliberately, inspect
the solver transaction, then install the three pinned official packages and
rerun the runtime checks. Keep rollback artifacts in a separate environment.

The following commands assume this repository and its components are sibling
checkouts and that the new environment is active. Check each checkout's branch and
update it deliberately before installation; an editable install follows the working
tree, not a release tag. A working Rust/Cargo toolchain is needed to build MolSysMT's
native extension (`cargo --version` is a quick preflight).

```bash
python -m pip install --no-deps --no-build-isolation \
  -e ../smonitor -e ../depdigest -e ../argdigest -e ../pyunitwizard \
  -e ../pytest-receptor -e ../gh-run-receptor \
  -e ../molsysmt -e ../molsysviewer
python -m pip check
python -c 'import molsysmt, molsysviewer, mmcif; print(molsysmt.__version__, molsysviewer.__version__)'
```

`--no-deps` preserves the Conda solution; `--no-build-isolation` uses the declared
build tools in this environment. Run the version check from the MolSysSuite checkout
or another neutral directory: stale `*.egg-info` in a component root can shadow the
editable installation's version metadata. For relevant local tests, use
`pytest --receptor=llm -n 12` from the component checkout; graphical Qt tests need a
display or Xvfb. The full suite is not implied by these smoke checks.

## Qt/PySide route on Linux

The default development route is official PySide6/Qt 6.11.2 from conda-forge.
MolSysViewer selects this canonical binding when present. Validate the full
environment after any Qt change with `python -m pip check`, the Viewer
standalone-host tests, and a real WebEngine transport smoke. A solver result
alone does not establish that WebEngine resources work at runtime; see
`uibcdf/molsysviewer#109` and `uibcdf/molsyssuite#57`.

### Historical UIBCDF rollback lane

The five aligned UIBCDF Qt/PySide 6.10.1 artifacts were validated locally with Python
3.14 on Linux, but are not available from the public `uibcdf` channel. They
remain rollback assets, not a dependency of the portable YAML. Use a separate
environment with an indexed local channel; do not mix this lane with the
canonical packages:

```bash
QT_CHANNEL=/absolute/path/to/indexed/qt-py314/channel
test -f "$QT_CHANNEL/linux-64/repodata.json"
conda install --override-channels \
  -c "file://$QT_CHANNEL" -c uibcdf -c conda-forge \
  'qt6-main=6.10.1' 'shiboken6-uibcdf=6.10.1' \
  'pyside6-essentials-uibcdf=6.10.1' 'pyside6-addons-uibcdf=6.10.1' \
  'qt6-positioning-uibcdf=6.10.1' 'qt6-webengine-uibcdf=6.10.1'
```

The coordinated Qt work belongs to `uibcdf/molsysviewer#93` and the Qt package owners;
publishing the family is a separate decision, not a side effect of creating this Linux
development environment. The environment originally created on this host used
this five-package local lane; the canonical migration is tracked in
`uibcdf/molsyssuite#52`. Check the installed packages before assuming that a
particular host has completed the migration.

## Automated Linux development probe

`.github/workflows/check-development-environment.yaml` checks relevant changes,
runs weekly and accepts manual dispatch. It creates a fresh Linux-64 environment
from the public recipe without an environment/download cache, installs the complete
eligible cohort, runs `pip check`, verifies actual editable import origins, and
loads the official Qt/WebEngine libraries. It retains source SHAs, admission
states, exclusions and actual Conda package metadata even after failure. This
probe is not a full scientific suite, GUI-rendering certificate or release gate.

The reusable module is `devtools/scripts/development_environment.py`:

```bash
python devtools/scripts/development_environment.py profile
python devtools/scripts/development_environment.py sources --workspace /path/to/checkouts
# Inside the Python 3.14 environment:
python devtools/scripts/development_environment.py install --workspace /path/to/checkouts
python devtools/scripts/development_environment.py runtime --workspace /path/to/checkouts
```

`profile(registry, recipe)` validates public channels and the coherent Qt stack,
and derives eligibility from the registered transition. `source_inventory(plan,
workspace)` checks every selected source's Python metadata before installation;
missing/incompatible sources fail instead of being silently omitted.
`install_editables(sources)` preserves the Conda solution with `--no-deps` and
`--no-build-isolation` and propagates installation/dependency failures.
`verify_runtime(sources)` checks Linux/Python, official Qt provenance, editable
origins and actual runtime imports. `checkout_sources(plan, workspace)` is the
CI fresh-checkout operation; it refuses occupied member directories and fetches
tag history for version-derived metadata. Source receipts may show generated
version files after editable builds; they do not conceal dirty state.

The old six-repository `molsys_dev_setup.py` convenience script does not validate
this profile or the complete eligible cohort. Use the profile operations above
for this environment. A failed probe remains failed and belongs to #52 or the
component owning the exposed compatibility/dependency boundary; it is not a
reason to relax Python metadata or claim a green scientific matrix.

## Remaining component migrations

Members absent from the editable command still need source, dependency and
development-environment evidence before joining this shared recipe. Their
migration is tracked by `uibcdf/molsyssuite#51`, under the phased
admission program `uibcdf/molsyssuite#29`. AmberTools and PyTraj are also absent from
this initial 3.14 recipe; optional integrations should not force older NumPy or
Biopython into the shared development base.

`uibcdf/molsyssuite#52` owns the reproducible eligible Linux base and its automated
checks. It closed on 2026-10-01 with the maintainer-approved scope of the eight
eligible components, after the fresh hosted probe established independent creation
and basic editable/runtime closure. See the
[archived decision](../../devguide/archive/centralize_python_3_14_development_environment.md).
The six remaining migrations stay open in `uibcdf/molsyssuite#51`. Broader
scientific/GUI evidence and public admission retain their component owners.
