# Informational CI profile pilot

## Scope and decision

The maintainer accepted the informational pilot under `uibcdf/molsyssuite#39`
on 2026-10-04. Its initial registered profiles cover GH Run Receptor, DepDigest
and Ackredit. It adds an inspection mode to the existing central review tool;
member workflows, required checks, caller versions and release gates retain
their current contracts. No shared policy release is introduced by the pilot.

On 2026-11-02 the principal maintainer accepted the prepared informational
extension to Pytest Receptor, SMonitor and ArgDigest. The active default
catalogue at that activation had **six members and thirty-three bound inputs**. Existing
three-member profile definitions are unchanged. The
[activation receipt](rollouts/ci_pilot_extension_adoption_39_20261102.json)
records the decision, exact sources, CLI/control checks and owner notices.
Mandatory enforcement is not part of this acceptance.

On 2026-11-03 the maintainer directed the next independent central expansion.
The catalogue at that delivery contained **nine members and forty-nine bound inputs**,
adding PyUnitWizard, LinDelINT and PeptideMT. Their published configured selections,
root configuration and environments are inspected without importing, collecting
or executing member code. The six previous profile definitions and their actual
reports are unchanged. New profiles opt into bounded collection-hook discovery
below. [Review, compatibility and controls](rollouts/ci_pilot_nine_member_extension_39_20261103.json).
No member response, implementation, required check or scientific run is needed
for these central source observations; member execution/adoption stays separate.

The next maintainer-directed independent review adds the six remaining public
Python members: MolSysMT, MolSysViewer, TopoMT, PharmacophoreMT, ElastNetMT and
DockingMT. The default catalogue now covers **all fifteen public Python members
and 117 bound inputs**. Private OpenCASTp is not silently added to the public
catalogue, and the non-Python MolSys-AI umbrella is not a Python-profile target.
All nine previous profile definitions and complete v1 reports remain unchanged.
[Public-source review, compatibility and controls](rollouts/ci_pilot_public_coverage_39_20261103.json).
No developer reply or component implementation is needed for this inspection.

On 2026-11-04 an explicit source review reconciles four diagnostic deltas from
the first hosted observer: MolSysMT's additive bounded smoke selections,
MolSysViewer's build/license and owner-tracked CI-only Pandas baseline,
PharmacophoreMT's received ArgDigest floor, and DockingMT's administrative test.
Only four reviewed-source references and seven input hashes change. The
fifteen-member/117-input catalogue, all lane/collection/owner declarations,
eleven other complete profiles and prior selection interpretations are preserved.
[Source composition, frozen observation, controls and delivery](rollouts/ci_pilot_source_reconciliation_39_20261104.json).
This deliberate review restores bounded input agreement at the recorded source
snapshots; it does not automatically accept later drift or qualify execution,
runtime/package compatibility, adoption or debt clearance.

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
is an invocation error. No member required CI job invokes this mode. The separate
central informational observer below does not add a member gate.

## Automated public-source observer

The maintainer accepted central automation under #39 on 2026-11-04. The
independent `.github/workflows/observe-ci-profiles.yaml` runs every Monday at
12:23 UTC, on manual dispatch from `main`, and on relevant observer/reader/
transport/catalogue pushes to `main`. It does not run on PRs, dispatch member
jobs, modify repositories or require any member adoption. Its separate job
is not connected to member required checks, publication gates or CI recovery.
The workflow uses Python 3.14, the existing pinned PyYAML parser and read-only
central contents permission, without cross-repository or publication secrets.

Run the same operation locally with the named development Python:

```bash
python devtools/scripts/observe_ci_profiles.py --output NEW_REPORT_DIRECTORY
```

`--profiles` and `--registry` select explicit local input documents;
`--scratch-parent` selects an existing parent for managed temporary projections.
The output directory must be new: existing reports/links are refused. All source
projections are deleted on success or failure; the requested final JSON/Markdown
outputs remain useful caller-owned reports. This acquisition is qualified on
Linux/Python 3.14; it does not establish another platform's scientific behavior.

`public_ci_sources::collect_public_profile` owns public acquisition;
`observe_ci_profiles::observe` orchestrates projections and delegates report
meaning to the unchanged `python_ci_status::inspect_pilot`. It contacts GitHub
anonymously, even when tokens exist in the process environment. Public repository
identity/visibility is checked before obtaining its default-branch commit and
complete immutable recursive tree. Selected raw files are acquired at that full
commit, with no redirects, verified against Git blob identities and SHA-256.
No Git checkout, archive extraction, imports, hooks, package installation or
member command execution occurs. The current catalogue's fifteen public Python
members are selected explicitly; private OpenCASTp and non-Python MolSys-AI are
not implicitly added or diagnosed as noncompliant.

