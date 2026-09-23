# Component release-version policy

## MOLI ownership note

This document is the **MolSysSuite release profile** for the MOLI public release-version baseline. The platform owner is `uibcdf/moli` (`devguide/policies/release_version_policy.md`). MolSysSuite retains historical-tag inventories, suite policy-release distinctions, and member-specific enforcement.

This document is normative for every repository registered as a MolSysSuite component.
It defines the public release identity shared by source tags, GitHub Releases, packages
and archival records.

## Canonical public identity

A public component release version has exactly three dot-separated, non-negative decimal
integers without leading zeroes except for zero itself:

```text
X.Y.Z
```

The complete accepted pattern is:

```text
^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$
```

The project or package version, Git tag and GitHub Release tag are the same exact string.
Do not add a `v` prefix. Do not publish alpha, beta, release-candidate, development,
post-release or local suffixes, including `a`, `b`, `rc`, `.dev`, `.post` or `+local`.
GitHub prereleases are not a MolSysSuite release channel.

Examples:

- accepted: `0.1.0`, `1.0.0`, `12.4.23`;
- rejected: `v1.0.0`, `1.0`, `01.0.0`, `1.0.0rc1`, `1.0.0.dev1`,
  `1.0.0.post1`, `1.0.0+local`.

## Candidates and development builds

Candidate evaluation uses staging channels, exact commit identities and evidence rather
than a public prerelease version. A candidate version supplied to staging still uses
`X.Y.Z`, but staging does not create or imply a public Git tag or GitHub Release.

A source checkout between releases may derive a truthful PEP 440 local identity such as
`1.2.3+4.gabc1234`; a dirty checkout may add `.dirty`. These strings describe development
build provenance and are not public release versions. They must not appear as the tag or
declared version of a published MolSysSuite release.

## Other versioned identifiers

This contract applies to component release identity, not every string containing a
version. In particular, it does not rename:

- MolSysSuite governance references such as `policy-v1.4.1`;
- third-party Action references such as `actions/checkout@v4`;
- schema, serialized-contract or API versions;
- Conda build numbers; or
- exact tool pins used by development environments.

These identifiers must remain explicit enough that they cannot be mistaken for a
component release.

## Historical tags

Never move or delete a published historical tag merely to satisfy this prospective
policy. `suite.toml` carries the closed inventory of nonconforming historical component
tags observed when this policy was adopted. The common gate accepts only those exact
repository/tag pairs; a new entry requires a central issue, evidence that the tag already
predated adoption, and review as governance debt. The inventory is not an exception for a
future release.

## Automation and release procedure

Python components deriving versions from Git configure their version provider's effective
tag-to-version parser with the exact canonical pattern and fail when it does not match.
For Versioningit this is `tool.versioningit.tag2version.regex` together with
`require-match = true`; an unknown or inert VCS key is not evidence. Static project
versions must themselves match the canonical pattern. Release workflows subscribe only
to stable release events, never `prereleased`.

The common repository gate checks project metadata, the dynamic tag filter, release-event
triggers and fetched Git tags. Component policy workflows run on every tag push so a
nonconforming tag produces immediate failed evidence. Publication workflows remain
responsible for comparing the event tag, built metadata and intended release version
before writing to a registry.

## Exceptions

A component cannot silently choose another public format. A temporary exception requires
a central issue, a documented reason and an expiration condition under the repository
ownership contract. Maturity, auxiliary membership and maintenance mode do not create an
implicit exception.
