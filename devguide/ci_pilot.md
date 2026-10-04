# Informational CI profile pilot

## Scope and decision

The maintainer accepted the informational pilot under `uibcdf/molsyssuite#39`
on 2026-10-04. Its initial registered profiles cover GH Run Receptor, DepDigest
and Ackredit. It adds an inspection mode to the existing central review tool;
member workflows, required checks, caller versions and release gates retain
their current contracts. No shared policy release is introduced by the pilot.

The implementation is `devtools/scripts/python_ci_status.py::inspect_pilot`.
It calls the existing `ci_lane_inventory` operations for configured job/event
and matrix facts. Their bounded command reader recognizes direct pytest and
`python -m coverage run ... -m pytest`, including the actual GH Run Receptor
coverage producer. It does not run shell code or follow arbitrary wrappers.

## Use

Refresh and inspect the registered local clones using `suite_status.py` before
cross-repository review. With the verified Python 3.14 development interpreter,
run from the central clone:

```bash
python devtools/scripts/python_ci_status.py --pilot WORKSPACE
python devtools/scripts/python_ci_status.py --pilot WORKSPACE --format json
python devtools/scripts/python_ci_status.py --pilot WORKSPACE \
  --repository uibcdf/ackredit --format json
```

`WORKSPACE` contains the member clones named in `suite.toml`. The tool performs
local reads; it does not fetch, install, dispatch tests or mutate repositories.
The default profile source is `devtools/ci_pilot_profiles.toml`; `--profiles`
can select an explicit reviewed source for a separate inspection. The report
names that source. A member outside its declared profiles is not silently added.

The normal `python_ci_status.py` review/status interface is preserved. Pilot
mode refuses `--require-adopted`. It exits zero after producing a diagnostic
report, including unknown or missing observations; malformed profile/CLI input
is an invocation error. No central or member required CI job invokes this mode.

## Profile contract

Each profile names a registered Python member, its owning CI review, the
immutable inspected source commit, active workflow/job bindings, required
event/minor targets and inspected full/smoke selection. It binds those statements
to SHA-256 hashes of the workflow, `pyproject.toml` and relevant environment or
backlog inputs. Hash drift or missing input invalidates selection review and
produces `unknown`; retaining the profile does not certify a changed selection.
The profile commit identifies the reviewed source, not a newly executed run.

Full versus smoke is reviewed from the actual selection and owning contract;
it is not inferred from a job name or an isolated pytest command. A smoke
profile needs an owning issue. Its reviewed level can match a permitted push
target while failing to match the full PR target. Runtime source changes and
external dependency resolution still need independent execution evidence.

To extend or refresh a profile, inspect the owner workflow/selection and
receiving evidence, then update the central profile with its issue and immutable
inputs. Use the existing impact issue and notify affected owners. Do not merely
replace a mismatched hash to suppress a finding. Another cohort or mandatory
enforcement needs an explicit reviewed rollout decision.

## Reading the report

| Lane state | Meaning |
| --- | --- |
| `configured` | The bound workflow exposes the requested Linux/minor/event cell with an observed test invocation and known gating/job-step eligibility. Reference filters are retained for receiving review. |
| `conditional` | A relevant cell exists, but its conditions or path filters prevent a guaranteed observation in the inspected event context. |
| `non_gating` | The observed tests tolerate failures; they are not a required passing lane. |
| `not_observed` | No requested static cell was observed, or its known condition excludes execution. This is a bounded finding, not a repository-wide verdict. |
| `unknown` | Profile drift, unavailable input, dynamic matrix, wrapper/reusable route or unresolved interpreter prevents a supported observation. |

`reviewed_test_level` and `reviewed_level_matches_target` describe selection
review separately from those lane states. Neither is an executed full-suite
result. `prior_hosted_review` retains existing review links; the tool does not
refresh or certify them. `execution_evidence = "not_requested"` and
`backlog_clearance = "not_evaluated"` prevent reuse as a passing execution or
skip-debt watermark.

Cron expressions/time zones are displayed, not certified for weekly cadence.
The scheduled/manual conditions in DepDigest and Ackredit reference recovery
outputs and probe inputs; they intentionally remain `conditional` until their
specific trigger/input semantics are modelled and tested. Branch protection,
API history uncertainty, executed watermarks, dependency closure, scientific
results, public artifacts and non-Linux architecture claims remain independent.

## First observation and verification

`devguide/rollouts/ci_pilot_39_20261004.json` retains the first report and its
administrative environment scope. All three profile input sets match.

| Member | Configured target cells | Conditional target cells |
| --- | --- | --- |
| GH Run Receptor | 11 | 0 |
| DepDigest | 2 | 9 |
| Ackredit | 3 | 8 |

These are event/minor observations, not job runs or compliance scores.
The 31 focused pilot/inventory/CI-policy tests pass on Python 3.14.7 with
published Pytest Receptor. They cover coverage-wrapped pytest, comment-only
versions, excluded minors, skipped/tolerated/filtered tests, dynamic and opaque
routes, selection drift and smoke/full separation. No scientific suite was run.

The named joint environment is qualified by existing hosted evidence but is
absent locally. This administration-only slice uses the existing compatible
Conda Python 3.14 environment after interpreter, dependency and owning module
origin checks. Its bounded scope, responsible maintainer, review date and exit
condition are in the receipt; it is not joint source/runtime qualification.
