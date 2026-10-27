# __COMPONENT_NAME__ contributor instructions

__SUITE_INSTRUCTIONS__

## Local development commands

The generated `devtools/conda-envs/` files are CI/bootstrap and clean
qualification fixtures. Shared-development eligibility and actual import/closure
receiving are recorded centrally; use the named shared environment when eligible.

Select the applicable commands and test scope for the change:

```bash
ruff check .
ruff format --check .
python -m pytest --receptor=llm
python devtools/devguide_index.py --check
```

The issue-backed lifecycle is mapped to this repository in
`devguide/reporting_protocol.md`. Add only accepted repository-specific actions
here, such as scientific contracts, source layouts, specialized gates and local
commands. Keep technical findings in issues, tests and maintained documentation.
