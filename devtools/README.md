# MolSysSuite Development Tools

This directory contains the tools and configurations for managing the MolSysSuite environments and distributing the suite via Conda meta-packages.

## Authenticated hosted member audits

The five central member audits use the Actions secret
`SUITE_REPOSITORIES_READ_TOKEN` when a registered member is private. Its
fine-grained PAT must select that repository under `uibcdf`, grant only
Contents/Issues read, and retain a maintainer-owned expiration/renewal date.
Secret presence does not prove its permissions or successful audits.

`devtools/scripts/repository_read_access.py` provides independently usable
ephemeral HTTPS Git authentication (`--git-credentials`) and bounded command
output (`--private-output`). For example:

```bash
python devtools/scripts/repository_read_access.py --git-credentials --private-output -- \
  git clone --depth=1 https://github.com/uibcdf/opencastp.git /tmp/owned-source
```

Supply the token through the environment, never arguments or a remote URL.
The helper accepts only registered GitHub HTTPS paths and never stores a
credential. Authentication is confined to source acquisition; installation
and import steps do not receive this secret. Without a token, private
acquisition fails rather than omitting the member or reporting success.

With `--private-output`, child stdout/stderr and exception details are
discarded. `--receipt PATH` records actual status and exit code;
`--source-inventory PATH` adds only registered identities and validated
immutable commits after successful acquisition. No private source, metadata,
labels, traceback or raw development receipt is uploaded. Private failures
require maintainer diagnosis in an authorized private session; suppression
never changes the result.

Authenticated jobs run only from trusted `main` on push, schedule or manual
dispatch. PRs retain offline label/profile regression checks and explicitly
lack cross-repository/private integration evidence. They receive neither
the PAT nor private sources; no `pull_request_target` route is introduced.
Offline success does not certify joint editable/import integration.
After public visibility returns, inspect the audits before retiring the PAT.

Ownership and historical access failures: `uibcdf/molsyssuite#102`.
Joint environment compatibility: `uibcdf/molsyssuite#82`. These are local
central audit operations, not a credential requirement for component repos.

## 1. Directory Structure

*   `conda-envs/`: YAML files to create local Conda environments manually.
*   `conda-build/`: Conda-build recipes for the official meta-packages.
*   `scripts/`: Independently usable coordination and development operators.

---

## Optional joint installation

Two dependency-only Conda bundles are being prepared under
`uibcdf/molsyssuite#67`. The first `molsyssuite` bundle selects MolSysMT and MolSysViewer;
`molsyssuite-dev` derives a build/test dependency base from the maintained Linux
Python 3.14 environment. They are optional conveniences. Individual component
and tool installation/use remains available through each owner's instructions.
Registration does not automatically add a component to either bundle.
Their own package recipes supply transitive dependencies; the runtime bundle
adds no separate support-library or JupyterLab selection.

There is no qualified first bundle release. The recipes contain no selected
version, executable payload or clone installer. See
[recipe preparation and release conditions](conda-build/README.md).
The first-package version, dependency constraints and validation matrix will be
reviewed once both MolSysMT and MolSysViewer reach version 1.0.

## Development with local clones

The current usable joint route is the
[Python 3.14 environment and editable-install guide](conda-envs/README.md),
governed by [the workspace contract](../devguide/development_workspace.md).
Create its named environment deliberately, then inspect sources and connect
eligible clones with the maintained `development_environment.py` operator.
The retained Python 3.12 YAML and fixed six-clone helper are historical inputs.

For one component, provision its compatible dependencies using its own guidance,
then install only that local clone with the chosen interpreter:

```bash
python -m pip install --no-deps --editable /absolute/path/to/local-clone
python -m pip check
```

Verify Python 3.14 and import origins before local development/tests. Native
components may also require their documented build tools and
`--no-build-isolation`. No central metapackage or all-clone install is required.

## Publication automation

Recipe changes do not publish packages. The publisher uses an exact candidate
and reviewed per-package plan: explicit manual builds go to staging; an eligible
direct public build requires a package release and successful exact-source
gates. Governance `policy-v*` releases do not publish packages. Missing plans
currently block both routes before a build or registry mutation.
