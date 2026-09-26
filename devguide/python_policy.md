# Python support policy

## Ownership

MolSysSuite owns the Python support rule for its registered members. The values in `suite.toml` and the transition and exception process below are normative. They initially match MOLI's direct-component range, but a MOLI revision does not automatically change the member rule.

This document is normative for repositories carrying the `python-package` capability in
`suite.toml`. Accepted by `uibcdf/molsyssuite#3`.

## Suite Python baseline

`suite.toml` defines the stable supported range `>=3.11,<3.14`, routine development version `3.13`, and required CI minors `3.11`, `3.12`, and `3.13`. The [suite CI policy](python_ci_policy.md) sets member evidence and rollout. Repository-specific environments may choose their dependencies while preserving the suite support claim.

## Changing the range

Adding or dropping a minor from the suite baseline is a MolSysSuite decision. MolSysSuite owns readiness assessment, staged rollout, admission evidence, and exceptions. Individual members do not change the common range unilaterally. A change affecting MolSysSuite's platform-facing contract is also raised in MOLI.

## Exceptions

An exception names its repository, differing value, reason, tracking issue and expiration
condition. It is recorded centrally and must not be represented as general support for the
suite. There are no initial exceptions.

## Phased adoption of a new minor

An accepted transition may add a target range and a target CI matrix under
`policies.python.transition` in `suite.toml`. Each participating component has a local
issue and one of two states:

- `authorized`: feasibility evidence has passed and the component is expected to adopt
  the target contract, but its metadata, packaging, documentation, and clean-install gates
  or public delivery are not yet all complete;
- `admitted`: those component-owned surfaces and gates agree, an immutable public release
  declares the target range, and independent clean installations have verified that
  release from every package channel the component claims to support. Only then may the
  component claim the target range.

Both states make the transition-aware conformance gate require the target range and CI
versions. This deliberately turns an authorization into an actionable failing gate until
the local update lands. Components absent from the transition continue to use the stable
default contract and may keep the immediately preceding compatible policy release during
the rollout. A component may not infer admission from another member, from being noarch,
or from one successful import.

A staging package is evidence for promotion, not public delivery. For a pure-Python
`noarch` Conda package, admission does not require a separate file named for the new
interpreter: the published `noarch` artifact must declare the target range, resolve in a
clean environment on that interpreter, and pass the component's installed-package smoke
test. Components distributed only as GitHub Release wheel and source archives meet the
same rule through those declared channels. A source branch, development install, or
staging label may remain `authorized` indefinitely but cannot be `admitted`.

The stable suite-wide range changes only when every required member is admitted or carries
an explicit exception. Until then, public suite-level prose must distinguish the default
range from individually admitted components.

## Rollout

This policy defines the target. Each repository that differs receives a local issue and
change, with its own dependency resolution and tests. A central adoption record tracks
collective completion without duplicating local analysis.
