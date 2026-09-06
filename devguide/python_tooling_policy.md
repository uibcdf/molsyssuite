# Python quality-tooling policy

This document is normative for repositories carrying the `python-library` profile in
`suite.toml`. Accepted by `uibcdf/molsyssuite#4`.

## Common responsibilities

Ruff is the formatter, import sorter and linter. Pytest is the test runner. The common
developer and CI checks are:

```bash
ruff format --check .
ruff check .
pytest
```

The corresponding local cleanup sequence is `ruff check --fix .` followed by
`ruff format .`, review and the complete test suite. Ruff formatting alone does not sort
imports; the fix step applies the enabled `I` rules.

Once a repository has migrated successfully, Black, isort and flake8 are removed from its
active development dependencies, configuration, commands and CI gates. Historical
references in archived records do not count as active use.

## Shared baseline and local configuration

Every Python repository enables at least Ruff rule families `E4`, `E7`, `E9`, `F` and `I`.
These cover fundamental pycodestyle failures, Pyflakes and import ordering without forcing
domain-specific preferences on every component.

Repositories may extend the rules, exclusions and per-file ignores for their own code.
They may not disable part of the common baseline silently. A required local conflict uses
the exception process below.

Ruff configuration stays in each repository's `pyproject.toml`, because source layouts,
generated files and notebooks differ. The suite owns the required subset and audits it;
it does not copy an entire configuration blindly into every member.

The initial shared configuration is equivalent to:

```toml
[tool.ruff]
target-version = "py311"

[tool.ruff.lint]
select = ["E4", "E7", "E9", "F", "I"]
```

Repositories may choose their own line length only when existing public or generated
material makes the common formatter default unsuitable.

## Type checking and runtime validation

No static type checker is part of the common gate at policy version 1.0. A repository may
run mypy, Pyright or another checker locally when it produces useful signal.

ArgDigest validates and normalizes runtime arguments; it is complementary to static type
checking, not a technical replacement for it. Its use is decided by API needs rather than
by this quality-tooling policy.

## Version management

The shared CI workflow will pin the Ruff version tested for a policy release. Repository
development environments use that version or a compatible newer version that produces
the same required result. Ruff upgrades are evaluated centrally and then propagated,
rather than discovered independently by eleven repositories.

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
