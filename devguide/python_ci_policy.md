# Python CI lane policy

## Ownership

MolSysSuite owns the Python CI target for registered members. The values in `suite.toml` and evidence process below are member policy. They initially match the corresponding MOLI direct-component values, but a MOLI revision does not automatically change this target.

This document is the accepted target for repositories carrying the
`python-package` capability in `suite.toml`. It records the decision in
`uibcdf/molsyssuite#39`. Adoption is phased: the registry entry and starter-kit
workflow do not assert that every existing member already conforms, and the
current repository checker does not yet enforce this policy.

## Member evidence for the suite CI baseline

The suite requires a routine Linux/Python 3.13 lane on direct pushes, a full
required suite on Linux/Python 3.13 for every pull request, a weekly full
Linux matrix for Python 3.11–3.14, and manual dispatch. A bounded smoke suite
is acceptable on direct pushes for a demonstrably expensive component only
when omitted coverage and
a full-suite lane are documented in a tracked component issue and linked from
the central adoption record. A member may run more Python and platform cells
on PRs, but the common PR gate requires the complete test suite on the routine
minor. A scheduled matrix is evidence only after its jobs pass; skipped,
cancelled, unresolved
and tolerated failures do not count. Stagger member schedules. Before member
admission or release, the full matrix must be green for the exact candidate
commit.

## Contributor routes and deferred tests

Repositories may permit named internal maintainers to push directly without
waiting for a full suite after each commit. Their routine push lane may be a
bounded smoke test. If a repository permits `[skip ci]` or another GitHub
skip marker on direct pushes, it must also run a conditional full Linux matrix
daily on its default branch. The daily decision examines commits since the
last successful *executed* full matrix, rather than only commits from one
calendar day. Any skipped commit still in that range triggers the full suite;
failed, missed, cancelled or inconclusive runs leave the backlog due. An
unavailable history or run API must cause the suite to run. An unconditional
weekly full matrix and manual dispatch remain available. A failure remains
visible and is owned by the component team.

External changes enter through a pull request. The full suite is required
before integration, regardless of who authored the PR; an internal maintainer
choosing a PR follows the same route. Repository access and branch protection
enforce the distinction between PR integration and direct maintainer pushes.
The required PR check must be stable and must fail when its full-suite test
fails or is skipped. Administrators with the explicit direct-push route
must retain that route; the policy does not require a full suite before their
push. The exact daily time and workflow structure belong to the component.

## Platforms and experimental versions

Linux and macOS arm64 are the suite's support target for public Python packages;
Windows is optional. Intel-based macOS (`x86_64`/`osx-64`) is outside the
supported platform matrix and is not a release gate. Its support may be
reconsidered if there is demonstrated user demand (`uibcdf/molsyssuite#59`).
The machine-readable `macos-architectures = ["arm64"]` applies to every member's
macOS claim; it does not add a claim to an unreviewed member. The
[source adoption inventory](rollouts/macos_arm64.md) tracks owners and remaining
runtime/claim reviews. Reconsideration begins with a concrete user need in a suite
issue and requires an explicit decision, component ownership and fresh evidence.
macOS arm64 needs recurring test evidence at least weekly and
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

## Member review record

Every registered Python package has one `[[python-ci-reviews]]` entry in
`suite.toml`. `pending` means that the member has not yet had a policy-grade
review; it does not mean that tests or workflows are absent. Pending entries
use `routine-test-level = "unreviewed"`,
`platform-claims-reviewed = false`, and an empty `platform-claims` list.
The read-only lane inventory may guide review, but cannot advance this state
on its own. An empty list while `platform-claims-reviewed = false` means the
claims are unknown, not that the member has declared every platform unsupported.

`partial` records a concrete member-owned gap and links its issue and
evidence. `adopted` requires a reviewed `full` or bounded `smoke` direct-push
routine test level, a full-suite PR lane, explicit platform claims, a local
issue, and hosted run evidence for the required routine and full lanes. A
member using CI-skip markers also needs evidence that its daily recovery
detects pending skips and retries after failure. A smoke review links the
local issue that defines its omitted coverage and full-suite route. An empty reviewed
platform list means that an incubating member makes no public OS support claim;
it does not waive its Linux CI lanes. A public platform claim needs the
recurring and installed-artifact evidence specified above. A `partial` or
`adopted` review must distinguish configured jobs from runs that executed and
passed; include run URLs and exact commit identifiers in its evidence.

`excepted` is a bounded member-owned deviation, with a local issue, reason,
owner, expiry date and testable removal condition. It does not turn a failed
or skipped lane green, and it cannot create a support claim. Run
`python devtools/scripts/python_ci_status.py` for the review inventory, or
add `--require-adopted` to assess rollout completion. The offline governance
guard checks record completeness and exception expiry; it cannot verify a
hosted result without inspecting GitHub. The repository checker will enforce
lane structure only after the member patterns and test levels have been
reviewed and a versioned policy release is published.
