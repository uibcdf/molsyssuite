---
summary: Declare isolated helper and data inputs for installed scientific tests.
issue: uibcdf/molsyssuite#117
status: active
opened: 2026-10-10
closed:
verification: measured
area: [governance, tooling, compatibility]
guard: tests/test_installed_test_support.py
normative: devguide/noarch_conda_workflow.md
blocked_by: []
supersedes: []
---

# Explicit support for installed scientific tests

**Reported:** PharmacophoreMT installed receiving under uibcdf/pharmacophoremt#10.
**Status:** Dedicated namespace accepted by the principal maintainer. Shared
implementation and local regressions pass; immutable hosted handoff is pending.
Consumer helper migration remains locally owned.

## What

Installed tests may legitimately need unshipped owner helpers and data. Existing
`installed_noarch.run_tests` selects source test files with importlib collection,
clears inherited pytest source paths, and checks every declared runtime payload
root before/after execution. It cannot currently provide direct scientific helper
imports without exposing the source tree or mixing an ambiguous `devtools` namespace.

The original consumer evidence at `3424f3ead0ef85ba9245a5edff4c58bb39d5fcfd`
reproduces helper collection failure in isolated tooling with two qualified SDK
pins, while editable finders can hide the gap. The separate source/dependency repair
uibcdf/pharmacophoremt#55 is closed; source science is not installed-artifact evidence.
Delivered import-root guards under uibcdf/molsyssuite#110 remain applicable.

## How: common support contract

Extend the existing runner through an independently reusable owned module,
`devtools/scripts/installed_test_support.py`. Keep owner fixture
choices and science local. A missing support declaration preserves existing behavior.
No component-specific importer or implicit helper discovery is proposed.

Accepted optional input in the committed `resources.toml` inventory:

```toml
[installed_tests.support]
schema = "molsyssuite.installed-test-support@1"
namespace = "phmt_test_support" # example; each owner chooses a distinct name
reason = "Reviewed unshipped scientific test support"

[[installed_tests.support.files]]
source = "phmt_test_support/helper.py"
target = "phmt_test_support/helper.py"
sha256 = "<reviewed 64-character lowercase digest>"

[[installed_tests.support.files]]
source = "tests/data/prepared_ccd/manifest.json"
target = "tests/data/prepared_ccd/manifest.json"
sha256 = "<reviewed 64-character lowercase digest>"
```

The versioned public profile uses the fields above. Pure validation/planning and
managed staging are reusable by other installed/native runners. Copy only
literal reviewed files from the qualification source, validate every digest before
copying, reject paths/symlinks escaping the owner and conflicting/duplicate targets,
and retain their relative staging layout. No wildcard tree copy, auto-rewriting
imports or extraction of arbitrary archives. Selection must not copy scientific
runtime roots/addons into test support or turn data entries into importable code.

Do not add the component root or the staging parent to `sys.path`. Bind only the
dedicated package/namespace with ordinary importlib machinery and its reviewed
search path. Files such as staged `tests/data/...` stay off the general module
search path; selected helper code can read them relative to its staged `__file__`.
Verify helper module origins and selected bytes before/after tests and preserve
existing primary/addon installed-origin checks. Retire private directories and
owned import bindings on success/failure, retaining caller/SDK identities.
This is origin/input validation for trusted tests, not a hostile-code sandbox.

The staged input receipt must distinguish helper/data support from runtime payload:
exact source/file/digests, provider revision, source/qualification/run-attempt
context when present, selected paths, completed checks and cleanup. It must preserve
producer/artifact identity and the existing source binding, not rebuild an archive
or declare helper bytes publicly installed. Unavailable context is explicitly unknown.
Local direct `run_tests` keeps its integer result; the existing CLI may emit an
optional support sidecar without changing exit status or required installed steps.

## Accepted decision: dedicated namespace

### A. Dedicated owner namespace (accepted)

Owners use a distinct support name, such as `phmt_test_support`, for helper imports
and internal helper dependencies. The shared stager exposes only that namespace.
Reject overlap with runtime payload roots, the SDK, standard/test tools or an
already-resolvable package; do not replace loaded caller modules.

Advantages: ordinary Python package imports; clear ownership and bounded origin
checks; reusable for every component; no shared `devtools` bridge or special
PharmacophoreMT code. Relative helper/data layouts can be preserved explicitly.

