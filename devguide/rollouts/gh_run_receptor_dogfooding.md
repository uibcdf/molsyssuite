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
| smonitor | wave 1 | ready | 6 | not yet recorded | supplementary |
| argdigest | wave 1 | ready; evidence source | 4 | paired attempts `22638022385` exercised by the provider gate; local operator adoption not measured | supplementary |
| depdigest | wave 1 | ready | 6 | not yet recorded | supplementary |
| pyunitwizard | wave 1 | ready | 7 | not yet recorded | supplementary |
| molsysmt | wave 1 | ready | 15 | not yet recorded | supplementary |
| molsysviewer | wave 1 | ready | 8 | not yet recorded | supplementary |
| pytest-receptor | infrastructure | ready | 3 | not yet recorded | supplementary |
| gh-run-receptor | infrastructure | active | n/a | hosted runs `34167676919`, `34201435368`, and `34213219459` | supplementary |
| topomt | incubating | deferred-ready | 4 | not yet recorded | supplementary |
| pharmacophoremt | incubating | deferred-ready | 3 | not yet recorded | supplementary |
| elastnetmt | incubating | deferred-ready | 4 | not yet recorded | supplementary |

The ArgDigest row is intentionally not `active`: consuming its run from a provider-hosted
gate validates cross-repository evidence handling but does not prove that ArgDigest
developers use the receptor in their own work.

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
