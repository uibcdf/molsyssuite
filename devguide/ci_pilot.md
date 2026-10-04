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
In the aggregate lane view, scheduled/manual conditions in DepDigest and Ackredit
reference recovery outputs and probe inputs and remain `conditional`. The
scenario view below distinguishes their concrete predicates. Branch protection,
API history uncertainty, executed watermarks, dependency closure, scientific
results, public artifacts and non-Linux architecture claims remain independent.

### Configured event scenarios

The next pilot slice adds `event_routes` to the JSON report and scenario lines
to text output. Aggregate lane states retain their event-only interpretation.
Each bound workflow now displays individual configured cron triggers, declared
manual defaults and a change to each declared boolean input. The latter changes
one input at a time; it is not an exhaustive combination or API history review.
The reusable operations are `ci_lane_inventory::inspect_event_routes` and
`ci_lane_inventory::condition_outcome`.

For each scenario, the bound test job and its direct dependencies retain their
raw conditions and predicate outcomes (`true`, `false`, or unknown). Known
string/boolean facts, grouping, negation, equality and `always()` are supported.
Unsupported functions, dynamic references and missing facts stay unknown;
neither operation executes expression or shell code. Typed defaults and
nonexistent schedule input properties follow [GitHub's context contract](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts#inputs-context);
empty properties, loose equality and `always()` follow its
[expression contract](https://docs.github.com/en/actions/reference/workflows-and-actions/expressions).

A true predicate is not runnable or successful job evidence: implicit success
checks, preceding setup/test steps, upstream results and workflow admission are
independent. `dependency_status = "not_evaluated"` and
`execution_evidence = "not_requested"` remain explicit. Selection-input drift
sets each scenario's `profile_inputs_current` to false; observed predicates in
changed files cannot reuse the selection review. No source hash, adoption state
or lane result is automatically upgraded.

The inspected DepDigest/Ackredit workflows distinguish these routes:

| Scenario | Test-job predicate | Decision-job predicate |
| --- | --- | --- |
| Weekly cron | true | false |
| Manual defaults (`probe_backlog = false`) | true | false |
| Manual debt probe (`probe_backlog = true`) | false | true |
| Daily recovery, detector result unavailable | unknown | true |

The daily result is not inferred from the presence of the cron or detector.
Bounded API tests separately supply hypothetical detector facts: successful
zero debt suppresses the matrix; debt or a failed detector permits it. Those
fixtures do not establish actual debt, a run outcome or a recovery watermark.
The source scenarios supplement the existing owner-reviewed routing evidence.

The dated second observation and its source/administrative verification are in
`devguide/rollouts/ci_pilot_routes_39_20261004.json`. Its 39 focused tests include
the original 31 and eight routing regressions; member workflows and scientific
suites were not changed or dispatched.

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
