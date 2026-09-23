# Python quality-tooling policy

## MOLI ownership note

This document is the **MolSysSuite tooling profile** for the MOLI Python quality baseline. The platform owner is `uibcdf/moli` (`devguide/policies/python_tooling_policy.md`). MolSysSuite retains suite-specific policy-release pins, synchronized-guide exclusions, migration sequencing, and conformance tooling.

This document is normative for repositories carrying the `python-package` capability in
`suite.toml`. Accepted by `uibcdf/molsyssuite#4`.

## Inherited quality baseline and member configuration

MOLI owns the shared formatter, linter, test runner, Ruff version, target version and required lint rules in [its pinned Python tooling policy](https://github.com/uibcdf/moli/blob/888902eb2ccc482c62c6f75da9d8f0bf9bb56442/devguide/policies/python_tooling_policy.md) and pinned `moli.toml`. Each member configures its own `pyproject.toml` for its source layout, generated files and notebooks, and may add stricter rules. After migration, members remove Black, isort and flake8 from active gates.

Root integration guides synchronized from another repository are read-only. Members list their exact paths in Ruff `extend-exclude`; [the vendored-guide policy](vendored_guides.md) checks exclusions and byte drift.

## Type checking and runtime validation

Static type checking remains a member decision unless MOLI changes the shared gate.

The [effective MOLI support-library policy](https://github.com/uibcdf/moli/blob/888902eb2ccc482c62c6f75da9d8f0bf9bb56442/devguide/policies/python_support_libraries_policy.md)
owns applicability of runtime support libraries. The [suite ecosystem review
profile](python_ecosystem_policy.md) records member adoption separately from Ruff
and static type checking.

## Version management

The pinned MOLI registry names the tested Ruff version. MolSysSuite's versioned
conformance workflow installs it. Member development environments use that version or
a compatible newer version producing the same required result. Ruff upgrades are
decided in MOLI and then adopted by MolSysSuite.

## Migration safety

A member migrates in this order:

1. add Ruff and the shared baseline;
2. run formatting and lint fixes as an isolated mechanical change;
3. run the repository's complete tests on its development environment;
4. replace CI commands;
5. remove Black, isort and flake8;
6. record any local extension or exception.

The old tools are not removed before the equivalent Ruff gates are green.

## Exceptions

An exception names its repository, rule, reason, tracking issue and expiration condition.
Local suppressions for individual lines follow normal repository practice and do not need
central tracking unless they disable a shared rule across a package or directory.
