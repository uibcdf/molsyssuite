# MolSysSuite coordination

MolSysSuite is the authority for policies and contracts shared by two or more member
repositories. Implementation details that affect only one component remain in that
component's repository.

Before filing or closing a defect or proposal, read
[`devguide/reporting_protocol.md`](devguide/reporting_protocol.md). Open the GitHub issue
first, then create the developer-guide record from `devguide/templates/report.md`.

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

Repository-specific tools and workflows remain local unless a suite policy explicitly
makes a tool or procedure common. Shared policies must state their applicability and must
provide a documented exception mechanism.

Run the offline governance guard before committing:

```bash
python devtools/scripts/validate_governance.py
```
