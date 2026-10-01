# __COMPONENT_NAME__

__DESCRIPTION__.

This repository is a MolSysSuite component owned by the UIBCDF team. Read
[`MOLSYSSUITE_GUIDE.md`](MOLSYSSUITE_GUIDE.md) and [`AGENTS.md`](AGENTS.md) before
contributing.

## Development

Use Python __DEV_VERSION__ for routine development. Supported user versions: __CI_VERSIONS__.
The official public installation route is the `uibcdf` Conda channel once this
component has published and verified a package. This checkout is for development;
it makes no public package claim.

```bash
conda env create -n __PACKAGE_NAME__-dev -f devtools/conda-envs/development_env.yaml
conda activate __PACKAGE_NAME__-dev
python -m pip install --no-deps --editable .
ruff check .
ruff format --check .
python -m pytest --receptor=llm
python devtools/devguide_index.py --check
```

When adding an optional engine or service, complete
[`devguide/optional_engine_review.md`](devguide/optional_engine_review.md) and follow
the shared contract linked there. Runtime libraries are added only for implemented
boundaries, with verified provider versions and component-owned evidence.

Before a first Conda release, classify the artifact and apply the
[shared noarch route](https://github.com/uibcdf/molsyssuite/blob/main/devguide/noarch_conda_workflow.md)
when eligible. Pin its reusable workflows, commit the reviewed release plan and
resource inventory, and qualify the installed file before public promotion.
A reviewed tested equivalent or bounded exception covers special conditions.

Assess coverage applicability and record missing reporting in an owning issue.
Once a meaningful default-branch report and actual upload are verified, add its
live Codecov percentage between tests and documentation. Explain report scope
and cadence: it reflects the last uploaded report and may lag later direct/skip
commits. Follow the
[shared coverage contract](https://github.com/uibcdf/molsyssuite/blob/main/devguide/repository_badges.md#coverage-percentage-applicability-and-cadence).
