---
summary: Standardize repository badges and MolSysSuite role identity.
issue: uibcdf/molsyssuite#23
status: active
opened: 2026-09-17
closed:
verification: measured
area: [governance, documentation, automation]
guard:
normative: devguide/repository_badges.md
blocked_by: []
supersedes: []
---

# Standardizing repository badges and MolSysSuite role identity

**Reported:** 2026-09-17, while publishing the gh-run-receptor documentation and
comparing its README with pytest-receptor and the other registered members.
**Status:** Active. The central role taxonomy, normative design, assets, snippet generator
and offline validator were accepted on 2026-09-20. Component adoption and authenticated
capability auditing remain pending.

## Central design checkpoint — 2026-09-20

The three proposed roles are now authoritative registry values: scientific component,
support library and developer tool. `suite.toml` assigns exactly one to every current
member. Role is independent from membership, maturity, development mode, technical
capabilities and temporary initiatives, as defined by `devguide/member_classification.md`.

Three accessible static Shields URLs carry centrally fixed text and colors.
`devtools/scripts/repository_badges.py` generates the ordered identity, policy, Python and
license baseline directly from the registry and performs a read-only offline check. Its
negative fixtures reject missing baseline claims, a wrong role, a wrong order and
workflow badges that point to another repository. Shields renders the image but does not
own the role or its meaning.

The policy explicitly separates identity from health and offline syntax from live
evidence. Codecov freshness, documentation deployment, GitHub Releases, package records
and DOI ownership require a later networked audit. The rollout matrix is recorded in
`devguide/rollouts/repository_badges.md`; all members remain pending and no component
README changed at this checkpoint.

## Stabilization-priority audit checkpoint — 2026-09-20

The six priority members have now completed the first networked capability audit. The
durable results, run IDs, public-service observations and adoption decisions are recorded
in `devguide/rollouts/repository_badges.md`. `gh-run-receptor` 1.0.0 interpreted the
selected CI, documentation and policy runs; native GitHub queries supplied workflow,
default-branch and release identity.

SMonitor, ArgDigest, DepDigest and PyUnitWizard have current default-branch Codecov data.
MolSysMT's coverage is stale and MolSysViewer's public Codecov totals are unknown, so
those two coverage badges are not authorized for adoption. Every documentation site is
public and its most recent deployment run passed, but MolSysMT's mixed-case metadata URL
is broken and must be replaced by the deployed lowercase path. Every component has a
public GitHub Release and matching public Conda package.

The public Zenodo records behind the MolSysMT and MolSysViewer badges satisfy the central
verification contract and have been promoted to `verified` in the Zenodo inventory.
SMonitor, ArgDigest and DepDigest remain only `enabled_reported` until a post-enablement
release is independently archived; no DOI badge is authorized for them.

The non-mechanical CI debt was already owned by `uibcdf/molsysmt#185` and
`uibcdf/molsysviewer#88`, so the audit did not create duplicates. Baseline and
presentation-only changes can proceed while their dynamic test badges continue to show
the authoritative non-green state.

The mechanical adoption then landed in all six audited repositories: SMonitor
`ecc1164`, ArgDigest `d1f1180`, DepDigest `544fd00`, PyUnitWizard `4be1c4c`, MolSysMT
`f1c6ae39c` and MolSysViewer `76d33be5`. Each README passes the central offline checker.
Hosted MolSysSuite policy runs pass for the first five; MolSysViewer continues to display
the real failure caused by two unformatted files from its concurrent Conda work. Its E2E
run also reproduces the current `setup-micromamba` failure already routed to the open CI
record. Neither failure is hidden or reclassified as badge-rollout success.

The remaining stabilizing members were audited and adopted next. Pytest Receptor
`c208cf2` carries tests, documentation, release, PyPI and Conda evidence; GH Run Receptor
`56f5b01` carries documentation, release and its verified DOI without inventing a
continuous-test or package-index badge; auxiliary Lindelint `bafc2fb` carries tests,
current Codecov, release and Conda evidence. Lindelint documentation remains absent
because its declared URL returns 404 and its deployment workflow has never run; the local
remediation is `uibcdf/lindelint#5`.

All hosted workflows triggered by those three adoption commits passed when inspected
through `gh-run-receptor`. The central generator was also made transition-aware: an
`authorized` Python component retains the default public range, and only an `admitted`
component receives the target-range badge. This preserves the strengthened public
delivery rule from `uibcdf/molsyssuite#29`.

## What

Define a suite-wide policy for the badges displayed at the start of member README files.
The policy should make repository identity and maintained capabilities comparable without
claiming evidence that a repository does not have.

Every registered member should carry one centrally governed MolSysSuite identity badge
with exactly one human-facing role:

- `scientific component`: MolSysMT, MolSysViewer, TopoMT, PharmacophoreMT, and ElastNetMT;
- `support library`: SMonitor, ArgDigest, DepDigest, and PyUnitWizard;
- `developer tool`: Pytest Receptor, GH Run Receptor, and Lindelint.

