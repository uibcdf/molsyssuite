# MolSysSuite coordination

MolSysSuite is the authority for policies and contracts shared by two or more member
repositories. Implementation details that affect only one component remain in that
component's repository.

Before filing or closing a defect or proposal, read
[`devguide/reporting_protocol.md`](devguide/reporting_protocol.md). Open the owning GitHub
issue first. Create a developer-guide record from `devguide/templates/report.md`
when durable analysis or a decision history is needed; a small finding may need
only the issue.

`MOLSYSSUITE_GUIDE.md` is the canonical component-facing summary of these rules. Every
member keeps a byte-identical root copy and requires it from its root `AGENTS.md`.
All canonical integration guides and their consumers are registered in `suite.toml`;
check or distribute them with `devtools/scripts/sync_vendored_guides.py`, never by
editing consumer copies.

Before cross-repository work, run `python devtools/scripts/suite_status.py`. It fetches
the registered component remotes and reports dirty, ahead, behind, missing, or
upstream-less checkouts without modifying their worktrees.

New Python components must be admitted in `suite.toml` and generated through the
versioned process in [`devguide/new_component_starter_kit.md`](devguide/new_component_starter_kit.md).
Do not begin from an arbitrary existing repository or an untracked private template.

Cross-repository references use `uibcdf/<repo>#<number>`. Do not use paths into sibling
repositories as stable identities.

Read [`devguide/cross_component_feedback.md`](devguide/cross_component_feedback.md) when
one component exposes a limitation in another. Report the need with consumer evidence
to the provider repository and cross-link local work; do not leave it only as a local
workaround.

For a fix in another owner's repository, follow that policy's contribution
route: issue for a need, owner-reviewed PR for a proposed fix, or an explicitly
authorized route for urgent work by or directly with Diego or Liliana. Existing
authorization for the same work remains valid within its scope; do not ask again.

Before publishing or rolling out a shared provider change with plausible consumer
impact, follow the shared-provider notice rule in that policy: update the impact
issue, identify consumers from registered inventories and send an actionable handoff
to their owning issues. Keep notice, adoption and tested artifact evidence separate.

Repository-specific tools and workflows remain local unless a suite policy explicitly
makes a tool or procedure common. Shared policies must state their applicability and must
provide a documented exception mechanism.

Run the offline governance guard before committing:

```bash
python devtools/scripts/validate_governance.py
```

For routine Linux Python development and tests, use the qualified
`molsyssuite@uibcdf_3.14` Conda environment from `devtools/conda-envs/` and
install participating eligible local clones with `python -m pip install
--no-deps --editable PATH`. Verify Python 3.14, dependency closure and import
origins before testing. Follow [devguide/development_workspace.md](devguide/development_workspace.md)
for bootstrap, native builds, current eligibility and tracked exclusions.

## Direct pushes and local validation

Follow [the CI checkpoint policy](devguide/python_ci_policy.md#direct-push-decisions-and-validation-checkpoints)
for authorized internal direct pushes. Batch focused local commits when remote
visibility is unnecessary; use a permitted interim skip only conditionally.
Choose local checks by affected code, inputs and scope, retaining completed
results while they remain applicable. Normally finish with an unskipped head
and inspect its applicable CI, or explicitly execute and verify its gates
manually. Record missing evidence and its recovery owner; do not clear full-suite
debt with administrative checks. PR, admission and publication gates require
executed exact-candidate evidence, including through the authorized manual route.

## Modular reusable tools

Before adding a feature, inspect existing tools and identify the owning module or
component. Implement or extend independently useful operations as documented reusable
tools in that owner, with their own contracts and tests; have consumers call them.
Keep task-specific decisions local and report missing sibling capabilities to the
provider with linked consumer evidence. Follow
[MOLSYSSUITE_GUIDE.md#modular-reusable-tools](MOLSYSSUITE_GUIDE.md#modular-reusable-tools)
for applicability, compatibility, performance and tracked exceptions.

## Temporary development resources

Follow [the resource lifecycle policy](devguide/temporary_resources.md). Keep
task ownership clear, retain temporary resources/evidence while needed and remove
them when their usefulness ends. Review retained resources at closeout; preserve
active/human work and caller-owned environments, and report cleanup failures.

## Durable working instructions

Keep technical findings in their owning issues, fixes, tests and maintained
guidance. Place only accepted lasting contributor actions in the appropriate
root or nested instructions, following
[MOLSYSSUITE_GUIDE.md#durable-working-instructions](MOLSYSSUITE_GUIDE.md#durable-working-instructions).
For work under `devguide/`, also read [devguide/AGENTS.md](devguide/AGENTS.md).
