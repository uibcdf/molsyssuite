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

When an incident reveals a reusable development rule, put an accepted
repository-wide rule in this root `AGENTS.md` and a directory-specific rule in
the appropriate nested `AGENTS.md` in the same change. If adoption must wait,
open an owned follow-up issue. Report a potentially shared member rule to
`uibcdf/molsyssuite`, with the local evidence and affected members; raise a
cross-MOLI contract in `uibcdf/moli`. For work under `devguide/`, also read
`devguide/AGENTS.md`. Do not use an instruction in place of a test or technical
contract.

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
