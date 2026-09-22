# CI acquisition of required suite dependencies

This document is normative for repositories carrying the `python-package` capability
in `suite.toml`. Accepted by `uibcdf/molsyssuite#31`.

## Required dependencies

When `project.dependencies` names another registered MolSysSuite component, the
repository must provide a CI route for acquiring that component before testing itself.
The generated pip-only starter lane is suitable only while its required dependencies
are available from its configured package index. MolSysSuite distributions are not
assumed to be on PyPI.

Two routes are accepted:

- A workflow uses `mamba-org/setup-micromamba` with a committed environment file under
  `devtools/conda-envs/`. The file and channel configuration must resolve the required
  sibling versions on every claimed Python lane. The repository owns its environment
  files and may use different ones for smoke, full matrix, documentation and release.
- A workflow installs each required sibling from a reviewed GitHub source pinned to a
  full commit SHA. It must still install the consumer and run its tests. A floating
  branch, unpinned URL or local editable sibling checkout is not release evidence.

The common checker reads `project.dependencies`, normalizes registered distribution
names, and reports `SIBLING_CI_ROUTE` when neither a referenced Conda environment file
nor full-SHA source routes exist. It is an offline structural check: it does not run the
Conda solver, verify package availability, prove that a source checkout installs, or
inspect optional extras. Hosted installation, import and test results provide that
evidence. CI failures caused by missing published builds must be addressed in the
consumer's environment or through a tracked, pinned source route; a green policy gate
alone does not claim dependency readiness.

This rule does not govern Conda release staging or promotion (`uibcdf/molsyssuite#27`)
or the dependency graph inventory (`uibcdf/molsyssuite#30`).
