# Repository badge and role-identity rollout

**Issue:** `uibcdf/molsyssuite#23`

**Policy:** `devguide/repository_badges.md`

**Started:** 2026-09-20

**Status:** Central phase, stabilization-priority audit and priority-member adoption
complete; remaining members are pending.

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

## Adoption matrix

| Member | Role | Membership | Maturity | Stabilization priority | State | Local issue |
| --- | --- | --- | --- | --- | --- | --- |
| smonitor | support library | primary | stabilizing | yes | adopted `ecc1164` | — |
| argdigest | support library | primary | stabilizing | yes | adopted `d1f1180` | — |
| depdigest | support library | primary | stabilizing | yes | adopted `544fd00` | — |
| pyunitwizard | support library | primary | stabilizing | yes | adopted `4be1c4c` | — |
| molsysmt | scientific component | primary | stabilizing | yes | adopted `f1c6ae39c` | `uibcdf/molsysmt#185` |
| molsysviewer | scientific component | primary | stabilizing | yes | adopted `76d33be5` | `uibcdf/molsysviewer#88` |
| pytest-receptor | developer tool | primary | stabilizing | no | pending | — |
| gh-run-receptor | developer tool | primary | stabilizing | no | pending | — |
| lindelint | developer tool | auxiliary | stabilizing | no | pending | — |
| topomt | scientific component | primary | incubating | no | pending | — |
| pharmacophoremt | scientific component | primary | incubating | no | pending | — |
| elastnetmt | scientific component | primary | incubating | no | pending | required for stale `enmmt/master` targets |

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

## Rollout order

1. Review the central role wording and rendered assets at README scale.
2. Audit the six priority members of the stabilization initiative with the offline checker
   and live evidence queries. **Complete 2026-09-20.**
3. Open a local issue only for a concrete remediation that cannot be applied as the
   mechanical adoption commit itself.
4. Adopt the remaining stabilizing members.
5. Admit incubating members without fabricating policy, release or documentation health.
6. Add the badge check to the common repository gate only after adoption or explicit
   exceptions cover every registered member.

The rollout must not overlap unrelated release changes in a component README. A badge
commit records only identity and evidence presentation; it does not repair the underlying
CI, release, documentation or archive capability.
