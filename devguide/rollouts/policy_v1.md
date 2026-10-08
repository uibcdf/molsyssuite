# MolSysSuite policy 1.0 rollout

**Issue:** `uibcdf/molsyssuite#6`
**Final policy release:** `policy-v1.5.2`
**Started:** 2026-09-06
**Status:** Completed 2026-09-27.

## Acceptance

Every member registered in `suite.toml` must either pass:

```bash
python devtools/scripts/check_repository.py ../<member> --repository uibcdf/<member>
```

or carry a central exception naming its reason, issue and expiration condition.

Migration work is prioritized using the cohorts in `suite.toml`: the six wave-1
libraries first, receptor repositories as supporting infrastructure, Lindelint as an
auxiliary component, and the three incubating scientific tools only when they enter
stabilization. Already completed infrastructure adoption remains valid; auxiliary and
incubating members do not block the wave-1 stabilization decision.

## Initial audit

Measured locally on 2026-09-06 with Python 3.13.15. Findings are stable audit codes, not
estimates of migration effort.

Corrected on 2026-09-06 by `uibcdf/molsyssuite#7`: the 1.0.0 guard did not inspect active
Ruff CI commands. This live matrix incorporates the corrected `RUFF_CI` results.

Corrected again by `uibcdf/molsyssuite#9`: the 1.1.0 guard confused Ruff's own isort
settings with the replaced standalone tool. Release 1.1.2 parses that configuration
structurally and preserves detection of actual legacy tooling. The intermediate immutable
1.1.1 tag is not usable because its reusable workflow checked out the prior policy release;
`uibcdf/molsyssuite#10` adds a regression for that self-reference.

Release 1.1.4 adds the vendored-guide ownership boundary from
`uibcdf/molsyssuite#12`. The guard requires explicit Ruff exclusions, while an independent
cross-repository workflow checks markers, inventory and exact byte equality. The
intermediate immutable 1.1.3 tag contains the policy behavior but its own test suite used
a checkout-local sibling fixture; 1.1.4 replaces that fixture with a hermetic one.

Release 1.1.5 registers Lindelint as the suite's auxiliary interpolation component and
adds all of its consumed guides to the byte-drift inventory. Auxiliary status makes the
common contract applicable without allowing its adoption work to block wave 1.

Release 1.1.6 resolves `uibcdf/molsyssuite#22`: a pinned Python policy workflow no
longer compares ambassador-guide bytes against its older tagged snapshot. It still
requires the local guide and pointer; the independent cross-repository sync workflow
compares bytes against current canonical sources. The local conformance command keeps
its default byte comparison.

Release 1.2.0 adds the phased Python-minor transition owned by
`uibcdf/molsyssuite#29`. The default remains Python 3.11--3.13; individually authorized
or admitted components use the target 3.11--3.14 contract. Policy 1.1.6 remains compatible
for repositories outside the transition, while a participating component must call 1.2.0.
Pytest Receptor is the first authorized component after local Python 3.14.7 and hosted
pytest 8/9 evidence passed.

Release 1.3.0 promotes the repository badge validator into the common offline and
reusable policy gate after every registered member adopted the canonical identity,
policy, Python and license baseline under `uibcdf/molsyssuite#23`. Conditional service
badges remain governed by networked evidence and are not inferred by the offline gate.

Release 1.3.1 captures pytest-receptor's subsequent transition from Python 3.14
`authorized` to `admitted`, so the same gate requires its public badge to claim the
delivered 3.11--3.14 range. Release 1.3.0 remains compatible for members whose registry
contract did not change.

Release 1.4.2 registers DockingMT as an incubating scientific component under
`uibcdf/molsyssuite#36` and carries the import-smoke fail-fast detector introduced by
`uibcdf/molsyssuite#33`. The immutable 1.4.1 snapshot predates DockingMT and therefore
correctly reports it as unregistered. Caller adoption of 1.4.2 is tracked by
`uibcdf/molsyssuite#34`; the release-version gate requires the new caller so a repository
cannot claim current conformance through an older snapshot.

Release 1.4.3 captures ArgDigest's admission to Python 3.14 after its public
0.13.0 release, exact-file Conda promotion, installed-package matrix, and verified
Zenodo source snapshot. ArgDigest must adopt the 1.4.3 caller before displaying
the Python 3.14 badge; caller rollout remains tracked under `uibcdf/molsyssuite#34`.

