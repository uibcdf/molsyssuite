# GH Run Receptor controlled-dogfooding rollout

**Issue:** `uibcdf/molsyssuite#19`
**Policy:** `devguide/gh_run_receptor_policy.md`
**Started:** 2026-09-08
**Status:** Active.

## State definitions

`ready` means the registered consumer carries `GH_RUN_RECEPTOR_GUIDE.md` and its
`.github/gh-run-receptor.yaml` passes the current configuration parser and its profiles
have been reviewed against GitHub-visible workflow topology. `active` requires recorded
use with repository, run, receptor revision, and outcome. `deferred` means semantic
readiness or live use is scheduled with a later stabilization cohort. No state in this
matrix grants sole release authority.

## Initial readiness audit

Measured locally on 2026-09-08 with Python 3.13.14 and gh-run-receptor development commit
`d98fc2f`. All ten registered consumers carry the guide and a schema-v1 configuration;
`python -m gh_run_receptor.cli config check <path>` accepted every file. Rule counts are
recorded below so that readiness is not inferred from filename presence alone.

| Member | Cohort | State | Rules | Measured use | Current authority |
| --- | --- | --- | ---: | --- | --- |
| smonitor | wave 1 | active | 6 | release run `34278594890` and docs run `34278595009`; provider gap `uibcdf/gh-run-receptor#35`, local fix `uibcdf/smonitor#10` | supplementary |
| argdigest | wave 1 | ready; evidence source | 4 | paired attempts `22638022385` exercised by the provider gate; hidden-matrix rule corrected in `uibcdf/argdigest#10`; local operator adoption not measured | supplementary |
| depdigest | wave 1 | ready | 6 | hidden-matrix rule corrected in `uibcdf/depdigest#9`; live use not yet recorded | supplementary |
| pyunitwizard | wave 1 | ready | 7 | hidden-matrix rule corrected in `uibcdf/pyunitwizard#73`; live use not yet recorded | supplementary |
| molsysmt | wave 1 | active | 15 | Conda run `33863123319`: source `success`, receptor `PASS`, 2/2 source jobs matched | supplementary |
| molsysviewer | wave 1 | active | 8 | CI `34212204054`, docs `34126994663`, release `33996342320`: source `failure`, receptor `FAIL`, complete source jobs matched | supplementary |
| pytest-receptor | infrastructure | ready | 3 | not yet recorded | supplementary |
| gh-run-receptor | infrastructure | active | n/a | hosted runs `34167676919`, `34201435368`, and `34213219459` | supplementary |
| lindelint | auxiliary | ready | 3 | workflow rules and guide synchronized in `ae4e3fc`; live use not yet recorded | supplementary |
| topomt | incubating | deferred | 4 | action-internal matrix correction tracked in `uibcdf/topomt#17` | supplementary |
| pharmacophoremt | incubating | deferred | 3 | action-internal matrix correction tracked in `uibcdf/pharmacophoremt#1` | supplementary |
| elastnetmt | incubating | deferred | 4 | action-internal matrix correction tracked in `uibcdf/elastnetmt#10` | supplementary |

The ArgDigest row is intentionally not `active`: consuming its run from a provider-hosted
gate validates cross-repository evidence handling but does not prove that ArgDigest
developers use the receptor in their own work.

## Guide distribution checkpoint

The policy summary was synchronized byte-identically from the canonical
`MOLSYSSUITE_GUIDE.md` and published in all members on 2026-09-08:

| Member | Synchronization commit |
| --- | --- |
| smonitor | `24841b8` |
| argdigest | `63ac2f4` |
| depdigest | `2e2ac18` |
| pyunitwizard | `77f7be9` |
| pytest-receptor | `da5195f` |
| gh-run-receptor | `3c8c25d` |
| molsysmt | `2124dfccc` |
| molsysviewer | `b3df448a` |
| topomt | `4b78133` |
| pharmacophoremt | `0aaca44` |
| elastnetmt | `cbd41ea` |
| lindelint | `ae4e3fc` |

`check_vendored_guides.py` passed after publication. These commits prove distribution;
they do not by themselves change any member from `ready` to `active`.

Lindelint joined after the initial ten-consumer audit. Its three exact rules classify CI,
documentation, and its action-internal Conda publication as `ci`, `docs`, and `release`;
the current guide and configuration parser were verified locally before `ae4e3fc`.

## Suite-wide profile-topology audit

The SMonitor finding triggered a review of every registered configuration carrying
`expected_platforms`. MolSysMT's requirement remains valid because its staging workflow
exposes platform names in GitHub jobs and artifacts. ArgDigest, DepDigest, and PyUnitWizard
used the same action-internal topology as SMonitor; their rules now select `release` in
commits `4e631f0`, `df5b7cd`, and `a64b51d`. GH Run Receptor 0.19.0 accepted each file and
`config explain` selected the exact release rule. Local regression tests preserve the
decision. These checks prove semantic readiness, not live operator adoption.

TopoMT, PharmacophoreMT, and ElastNetMT have the same incorrect hidden-matrix declaration.
Their corrections are tracked in `uibcdf/topomt#17`, `uibcdf/pharmacophoremt#1`, and
`uibcdf/elastnetmt#10`. They are recorded as `deferred`, rather than `deferred-ready`,
until that simple integration work is scheduled with the incubating cohort. This residue
does not block the first stabilization wave.