Cost: the actual owner must review import changes in tests/helpers and any
path-sensitive behavior. The current static closure is 28 helpers, not a license
to migrate or package them automatically. A support name beginning with
`pharmacophoremt` could match its existing setuptools `pharmacophoremt*` discovery;
use a deliberate unshipped location/name or reviewed packaging exclusion.
Source-relative Git/subprocess assumptions may need owner adaptations. Those
scientific fixture decisions remain the component team's work.

### B. Explicit legacy namespace bridge (not selected)

Retain existing `devtools.*` imports with a per-module reviewed bridge to staged
files. Resolve every leaf/package collision with SDK modules; refuse preloaded
consumer/source helpers, undefined aliases and broad namespace/path merging.
All transitive helper modules, namespace parents and data still require declaration.

Advantage: fewer owner import edits. Cost: a more complex shared import resolver,
cache/collision/restoration guards and compatibility surface for a generic namespace
already used by the SDK. Supporting it is a separate contract decision, not a
silent fallback to owner source paths. This route has not been prototyped or qualified.

## Why

The same installed-test boundary affects any component with unshipped helpers.
Explicit owner inputs and a shared loader avoid copied workaround implementations
and keep source tests, runtime package bytes, fixture support and scientific evidence
separate. Neither choice introduces a scientific suite, member dependency floor,
release requirement or mandatory migration.

## What is measured and what is assumed

2026-10-13, qualified Linux Python 3.14.7, both local receptor editable origins
verified, seven accepted #82 closure conflicts retained. After `suite_status.py`,
consumer source `eca174ba3daaf1c6d3ff7e735cae593442d0487b` was current and clean.
A static AST scan finds 23 direct helper-importing test files and 28 transitively
referenced `devtools.*` modules. All 51 recorded file digests match blobs of that
immutable commit. Dynamic imports, full data closure and portability are not inferred.

[Prototype receipt](../rollouts/installed_support_proposal_117_20261013.json)
contains exact prototype driver source/digest and seven actual subprocess controls.
Each invokes current public `installed_noarch.run_tests` under `python -P`, outside
a synthetic component, using synthetic installed runtime/addon records. The prototype
manually binds a dedicated namespace and applies helper/data checks; production
SDK support validation/staging/receipts are not implemented or qualified.

| Control | Actual outcome |
| --- | --- |
| Missing support | Collection fails, exit 2 |
| Dedicated namespace, sibling helper, relative data | Passes, exit 0; source/staging parents absent from `sys.path`, SDK preserved |
| SDK namespace collision | Refused before binding/tests |
| Runtime namespace collision | Refused before binding/tests |
| Source addon loaded during tests | Actual runner rejects installed provenance |
| Helper origin changed to source during tests | Prototype post-check rejects origin |
| Staged data changed during tests | Prototype post-check rejects bytes |

All managed prototype resources are retired after children exit. No real molecular
helpers/data are executed, no shared environment is changed, and no scientific,
Conda/public artifact or full platform matrix is claimed. Other platforms, regular
package initializer behavior, missing/dynamic support inputs and complete lifecycle
cases still require production guards if the contract is accepted.

## Alternatives and refuted paths

- Adding the entire owner root to Python paths exposes molecular source packages.
- Copying all `devtools` exposes undeclared tools and ignores SDK ownership.
- Moving helpers into the public runtime merely to make tests import them changes
  product/dependency semantics without showing a runtime need.
- Copying Python runtime source under a support alias would undermine candidate tests.
- Guessing fixture dependencies or changing import strings in staged copies obscures
  what was executed; owner-reviewed inputs/imports must stay explicit.
- Updating the publication pin alone or reusing source-suite success does not solve
  the isolated installed-helper failure.

## Scope and exclusions

Shared optional support operations, public input/receipt contract, administrative
runner controls and immutable provider handoff. No component source/helper migration,
scientific algorithm or fixture judgment, consumer pin update, candidate/release,
package reconstruction or new common gate. A bounded owner local equivalent remains
available under current guidance until a qualified shared route is adopted.

## Acceptance criteria

1. Principal maintainer chooses dedicated namespace or explicit legacy compatibility.
2. Implement independently reusable validation/staging/origin/lifecycle operations,
   integrated additively into the actual installed runner/resource review.
3. Guard positive direct helper/relative data and negative payload/addon shadowing,
   namespace/cache collisions, missing/hash/path violations and failures/cleanup.
4. Preserve actual source/producer/artifact/run-attempt binding and before/after
   installed-origin checks, optional sidecar identity and existing exit semantics.
5. Document applicability/limits and deliver an immutable qualified provider and
   actionable owner notice. Actual consumer adoption/scientific artifact cells stay local.

