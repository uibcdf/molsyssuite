---
summary: Standardize public component release versions and tags as X.Y.Z.
issue: uibcdf/molsyssuite#32
status: active
opened: 2026-09-21
closed:
verification: inspected
area: [release, packaging, governance]
guard:
normative:
blocked_by: []
supersedes: []
---

# Public component releases need one unambiguous version identity

**Reported:** 2026-09-21, while reviewing whether the component-facing governance guide
actually prohibited `vX.Y.Z` tags and prerelease suffixes.
**Status:** Active proposal while the normative policy, common gate, starter kit and
component rollout are implemented.

## What

Require every public MolSysSuite component release and its corresponding Git and GitHub
Release tag to use exactly three numeric components: `X.Y.Z`. The version and tag are the
same string. Prefixes such as `v` and PEP 440 or SemVer suffixes such as `a`, `b`, `rc`,
`.dev`, `.post` and `+local` are not public release identities.

This is a release rule, not a prohibition on truthful development-build provenance. A
checkout between releases may report a local identity such as `1.2.3+4.gabc1234`, and a
dirty checkout may add `.dirty`; neither may be published or represented as a release.

## How

Define a central release-version policy with one exact regular expression and register it
in `suite.toml`. Summarize the rule in `MOLSYSSUITE_GUIDE.md`, configure the Python starter
kit to derive versions only from conforming Git tags, reject prerelease release-event
triggers, and extend the common repository checker to inspect both version configuration
and Git tags.

The reusable conformance checkout must fetch tags, and every component policy caller must
run on tag pushes. Existing nonconforming historical tags are retained as immutable
archive identities and enumerated centrally; the allowlist is closed and cannot admit a
new spelling accidentally.

MolSysSuite governance tags such as `policy-v1.3.1` are excluded because they identify a
policy artifact rather than a component release. Third-party Action references such as
`actions/checkout@v4` are also outside the contract.

## Why

The canonical guide currently describes releases and DOI evidence without defining a
release identifier. The starter template uses `0.1.0.dev0`, many versioningit
configurations accept every tag, and several release workflows listen for
`prereleased`. A convention inferred from recent tags is not a policy and cannot protect
new components or automated publication.

## What is measured and what is assumed

Measured on 2026-09-21 from fetched local clones: every current component's recent public
tags uses three numeric components. PyUnitWizard retains ten beta-era tags and MolSysMT
retains five beta-era tags that do not. No other registered component has a nonconforming
Git tag. The measurements used `git tag --list` and the proposed exact pattern against all
thirteen registered component checkouts.

Inspected configuration initially showed all twelve then-registered Python components
deriving versions with versioningit, but only ElastNetMT and Lindelint declared a
numeric-leading tag filter, and that filter was not exact. The generated starter instead
carried a static `0.1.0.dev0` version. Multiple Conda and Zenodo workflows explicitly
subscribed to the `prereleased` event.

Ackredit was admitted concurrently as the thirteenth component with a conforming static
`0.5.0` version and five canonical historical tags. Its first hosted run correctly showed
that `policy-v1.4.0`, published immediately before the admission commit, could not know the
new repository. Patch release `policy-v1.4.1` includes the admitted registry state; every
component caller must use that release before this rollout closes.

Assumed: historical tags remain useful archival identities and should not be deleted or
moved. The policy therefore controls future release behavior without rewriting history.

The SMonitor 0.16.0 rollout exposed a conformance-gap in the first `policy-v1.4.0`
checker. `PYTHONPATH=. python devtools/scripts/check_repository.py --repository
uibcdf/smonitor ../smonitor` reports `RELEASE_TAG_FILTER` because it requires the literal
`tool.versioningit.vcs.tag-filter` value. SMonitor instead uses versioningit's effective
`tool.versioningit.tag2version.regex` with `require-match = true`; its
`tests/test_release_version_identity.py` exercises acceptance of canonical tags and
rejection of prefixes, incomplete versions, leading zeroes, prerelease, development,
and local suffixes. Adding a `vcs.tag-filter` key merely to satisfy the checker would
not prove runtime filtering. The same command also reports `RELEASE_POLICY_GATE` because
SMonitor still calls the previous `policy-v1.3.0` workflow. Rollout should validate the
provider's effective tag behavior, then advance the caller to a corrected shared gate;
it must not require inert configuration as evidence. This is separate from SMonitor's
verified Python 3.14 package admission under `uibcdf/molsyssuite#29`.

## Alternatives and refuted paths

- **Treat this as an undocumented convention.** Rejected because the starter and release
  workflows already encode conflicting behavior.
- **Allow both `vX.Y.Z` and `X.Y.Z`.** Rejected because two spellings create needless
  normalization and mismatches among package metadata, tags, assets and DOI records.
- **Allow release candidates.** Rejected because the suite has chosen staging channels
  and candidate evidence rather than public prerelease version identities.
- **Forbid local development metadata.** Rejected because commit and dirty provenance is
  useful and is not a public release claim.
- **Delete historical beta tags.** Rejected because immutable historical references must
  be preserved; a bounded legacy inventory is safer.

## Scope and exclusions

The rule applies to public releases of every registered component, independent of role,
membership, maturity or development mode. It covers the package/project version, Git tag
and GitHub Release tag.

Excluded: central MolSysSuite policy-release tags, third-party Action references, schema
versions, file-format versions, API-contract versions, Conda build numbers and transient
development-build metadata. Candidate staging versions still use `X.Y.Z`, but staging
does not itself create a public release.

## Acceptance criteria

- A normative central document defines the exact format, equality rule, exclusions,
  development-build distinction, historical-tag treatment and exception process.
- `suite.toml` exposes the rule and its bounded historical inventory.
- `MOLSYSSUITE_GUIDE.md` states the rule without requiring contributors to infer it.
- The starter kit no longer generates a prerelease version and accepts only exact release
  tags for version derivation.
- The common offline gate rejects nonconforming static versions, permissive dynamic tag
  filters, prerelease event triggers and unregistered nonconforming Git tags.
- The reusable gate fetches tags, and component policy callers run for tag pushes.
- Every current component passes the accepted gate; component copies of the guide are
  byte-identical to the canonical source.

## Local implementation issues

None unless a component cannot adopt the mechanical rollout without a repository-local
exception. The central issue owns the uniform configuration change.

## Dependencies and risks

The open coordinated Conda proposal `uibcdf/molsyssuite#27` uses stable three-part
candidate versions and is compatible with this rule. Release automation must not confuse
external Action refs beginning in `v` with component release tags.

## Provenance

Inspection performed 2026-09-21 in the registered sibling checkouts after
`devtools/scripts/suite_status.py` fetched their remotes. No package build, tag mutation or
release operation was performed.
