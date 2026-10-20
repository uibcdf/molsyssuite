---
summary: Consolidate the named Python 3.14 editable development workspace and honest integration scope.
issue: uibcdf/molsyssuite#82
status: partial
opened: 2026-10-03
closed:
verification: measured
area: [governance, compatibility]
guard:
normative: devguide/development_workspace.md
blocked_by: []
supersedes: []
---

# Default Python 3.14 editable development workspace

**Reported:** Through uibcdf/molsyssuite#82 and uibcdf/moli#40.
**Status:** Partial; maintained guidance and all sixteen member copies delivered and audited. TopoMT and cross-domain integration remain tracked.

**Current workspace observation, 2026-10-20:** Recorda and Praxis now admit
the latest published ArgDigest 0.16.0, SMonitor 0.21.0 and DepDigest 0.15.1.
Their five metadata conflicts are resolved in the named editable workspace,
with their previous runtime floors preserved. The seven earlier accepted
external findings remain; no new exception or runtime failure is inferred.
Source receiving and the unchanged public Recorda 0.3.0 archive remain separate
(see the dated receiving section below). Shared Ruff remains 0.16.10 against
immutable policy tooling 0.16.5; the current administrative checks use the
existing isolated tooling or exact hosted policy, preserving the shared tool.

## What

Make the named Linux Python 3.14 environment and editable local-clone workflow
unambiguous in current policy, root instructions, canonical member guide and
starter. Keep planned eligibility, measured integration and public/scientific
qualification separate. Preserve active local work.

## How

Reuse the existing `development_environment.py` profile, source inventory,
editable installer and runtime verifier. Change the stale opt-in descriptions,
document interpreter/dependency/import verification and direct tests through the
selected Python interpreter. Use the registry-derived installer rather than a
fixed partial list. Distribute the canonical guide through the registered tool.

## Why

The README and opening issue still describe eight eligible sources, whereas the
current registered profile includes fourteen. The recipe/module still call it
opt-in, although the accepted routine baseline is Python 3.14. These discrepancies
make it unclear how to develop together and which integration remains unverified.

## What is measured and what is assumed

Native run `37135810313` at suite source
`c23dfb7bf95818fbc6a3765c87516232da9461f7` succeeds. Primary retained artifact
`11278797600`, `linux-py314-development-37135810313-1` (43,088 bytes), contains
profile, source, editable, runtime and Conda package receipts. Inspected runtime
evidence records fourteen actual imports, Python 3.14.7 and official Qt 6.11.2.
Its installation/dependency and runtime steps executed successfully; no scientific
test or public release evidence follows. The compact receptor agrees with native
GitHub conclusions. Summary evidence is maintained in
`devguide/rollouts/development_workspace_82.json`.

TopoMT is absent from current transition authorization, not currently rejected by
the common Python metadata rule. Sabueso is outside suite membership and has no
joint fourteen-member integration receipt here. Its current source depends on
Ackredit's development contract; its public 0.9.0 delivery and receiving closure
are now independently reviewed under uibcdf/molsyssuite#51. That does not
establish Sabueso's full joint editable-workspace qualification.

## Alternatives and refuted paths

- A fixed eight-member command would leave newly eligible clones disconnected.
- Connecting arbitrary sources with pip dependencies would bypass the Conda
  closure and component ownership.
- Counting Sabueso as a suite member would change delegated governance rather
  than prove compatibility.
- Running the deferred MolSysMT/MolSysViewer scientific suites is unnecessary
  for this development-environment guidance and integration evidence.

## Scope and exclusions

Linux x86_64 development integration and registered guide consumers. No changes
to component scientific implementations, user environments, CI cadence, public
artifacts, immutable policy tags or OS claims. Direct MOLI adoption and Sabueso
implementation remain with their owners. TopoMT integration and cross-domain
closure remain explicit pending work until separately evidenced.

## Acceptance criteria

