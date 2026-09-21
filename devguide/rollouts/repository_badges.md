# Repository badge and role-identity rollout

**Issue:** `uibcdf/molsyssuite#23`

**Policy:** `devguide/repository_badges.md`

**Started:** 2026-09-20

**Status:** Complete. Every registered member has adopted the baseline and the offline
checker is enforced by the common repository gate in `policy-v1.3.0`.

## Central checkpoint

The central phase accepts three roles, records one role for every registered member,
generates accessible static Shields identity badges and canonical baseline snippets from
`suite.toml`, and validates locally provable README claims. Shields only renders the
centrally controlled label and color; it is not the role authority. No component README
was changed during this phase.

Network-only claims remain outside the offline validator. A later audit must verify live
workflow, coverage, documentation, release, DOI and package surfaces before conditional
badges are treated as current evidence.

## Stabilization-priority network audit — 2026-09-20

The authenticated audit covered the six members named by the stabilization initiative.
All use `main` as their default branch. GitHub workflow evidence was interpreted with
`gh-run-receptor` 1.0.0 and checked against native GitHub metadata; public-service
queries used credential-free endpoints and omitted every existing Codecov query
parameter.

| Member | Continuous tests | Coverage | Documentation | Release / DOI / Conda | Adoption decision |
| --- | --- | --- | --- | --- | --- |
| smonitor | PASS, run `35495668151` | 94.99%, updated 2026-09-20 | public site and deploy run `34290028307` PASS | release and Conda `0.15.0`; DOI not yet verified | retain tests, coverage, docs, release and Conda; omit DOI |
| argdigest | PASS, run `35495668334` | 92.27%, updated 2026-09-20 | public site and deploy run `33493084603` PASS | release and Conda `0.12.1`; DOI not yet verified | retain tests, coverage, docs, release and Conda; omit DOI |
| depdigest | PASS, run `35495668179` | 92.58%, updated 2026-09-20 | public site and deploy run `31268656692` PASS | release and Conda `0.10.1`; DOI not yet verified | retain tests, coverage, docs, release and Conda; omit DOI |
| pyunitwizard | PASS, run `35495668224` | 91.46%, updated 2026-09-20 | public site and deploy run `32129605939` PASS | release and Conda `0.25.0`; DOI verified | retain all six conditional surfaces |
| molsysmt | latest `CI smoke` run `35495668325` cancelled | 78.79%, last updated 2026-03-25 | lowercase public site and deploy run `31781220979` PASS | release and Conda `0.12.0`; DOI verified | tests may show their real state; omit stale coverage; fix workflow and docs targets |
| molsysviewer | FAIL, run `35495668382` | public repository active but totals unknown since 2026-03-18 | public site and deploy run `20903875906` PASS | release and Conda `0.7.0`; DOI verified | tests may show their real state; omit coverage |

The audit also found that MolSysViewer's policy run `35510393219` fails because two
repository files are not Ruff-formatted. The policy badge may display that real failure;
it must not be hidden or converted into a static success claim. The files belong to the
separate Conda work already under active development and are not changed by this rollout.

The existing local records already own the non-mechanical test-health work:
`uibcdf/molsysmt#185` covers the missing README workflow and repeated non-green smoke
runs, while `uibcdf/molsysviewer#88` covers hosted CI that has not reached a trustworthy
green state. No duplicate local issue is needed. The MolSysMT documentation link must use
the deployed lowercase path; the mixed-case metadata URL returns 404. Removing Codecov
query parameters, changing documentation links, and replacing static Conda claims with
package-specific dynamic badges are mechanical adoption edits.

Both existing DOI badges passed the central Zenodo public-record contract. MolSysMT
0.12.0 and MolSysViewer 0.7.0 are now `verified` in
`devguide/rollouts/zenodo_inventory.toml`, including concept DOI, version DOI, record
identity and exact archived source-snapshot inventory.

## Remaining stabilizing-member audit — 2026-09-20

The second audit covered Pytest Receptor, GH Run Receptor and the auxiliary Lindelint
developer tool. The same GitHub, public-service and least-disclosure rules were used.

| Member | Continuous tests | Coverage | Documentation | Release / DOI / distribution | Adoption decision |
| --- | --- | --- | --- | --- | --- |
| pytest-receptor | PASS, run `35512512809` | inactive with no totals | public site and deploy run `35512512786` PASS | release, PyPI and Conda `1.0.0`; DOI unknown | retain tests, docs, release, PyPI and Conda; omit coverage and DOI |
| gh-run-receptor | no continuous test workflow | inactive with no totals | public site and deploy run `35464838526` PASS | release `1.0.0` and DOI verified; distributed as a GitHub CLI extension | retain docs, release and DOI; omit tests, coverage and package-index badges |
| lindelint | PASS, run `35510393167` | 55.13%, updated 2026-09-20 | declared site returns 404 and deployment workflow has no runs | release and Conda `0.2.0`; PyPI absent; DOI unknown | retain tests, coverage, release and Conda; omit docs, PyPI and DOI |

Lindelint's missing documentation surface is tracked by `uibcdf/lindelint#5`; its badge
is omitted until a workflow run deploys a verified public result. Pytest Receptor and GH
Run Receptor are transition-`authorized`, not `admitted`, for Python 3.14, so their
public badges retain the default 3.11--3.13 range. The central generator now changes a
component badge to the target range only after the registry records `admitted`.

