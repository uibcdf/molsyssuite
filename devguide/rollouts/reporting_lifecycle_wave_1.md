# Reporting lifecycle rollout: stabilization wave 1

**Issue:** `uibcdf/molsyssuite#13`  
**Policy:** `uibcdf/molsyssuite#11`  
**Started:** 2026-09-07  
**Status:** Active.

## Scope

The first stabilization wave is:

- SMonitor;
- ArgDigest;
- DepDigest;
- PyUnitWizard;
- MolSysMT;
- MolSysViewer.

Pytest Receptor and GH Run Receptor are supporting infrastructure. Their existing policy
adoption remains useful, but they do not define completion of this stabilization wave.

TopoMT, PharmacophoreMT, and ElastNetMT are incubating. The common semantic contract
applies to them, but missing local reporting machinery does not block wave 1 and will be
scheduled when each repository enters stabilization.

## Per-repository acceptance

- Contributor guidance routes suite-wide work centrally and local work locally.
- Pending bug and proposal queues have documented local paths.
- Queued and archived reports use stable owning-issue identity and common statuses.
- Resolved reports are archived rather than deleted and cite a guard or normative record.
- A generated index and offline validator detect metadata and lifecycle drift.
- Filing and closing instructions include GitHub issue synchronization.
- Existing stricter tools and compatible archive layouts are preserved.

## Adoption matrix

| Member | State | Local issue | Notes |
| --- | --- | --- | --- |
| smonitor | pending audit | — | wave 1 |
| argdigest | partial | `uibcdf/argdigest#4` | governance pointer exists; lifecycle surface still requires audit |
| depdigest | partial | `uibcdf/depdigest#3` | governance pointer exists; lifecycle surface still requires audit |
| pyunitwizard | pending audit | — | wave 1 |
| molsysmt | reference implementation | — | verify against the common contract without flattening local policy |
| molsysviewer | reference implementation | — | verify against the common contract without flattening local policy |

## Rollout discipline

- Audit before editing and open a local issue only when a concrete gap exists.
- Reuse MolSysMT and MolSysViewer semantics; do not copy repository-specific machinery
  blindly.
- Keep semantic adoption separate from enforcement in the shared conformance workflow.
- Do not let incubating repositories determine or delay wave-1 completion.
