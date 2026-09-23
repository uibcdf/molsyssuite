# Component release-version policy

## MOLI ownership note

This document is the **MolSysSuite release profile** for the MOLI public release-version baseline. The platform owner is `uibcdf/moli` (`devguide/policies/release_version_policy.md`). MolSysSuite retains historical-tag inventories, suite policy-release distinctions, and member-specific enforcement.

This profile applies to every repository registered as a MolSysSuite component.

## Inherited public release identity

The accepted public version format, Git tag identity and prerelease rule are defined only in [MOLI’s pinned release-version policy](https://github.com/uibcdf/moli/blob/a92fafbc22423f078ab1a8534bda589b41bc5c64/devguide/policies/release_version_policy.md) and its pinned `moli.toml`. MolSysSuite keeps the member enforcement, historical tag inventory and separate `policy-vX.Y.Z` governance-release namespace. Third-party Action refs, schema versions, Conda build numbers and tool pins remain separate identifiers.

## Historical tags

Never move or delete a published historical tag merely to satisfy this prospective
policy. `suite.toml` carries the closed inventory of nonconforming historical component
tags observed when this policy was adopted. The common gate accepts only those exact
repository/tag pairs; a new entry requires a central issue, evidence that the tag already
predated adoption, and review as governance debt. The inventory is not an exception for a
future release.

## Automation and release procedure

The member gate derives its accepted version parser from the pinned MOLI registry.
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
