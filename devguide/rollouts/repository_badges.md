# Repository badge and role-identity rollout

**Issue:** `uibcdf/molsyssuite#23`

**Policy candidate:** `devguide/repository_badges.md`

**Started:** 2026-09-20

**Status:** Central phase complete; component adoption has not started.

## Central checkpoint

The central phase accepts three roles, records one role for every registered
member, provides accessible SVG identity assets, generates canonical baseline snippets
from `suite.toml`, and validates locally provable README claims. No component README was
changed during this phase.

Network-only claims remain outside the offline validator. A later audit must verify live
workflow, coverage, documentation, release, DOI and package surfaces before conditional
badges are treated as current evidence.

## Adoption matrix

| Member | Role | Membership | Maturity | Stabilization priority | State | Local issue |
| --- | --- | --- | --- | --- | --- | --- |
| smonitor | support library | primary | stabilizing | yes | pending | — |
| argdigest | support library | primary | stabilizing | yes | pending | — |
| depdigest | support library | primary | stabilizing | yes | pending | — |
| pyunitwizard | support library | primary | stabilizing | yes | pending | — |
| molsysmt | scientific component | primary | stabilizing | yes | pending | — |
| molsysviewer | scientific component | primary | stabilizing | yes | pending | — |
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

## Rollout order

1. Review the central role wording and rendered assets at README scale.
2. Audit the six priority members of the stabilization initiative with the offline checker and live
   evidence queries.
3. Open a local issue only for a concrete remediation that cannot be applied as the
   mechanical adoption commit itself.
4. Adopt the remaining stabilizing members.
5. Admit incubating members without fabricating policy, release or documentation health.
6. Add the badge check to the common repository gate only after adoption or explicit
   exceptions cover every registered member.

The rollout must not overlap unrelated release changes in a component README. A badge
commit records only identity and evidence presentation; it does not repair the underlying
CI, release, documentation or archive capability.