- Default environment, valid editable command, interpreter/import verification,
  reinstallation conditions and exceptions are clear in maintained guidance.
- Registered guide consumers and new-member starter receive the same action.
- Exact fourteen-member integration and current exclusions are recorded honestly.
- Return the source, verification and remaining cross-domain integration need to
  MOLI #40; keep any unfulfilled integration acceptance visible.
- Governance and relevant existing environment/starter checks pass.

## Local implementation issues

- `uibcdf/topomt#16` and `uibcdf/molsyssuite#51`: shared-profile integration review.
- `uibcdf/moli#40` and `uibcdf/sabueso#109`: direct-component guidance and joint
  development-environment qualification.

## Dependencies and risks

Editable installations follow live local sources, so later metadata or native
changes can invalidate an earlier import receipt. Automatic profile expansion
does not certify joint integration. Keep fresh receipts and failed probes visible.

## Provenance

2026-10-03 Linux coordination workspace; hosted Python 3.14.7 receipt inspection.
Local administrative tests use the explicit Python 3.14.7 interpreter in
`/tmp/moli31-sabueso-env`, without modifying existing development environments.

## Delivered guidance — 2026-10-03

Canonical source `784c9c228e59319804ee57e8d49f7f4a1f6d5a80` publishes the
workspace contract, aligned default descriptions, root/member/starter actions and
measured fourteen-source receipt. All sixteen canonical copies are delivered and
required through their existing root instructions. Exact delivery commits and
concurrent Ackredit preservation are in the rollout receipt.

Eight existing environment/starter tests pass on Python 3.14.7, along with the
offline governance guard and changed-file Ruff checks. Exact-source native
governance `37137836658`, component-guide audit `37137836542` (17 jobs) and
registered guide audit `37137836549` pass. A subsequent fresh development probe
`37137836610` also succeeds at the published guidance source. Initial guide-audit
attempts ran before delivery; post-delivery reruns pass with history retained.

This does not close the remaining integration criteria: TopoMT is outside current
profile authorization, and joint Sabueso/suite compatibility still needs an
owner-reviewed receipt under MOLI #40. The status stays partial. No scientific
suite was run and no host development environment or public artifact was changed.
The accepted guidance and pending integration are returned to uibcdf/moli#40.

## Latest published provider compatibility — 2026-10-20

The initial installed metadata check found five additional conflicts: Recorda
excluded ArgDigest >=0.16 and SMonitor >=0.20; Praxis also excluded DepDigest
>=0.14. Fresh remote metadata retained those ceilings, so reinstalling it alone
could not resolve them. Liliana decided that these consumers must be compatible
with the latest published providers. Owner work is uibcdf/recorda#24 and
uibcdf/praxis#10, with direct-component coordination in uibcdf/moli#40.

Independent receiving used original public Conda files ArgDigest 0.16.0 py_0,
SMonitor 0.21.0 py_2 and DepDigest 0.15.1 py_0 in a fresh disposable Linux
Python 3.14.8 environment. The provider identity checker validated their
coordinates, digests, origins and 39/40/17 Python files. `pip check` was clean.
Joint editable tests passed 345 Recorda cases with recovery explicitly enabled
and 154 Praxis cases; only the optional real-MolSysMT case was unavailable.
Those results qualify the tested compatibility boundaries, not a consumer
release or a deferred scientific suite.

Source commits `4a94b5dc0a783160335b0e9c18aab7f85e81ab70` (Recorda) and
`6d092a991ab3fd05fdfab4206094cd48d423b1b2` (Praxis) preserve the previous
floors while extending bounded upper limits to include the current releases.
Recorda aligns all five environments and its exact public identity checks.
Praxis retains existing installed recording tests with its legacy cohort and
adds a distinct latest-provider profile: internal pushes use Linux/Python 3.14;
PR, scheduled and manual runs use eight Linux/macOS arm64 × Python 3.11–3.14
cells. Publication preflight rejects a missing full latest-provider matrix.

