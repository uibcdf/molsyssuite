# Python CI lane policy

## Ownership

MolSysSuite owns the Python CI target for registered members. The values in `suite.toml` and evidence process below are member policy. They initially match the corresponding MOLI direct-component values, but a MOLI revision does not automatically change this target.

This document is the accepted target for repositories carrying the
`python-package` capability in `suite.toml`. It records the decision in
`uibcdf/molsyssuite#39`. Adoption is phased: the registry entry and starter-kit
workflow do not assert that every existing member already conforms, and the
current repository checker does not yet enforce this policy.

## Member evidence for the suite CI baseline

The suite requires a routine Linux/Python 3.13 lane on pushes and pull requests, a weekly Linux matrix for Python 3.11–3.13, and manual dispatch. A bounded smoke suite is acceptable for a demonstrably expensive component only when omitted coverage and a full-suite lane are documented in a tracked component issue and linked from the central adoption record. A scheduled matrix is evidence only after its jobs pass; skipped, cancelled, unresolved and tolerated failures do not count. Stagger member schedules. Before member admission or release, the full matrix must be green for the exact candidate commit.

## Platforms and experimental versions

Linux and macOS are the suite's support target for public Python packages;
Windows is optional. MacOS needs recurring test evidence at least weekly and
installed-package evidence before a release claim. An incubating member may
declare no platform support yet. A bounded macOS exception needs a central
issue, owner and retirement condition; it does not create a macOS support claim.
Windows is claimed only after comparable evidence. Neither `noarch` packaging nor a platform
name inside an action's inputs establishes runtime compatibility or an
observable GitHub job for that platform. Member-specific platform claims and
exceptions will be recorded during the phased rollout; the central minimum
does not manufacture claims for members that have not made them.

At least weekly, macOS runs the required tests on the routine Python minor;
the same applies to Windows if claimed. Before a public release, the exact
candidate's installed package and dependency closure are tested on every
claimed OS and Python minor, including representative runtime behavior and
available entry points. A macOS exception keeps the limitation visible and
tests every platform actually claimed. A skipped, cancelled, tolerated-failure
or merely configured lane is not passing evidence. The
[candidate evidence lifecycle](release_version_policy.md#candidate-evidence-lifecycle)
applies; a changed candidate or closure needs fresh evidence. An unmet gate
needs a separate bounded release decision where permitted, while its actual
result remains visible. An exception cannot certify an untested platform.

An unsupported Python minor belongs in a separate, explicitly dispatched
feasibility workflow that is not a required branch check. Its failure should
remain visible. A `continue-on-error` cell in otherwise green CI is not a
passing support gate. When a minor is accepted for a component, it joins the
required full matrix and the Python-support admission process applies.

## Evidence and adoption

The owning component chooses its workflow structure, environment solver and
specialized tests. The contract is about observable test outcomes, not common
YAML. GitHub remains authoritative for run, job and step conclusions. The
[suite developer-tools policy](python_ecosystem_policy.md) governs agent
inspection of hosted runs. An external registry such as
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
