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
