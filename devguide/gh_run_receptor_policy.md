# GH Run Receptor controlled-dogfooding policy

This document is normative for every repository registered in `suite.toml`. Accepted by
`uibcdf/molsyssuite#19`. It governs development-time GitHub Actions inspection; it does
not transfer ownership of workflow conclusions or release decisions to the receptor.

## Authority and purpose

GH Run Receptor is the preferred first inspection path for routine development because it
preserves structured evidence while bounding human- and LLM-facing output. GitHub's source
run, job, artifact, and conclusion data remain authoritative. A receptor interpretation
is a compact view of those facts, not a replacement authority.

During controlled dogfooding, GH Run Receptor is supplementary. It must not be the only
approval input for package publication, a GitHub Release, deployment, citation change, or
another irreversible operation. Repository release owners retain responsibility for the
underlying evidence and local gates.

## Version selection

Routine use selects the latest published release admitted by the consuming repository.
Shared automation pins a release tag or immutable commit; it never selects a floating
development branch.

An unreleased capability may be evaluated only as an explicit experiment pinned to an
exact reviewed commit. The trial records the commit and does not describe that behavior
as released or stable. Once a release contains the capability, consumers return to the
published version unless a new experiment is separately justified.

## Inspection and fallback

Developers may use the repository configuration and receptor profile as the default route
for `inspect`, `watch`, replay, published-report inspection, or comparison. They consult
native GitHub evidence when any of these conditions holds:

- the receptor reports `INCOMPLETE` or exits because evidence is unavailable;
- acquisition, parsing, configuration, or contract validation fails;
- the report omits a fact needed for the current decision;
- receptor interpretation disagrees with GitHub source facts;
- the operation is outside the documented profile or capture contract;
- an irreversible action requires confirmation beyond the demonstrated scope.

Fallback is targeted and on demand. Printing complete native output beside every compact
report is not required and defeats the token-economy purpose.

## Feedback and provider ownership

A missing, misleading, unsafe, or unnecessarily verbose receptor behavior belongs to
`uibcdf/gh-run-receptor`. The provider report includes:

- consuming repository and workflow;
- run ID or stable run URL and attempt when relevant;
- receptor version or exact commit, profile, capture mode, and command shape;
- expected and observed result;
- the smallest sanitized bundle or structured excerpt that reproduces the behavior;
- impact on correctness, release confidence, operability, or token use.

The consumer opens a local issue only for a concrete integration change, tracked
workaround, or adoption exception, and cross-links the provider issue. A workaround names
its removal condition. Observations do not remain solely in conversational history.

## Evidence security

Public reports and attachments contain no credentials, tokens, private-repository data,
secret-bearing log lines, or unrestricted evidence bundles. Redaction in the receptor is
defense in depth, not authorization to publish captured material. When a minimal public
reproduction is impossible, use the provider repository's private security channel or an
appropriately restricted team channel.

The receptor remains read-only under this policy. Rerunning, cancelling, approving,
publishing, or mutating a workflow is outside its adopted authority.

## Readiness, adoption, and authority states

The rollout keeps three claims separate:

- **ready:** the component has current guidance and a valid repository configuration;
- **active:** a recorded developer or workflow invocation used the receptor and retained
  enough provenance to evaluate the result;
- **graduated:** collective evidence permits stronger authority than supplementary use.

Guide presence or valid configuration proves only readiness. Using a member's public run
as a provider fixture does not prove that the member's developers adopted the tool.

## Exceptions

A component may deviate only through a tracked exception naming the repository, affected
rule, reason, behavioral consequence, issue, and expiration condition. An unavailable
workflow, unsupported environment, or demonstrated receptor defect can justify an
exception. Preference for unrestricted output without evidence does not.

Incubating status may defer scheduled rollout work, but it does not permit a silent fork
of the policy when the receptor is used.

## Graduation criteria

Version 1.0 alone does not graduate the receptor. A proposal for mandatory use or sole
approval authority requires all of the following evidence:

- published, frozen contracts for every surface on which the stronger authority depends;
- demonstrated installation and Action execution on every claimed operating system;
- truth-preserving incomplete, degraded, and acquisition-error behavior;
- measured use across CI, documentation, Conda, and release workflow families;
- at least one active member in each non-deferred stabilization cohort;
- bounded-output and token-reduction measurements on representative runs;
- no unresolved known defect that can turn missing evidence into a pass;
- a tested native fallback and documented incident procedure;
- security review of tokens, logs, bundles, caches, pull requests, and private evidence;
- an explicit central decision changing `sole-release-authority` in `suite.toml`.

Until those conditions are recorded, the safe default remains preferred first inspection
with native fallback and independent release gates.
