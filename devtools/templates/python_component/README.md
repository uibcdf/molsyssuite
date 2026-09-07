# __COMPONENT_NAME__

__DESCRIPTION__.

This repository is a MolSysSuite component owned by the UIBCDF team. Read
[`MOLSYSSUITE_GUIDE.md`](MOLSYSSUITE_GUIDE.md) and [`AGENTS.md`](AGENTS.md) before
contributing.

## Development

Use Python 3.13 for routine development. The supported user range is Python 3.11–3.13.

```bash
python -m pip install -e '.[test]'
ruff check .
ruff format --check .
pytest
python devtools/devguide_index.py --check
```