Release 1.4.5 records PyUnitWizard's admission after its 0.26.0 public release,
exact-file noarch Conda promotion, eight-cell clean installed-package matrix,
and independent public Python 3.14 installation. The source tag was also
installed in a clean environment against published Conda dependencies. The
PyUnitWizard policy caller and public Python badge must adopt 1.4.5 together;
this does not automatically migrate other members' policy pins.

Release 1.4.6 adds the offline `SIBLING_CI_ROUTE` guard from
`uibcdf/molsyssuite#31`. A component with a required registered sibling must expose
a committed Conda environment through `setup-micromamba` or an explicit pinned-source
install in CI. The guard only checks structure; installed imports and test results
remain the component's responsibility. Caller adoption is tracked by
`uibcdf/molsyssuite#34` independently of guide-copy synchronization.

Release 1.4.7 introduced inheritance of platform engineering values from the immutable MOLI
revision recorded in `suite.toml`. MolSysSuite retains member adoption and
exception state; the `policy-v1.4.6` gate remains accepted during rollout.
The new gate checks the exact MOLI registry revision and rejects locally copied
platform values. Starter metadata and Python CI versions are generated from
the effective registry. Its guide-audit workflows lacked the required MOLI checkout,
so the immutable 1.4.7 release cannot serve as a fully green governance snapshot.
Release 1.4.8 adds that checkout in both guide audits. Caller migration remains
under `uibcdf/molsyssuite#34`.

Release 1.4.9 reads the pinned MOLI registry directly from its Git commit, so a
newer local MOLI checkout can validate against the recorded immutable snapshot.
The valid 1.4.8 caller remains compatible and satisfies the existing release gate.

Release 1.4.10 moves the effective MOLI snapshot to
`888902eb2ccc482c62c6f75da9d8f0bf9bb56442` after that revision's governance
validator and policy tests passed in an isolated worktree. It adds inherited
support-library and developer-tool policies. Their member review states are
tracked separately in `suite.toml` and
[`python_ecosystem.md`](python_ecosystem.md); a compatible policy caller in the
matrix below does not establish adoption of either new policy.

Release 1.4.11 authorizes MolSysMT and MolSysViewer to enter the Python 3.14
transition under `uibcdf/molsyssuite#29`. Their component-specific compatibility
lists are empty because earlier snapshots do not contain these authorizations;
both must use the 1.4.11 caller. The transition-aware gate requires the target
range and CI matrix for these two components. This authorization does not
admit their unreleased 0.22.4 and 0.23.4 candidates or change the suite-wide
stable default. Each component must pin this immutable release and complete its
own public-delivery and independent clean-install gates before admission.

Release 1.4.12 pins MOLI `15b38fbe17b6ee9fa9aac2a8e21b80d76a8da70f`,
which defines the narrow support-library bootstrap rule in `uibcdf/moli#29`.
Under `uibcdf/smonitor#29`, SMonitor's ArgDigest and DepDigest bootstrap
boundaries are structurally inapplicable only while both providers require
SMonitor at runtime. The member review records hosted source and clean
published Linux installation/import-order evidence. The earlier bounded
exception is removed; ordinary consumers remain subject to the unchanged
applicability rules. Release 1.4.11 remains a compatible CI policy caller;
member review state is read from the effective central inventory in 1.4.12.

Release 1.5.0 returns normative member engineering policy to MolSysSuite under
`uibcdf/moli#30` and `uibcdf/molsyssuite#53`. Its registry and checker use local
MolSysSuite policy values; the recorded MOLI commit is only platform-contract
context for the suite. The published `policy-v1.5.0` tag is immutable. Its copy
of `MOLSYSSUITE_GUIDE.md` incorrectly calls 1.5.0 the effective release for
every member and calls the MOLI commit the effective quantity-policy snapshot.
Those statements are documentation errors in the historical tag: each member's
effective automated engineering policy is the release pinned by its workflow,
and quantity-integrity adoption is tracked separately. The canonical guide on
`main` is corrected under `uibcdf/molsyssuite#54`; do not move the tag. Caller
adoption remains tracked in `uibcdf/molsyssuite#34`.

Release 1.5.1 supersedes the central 1.5.0 release for new callers. It carries
the corrected guide and new-component instructions without changing member
engineering values. Release 1.5.0 remains an allowed historical snapshot; its
tag and contents are not rewritten. Member caller adoption remains a separate
rollout under `uibcdf/molsyssuite#34`.

