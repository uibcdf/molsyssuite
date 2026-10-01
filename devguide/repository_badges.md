# Repository badges and MolSysSuite role identity

## Ownership

MolSysSuite owns member badge rules, role taxonomy, generated snippets, rollout state and conformance checks. The evidence principle here is a suite rule for its members; MOLI separately governs badges of directly governed components.

This document defines the accepted central design for README badges in registered
MolSysSuite repositories. The completed adoption is recorded in
[`rollouts/repository_badges.md`](rollouts/repository_badges.md), and policy release
`policy-v1.3.1` enforces the offline baseline through the common repository gate.

## Principles

**Identity is not health.** The MolSysSuite role badge says what a repository is and who
governs its shared contracts. It does not claim that CI passes, a release exists, coverage
is current, documentation is deployed, or an archive has been verified.

Every badge must make one bounded claim backed by the surface to which it links. When a
capability is absent, stale, unverifiable, or intentionally deferred, absence is better
than an unsupported claim. A static green badge must never stand in for a live result.

Badges are a compact entry point, not the source of truth. GitHub Actions, Codecov,
documentation hosting, GitHub Releases, package registries and Zenodo retain authority
over their own state.

## Roles

Every registered member has exactly one human-facing `role` in `suite.toml`. Roles
describe the repository's primary relationship to users; they do not determine its
membership, maturity, development mode, capabilities or planning priority. The complete
classification contract lives in [`member_classification.md`](member_classification.md).

### scientific-component

Scientific components expose molecular-science models, analysis, transformation or
visualization directly to users: MolSysMT, MolSysViewer, TopoMT, PharmacophoreMT and
ElastNetMT.

### support-library

Support libraries provide reusable runtime contracts consumed by scientific components:
SMonitor, ArgDigest, DepDigest and PyUnitWizard. PyUnitWizard remains scientific software;
the role records that its suite-facing responsibility is the shared units boundary.

### developer-tool

Developer tools primarily support testing, CI inspection or repository maintenance:
Pytest Receptor, GH Run Receptor and Lindelint. An auxiliary member may therefore be a
developer tool without changing either field's meaning.

The three role badges use the Shields static-badge endpoint with centrally fixed labels
and colors. Shields is the renderer, not the authority: `suite.toml` owns the role,
`repository_badges.py` generates the complete Markdown, and the badge link targets this
document. The Markdown alt text names both MolSysSuite and the role, so color is never the
only signal. The supported URL syntax is documented by
<https://shields.io/badges/static-badge>.

Do not hand-edit or copy a Shields URL from another member. Rendering availability is not
role evidence and a temporary renderer outage does not change repository identity.

## Baseline and order

The baseline appears near the start of the README in this order:

1. MolSysSuite identity and role;
2. MolSysSuite policy conformance;
3. supported Python versions for a member with the `python-package` capability;
4. license.

Generate it from the registry rather than copying another repository:

```bash
python devtools/scripts/repository_badges.py snippet \
  --repository uibcdf/pyunitwizard
```

The policy badge targets the repository's own `molsyssuite-policy.yml` workflow on the
default branch. A repository without that workflow does not carry a fabricated passing
badge: its rollout state remains pending or blocked until the policy gate exists. The
Python badge links to the suite support contract, and the license badge links to the
repository's own `LICENSE` file.

## Conditional capability badges

After the baseline, a repository may advertise only capabilities it actually maintains:

- continuous tests, when a push or pull-request workflow runs the component tests;
- Codecov's live percentage, required when meaningful default-branch coverage
  reporting is maintained for that repository, with the evidence rules below;
- documentation, when the linked public site is deployed and maintained;
- release, when GitHub Releases are part of the component's release process;
- DOI, when the badge resolves to that repository's verified archival record;
- PyPI, Conda, npm or other distribution channels, when the linked package exists there.

The displayed order is tests, coverage, documentation, release, DOI and distribution.
Omit inapplicable capabilities rather than preserving an empty slot. Prerelease-only or
incubating repositories must not imply a stable public release merely to match mature
members.

Workflow badges name their actual function. A policy-only workflow is not labelled
“Tests”, a manually dispatched release gate is not continuous CI, and a documentation
build that has never deployed does not authorize a public-docs badge.

## Coverage percentage, applicability and cadence

An applicable component with a maintained meaningful coverage report displays a
live Codecov **percentage** in its main README between tests and documentation.
Use its own project and actual default branch. Generate the public snippet with
`coverage_badge(repository, branch)` in `devtools/scripts/repository_badges.py`
after reviewing evidence. Do not write the percentage by hand, substitute a
passing-status image, include a token, or quietly select only one flag/component.

Applicability follows tested executable code, not maturity or repository role.
Scientific libraries and auxiliary developer tools can both have meaningful
coverage. Central MolSysSuite and a specification-oriented subsystem must be
assessed explicitly: tooling/governance coverage measures that code only and
must not imply coverage of an unimplemented scientific or agent runtime. No
configured upload or absence of public data by itself proves applicability or
non-applicability. A justified non-applicable outcome names the current code
boundary and the condition that requires reassessment.

Preserve a reviewed inventory for every registered member and the suite root.
Record default branch, inspected source SHA, coverage-producing route and cadence,
completed Codecov report SHA/percentage, observed service timestamp, actual upload
step/run when available, README outcome and owning follow-up. A numeric SVG alone
does not establish recent accepted evidence: branch caches can inherit totals
onto skipped commits. A commit timestamp is not an upload timestamp. Check the
completed report and uploader independently, and keep unavailable evidence visible.

