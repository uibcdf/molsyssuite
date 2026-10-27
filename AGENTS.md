# MolSysSuite coordination

## Mandatory MolSysSuite instructions

Read and follow `MOLSYSSUITE_GUIDE.md` before working in this repository.

Within their stated scope, its common rules take precedence over this file
and any nested `AGENTS.md`. Local instructions may refine them; deviations
require the documented policy exception process.

The synchronized guide is owned by `uibcdf/molsyssuite`. It includes the
[reusable-tool ownership rules](MOLSYSSUITE_GUIDE.md#modular-reusable-tools)
and [working-instruction rules](MOLSYSSUITE_GUIDE.md#durable-working-instructions).
For work under `devguide/`, also read `devguide/AGENTS.md` and its local
reporting protocol. Keep repository-specific instructions below.

## Central ownership and commands

MolSysSuite owns policies/contracts shared by members and the official member
registry, starter and canonical guide inventories in `suite.toml`. Component-only
implementation stays with its owner. Before coordinated work run
`python devtools/scripts/suite_status.py`; preserve primary human/dirty work.

Read `devguide/reporting_protocol.md` and `devguide/AGENTS.md` before changing
issue-backed records. Use `devguide/templates/report.md`, regenerate indexes and
run the offline governance guard before committing:

```bash
python devtools/scripts/devguide_index.py
python devtools/scripts/validate_governance.py
```

Common-guide changes are made here. Distribute registered canonical sources
only with `devtools/scripts/sync_vendored_guides.py`; keep notices, delivered
commits and executed/public-artifact evidence separate. The maintained
`devguide/CHECKPOINT.md` routes current coordination and explicitly deferred work.
For routine Python work use the named shared environment and participating
no-deps editables under `devguide/development_workspace.md`; central commands
are administrative checks and do not qualify member scientific behavior.