After verifying both primary clones were clean, they were fast-forwarded and
reinstalled with `pip install --no-deps --no-build-isolation --editable PATH`
in the caller's named `molsyssuite@uibcdf_3.14`. Python 3.14.7, all five provider/
consumer origins and both local receptors were verified. All five new conflicts
disappeared; the original seven external findings remain visible. Recorda passed
345 cases and Praxis passed 156 cases with its real-MolSysMT module explicitly
excluded. Providers, other primary worktrees and the accepted seven exceptions
were not changed.

The immutable public Recorda 0.3.0 archive still carries its old ceilings.
Public-only joint installation with the new cohort therefore needs a separately
authorized new Recorda release; source metadata does not rewrite an existing
file. Optional Recorda omission in Praxis's public latest-provider lane is
explicit, while the joint editable receipt exercises recording. This does not
close TopoMT authorization or broader cross-domain integration criteria; #82
remains partial. Exact local/hosted scopes and remaining ownership are in
[the receiving receipt](../rollouts/latest_public_workspace_cohort_82_20261020.json).

Hosted observation at this checkpoint: all eight new Praxis latest-provider
cells pass with 153 tests and four explicit optional omissions each (Recorda
and real MolSysMT absent). Their retained provider JSON and JUnit ZIP digests
are independently checked. The whole workflows are not yet certified: native
step verification accepts 13 completed Recorda jobs and 18 completed Praxis
jobs, while each `tests (macos-latest, 3.14)` installed cell is still queued with
no runner assigned. Recovery remains with the current owner workflows
`39471202391` and `39471277865`; do not count queued work as executed evidence.

## Hosted recovery and final receiving — 2026-10-20

The two previously queued macOS/Python 3.14 jobs subsequently received runners
and passed on their original attempts. Complete exact-source native verification
now accepts all fourteen Recorda jobs in `39471202391` and all nineteen Praxis
jobs in `39471277865`, including every declared mandatory executed step;
Praxis's separate governance `39471278501` also passes. The historical queued
observation above is preserved. uibcdf/recorda#24 and uibcdf/praxis#10 close
the requested source/development receiving scope with links to their unchanged
runtime guards and dated receipts. No new public consumer release is claimed.

Central checkpoint `05126c54d45a118db966070d1c42b2198713820c` passes all
seven applicable workflows with independently verified required jobs/steps:
governance/coverage, member guides, registered vendored guides, dependency
manifests, relationship labels, Zenodo and fresh fourteen-member development
integration. Trusted Linux run `39472963178` creates the public-channel Conda
profile, installs its fourteen source editables, checks dependency closure and
verifies source imports/official Qt. Three bounded sanitized public receipts
retain source identities and successful checkout/install/runtime results, with
private checkout/stdout details withheld by the existing access wrapper.

This fresh suite-only profile result complements the separate local Recorda/
Praxis receiving; neither is relabeled as a combined sixteen-component
qualification. TopoMT authorization and the remaining broader direct-MOLI joint
integration criteria remain open. Public Recorda 0.3.0 remains immutable and
needs a future owner-selected new release for public-only latest-cohort installs.
#82 stays partial for those separate scopes, with its five additional local
metadata conflicts resolved and the original seven external findings retained.

## Explicit next-publication owner — 2026-10-20

[uibcdf/recorda#26](https://github.com/uibcdf/recorda/issues/26) is now the open
follow-up for a new release carrying the source compatibility accepted in
uibcdf/recorda#24. It records the provider cohort, existing preparation evidence,
new-version/exact-artifact gates and public-only installation gap. It is
cross-linked from this issue, uibcdf/moli#40 and uibcdf/praxis#10. Recorda owns
version and timing; the original 0.3.0 archive remains unchanged. After public
receiving, Praxis can qualify that new optional public recording package.

Coordination is paused at the user's request; see the
[current checkpoint](../CHECKPOINT.md) for completed evidence and resumption.