The projection contains bound inputs, existing root pytest configurations and
all hook names in declared collection roots/ancestors. A complete bounded remote
tree checks the original collection entry count and linked/submodule boundaries
before building the smaller projection. Unrelated runtime/scientific data is not
downloaded. Missing bound files remain observed drift. Unsupported entries,
incomplete trees, byte mismatches, private/moved/inaccessible sources and service
failures clear that member's projection, so the reader reports **unknown**.
Other members continue; raw service/exception bodies are never reported.

Resource limits are observer limits, not new component requirements: 8 MiB JSON
transport responses; 25,000 tree entries; 256 fetched files, 1 MiB/file and 8 MiB
per member; the existing 10,000-entry collection bound; and a ten-minute request
start budget plus bounded in-flight HTTP requests. Raw reads use a 20-second
socket timeout; the JSON transport has bounded retry/backoff. Source workflow
preflight bounds aliases/depth/nodes, jobs/steps/scenarios, script size and static
matrix products before calling the reader. A component exceeding these limits
needs observer review, not a workflow rewrite. The central job timeout is
20 minutes. Anonymous API limits can make an observation unavailable; retry in
a later observer run rather than borrowing private credentials or certifying it.

Outputs are `observation.json` (`molsyssuite.ci-profile-observation@1`) and
`summary.md`, retained as the `public-ci-profile-observation` Actions artifact
for 30 days. The envelope contains source acquisition state, immutable branch
snapshot/tree/blob/input hashes, central input/code hashes and the unchanged
pilot report/schema. The hosted central commit is recorded when available.
The summary states explicitly that it is not executed-test, adoption or debt
evidence. Current hashes can preserve a bounded review even at a newer commit;
drift invalidates it without changing the catalogue automatically.

Diagnostic drift/unavailability exits zero after producing the report. Invalid
local catalogues, implementation errors or failed artifact retention fail this
central observer job; they do not become a member test failure. No automatic
issue/reminder, profile acceptance, CI enforcement, source pin, guide/policy
release, package, scientific or platform qualification follows. Closure and
owner dispositions remain separate. Use a qualified immutable central source
and its catalogue together when consuming this optional operation.

## Profile contract

Each profile names a registered Python member, its owning CI review, the
immutable inspected source commit, active workflow/job bindings, required
event/minor targets and inspected full/smoke selection. It binds those statements
to SHA-256 hashes of the workflow, `pyproject.toml` and relevant environment or
backlog inputs. Hash drift or missing input invalidates selection review and
produces `unknown`; retaining the profile does not certify a changed selection.
The profile commit identifies the reviewed source, not a newly executed run.

The #160 correction also invalidates review when an unbound root pytest
configuration appears (`pytest.toml`, `.pytest.toml`, `pytest.ini`, `.pytest.ini`,
`pyproject.toml`, `tox.ini` or `setup.cfg`). Discovery does not parse or execute
unbound contents or infer which configuration wins. Review the selection and
explicitly bind the applicable files before restoring the level; a subset must
retain its reviewed smoke contract. Without the optional collection scope below,
root discovery is not general ancestor, nested-hook, wrapper or runtime/environment
inspection. The
[regression and bounded proof](archive/ci_pilot_unbound_pytest_configuration.md)
preserve those limits and the existing informational mode.

### Optional collection-hook scope

A reviewed profile can declare `collection-roots = ["tests"]`. It names the
actual selected repository-relative directories, not file globs or a policy
requiring every component to use that layout. The three new profiles bind their
real `testpaths` configuration and use this scope, as do the six later public
profiles. Existing profiles without the
field retain their original behavior.

The new catalogue uses `schema-version = 2`; the reader continues to accept
version 1. Collection roots require version 2, so an older reader rejects the
new catalogue instead of silently ignoring its inspection scope. Use the reader
and catalogue from the same delivered central commit. Version 2 profiles without
collection roots preserve their original version 1 report semantics. The report
schema remains `molsyssuite.ci-pilot@1` for reports without scoped selections,
with an optional per-member hook scope. Scoped reports use version 2 below.

