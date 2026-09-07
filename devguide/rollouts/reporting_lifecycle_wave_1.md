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
| smonitor | adopted | `uibcdf/smonitor#7` | existing adoption at `85c2896`; 15 offline report tests pass with 2 network skips |
| argdigest | adopted | `uibcdf/argdigest#6` | pass at `e18aa19`; 225 local tests; three legacy archive exemptions documented |
| depdigest | adopted | `uibcdf/depdigest#5` | pass at `0ebce25`; 52 local tests; one legacy archive exemption documented |
| pyunitwizard | active | `uibcdf/pyunitwizard#72` | audit complete; migration deferred to preserve active local product and CI work |
| molsysmt | verified reference | — | offline validator and generated-index check pass on 2026-09-07 |
| molsysviewer | verified reference | — | 86 reporting-protocol tests and generated-index check pass on 2026-09-07 |

## Verification log

On 2026-09-07 the existing reference implementations were checked without changing
their layouts:

```bash
# MolSysMT
python devtools/scripts/validate_devguide.py
python devtools/scripts/devguide_index.py --check

# MolSysViewer
python -m pytest -q -p no:cacheprovider tests/test_reporting_protocol.py
python devtools/devguide_index.py --check
```

Both pass. MolSysMT's typed archive and MolSysViewer's flat archive therefore remain
valid examples of the same lifecycle.

## Rollout discipline

- Audit before editing and open a local issue only when a concrete gap exists.
- Reuse MolSysMT and MolSysViewer semantics; do not copy repository-specific machinery
  blindly.
- Keep semantic adoption separate from enforcement in the shared conformance workflow.
- Do not let incubating repositories determine or delay wave-1 completion.
