# MolSysSuite policy 1.0 rollout

**Issue:** `uibcdf/molsyssuite#6`
**Policy release:** `policy-v1.3.1`
**Started:** 2026-09-06
**Status:** Active.

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

| Member | Cohort | State | Local issue | Evidence / initial findings |
| --- | --- | --- | --- | --- |
| pytest-receptor | infrastructure | adopted | `uibcdf/pytest-receptor#2` | policy 1.1.6 run `35468881428` |
| gh-run-receptor | infrastructure | adopted | `uibcdf/gh-run-receptor#22` | policy 1.1.6 run `35469618608`; 443 local tests |
| lindelint | auxiliary | adopted | `uibcdf/lindelint#4` | policy 1.1.6 run `35468888550` |
| argdigest | wave 1 | adopted | `uibcdf/argdigest#4` | policy 1.1.6 run `35468876708` |
| depdigest | wave 1 | adopted | `uibcdf/depdigest#3` | policy 1.1.6 run `35468878368` |
| elastnetmt | incubating | badge baseline adopted; policy debt open | `uibcdf/elastnetmt#12` | live policy workflow exposes `GOVERNANCE_POINTER`, `RUFF_CONFIG`, `VENDORED_GUIDE_RUFF`, `LEGACY_TOOL` |
| dockingmt | incubating | adoption active | `uibcdf/dockingmt#1` | admission inspection found the policy caller, canonical badges, integration guides and reporting lifecycle absent |
| molsysmt | wave 1 | adopted with exception | `uibcdf/molsysmt#211` | policy 1.1.6 run `35468885292`; legacy-tree exception `uibcdf/molsysmt#212` |
| molsysviewer | wave 1 | adopted | `uibcdf/molsysviewer#87` | policy 1.1.6 run `35468887226` |
| pharmacophoremt | incubating | badge baseline adopted; policy debt open | `uibcdf/pharmacophoremt#3` | live policy workflow exposes `GOVERNANCE_POINTER`, `PYTHON_RANGE`, `PYTHON_CI`, `RUFF_CONFIG`, `VENDORED_GUIDE_RUFF`, `LEGACY_TOOL` |
| pyunitwizard | wave 1 | adopted | `uibcdf/pyunitwizard#74` | policy 1.1.6 run `35468880337`; 495 local tests, 10 skips |
| smonitor | wave 1 | adopted | `uibcdf/smonitor#12` | policy 1.1.6 run `35468874895`; local suite passed |
| topomt | incubating | badge baseline adopted; policy debt open | `uibcdf/topomt#16` | structural policy check passes; hosted full Ruff lint remains red |

## Active exceptions

### MolSysMT legacy-tree Ruff boundary

- **Repository:** `uibcdf/molsysmt`.
- **Rule:** full `E4`, `E7`, `E9`, `F`, `I` lint and Ruff-format coverage over
  the legacy core, tests and documentation trees.
- **Reason:** immediate migration reported 13,500 core findings and would mix a
  repository-wide mechanical rewrite with policy adoption. Current maintenance
  tooling and the MolSysViewer add-on use the full shared gate; the core retains
  a separate `F821`, `F822`, `F823`, `B006`, `B023` critical-rule gate.
- **Tracking issue:** `uibcdf/molsysmt#212`.
- **Expiration:** remove the exception when every maintained Python tree passes
  the full shared lint and format gate; any permanent generated or historical
  exclusion requires a separate justification.

## Rollout discipline

- Start with repositories already technically conforming to validate routing and workflow
  invocation.
- Open a local issue only when a concrete repository change starts.
- Keep formatting-only changes separate from behavioral fixes.
- Run each repository's existing tests before removing a legacy gate.
- Update this matrix from measured checker output, not from intent.
- Do not close the central issue when the first member passes.
