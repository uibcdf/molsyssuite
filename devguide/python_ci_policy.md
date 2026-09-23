# Python CI lane policy

## MOLI ownership note

This document is the **MolSysSuite CI adoption profile** for the MOLI Python CI baseline. The platform engineering-policy owner is `uibcdf/moli` (`devguide/policies/python_ci_policy.md`). MolSysSuite retains the detailed member rollout/evidence contract and may impose stricter modeling-ecosystem requirements without weakening the MOLI baseline.

This document is the accepted target for repositories carrying the
`python-package` capability in `suite.toml`. It records the decision in
`uibcdf/molsyssuite#39`. Adoption is phased: the registry entry and starter-kit
workflow do not assert that every existing member already conforms, and the
current repository checker does not yet enforce this policy.

## Member evidence for the inherited CI baseline

MOLI defines the routine event, Python and operating-system requirements, the full matrix, its frequency and manual dispatch in [the pinned platform CI policy](https://github.com/uibcdf/moli/blob/888902eb2ccc482c62c6f75da9d8f0bf9bb56442/devguide/policies/python_ci_policy.md) and pinned `moli.toml`. A bounded smoke suite is acceptable for a demonstrably expensive component only when omitted coverage and a full-suite lane are documented in a tracked component issue and linked from the central adoption record. A scheduled matrix is evidence only after its jobs pass; skipped, cancelled, unresolved and tolerated failures do not count. Stagger member schedules. Before member admission or release, the full matrix must be green for the exact candidate commit.

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
YAML. GitHub remains authoritative for run, job and step conclusions. The
[effective MOLI developer-tools policy](https://github.com/uibcdf/moli/blob/888902eb2ccc482c62c6f75da9d8f0bf9bb56442/devguide/policies/python_developer_tools_policy.md)
governs agent inspection of hosted runs. An external registry such as
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
