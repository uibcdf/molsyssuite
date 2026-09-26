# GH Run Receptor controlled-dogfooding policy

This is the MolSysSuite dogfooding profile for the [effective MOLI developer-tools
policy](https://github.com/uibcdf/moli/blob/15b38fbe17b6ee9fa9aac2a8e21b80d76a8da70f/devguide/policies/python_developer_tools_policy.md).
It is normative for registered members and accepted by `uibcdf/molsyssuite#19`.
MOLI owns general inspection, version, fallback and release-authority rules;
this profile tracks suite-member evidence, feedback and exceptions.

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
- active evidence from both stabilization-priority and non-priority members;
- bounded-output and token-reduction measurements on representative runs;
- no unresolved known defect that can turn missing evidence into a pass;
- a tested native fallback and documented incident procedure;
- security review of tokens, logs, bundles, caches, pull requests, and private evidence;
- an explicit MOLI decision on any change to the general release-authority rule,
  followed by a suite decision on member applicability.

Until those conditions are recorded, this profile makes no stronger authority claim.