The README explains the report scope and cadence beside the badge, including
that it reflects the last uploaded report and may lag later direct/skip commits.
For a scheduled producer, judge recency against its declared cadence and the
date of its most recent executed upload. For a dormant repository, record source
continuity rather than impose a universal report-age cutoff. If expected reports
are missed, source drift is unexplained, or service evidence is stale/unavailable,
track the owning repair and withhold a new badge claim until evidence is reviewed.
Coverage percentage is not a full-matrix pass or scientific certification; a
valid report from one lane can coexist with failures in other lanes.

Missing producers, stale reports and temporarily deferred reviews require an
owner-local issue cross-linked to the central adoption issue. A bounded exception
names reason, owner, review/expiry date, interim README behavior and removal
condition. The initial MolSysMT deferral waited for its next reviewed recent report. On
2026-10-01 the maintainer explicitly authorized one complete Linux/Python 3.13
refresh under uibcdf/molsysmt#286. Additional full scientific execution requires
its ordinary component policy or explicit authorization; a missing badge alone
does not authorize it.

Coverage reporting follows existing component CI and skip-recovery policies.
This badge rule adds no full suite to internal direct pushes and defines no
common minimum coverage percentage. Component owners retain coverage selections,
language/report scope and scientific remediation.

## Offline validation

The central checker validates facts available in a checkout and is also called by the
common repository conformance gate:

```bash
python devtools/scripts/repository_badges.py check ../pyunitwizard \
  --repository uibcdf/pyunitwizard
```

It checks the exact role, repository-qualified policy workflow, Python support badge,
license link, baseline order and foreign workflow targets. It is read-only and reports
independent findings. Every registered member adopted the baseline before enforcement
was enabled; conditional service claims remain outside this offline gate.
Existing public Codecov Markdown is also checked for repository identity, project
link and absence of token/partial-report query parameters. Missing coverage and
freshness remain explicit adoption/network reviews, not inferred from Markdown.

Offline Markdown shape cannot prove that a service is live. In particular, it cannot
establish that Codecov contains recent data, Pages serves the intended site, a release is
published, a package exists, or a Zenodo repository identifier belongs to the component.

## Networked audit

A separate authenticated networked audit will compare conditional badges with their
authoritative services. It must preserve unavailable evidence as unavailable rather than
passing it, and must distinguish an invalid response from a network failure.

The audit verifies at least:

- the default branch and workflow file named by an Actions badge;
- the latest completed default-branch run and its actual purpose;
- current Codecov repository identity and upload recency;
- the final URL and repository identity of documentation and DOI badges;
- GitHub Release state and package-registry coordinates.

Tokens, signed URLs and private endpoints must never appear in README badge Markdown,
generated snippets, issue text or audit output. The existing Zenodo inventory remains the
authority for verified DOI evidence; the badge audit consumes it rather than inventing a
second archival record.

### Reusable public coverage probe

```bash
python devtools/scripts/coverage_audit.py --repository uibcdf/molsysviewer
```

`inspect_codecov(repository, fetch=public_payload, pages=3)` discovers the default
branch from GitHub, examines the public branch cache and rendered SVG, and scans
up to three 100-commit pages for an explicitly complete report. Its JSON receipt
keeps source SHA, commit timestamp, branch-cache state, observation time and
service errors separate. A skipped commit's inherited totals do not satisfy a
complete report. A bounded search without a report is incomplete evidence, not
proof that the project has never uploaded. The CLI exits nonzero for missing,
invalid or unavailable evidence. It does not determine report freshness,
applicability, full-suite health or upload time; review the owner's cadence and
matching native upload step separately. Consumers may inject a bounded public
fetcher; the default uses no credentials and limits response size and duration.

The service interfaces follow Codecov's
[commit-list API](https://docs.codecov.com/reference/repos_commits_list),
[branch detail](https://docs.codecov.com/reference/repos_branches_retrieve) and
[status-badge documentation](https://docs.codecov.com/docs/status-badges).
The dated rollout is [coverage_badges.md](rollouts/coverage_badges.md).

## Exceptions and changes

An exception is central, explicit and time-bounded. It names the affected badge, reason,
owning issue and removal condition. Repository-local prose does not waive a shared rule.

Changing a role requires a central issue because it changes public suite
identity. Adding or removing a conditional badge is local when it merely follows a change
in the underlying capability, but the evidence and ordering rules remain central.

New components receive a role during admission. An incubating component adopts the
identity badge immediately when its governance guide lands, while health and capability
badges appear only as their real surfaces mature.

## Central administrative coverage producer

MolSysSuite measures `devtools/scripts` with branch coverage during its existing
`unittest discover -s tests` execution in `validate_governance.yaml` on Linux/Python
3.13. Child processes are not instrumented or combined; unexecuted scripts stay
in the denominator. This is central administrative coverage, not a measure of
member scientific packages. The exact run's XML is retained for 14 days. A
separate job downloads that XML and uses OIDC to upload from `main` on push or
manual dispatch. The test job has read-only permissions; PRs do not publish.
Missing reports or upload errors fail the publisher and remain visible.

A live badge is added only after independent service acceptance. Its percentage
can lag internal lightweight or skipped pushes and has no required floor.
`tests/test_coverage_workflow.py` guards the trusted publication boundary and the
existing administrative test selection.
