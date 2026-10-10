---
summary: Track hosted cross-repository audits blocked while OpenCASTp is temporarily private.
issue: uibcdf/molsyssuite#102
status: partial
opened: 2026-10-04
closed:
severity: medium
verification: reproduced
area: [governance, automation, compatibility]
guard:
normative:
blocked_by: []
supersedes: []
---

# Hosted audits cannot read a temporarily private member

## What

The maintainer confirms OpenCASTp's private visibility is intentional and
temporary. The five cross-repository audits triggered by registry commit
`a3a376e451a0882e209cdc3af0787d1e59ee8198` fail acquiring that registered
source or its labels. Central governance passes independently. No scientific
or component implementation defect is inferred from these access failures.

## How

GitHub's authenticated repository metadata reports `uibcdf/opencastp` private.
Published GH Run Receptor 1.2.0 first inspects the failed native runs; their
failed-step logs corroborate the access limitation:

| Audit | Native run | Executed failure |
| --- | --- | --- |
| Component labels | [37230243819](https://github.com/uibcdf/molsyssuite/actions/runs/37230243819) | Repository-scoped token cannot resolve OpenCASTp. |
| Vendored guides | [37230243826](https://github.com/uibcdf/molsyssuite/actions/runs/37230243826) | Unauthenticated clone cannot acquire HTTPS credentials. |
| Joint development environment | [37230243818](https://github.com/uibcdf/molsyssuite/actions/runs/37230243818) | Same source-fetch failure before installation/runtime qualification. |
| Component guides | [37230243839](https://github.com/uibcdf/molsyssuite/actions/runs/37230243839) | OpenCASTp checkout returns Not Found. |
| Dependency manifests | [37230243829](https://github.com/uibcdf/molsyssuite/actions/runs/37230243829) | OpenCASTp checkout returns Not Found. |

At reproduction, source-fetch jobs used unauthenticated clones or the central
repository's checkout token; labels used its `GITHUB_TOKEN`. No cross-repository
read secret was then configured. Private-member access is not implied by
registered membership or a past successful joint-environment receipt.

## Why

Removing the member or claiming these unexecuted checks pass would misstate
coverage. Changing a private repository's visibility is a maintainer decision.
The intentional temporary restriction remains; current access failures stay
visible until their recovery is executed and verified.

## Accepted temporary scope and recovery

Responsible maintainer: LMMV. Review by 2026-10-11. Keep OpenCASTp registered
and private, and track the five audits as pending due to access. This is a
temporary availability limitation, not a successful audit, joint integration
or waiver of admission/release gates.

When public visibility returns, execute and inspect the five affected audits
against a recorded central head, including actual joint source/install/runtime
checks. If privacy lasts longer, explicitly review a narrowly scoped read
credential route. The initial provisional decision created no credential and
changed no visibility or audit coverage. The 2026-10-10 authorization below
supersedes its access-route deferral; historical failures remain visible.

## Acceptance criteria

- Preserve the access-failure runs and central/member ownership links.
- Resolve temporary access through the maintainer's chosen route.
- Execute and inspect the five affected audits on a recorded central head.
- Retain failed, skipped or unavailable member checks as such until recovery.

## Local implementation issues

uibcdf/molsyssuite#82 owns joint development evidence;
uibcdf/molsyssuite#39 owns the independent CI review;
uibcdf/opencastp#3 owns the component's CI review. No component source repair
is requested by this central access record.

## Provenance

2026-10-04, Linux; administrative native GitHub metadata/log inspection with
published GH Run Receptor 1.2.0. No private source is copied into this public
record. No scientific suite, credential mutation or visibility change occurs.

## Policy 1.5.9 guide recovery — 2026-10-08

MolSysMT's public Python/ecosystem qualification is frozen at
`3116b7d9f1fa9ba4d09b81a8f24a22b749805f9f` by `policy-v1.5.9`. The
central governance gate `37741900682` passes. Fresh environment audit
`37741900635` again stops at the OpenCASTp source fetch before solving or
installation; label audit `37741900657` cannot resolve that member, and
dependency audit `37741900673` cannot check out its source. Guide audits
`37741900672`/`37741900945` retain the same unavailable acquisition boundary.

The official tool independently verifies all fifteen accessible guide
consumers at their published current main revisions. OpenCASTp's sixteenth
copy remains **unavailable**; its intentionally dirty primary was preserved
and no source/access/visibility change was made. When access returns, run
`sync_vendored_guides.py` for its registered `MOLSYSSUITE_GUIDE.md` relationship
from the current canonical source, then execute the five recovery audits on
a recorded central head. The original LMMV ownership and 2026-10-11 review
remain unchanged. The receipt is
[MolSysMT receiving and policy delivery](../rollouts/molsysmt_python314_ecosystem_51_20261008.json).

## Authorized fine-grained read route — 2026-10-10

The maintainer chose a fine-grained PAT selecting `uibcdf/opencastp` with
Contents/Issues read and confirmed creating Actions secret
`SUITE_REPOSITORIES_READ_TOKEN`. Native secret metadata confirms its presence
(not its value, permissions or expiration). No key is retrieved, printed or
committed; no repository visibility changes.

The five workflows now use the secret on trusted `main` only. Matrix source
checkouts do not persist credentials. Raw clones use the registered-HTTPS
helper in `devtools/scripts/repository_read_access.py`; installation/import
commands do not receive the acquisition secret. Private command stdout/stderr
and exception details are discarded without changing failure status. Public
environment artifacts contain only actual step results plus allowlisted
registered source identities/immutable commits, never raw private metadata.

PRs run offline label/profile regression checks and explicitly lack private
hosted integration evidence; they receive no PAT or private sources. This is
an authentication boundary, not full-suite debt clearance or public admission.
The reusable operation/receipt contract is documented in `devtools/README.md`.

The regression guard is `tests/test_repository_read_access.py`: real Git
credential-protocol checks reject foreign hosts/paths, never store a token or
fall back to cached credentials; real child-command checks discard private
stdout/stderr and preserve nonzero failures; receipt tests reject unknown
identities and strip private metadata. Workflow checks protect trusted-main
credential routes and bounded artifact paths.

Local Python 3.14.7 verification selected 17 audit/profile/label tests, all
passing. Existing seven workspace dependency conflicts remain accepted under
uibcdf/molsyssuite#82. Fresh native recovery of all five audits is pending;
this record remains partial until their actual acquisition/check outcomes are
inspected. LMMV owns PAT renewal/revocation; its undisclosed expiration is not
inferred from GitHub secret metadata. Scientific and release gates remain
component-owned and unchanged.
