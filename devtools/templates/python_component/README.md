# __COMPONENT_NAME__

__DESCRIPTION__.

This repository is a MolSysSuite component owned by the UIBCDF team. Read
[`MOLSYSSUITE_GUIDE.md`](MOLSYSSUITE_GUIDE.md) and [`AGENTS.md`](AGENTS.md) before
contributing.

## Development

Use Python __DEV_VERSION__ for routine development. Supported user versions: __CI_VERSIONS__.

```bash
python -m pip install -e '.[test]'
ruff check .
ruff format --check .
pytest
python devtools/devguide_index.py --check
```
