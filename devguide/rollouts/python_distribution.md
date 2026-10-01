# Python distribution adoption baseline

Coordination: uibcdf/molsyssuite#45. Normative contract:
[Python distribution member policy](../python_distribution_policy.md).
Active analysis: [member adoption report](../pending_proposals/complete_python_distribution_adoption.md).

## 2026-10-01 immutable source inspection

This is an initial source audit of all 14 registered Python members, not a
completed member review or a current public installation certification.
The original baseline recorded pending/pending/unknown. The four delivered
noarch migrations below now have member-owned partial reviews; their access
remains unknown. The ten other reviews still await their own recorded adoption.
Existing recipes, published packages and scientific test results are not erased
by those administrative states.

The central checker at `bf3f06165f34ae542f830db57bf35519831224a0` returned no
repository findings for all 14 inspected checkouts. Its distribution coverage
does **not** include the whole early dependency/artifact/publication contract.
The independently invoked existing `conda_release_contract.workflow_findings`
returned 26 source findings in nine publisher repositories. Three publisher
repositories passed this bounded check; two repositories have no Conda publisher.
Those two empty finding lists are non-applicability, not adoption proof.
Local tested equivalents and historical public receipts must be reviewed before
treating any common-profile finding as an independently reproduced release defect.

| Member source | Full inspected SHA | Shared publisher source profile | Distribution review evidence and remaining scope |
| --- | --- | --- | --- |
| [smonitor](https://github.com/uibcdf/smonitor/tree/9e24c4860611b0d44fad6c4161892ed8c76ead6b) | `9e24c4860611b0d44fad6c4161892ed8c76ead6b` | 2 findings | Conda claimed. No required project dependencies; recipe Python bounds match. Local exact-tag/version guards exist. Promotion still lacks the pinned independent verifier and retained promotion receipt expected by the shared profile. |
| [argdigest](https://github.com/uibcdf/argdigest/tree/e939714525d86c504c52801e8a89eee6b3a48bc4) | `e939714525d86c504c52801e8a89eee6b3a48bc4` | 2 findings | Conda claimed; README explicitly excludes PyPI. Recipe preserves required sibling floors. Several runtime-bearing environments list unbounded smonitor/depdigest; test_env_core.yaml preserves the floors. Promotion has two shared-profile findings. |
| [depdigest](https://github.com/uibcdf/depdigest/tree/a58448663c83e4a3042eceaa09c87dda4bea4b06) | `a58448663c83e4a3042eceaa09c87dda4bea4b06` | Pass (source conformance) | Conda claimed. Recipe and runtime environments retain the smonitor floor. Shared publisher profile passes; immutable direct/staged/public evidence is already recorded in the Conda rollout. Whole distribution adoption still needs its member-owned review. |
| [pyunitwizard](https://github.com/uibcdf/pyunitwizard/tree/4e38a8249d54ae0c897d3f354df8a314c1bd1e9f) | `4e38a8249d54ae0c897d3f354df8a314c1bd1e9f` | 2 findings | Conda claimed. Recipe preserves required dependencies and sibling floors. Runtime-bearing environments omit or weaken direct requirements: production_env.yaml has unbounded smonitor/depdigest, and test_env.yaml has no explicit numpy requirement. Promotion has two shared-profile findings. |
| [pytest-receptor](https://github.com/uibcdf/pytest-receptor/tree/b08bb9e6ced2f57a04b3a1952945c018ba0c5725) | `b08bb9e6ced2f57a04b3a1952945c018ba0c5725` | 2 findings | Conda and PyPI claimed. Recipe matches pytest and Python bounds; native pip routes install declared extras. Promotion has two shared-profile findings. Both public routes and packaged payloads need distinct review evidence. |
| [gh-run-receptor](https://github.com/uibcdf/gh-run-receptor/tree/febdbbd499743919589f61886c9cf1de4f503521) | `febdbbd499743919589f61886c9cf1de4f503521` | Not applicable (no publisher) | Pinned GitHub CLI extension, Action/workflow and GitHub Release wheel/sdist are documented; package-index publication is explicitly excluded. There is no Conda publisher or recipe. Python runtime dependencies are empty. Embedded JSON schemas need artifact-specific evidence. Absence of a Conda publisher is non-applicability, not a passing publisher audit. |
| [molsysmt](https://github.com/uibcdf/molsysmt/tree/59360a54c2ff8011c22daea5ba941cc6fa0f5c7d) | `59360a54c2ff8011c22daea5ba941cc6fa0f5c7d` | Pass (source conformance) | Conda claimed. Native and ABI3/rattler routes, py-mmcif name translation, runtime environments and exact sibling sources have a dedicated dependency inventory/auditor under MolSysMT#245. Shared publisher profile passes. Native extension/data/form resources and each claimed artifact route still require their member-owned distribution review. |
| [molsysviewer](https://github.com/uibcdf/molsysviewer/tree/9ef746243c03c9ab7ea5c92d6f69d1abd312a68c) | `9ef746243c03c9ab7ea5c92d6f69d1abd312a68c` | Pass (source conformance) | Conda and an unqualified pip installation command are documented, plus a separate npm publisher. Required recipe names/floors agree with project metadata; the inspected development environment lacks several direct requirements. Shared publisher profile passes. Embedded viewer.js/version and remote schemas have local guards. Historical Windows launcher failure remains Viewer#101 / MolSysSuite#47. |
| [topomt](https://github.com/uibcdf/topomt/tree/c0229057111d459c28d79c946d7cf21d9e44e91c) | `c0229057111d459c28d79c946d7cf21d9e44e91c` | 4 findings | Conda installation is documented. Required recipe names are present, but Python is unbounded and recipe/runtime extras need classification. Publisher has four shared-profile findings, uses @main, and fans out across interpreter/platform entries. Manual recipe instructions still request Python 3.7. Named CI source routes remain separate test evidence. |
| [pharmacophoremt](https://github.com/uibcdf/pharmacophoremt/tree/175b2d503ffd69cf9ebc52adb27a1930984834c9) | `175b2d503ffd69cf9ebc52adb27a1930984834c9` | 4 findings | Installation documentation still names pocketmt. Recipe omits argdigest, rdkit and networkx required by pyproject.toml, and leaves Python unbounded. Publisher has four shared-profile findings and uses @main. Manual recipe instructions still request Python 3.7. |
| [elastnetmt](https://github.com/uibcdf/elastnetmt/tree/d7ed87e0215e96888fc35a2238ac32ccc019e0fa) | `d7ed87e0215e96888fc35a2238ac32ccc019e0fa` | 4 findings | Conda installation is documented. Recipe omits required numpy, smonitor, argdigest and depdigest and leaves Python unbounded; runtime environments also need dependency review. Publisher has four shared-profile findings and uses @main. Manual recipe instructions still request Python 3.7. |
| [dockingmt](https://github.com/uibcdf/dockingmt/tree/35e834be83aa30fc9e0b03a74aa84aa3991abc24) | `35e834be83aa30fc9e0b03a74aa84aa3991abc24` | Not applicable (no publisher) | Development from source is documented; no Conda recipe or publisher is present. The CI Conda environment and separate exact sibling-source installation are an existing development route. A first public release remains prospective. Absence of a publisher is non-applicability, not a passing publisher audit. |
| [ackredit](https://github.com/uibcdf/ackredit/tree/7277bd5241a18c15c0fa9eb8e7acc98ce1332c90) | `7277bd5241a18c15c0fa9eb8e7acc98ce1332c90` | 2 findings | Source installation is documented; the Conda command is expressly conditional on Ackredit#22. Recipe names and floors match metadata; development/test/docs environments weaken the required floors. Publisher has two shared-profile findings. Its optional promote input performs a second build/upload to main rather than an exact-file label promotion. |
| [lindelint](https://github.com/uibcdf/lindelint/tree/9a3bc717c03d6e699df8fe3df813b9f1a10a7908) | `9a3bc717c03d6e699df8fe3df813b9f1a10a7908` | 4 findings | Conda is claimed. Required recipe names are present but Python is unbounded; scikit-learn is an extra runtime recipe requirement needing component classification. Runtime environments omit the official uibcdf channel in their committed channel list. Publisher has four shared-profile findings and uses @main. Manual recipe instructions still request Python 3.7. Scientific defects remain component-owned. |

## Provenance and repeatable administrative checks

Host: Linux development workspace. Measured interpreter: `Python 3.13.15`.
Inspection date: 2026-10-01.
Only tracked source/configuration and GitHub issue metadata were inspected.
No scientific suite, package build, workflow dispatch, upload, promotion,
credential verification or new public-channel solve was performed.

Before inspecting members, `python devtools/scripts/suite_status.py` fetched
registered remotes. Original ArgDigest and TopoMT local files were preserved;
inspection used clean isolated clones checked against remote-main at the full
SHAs above. GitHub issue closure or an unpublished working-tree report does not
certify a different remote-main tree. In particular, Viewer#106 was closed with
reported working-tree evidence; its named new auditor is absent from the Viewer
SHA inspected above, so this baseline does not infer hosted or delivered adoption.

Reproduce the bounded checks on a workspace whose child directory names match
the registered repositories:

```bash
python devtools/scripts/python_distribution_status.py
python devtools/scripts/check_repository.py WORKSPACE/MEMBER --repository uibcdf/MEMBER --json
python devtools/scripts/conda_release_contract.py WORKSPACE/MEMBER
```

Inspect the recipe, runtime environment/source route and artifact-resource
guards separately; these three commands cannot certify the complete distribution
policy. A read-only publisher audit may fail while the general repository checker
passes; preserve both results and their different scopes.

## Accepted decisions, 2026-10-01

The maintainer authorized adapting the four legacy publishers now and migrating
TopoMT, PharmacophoreMT, ElastNetMT and LinDelINT to `noarch: python`.
Their inspected recipes did not already declare noarch; no bundled native
extensions/executables were found in these tracked trees. The first affected
candidate needs staged installed qualification. No version, tag or publication
has been authorized here.

Issues opened before member implementation: uibcdf/topomt#78,
uibcdf/pharmacophoremt#10, uibcdf/elastnetmt#18 and uibcdf/lindelint#13.
The [noarch workflow guide](../noarch_conda_workflow.md) defines the common route.
Provider-owned exact-file upload, needed to inspect bytes before publication,
is uibcdf/action-build-and-upload-conda-packages#45, delivered at
`932fbef84440efbc97eb2275360fd3a767fdb47c`. Native administrative run 36894554807
and existing multi-variant run 36894554760 passed at that SHA; no actual upload
or Marketplace release occurred.

Ordinary scientific CI selections and internal direct/skip push permissions
remain intact. Candidate failures stay component-owned; a skipped-jobs probe
cannot replace their evidence. Offline guards establish administrative readiness,
not installed/public qualification.

The remaining publication credential model is owned by uibcdf/moli#8.
Access remains explicitly unknown; referencing ANACONDA_UIBCDF_TOKEN in a workflow
does not confirm its availability, scope or validity. This does not block recording
source adoption or a truthful pre-publication member review.

## Remaining handoff

Continue member-owned distribution adoption
issues and register partial/adopted states only with the corresponding member
evidence. Existing local work includes MolSysMT#245, Viewer#101/#106 and Ackredit#22;
those narrow themes are not automatically whole-policy adoption.

Preserve the separately tracked scientific execution reviews of MolSysMT and
MolSysViewer. Do not convert configured jobs, a passing publisher checker, historical
package receipts or another route's artifact into fresh scientific/installed-route
evidence. The other authorized blocks remain #68, #59, #46/#18 and #52 in that order.

## Delivered noarch migrations, 2026-10-01

Common source: `a44e86a4f6a01dcbfe28fde46d886bc5cd4254c2`. Central native
governance run 36898671705 passed all 249 administrative tests and the source
publication audit. Fifteen canonical guide copies were synchronized and pushed
through `sync_vendored_guides.py`; original sibling worktrees were preserved.

| Member review | Delivered full SHA | Exact-source administrative run | Illustrative wheel resources |
| --- | --- | --- | --- |
| uibcdf/topomt#78 | `e113a69a24ce18a23a7a0ed768ad8dec8eea8ae8` | [36902529148](https://github.com/uibcdf/topomt/actions/runs/36902529148) — passed | 297 paths, matching 0.0.0 embedded version |
| uibcdf/pharmacophoremt#10 | `c60880da4b5c7b0bff3fccc87936fed73ba69fad` | [36902560277](https://github.com/uibcdf/pharmacophoremt/actions/runs/36902560277) — passed | 47 paths, matching 0.0.0 embedded version |
| uibcdf/elastnetmt#18 | `af919eac0c7c5b522810eed565b0ff86a409cfe4` | [36902560182](https://github.com/uibcdf/elastnetmt/actions/runs/36902560182) — passed | 4 paths, matching 0.0.0 embedded version |
| uibcdf/lindelint#13 | `bde35d5762aff98cb6c80c78e042488a8a33190b` | [36902560332](https://github.com/uibcdf/lindelint/actions/runs/36902560332) — passed | 3 paths, matching 0.0.0 embedded version |

All four now produce a single noarch coordinate, preserve metadata Python bounds
and required recipe dependencies, use pinned thin wrappers and retain common
pre-upload/resource/source/producer/public controls. TopoMT's three concurrent
upstream commits were preserved by rebasing before pushing. PharmacophoreMT's
obsolete opocket package-data declaration and ElastNetMT's missing py.typed
packaging were corrected; all inventoried paths were present in isolated wheels.

The illustrative local wheels test setuptools packaging only: no Conda artifact
was built/uploaded, no public PyPI claim is made, and no installed scientific gate
was executed. Whole-policy adoption remains partial. Member issues record the
remaining runtime-environment/source-route/public-claim review, retained recipe
extras, component-owned installed scientific gate/descriptor and actual candidate
plan. Missing gates fail closed; no release plan or access confirmation is invented.

No ordinary source scientific CI selection or internal push permission was
changed. Guide/implementation pushes used the existing skip-CI development route;
its accepted recovery policy retains that debt. Only administrative workflows
were dispatched. MolSys-AI's pre-existing three README badge findings remain
outside this Python publisher migration; its local report index passed and its
canonical guide copy was synchronized.
