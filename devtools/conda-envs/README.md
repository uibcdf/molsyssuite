# MolSysSuite development environments

The opt-in [Python 3.14 recipe](molsyssuite-dev-py314.yaml) creates a shared
development base for MolSysMT, MolSysViewer, and the MolSysSuite support and developer
tools that already admit Python 3.14. It is not an installed-package release gate or a
suite-wide support claim. The older `molsyssuite-dev.yaml` remains a separate Python
3.12 profile; `molsyssuite.yaml` is for published component packages, not editable
development.

From this repository, create the environment with Conda or Mamba:

```bash
conda env create --file devtools/conda-envs/molsyssuite-dev-py314.yaml
conda activate 'molsyssuite@3.14'
```

If your Conda installation has multiple environment directories, pass an explicit
`--prefix /absolute/path/to/envs/molsyssuite@3.14` to `conda env create` and activate
that same path. Mamba accepts the same environment file. The recipe uses only `uibcdf`
and `conda-forge`; it avoids the `matplotlib` metapackage because that can pull in
canonical PySide6 alongside the separately namespaced UIBCDF Qt family.
The YAML resolved in Linux-64 dry runs with Conda 26.5.3 and Mamba using cached channel
metadata on 2026-09-26; clean creation from this file and other platforms remain to be
tested.

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

## Optional UIBCDF Qt/PySide on Linux

The five aligned UIBCDF Qt/PySide 6.10.1 artifacts were validated locally with Python
3.14 on Linux, but are not available from the public `uibcdf` channel. Do not add them
to the portable YAML or silently replace them with canonical PySide6. If you have an
indexed local channel containing all five exact artifacts, install them separately:

```bash
QT_CHANNEL=/absolute/path/to/indexed/qt-py314/channel
test -f "$QT_CHANNEL/linux-64/repodata.json"
conda install --override-channels \
  -c "file://$QT_CHANNEL" -c uibcdf -c conda-forge \
  'qt6-main=6.10.1' 'shiboken6-uibcdf=6.10.1' \
  'pyside6-essentials-uibcdf=6.10.1' 'pyside6-addons-uibcdf=6.10.1' \
  'qt6-positioning-uibcdf=6.10.1' 'qt6-webengine-uibcdf=6.10.1'
```

This local lane is not portable to macOS or Windows. The coordinated Qt work belongs
to `uibcdf/molsysviewer#93` and the Qt package owners; publishing the family is a
separate decision, not a side effect of creating this environment.

## Current limits and maintenance

Ackredit, DockingMT, ElastNetMT, LindeLint, PharmacophoreMT, and TopoMT still exclude
Python 3.14 in their package metadata and are intentionally absent from the editable
command. Their migration is tracked by `uibcdf/molsyssuite#51`, under the phased
admission program `uibcdf/molsyssuite#29`. AmberTools and PyTraj are also absent from
this initial 3.14 recipe; optional integrations should not force older NumPy or
Biopython into the shared development base.

`uibcdf/molsyssuite#52` owns improvement of this recipe: clean creation on supported
development platforms, dependency and channel drift checks, a distributed Qt route,
and eventual coverage of every registered Python component or an explicit exception.
