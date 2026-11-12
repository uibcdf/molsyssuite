---
summary: Receive canonical GitHub SSH origins for normal directory installations.
issue: uibcdf/molsyssuite#178
status: resolved
opened: 2026-11-12
closed: 2026-11-12
verification: reproduced
area: [tooling, distribution]
guard: tests/test_directory_source_contexts.py
normative:
blocked_by: []
supersedes: []
---

# Canonical SSH origins in directory-source contexts

**Reported:** BindingMT #100 retains actual source-context refusals under #178.
**Status:** Provider extension and local qualification complete; published-source
native proof and consumer receiving are retained in the owning issue.

## What

Central `e5270b858c0ce4d16913059762133fb802e7fa8d` only accepts HTTPS origins.
The source follows its declared profile, but normal directory installations from
ordinary GitHub SSH clones cannot qualify. Before this extension, four of five
new test methods fail at that original refusal; negative origin cases already
refuse correctly. No earlier failure is relabeled as receiving.

## How

Normalize only the observed local directory `origin`: exact scp-style
`git@github.com:OWNER/REPO[.git]` or `ssh://git@github.com[:22]/OWNER/REPO[.git]`
maps to its existing HTTPS identity. Require exactly two literal path segments;
reject credentials, alternate users/hosts/ports, ambiguous/traversing/encoded
paths, query/fragment and configured whitespace. Git output removes only its
final newline, preserving configured leading/trailing/newline characters for
refusal. Compare the result with the still-HTTPS declaration.

Keep full commit, root checkout, tracked/untracked cleanliness, installed version,
actual PEP 610 directory and normal-install requirements. Editable metadata stays
excluded. Public Git-install metadata and pinned Git acquisition stay HTTPS-only.
This local identity comparison does not attest a remote server or native bytes.

## Why

The central SDK owns this reusable capability. Consumers should receive a reviewed
extension rather than rewrite their actual remotes or fork the private checker.
The existing source/artifact/public/scientific gates retain their owners.

## What is measured and what is assumed

Published Pytest Receptor 1.2.3 records 59 passing selected tests, zero skips, in
directory/source provenance and legacy/context dependency-route modules. Five
new methods exercise accepted SSH identities, nineteen negative origin forms,
existing commit/cleanliness/metadata refusals, actual context dispatch and a real
offline pip normal install into an owned target. The latter reads real generated
PEP 610 metadata and does not install into the shared prefix or import science.
The passing local fixture is provider qualification, not BindingMT receiving.

## Alternatives and refuted paths

- Broadening `repository_url` would also accept new transports for public/pinned
  Git acquisition. The reviewed need is confined to local directory origins.
- Mutating real clone remotes or using synthetic HTTPS provenance would not
  qualify the actual consumer context. Only owned test fixtures are changed.
- Arbitrary SSH hosts, usernames, aliases, credentials or ports are unnecessary
  for the reported canonical GitHub forms.

## Scope and exclusions

One source-provenance operation, meaningful actual-Git/installation regressions
and its technical SDK contract. No new schema, source cohort, Python admission,
environment switch, member pin, remote/config change, package/policy release or
scientific execution. The #82 pause and deferred scientific work are preserved.

## Acceptance criteria and guard relevance

The guard module reproduces the original refusal, compares actual equivalent
origins and retains adverse controls. It exercises the extended mechanism rather
than merely naming a runnable test. The real pip fixture proves the normal
installation/metadata boundary locally; the contextual test exercises the public
auditor. Other Git/source/legacy/context tests retain their original behavior.
Ruff, generated indexes, offline governance and whitespace must pass before
publication. Exact hosted jobs/steps and owner handoff follow in #178.

## Local implementation issues

Provider work: uibcdf/molsyssuite#178. Actual SDK pin/context adoption remains
uibcdf/bindingmt#100; its retained failures are not independently replayed or
superseded by this central fixture. No component source is edited here.

## Dependencies and risks

Identity normalization is not authentication. Keep the distinction between
declarations, actual installed metadata, remote origin and qualified artifacts.
No new dependency or runtime requirement is added.

## Provenance

2026-11-12 local, Linux/Python 3.14.7 in the named shared environment. The host's
twelve known pip-check findings remain separate. Published receptor bytes are
verified in an isolated target; primary editables and user work are preserved.
[Normalized source, baseline and result receipt](../rollouts/ssh_directory_origins_178_20261112.json).
Task resources are positively owned and retired after durable proof; #171 uses
the same task root next, without expanding cleanup to other sessions.
