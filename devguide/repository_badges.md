# Repository badges and MolSysSuite role identity

This document defines the accepted central design for README badges in registered
MolSysSuite repositories. Member adoption is tracked separately in
[`rollouts/repository_badges.md`](rollouts/repository_badges.md); until that rollout is
complete, absence of the new baseline is recorded migration work rather than a policy
violation in the general repository gate.

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
- Codecov, when current default-branch coverage is uploaded for that repository;
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

## Offline validation

The central checker validates facts available in a checkout:

```bash
python devtools/scripts/repository_badges.py check ../pyunitwizard \
  --repository uibcdf/pyunitwizard
```

It checks the exact role, repository-qualified policy workflow, Python support badge,
license link, baseline order and foreign workflow targets. It is read-only and reports
independent findings. During rollout it is run explicitly; it becomes part of the common
repository gate only after every applicable member has adopted or carries an approved
exception.

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

## Exceptions and changes

An exception is central, explicit and time-bounded. It names the affected badge, reason,
owning issue and removal condition. Repository-local prose does not waive a shared rule.

Changing a role requires a central issue because it changes public suite
identity. Adding or removing a conditional badge is local when it merely follows a change
in the underlying capability, but the evidence and ordering rules remain central.

New components receive a role during admission. An incubating component adopts the
identity badge immediately when its governance guide lands, while health and capability
badges appear only as their real surfaces mature.
