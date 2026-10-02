---
summary: Develop structured workflow timeout evidence after gh-run-receptor 1.0.
issue: uibcdf/molsyssuite#25
status: open
opened: 2026-09-19
closed:
verification: measured
area: [tooling, ci, governance]
guard:
normative:
blocked_by: []
supersedes: []
---

# Structured workflow timeout evidence is missing

**Reported:** 2026-09-19, while closing the only absent authentic outcome in the
gh-run-receptor 1.0 corpus.
**Status:** Design review resumed on 2026-10-02. GH Run Receptor 1.0 is published;
producer ownership still requires the maintainer decision below before implementation
or component admission.

## What

Evaluate a reusable producer of structured operation-timeout evidence for GitHub Actions.
The producer would let a cooperating workflow distinguish a deadline enforced around a
known command from manual cancellation, matrix fail-fast, concurrency cancellation, or
runner loss. gh-run-receptor and other consumers could report that producer fact without
overwriting GitHub's authoritative workflow-run conclusion.

The proposal does not yet accept a repository name or a new MolSysSuite component. Its
first decision is whether the capability belongs in gh-run-receptor, in a small separate
Action, or as an interoperability contract implemented by existing timeout Actions.

## How

The provisional MVP has four boundaries:

1. A command-owning Action or adapter enforces a caller-selected deadline shorter than
   the enclosing GitHub job timeout.
2. Before returning its timeout exit status, it writes a bounded versioned event such as
   `producer-outcome@1` with repository, run, attempt, job, operation, deadline, elapsed
   duration, terminal reason, and producer identity.
3. A following `if: always()` step publishes that file through a commit-pinned artifact
   action. Consumers verify artifact identity, digest, schema, source run/attempt, and
   producer provenance before accepting it as a producer assertion.
4. Renderers keep both layers visible, for example:

```text
CANCELLED source | producer_timeout operation=tests limit=20m
```

`producer_timeout` is deliberately not `TIMED_OUT`. The latter remains reserved for an
exact GitHub source conclusion. A producer event cannot rewrite run, job, or step truth.

The event contract should be useful beyond gh-run-receptor: a JSON Schema, deterministic
examples, bounded fields, explicit unknown-value behavior, and no MolSysSuite repository
names in the runtime model. Linux, macOS, and Windows process termination must be tested
separately; killing a shell without terminating its child process tree is not sufficient.

## Why

MolSysSuite runs long and expensive Conda builds, scientific tests, documentation jobs,
and multi-operating-system matrices. A generic GitHub `cancelled` result cannot establish
whether a controlled operation exceeded its budget, a user cancelled the run, concurrency
replaced it, or another matrix job triggered fail-fast. Structured timeout provenance
would improve diagnosis, retry targeting, resource accounting, and token-efficient agent
reports in MolSysMT, MolSysViewer, and supporting tools.

The need is not MolSysSuite-specific. GitHub exposes `timed_out` as a workflow-run filter
and check conclusion, while its workflow syntax defines `timeout-minutes` as automatic
cancellation. Existing community Actions can enforce command timeouts, but the inspected
ones primarily expose step outputs or retry behavior. A portable, versioned evidence
artifact tied to source identity could serve any CI consumer, dashboard, or coding agent.

## What is measured and what is assumed

Measured in `uibcdf/gh-run-receptor#45` on 2026-09-19:

- GitHub's documented `timeout-minutes` behavior and repository-owned run `34027741137`
  both produced cancellation rather than a `timed_out` workflow run;
- an authenticated scan of 889 deduplicated public repositories across ten popularity,
  language, Actions-topic, and organization cohorts returned zero request errors and zero
  `status=timed_out` runs;
- gh-run-receptor now preserves an exact synthetic source value through assessment,
  rendering, and process status without claiming an authentic fixture.

A bounded prior-art review found:

- [`nick-fields/retry`](https://github.com/nick-fields/retry) enforces cross-platform
  command deadlines, distinguishes timeout/error retry modes, and exposes attempts, exit
  code, and error as step outputs;
- [`Wandalen/wretry.action`](https://github.com/Wandalen/wretry.action) applies a timeout
  across retries and exposes an output JSON map; and
- community retry-command Actions may return exit status 124, but at least one documents
  that the underlying process may continue until the runner terminates it.

The review did not identify a versioned, source-bound timeout evidence artifact designed
for independent consumers. That is a bounded search result, not a claim that no such tool
exists. A broader prior-art and maintainer-collaboration review is required before code.

It is assumed, not yet measured, that at least two MolSysSuite workflow families can place
the controlled deadline early enough to emit and upload evidence before GitHub cancels the
job. The pilot must test that assumption.

## Alternatives and refuted paths

- Parsing or requesting a printed `TIMED_OUT` marker is rejected. Logs are untrusted and
  the marker is trivially spoofed. Human-readable output may accompany an event but cannot
  replace it.
- Reclassifying GitHub `cancelled` from elapsed time or `timeout-minutes` is rejected.
  Manual, concurrency, fail-fast, and deadline cancellation are not interchangeable.
- A GitHub App is not the MVP. An App could create authentic check-level `timed_out`
  results or observe workflows externally, but introduces a hosted service, private key,
  installation lifecycle, `checks:write`, secret rotation, and a new security boundary.
- Reimplementing a cross-platform timeout engine immediately is rejected until the
  proposal evaluates adapting or contributing to established Actions such as
  `nick-fields/retry`.
- Adding the feature to gh-run-receptor before 1.0 is rejected because its current stable
  target is a read-only consumer contract. Producer execution must not delay that release.

## Scope and exclusions

The initial consumers are the MolSysSuite `repository` profile, especially MolSysMT and
MolSysViewer Conda/CI workflows, with gh-run-receptor as the likely report consumer.
Community portability is required before describing the result as a general tool.

The MVP excludes whole-workflow cancellation, mutation of GitHub state, inference from
logs, opaque third-party `uses:` step wrapping, a continuously hosted service, and claims
about native GitHub timeout causality. Runner disappearance and GitHub killing the job
before the event is written remain explicit `not_observed` cases.

## Acceptance criteria

- gh-run-receptor 1.0 is published before implementation begins.
- A second prior-art review decides reuse, upstream contribution, adapter, or new
  implementation with concrete compatibility and maintenance evidence.
- At least two distinct MolSysSuite workflow families measure the diagnostic need and
  identify an operation that can be wrapped before the enclosing job deadline.
- The proposal chooses one owner: gh-run-receptor extension, existing external Action
  integration, or a newly admitted MolSysSuite component. Ownership is not split.
- A provisional event schema distinguishes source conclusion, producer outcome, timeout
  limit, elapsed time, operation identity, run/attempt/job identity, and evidence
  completeness.
- Threat analysis covers malicious commands, output/log injection, child processes,
  secrets, artifact substitution, pull requests, forks, and resource bounds.
- A prototype proves Linux, macOS, and Windows behavior and retains GitHub's source
  conclusion independently.
- If a new component is accepted, it is registered in `suite.toml` and generated through
  the new-component starter kit before repository implementation.
- Public documentation explains when the mechanism cannot emit evidence and provides a
  native GitHub fallback.

## Local implementation issues

- `uibcdf/gh-run-receptor#45` — resolved discovery and evidence-policy issue; supplies the
  upstream ambiguity, broad negative search, and non-inference contract.

`uibcdf/gh-run-receptor#46` already owns the future consumer implementation and
remains blocked by this central ownership/contract decision. No producer implementation
issue is opened yet; create it in the selected owner before producer code.

## Dependencies and risks

The former 1.0 schedule gate is satisfied. Producer ownership and contract selection
remain undecided; no open release issue is used as a false technical blocker. The main risks are duplicating mature timeout Actions, failing
to terminate child processes portably, losing the event when GitHub kills the runner,
overstating a producer assertion as GitHub truth, and adding supply-chain surface to every
instrumented workflow.

The strongest mitigation is a narrow producer contract with explicit provenance and
absence semantics, followed by reuse of established execution machinery where its
security and termination behavior satisfy the contract.

## Provenance

Drafted on 2026-09-19 from the gh-run-receptor 0.22.0/1.0 evidence audit, issue
`uibcdf/gh-run-receptor#45`, GitHub's current workflow syntax, workflow-runs REST and
status-check documentation, and the public repositories of the inspected community
Actions. No new component, workflow, permission, or runtime dependency was created.


## Second design review — 2026-10-02

### Release gate and existing ownership

[GH Run Receptor 1.0.0](https://github.com/uibcdf/gh-run-receptor/releases/tag/1.0.0)
was published at `2026-09-19T19:39:35Z`, confirmed through native release metadata.
The consumer follow-up uibcdf/gh-run-receptor#46 already exists. Source
`1f378f2ccd0e8cf8c0d4cbb73431c712611955b1` has bounded producer-artifact
selection, digest checking, ZIP/JSON validation and offline replay in
`gh_run_receptor.events` and `gh_run_receptor.bundle`. Its strict `events@1`
contract only accepts `conda.package`; generic operation events cannot be passed
to it under the existing schema identifier. Consumer integration belongs there,
with compatibility tests and a separately accepted contract version.

### Repeatable prior-art findings

Inspected the following immutable upstream sources and current documented
interfaces. This bounded review did not find a drop-in source-bound timeout
artifact producer. It is not an exhaustive claim about all Actions.

| Candidate | Inspected source | Useful capability | Missing evidence or compatibility |
| --- | --- | --- | --- |
| nick-fields/retry | `1c62e0697831d444be410bc770cc1576ab22de08` | Command deadline, retries, cross-platform shells and tree-kill invocation | No typed terminal reason or source-bound artifact; timeout and ordinary exit 1 can both return exit code 1. `exit_error` is text. Killing requests are not awaited through a callback or independently confirmed. |
| Wandalen/wretry.action | `e94c43bf2e865e7dbbd90b0c1061053f5888932a` | Command/Action retry and overall timeout input | The declared output is a map from the wrapped operation, not a timeout evidence record. Its root composite references a nested Action by mutable tag; pinning that root alone does not freeze the nested implementation. Process termination was not certified in this review. |
| corrupt952/actions-retry-command | `03ec8eb092de8cc03e411ad1d2aced2e951428cd` | Command deadline and final exit code | Its README explicitly says a timed-out process can continue running. Exit 124 alone cannot distinguish a supervised deadline from a command that exits 124 itself. |

Primary inspected files:

- [retry execution and outputs](https://github.com/nick-fields/retry/blob/1c62e0697831d444be410bc770cc1576ab22de08/src/index.ts),
  including the direct `tree-kill` call and timeout-error branch;
- [wretry Action metadata](https://github.com/Wandalen/wretry.action/blob/e94c43bf2e865e7dbbd90b0c1061053f5888932a/action.yml);
- [retry-command limitations](https://github.com/corrupt952/actions-retry-command/blob/03ec8eb092de8cc03e411ad1d2aced2e951428cd/README.md).

A composite adapter around these unchanged interfaces cannot claim a verified
terminal reason or successful child cleanup merely by parsing their text or
exit status. An upstream typed-output change could make reuse possible, but it
is not delivered evidence and no upstream contact or contribution was made.

### Concrete ownership decision to review

**Recommended direction:** a small dedicated command-supervision Action owns
the producer and its independently useful event contract. GH Run Receptor
consumes the event under uibcdf/gh-run-receptor#46. MolSysSuite coordinates
interoperability, admission and pilots. The producer would reuse reviewed
process-management primitives where their behavior is adequate, rather than
copying an Action or deriving timeout from its output. The engine/language,
repository name and admission are not accepted by this recommendation.

Alternatives requiring an explicit maintainer choice:

1. Obtain typed outcomes, child-cleanup evidence and event emission in an
   existing upstream Action, then integrate that pinned producer. This avoids
   a new maintained producer but makes delivery depend on an external project.
2. Add command supervision inside GH Run Receptor. This combines execution and
   inspection ownership and requires an explicit expansion of its current
   read-only product boundary; it is not covered by consumer issue #46 alone.

No new repository, release, runtime dependency or workflow rollout is authorized
by this design record. If a separate producer is accepted, its owning issue and
registered admission/generation route precede implementation. The existing
starter kit is for Python components; a JavaScript Action needs a reviewed
generation profile rather than an arbitrary copied repository.

### Provisional event contract for the selected producer

These requirements are reviewable design, not a published schema or a common
mandatory CI policy:

- One bounded JSON document per operation; versioned schema, strict keys and
  finite integer durations. The proposed identifier `producer-outcome@1`
  remains provisional. At most 16 KiB, no logs, commands, environment values
  or error text in the document.
- Source identity: repository, run ID, run attempt, tested head SHA, workflow
  identity, job key and explicit matrix identity. A matrix cell must not collide
  with another artifact or be assigned to a native job through a name guess.
  Unresolved native-job correlation is explicit incomplete evidence.
- Producer identity: repository and immutable implementation SHA, independently
  checked against the trusted workflow configuration. Event self-declaration
  and artifact digest alone do not authenticate a producer.
- Operation identity: caller-selected safe identifier, operation attempt,
  deadline milliseconds, monotonic elapsed milliseconds and bounded cleanup
  grace. Wall-clock timestamps may aid diagnosis but cannot decide timeout.
- Observed terminal reason: `completed`, `exit_failure`, `deadline_exceeded`,
  `interrupted` or `supervisor_error`. Deadline evidence comes from the
  supervisor's own observed timer, not exit 124, printed markers or duration.
  Cancellation racing with a deadline must be tested and cannot acquire a
  guessed reason.
- Exit code/signal remain separate, nullable when unavailable. Termination
  evidence is `confirmed`, `unconfirmed` or `not_required`; a cleanup request
  is not confirmation. Failure to confirm cleanup must prevent success.
- GitHub's run/job/step status remains native consumer evidence, outside the
  producer's asserted outcome. A timed-out operation normally fails its step;
  the consumer reports that source failure plus the producer deadline fact.
- Consumers keep accepted, missing, malformed, untrusted, contradictory and
  incomplete evidence distinct. Missing publication means `not_observed`,
  never success or inferred timeout. Unknown schema versions are unsupported.

Publication follows in a bounded `if: always()` step using an immutable artifact
Action revision and an artifact name qualified by run, attempt, job/matrix and
operation. The controlled deadline and cleanup/upload allowance must fit the
**remaining** enclosing job budget, including time spent before the operation.
GitHub can still stop the runner before publication; native evidence remains
the fallback. Artifact selection/digest checks and safe bounded parsing should
reuse the existing consumer mechanisms with the required schema extension.

### Pilot candidates and limits

Two distinct workflow families expose concrete command boundaries:

| Family | Existing boundary | Current evidence and proposed first probe |
| --- | --- | --- |
| Developer-tool tests | GH Run Receptor `python-routine.yml`: complete package suite within a 20-minute job | Native [36935965052](https://github.com/uibcdf/gh-run-receptor/actions/runs/36935965052) passed at `da225de8e1a574b5f4b3469f6b89a03548632e7f`; its measured test step ran 7 seconds. First probe would be an inert supervisor fixture, not an extra package-suite execution. |
| Installed-artifact qualification | MolSysSuite `test-installed-noarch-conda.yaml`: explicit installed-test command within a 45-minute job | Source inspection identifies the hook and post-test provenance check. No installed scientific candidate was selected or executed. First probe would exercise the same command/publication shape with an inert child process. |

The Conda **build** in `publish-noarch-conda.yaml` is an opaque `uses:` step
from its own provider. A command wrapper at the caller cannot supervise its
internal build correctly; later adoption must be decided within that provider,
not by wrapping the entire external Action or adding a job-level time inference.

The table proves candidate integration points, not measured diagnostic benefit,
portable termination or a safe production deadline. Subsequent pilots must
prove success, ordinary failure, voluntary exit 124, true deadline, stubborn
children/grandchildren, cancellation races, missing/failed upload and rejected
artifact substitution on Linux, macOS ARM and Windows. Initial probes should
be seconds long, contain no credentials and upload no packages. No MolSysMT or
MolSysViewer source, CI or scientific selection was changed for this review.

### Trust boundary and applicability

This proposed capability is opt-in for cooperating workflows whose maintainers
can reserve time for evidence publication. It adds no required timeout, retry
or suite execution to all components. Adoption failures keep native reporting
and an owner-local tracked exception if a later shared requirement applies.

A workflow's arbitrary command can write files and communicate with the runner.
Neither a digest nor a versioned JSON file isolates a malicious command. Initial
pilots accept only configured trusted producer/workflow revisions and treat
fork/untrusted-PR events as untrusted assertions. No privileged
`pull_request_target` execution or credential-bearing command is needed.
Rejected artifacts must not hide or rewrite the source conclusion. The threat
review must test stdout workflow-command injection, file replacement, process
escape, archive traversal/expansion and source/attempt substitution before
claiming trusted production evidence.

### Decision boundary

The release prerequisite is satisfied and the second prior-art/consumer review
is recorded. Producer ownership is now the next maintainer decision. Until it
is made, #25 remains open and uibcdf/gh-run-receptor#46 remains blocked; the
provisional contract is not advertised as an implemented capability.
