---
summary: Direct adoption-status execution imports a foreign editable devtools namespace.
issue: uibcdf/molsyssuite#153
status: resolved
opened: 2026-10-28
closed: 2026-10-28
severity: medium
verification: reproduced
area: [governance, tooling]
guard: tests/test_governance.py::VendoredGuideSynchronizationTests::test_adoption_entrypoints_use_owner_checker_with_foreign_devtools
normative:
blocked_by: []
supersedes: []
---

# Adoption-status owner-local imports

**Reported:** During PeptideMT receiving in uibcdf/molsyssuite#152.
**Status:** Fixed; exact published central gate and final handoff are retained in #153.

## What and how

The documented direct `python devtools/scripts/adoption_status.py --help`
command failed before argument parsing in the named shared development profile.
A participating editable distribution supplies a foreign `devtools.scripts`
namespace. The qualified package import raises ImportError for a missing
check_repository; the former fallback caught only ModuleNotFoundError.
A foreign module or regular package could also be imported instead of the owner.

Use the same explicit package/direct distinction already implemented by the
central checker and guide synchronizer. Module execution uses a relative import;
direct execution imports the sibling from Python's script directory. Do not
catch arbitrary implementation import errors, mutate sys.path or repair a
foreign installation to make the command work.

## Why

Administrative adoption commands must load their own checker in the documented
editable development workspace. Reporting a stale guide or missing caller must
remain a truthful inventory result, not an unrelated import crash.

## Evidence and regression

At parent 3a584fc535502751ba82756c9c86a769410a1478, the actual named-environment
command exits 1 with the reported ImportError. The new fresh-process regression
fails before the fix for all three foreign inputs: an empty namespace, poisoned
namespace modules and a poisoned regular package. After the fix, direct help
succeeds and actual selected policy inventory returns valid JSON plus the
expected nonzero --check exit for a missing caller. Module execution retains the
same results against foreign namespaces. Python's module resolution selects a
foreign regular package before this entry point runs; that separate interpreter
behavior is not represented as fixed.

All 20 affected synchronization/adoption tests pass with pytest-receptor, as do
Ruff format/check and the offline governance guard. The regression names the
actual mechanism, including read-only inventory behavior and failure status;
no new science or broad package-workspace qualification is claimed.

## Scope and provenance

2026-10-28, Linux, molsyssuite@uibcdf_3.14, Python 3.14.7. Both receptor imports
resolve to their existing local sibling sources. The twelve known pip-check
findings remain unchanged under #135; no dependency, guide, caller or policy
release is modified. Temporary fixtures are owned and cleaned by their contexts.
The immutable published commit and exact native administrative gate are retained
in the owning issue at closeout.