Release 1.5.2 corrects the `SIBLING_CI_ROUTE` false positives in
`uibcdf/molsyssuite#55`: the checker now recognizes an executed requirements
file with full-commit sibling pins and a pinned checkout that CI installs,
alongside referenced Conda environment packages. Routes may cover different
siblings in the same workflow. This changes conformance detection, not member
dependency versions. Releases 1.5.0 and 1.5.1 remain immutable compatible
snapshots; caller adoption is tracked in `uibcdf/molsyssuite#34`.

## Initial audit snapshot

The table below preserves the member states measured during the initial rollout.
It is not the current adoption inventory.

| Member | Cohort | Initial state | Local issue | Evidence / initial findings |
| --- | --- | --- | --- | --- |
| pytest-receptor | infrastructure | adopted | `uibcdf/pytest-receptor#2` | policy 1.1.6 run `35468881428` |
| gh-run-receptor | infrastructure | adopted | `uibcdf/gh-run-receptor#22` | policy 1.1.6 run `35469618608`; 443 local tests |
| lindelint | auxiliary | adopted | `uibcdf/lindelint#4` | policy 1.1.6 run `35468888550` |
| argdigest | wave 1 | adopted | `uibcdf/argdigest#4` | policy 1.1.6 run `35468876708` |
| depdigest | wave 1 | adopted | `uibcdf/depdigest#3` | policy 1.1.6 run `35468878368` |
| elastnetmt | incubating | badge baseline adopted; policy debt open | `uibcdf/elastnetmt#12` | live policy workflow exposes `GOVERNANCE_POINTER`, `RUFF_CONFIG`, `VENDORED_GUIDE_RUFF`, `LEGACY_TOOL` |
| dockingmt | incubating | adoption active | `uibcdf/dockingmt#1` | admission inspection found the policy caller, canonical badges, integration guides and reporting lifecycle absent |
| molsysmt | wave 1 | adopted; Ruff exception resolved | `uibcdf/molsysmt#211` | policy 1.1.6 run `35468885292`; full-tree Ruff run `35788061365`, guarded by `uibcdf/molsysmt#212` |
| molsysviewer | wave 1 | adopted | `uibcdf/molsysviewer#87` | policy 1.1.6 run `35468887226` |
| pharmacophoremt | incubating | badge baseline adopted; policy debt open | `uibcdf/pharmacophoremt#3` | live policy workflow exposes `GOVERNANCE_POINTER`, `PYTHON_RANGE`, `PYTHON_CI`, `RUFF_CONFIG`, `VENDORED_GUIDE_RUFF`, `LEGACY_TOOL` |
| pyunitwizard | wave 1 | adopted | `uibcdf/pyunitwizard#74` | policy 1.1.6 run `35468880337`; 495 local tests, 10 skips |
| smonitor | wave 1 | adopted | `uibcdf/smonitor#12` | policy 1.1.6 run `35468874895`; local suite passed |
| topomt | incubating | badge baseline adopted; policy debt open | `uibcdf/topomt#16` | structural policy check passes; hosted full Ruff lint remains red |

## Resolved exceptions

### MolSysMT legacy-tree Ruff boundary — resolved 2026-09-22

- **Repository:** `uibcdf/molsysmt`.
- **Former exception:** full `E4`, `E7`, `E9`, `F`, `I` lint and Ruff-format
  coverage over the legacy core, tests and documentation trees was deferred
  during the initial policy rollout.
- **Tracking issue:** `uibcdf/molsysmt#212`.
- **Resolution:** the temporary Python-tree exclusions and narrow critical-rule
  substitute were removed. `ruff check .` and `ruff format --check .` cover
  every tracked Python file; the local file-selection guard detects hidden
  exclusions. The hosted Ruff workflow passed in run `35788061365`, and the
  central registry no longer records an active exception.

## Rollout discipline

- Start with repositories already technically conforming to validate routing and workflow
  invocation.
- Open a local issue only when a concrete repository change starts.
- Keep formatting-only changes separate from behavioral fixes.
- Run each repository's existing tests before removing a legacy gate.
- Update this matrix from measured checker output, not from intent.
- Do not close the central issue when the first member passes.

## Completion

