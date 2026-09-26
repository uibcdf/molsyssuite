# New component starter kit

This guide defines how a new MolSysSuite component begins as a suite member instead of
acquiring shared conventions later. The executable template lives under
`devtools/templates/python_component/` and is instantiated by
`devtools/scripts/bootstrap_component.py`.

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
  pinned [MOLI engineering policies](https://github.com/uibcdf/moli/blob/15b38fbe17b6ee9fa9aac2a8e21b80d76a8da70f/devguide/governance/policy_inheritance.md);
- routine and full Python CI lanes generated from the inherited MOLI Python baseline,
  using committed Conda test and development environments with the `uibcdf` and
  `conda-forge` channels, plus independent Ruff format and lint gates and the exact
  published `pytest-receptor==1.1.0` tool pin;
- the canonical `MOLSYSSUITE_GUIDE.md` and an `AGENTS.md` that requires it;
- an explicit Ruff exclusion for that synchronized guide, leaving canonical and local
  documentation under the repository's own formatter;
- pending bug and proposal queues, a permanent archive, report template, generated
  indexes and an offline lifecycle validator;
- a `src/` package, import smoke test, README and Git ignore baseline.

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
   `uibcdf/action-build-and-upload-conda-packages`. Build and test the exact candidate;
   verify clean installation from the public channel before adding user installation
   claims. The channel credential belongs in CI secrets, never this repository; access
   guidance is tracked in MOLI #8.
7. Confirm that the initial public version and tag satisfy the inherited MOLI release
   policy; use staging for candidate evidence. Record this member's distribution
   review in `suite.toml` and its issue.
8. Add any coordinated rollout or compatibility work to its owning central issue.

## Ongoing maintenance

The generated copies follow the policies named in `suite.toml`; the central policy is
the source of truth. Synchronize `MOLSYSSUITE_GUIDE.md` centrally, update the kit when a
new universal requirement is accepted, and test generation as part of central
governance validation. Existing components are not automatically rewritten when the kit
changes: their conformance is managed through explicit rollouts.