The reader inspects `conftest.py` names in the declared trees and their ancestors
inside the repository, including the repository root. Every existing hook needs
an explicitly reviewed input digest. A new unbound hook, a changed/missing bound
hook, a missing tree, a linked tree/hook, or unavailable inspection invalidates
selection review and makes its targets **unknown**. The traversal does not follow
linked directories or import/execute hooks. It accepts 1–16 canonical nonoverlapping
directories and stops after 10,000 directory/file entries per profile; reaching
the bound is unknown, not a claim that no more hooks exist.

This is bounded hook discovery, not a parser for hook behavior, ancestor files
outside the repository, installed pytest plugins, runtime environment variables
or arbitrary wrapper/plugin import closure. Reviewers still own selection scope
and full/smoke classification. Matching inputs do not certify new scientific
code, engine availability or executed collection. A synthetic two-test collection
actually shrinks to one after adding a hook; the new reader rejects such an
unreviewed hook before retaining the selection label. No member tests are used
by that regression.

Full versus smoke is reviewed from the actual selection and owning contract;
it is not inferred from a job name or an isolated pytest command. A smoke
profile needs an owning issue. Its reviewed level can match a permitted push
target while failing to match the full PR target. Runtime source changes and
external dependency resolution still need independent execution evidence.

### Explicit scoped selections and execution context

A catalogue-v2 lane may use `test-level = "scoped"` with bounded nonempty
`selection-context` and an owning `scope-issue`. This describes an explicit
subset that is neither a complete selection nor a smoke exception. It never
matches a `full` or `smoke` target merely because its inputs match. Full/smoke
lanes may also retain optional context text; existing lanes without it keep
their exact report shape. This does not add `scoped` to the member-policy
registry's allowed routine levels, grant an exception or change adoption.

Reports containing scoped lanes use **`molsyssuite.ci-pilot@2`**, including when
their inputs drift and the observed state is unknown. The prior report schema
and complete reports remain identical for the earlier nine profiles. Older
catalogue-v2 readers reject the new scoped level instead of silently treating
it as full; use the reader/catalogue from the same immutable delivery.

The Viewer ordinary CI explicitly excludes `qt_runtime`; its core report is
scoped and retains owner #93. The separate experimental Qt workflow remains
outside this profile and the #57 deferral is unchanged. This annotation neither
introduces a Qt gate nor negates a previous bounded owner acceptance.
MolSysMT separately retains its explicit smoke, static full PR matrix and
unresolved dynamic weekly matrix. Its opt-in parity selection and source-pair
conditions remain explicit context, not a universal scientific-completeness
claim. ElastNetMT's neutral copied tests use their copied pyproject configuration;
builder/native/archive outcomes remain unexecuted prerequisites. TopoMT's package
doctests, owner-specific environments and early maturity are preserved, as are
PharmacophoreMT's environments and DockingMT's coverage-only matrix options.

Context is explanatory inspected evidence, not execution of shell, callbacks,
generated matrices, installed plugins, optional engines or scientific code.
Unknown dynamic cells remain unknown even when the configured command is full.

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

The 2026-10-04 inspected DepDigest/Ackredit workflows distinguished these routes:

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

### Explicit cancellation facts — 2026-11-12

Under `uibcdf/molsyssuite#177`, `condition_outcome`, `scenario_matrix` and
`inspect_event_routes` accept keyword-only `cancelled: bool | None = None`.
This is a caller-supplied hypothetical workflow fact, not a synthetic GitHub
context property or a job-result inference. Only actual booleans are accepted;
integers, strings and other types raise `ValueError`. `None` leaves
`cancelled()` unknown. Event names and `needs.*.result` never supply that fact.

| Supplied fact | `cancelled()` | `!cancelled()` |
| --- | --- | --- |
| `False` | false | true |
| `True` | true | false |
| omitted / `None` | unknown | unknown |

For example:

```python
from devtools.scripts.ci_lane_inventory import condition_outcome

assert condition_outcome("!cancelled()", "workflow_dispatch") is None
assert condition_outcome("!cancelled()", "workflow_dispatch", cancelled=False) is True
assert condition_outcome("!cancelled()", "workflow_dispatch", cancelled=True) is False
```

Supplying a boolean opts into the existing bounded scenario mode even without
a context mapping; `always()` remains true in that mode, including during
cancellation. Calls without the new fact retain their earlier event-only or
explicit-context behavior. Only zero-argument `cancelled()` is added to the
supported calls; `success()`, `failure()` and arbitrary expressions remain
unsupported. Known boolean short-circuits retain three-valued outcomes. Matrix
operand selection retains its stricter unknown/unavailable-branch and call
validation rules; missing facts never become a passing or invented matrix cell.

