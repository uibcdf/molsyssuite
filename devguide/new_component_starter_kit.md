# New component starter kit

This guide defines how a new MolSysSuite component begins as a suite member instead of
acquiring shared conventions later. The executable template lives under
`devtools/templates/python_component/` and is instantiated by
`devtools/scripts/bootstrap_component.py`.

## Admission before generation

Start with a central proposal describing the component's purpose, owner, relationship to
existing members, maturity cohort and required profiles. Add the accepted component to
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

- package metadata for Python `>=3.11,<3.14` and development dependencies pinned to the
  suite Ruff policy release;
- Linux CI for Python 3.11, 3.12 and 3.13, plus independent Ruff format and lint gates;
- the canonical `MOLSYSSUITE_GUIDE.md` and an `AGENTS.md` that requires it;
- an explicit Ruff exclusion for that synchronized guide, leaving canonical and local
  documentation under the repository's own formatter;
- pending bug and proposal queues, a permanent archive, report template, generated
  indexes and an offline lifecycle validator;
- a `src/` package, import smoke test, README and Git ignore baseline.

This is a minimum, not a ceiling. Scientific validation, documentation, UI tests,
release automation and component-specific dependencies are added according to the
component's profile and risks.

## First-commit checklist

1. Run `python devtools/devguide_index.py --check` and `pytest` in Python 3.13.
2. Run `ruff check .` and `ruff format --check .`.
3. From MolSysSuite, run `python devtools/scripts/check_repository.py <path>
   --repository uibcdf/<repository>`.
4. Replace the generated README description with a concrete purpose and initial public
   boundary; document any intentional policy exception with an issue and expiry.
5. Create the remote repository, protect `main`, enable the CI workflow and confirm all
   three Python lanes pass.
6. Add any coordinated rollout or compatibility work to its owning central issue.

## Ongoing maintenance

The generated copies follow the policies named in `suite.toml`; the central policy is
the source of truth. Synchronize `MOLSYSSUITE_GUIDE.md` centrally, update the kit when a
new universal requirement is accepted, and test generation as part of central
governance validation. Existing components are not automatically rewritten when the kit
changes: their conformance is managed through explicit rollouts.