## Incubating-member audit — 2026-09-21

The final audit covered TopoMT, PharmacophoreMT and ElastNetMT. All three now have a real
`molsyssuite-policy.yml` workflow and use the `release` gh-run-receptor profile for
action-internal Conda platform builds, resolving `uibcdf/topomt#17`,
`uibcdf/pharmacophoremt#1` and `uibcdf/elastnetmt#10` without pretending that hidden
platforms are GitHub-visible jobs.

| Member | Continuous tests | Coverage | Documentation | Release / distribution | Adoption decision |
| --- | --- | --- | --- | --- | --- |
| topomt | active and FAIL, runs `35570454286` and policy `35570454714` | inactive totals; last update 2025-11-08 | URL serves PocketMT content; `uibcdf/topomt#18` | no release, PyPI or Conda record | baseline plus truthful tests; omit coverage, docs and distribution |
| pharmacophoremt | workflow disabled by inactivity; last PASS `20023056315` | 36.28%, last update 2025-12-08 | mixed PharmacophoreMT/PocketMT content; `uibcdf/pharmacophoremt#4` | no release, PyPI or Conda record | baseline only; omit stale or inactive capabilities |
| elastnetmt | active and FAIL, runs `35570454359` and policy `35570454800` | Codecov endpoint unavailable during audit | public site has misspelled repository identity | GitHub release `0.1.0`; no PyPI or Conda record | baseline, truthful tests and release; omit coverage, docs and package channels |

The policy failures are not rollout failures or hidden health claims. TopoMT continues
under `uibcdf/topomt#16`; PharmacophoreMT and ElastNetMT policy debt is tracked by
`uibcdf/pharmacophoremt#3` and `uibcdf/elastnetmt#12`. ElastNetMT's stale `enmmt/master`
README targets were corrected under `uibcdf/elastnetmt#11`. Documentation remains absent
until the component issues above produce freshly deployed, correctly identified sites.

## Adoption matrix

| Member | Role | Membership | Maturity | Stabilization priority | State | Local issue |
| --- | --- | --- | --- | --- | --- | --- |
| smonitor | support library | primary | stabilizing | yes | adopted `ecc1164` | — |
| argdigest | support library | primary | stabilizing | yes | adopted `d1f1180` | — |
| depdigest | support library | primary | stabilizing | yes | adopted `544fd00` | — |
| pyunitwizard | support library | primary | stabilizing | yes | adopted `4be1c4c` | — |
| molsysmt | scientific component | primary | stabilizing | yes | adopted `f1c6ae39c` | `uibcdf/molsysmt#185` |
| molsysviewer | scientific component | primary | stabilizing | yes | adopted `76d33be5` | `uibcdf/molsysviewer#88` |
| pytest-receptor | developer tool | primary | stabilizing | no | adopted `c208cf2` | — |
| gh-run-receptor | developer tool | primary | stabilizing | no | adopted `56f5b01` | — |
| lindelint | developer tool | auxiliary | stabilizing | no | adopted `bafc2fb` | `uibcdf/lindelint#5` |
| topomt | scientific component | primary | incubating | no | adopted `540003a` | `uibcdf/topomt#16`, `uibcdf/topomt#18` |
| pharmacophoremt | scientific component | primary | incubating | no | adopted `56dd1f8` | `uibcdf/pharmacophoremt#3`, `uibcdf/pharmacophoremt#4` |
| elastnetmt | scientific component | primary | incubating | no | adopted `eacb415` | `uibcdf/elastnetmt#11`, `uibcdf/elastnetmt#12` |

`pending` means no adoption claim has been made. The matrix is not inferred from current
badge counts and does not turn a syntactically similar existing badge row into adoption.
The initiative column is temporary planning state; it does not alter role, membership or
maturity.

The six adopted READMEs use the generated baseline and the audited conditional order.
SMonitor, ArgDigest, DepDigest and PyUnitWizard retain tokenless current Codecov badges;
MolSysMT and MolSysViewer omit coverage. All six use public documentation targets,
dynamic GitHub Release and package-specific Conda badges. PyUnitWizard, MolSysMT and
MolSysViewer use their verified concept DOI. Hosted policy checks passed for five
members. MolSysViewer truthfully displays its failing policy state; its existing local
issue remains open and the adoption does not claim health.

The remaining three stabilizing READMEs also pass the central offline checker. Their
adoption commits triggered hosted policy and applicable CI/documentation checks; all
runs and job groups inspected by `gh-run-receptor` completed successfully. The
documentation omission for Lindelint is therefore a deliberate evidence boundary, not a
forgotten badge.

## Rollout order

1. Review the central role wording and rendered assets at README scale.
2. Audit the six priority members of the stabilization initiative with the offline checker
   and live evidence queries. **Complete 2026-09-20.**
3. Open a local issue only for a concrete remediation that cannot be applied as the
   mechanical adoption commit itself.
4. Adopt the remaining stabilizing members. **Complete 2026-09-20.**
5. Admit incubating members without fabricating policy, release or documentation health.
   **Complete 2026-09-21.**
6. Add the badge check to the common repository gate only after adoption or explicit
   exceptions cover every registered member. **Complete in `policy-v1.3.0`.**

The rollout must not overlap unrelated release changes in a component README. A badge
commit records only identity and evidence presentation; it does not repair the underlying
CI, release, documentation or archive capability.
