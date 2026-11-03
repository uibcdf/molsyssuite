# Optional frontend DOM-test review

This unqueued worksheet is for __REPOSITORY__ when it acquires a frontend panel
or scientific addon. It makes no implementation/adoption claim. With no such
boundary, leave it unused; no Node installation or new CI job is required.

Use the [MolSysSuite optional pattern](https://github.com/uibcdf/molsyssuite/blob/main/devguide/frontend_dom_tests.md)
and [shared-tool catalogue](https://github.com/uibcdf/molsyssuite/blob/main/devguide/shared_tools.md).
Open or reuse the owning issue under the local [reporting protocol](reporting_protocol.md)
for concrete adoption work. A qualified local route may remain in use.

## Owner and execution route

- Owner issue, reviewed source commit and local maintainers:
- Panel modules and actual code-loading/extraction mechanism:
- Source versus installed-archive scope; archive/digest and origin checks if applicable:
- Reviewed Node/Python, development-only dependencies, lockfile and action revisions:
- Direct test command, meaningful assertions and CI events/job:
- Production backend fixture/module drift checks and their existing Python lane:

Keep generic widget/comm/rendering with MolSysViewer and molecular operations
with their provider. The component owns panel meanings and assertions. A small
test model is not a replacement provider. Do not copy production JavaScript into
tests or install unused scientific dependencies for a DOM-only extraction route.

## Isolation and evidence

- Context/window and callback cleanup on success/failure; handler/cleanup error propagation:
- Independent instances, repeated mounting and owned subscription cleanup:
- Missing/error/zero/unit/identity state and action semantics:
- Actual local and hosted results, source/workflow/run/attempt and tool identities:
- Useful retained resources, owner, removal condition and review date:
- Remaining real comm/browser/pixels/camera/C6/scientific/publication gates:

Preserve failed outcomes and existing scientific/full/recovery/release gates.
DOM success is only its declared interface scope. Local results or a generated
workflow do not establish hosted or installed execution. No shared DOM library,
Node version, coverage floor or harness is mandated by this worksheet.
