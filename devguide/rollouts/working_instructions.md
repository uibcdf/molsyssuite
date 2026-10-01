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

## Completed delivery, 2026-10-01

Provider: `406e45e76b57e857372d6712a44ca2d40f413152`; central governance
36873854500 passed (224 administrative tests). All 15 member routes passed
locally after canonical sync; all local report index checks passed, using
MolSys-AI's `scripts/devguide_index.py` equivalent. MolSysMT's complete offline
developer-guide validator and its local Ruff check also passed.

| Member | Published adoption commit |
| --- | --- |
| uibcdf/smonitor | `9e24c4860611b0d44fad6c4161892ed8c76ead6b` |
| uibcdf/argdigest | `e939714525d86c504c52801e8a89eee6b3a48bc4` |
| uibcdf/depdigest | `a58448663c83e4a3042eceaa09c87dda4bea4b06` |
| uibcdf/pyunitwizard | `4e38a8249d54ae0c897d3f354df8a314c1bd1e9f` |
| uibcdf/pytest-receptor | `b08bb9e6ced2f57a04b3a1952945c018ba0c5725` |
| uibcdf/gh-run-receptor | `febdbbd499743919589f61886c9cf1de4f503521` |
| uibcdf/molsysmt | `59360a54c2ff8011c22daea5ba941cc6fa0f5c7d` |
| uibcdf/molsysviewer | `9ef746243c03c9ab7ea5c92d6f69d1abd312a68c` |
| uibcdf/topomt | `c0229057111d459c28d79c946d7cf21d9e44e91c` |
| uibcdf/pharmacophoremt | `175b2d503ffd69cf9ebc52adb27a1930984834c9` |
| uibcdf/elastnetmt | `d7ed87e0215e96888fc35a2238ac32ccc019e0fa` |
| uibcdf/dockingmt | `35e834be83aa30fc9e0b03a74aa84aa3991abc24` |
| uibcdf/ackredit | `7277bd5241a18c15c0fa9eb8e7acc98ce1332c90` |
| uibcdf/lindelint | `9a3bc717c03d6e699df8fe3df813b9f1a10a7908` |
| uibcdf/molsys-ai | `1f7fd4ff9aa97b2ef0740684aaf27be21a59a78f` |

Original root instructions and the three existing nested files were preserved.
TopoMT remote advanced to `3da03db` during delivery; its adoption commit was
rebased without conflict and pushed, preserving concurrent component work.
No scientific suites or publications were initiated. Guide synchronization was
performed only by the canonical sync tool; direct internal commits used the
existing skipped-CI recovery contract.

Native member-guide run 36874496180 passed all 15 component checks; vendored-guide
run 36874500880 passed. Earlier runs 36873854606/36873854489 detected the
pre-delivery gap; no waiver was used. The published provider remains independently
guarded by ten instruction tests and three starter tests. This completes #66;
future human-facing reporting behavior remains #65.