## GH Run Receptor 0.19.1 guide checkpoint

Release 0.19.1 is the current admitted routine-use version. Its canonical
`GH_RUN_RECEPTOR_GUIDE.md` was synchronized byte-identically to all eleven registered
consumers after public release verification on 2026-09-08:

| Consumer | Synchronization commit |
| --- | --- |
| smonitor | `c3676d8` |
| argdigest | `647e443` |
| depdigest | `93c35b5` |
| pyunitwizard | `0af6edf` |
| pytest-receptor | `a995c67` |
| molsysmt | `d88e78bfd` |
| molsysviewer | `c9d1da00` |
| topomt | `3597a99` |
| pharmacophoremt | `e356a51` |
| elastnetmt | `92b5922` |
| lindelint | `0963fd1` |

The shared Conda publishing Action, which is a distribution target but not a registered
suite member, received the same guide in `uibcdf/action-build-and-upload-conda-packages`
commit `7936e09`. Provider contract, minimum-GitHub-CLI, and three-operating-system Action
runs `34285137551`, `34285137250`, and `34285137260` passed before public release
`385099198`. Guide synchronization proves current instructions and version selection; it
does not by itself promote any row from `ready` to `active`.

## First wave-1 dogfooding evidence

The first controlled consumer invocations used gh-run-receptor commit `3c8c25d` with each
repository's own default-branch configuration and `capture=metadata`. The structured
reports were compared field by field with `gh run view --json` rather than accepted from
their rendered verdict alone.

- MolSysMT run `33863123319` selected `.github/workflows/test_conda_abi3.yaml` and the
  `conda` profile. Repository, head SHA, `completed`/`success`, and both successful jobs
  matched GitHub exactly; the receptor reported `PASS` with sufficient evidence.
- MolSysViewer run `34212204054` selected `.github/workflows/CI.yaml` and the `ci` profile.
  Repository, head SHA, `completed`/`failure`, and all seven failed jobs matched GitHub
  exactly; the receptor reported `FAIL` with sufficient evidence.
- MolSysViewer run `34126994663` selected `.github/workflows/docs-notebooks.yaml` and the
  `docs` profile. Its failed conclusion, head SHA, and single failed job matched GitHub;
  the receptor reported `FAIL`/exit 1 with sufficient evidence.
- MolSysViewer run `33996342320` selected `.github/workflows/npm-publish.yaml` and the
  `release` profile. Its failed conclusion, head SHA, and single failed job matched
  GitHub; the receptor reported `FAIL`/exit 1 with sufficient evidence.

Together these invocations cover CI, documentation, Conda, and release profiles. No logs
were requested, so they establish compact conclusion and job-inventory parity, not
failure-cause diagnosis. Native inspection remained the independent comparison path.

## SMonitor release dogfooding evidence

SMonitor's 0.14.0 publication supplied the first ordinary wave-1 use after the initial
pilot. Metadata-only inspection of docs run `34278595009` with development commit
`921f434` selected the repository's `docs` profile, matched GitHub's successful
conclusion and 1/1 successful job, and exited 0.

The same revision exposed a real configuration boundary on release run `34278594890`.
GitHub reported `completed`/`success` and three successful Python-matrix jobs, while the
configured Conda profile returned `FAIL` because all four expected native platforms were
absent from GitHub job and artifact names. The workflow delegates its native matrix to a
composite publishing action. Native inspection confirmed the three jobs; the public
Anaconda API independently confirmed 12 SMonitor 0.14.0 distributions covering Python
3.11--3.13 on `linux-64`, `osx-64`, `osx-arm64`, and `win-64`.

The provider capability is tracked in `uibcdf/gh-run-receptor#35`, and the consumer
workaround and regression guard in `uibcdf/smonitor#10`. SMonitor now maps that workflow
to `release`. A repeated metadata-only inspection from exact commit `d959dfe` returned
`PASS`, retained event `release`, ref `0.14.0`, and source SHA
`59bf831cd21cb0608e6f56a3f6d00135f35e2951`, while correctly reporting
`registry=not_observed` and `archive=not_observed`. The external Anaconda query therefore
remained part of the release decision instead of being replaced by receptor output.

## Rollout order

1. Record ordinary inspection in gh-run-receptor and at least one wave-1 component.
2. Exercise CI, documentation, Conda, and release profiles without changing their existing
   approval gates.
3. File provider feedback for every truth, completeness, or output-bound discrepancy and
   cross-link only concrete consumer work.
4. Extend active use through wave 1 and supporting infrastructure.
5. Schedule incubating members when their stabilization work produces representative runs.
6. Evaluate the graduation criteria independently of the package version number.

## Updating the matrix

Change a state only from measured evidence. Record the component, run ID, receptor release
or immutable commit, profile, result, fallback use, and linked provider issue when a
discrepancy occurred. A successful configuration check is readiness evidence; it is not an
adoption event. A compact report that was never compared with the decision-relevant source
facts is usage evidence, not correctness evidence.
