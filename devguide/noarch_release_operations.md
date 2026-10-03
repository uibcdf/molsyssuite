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
installed-test claim. Independent provider execution qualification and a later
ordinary-release effort comparison remain pending under #92.
