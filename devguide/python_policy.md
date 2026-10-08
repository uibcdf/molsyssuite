# Python support policy

## Ownership

MolSysSuite owns the Python support rule for its registered members. The values in `suite.toml` and the transition and exception process below are normative. They initially match MOLI's direct-component range, but a MOLI revision does not automatically change the member rule.

This document is normative for repositories carrying the `python-package` capability in
`suite.toml`. Accepted by `uibcdf/molsyssuite#3`.

## Suite Python baseline

As directed by the suite maintainer on 2026-10-02, every registered Python
package must adopt `>=3.11,<3.15`, with required full CI minors `3.11`, `3.12`,
`3.13` and `3.14`. `suite.toml` declares that common requirement. Routine
local development and testing use `3.14`. This applies to incubating and auxiliary
packages as well as the initial transition cohort, and is tracked by
`uibcdf/molsyssuite#29` and `uibcdf/molsyssuite#51`.

Use the shared Python 3.14 development environment where the member's normal
dependency closure is installable. A member still unable to install or run on
3.14 records the blocker, owner and exit condition; it may use a temporary
older environment only for that bounded migration work. Do not describe an
override, editable install or feasibility probe as delivered 3.14 support.
Compatibility tests for supported older minors remain required.

The [development workspace contract](development_workspace.md) defines the
named Linux environment, editable local-clone installation, interpreter/import
verification and tracked exclusions. Follow its current registry-derived cohort
rather than assuming every member or direct MOLI component is already integrated.

The requirement is distinct from verified delivery: a component whose
metadata, tests or public artifacts still lag has pending adoption, not
permission to ignore 3.14 and not automatic certification. The [suite CI
policy](python_ci_policy.md) sets evidence and deferred-test routes. Missing
compatibility remains component-owned and requires tracked, bounded exceptions
when adoption cannot yet be completed.

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

The common conformance gate now requires the target range and CI versions for
every Python package, including components absent from the qualification
table. `authorized` and `admitted` record evidence and delivery progress; they
do not determine whether the obligation applies. Compatible older immutable
policy releases retain their historical behavior until a caller is migrated;
pinning one does not waive the current requirement. A component may not infer
admission from another member, from being noarch, or from one successful import.

Reviewed historical quality callers are registered in
`governance.transition-compatible-policy-releases`. A component's explicit
`compatible-policy-releases` list remains restrictive; adding a reviewed release
to the catalogue does not override that component list. Retain immutable
workflow and executed quality-step evidence in the owning transition issue when
registering an existing caller. Recognizing its Ruff gate does not establish
Python admission, a complete scientific suite or public-package qualification.
The scoped MolSysViewer `policy-v1.5.7` registration is recorded under
uibcdf/molsyssuite#39 and uibcdf/molsysviewer#93.

A staging package is evidence for promotion, not public delivery. For a pure-Python
`noarch` Conda package, admission does not require a separate file named for the new
interpreter: the published `noarch` artifact must declare the target range, resolve in a
clean environment on that interpreter, and pass the component's installed-package smoke
test. Components distributed only as GitHub Release wheel and source archives meet the
same rule through those declared channels. A source branch, development install, or
staging label may remain `authorized` indefinitely but cannot be `admitted`.

The previous universal-admission prerequisite for changing the required range
is superseded by the maintainer's 2026-10-02 decision. Public suite prose must
still distinguish mandatory adoption from verified member delivery. During
this rollout, badges for components not yet admitted retain the previous
three-minor claim from `transition.previous-ci-versions`; advancing the common
requirement alone must not generate a new delivered-support claim.

## Rollout

This policy defines the target. Each repository that differs receives a local issue and
change, with its own dependency resolution and tests. A central adoption record tracks
collective completion without duplicating local analysis.