## Local implementation issues

uibcdf/pharmacophoremt#10/#23: initial actual consumer; helper selection/import
migration, fixture/path portability and eight-cell candidate qualification remain
owner work. Other member reuse is prospective, not an adoption inventory claim.

## Dependencies and risks

The namespace choice is accepted. A static helper closure does not settle runtime
fixtures or source-sensitive operations. Other owner namespaces/layouts may reveal
unsupported shapes requiring tracked equivalents; this should not force scientific
refactoring through shared governance. Existing exact-byte and installed-root evidence
remains distinct from support origin checks and from scientific correctness.

## Provenance

Existing provider `15360fa0480bd3c6443715713bdf03700b8d5040`; actual consumer
`eca174ba3daaf1c6d3ff7e735cae593442d0487b`; original reproduced gap/receipt under
`3424f3ead0ef85ba9245a5edff4c58bb39d5fcfd` and separate #55 source-dependency repair.
Prototype inputs/driver/results are retained in the linked receipt. Primary owner files and consumer pins retain their bytes. Initial prototype
inputs/measurements remain unchanged; the accepted shared implementation follows.

## Implementation checkpoint — 2026-10-13

The principal maintainer accepted a dedicated support namespace after the prepared
alternatives. `installed_test_support` now owns reusable pure source validation,
managed staging, package/namespace binding, origin/byte checks, import/resource
retirement, source/provider Git blob binding and unshipped payload checking.
No parent source/staging path is added to Python paths and no legacy alias is exposed.
Regular initializer and nested namespace behavior is guarded through actual imports.

`installed_noarch.run_tests` keeps its integer result with optional output/context
keywords. It checks the candidate before support initialization and before/after
tests, retains support checks on failure, and emits the optional sidecar after
retirement. The published tests command preserves original candidate/file/digest,
qualification source and actual run/attempt, with provider identity from
`job.workflow_sha`. Optional per-cell sidecars are retained in run/attempt-qualified
artifacts; no-support calls retain their route and emit no support file. Noarch
resource review validates input declarations and archive inspection rejects an
accidentally shipped support namespace. Existing artifact bytes, descriptors and
scientific required-step names remain unchanged.

Version 1 intentionally qualifies serial in-process pytest, pure Python code and
explicit portable data, with 1024-file, 64 MiB/file and 256 MiB aggregate limits.
Worker execution is rejected for this profile; source/no-support parallel policy
is unchanged. Larger, filtered/LFS, native or source/Git-sensitive fixtures remain
owner-reviewed equivalents or tracked provider extensions. Selected plain Git
bytes are checked against a supplied source commit; absent local source/provider
identity is explicitly unknown. Artifact/qualification/run labels do not replace
the original candidate/source-binding and installed exact-byte gates.

Local qualified Python 3.14.7 runs all 512 central administrative tests successfully
(one explicitly opt-in native Mamba skip). Focused actual-runner, resource and
source-import controls pass, including a Bash invocation of the published command
with original source/digest/attempt labels. Prototype-only code is not closure proof:
these new regressions exercise the actual owned module, actual installed runner and
actual workflow command. Missing/helper hash/path/symlink/size violations, namespace
SDK/runtime/cached collisions, initializer/copy/test failures, source-addon and
helper/data origin drift, source commit mismatches, serial-worker refusal and
accidental artifact payload inclusion are guarded. Every owned support tree/import
binding is retired after failure/success; caller resources remain preserved.

Maintained publisher inventory (`python_distribution_status.py --publisher-kind
shared-noarch`) lists nine registered fixed callers: ArgDigest, Pytest Receptor,
GH Run Receptor, TopoMT, PharmacophoreMT, ElastNetMT, DockingMT, Ackredit, LinDelINT.
That inventory includes historical/suspended routes (notably ElastNetMT's native
transition) and is not a new adoption claim. Only PharmacophoreMT has the concrete
support need measured here; all other reuse is prospective and all pins remain
unchanged. Existing publication/qualified local routes can remain in use.

Before-publication acceptance notice:
https://github.com/uibcdf/molsyssuite/issues/117#issuecomment-6151933913 and
https://github.com/uibcdf/pharmacophoremt/issues/10#issuecomment-6151934614.
Current shared source/API/workflow/guide qualification and immutable handoff will
be recorded there after exact hosted CI. Owner import/data/portability review and
actual eight-cell scientific artifact qualification remain #10/#23; central work
does not move the 28 helpers, rerun source science or reconstruct a package.
