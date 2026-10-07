# __COMPONENT_NAME__ contributor instructions

Read `MOLSYSSUITE_GUIDE.md` before making changes. It routes suite-wide policy,
compatibility, tooling and cross-component proposals to `uibcdf/molsyssuite` while this
repository remains authoritative for its implementation and product behavior.

Use English in code, documentation, issues and commits. Keep changes focused, test
user-visible behavior, preserve human work and never commit secrets.

Routine development and pytest use Python 3.14 in a compatible Conda environment.
Install the local clone with `python -m pip install --no-deps --editable .` after
Conda supplies dependencies; verify interpreter, dependency closure and import
origins. Use the suite's named Linux development profile when this member is
eligible; otherwise track the missing integration as the canonical guide directs.
Native builds may need declared in-environment tools and `--no-build-isolation`.

Choose local gates before committing from the changed code, inputs and scope:

- For documentation, instructions or evidence, run applicable reporting/index,
  link and synchronized-guide checks. Run `python devtools/devguide_index.py
  --check` for developer-guide changes; do not require scientific pytest merely
  because prose changed.
- For executable behavior, dependencies, metadata, packaging or integration,
  run relevant code/contract tests and applicable Ruff checks. Broaden to the
  full suite when the affected boundary, PR, admission or release requires it.
- For scientific exploration, run informative hypothesis cases and record
  their limits; do not infer broader equivalence from an administrative CI run.

Available commands (select the applicable checks and test scope):

```bash
ruff check .
ruff format --check .
python -m pytest --receptor=llm
python devtools/devguide_index.py --check
```

Retain completed local results while tested code, inputs, environment and scope
remain applicable; rerun or broaden when changes or failures invalidate them.
Follow [the common checkpoint route](MOLSYSSUITE_GUIDE.md#direct-pushes-and-validation-checkpoints)
for conditional internal batching/skips, exact-head CI verification and visible
recovery debt. Full PR and release gates remain mandatory.

Follow `devguide/reporting_protocol.md` for every durable bug or proposal record. Open
the owning GitHub issue first, regenerate indexes after lifecycle changes, and archive
resolved records instead of deleting them.

Before publishing or rolling out a shared provider change with plausible consumer
impact, follow
[the shared-provider notice rule](MOLSYSSUITE_GUIDE.md#shared-stewardship-across-components):
update the impact issue, identify consumers from registered inventories and send an
actionable handoff to their owning issues. Keep notice, adoption and tested artifact
evidence separate.

For a fix in another owner's repository, follow the canonical guide's
cross-repository contribution route: issue for a need, owner-reviewed PR for a
proposed fix, or an explicitly authorized route for urgent work by or directly
with Diego or Liliana. Existing authorization remains valid within its scope.

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

## Temporary development resources

Follow [the common resource policy](MOLSYSSUITE_GUIDE.md#temporary-development-resources).
Keep ownership clear, retain temporary resources and evidence while needed,
and remove them when their usefulness ends. Review retention at task/release
closeout; preserve active/human work and report cleanup failures.

## Durable working instructions

Follow [the canonical instruction policy](MOLSYSSUITE_GUIDE.md#durable-working-instructions)
when placing accepted lasting contributor actions. Keep technical findings in
owning issues, tests and maintained guidance. For work in `devguide/`, read
[devguide/AGENTS.md](devguide/AGENTS.md) and its local reporting protocol.
