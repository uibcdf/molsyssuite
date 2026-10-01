# New component starter kit

This guide defines how a new MolSysSuite component begins as a suite member instead of
acquiring shared conventions later. The executable template lives under
`devtools/templates/python_component/` and is instantiated by
`devtools/scripts/bootstrap_component.py`.

The generated component-facing guide carries the prospective macOS Apple Silicon
boundary. New components must not add Intel macOS runners or publication targets,
or claim arm64 compatibility without their own installed/runtime evidence. Use
the [shared support policy](python_ci_policy.md#platforms-and-experimental-versions).

## Admission before generation

Start with a central proposal describing the component's purpose, owner, relationship to
existing members, role, membership, maturity, development mode and required capabilities.
Add the accepted component to
`suite.toml` before generating its repository. Registration makes applicability explicit
and lets the central conformance checker distinguish a member from an unrelated project.

Do not use the kit to create a second implementation of a capability already owned by a
member without first resolving ownership in the proposal.

## Generate the repository

From a MolSysSuite checkout, run:

```bash
python devtools/scripts/bootstrap_component.py ../newcomponent \
  --repository uibcdf/newcomponent \
  --description "One sentence describing the component"
```

The command refuses unregistered repositories and non-empty destinations. It derives a
valid import name from the registered component name unless `--package` is supplied.

The generated baseline contains:

- package metadata, Git-derived release parsing and Ruff settings generated from the
  [MolSysSuite member policies](README.md) and values in `suite.toml`;
- routine and full Python CI lanes generated from the MolSysSuite Python baseline,
  using committed Conda test and development environments with the `uibcdf` and
  `conda-forge` channels, plus independent Ruff format and lint gates and the exact
  published `pytest-receptor==1.1.0` tool pin;
- the canonical `MOLSYSSUITE_GUIDE.md` and an `AGENTS.md` that requires it and
  explicitly routes modular reusable tool design to its canonical section;
- a scoped `devguide/AGENTS.md` that points to the root instructions and the
  local reporting protocol, distinguishes active queues from archive/history,
  and is present in the generated repository from its first commit;
- an explicit Ruff exclusion for that synchronized guide, leaving canonical and local
  documentation under the repository's own formatter;
- pending bug and proposal queues, a permanent archive, report template, generated
  indexes and an offline lifecycle validator;
- a `src/` package, import smoke test, README and Git ignore baseline.

The generated `devguide/optional_engine_review.md` worksheet links the
[optional engine integration contract](optional_engine_integration.md). Use it
when introducing an optional library, executable, service or saved-result adapter.
It records route-specific requirements, result boundaries, evidence and bounded
exceptions without installing unused engines or imposing a component layout.

This is a minimum for a component with no required runtime dependencies. When adding
one, keep `project.dependencies`, the Conda test and development environments, and
the future recipe's run requirements aligned. Verify an installed import on every
claimed Python lane. A temporary full-commit source install for an unpublished
sibling can support tests but cannot establish a public installation route. Follow
the inherited [distribution contract](python_distribution_policy.md) and the
suite's [CI dependency resolution](ci_dependency_resolution.md) rule. Scientific
validation, documentation and UI tests are added according to the component's risks.

## First-commit checklist

1. Run `python devtools/devguide_index.py --check` and
   `python -m pytest --receptor=llm` in the inherited routine Python version.
2. Run `ruff check .` and `ruff format --check .`.
3. From MolSysSuite, run `python devtools/scripts/check_repository.py <path>
   --repository uibcdf/<repository>`.
   Repeat this check whenever `project.dependencies` changes.
4. Replace the generated README description with a concrete purpose and initial public
   boundary; document any intentional policy exception with an issue and expiry.
5. Create the remote repository, protect `main` and enable the CI workflow. Stagger the
   generated cron minute, confirm the routine push/PR gate, manually dispatch the
   full matrix and confirm every supported minor passes before counting its schedule
   as evidence. Follow the [Python CI lane policy](python_ci_policy.md) thereafter.
6. Before public distribution, add `devtools/conda-build/` with a recipe whose run
   dependencies match `pyproject.toml`, and a reviewed workflow invoking
   a reviewed pinned `uibcdf/action-build-and-upload-conda-packages`. Follow the
   [Conda publication contract](conda_publication_policy.md): classify the artifact
   profile, commit the pre-tag route plan and adopt the lightweight publication
   guard plus common independent verifier (or a documented tested equivalent).
   Build and test the exact candidate;
   verify clean installation from the public channel before adding user installation
   claims. The channel credential belongs in CI secrets, never this repository; access
   guidance is tracked in MOLI #8.
7. Confirm that the initial public version and tag satisfy the MolSysSuite release
   policy; use staging for candidate evidence. Record this member's distribution
   review in `suite.toml` and its issue.
8. Add any coordinated rollout or compatibility work to its owning central issue.
9. When optional-engine boundaries exist, complete the generated review worksheet
   or a documented local equivalent and link the member ecosystem review. Separate
   absence guards, installed-engine evidence and live service checks. Verify the
   required provider release before claiming a public installation route.

10. Inspect existing tools before adding capabilities. Apply the
    [modular reusable tools policy](modular_reusable_tools.md), identify the owner
    and supported contract, and verify the consumer actually calls the reusable tool.
    Record any temporary implementation exception with ownership and expiry.
11. Check that root `AGENTS.md` distinguishes technical findings (owning
    issues, fixes, tests and documentation) from lasting instructions about
    how agents or contributors work; `devguide/AGENTS.md` must be present and
    point to the reporting route. A new member must have these files at
    creation, rather than waiting for a later member rollout (MolSysSuite #66).
    Generation uses the same [working-instruction route checker](working_instructions_policy.md)
    as the member-guide audit; comments and examples cannot satisfy active routes.

## Ongoing maintenance

The generated copies follow the policies named in `suite.toml`; the central policy is
the source of truth. Synchronize `MOLSYSSUITE_GUIDE.md` centrally, update the kit when a
new universal requirement is accepted, and test generation as part of central
governance validation. Existing components are not automatically rewritten when the kit
changes: their conformance is managed through explicit rollouts.

## First Conda publication

The generated checkout makes no public package claim. Classify the actual
artifact before its first Conda release. Eligible Python code and resources use
the [shared noarch workflow](noarch_conda_workflow.md) with pinned callers, reviewed
candidate plan, resource inventory and component installed gate. A tested
equivalent or bounded policy exception covers special build conditions. Do not
copy an arbitrary publisher or infer platform support from noarch.
