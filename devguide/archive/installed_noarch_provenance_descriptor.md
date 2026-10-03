---
summary: Accept the published installed workflow's post-scientific provenance descriptor.
issue: uibcdf/molsyssuite#89
status: resolved
opened: 2026-10-03
closed: 2026-10-03
severity: high
verification: reproduced
area: [distribution, tooling, ci]
guard: tests/test_installed_noarch.py::InstalledNoarchTests::test_prepare_accepts_provenance_recheck_from_published_workflow
normative:
blocked_by: []
supersedes: []
---

# Installed noarch preparation rejects its executed provenance check

**Reported:** 2026-10-03, actual Ackredit staged-file qualification.
**Status:** Resolved; accepted helper and eight-cell hosted qualification pass.

## What

Ackredit run `37136817748` selects the exact staged producer source
`598abf993a2409c025de5e912acd7eb45a257ebd` and fails in `installed / prepare`:
`installed descriptor differs from this reusable workflow's executed jobs/steps`.
The eight required runtime cells do not execute. Its retained descriptor is
`installed-noarch-descriptor-37136817748-1`.

## How

The shared workflow at `2a2a459cc3795bb92766fffa0fe28f4d80f01ad4` actually
executes four scientific/provenance steps. Ackredit declares all four, including
`Recheck installed provenance after scientific tests`. The helper compares its
required list against only the first three; inspected central source `61868db`
retains that mismatch. The regression reads the published workflow's actual
step declaration and passes it through the real preparation function. It fails
before this correction with the same ContractError.

The correction accepts the exact existing three-step legacy profile and the
published four-step profile, preserving the requested fourth step in the
promotion descriptor. It still rejects unknown, incomplete or reordered steps.
Existing tests preserve matrix, source, filename and legacy-profile checks.

## Why

The helper blocks safe promotion despite an intact digest-bound file. The
successful producer is `37136075066`; `ackredit-0.9.0-py_0.tar.bz2` has SHA-256
`37661090f6ad19a74b8155d8a4d4b4a068c9099f4ceba0743b3abfe887e97fe1` and
a verified `uibcdf.conda-upload@1` staging receipt. Independent download matches
the hash. Ordinary fresh Python 3.11–3.14 installations pass all 36 unchanged
Sabueso integration tests and its public workflow, but cannot replace the
required hosted Linux/macOS-arm64 matrix.

## What is measured and what is assumed

GH Run Receptor identifies the failed step; a bounded native excerpt provides
the exact error. The head SHA matches the staged candidate, independently of
the first dispatch `37136473226`, which correctly rejected a concurrent main
advance. The local reproducer runs on Python 3.14.7 in
`molsyssuite@uibcdf_3.14`. No public promotion or new registry mutation occurs.

## Alternatives and refuted paths

Removing the explicit post-scientific check from Ackredit would weaken its
qualification. Rebuilding or replacing the registered build-0 file would break
immutable identity. General action v2.3.0 adoption does not correct this helper.

## Scope and exclusions

This repair aligns accepted descriptors with the already executed workflow.
It changes no source/artifact identity binding, solver priority, mutation,
publication authority or scientific selection. The corrected qualification
caller versus existing producer-source boundary and strict staging solver
failure remain owned by uibcdf/molsyssuite#88.

## Acceptance criteria

- Fail before the correction using the real workflow's fourth-step declaration.
- Preserve all four required steps in the generated promotion descriptor.
- Keep legacy profile compatibility and reject unknown/incomplete/reordered lists.
- Pass existing preparation tests, full central tests and offline governance.
- Publish the accepted immutable helper for the owning qualification route.

## Local implementation issues

Ackredit delivery is uibcdf/ackredit#22 and uibcdf/ackredit#75; receiving evidence
is uibcdf/sabueso#108. Shared delivery coordination is uibcdf/molsyssuite#78.

## Dependencies and risks

Actual installed qualification of the existing file still requires the owning
route correction in #88 and reviewed consumer adoption. This source fix does
not qualify or authorize a public artifact.

## Provenance

2026-10-03, Linux, Python 3.14.7. Prepared in an isolated central clone from
`61868db`; primary component and central worktrees remain untouched.


## Resolution — 2026-10-03

PR #90 is integrated with PR #91 preserving both histories. Accepted immutable
workflow source is `c3e2b9b3dabf3d1c65349c389a23048957bea21a`; all 286 central
tests and exact-source hosted governance `37151428556` pass on Python 3.14.
The registered guard reads the actual published workflow and rejects the old
three-only preparation implementation, unknown, incomplete and reordered lists.

Ackredit adopts both corrected callers at
`92871148a762ea4b4786a64d13afd66a5b0bf8e7`, with 1,545 local tests passing
without skips. Native installed run `37152044426` passes preparation and all
eight Linux/macOS-arm64 Python 3.11–3.14 cells, retaining all four required
steps. Original producer `598abf993a2409c025de5e912acd7eb45a257ebd`, filename
and digest remain unchanged. Authorized promotion `37152421084` independently
verifies that native matrix/source binding and the public label/index of those
same bytes. The source-bound correction is resolved; remaining component
public-installation/receiver work belongs to uibcdf/ackredit#22 and
uibcdf/sabueso#108. No Windows qualification or action v2.3.0 adoption is claimed.

Detailed caller/receipt handoff and primary observations are maintained in
`devguide/rollouts/installed_noarch_88_89.md` and
`devguide/rollouts/installed_noarch_88_89.json`.