These roles are an accepted identity classification. They are distinct from the other
member fields and from temporary planning initiatives. The registry, rather than README
prose, is their authority.

The badge row should then use a small common order:

1. MolSysSuite membership and role;
2. MolSysSuite policy conformance;
3. continuous tests or CI, when a continuous workflow really runs them;
4. Codecov coverage, when current coverage is uploaded for that repository;
5. documentation deployment, when a public documentation site is maintained;
6. latest release, when the repository publishes GitHub Releases;
7. supported Python versions, for the `python-package` capability;
8. license;
9. optional DOI and installation-channel badges backed by maintained public records.

The first, second, seventh, and eighth items form the expected identity baseline for
Python members once the policy workflow is adopted. The other items are capability
badges: absence must not be disguised by a static green badge.

## How

Maintain the normative `devguide/repository_badges.md` and its registry entry. Give every
member one `role` value independent of membership, maturity, development mode,
capabilities and initiatives. The normative document defines:

- exact badge labels, order, link targets, colors, and accessible alt text;
- applicability and the documented exception mechanism;
- what live evidence authorizes each dynamic badge;
- which badge links to the workflow and which links to the user-facing result;
- how prereleases, repositories without releases, and incubating members are presented;
- how stale, renamed, moved, or retired services remove a badge.

Use three static Shields badge URLs generated from the central registry. The generator
fixes wording, colors, alt text and policy links, preventing components from composing
their own identity. Shields is only the renderer: the registry and linked MolSysSuite
policy remain authoritative. This avoids maintaining handwritten SVG geometry while
matching the renderer already used for the Python and license badges.

Generate canonical Markdown snippets from `suite.toml`. An offline validator should
check the identity badge, repository-qualified workflow paths, Python range, license,
ordering, and declared capability badges. It must check intent rather than only matching
an image-shaped string: for example, a documentation badge is valid only when its source
names a real local deployment workflow and its link names the declared public site.

Use a separate authenticated audit for facts that cannot be proved offline, such as a
public GitHub Release, a successful Codecov upload, or a reachable Pages site. The offline
merge gate must remain useful without network credentials. Central rollout evidence
should record both checks and should create component issues only when a repository needs
concrete local remediation.

## Why

Badges currently mix identity, build health, distribution, and scientific citation with
no common ordering or applicability rule. A reader cannot tell whether a missing badge
means a missing capability, an unconfigured README, or a deliberate exception. No member
currently identifies its role in MolSysSuite.

The policy badge and a distinct membership badge answer different questions. The former
reports whether a shared conformance workflow passed; the latter says that the repository
is a governed suite member and explains its role. Neither replaces component CI,
coverage, documentation, release, license, or citation evidence.

A common design also makes omissions actionable. Coverage should be promoted because it
is valuable evidence, but only when Codecov receives current default-branch data. A
workflow badge must never be labelled “Tests” when the named workflow only checks policy,
and a manual release gate must not be presented as continuous CI.

## What is measured and what is assumed

The audit read the first 30 lines of every registered README, inspected local workflow
trees, ran `python devtools/scripts/suite_status.py`, and queried each repository's
`latestRelease` through the GitHub GraphQL API on 2026-09-17.

| Repository | README badges | Policy workflow | Docs workflow | Codecov in workflows | Latest release |
| --- | ---: | --- | --- | --- | --- |
| smonitor | 6 | yes | yes | yes | 0.15.0 |
| argdigest | 5 | yes | yes | yes | 0.12.1 |
| depdigest | 7 | yes | yes | yes | 0.10.1 |
| pyunitwizard | 6 | yes | yes | yes | 0.25.0 |
| molsysmt | 7 | yes | yes | yes | 0.12.0 |
| molsysviewer | 7 | yes | yes | yes | 0.7.0 |
| pytest-receptor | 4 | yes | yes | no | 1.0.0 |
| gh-run-receptor | 5 | yes | yes | no | 0.21.1 |
| lindelint | 0 | yes | yes | yes | 0.2.0 |
| topomt | 0 | no | yes | yes | none |
| pharmacophoremt | 0 | no | yes | yes | none |
| elastnetmt | 3 | no | yes | yes | 0.1.0 |

All twelve local checkouts contain a license file. Ten workflow trees mention Codecov,
but only six READMEs advertise coverage for their own repository. Four READMEs show a
documentation badge even though all twelve trees contain a Sphinx/Pages-oriented
workflow; workflow presence alone does not prove a currently deployed public site.

Ten repositories have a non-draft, non-prerelease latest GitHub Release. TopoMT and
PharmacophoreMT do not. Nine repositories have the MolSysSuite policy workflow; the three
incubating scientific repositories do not yet have it.

The ElastNetMT README still points its CI and Codecov badges at `uibcdf/enmmt` and the
`master` branch. This is measured stale identity, not merely inconsistent styling, and
should receive a local remediation issue during rollout rather than be silently copied
into a template.

