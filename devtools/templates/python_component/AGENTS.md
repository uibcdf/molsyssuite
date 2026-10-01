# __COMPONENT_NAME__ contributor instructions

Read `MOLSYSSUITE_GUIDE.md` before making changes. It routes suite-wide policy,
compatibility, tooling and cross-component proposals to `uibcdf/molsyssuite` while this
repository remains authoritative for its implementation and product behavior.

Use English in code, documentation, issues and commits. Keep changes focused, test
user-visible behavior, preserve human work and never commit secrets.

Run these local gates before committing:

```bash
ruff check .
ruff format --check .
python -m pytest --receptor=llm
python devtools/devguide_index.py --check
```

Follow `devguide/reporting_protocol.md` for every durable bug or proposal record. Open
the owning GitHub issue first, regenerate indexes after lifecycle changes, and archive
resolved records instead of deleting them.

Report defects and needs in their owning issues; put source behavior, edge
cases and workarounds in code, regression tests and technical documentation,
not in `AGENTS.md`. Only when normal repository review accepts a lasting rule
about how contributors or agents should work across future tasks, place a
repository-wide working instruction here or a directory-specific one in the
appropriate nested `AGENTS.md`. Open an adoption issue only if that accepted
instruction cannot be placed with the fix or decision. Do not ask for a
separate `AGENTS.md` decision for every defect. Propose a shared member
working instruction to `uibcdf/molsyssuite` only with evidence beyond this
repository; raise a cross-MOLI contract in `uibcdf/moli`. For work under
`devguide/`, also read `devguide/AGENTS.md`.

Before adding a required MolSysSuite sibling to `project.dependencies`, consult
`uibcdf/molsyssuite/devguide/ci_dependency_resolution.md` and replace the generated
pip-only CI lane with a verified dependency acquisition route.

## Modular reusable tools

Before adding a feature, inspect existing tools and identify the owning module or
component. Implement or extend independently useful operations as documented reusable
tools in that owner, with their own contracts and tests; have consumers call them.
Keep task-specific decisions local and report missing sibling capabilities to the
provider with linked consumer evidence. Follow
[MOLSYSSUITE_GUIDE.md#modular-reusable-tools](MOLSYSSUITE_GUIDE.md#modular-reusable-tools)
for applicability, compatibility, performance and tracked exceptions.

## Durable working instructions

Follow [the canonical instruction policy](MOLSYSSUITE_GUIDE.md#durable-working-instructions)
when placing accepted lasting contributor actions. Keep technical findings in
owning issues, tests and maintained guidance. For work in `devguide/`, read
[devguide/AGENTS.md](devguide/AGENTS.md) and its local reporting protocol.
