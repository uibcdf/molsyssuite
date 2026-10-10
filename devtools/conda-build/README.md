# Optional central dependency bundles

MolSysSuite owns this local product preparation under `uibcdf/molsyssuite#67`.
The accepted model offers joint installation for users and developers while
preserving individual component/tool installation, use and instructions.
Neither bundle is a prerequisite for accessing a tool, developing one component,
or participating in the suite.

| Bundle | Prepared scope | Separate operations |
| --- | --- | --- |
| `molsyssuite` | MolSysMT and MolSysViewer, plus their declared transitive dependencies | Component ownership, releases and scientific qualification |
| `molsyssuite-dev` | Current `molsyssuite-dev-py314.yaml` dependency base | Individual or cohort editable installs, native builds, scientific/GUI tests and additional component-specific/docs tools |

The developer bundle contains some public support libraries already present in
that base. It does not install the runtime bundle, MolSysMT/Viewer distributions,
or source clones. Tools retain their owning packages/repositories and independent
entry points. The legacy `molsys-dev-setup` helper remains in source history and
is not included in these metadata-only recipes. Use
[`development_environment.py`](../scripts/development_environment.py) for the
qualified cohort, or `python -m pip install --no-deps --editable PATH` for an
individual clone after provisioning its compatible dependency closure.

For the first runtime bundle, only MolSysMT and MolSysViewer are selected
directly alongside the Python bounds. Their own Conda recipes govern support
libraries and other transitive requirements. JupyterLab is not a separate
runtime-bundle requirement. Further additions require an explicit scope review;
they do not follow automatically from membership or from being a dependency.

## Independently usable preparation operation

`central_metapackages.py` is the central local adapter. It reuses the shared
Conda plan validator, sandboxed template parser and maintained development
profile validator; it does not weaken the Python-artifact adapters. Its contract:

- Require a committed, valid `release_plan.toml` beside the selected template,
  matching its package and the explicit version. No version/build default.
- Require profile `metapackage` and executed job/step requirements for every
  declared native workflow. Actual gate acquisition remains the subsequent
  shared preflight operation.
- Accept only metadata-only `noarch: generic`, explicit `meta_<build>` identity,
  plain unique public Conda dependency specs and reviewed brief recipe tests.
  Reject sources, output packages, host/build requirements, build scripts,
  entry points, platform selectors and dependencies coupling the two bundles.
- Derive developer requirements from the maintained environment instead of
  maintaining a second list. Its preparation scope is currently Linux/Python
  3.14. Runtime Python bounds are 3.11–3.14; no supported installed matrix is
  established merely by those bounds or by noarch metadata.
- Write just `meta.yaml` to a new task-owned directory. Refuse an existing
  destination, preserve caller resources, and return the exact expected filename.
  Retain the output while building; the caller owns its cleanup and receipts.
  Failed writes remove only the newly created directory; cleanup errors are
  reported. The hosted caller removes the recipe after receipt retention,
  including after a failed build/preflight.

After selecting and reviewing an actual release plan, run:

```bash
python devtools/scripts/central_metapackages.py \
  --package molsyssuite --version X.Y.Z \
  --output-directory /tmp/task-owned-runtime-recipe
```

`X.Y.Z` is a placeholder. **No active plans or chosen release versions exist
yet**, so the command currently fails before creating its output. The recipe
templates are inputs to this operation, not standalone build directories.
`--github-output PATH` writes `directory` and `filename` for the local caller.
`prepare_recipe(root, package, version)` performs the same validation without
writing files, connecting clones, installing dependencies or contacting services.
Regression guards are in `tests/test_central_metapackages.py`.

## Remaining release work

The local publisher uses Python 3.14, the generated recipe and its exact
`meta_<build>` filename. It keeps the existing action pins, explicit staging,
exact-source native preflight, producer receipts and independent public verifier.
This preparation creates no selected candidate or publication authorization.

Review concrete version/build, dependency constraints, capability checks and
claimed platform/Python cells before committing active plans. For the first
changed profile, use staging and retain each original artifact's source/build
and SHA-256. Implement and execute clean installed qualification for every
claimed cell before authorizing promotion of those same bytes; independently
verify the public label and solver index afterward. The missing installed
qualification/promotion caller remains tracked in #67. Never infer its success
from these unit tests, an editable workspace, a solver-only result or brief
Linux recipe tests. Metapackages do not inherit component scientific suites.

The central publication exception remains active until those gates are complete.
