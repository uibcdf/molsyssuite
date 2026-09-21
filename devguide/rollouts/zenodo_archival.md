# Zenodo archival rollout

**Policy:** `devguide/zenodo_policy.md`  
**Issue:** `uibcdf/molsyssuite#24`  
**Inventory:** `devguide/rollouts/zenodo_inventory.toml`  
**Started:** 2026-09-19  
**Status:** Active.

This rollout separates policy adoption from external archival evidence. `required` means
the component must satisfy the policy before its next public release after adoption;
`optional` means incubation or auxiliary status does not yet create a release gate.
Neither mode is evidence that a Zenodo connection or record exists.

| Component | Mode | Evidence state | Evidence |
| --- | --- | --- | --- |
| SMonitor | required | absent | no public record found; remediation `uibcdf/smonitor#14` |
| ArgDigest | required | absent | no public record found; remediation `uibcdf/argdigest#11` |
| DepDigest | required | absent | no public record found; remediation `uibcdf/depdigest#11` |
| PyUnitWizard | required | verified | 0.25.0; concept DOI `10.5281/zenodo.8088374`; version DOI `10.5281/zenodo.21993780`; one source snapshot independently matched |
| pytest-receptor | required | unknown | audit not yet performed |
| gh-run-receptor | required | verified | 1.1.1; concept DOI `10.5281/zenodo.22843377`; version DOI `10.5281/zenodo.22871415`; one source snapshot independently matched |
| MolSysMT | required | unknown | repository claims need public-record verification |
| MolSysViewer | required | unknown | repository claims need public-record verification |
| TopoMT | optional | unknown | incubating |
| PharmacophoreMT | optional | unknown | incubating |
| ElastNetMT | optional | unknown | incubating |
| Lindelint | optional | unknown | auxiliary |

The machine-readable inventory is authoritative for the dated evidence above. Update it
only from a bounded public audit or an explicitly labeled maintainer observation. A
successful GitHub Release, repository badge, metadata file, webhook observation or
reported account toggle never promotes a row to `verified` by itself.

## Next adoption work

1. Audit the remaining required components without publishing or changing external state.
2. Open a component issue only where the audit identifies concrete metadata, workflow,
   badge or record remediation.
3. Require a verified public record for each component's next release; historical
   backfill is a separate decision.
4. Revisit optional components when they enter stabilization or prepare a public release.
