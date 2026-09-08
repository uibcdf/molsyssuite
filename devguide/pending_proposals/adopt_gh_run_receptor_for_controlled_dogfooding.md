---
summary: Adopt gh-run-receptor for controlled dogfooding across MolSysSuite.
issue: uibcdf/molsyssuite#19
status: open
opened: 2026-09-08
closed:
verification: measured
area: [governance, ci, tooling]
guard:
normative:
blocked_by: []
supersedes: []
---

# Adopting gh-run-receptor for controlled dogfooding across MolSysSuite

**Reported:** 2026-09-08 after gh-run-receptor reached an evidence-based 96% of its
roadmap to 1.0 and its guide had been distributed to the registered consumers.
**Status:** Open; controlled adoption is proposed but is not yet a suite policy.

## What

Adopt gh-run-receptor as the preferred first inspection path for GitHub Actions during
MolSysSuite development. The adoption is deliberately controlled: the receptor is a
supplementary observer, GitHub conclusions remain authoritative, and no component may
make it the sole release authority until the central policy graduates it.

The purpose is twofold: reduce avoidable LLM-token consumption during routine workflow
inspection and expose missing, misleading, or excessively verbose interpretations through
real use across the suite's different workflow families.

## How

The proposed operating policy is:

1. Use the latest published gh-run-receptor release for routine inspection.
2. Use post-release behavior only in an explicitly experimental trial pinned to an exact,
   reviewed commit. Never point shared automation at a floating `main` branch.
3. Treat `PASS`, `FAIL`, and descriptive comparisons as compact views of captured facts,
   not replacements for GitHub's source conclusions.
4. Fall back to native `gh run view` inspection when the receptor returns `INCOMPLETE`,
   exits with an acquisition or receptor error, omits evidence needed for the decision,
   or disagrees with GitHub.
5. Do not use gh-run-receptor as the only approval source for a package publication,
   release, deployment, citation update, or other irreversible operation during this
   adoption period.
6. Report a receptor limitation to `uibcdf/gh-run-receptor` with the consuming repository,
   workflow, run ID, selected profile and capture mode, expected result, observed result,
   and the smallest sanitized evidence that reproduces it. Cross-link a consumer issue
   only when a concrete local change or workaround exists.
7. Never attach credentials, unredacted secret-bearing logs, private-repository evidence,
   or unrestricted bundles to a public issue.
8. A member that cannot adopt the preferred path records an exception with its reason,
   behavioral consequence, expiration condition, and tracking issue. Silent divergence is
   not an exception.

Routine development may therefore use the receptor first and native inspection on demand.
Release owners retain responsibility for consulting the underlying evidence whenever a
decision exceeds the receptor's demonstrated scope.

## Why

The shared `GH_RUN_RECEPTOR_GUIDE.md` is already registered for ten consumer repositories,
and the tool has been exercised against CI, documentation, Conda, release, rerun, and
terminal-reporting workflows. Coordinated dogfooding turns that distribution into useful
operational evidence instead of waiting for 1.0 without heterogeneous use.

A central policy is necessary because this changes developer practice in more than one
member. Leaving the rule implicit would produce different trust thresholds, fallback
behavior, version selection, and feedback quality across repositories.

## What is measured and what is assumed

Measured in `uibcdf/gh-run-receptor` on 2026-09-08:

- 334 local tests pass with `pytest --receptor=llm`;
- Ruff, contract compatibility, devguide validation, wheel build, and clean-environment
  wheel installation pass;
- hosted run `34213219459` validates real paired ArgDigest attempts and explicit passing
  and failing comparison policies;
- the project roadmap records 96% evidenced implementation credit toward 1.0;
- release `0.18.0` is the latest published version, while comparison policies and the
  same-revision reusable reporter are post-release capabilities.

The claim that broader use will uncover additional limitations is an expectation, not a
measurement. No evidence yet establishes equal interpretation quality across every member,
private repository, fork, workflow type, or release decision.

## Alternatives and refuted paths

- Waiting for 1.0 before any suite use is rejected because it withholds the diverse
  feedback needed to justify 1.0.
- Making the tool mandatory or the sole release gate now is rejected because remaining
  evidence and aggregation gaps are documented.
- Referencing a floating development branch is rejected because different runs could use
  unreviewed behavior under the same configuration.
- Filing every observation only in the consuming repository is rejected because the
  provider would lose actionable cross-component evidence.
- Printing full native workflow output alongside every receptor report is rejected because
  it defeats token economy; native output is an on-demand safety net.

## Scope and exclusions

The proposal applies to every repository registered in `suite.toml`, across
`python-library`, scientific, application, and infrastructure profiles. It governs
development-time GitHub Actions inspection and feedback.

It does not require an immediate workflow edit in every member, replace repository-local
release gates, authorize automatic reruns or cancellation, expose private evidence, or
declare the unreleased development surface stable. Packaging and releasing
gh-run-receptor remain owned by `uibcdf/gh-run-receptor`.

## Acceptance criteria

- A normative suite policy records applicability, safe defaults, fallback conditions,
  experimental pinning, security boundaries, exception handling, and graduation criteria.
- `suite.toml` registers the accepted policy and its normative document.
- A rollout record distinguishes guide availability, routine use, experimental use, and
  observed feedback across stabilization, infrastructure, and incubating cohorts.
- At least one workflow family beyond gh-run-receptor itself supplies measured dogfooding
  evidence without using the receptor as its sole release authority.
- Provider feedback uses stable `uibcdf/gh-run-receptor#<number>` identities and consumer
  workarounds cross-link them where applicable.
- The policy states the evidence required before gh-run-receptor may become mandatory or a
  sole approval input; reaching version 1.0 by itself is not sufficient.
- The offline governance guard validates the policy registration and report lifecycle.

The accepted normative document will be recorded in `normative` before closure.

## Local implementation issues

None are opened automatically. Existing guide distribution is sufficient to begin manual
trials. A member issue is required only for a concrete workflow change, local workaround,
or tracked adoption exception.

## Dependencies and risks

Basic dogfooding is not blocked by a new release because published `0.18.0` supports the
established inspection path. Trials of post-release comparison and reusable-reporting
capabilities depend on an exact reviewed commit until the next release publishes them.

The principal risks are false confidence in a compact interpretation, accidental use of
floating development code, disclosure of sensitive evidence, and feedback fragmentation.
The operating rules above turn each risk into an explicit boundary or fallback.

## Provenance

Inspection performed on 2026-09-08 from the MolSysSuite checkout and the synchronized
gh-run-receptor development record. Relevant gh-run-receptor implementation commit:
`d98fc2f`; governance checkpoint commit: `7c2928c`; hosted validation run:
`34213219459`; Python: 3.13.14; operating system: Linux.
