# Python support policy

This document is normative for repositories carrying the `python-library` profile in
`suite.toml`. Accepted by `uibcdf/molsyssuite#3`.

## Supported versions

MolSysSuite Python libraries declare:

```text
requires-python = ">=3.11,<3.14"
```

They support Python 3.11, 3.12 and 3.13. Python 3.13 is the routine development version:
local development environments, maintenance commands and the most complete CI lane should
run there.

The string above is the canonical representation used in `suite.toml`; semantically
equivalent forms such as `>=3.11.0,<3.14.0` conform as well. The policy guards supported
versions, not punctuation.

Supporting a version means that installation metadata admits it and the repository's
required test suite runs on it. Each Python library therefore has Linux CI lanes for all
three supported minor versions. Repositories may add operating systems, dependency
variants and specialized lanes according to their own risks.

## One range, two responsibilities

The full supported matrix protects users; the development version gives maintainers one
predictable default. Developing on 3.13 does not permit using syntax or standard-library
APIs unavailable on 3.11.

Repository-specific environments stay local. Their package choices may differ, but they
must not silently change the supported range or default Python version.

## Changing the range

Adding or dropping a Python minor is a suite-wide compatibility decision. It requires a
central proposal that records dependency readiness, member impact, CI availability and a
migration plan. Individual repositories do not change the common range unilaterally.

## Exceptions

An exception names its repository, differing value, reason, tracking issue and expiration
condition. It is recorded centrally and must not be represented as general support for the
suite. There are no initial exceptions.

## Rollout

This policy defines the target. Each repository that differs receives a local issue and
change, with its own dependency resolution and tests. A central adoption record tracks
collective completion without duplicating local analysis.
