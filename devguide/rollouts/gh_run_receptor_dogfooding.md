# GH Run Receptor controlled-dogfooding rollout

**Issue:** `uibcdf/molsyssuite#19`
**Policy:** `devguide/gh_run_receptor_policy.md`
**Started:** 2026-09-08
**Status:** Active.

## State definitions

`ready` means the registered consumer carries `GH_RUN_RECEPTOR_GUIDE.md` and its
`.github/gh-run-receptor.yaml` passes the current configuration parser. `active` requires
recorded use with repository, run, receptor revision, and outcome. `deferred` means
readiness exists but scheduled use follows the stabilization cohort. No state in this
matrix grants sole release authority.

## Initial readiness audit

Measured locally on 2026-09-08 with Python 3.13.14 and gh-run-receptor development commit
`d98fc2f`. All ten registered consumers carry the guide and a schema-v1 configuration;
`python -m gh_run_receptor.cli config check <path>` accepted every file. Rule counts are
recorded below so that readiness is not inferred from filename presence alone.

| Member | Cohort | State | Rules | Measured use | Current authority |
| --- | --- | --- | ---: | --- | --- |
| smonitor | wave 1 | active | 6 | release run `34278594890` and docs run `34278595009`; provider gap `uibcdf/gh-run-receptor#35`, local fix `uibcdf/smonitor#10` | supplementary |
| argdigest | wave 1 | ready; evidence source | 4 | paired attempts `22638022385` exercised by the provider gate; local operator adoption not measured | supplementary |
| depdigest | wave 1 | ready | 6 | not yet recorded | supplementary |
| pyunitwizard | wave 1 | ready | 7 | not yet recorded | supplementary |
| molsysmt | wave 1 | active | 15 | Conda run `33863123319`: source `success`, receptor `PASS`, 2/2 source jobs matched | supplementary |
| molsysviewer | wave 1 | active | 8 | CI `34212204054`, docs `34126994663`, release `33996342320`: source `failure`, receptor `FAIL`, complete source jobs matched | supplementary |
| pytest-receptor | infrastructure | ready | 3 | not yet recorded | supplementary |
| gh-run-receptor | infrastructure | active | n/a | hosted runs `34167676919`, `34201435368`, and `34213219459` | supplementary |
| topomt | incubating | deferred-ready | 4 | not yet recorded | supplementary |
| pharmacophoremt | incubating | deferred-ready | 3 | not yet recorded | supplementary |
| elastnetmt | incubating | deferred-ready | 4 | not yet recorded | supplementary |

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

`check_vendored_guides.py` passed after publication. These commits prove distribution;
they do not by themselves change any member from `ready` to `active`.

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