The final `policy-v1.5.2` release was adopted by all 14 registered policy callers.
`adoption_status.py --kind policy --check` reported 14/14 current, and all 14
hosted policy workflows passed. `sync_vendored_guides.py` reported all 15
registered `MOLSYSSUITE_GUIDE.md` copies current. Central governance run
`36310377046`, vendored-guide run `36310587878`, and component-guide run
`36310587903` passed. The checker was run locally against every member and
the final 15 checkouts were current and clean against their remotes.

The initial conformance rollout is complete. `uibcdf/molsyssuite#56` now owns
the six unassigned Python ecosystem reviews formerly linked to this issue;
other partial reviews remain with their member-local issues. Future guide
and policy releases follow `devguide/adoption_lifecycle.md`.


## Ackredit delivered-support snapshot — 2026-10-04

Policy 1.5.6 is published at `f663290e6bc5a1cac66f3a7b979b918a4233fc2b` to capture Ackredit's verified Python 3.11–3.14
public Conda admission under uibcdf/molsyssuite#51 / #29. The original 0.9.0
`py_0` file, four exact-source gates, eight Linux/macOS-arm64 installed cells
and independent normal public Python 3.14 installation meet the existing
criteria. This snapshot preserves older tags and other member states.
Only Ackredit's caller must adopt it to claim the new delivered range;
compatible callers elsewhere remain permitted. The canonical suite guide
refresh communicates the current snapshot separately from caller adoption.
Publication, synchronized copies and actual exact-head gates remain distinct
in `devguide/rollouts/ackredit_python314_admission_51.json`.

All sixteen guide copies are published/current. Ackredit adopts the snapshot
and badge at `8c743b3f54da8ed172e9b9ff5d8eff02d9b8c410`; its routine, policy
and publication checks pass. Other compatible callers remain unchanged.


## Archival experiment tag capability — 2026-10-04

Policy 1.5.7 is published at `f1ae1a043720e33493024d8afcab1e45375e42a2`
under uibcdf/molsyssuite#84. Nonempty `archive/<description>` tags preserve
experimental or historical commits without package, GitHub Release or
publication-evidence meaning. Canonical public `X.Y.Z`, candidate gates and
existing immutable tags remain protected. A repository using archive tags
needs the capable policy and an unconditional all-tag trigger; the starter now
uses `tags: ["**"]`, and the gate rejects filters that miss or skip such pushes.

All sixteen canonical guide copies are published/current. MolSysMT adopts
the caller and trigger at `1945498ff1caf36be14d3b8a364fa02482b042d6`; native
administrative conformance run `37208585357` passes on that exact head.
Fourteen other policy callers remain compatible (Ackredit at 1.5.6, thirteen at
1.5.4); guide delivery does not imply universal caller adoption. Native central
governance, development workspace and both final guide audits pass.
`devguide/rollouts/archive_tags_84.json` preserves publication, notices,
negative publisher controls, delivery commits and bounded evidence separately.
No scientific run or publication was manufactured. MOLI reviews possible
direct-component/support-provider applicability independently in uibcdf/moli#47.

## MolSysMT delivered Python qualification — 2026-10-08

Policy `policy-v1.5.9` is published at
`3116b7d9f1fa9ba4d09b81a8f24a22b749805f9f` under uibcdf/molsyssuite#51 from the
independently received MolSysMT 0.23.0 / Viewer 0.24.0 public pair. It freezes
MolSysMT's `admitted` state and matching four-minor badge; Python requirements
and engineering gates are unchanged. Its support-library/developer-tool
reviews are separately `adopted` under uibcdf/molsysmt#244.

The [receiving and delivery receipt](molsysmt_python314_ecosystem_51_20261008.json)
retains evidence and policy/member/guide delivery independently. Existing
immutable tags remain fixed; only MolSysMT's caller requires this qualified
badge snapshot. Other compatible callers and component qualification states
remain unchanged. Canonical guide refreshes do not clear scientific skip debt.

MolSysMT delivery `a04ec0fa3a947a7c959b7f56b09301bb37eceb90` passes exact
manual policy/Ruff `37742928564` and devguide `37742932367`; #237/#244 are
closed with archived guards and the board agrees. All fifteen accessible
canonical guide consumers are published/current under the official source,
destination and byte checks. OpenCASTp remains unavailable under #102's
accepted temporary scope (review 2026-10-11/access change); its primary is
preserved and its sixteenth guide copy is not claimed current. The five hosted
access failures remain visible. No consumer scientific debt is cleared.
