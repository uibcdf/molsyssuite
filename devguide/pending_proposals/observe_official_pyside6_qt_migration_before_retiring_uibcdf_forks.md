---
summary: Observe official PySide6/Qt adoption before considering retirement of the UIBCDF forks.
issue: uibcdf/molsyssuite#57
status: active
opened: 2026-09-27
closed:
verification: measured
area: [packaging, compatibility, coordination]
guard:
normative:
blocked_by: []
supersedes: []
---

# Observe official PySide6/Qt adoption before considering fork retirement

**Reported:** 2026-09-27 after clean-environment PySide6/Qt 6.11.2 probes
for the coordinated public MolSysMT/MolSysViewer pair.
**Status:** Active; Linux feasibility is demonstrated, but the observation
period and platform gates remain open.

## What

Coordinate a suite-level transition away from requiring the five UIBCDF
PySide6/Qt fork packages. Retain their repositories, tags and packages during
an observation period. Any archive or retirement decision must be explicit
and subsequent to consumer, CI, development and release evidence.

## How

MolSysViewer implements canonical-first selection under
`uibcdf/molsysviewer#109`; its platform wording is tracked in
`uibcdf/molsysviewer#97`. The central Linux Python 3.14 development recipe
in `uibcdf/molsyssuite#52` should adopt canonical Qt after its own clean
solve and smoke tests. Inventory all five fork references in recipes,
workflows, docs, package metadata and supported environments. Run native
Windows and macOS ARM tests, decide the macOS Intel route explicitly, then
observe at least one later release candidate with no required fork dependency.
Keep exact test and rollback coordinates in the component records.

## Why

The UIBCDF fork stack addressed a real WebEngine packaging limitation, but
five coordinated native builds cost substantial time and complicate upgrades.
Official 6.11.2 now looks viable on Linux. The shared development and
support implications are larger than the Viewer loader alone, so MolSysSuite
owns the collective observation and retirement decision.

## What is measured and what is assumed

Measured 2026-09-27 on Linux x86-64: clean Conda environments with public
`molsysmt=0.22.4` and `molsysviewer=0.23.4` plus conda-forge
`pyside6=6.11.2`, `qt6-webengine=6.11.2`, and `qt6-positioning=6.11.2`
resolved on Python 3.11–3.14 and passed real WebEngine transport and
two-generation payload delivery. With modified Viewer source, the complete
standalone test file passed 42 tests with two graphical/GPU skips on Python
3.14. The manually dispatched Viewer [CI run
36338541516](https://github.com/uibcdf/molsysviewer/actions/runs/36338541516)
passed 7/7 at commit `19dadc1a0adb1ff7477fe9e7866e807b015c8f36`,
including the Linux Xvfb Qt pipeline using canonical 6.11.2. This still
does not verify framebuffer correctness. Windows `win-64` and macOS ARM
`osx-arm64` resolved in Conda dry runs
only. The `osx-64` Conda solve failed because conda-forge lacks Qt WebEngine
6.11.2 there; official PyPI publishes a macOS universal2 wheel, but no Intel
runtime test has been done. Apple lists macOS 27 for Apple-silicon Macs only,
while macOS 26 still receives security maintenance. None of this decides
MolSysSuite's macOS Intel policy.

Assumed, not yet proved: that all MolSysSuite consumers can relinquish the
fork, that official Qt works on the target native Windows/macOS hosts, and
that a full release candidate can run without needing the fallback.

## Alternatives and refuted paths

Immediate deletion of the fork repositories was rejected: it would erase
rollback capacity before native and release gates. Keeping the fork as the
default despite successful official-stack probes would retain build cost
without a demonstrated need. A solver-only platform result is not a GUI
runtime certificate. Retiring macOS Intel merely because macOS 27 excludes it
would conflate an Apple OS support change with our own explicit policy.

## Scope and exclusions

This central issue governs dependency direction, common development guidance,
observation and eventual retirement criteria. Viewer loader code and tests
remain local to `uibcdf/molsysviewer#109`; support wording remains local to
`uibcdf/molsysviewer#97`. No repositories, releases or Conda files are deleted
by opening or working this issue.

## Acceptance criteria

- Central development instructions no longer require local UIBCDF Qt paths.
- A platform/capability matrix clearly separates runtime-tested, solver-only,
  untested and explicitly unsupported cases.
- Native Windows/macOS ARM evidence is linked; macOS Intel has a tested wheel
  path or an approved retirement decision.
- At least one subsequent release candidate passes without the fork as a
  required dependency, and every remaining fork consumer or exception is
  inventoried.
- Maintainers explicitly decide whether the fork repositories remain as
  rollback assets, are archived, or require further maintenance. Any actual
  deletion is a separate authorized operation.

The future durable guard is the central environment/consumer inventory and
the local Viewer tests; an eventual normative support policy must be named
before this issue closes.

## Local implementation issues

- `uibcdf/molsysviewer#109` — canonical-first Qt host and test/CI migration.
- `uibcdf/molsysviewer#97` — user-facing standalone support boundary.
- `uibcdf/molsyssuite#52` — central Linux Python 3.14 environment.

## Dependencies and risks

No formal blocking issue is known yet. Native GUI access and WebEngine
platform availability may limit certification; keep those outcomes explicit.
