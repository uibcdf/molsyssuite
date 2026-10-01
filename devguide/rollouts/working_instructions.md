# Durable working-instruction adoption

Coordination: uibcdf/molsyssuite#66. Normative rules:
[working_instructions_policy.md](../working_instructions_policy.md).

## Initial inventory, 2026-10-01

Fetched isolated main checkouts were clean. Every member had root instructions;
only GH Run Receptor, MolSysMT and MolSysViewer had developer-guide instructions.
Existing local layouts, instruction content and unrelated working checkouts are
preserved. The common route additions are owned by this central rollout; distinct
local implementation or exceptions require their own owning issue.

| Member | Inspected source | Existing devguide instructions |
| --- | --- | --- |
| uibcdf/smonitor | `91a80981405b83f5fc9c4b9b11640db153a5b4e5` | missing; add |
| uibcdf/argdigest | `9ee927c9256c34aeff7cc929fc0e4c1f269b5723` | missing; add |
| uibcdf/depdigest | `86fe1087f540d33a86a277936f4e46acfa27a886` | missing; add |
| uibcdf/pyunitwizard | `66e35d3ca896bf3ed7e76ff9e53dd5c49bf447e3` | missing; add |
| uibcdf/pytest-receptor | `5448ca31a1df03130d8a0a9eb7a367bed798f81b` | missing; add |
| uibcdf/gh-run-receptor | `293e2ca0746322ae9c76d854f805c55f77f1935f` | present; preserve |
| uibcdf/molsysmt | `8195ef2e0d59cfb2f8e73843b4400e7323ece787` | present; preserve |
| uibcdf/molsysviewer | `3db82d02b71d773cb3263b00a1bc37e4235ade79` | present; preserve |
| uibcdf/topomt | `ad388afe169dbcda982d582675eea01f4bf3c5b4` | missing; add |
| uibcdf/pharmacophoremt | `54d0029c3e4e1f9729c81b9c1c3af925d5f6e9ac` | missing; add |
| uibcdf/elastnetmt | `b9e3ab29a34ab69006d68df8dff62f31792c93a3` | missing; add |
| uibcdf/dockingmt | `d0cc7d254a40d515375112fc751b5f77ee03bb86` | missing; add |
| uibcdf/ackredit | `10f1a30bf423aa680d8f49726172e0cec3517ce5` | missing; add |
| uibcdf/lindelint | `fa1f37a241e1daf30e7596cc4e97a903fd98aa57` | missing; add |
| uibcdf/molsys-ai | `95bc2805e590cb68212b21189a6352451ad4b590` | missing; add |

## Verification boundaries

The same mechanical provider checks root/nested files, active canonical routes
and real local targets. It rejects hidden examples and incomplete/expired
exceptions; it does not establish prose quality or scientific correctness. Ten
regression tests and the starter tests exercise these mechanisms. The existing
component-guide workflow gains the check; Python policy caller versions, native
scientific CI, platform claims and release permissions are unaffected. No package
or policy release is needed for this guide/route audit adoption.

Existing specialized instructions remain authoritative for local scope. Review
confirmed that new actions concern accepted contributor behavior and reference
current canonical guidance rather than incident details. Technical findings do
not acquire AGENTS rules automatically. No exception is currently requested.

Delivery and hosted results are recorded after committed-source guide sync.
