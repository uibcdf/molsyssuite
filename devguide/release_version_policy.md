# Component release-version policy

## Ownership

MolSysSuite owns public release-version rules for its members, including their historical-tag inventory, policy-release distinction and conformance gate. `suite.toml` carries the machine-readable rule.

This profile applies to every repository registered as a MolSysSuite component.

## Public release identity

Member public releases use canonical `X.Y.Z` versions and matching Git tags; new public prerelease tags are disallowed. `suite.toml` provides the anchored parser. MolSysSuite keeps the member enforcement, historical tag inventory and separate `policy-vX.Y.Z` governance-release namespace. Third-party Action refs, schema versions, Conda build numbers and tool pins remain separate identifiers.

The project/package version, Git tag and GitHub Release tag agree. Development
checkouts may carry truthful derived identities, but candidate evaluation uses
staging and exact-commit evidence rather than public prerelease tags.

## Candidate evidence lifecycle

Before tagging or publishing, record a reviewable receipt for every required
gate: the member repository, exact source commit, intended version and route;
gate name, observed result, run link and tested OS/Python or combined scope;
and immutable input identities. Inputs include required dependency metadata and
resolved closure, recipe/build inputs, generated runtime resources, and the
candidate artifact coordinate and digest once built. A combined gate names
every component and artifact it consumed. An unspecified input cannot prove
that earlier evidence still applies.

Changing a source commit, dependency contract or closure, build input,
generated resource, artifact, or tested scope makes every consuming gate stale.
Rerun it for the new candidate and retain the old result as history. An
unchanged gate may be reused only when its complete recorded inputs, scope and
artifact digest, where relevant, are demonstrably unchanged. If one participant
of a combined installed-package gate changes, rerun the combined gate; unchanged
participants need not be rebuilt solely for that reason. Record the reuse and
replacement decisions before publication. Each claimed distribution route
needs its own archive and installed-runtime evidence under the
[distribution policy](python_distribution_policy.md).

## Bounded release-gate exceptions

A failed, skipped, cancelled or tolerated-failure gate keeps its actual result.
If the member's release authority permits an unmet waivable gate, it records a
separate dated **release decision with exception** before publication. The
record names the exact candidate, version, artifact when applicable, gate,
affected capability and scope, observed result and evidence link, compensating
evidence and limits, decision owner, owner-local remediation issue, public
limitation, and expiry or re-decision condition.

The decision applies only to that candidate and scope. It cannot certify an
untested platform, change a failed result into a pass, satisfy a later candidate
or waive a non-waivable scientific or safety gate. An expired exception blocks
the claim until a new decision is recorded. Member repositories define their
specialized gates and decision authority; MolSysSuite may impose additional
release approval and admission requirements.

## Historical tags

Never move or delete a published historical tag merely to satisfy this prospective
policy. `suite.toml` carries the closed inventory of nonconforming historical component
tags observed when this policy was adopted. The common gate accepts only those exact
repository/tag pairs; a new entry requires a central issue, evidence that the tag already
predated adoption, and review as governance debt. The inventory is not an exception for a
future release.

## Archive tags

Accepted under uibcdf/molsyssuite#84, the reserved `archive/<description>`
namespace preserves an experiment or other historical commit without a public
release claim. It applies to registered component repositories; the suffix is
nonempty and the whole name must be a valid Git tag. Record the preserved commit,
purpose and owner in an annotation or an owning issue. Keep an archive tag stable
and do not delete or move an existing tag merely to satisfy conformance.

An archive tag is neither a public package version nor a GitHub Release identity.
It cannot supply release/public-artifact evidence or authorize build, upload or
promotion. Public versions retain the exact `X.Y.Z` parser, metadata/tag agreement
and exact-candidate gates. A later separately qualified canonical release may
reuse a preserved commit; the archive marker itself supplies no authorization.
This namespace does not accept arbitrary noncanonical or prerelease tags and
does not expand the closed historical release inventory.

Archive pushes still run the conformance workflow. Configure an unconditional
caller on all tag pushes, normally with `tags: ["**"]`; `"*"` does not match
names containing `/`. The shared guard rejects a missing/filtered/conditional
capable tag caller with `ARCHIVE_TAG_TRIGGER`. The workflow reader is the
reusable `ci_lane_inventory.load_workflow` operation; it preserves YAML event
keys as strings and refuses unavailable or malformed input. GitHub documents
the wildcard distinction in its
[filter reference](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#filter-pattern-cheat-sheet).
A Python member using this
capability adopts `policy-v1.5.7` or a registered compatible newer caller; the
common checker reports `ARCHIVE_POLICY_GATE` when archive tags coexist with an
older caller. Members without archive tags may keep their compatible policy
pins. Other governed repositories follow their applicable enforcement route.
Published earlier policy tags and their historical failures remain immutable.

Before enabling this capability in a member, inspect its publisher triggers and
version parsers. An archive push must not write to a registry; every publication
route validates a canonical public identity before a registry operation. A
mistaken GitHub Release or dispatch using an archive name must be refused,
including when the commit or package metadata otherwise looks valid. The shared
Conda plan/preflight already rejects a noncanonical version before acquiring
release gates or registry authorization. Local publishers need equivalent
controls and relevant negative evidence. Guide receipt alone does not certify
publisher behavior, scientific compatibility or a public artifact.

## Automation and release procedure

The member gate derives its accepted version parser from `suite.toml` in the called suite policy release.
Components deriving versions from Git configure their effective parser accordingly.

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
