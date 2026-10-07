---
summary: Provide reusable selective environment generation and checked Conda management.
issue: uibcdf/molsyssuite#108
status: active
opened: 2026-10-07
closed:
verification: measured
area: [governance, tooling, compatibility]
guard: tests/test_conda_environment_tools.py
normative:
blocked_by: []
supersedes: []
---

# Shared Conda environment operations

**Reported:** 2026-10-07 during PharmacophoreMT #10's distribution review.
**Status:** Shared operations implemented and locally measured; immutable hosted qualification and first consumer adoption pending.

## What

Provide explicitly invoked reusable generation and create/update operations that
keep shared Python/dependency contracts intact. Keep component-specific tooling,
scientific/native bootstrap conditions, source contexts and output selection in
the owner. This extends development tooling, without adding an automatic CI lane,
publication action, new dependency floor or release version.

## How

Reuse the qualified dependency_constraints and source/context operations. Separate
pure validation/document generation from checked manager invocation and thin owner
CLIs. Generate only explicitly selected environment documents from metadata and
owner tooling; validate every prospective output before writes and offer a
non-mutating drift check. Never parse/dump a Jinja recipe as plain YAML, rewrite a
plan/Git manifest or infer science from a dependency declaration. Preserve existing
Python restrictions and bound complete minor/routine/source-context selections.

Invoke Conda/Mamba with an argument vector, checked exit status, strict priority,
an explicit new name or verified active prefix, temporary cleanup and no import
side effects. Document applicability, unsupported expressions/owner review, direct
API/CLI contracts and qualified immutable adoption. Existing local callers retain
their behavior until an explicit reviewed migration.

## Why

PharmacophoreMT's current broadcaster can replace recipe identity, host/runtime
and Python controls using an outdated nested list. Its helpers run at import,
replace Python constraints and ignore manager errors. LinDelINT #13 and ElastNetMT
#18 repaired analogous helpers locally; duplicating those operations for a third
consumer would create another implementation of the same contracts.

## What is measured and what is assumed

Source inspection at PharmacophoreMT `e1cbe7b48e8804a528bee0b3f176ce329e99c3a2`
finds raw Jinja recipe YAML loading/writing, unchecked shell subprocess calls and
import-time actions. Qualified local reference controls at ElastNetMT
`638354fad54e11eda93e92ddb26159619cb13c8f` have fourteen executed administrative
guards plus hosted independent governance. LinDelINT #13 provides another reviewed
local reference. These are owner-specific implementations, not an accepted common
operator. No real Conda environment operation or scientific compatibility result
is inferred.

## Alternatives and refuted paths

A copied sibling helper leaves multiple implementations to maintain. Removing
special scientific restrictions or rebuilding Conda environments without review
is not an accepted migration. Manually maintained environment files plus existing
shared preflight remain the interim reviewed route; broken legacy helper output
cannot authorize a candidate.

## Scope and exclusions

Actual current need: PharmacophoreMT #10. Candidate reuse: ElastNetMT #18 and
LinDelINT #13; later ordered review: TopoMT #78. Identify additional consumers
from registered inventories before any broader rollout. Optional capability only;
scientific algorithms/native builds, publication credentials, automatic release
choices, installed artifacts and source-free public closure are separate.

## Acceptance criteria

- Reusable documented independently tested operations over existing proof APIs.
- Selective metadata/tool/context generation, all validation before writes,
  non-mutating drift mode and protected recipe/plan/Git/specialized-file scope.
- Whole-minor/routine/source-context proof without silently widening a selector.
- Explicit manager/target identity, argument vectors, checked status, strict
  priority, cleanup and inert imports, with negative guards.
- Qualified immutable SDK, prospective impact/consumer notice and first owner
  adoption with independently executed administrative evidence.
- Separate configuration/adoption evidence from real environment, science,
  candidate/install/public proof. The eventual guard names the shared module's
  runnable regression target; no closure guard is invented before implementation.

## Local implementation issues

- uibcdf/pharmacophoremt#10: current helper replacement and thin owner selection.
- uibcdf/elastnetmt#18, uibcdf/lindelint#13: potential reuse; current local controls
  remain intact until adoption.
- uibcdf/topomt#78: candidate applicability to inspect during the later review.
- uibcdf/molsyssuite#45: distribution coordination remains partial.

## Dependencies and risks

Legacy output remains unqualified for candidates. Actual source-free environment
checks and scientific dependency/native restrictions still require owner evidence.
Do not use an administrative check to clear scientific CI debt.

## Provenance

Inspection and current administrative work: Linux, qualified
`molsyssuite@uibcdf_3.14`, Python 3.14.7, accepted dependency SDK
`2d32048457c6d37093ae509f5626d00a5cda121b`. Seven existing workspace closure
conflicts remain tracked under uibcdf/molsyssuite#82.

## Implementation checkpoint — 2026-10-07

The additive module `devtools/scripts/conda_environment_tools.py` provides pure
selective generation, drift checking, whole-minor selection and explicit checked
Conda/Mamba creation/update over the existing @3 context and range APIs. Contract
and owner profile are documented in `devguide/conda_environment_tools.md`. Twelve
executed regression tests pass in Python 3.14.7, including non-mutating invalid
inputs, protected/unselected files, source drift, strict argument-vector manager
failures, active-prefix identity and temporary cleanup. No real environment was
created or updated; scientific/native and publication evidence remain separate.

Prospective notice before publication/adoption:

- Provider: https://github.com/uibcdf/molsyssuite/issues/108#issuecomment-6033131377
- PharmacophoreMT (actual need): https://github.com/uibcdf/pharmacophoremt/issues/10#issuecomment-6033132774
- ElastNetMT (candidate): https://github.com/uibcdf/elastnetmt/issues/18#issuecomment-6033133169
- LinDelINT (candidate): https://github.com/uibcdf/lindelint/issues/13#issuecomment-6033133535
- TopoMT (candidate): https://github.com/uibcdf/topomt/issues/78#issuecomment-6033133922

Candidates retain their accepted local tools/pins. First adoption is still owed
to PharmacophoreMT #10; no broader automatic migration or guide distribution is
inferred. This additive SDK tool guide is provider-local documentation rather
than a new canonical component-facing governance requirement. Existing SDK
consumers are opt-in and unaffected until they change their pin/call.
