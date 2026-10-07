# Temporary development resources

## Applicability and ownership

This policy applies to all repositories registered in `suite.toml`, their
contributors and applicable development, test, documentation, build and
qualification tools. MolSysSuite owns the member policy under
`uibcdf/molsyssuite#104`; `uibcdf/moli#61` coordinates the platform boundary.

Use `/tmp` or another suitable temporary location when appropriate. Give each
task's resources identifiable ownership. Retain resources while they are needed,
and remove them when their useful lifetime ends. Evidence may remain in `/tmp`
for follow-up or failure analysis; relocation is not required.

## During a task

Prefer managed temporary directories for disposable tests and tooling. Reuse
standard lifecycle support such as `tempfile.TemporaryDirectory` or the owner's
existing equivalent. Cleanup must run after success and failure and must report
errors. A shared operation belongs in its provider; a component chooses which
task-specific resources and evidence it still needs.

Keep output receipts outside a disposable working directory when the operation
must remove that directory on exit. Their destination may itself be `/tmp`.
Do not delete an output still needed for verification or remove a caller-owned
directory as a side effect of a reusable operation. A deliberately persistent
development environment has its own lifecycle.

## At task and release closeout

Review resources created or retained by the task. Remove obsolete test/build
outputs, extracted packages, disposable environments, documentation builds and
task-specific caches after their last required use. A completed release does
not justify keeping an entire disposable environment indefinitely.

Retain only resources that still have a use, with their owner and follow-up
purpose clear in the working record when the task spans sessions. Preserve
the original package identity and required evidence. Remove evidence when it
is no longer needed; existing issue/receipt retention contracts still apply.

Before removal, check ownership, active use and human changes. Review old
resources by explicit paths, not by a global age/prefix deletion rule. Handle
registered Git worktrees through Git after preserving changes. Do not delete
another session's resources, shared environments or system-private directories
without the responsible owner's authorization. Cleanup failures remain visible
and owned until resolved.

## Exceptions and implementation review

Resources still needed are ordinary retention under this policy. A tool that
cannot yet provide required lifecycle handling records a bounded implementation
exception in its owning issue: affected operation/resource, reason, responsible
owner, interim retention/cleanup procedure, review date and removal condition.
Cross-link a shared-provider limitation with consumer evidence using the
cross-component feedback protocol.

Guide synchronization proves instruction delivery. Review each applicable
tool's resource lifecycle separately; source inspection, executed cleanup and
retrospective owner cleanup are different evidence. No scientific suite is
required merely to update this policy or its synchronized copies.
