# Operating an existing staged noarch release

Implementation follow-up: uibcdf/molsyssuite#92. This administrative capability
applies to staged `noarch-python` members using the shared native publisher.
It reuses the existing [publication contract](conda_publication_policy.md) and
[noarch workflow](noarch_conda_workflow.md); reviewed local equivalents and
documented exceptions keep their existing routes. It adds no internal-push gate.

## Normal path

1. Commit the component's reviewed release plan, resources and thin callers.
   Qualify the original candidate through its declared source gates and dispatch
   its staging wrapper once. Retain the successful producer run ID.
2. Use a clean isolated clone at the **original producer candidate**. Choose a
   reviewed workflow branch/tag and its full qualification commit. Usually these
   identify the same candidate. That commit must also exist in the local clone.
3. Run the administrative entry point from a reviewed immutable MolSysSuite
   clone, using the qualified Python environment with PyYAML/Jinja2/packaging:

   ```bash
   python /path/to/reviewed/molsyssuite/devtools/scripts/noarch_release.py \
     --root /path/to/original/component --repository uibcdf/COMPONENT \
     --producer-run-id PRODUCER_RUN --qualification-sha QUALIFICATION_SHA \
     --workflow-ref REVIEWED_BRANCH_OR_TAG --output installed-handoff.json
   ```

   The tool derives filename, digest, version and original producer identity
   from native receipts. `next_command` is an argument array for the existing
   `gh workflow run`; no command is executed by the tool. Review the receipt
   and dispatch that installed wrapper. Retain its native run ID.
4. Repeat the same entry point with `--installed-run-id INSTALLED_RUN` and
   `--promotion-workflow .github/workflows/COMPONENT_PROMOTION.yaml`. It verifies
   the complete existing installed matrix and emits the existing promoter's
   arguments. After the owner's release decision, dispatch that promoter once.
   The promoter reacquires source gates and verifies installed evidence before
   any registry mutation; a prepared handoff is not an upload permission.
5. Recheck with `--installed-run-id INSTALLED_RUN --verify-public`. Retain its
   public receipt alongside the native promotion/effect receipts. Installed
   matrices, main-label/index availability and consumer runtime adoption prove
   different facts. A normal clean public installation remains separate.

`GH_TOKEN` may supply read-only GitHub credentials; otherwise the tool uses the
existing `gh auth` login. It needs no registry secret. Receipt JSON is printed
and written to `--output`. Failure exits nonzero with `state=unverified` and
provides no dispatch command. The tool does not install packages or run tests.

The initial operator adapter checks the shared staging job's executed steps,
one bounded native receipt ZIP, and callers pinned to full shared commits which
forward each generated input unchanged. Custom orchestration requires a
reviewed adapter or retains its existing tested local equivalent.

The standard adapter also rejects additional required caller inputs that it
does not generate, before emitting a dispatch command (`uibcdf/molsyssuite#101`).
This includes required inputs with defaults: the bounded adapter does not
silently choose component-specific gate evidence. Optional extra inputs retain
their current behavior. For example, ArgDigest's independent minimal-core gate
requires `core_run_id`; use its maintained local route until a reviewed adapter
binds that evidence explicitly. The opt-in reviewed profile below now provides
that adapter; the existing local route remains available. Retain that gate and
the complete matrix.
Read-only verification of an already public file remains supported and emits
no dispatch, irrespective of a component's additional preparation inputs.

## Optional additional component gates

Under the accepted decision in #92, the operator supports reviewed data profiles
in `devtools/noarch_gate_profiles.toml`. There is no new required component gate
or mandatory operator migration. `load_gate_profile` selects a repository-owned
profile and `verify_additional_gates` checks its source/guard/native evidence;
no component Python verifier or scientific code is imported/executed centrally.
The native checks reuse `verify_installed_matrix.verify_native_gate`, which
supports an exact title, complete expected job set and event as optional bounds.
Its existing source-CI callers keep their prior selected-job behavior.

For a component promoter with an additional core gate, supply the profile and
the actual completed run identity:

```bash
python devtools/scripts/noarch_release.py \
  --root /path/to/original/argdigest --repository uibcdf/argdigest \
  --producer-run-id PRODUCER_RUN --installed-run-id INSTALLED_RUN \
  --qualification-sha INSTALLED_QUALIFICATION_SHA \
  --promotion-sha REVIEWED_PROMOTER_SHA --workflow-ref main \
  --promotion-workflow .github/workflows/promote_conda_package.yaml \
  --gate-profile argdigest-core-v2 --gate-run core_run_id=CORE_RUN \
  --output promotion-handoff.json
```

Three source identities have separate jobs: the original producer identifies
package bytes; `qualification_sha` identifies the installed workflow/evidence;
`promotion_sha` identifies the actual promoter caller selected by `workflow_ref`.
The latter defaults to the qualification source for existing users. A separate
promotion source requires installed evidence; it does not replace the candidate
or installed qualification. A moved dispatch ref produces no command.
ArgDigest's reviewed guard requires `main`, so its profile rejects another
dispatch ref. Source-bound caller/guard changes require a reviewed profile
refresh, rather than an implicit default or generic extra-input flag.