The 2026-09-19 Zenodo rollout audit found a stronger citation-identity defect that the
initial badge count did not detect: SMonitor and DepDigest both used badge repository ID
`137937243`. GitHub identifies that ID as `uibcdf/molsysmt`, and Zenodo redirected both
badges to MolSysMT 0.12.0 DOI `10.5281/zenodo.17850104`. The false badges are tracked by
`uibcdf/smonitor#13` and `uibcdf/depdigest#10`; their own archival work is separate in
`uibcdf/smonitor#14` and `uibcdf/depdigest#11`. This proves that the validator must compare
the badge's resolved repository identity, not merely recognize Zenodo-shaped Markdown.

The three-role assignment and centrally generated Shields URLs are accepted central
design. They have not yet completed component review or README-scale rollout, which
remains visible in the adoption matrix rather than weakening the accepted role vocabulary.

## Alternatives and refuted paths

- One identical `MolSysSuite` badge without a role is simpler but loses the distinction
  that motivated the identity work and makes the badge little more than an organization
  label.
- Encoding roles only through color was rejected because it is inaccessible and unclear
  when badges are copied outside GitHub.
- Reusing the former mixed cohorts (`wave-1`, `infrastructure`, `auxiliary`,
  `incubating`) as public roles was rejected because those values conflated delivery
  priority, function, membership and maturity.
- Deriving the one role mechanically from multi-valued capabilities was rejected because
  capabilities activate technical policy and do not form an exclusive public taxonomy.
- Requiring every candidate badge in every repository was rejected because releases,
  coverage, documentation sites, DOI records, and distribution channels are genuinely
  conditional.
- Treating the MolSysSuite policy badge as a substitute for component CI was rejected;
  the workflows protect different properties.
- Copying current README rows as the standard was rejected because the inventory contains
  missing badges, inconsistent labels and colors, token-bearing Codecov URLs, and stale
  repository targets.
- Validating only Markdown syntax was rejected because a well-formed badge can still
  point at the wrong repository or imply a capability that is not delivered.

## Scope and exclusions

The proposal applies to every repository registered in `suite.toml`, with
capability-based conditions. It covers the README badge row, central identity assets,
machine-readable role authority, validation, exceptions, and coordinated rollout.

It does not require every repository to adopt Codecov, publish documentation, create a
release, mint a DOI, or distribute through Conda or PyPI. It does not redesign component
logos or turn planning initiatives into branding. GitHub repository topics, taglines,
and homepages are related public metadata but remain outside this first badge policy.

## Acceptance criteria

- One exclusive role vocabulary and assignment is accepted for all registered
  members and recorded in `suite.toml`.
- A normative badge policy defines baseline, conditional badges, ordering, links,
  accessibility, evidence requirements, and exceptions.
- Three centrally generated MolSysSuite role badges are rendered and reviewed at README scale.
- Canonical Markdown snippets are generated from the registry rather than hand-copied.
- An offline intent-oriented validator detects a missing or wrong identity, policy,
  Python, or license badge and rejects cross-repository workflow and citation targets.
- A networked audit distinguishes existing files from live CI, Codecov, documentation,
  release, DOI, and package surfaces.
- The stale ElastNetMT `enmmt/master` badges are tracked and corrected locally.
- A rollout record shows every member as adopted, excepted with an expiry condition, or
  blocked by a stable local issue.
- The policy and rollout are summarized in `MOLSYSSUITE_GUIDE.md` for component
  contributors.

The normative record is `devguide/repository_badges.md`; the central offline validator is
`devtools/scripts/repository_badges.py`. Closure still requires component adoption,
networked capability evidence and promotion of the mature check into the common gate.

## Local implementation issues

- `uibcdf/molsysmt#185` owns the missing CI workflow target and non-green continuous-test
  history exposed by the priority audit.
- `uibcdf/molsysviewer#88` owns the hosted CI failures and lack of trustworthy current
  coverage exposed by the priority audit.
- `uibcdf/lindelint#5` owns the declared documentation URL that returns 404 and the
  deployment workflow with no recorded run.
- ElastNetMT still requires a local issue before its later incubating-member adoption
  because its current badge targets are already known to be stale.

Other component issues should be created only where the rollout finds a concrete local
change that cannot be applied as part of the mechanical badge-adoption commit.

## Dependencies and risks

The role vocabulary may be contentious around PyUnitWizard, SMonitor, and auxiliary or
incubating repositories. A role must remain a documentation aid, not silently
change package ownership or technical policy applicability.

Dynamic badges can report the last completed run rather than the exact default-branch
revision, and external services can return a successful image for stale data. The policy
must document this limitation and retain direct links to the authoritative service page.
Static Shields rendering adds an external availability dependency but no authority over
the claim. If a future requirement demands self-hosting or a custom logo, generate pinned
assets with a maintained renderer rather than returning to handwritten SVG geometry.

## Provenance

Measured on 2026-09-17 from the twelve checkouts registered in `suite.toml`, all on
`main`. `suite_status.py` reported eleven clean/current repositories and one unrelated
untracked notebook in TopoMT. GitHub measurements used authenticated `gh` against the
`uibcdf` organization. Host: Linux 7.0.0-28-generic x86_64; repository policy version
`1.0`, policy release `policy-v1.1.5`.
