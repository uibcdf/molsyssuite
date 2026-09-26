# Python quality-tooling policy

## Ownership

MolSysSuite owns the Python quality baseline for its registered members. `suite.toml` supplies the machine-readable values; this document defines their use and exceptions.

This document is normative for repositories carrying the `python-package` capability in
`suite.toml`. Accepted by `uibcdf/molsyssuite#4`.

## Suite quality baseline and member configuration

The suite requires Ruff `0.16.5` for formatting and linting, pytest for tests, Ruff target `py311`, and lint families `E4`, `E7`, `E9`, `F`, and `I`. Each member configures its own `pyproject.toml` for its source layout, generated files and notebooks, and may add stricter rules. After migration, members remove Black, isort and flake8 from active gates.

Root integration guides synchronized from another repository are read-only. Members list their exact paths in Ruff `extend-exclude`; [the vendored-guide policy](vendored_guides.md) checks exclusions and byte drift.

## Type checking and runtime validation

Static type checking remains a member decision unless MolSysSuite changes the shared gate.

The [suite ecosystem policy](python_ecosystem_policy.md) owns applicability of
runtime support libraries and records member adoption separately from Ruff
and static type checking.

## Version management

The suite registry names the tested Ruff version. MolSysSuite's versioned
conformance workflow installs it. Member development environments use that version or
a compatible newer version producing the same required result. Ruff upgrades are
decided and released by MolSysSuite.

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