Select the profile whose reviewed input blobs match the actual producer and
promoter. `argdigest-core` retains the original 0.14.0 review unchanged;
`argdigest-core-v2` adds the independently reviewed 0.15.0 probe contract.
Both retain the same required local guard, file/source bindings and complete
matrix. The latter adds explicit-pipeline and lower-bound capture-refusal checks
to the existing NumPy-free probe. A later release can use a profile only while
its recorded source inputs match; a version name alone is not qualification.
The v2 read-only checkpoint verifies original public bytes, the full installed
matrix and twelve core jobs without providing a new dispatch command. Receipt:
`devguide/rollouts/argdigest_core_profile_v2_92_20261008.json`.

Each profile records its owner issue and immutable reviewed sources,
`caller-inputs` (hashes at the promoter source), `producer-inputs` (hashes at
the original candidate), the shared promotion job and the prior local guard
which consumes each additional run input. Gate records fix native workflow,
digest-bearing file title, matrix job template, platform/runner mapping and
executed required steps. Matrix dimensions derive from the candidate release
plan. Required input/default choices are explicit; additional inputs cannot
overwrite standard source/file fields. A removed, conditional, tolerated or
unconnected guard fails preparation. Every required native job/step, source,
file title and attempt must match; incomplete, failed or mixed evidence fails.

The component retains its actual verification immediately before promotion.
A prepared central receipt does not waive that verification or authorize a
mutation. `--verify-public` can include the same profile to inspect an already
published file and its additional gate; it emits no publication command.
An unknown profile/input or source drift leaves the standard fail-closed/local
route. Another explicitly reviewed catalog can be selected with `--gate-profiles`;
its path/digest is retained in the receipt. Such selection is not an automated
review or permission to relax a component gate. Use the existing owner issue
and impact handoff when adding/updating a profile for another member.

The ArgDigest checkpoint independently verifies the existing producer, installed
matrix, twelve core cells and exact public file without rerunning or promoting
anything. Primary receipt:
`devguide/rollouts/release_gate_profiles_92_20261004.json`.
`tests/test_noarch_gate_profiles.py` protects invalid gate evidence, removed
dependencies, explicit promoter/installed identities and no repeat promotion.
An ordinary future release must still provide the operator-effort observations
described below; this read-only checkpoint does not establish that comparison.

## Recovery for already registered bytes

Keep the successful producer run and original candidate. Correct administrative
workflow/tooling through the owning repository and select its explicitly reviewed
full qualification commit and branch/tag. Run the same entry point against the
original candidate clone. Never change the archive, recipe, original scientific
selection or package source to repair an administrative qualification failure.

An existing successful installed run can be supplied directly; verification
does not execute its tests again. A changed test selection or package requires
the component's new candidate qualification, not this recovery path.

Every handoff checks current registry identity. If the exact file already has
`main`, the tool requires its installed run, independently verifies public
metadata/index and emits **no next dispatch**. A missing installed receipt,
changed digest, unavailable evidence or public-index inconsistency stops the
operation. After an uncertain mutation, use read-only verification and the
existing owner recovery route; never rebuild or retry a write to obtain green.

GitHub dispatch accepts a branch/tag which may move after this read. The tool
checks its current SHA but cannot freeze a future dispatch. Keep a stable reviewed
ref and verify the resulting native workflow head; the installed-source binding
and promoter will reject evidence for another qualification commit. Historical
receipt artifacts may expire; missing evidence requires owning-tool recovery.

## Evidence for the operator implementation

On 2026-10-03 the tool independently verified both original producer receipt
ZIPs, existing full installed matrices and public hashes for Ackredit 0.9.0 and
Pytest Receptor 1.2.1. See `devguide/rollouts/release_pipeline_92.json`.
Both files were already public: these checks made no mutation, solve or fresh
installed-test claim. Independent provider execution qualification passed all eight hosted cells
in run 37159007278 at `da485db244e2b9039e5302962eeb5fd4f5cd8868`; primary
receipts are in `devguide/rollouts/noarch_install_qualification_92.json`.
A later ordinary-release effort comparison remains pending under #92.


## Independent installed-tool qualification

Maintainers can manually dispatch `.github/workflows/qualify-noarch-install.yaml`
from a reviewed immutable provider source. It uses frozen local catalogs of two
verified public archive versions to reproduce strict-priority exclusion, real
Conda dependency solving, the exact registered staging URL and outside-source
provider smoke checks on eight declared cells. The workflow also executes the
actual shared scientific-launch and administrative-child regressions. It does
not rebuild/upload packages or execute component scientific suites. Catalogs
are controlled fixtures; this run certifies the exercised installation tools
and contexts, not an independent new live release.

## Recording a later ordinary release

Retain component/version, original candidate, provider pins, producer, installed
and promotion run IDs, failed/repeated runs with reasons, manual operator steps,
start/end timestamps and separately measured active operator time. Link native
receipts and record whether this entry point was used. Compare like scopes with
the bounded historical sample; native elapsed time alone does not measure human
work. Select any improvement target only after recording that comparison.
