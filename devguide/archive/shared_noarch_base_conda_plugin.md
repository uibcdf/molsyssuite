---
summary: The shared noarch publisher uses the qualified active Conda build executable.
issue: uibcdf/molsyssuite#80
status: resolved
opened: 2026-10-03
closed: 2026-10-03
severity: high
verification: inspected
area: [distribution, tooling, ci]
guard: tests/test_conda_release_contract.py::CondaReleaseContractTests::test_shared_noarch_build_uses_qualified_active_environment_provider
normative:
blocked_by: []
supersedes: []
---

# Named publisher environment did not supply the base Conda build plugin

## What and ownership

Pytest Receptor run 37111808160 fails before archive production with
`conda: error: argument COMMAND: invalid choice: 'build'`. The named publisher
contains conda-build but the shell invokes the base manager. Uploads skip;
that run never registered a package. The same defect is provider-owned in
uibcdf/action-build-and-upload-conda-packages#46, with shared adoption #78 and
component delivery uibcdf/pytest-receptor#32. Temporary workaround review was
tracked in uibcdf/pytest-receptor#34; it is not evidence of its deployment.

## Resolution — 2026-10-03

The accepted provider `8da628d9b393e184c3bf3722708b19dcfbf7ef0a` selects
`command conda` from the active environment. Shared publisher
`2fb344525ca0eea817dc24a518f4a6bf26e311cf` retains upload-free building,
recipe tests, inspection and separate immutable upload receipts.

The native jobs of Pytest Receptor producer 37136074225 and Ackredit producer
37136075066 actually execute the build, recipe tests, archive inspection and
verified staging upload. Source and receipt bindings are retained in
`devguide/rollouts/release_pipeline_92.json` and
`devguide/rollouts/installed_noarch_88_89.json`. The previously failed native
conclusions remain failure. Public promotion and component runtime tests are
distinct evidence, not prerequisites for proving the repaired executable.

## Guard relevance and provenance

The selected central guard rejects the old shared build-action reference and
requires the qualified provider while keeping building free of upload. The
provider owns the runtime shell/plugin reproducer and native real-build
qualification; see the #78 archived adoption record. Native producer job/step
JSON and digest-bound receipts were independently read on 2026-10-03.
The central guard is addressable in the offline governance validator.
