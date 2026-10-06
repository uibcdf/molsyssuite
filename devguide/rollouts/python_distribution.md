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

### Installed workflow delivery

The common installed qualification module/workflow and controls are now delivered
at `42e4de425871c125ef058842075c39e50fc6ac64`; exact-source central native
governance 36908141209 passed 256 administrative tests. The four members have
a manual installed caller and committed six-cell Linux/macOS arm64 Python
3.11-3.13 descriptor, with the complete local tests selection. This workflow
checks native run head as well as checkout, exact downloaded/installed Conda
coordinate/digest, ordinary public dependency provenance, imported/installed
resources and imports within pytest. It rejects an empty test execution.
No scientific installed workflow was dispatched and no candidate was selected.

| Member | Full installed-wrapper source | Native administrative check |
| --- | --- | --- |
| uibcdf/topomt#78 | `16700eb57507eaa33743b1ec73587f48dd085338` | [36908419786](https://github.com/uibcdf/topomt/actions/runs/36908419786) — passed |
| uibcdf/pharmacophoremt#10 | `3a43752e7cb1f587127f4c8c8bf45a9575e56a0f` | [36908419176](https://github.com/uibcdf/pharmacophoremt/actions/runs/36908419176) — passed |
| uibcdf/elastnetmt#18 | `7c3466a638167e5a5f46cc48a7aa95af66b77bc9` | [36908419767](https://github.com/uibcdf/elastnetmt/actions/runs/36908419767) — passed |
| uibcdf/lindelint#13 | `73a90d98a9b69553dab039a3ce3b2f5f05d8aef8` | [36908448644](https://github.com/uibcdf/lindelint/actions/runs/36908448644) — passed |

The earlier remaining task to implement the installed gate/descriptor is
therefore replaced by executing and reviewing it for an actual candidate. Other
whole-policy adoption gaps remain partial; configured scientific gates do not
prove scientific or installed compatibility. Provider upload issue #45 was
resolved with its owning README/negative guards and native evidence.


## Current inventory and PyUnitWizard delivery — 2026-10-06

The historical 14-source audit above is preserved. The current registry has
**15 Python package members** after OpenCASTp admission: **five partial, ten
pending**, zero adopted/excepted. Access is confirmed for one observed release
and remains unknown in fourteen other reviews. These are adoption-record
states, not a count of working libraries or published packages. OpenCASTp's
member review remains uibcdf/opencastp#2; its temporary private visibility and
uibcdf/molsyssuite#102 audit limitation are unchanged.

| Reviewed route | Exact evidence | Current disposition |
| --- | --- | --- |
| PyUnitWizard 0.28.1 / public noarch Conda | Original `25a4bc2468da4ef3af2a638c0bf068becf2acfb4`; owner closure `900f62a4cdc61bdaedfa50e1407a7c651a0cc26d`; uibcdf/pyunitwizard#112 | partial adoption / partial CI-recipe / access confirmed for this authorized observed release |
| Source gates | Five original-source workflows, 29 required jobs independently verified through the shared native gate verifier | executed evidence; not configured jobs alone |
| Producer / installed / promotion | [37307676226](https://github.com/uibcdf/pyunitwizard/actions/runs/37307676226), [37308199459](https://github.com/uibcdf/pyunitwizard/actions/runs/37308199459), [37309227696](https://github.com/uibcdf/pyunitwizard/actions/runs/37309227696) | all success; 30 installed cells plus original-source binding |
| Public exact file | `noarch/pyunitwizard-0.28.1-py_0.tar.bz2`; SHA-256 `d4654faf93ed4181bf331f7d382379e78f02784f71f678ad19d0ac43d8062cc6` | independent main-label/index verifier and downloaded bytes match |
| Runtime payload / metadata | 84 runtime files (83 Python modules plus `py.typed`) equal original source; generated/metadata version and required dependencies match | no rebuild or replacement |
| Dependency routes | All eight recorded route hashes match the original candidate; production SMonitor/DepDigest floors and test NumPy are corrected | maintained preflight/negative guards and whole-policy review remain uibcdf/pyunitwizard#114 |

Primary central receipt: [pyunitwizard_distribution_45_20261006.json](pyunitwizard_distribution_45_20261006.json).
The owner retains 30 Conda/pip/JUnit closures: baseline/storage/prepared eight
each, optional OpenFF six (Python 3.12–3.14). Baseline public Ackredit 0.9.0 and
prepared public 0.10.1 have separate bounded evidence; no dependency floor changes.
A fresh public install and 43 attribution guards are owner-reported in the
immutable closure receipt, not rerun centrally.

PyUnitWizard uses a documented local publisher/installed/promoter route with
the reviewed UIBCDF provider and fixed shared public verifier. This review does
not replace that orchestration or force an inapplicable generic operator adapter.
Whole-policy status is partial because archived one-time preflight results do
not identify a maintained runtime-route checker and negative regression guards.
The provider team owns that delivery/identification in #114. No new scientific
execution, OpenFF integration review, public mutation, PyPI/Windows claim,
version-1.0 admission, MolSysMT adoption or stable provisional API follows.

Reproduce central inventory and bounded source checks with the qualified 3.14
environment; module invocation retains this repository's tool import origin:

```bash
python -m devtools.scripts.python_distribution_status
python -m devtools.scripts.check_repository ORIGINAL_CANDIDATE_CLONE --repository uibcdf/pyunitwizard --json
python -m devtools.scripts.conda_release_contract ORIGINAL_CANDIDATE_CLONE
```

The first full-matrix job selection excludes its unrelated decision job;
every one of its eight scientific jobs must execute successfully. The other
four source profiles and the 31-job installed workflow require their exact
job sets. Administrative native evidence, archive bytes, installed/runtime
results and public availability remain separately identified in the receipt.