`scenario_matrix(matrix, event, context, cancelled=...)` uses the same fact for
conditional JSON selection. `inspect_event_routes(document, test_job,
cancelled=...)` propagates it to configured route job predicates, direct needs,
test-step predicates and matrix observations. Explicit reports retain
`cancelled` at route level; omitted/`None` calls preserve the previous report
shape. Call separately with `False` and `True` to compare those hypotheses;
this does not expand every input combination or add observed execution history.
The ordinary CLI/pilot remains unchanged and never assumes noncancellation.

This matches the bounded distinction in GitHub's
[status-function semantics](https://docs.github.com/en/actions/reference/workflows-and-actions/expressions#status-check-functions)
and [cancellation procedure](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-cancellation).
The reader does not model implicit success checks, job admission, preceding
steps, server reevaluation, runner signals, dependency state or force-cancellation.
`execution_evidence = "not_requested"` and `dependency_status = "not_evaluated"`
remain explicit. No workflow, SDK pin, pilot classification, required gate or
scientific receiving is changed. PharmacophoreMT #169 retains its independently
delivered cancellable workflow and any later observer adoption.

### Bounded scenario matrices — 2026-11-04

`ci_lane_inventory::scenario_matrix(matrix, event, context)` adds an optional
`matrix` observation to each available job in `event_routes`. Its `status` is
`none`, `static`, `resolved` (a supported `fromJSON` expression), or `unresolved`.
`combinations` contains configured source cells; unresolved input returns an
empty list, never a synthetic passing cell. An absent matrix has one empty combination.
Text output shows the status/count and the resolved dynamic combinations.
This is an additive observation in the existing report schemas; the catalogue,
aggregate targets, selection review and execution/debt fields retain their
meanings. Older readers simply lack this optional scenario observation.

The bounded reader supports whole-matrix and axis-level `fromJSON` with JSON
literals or known scenario string facts, and branch selection using supported
event/input predicates. It preserves Actions operand-returning `&&`/`||`,
single-quote escaping, truthiness and the existing string/boolean equality
rules; it does not use Python `eval` or execute workflow code. Missing facts,
unsupported syntax/functions and ambiguous branches remain unknown. Supported
known short-circuits can select a branch without needing irrelevant facts.
See [GitHub's expression contract](https://docs.github.com/en/actions/reference/workflows-and-actions/expressions).

Inspection rejects malformed/duplicate-key/nonfinite JSON, nested Actions
expressions, empty axes and unsupported shapes. Bounds are 32,768 characters
per expression/string, 512 expression AST nodes, 16 matrix nesting levels,
4,096 structure nodes, 22 matrix keys and 256 prospective combinations including
additive include entries. Unknown/over-limit cases remain `unresolved`; these
are observer limits, not new component CI requirements. Include/exclude uses
the same existing static expansion semantics. The event-only aggregate reader
deliberately continues to leave dynamic matrices unknown.

For the unchanged published MolSysMT weekly workflow, scheduled routes and
manual defaults configure five cells (Linux/Python 3.11–3.14 and macOS/Python
3.14); the explicit `python_313_only=true` scenario configures only Linux/3.13.
The recovery-probe scenario still describes five source cells while its test
predicate is false. Missing detector results keep other job predicates unknown.
Configured cells do not establish job admission, executed tests, a passing full
matrix, debt clearance or platform qualification. Each scenario retains its
`profile_inputs_current`; a matrix observed after drift cannot reuse review.

[Source, compatibility and regression receipt](rollouts/ci_pilot_scenario_matrices_39_20261104.json).
All fifteen previous complete reports are equal after removing only this
additive job field. No member tests or jobs are run, no caller/catalogue/required
gate is changed, and no developer reply or component modification is requested.

The dated second observation and its source/administrative verification are in
`devguide/rollouts/ci_pilot_routes_39_20261004.json`. Its 39 focused tests include
the original 31 and eight routing regressions; member workflows and scientific
suites were not changed or dispatched.

### Refreshed source observation — 2026-10-22

The existing three-member pilot now binds DepDigest `41075197307a933c80197f419093342ef5abcec0`,
GH Run Receptor `c60ed4f55e8f7160486cda8c6083a5b40933e309` and Ackredit
`b2af6c45296a3421c7a3f2f2ed7491021c0b77cf`. All thirteen bound inputs match.
GH Run Receptor and Ackredit retain their previous input bytes. DepDigest's
three changed inputs were reviewed semantically: documentation URL, preflight
SDK pins, four macOS runner labels and the full-matrix cancellation predicate.
Test selections, matrix minors, events/manual defaults, recovery detector and
gating flags otherwise retain their reviewed structure.

DepDigest now uses `!cancelled()` instead of `always()` in its full-matrix
job condition. The parser leaves that function unknown without runtime facts;
weekly, daily and manual-full predicates are therefore unknown. Its explicit
`probe_backlog = true` still proves that the test-job predicate is false.
The earlier table remains a dated observation, not the current DepDigest result.
Ackredit's configured predicates retain the earlier interpretation. Aggregate
target states remain GH Run Receptor 11 configured, DepDigest 2 configured/9
conditional and Ackredit 3 configured/8 conditional.

Forty focused central pilot/event/inventory/policy tests pass with Pytest
Receptor. The new regression protects unknown cancellation facts and the
provable probe exclusion without changing the parser. The normalized source,
route, test and owner-notice evidence is in
`devguide/rollouts/ci_pilot_refresh_39_20261022.json`. Member execution, dependency
status, skipped-debt clearance and receiving approval are not inferred. This
refresh retains the same informational cohort and does not enable enforcement.

### Refreshed source observation — 2026-11-02

The same cohort now binds DepDigest `9dc562144b6fed9d6408ac9b64997c8636b1ccbe`,
GH Run Receptor `08bad8de95a70c31ea5f0c25b10d83d7457932d1` and Ackredit
`4beb850c8ba814e6103b4d303128a1a36eb57610`. Ten DepDigest/Ackredit inputs
remain identical. GH Run Receptor's reviewed changes introduce the `src/`
layout, importlib import mode, scope markers and the already accepted SDK ref.
Whole parsed configuration equality after those precise changes confirms that
the unfiltered pytest selections, event routes and matrices are preserved.

GH Run Receptor now classifies and audits collected tests. The profile binds
`tests/conftest.py` and `gh_run_receptor_tools/test_inventory.py` as two additional
selection inputs, bringing the cohort total to fifteen. They add labels or
reject inconsistent inventories; they do not deselect tests. The classification
JSON's exact hash and 446 active function records are retained as review context,
not a selection input: neither full invocation filters those labels. Changes to
the hook/auditor code invalidate review; ordinary additional test records need
not invalidate it. A controlled hook mutation makes all eleven GH Run Receptor
targets unknown; original bytes are restored afterwards.

The real informational CLI and forty focused central tests pass. Aggregate
observations remain DepDigest 2 configured/9 conditional, GH Run Receptor 11
configured and Ackredit 3 configured/8 conditional. Unknown cancellation facts
remain unknown. The [dated receipt](rollouts/ci_pilot_refresh_39_20261102.json)
retains immutable inputs, semantic review, scenarios and controlled drift.
These are source observations, not new member runs, owner acceptance or
skip-debt clearance. No parser, member workflow or enforcement is changed.

### Accepted extension — 2026-11-02

The principal maintainer accepted the reviewed three-to-six recommendation.
`devtools/ci_pilot_profiles.toml` now activates Pytest Receptor, SMonitor and
ArgDigest alongside DepDigest, GH Run Receptor and Ackredit. The
[original proposal catalogue](rollouts/ci_pilot_expansion_candidate_39_20261102.toml)
and [source review](rollouts/ci_pilot_expansion_review_39_20261102.json) retain
their pre-decision provenance; current adoption is recorded in the
[separate activation receipt](rollouts/ci_pilot_extension_adoption_39_20261102.json).
The active profile definitions match that reviewed catalogue, with all thirty-three
inputs verified against their original and current published source bytes.

The actual default command returns six members, and the explicit member selector
works. Forty-three focused central tests pass. A new unbound root pytest
configuration in the SMonitor projection invalidates its eleven target reviews
while preserving the other five. Combining the pilot with `--require-adopted`
continues to fail as an invocation error. No parser or member implementation changes.

The extension adds useful variation: Pytest Receptor's serial/distributed
Python/pytest-major combinations, SMonitor's local branch-coverage threshold,
and ArgDigest's full/core dependency environments. Those remain owner contracts.
The central Linux/minor/event view does not independently qualify every extra
matrix axis, optional dependency, local quality gate or passing run. Existing
unknown predicates, execution/debt boundaries and informational-only behavior
are retained. Further cohort expansion or mandatory enforcement still requires
its own explicit reviewed decision; #39 retains the remaining adoption scope.
