# Python CI lane policy

This document is the accepted target for repositories carrying the
`python-package` capability in `suite.toml`. It records the decision in
`uibcdf/molsyssuite#39`. Adoption is phased: the registry entry and starter-kit
workflow do not assert that every existing member already conforms, and the
current repository checker does not yet enforce this policy.

## Routine and full coverage

Every push and pull request must have a gating Linux test lane on Python 3.13,
the suite's routine development version. The default is the component's
required test suite. A bounded smoke suite is acceptable only for a
demonstrably expensive component when the omitted coverage and a full-suite
lane are documented in a tracked component issue and linked from the central
adoption record. A passing quality, documentation or release job is not a
substitute for a test lane. Extra routine versions are welcome but not required
suite-wide.

At least weekly, a gating Linux matrix must run the component's complete
required test suite on every minor in its effective supported Python range.
The effective range is the accepted default in `policies.python`, or the
transition target for a component listed as `authorized` or `admitted` under
`policies.python.transition`. A workflow file that schedules a matrix is not
proof it ran; a skipped, cancelled, unresolved or tolerated-failure job does
not provide passing evidence. Schedule timing is local to each component and
should be staggered rather than concentrated at the start of an hour.

The first new scheduled matrix must pass a manual dispatch before it is
counted as evidence. Before admitting a new Python minor or publishing a
release, the full supported-minor matrix must be green for the exact candidate
commit, whether triggered by schedule or manual dispatch. A previously green
commit cannot stand in for a changed candidate.

## Platforms and experimental versions

Linux is the common minimum. A component may claim macOS or Windows support
only with a representative gating lane and a regular full supported-minor
matrix for that platform, or a centrally tracked exception with a reason,
owner and retirement condition. Neither `noarch` packaging nor a platform
name inside an action's inputs establishes runtime compatibility or an
observable GitHub job for that platform. Member-specific platform claims and
exceptions will be recorded during the phased rollout; the central minimum
does not manufacture claims for members that have not made them.

An unsupported Python minor belongs in a separate, explicitly dispatched
feasibility workflow that is not a required branch check. Its failure should
remain visible. A `continue-on-error` cell in otherwise green CI is not a
passing support gate. When a minor is accepted for a component, it joins the
required full matrix and the Python-support admission process applies.

## Evidence and adoption

The owning component chooses its workflow structure, environment solver and
specialized tests. The contract is about observable test outcomes, not common
YAML. GitHub remains authoritative for run, job and step conclusions;
gh-run-receptor is the preferred first inspection tool when available, with
native GitHub inspection for missing detail. An external registry such as
Anaconda is a separate publication gate, not a substitute for test evidence.

The read-only `devtools/scripts/ci_lane_inventory.py` helps identify
configured event and matrix cells, direct pytest commands, conditions and
non-gating jobs. It cannot prove execution or distinguish a complete test
suite from smoke tests. The future policy checker must validate those
semantics against component-specific workflow patterns and hosted evidence
before it can enforce this contract. Until that checker and a versioned shared
policy release exist, this is an adoption target, not a claim of compliance.

Existing repositories receive local migration issues only for concrete
workflow changes or exceptions. The central issue tracks the collective
rollout and records reviewed member claims. An exception cannot silently
change the common Python range or another member's support claim.
