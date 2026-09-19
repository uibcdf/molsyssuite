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
**Status:** Open design proposal; investigation may continue now, but implementation and
component admission are explicitly scheduled after gh-run-receptor 1.0.

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

No implementation issue is opened yet. Component-local issues follow only after this
central proposal selects ownership and gh-run-receptor 1.0 is published.

## Dependencies and risks

Implementation is schedule-gated by gh-run-receptor 1.0, but no open issue is used as a
false technical blocker. The main risks are duplicating mature timeout Actions, failing
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
