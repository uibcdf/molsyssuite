---
summary: Resolve guide-tool imports from their owner in editable workspaces.
issue: uibcdf/molsyssuite#111
status: resolved
opened: 2026-10-07
closed: 2026-10-07
severity: medium
verification: reproduced
area: [governance, tooling]
guard: tests/test_governance.py::VendoredGuideSynchronizationTests::test_documented_scripts_resolve_owner_modules_with_foreign_devtools
normative:
blocked_by: []
supersedes: []
---

# Guide commands import another editable repository's tools

**Reported:** During the registered guide rollout in uibcdf/molsyssuite#104.
**Status:** Repaired and verified on the published exact source; guard retained.

## What

In molsyssuite@uibcdf_3.14, Python 3.14.7, from the owner root:

```bash
python devtools/scripts/sync_vendored_guides.py --help
```

fails before argument processing: first `ModuleNotFoundError` for
devtools.scripts.check_repository, then `ImportError` for ci_lane_inventory
from a foreign devtools.scripts namespace. The same operation invoked as a
module from the owner root succeeds. Direct check_vendored_guides,
check_repository and repository_badges commands reproduce the same import-chain
problem. The existing suite_status entry point succeeds.

## How

Direct execution places the script directory, rather than the repository root,
first on Python's import path. Absolute package imports consult other editable
devtools namespaces. An exception-based fallback does not establish module
ownership and may fail or silently load foreign tools.

The four affected modules select imports by execution context: package-relative
imports for module use and sibling imports from the script directory for direct
execution. The synchronizer reads the registry through the existing suite_policy
operation. Existing Finding types, registry semantics, selectors, return codes
and source/destination protections remain intact.

## Why

The documented central distribution command must work with the accepted editable
workspace. Uninstalling participating components or changing their namespaces is
not needed to repair the owner's command. Source policy and copied guide bytes
must remain bound to their registered owners.

## What is measured and what is assumed

The actual direct-command failures were reproduced on source
00c1303ef09bcb5b392f15f0fece44f10bd970f5. New subprocess regressions fail before
the repair with deliberately conflicting namespace and regular devtools packages.
The module control already passes before the repair. After repair, all 137
governance tests pass, including 14 guide synchronization tests and three new
subprocess tests. Applicable Ruff lint/import and formatting checks pass.

The real Git fixture uses a local bare origin, published source and committed
consumer copy. The actual CLI reports drift without writing, synchronizes exact
bytes, and rejects dirty consumers, uncommitted sources and unpublished source
heads while preserving the previous content. Managed fixtures are removed after
test completion. These results prove tool behavior, not scientific qualification.

## Alternatives and refuted paths

Only prepending the owner root leaves a namespace package vulnerable to a regular
foreign package later on the import path. Explicit sibling/relative imports avoid
that ambiguity for the supported entry points. No custom importer, package-layout
migration or broad exception catch is needed. No blanket audit or repair of every
central entry point is claimed.

## Scope and exclusions

Central synchronizer and its observed import chain only. This implementation fix
changes no member policy, guide bytes, component dependencies or workflow pins.
Current central guide/audit tools consume it; frozen policy/SDK revisions retain
their original code until independently adopted. Policy-v1.5.8 remains immutable.
Direct use is tested from a neutral directory, including a foreign regular package;
module use is tested from the owner root with the observed foreign namespace.
Resolving a foreign regular package before Python can locate the owner module is
outside this module invocation claim.

## Acceptance criteria

- Documented direct commands resolve owner modules in the accepted workspace.
- Module invocation retains selected-guide behavior.
- Real CLI synchronization preserves exact-byte and Git safety boundaries.
- Local governance/lint/format and exact-source native central gates pass.
- Retain the relevant regression and archive this record at closure.

## Local implementation issues

No member source changes or caller adoption required. Central #104 supplies the
consumer case; #82 retains unrelated development-environment integration debt.
The existing private-access decision in #102 is independent of CLI resolution.

## Dependencies and risks

The seven previously known workspace dependency conflicts remain unchanged;
the relevant receptor imports still originate in their participating local clones.
Do not infer that unrelated entry points or old immutable snapshots are repaired.

## Provenance

2026-10-07, Linux x86_64, molsyssuite@uibcdf_3.14, Python 3.14.7, Ruff 0.16.5.
Before/after local logs are retained while needed in /tmp/molsyssuite111_before.log
and /tmp/molsyssuite111_after.log. No environment, primary sibling clone or
scientific/public artifact was modified for this repair.

## Resolution and qualification — 2026-10-07

The accepted implementation is
75f6feb86d8ac4db6fb4a784b89b67e461336988. Native governance run
[37681806409](https://github.com/uibcdf/molsyssuite/actions/runs/37681806409)
is verified for that exact commit, push event, workflow, both jobs and required
executed governance/test/publication-control/coverage-upload steps. All 431
central tests pass. The documented direct CLI and badge registry operation also
pass from /tmp in the actual qualified editable workspace after the repair.

The declared guard exercises real subprocess resolution with foreign packages
and actual synchronization against a local published Git origin. It failed
before repair at the foreign import boundary, then passed after repair; the
module control already passed. It also proves the unchanged real Git source
and destination refusal behavior, rather than only checking import statements.
The relevant 137 local tests and Ruff checks pass. No new policy rule, frozen
snapshot retag or consumer source migration is part of this resolution.

Applicable hosted guide and dependency audits pass all fifteen public-member
jobs at this source: runs 37681806498 and 37681806410. The private OpenCASTp
checkout fails in both; vendored-guide audit 37681806528 likewise fails before
comparison at its private checkout. These remain genuine independent failures
owned by #102, with no access decision changed or claim of full global success.

All test workspaces and local Git origins use managed TemporaryDirectory
lifecycles. Small diagnostic logs remain while useful. The archive/index and
final unskipped documentation checkpoint complete central issue closeout;
#104's component tool lifecycle reviews and #82's existing workspace debts
retain their separate owners.
