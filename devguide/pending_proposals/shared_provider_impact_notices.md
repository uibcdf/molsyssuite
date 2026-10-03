---
summary: Track shared-provider impact notices and their consumer adoption inventory.
issue: uibcdf/molsyssuite#79
status: active
opened: 2026-10-03
closed:
verification: inspected
area: [governance, distribution, tooling]
guard: tests/test_python_distribution_status.py
normative: devguide/cross_component_feedback.md
blocked_by: []
supersedes: []
---

# Shared-provider impact and adoption notices

**Reported:** 2026-10-03, provider handoff and maintainer review.
**Status:** Active; the maintainer has accepted the rule for all shared providers.
Normative guidance and starter instructions are implemented; member delivery and
its measured audit remain in progress.

## What

uibcdf/moli#39 requests an explicit impact-notice route for shared auxiliary
providers. During uibcdf/molsyssuite#78 adoption, the maintainer identified a
governance gap: consumers of the shared Conda publisher should be available from
a maintained list, with their references, rather than discovered afresh for each
notice. This record retains that concrete implementation under the existing
owning issue; it does not close its broader guidance work.

## How

`suite.toml` registers `devguide/rollouts/conda_publishers.json` under the existing
Conda publication policy. The inventory covers every registered member plus
MolSysSuite's own publisher, with exact inspected source, active workflow/job,
provider reference and observed publisher kind. The existing independently
usable `python_distribution_status.py` owns listing, observation and drift checks.
The offline guard rejects omitted/duplicate members, contradictory kinds and
mutable shared-workflow references.

List consumers without examining their worktrees:

```bash
python devtools/scripts/python_distribution_status.py --publishers
python devtools/scripts/python_distribution_status.py --publisher-kind shared-noarch
```

After `suite_status.py` fetches the registered remotes, check the recorded callers:

```bash
python devtools/scripts/python_distribution_status.py --check-publishers WORKSPACE
```

Regenerate the observation when adoption changes, review the diff and commit it:

```bash
python devtools/scripts/python_distribution_status.py --observe-publishers WORKSPACE \
  > devguide/rollouts/conda_publishers.json
```

The observation reads committed `origin/main` through Git, never changes component
worktrees, ignores workflow backups/subdirectories and excludes upload-free
provider qualification steps. It does not fetch, execute CI or notify consumers.
Unrelated source commits do not create caller drift. A notice identifies the
published provider/shared SHA, affected members, migration, qualification evidence
and each member's existing owner issue. Notifications and adoption receipts remain
separate; a list does not certify successful staging or public delivery.

## Why

The accepted Conda contract permits native and metapackage profiles and reviewed
local equivalents. The noarch workflow is a narrower capability. A consumer list
must therefore include local and unobserved routes as well as shared users, so
missing adoption is visible without treating every difference as a defect.

## What is measured and what is assumed

Source observation on 2026-10-03 finds six shared noarch consumers, six member
local publishers, four members with no recognized Conda publisher, and one
central local publisher. Exact full source SHAs and caller references are in the
registered JSON. No public availability or fresh scientific result is inferred.
The scanner recognizes the suite's registered shared publisher and build/upload
provider calls. Other custom implementations require explicit review/extension;
`no-conda-publisher-observed` is an observation within that scope.

Shared consumers are Ackredit, Pytest Receptor, TopoMT, PharmacophoreMT,
ElastNetMT and LinDelINT. Their uibcdf/molsyssuite#78 owner handoffs are listed in
`adopt_qualified_conda_build_environment_correction.md`.

SMonitor, ArgDigest, DepDigest, PyUnitWizard and MolSysViewer have local publishers
and noarch recipes. Their workflow equivalence and potential convergence are
pending member review; pure Python alone does not require migrating an already
qualified local route. MolSysViewer migration remains deferred with its active
team work. MolSysMT has a native profile, and the central publisher handles
metapackages under uibcdf/molsyssuite#67. GH Run Receptor, DockingMT, MolSys-AI and
OpenCASTp have no recognized Conda publishing route in the inspected sources.

## Alternatives and refuted paths

Repeated free-form searches do not provide a maintained adoption list. A second
member list disconnected from `suite.toml` can miss new admissions; the guard
requires complete registry coverage. Requiring the noarch Python workflow for
native or metapackage profiles would contradict the accepted contract. Automatic
package publication does not follow from a provider impact notice.

## Scope and exclusions

The concrete inventory covers Conda publisher adoption. The accepted impact-notice rule covers all shared auxiliary providers, workflows,
actions and canonical guides. Its canonical guide delivery, starter instructions,
provider discoverability and platform feedback complete the broader scope of #79. No component
publisher migration, scientific suite or package release is performed here.

## Acceptance criteria

### Accepted scope — 2026-10-03

The maintainer chose all shared providers: auxiliary libraries, reusable workflows,
development/publication actions and canonical guides. The adopted rule is in
`devguide/cross_component_feedback.md`; the canonical member guide, central root
instructions and starter instructions carry the lasting action. The rule reuses
issues by theme, preserves internal maintainer CI routes and provider ownership,
and provides bounded exceptions. Guide distribution and provider discoverability
are verified before this coordination issue closes.

- Keep complete publisher/consumer identities and references queryable centrally.
- Protect inventory completeness and source observation boundaries with tests.
- Record uibcdf/molsyssuite#78 notices and later member-owned adoption separately.
- Decide and publish the broader impact-notice guidance requested by uibcdf/moli#39,
  distribute accepted instructions and verify provider discoverability before
  resolving this central issue.

## Local implementation issues

The immediate six publication handoffs remain in uibcdf/ackredit#22,
uibcdf/pytest-receptor#32, uibcdf/topomt#78, uibcdf/pharmacophoremt#10,
uibcdf/elastnetmt#18 and uibcdf/lindelint#13. Existing local publisher reviews
remain uibcdf/molsyssuite#45; no new migration is mandated by this inventory.

## Dependencies and risks

Recorded consumers can advance after inspection. Recheck fetched main before
rollout and record actual adopted commits. Provider/consumer notices do not
authorize release decisions. The maintainer approved the broader normative scope before implementation;
future changes that require a new policy choice remain subject to consultation.

## Provenance

### Guide-copy housekeeping — 2026-10-03

GH Run Receptor 1.2.0 is publicly released. The accepted Ackredit guide explicitly
marks its portable API as candidate-only pending public delivery. Their canonical
copies are synchronized through `sync_vendored_guides.py` in 14 isolated component
clones, preserving team work and updating no runtime source. Native full vendored
guide audit [37126830402](https://github.com/uibcdf/molsyssuite/actions/runs/37126830402)
passes. Exact delivery commits are in
`devguide/rollouts/guide_sync_20261003.json`. A copied guide is not runtime or
artifact-adoption evidence. This housekeeping does not resolve the broader #79.

2026-10-03, Linux workspace, Python 3.13.15 and PyYAML. Source inspection uses
read-only Git operations on remotes fetched by `suite_status.py`. The #78
integration is published at `2a2a459cc3795bb92766fffa0fe28f4d80f01ad4`, and hosted
governance run 37125099269 passes its 273 tests on the configured Python 3.14 lane.
