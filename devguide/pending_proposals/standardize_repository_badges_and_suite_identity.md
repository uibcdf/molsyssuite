---
summary: Standardize repository badges and MolSysSuite role identity.
issue: uibcdf/molsyssuite#23
status: open
opened: 2026-09-17
closed:
verification: measured
area: [governance, documentation, automation]
guard:
normative:
blocked_by: []
supersedes: []
---

# Standardizing repository badges and MolSysSuite role identity

**Reported:** 2026-09-17, while publishing the gh-run-receptor documentation and
comparing its README with pytest-receptor and the other registered members.
**Status:** Open; the inventory and candidate policy are documented, but the role
taxonomy, exact badge design, applicability rules, and rollout have not been accepted.

## What

Define a suite-wide policy for the badges displayed at the start of member README files.
The policy should make repository identity and maintained capabilities comparable without
claiming evidence that a repository does not have.

Every registered member should carry one centrally governed MolSysSuite identity badge
with exactly one human-facing role:

- `scientific component`: MolSysMT, MolSysViewer, TopoMT, PharmacophoreMT, and ElastNetMT;
- `support library`: SMonitor, ArgDigest, DepDigest, and PyUnitWizard;
- `developer tool`: Pytest Receptor, GH Run Receptor, and Lindelint.

These display roles are a proposal, not an accepted reclassification. They are distinct
from stabilization cohorts and from the multiple technical profiles already assigned in
`suite.toml`. The registry, rather than README prose, should become their authority.

The badge row should then use a small common order:

1. MolSysSuite membership and role;
2. MolSysSuite policy conformance;
3. continuous tests or CI, when a continuous workflow really runs them;
4. Codecov coverage, when current coverage is uploaded for that repository;
5. documentation deployment, when a public documentation site is maintained;
6. latest release, when the repository publishes GitHub Releases;
7. supported Python versions, for the `python-library` profile;
8. license;
9. optional DOI and installation-channel badges backed by maintained public records.

The first, second, seventh, and eighth items form the expected identity baseline for
Python members once the policy workflow is adopted. The other items are capability
badges: absence must not be disguised by a static green badge.

## How

Add a normative `devguide/repository_badges.md` after the design is accepted and register
the policy in `suite.toml`. Give every member one `display-role` value independent of its
existing `profiles`. The normative document should define:

- exact badge labels, order, link targets, colors, and accessible alt text;
- applicability and the documented exception mechanism;
- what live evidence authorizes each dynamic badge;
- which badge links to the workflow and which links to the user-facing result;
- how prereleases, repositories without releases, and incubating members are presented;
- how stale, renamed, moved, or retired services remove a badge.

Prefer three centrally owned static SVG identity badges generated from one source and
committed under a stable path in `uibcdf/molsyssuite`. This permits use of the existing
MolSysSuite logo, avoids making identity depend on a third-party badge renderer, and
prevents each component from choosing its own wording or colors. Each badge should carry
text as well as color and link to a public MolSysSuite page explaining membership and
roles. A Shields.io prototype remains useful for evaluating dimensions and wording, but
should not become the authority merely because it is quick to compose.

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

The proposed three-role assignment and the choice to host custom SVGs centrally are
design recommendations. They have not yet been tested with maintainers or rendered at
README scale.

## Alternatives and refuted paths

- One identical `MolSysSuite` badge without a role is simpler but loses the distinction
  that motivated the identity work and makes the badge little more than an organization
  label.
- Encoding roles only through color was rejected because it is inaccessible and unclear
  when badges are copied outside GitHub.
- Reusing stabilization cohorts (`wave-1`, `infrastructure`, `incubating`) as public roles
  was rejected because cohorts describe delivery timing, not what a repository is.
- Deriving the one display role mechanically from existing multi-valued profiles was
  rejected because profiles describe policy applicability and do not form an exclusive
  public taxonomy.
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

The proposal applies to every repository registered in `suite.toml`, with profile-based
and capability-based conditions. It covers the README badge row, central identity assets,
machine-readable role authority, validation, exceptions, and coordinated rollout.

It does not require every repository to adopt Codecov, publish documentation, create a
release, mint a DOI, or distribute through Conda or PyPI. It does not redesign component
logos or turn stabilization cohorts into branding. GitHub repository topics, taglines,
and homepages are related public metadata but remain outside this first badge policy.

## Acceptance criteria

- One exclusive display-role vocabulary and assignment is accepted for all registered
  members and recorded in `suite.toml`.
- A normative badge policy defines baseline, conditional badges, ordering, links,
  accessibility, evidence requirements, and exceptions.
- Three centrally owned MolSysSuite role badges are rendered and reviewed at README scale.
- Canonical Markdown snippets are generated from the registry rather than hand-copied.
- An offline intent-oriented validator detects a missing or wrong identity, policy,
  Python, or license badge and rejects cross-repository workflow targets.
- A networked audit distinguishes existing files from live CI, Codecov, documentation,
  release, DOI, and package surfaces.
- The stale ElastNetMT `enmmt/master` badges are tracked and corrected locally.
- A rollout record shows every member as adopted, excepted with an expiry condition, or
  blocked by a stable local issue.
- The policy and rollout are summarized in `MOLSYSSUITE_GUIDE.md` for component
  contributors.

The future `normative` record is expected to be `devguide/repository_badges.md`; the
future `guard` is expected to be the central offline badge validator. Exact names remain
open until implementation begins.

## Local implementation issues

None opened yet. Acceptance of the central design should precede mass issue creation.
ElastNetMT will require a local issue because its current badge targets are already known
to be stale. Other component issues should be created only where the rollout finds a
concrete local change that cannot be applied centrally.

## Dependencies and risks

The role vocabulary may be contentious around PyUnitWizard, SMonitor, and auxiliary or
incubating repositories. A display role must remain a documentation aid, not silently
change package ownership or technical policy applicability.

Dynamic badges can report the last completed run rather than the exact default-branch
revision, and external services can return a successful image for stale data. The policy
must document this limitation and retain direct links to the authoritative service page.
Custom central SVG assets add an asset-versioning responsibility; immutable release paths
or backward-compatible stable paths should be evaluated before rollout.

## Provenance

Measured on 2026-09-17 from the twelve checkouts registered in `suite.toml`, all on
`main`. `suite_status.py` reported eleven clean/current repositories and one unrelated
untracked notebook in TopoMT. GitHub measurements used authenticated `gh` against the
`uibcdf` organization. Host: Linux 7.0.0-28-generic x86_64; repository policy version
`1.0`, policy release `policy-v1.1.5`.
