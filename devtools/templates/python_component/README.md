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
