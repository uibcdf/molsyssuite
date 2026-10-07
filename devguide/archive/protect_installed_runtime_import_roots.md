---
summary: Protect all declared installed import roots against pytest source paths.
issue: uibcdf/molsyssuite#110
status: resolved
opened: 2026-10-07
closed: 2026-10-07
verification: reproduced
area: [governance, distribution, tooling]
guard: tests/test_installed_imports.py
normative: devguide/noarch_conda_workflow.md
blocked_by: []
supersedes: []
---

# Installed runtime imports across package roots

**Reported:** 2026-10-07 from uibcdf/dockingmt#47.
**Status:** Shared provider accepted; consumer/artifact adoption remains owned separately.

## What

Pytest's inherited pythonpath can restore source even with safe-path Python and
importlib collection. A cached installed primary can hide source imports from
an addon because the previous guard checks only the primary package.
File-resource checks do not establish the actual runtime import origin.

## How

Add reusable root-selection and loaded-origin operations in installed_imports.py.
Derive primary/additional Python roots from reviewed resources; an optional
import_roots list may add roots but cannot omit declared Python payload.
Check loaded roots/descendants and all namespace paths before/after tests;
avoid eagerly importing optional integrations. Clear inherited pytest pythonpath
and enforce importlib collection after component arguments. Preserve reviewed
administrative helper subprocesses and exact producer/archive bindings.

## Why

DockingMT and TopoMT carry addons. Receiving evidence must refer to installed
code. A common operation protects other distributions without copied workarounds.

## What is measured and what is assumed

Three actual-runner subprocess regressions fail before the fix: source pythonpath
selects the source addon; cached source addons and addons loaded during tests
wrongly pass the primary-only guard. Corrected behavior accepts the installed
case and rejects both source cases. Other guards exercise explicit roots,
argument precedence, namespaces/descendants, unknown origins and symlink escape.
These are synthetic prefixes, not scientific artifacts or Conda installations.
Final local/hosted counts and immutable delivery are recorded at acceptance.

## Alternatives and refuted paths

The receiving pythonpath override alone cannot reject cached/injected source
addons. Eager imports would force optional integrations/dependencies. Check
loaded modules without claiming unexecuted optional integrations were tested.

## Scope and exclusions

Shared provider, resource review, reusable API/tests and documentation. Existing
immutable callers keep their pins; artifact rollout is separately owned.
No scientific dispatch, dependency installation, release/version selection,
existing-file reconstruction or package build/upload/promotion.

## Acceptance criteria

- Actual-runner failing-before/passing-after regressions protect the mechanism.
- All declared loaded roots, descendants and namespace paths are checked.
- Optional integrations and reviewed administrative subprocesses stay usable.
- Existing noarch/publication tests and exact-head central hosted gates pass.
- Deliver immutable provider and actionable notices from maintained inventories;
  distinguish provider qualification, consumer adoption and installed artifacts.

## Local implementation issues

Initial consumer uibcdf/dockingmt#47 retains its bounded override. TopoMT
uibcdf/topomt#78 and uibcdf/elastnetmt#18 are candidate addon consumers. Maintained shared-publisher
inventory lists ArgDigest, Ackredit, Pytest Receptor, GH Run Receptor, LinDelINT,
ElastNetMT, PharmacophoreMT, TopoMT and DockingMT. Other/local publishers are not
automatically migrated; affected released qualifications remain unknown.

## Dependencies and risks

Unusual path-dependent helpers need a reviewed equivalent preserving origin
checks. Checkpoint observations are not adversarial-unload/tamper attestation.
Historical evidence stays intact. #102 private acquisition affects separate
global audits. Accepted workspace #82 conflicts are unchanged.

## Provenance

2026-10-07, Linux x86_64, molsyssuite@uibcdf_3.14, Python 3.14.7,
pytest 9.1.1, Ruff 0.16.5. Receptor imports originate from eligible local clones;
pip-check retains the same seven #82 conflicts. No environment changes.

## Local qualification and advance notices — 2026-10-07

Twelve new regression tests and 58 focused installed/noarch/operator cases pass.
The existing actual published-launch administrative-helper regression remains
included and passes. Ruff lint/format pass. Three selected actual-runner
regressions demonstrably fail before the implementation (saved local log) and
pass afterward. No scientific artifact or environment is installed.

Review of the nine immutable publisher-inventory sources derives all primary
roots, plus molsysviewer_topomt, molsysviewer_elastnetmt and
molsysviewer_dockingmt in the three addon distributions. Root selection passes
for every reviewed inventory; this is declaration evidence, not loaded scientific
or archive qualification. Primary sibling clones are not edited.

Advance notice is delivered to all nine owner issues and this issue before
provider publication. Local acquisition receipts are retained for final handoff;
immutable provider and exact hosted results follow separately.

## Accepted immutable provider and guard relevance — 2026-10-07

Provider `948d0267de8fa43c542ab7eba28b9f8b7fbf095e` passes independently
verified native governance 37602443801: exact event/workflow/source/attempt,
both jobs and required executed steps agree; 428 tests, publication controls
and dependent coverage upload pass. Twelve new guards and 58 focused local
checks protect runtime-root selection, actual before/after import origins and
pytest argument precedence. The three original actual-runner failures are
regressions in tests/test_installed_imports.py, proving relevance as well as
selector addressability. Existing published administrative-helper launch passes.

All nine registered owner issues received advance notice; the receipt keeps
exact reviewed source inventories and notice URLs. TopoMT, ElastNetMT and
DockingMT declare extra addon roots; declaration review does not certify their
loaded scientific behavior. Accepted workflow identity is the same provider
commit with .github/workflows/test-installed-noarch-conda.yaml. Existing caller
pins and exact producer/file/digest evidence are unchanged; subsequent optional
adoption/real installed qualification stays in their existing owner issues.
No universal migration, scientific dispatch or package mutation was performed.

Receipt: devguide/rollouts/installed_import_roots_110_20261007.json.
The explicit DockingMT receiving override remains compatible. Removing any
consumer guard requires its owner to qualify the actual selected installed
candidate using the accepted provider; historical qualifications are preserved.
