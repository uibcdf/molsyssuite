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
**15 Python package members** after OpenCASTp admission: **eleven partial, four
pending**, zero adopted/excepted. Access is confirmed for six observed Conda deliveries
and remains unknown in nine other reviews, including GH Run Receptor's
official Conda route. These are adoption-record
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


## Ackredit and Pytest Receptor delivery — 2026-10-06

| Member | Qualified original public file | Native evidence | Remaining owner review |
| --- | --- | --- | --- |
| Ackredit | `ackredit-0.10.1-py_0.tar.bz2`; SHA-256 `26e75a0780ad4e6abc2de55df90b29b4a2aa4e510d6b50fa54a5812ad929228e`; source `dd500842b6085111e01e62cfc243f68406eb8cc7` | producer [37268654191](https://github.com/uibcdf/ackredit/actions/runs/37268654191); installed [37268949725](https://github.com/uibcdf/ackredit/actions/runs/37268949725), all eight cells; four source gates / 17 required jobs | uibcdf/ackredit#108; current source `85deae594e65b2fd443d6ca9a7347eb2bda537e1` passes source conformance |
| Pytest Receptor | `pytest-receptor-1.2.1-py_0.tar.bz2`; SHA-256 `77bf3694bc903f606d4323b88e3bb3aea9628618036b53073f5a5dbd5dbc73cb`; source `6c4686c55ee5e004160ba4c36a499ff7e5c8a64b` | producer [37136074225](https://github.com/uibcdf/pytest-receptor/actions/runs/37136074225); installed [37148738757](https://github.com/uibcdf/pytest-receptor/actions/runs/37148738757), all eight cells; qualification `98e2cf35b24896891b3d95a684facb5c0212c48d`; two source gates / 18 required jobs | uibcdf/pytest-receptor#38; current source `ac0aa0379ab34370a8379431b0bacd1d537f2ed5` passes source conformance |

Primary receipts: [ackredit_distribution_45_20261006.json](ackredit_distribution_45_20261006.json)
and [pytest_receptor_distribution_45_20261006.json](pytest_receptor_distribution_45_20261006.json).
The shared operator independently verifies both producers' native receipt ZIPs,
original candidate identity, installed binding and executed steps, plus current
public label/index. It emits no dispatch: `state=public-verified`,
`mutation_performed=false`, `next_command=null`. Public downloaded bytes pass
`noarch_conda.inspect_recipe`/`inspect_artifact`. The original files are not
rebuilt, replaced or promoted again.

Pytest Receptor's distinct public PyPI files also pass its existing
`devtools/check_release.py` against original source: wheel SHA-256
`683200648785f3894357891b238cdc0780c1e874dcf067882dbba2aaa2c527c3`;
sdist `e0e1db8049d2ec85d7828ea3ead631a27d09ecf13f496fc75197c89a6a3a1a48`.
PyPI metadata and owner receipts match downloaded hashes. Existing clean
public pip/Conda installs remain owner-reported runtime evidence, not repeated
centrally. Ackredit claims public Conda, not an unresolved PyPI-only route.

Both states advance pending → partial, CI/recipe remains partial, and access
is confirmed only for the successful observed authorized releases. No member
is newly adopted. The formal reviews retain concrete work: classify all actual
runtime/build-only/CI/source routes and identify/deliver a maintained reusable
dependency preflight with meaningful negative guards. Ackredit's old weak
floors are corrected; name-only installation-page guards do not protect all
route constraints. Pytest Receptor's existing recipe/resources/PyPI guards
remain useful; its legacy named 3.13 environment needs explicit classification
alongside the common 3.14 development route. Required sibling-source installs
are inapplicable to its public runtime closure; the provider's self-test pin
exception remains intact.

The original 1.2.1 source compares unequal to today's later canonical guide,
while its reviewed current main is conformant. This dated source comparison is
retained in the receipt; it does not justify rewriting the immutable tag/file
or claiming a current guide defect. Ackredit's active 0.11.0 release #107 and
provider stability/receiving decisions are not certified by its old 0.10.1
archive. No Windows support, general Action-v2.3.0/withdrawal migration,
scientific execution, new public install or change to internal push lanes follows.


## Core providers and GH Run Receptor delivery — 2026-10-06

The current inventory is **eleven partial / four pending**, zero newly adopted
or excepted. Six reviews have confirmed access bounded to observed authorized
Conda delivery; nine remain unknown. Pending reviews are MolSysMT, MolSysViewer,
DockingMT and OpenCASTp. Their existing scientific deferrals, development and
private-access conditions are unchanged.

| Member / exact existing public route | Independently inspected evidence | Owner adoption work |
| --- | --- | --- |
| SMonitor 0.18.0 / Conda noarch | Original `b79cca8eb9bd878d0d3439876eca4ed26560e916`; producer [36271508179](https://github.com/uibcdf/smonitor/actions/runs/36271508179), promotion [36271902608](https://github.com/uibcdf/smonitor/actions/runs/36271902608); public label/index/bytes match `7fba29b56853771ceaf477de50aeed0cf9e93e2053e484de4e18c18ea1abe578`; version/runtime/resources pass; native Windows Python 3.13 command smoke | uibcdf/smonitor#35: formal routes, claimed installed-cell qualification and maintained early/resource negative guards; local publisher retained |
| ArgDigest 0.14.0 / Conda noarch | Original `0fa776af2d271065c60727c28480b20c3ce09aee`; producer [37210475369](https://github.com/uibcdf/argdigest/actions/runs/37210475369); qualification `be39e899f3b9fef2d4ce705799ae19770f41f769`; installed [37213239915](https://github.com/uibcdf/argdigest/actions/runs/37213239915) / twelve cells and opt-in core [37211211381](https://github.com/uibcdf/argdigest/actions/runs/37211211381) independently verified; public exact digest `983dca0f6bd0944d81fb1efc01e1dfa5c951e95abac6e7a0a08a13b7370d3b9e` | uibcdf/argdigest#28: six rejected unbounded SMonitor/DepDigest comparisons in development/docs/test environments; formal route review and maintained negative guards |
| DepDigest 0.13.0 / Conda noarch | Original `df771e00e886fd9b12915adf54c1bd75c4b5476c`; producer [37194076957](https://github.com/uibcdf/depdigest/actions/runs/37194076957), installed [37194436139](https://github.com/uibcdf/depdigest/actions/runs/37194436139) / twelve cells plus producer verification, promotion [37194867340](https://github.com/uibcdf/depdigest/actions/runs/37194867340); producer/public bytes digest `e011d725c8a831ae46cd6b8d114185d04248e32b4d6701c70f988d19cc69f67b`; all nine owner preflight input hashes match current source | uibcdf/depdigest#30: maintain whole-route dependency/resource guards; recorded one-time negatives and clean installs remain owner evidence; local publisher retained |
| GH Run Receptor 1.2.0 / GitHub wheel, sdist, extension | Original `c3df5ad87f7bab95c53be3f7b0b3007f59d7abf3`; [compatibility 37073452071](https://github.com/uibcdf/gh-run-receptor/actions/runs/37073452071) / twelve source-build/install/smoke cells, [publication 37073949431](https://github.com/uibcdf/gh-run-receptor/actions/runs/37073949431); downloaded wheel/sdist/checksum manifest pass owner verifier and live digests; both archives contain exact generated version, Python bounds and nine frozen schemas | uibcdf/gh-run-receptor#60: review official Conda applicability/prospective route or bounded exception and maintained archive-negative guards; Conda access remains unknown |

Receipts: [SMonitor](smonitor_distribution_45_20261006.json),
[ArgDigest](argdigest_distribution_45_20261006.json),
[DepDigest](depdigest_distribution_45_20261006.json),
[GH Run Receptor](gh_run_receptor_distribution_45_20261006.json).

These are positive administrative and existing native evidence observations, not
new scientific runs. General conformance and one passing public release do not
close the whole member distribution review. The archive inspection operation
accepts explicit read-only inputs for SMonitor/DepDigest; it does not rewrite
their local plans or certify shared-schema conformance. SMonitor's historical
Windows smoke is narrower than a twelve-cell exact-artifact matrix. GH Run
Receptor's matrix-built wheels differ from its single public wheel; the prior
central isolated public-wheel receipt remains uibcdf/molsyssuite#75. No public
Conda/PyPI claim or credential assurance is inferred from its GitHub release.

ArgDigest's six environment comparisons are a current constraint defect,
separate from its byte-preserving completed release. Its existing reusable
constraint/recipe operations and metadata guards should be extended or reused
before introducing a new implementation. DepDigest's owner preflight
classification and negative cases remain valuable dated evidence; maintaining
their operation for future inputs is the bounded remaining need. Empty required
Python dependencies in SMonitor/GH Run Receptor require applicability reasoning
rather than fabricated sibling source-floor tests. No component source, artifact,
scientific selection, visibility setting or internal-push lane changes here.

## ArgDigest required-provider floors corrected — 2026-10-06

The preceding six rejected environment comparisons are fixed at
`94cffa861146c6520585aefff02523f03e0a9704` under uibcdf/argdigest#28.
Only development/docs/routine-test entries acquire the minima already declared
by runtime metadata and the public 0.14.0 artifact. Core tests and build-only
tooling keep their reviewed roles. The compatibility guard now protects the
four runtime-bearing routes and meaningful provider mutations; stronger bounds
remain permitted. It does not claim complete constraint parsing or route solving.

Local regression evidence is three failed / nineteen passed before, then
twenty-two passed after. The six owner reporting checks and offline governance,
index, general conformance and Ruff checks also pass. The existing normal push
CI runs automatically; no manual full-matrix dispatch, rebuild or promotion is
part of this correction. Exact hosted results and updated environment hashes
are retained in the [new correction receipt](argdigest_environment_floors_45_20261006.json).

The [original review receipt](argdigest_distribution_45_20261006.json) preserves
its dated diagnosis and the independent public-file evidence. ArgDigest remains
partial pending the rest of its owner route/preflight review. Inventory totals
remain eleven partial / four pending, with six observed deliveries confirming
bounded access and nine unknown states.

## ArgDigest formal adoption — 2026-10-06

The later whole-route review completes uibcdf/argdigest#28. Source
`ad920c515f7c08b6a85492f6aa2094405683899d` inventories one recipe, five
environments and eleven workflows and invokes the accepted shared tool
`43b9f94bf5ab0ec3f54a4b2ca5b23b791d6af0bc` before ordinary tests and exact
candidate builds. The CI actually audits all 17 routes and passes 315 tests with
one unavailable sibling integration skipped; both hosted policies pass. The
closing record at `7f93b23cc8da64747d3e4608218d769f5e7cc21f` changes only
report/archive/index inputs and preserves the qualified implementation bytes.

ArgDigest now has adopted/ready/confirmed status, bounded to this reviewed source
contract and observed original public delivery. Inventory totals are **one
adopted / ten partial / four pending**, six bounded confirmed deliveries and nine
unknown access states. The [adoption receipt](argdigest_distribution_adoption_45_20261006.json)
keeps provider identity, all route hashes, administrative/native evidence and the
original 0.14.0 file qualification separate. No new package bytes, source tag,
scientific matrix dispatch or other component adoption is inferred.

## Ackredit formal adoption — 2026-10-06

The owner completed uibcdf/ackredit#108 and integrated its existing #110 at
`edd6df2ae3ebe9143ca87043c3ccb94207a4a545`. Central review of archived closeout
`61742c40793cb66136a77b2e19516579774c6a81` verifies all 16 inventoried routes
(one recipe, five environments, ten workflows) and general conformance. The
accepted shared preflight is pinned to `43b9f94bf5ab0ec3f54a4b2ca5b23b791d6af0bc`
and executes in CI; staging requires successful exact-candidate CI before build.

Final-head CI [37451553223](https://github.com/uibcdf/ackredit/actions/runs/37451553223)
executes all seven jobs, including the dependency audit, strict documentation,
Ruff and five installed source cells (2119 passed / eight skipped each). Both
hosted policies pass at that same source. These observed source cells do not
replace the public-file matrix. The original central 0.10.1 receipt remains
unchanged; the owner's immutable 0.11.0 receipt separately retains its original
source and digest, eight installed/receiving cells, same-byte promotion and clean
public Linux/Python 3.14 installation. No new central artifact qualification is
claimed from reading that later receipt.

Ackredit is **adopted / ready / confirmed**, bounded to current source adoption
and observed authorized deliveries. Totals are **two adopted / nine partial /
four pending**, six bounded confirmed deliveries and nine unknown access states.
The [adoption receipt](ackredit_distribution_adoption_45_20261006.json) records
the evidence boundaries. API/admission decisions, provisional evidence APIs,
future credentials, other consumers and shared-workspace qualification remain
separate. No archive is rebuilt, uploaded or promoted by this review.

## Pytest Receptor formal adoption — 2026-10-06

The owner review uibcdf/pytest-receptor#38 is complete at
`4065003d56d15735fb2bbc5e71ced50d5d988d4c`, archived at
`9220984a8402718b93518600ffe035e3f3ff5ec3`. All 13 maintained inputs are
classified and audited against shared tool `43b9f94bf5ab0ec3f54a4b2ca5b23b791d6af0bc`.
Legacy supported-minor compatibility, metadata/runtime bounds and the accepted
own-source self-test exception remain intact. The audit belongs to the existing
mandatory `lint` check; tests/benchmarks/builds wait for it. The original 11 strict
PR checks are unchanged. Conda and future PyPI source preparation require exact
executed native gates before building; PyPI retains its gate receipt separately
from distributions and does not require a Conda upload.

Implementation and closing source each pass all 12 ordinary CI jobs, including
220 serial and 220 xdist tests in every Linux Python 3.11–3.14 / pytest 8–9
cell without skips. Reporting, suite and publication policies also pass. The
[adoption receipt](pytest_receptor_distribution_adoption_45_20261006.json) separates
those source controls from the original independently verified public 1.2.1
Conda/PyPI files, eight exact-file installed cells and owner-measured clean
installation. Native CI's temporary candidate wheel is not a registered-file
replacement or a new public release.

Status is **adopted / ready / confirmed**, with access bounded to observed
authorized deliveries. Current totals: **three adopted / eight partial / four
pending**, six bounded confirmed deliveries and nine unknown access states.
No API/schema, client pin/guide adoption, registered-archive upload/promotion,
self-test exception or Windows-support change is inferred. Joint-workspace
qualification and future credentials retain separate evidence.


## PyUnitWizard general-contract adoption — 2026-10-06

uibcdf/pyunitwizard#114 is resolved at implementation
`d128b37b4339d3b8520678cc9d8924f902d14a7b` and archived closeout
`6cfc9ae5281532d46a09d5059902d49fa7c1d19a`. Accepted shared provider
`20628bd5dba6d759669b0d444fe657eb1edad33f` qualifies the general @2 route
contract with 364 hosted tests and 74 focused local controls. The original @1
contract/current client pins remain valid; existing owners received the delivery.

The owner maintains 22 route inputs (one recipe, nine environments, twelve
workflows), justified compatible purpose-specific narrowing and default actual
installed public bounds. Its local publisher retains version/resources/file/
installed/public controls. Future prebuild qualification requires the original
five exact-source workflows and 29 executed job/step profiles, including the
installed dependency checks; declaration-only bootstrap cannot qualify alone.

Ordinary CI 37497852682 executes the audit and passes **785 tests / 19 skips**;
implementation policy 37497853464 and closing policy 37499214277 also pass.
Forty focused owner checks and nine closing reporting checks pass locally.
No extra full/optional scientific workflow is dispatched for this source review.
The [adoption receipt](pyunitwizard_distribution_adoption_45_20261006.json)
retains exact identities/input hashes and the earlier independent original public
0.28.1 receipt unchanged. Source controls do not transfer old artifact gates to
a new candidate. No rebuild/upload/promotion or scientific/public API change.

Current totals: **four adopted / seven partial / four pending**, with six
bounded confirmed deliveries and nine unknown access states. PyUnitWizard is
**adopted / ready / confirmed** for its reviewed route; #45 remains partial.


## SMonitor adoption and refreshed public releases — 2026-10-06

Following the maintainer's pause for new provider releases, review resumes against
SMonitor **0.19.0 build 1** and ArgDigest **0.15.0 build 0**. Earlier public and
adoption receipts remain intact. Read-only central operations independently bind
original candidates, producer receipt ZIP digests, all required source jobs,
twelve exact-file installed cells, promotion receipts, public registry/index and
downloaded archive hashes/metadata/resources. ArgDigest's distinct twelve-cell
NumPy-free old-provider matrix also verifies; its full scoped-capture matrix
requires public SMonitor 0.19.0. No scientific tests or package/public operations
are dispatched by this review.

Separate immutable release reviews:
[smonitor_public_0_19_0_45_20261006.json](../rollouts/smonitor_public_0_19_0_45_20261006.json)
and [argdigest_public_0_15_0_45_20261006.json](../rollouts/argdigest_public_0_15_0_45_20261006.json).
Original SMonitor `f604b940ab281df4554869fdd24f796ea6d42c27` /
`4b876b4993b1e2caeed40851402a931f3b245ed7c1916d9483d81bc90274e31c`
and ArgDigest `57447cc4ec1f7ce85078f8a939892efd075bc919` /
`b0f22038a8ad1c888dca10adedaca0fa14d2383a685a97c0602b7ca05f29d6a1`
remain distinct from current source and other API-consuming repositories.

SMonitor #35 implementation **169d070b2b0894eb452c5a962db5757b92f202f8** retains
the release team's ten resources, installed caller and same-file promoter while
adding the maintained general @2 inventory, thin shared-tool invocation and
negative guards. Fifteen routes cover one recipe, five environments and nine
workflows. Required Python dependencies are empty with reasoned source-floor
non-applicability; optional bridge/collective checks are separate. Runtime Python
bounds, strict public docs channels, backend host requirements and template
recipe tests are maintained. Future candidate build/promote bootstrap requires
all twelve executed source jobs plus common policy, retaining its receipt before
mutation. Future installed test environments include developer parser tools.

Accepted provider **25363f2a2c902c04b2cdc8b301a3e1c1ff0c0918** passes native
37507549797 with **368 tests and dependent coverage**; 78 focused local checks
pass. The earlier independent-resource operation and invalid-requirements
diagnostic preserve valid @1/@2 behavior and existing client pins. Known client
acceptance notices follow the earlier prepublication impact notice; no other
migration is imposed.

Owner local checks pass **151 tests / two unresolved-report skips**, four
controlled route/resource/version mutations, required Ruff, indexes, whitespace
and conformance. Exact implementation CI 37529262021 and QA 37529261919 each
execute 15-route/default installed-bound checks and pass **631 / five skips**;
collective QA passes three tests, strict QA seven and wheel/CLI packaging smoke.
Docs 37529261976 builds with five warnings; policy 37529262843 passes. Archive
commit **55745e77b5893edd958325b81388b87f663f16be** changes reports only;
local closing reporting checks pass **103 / one unresolved-report skip**.
Its applicable policy 37529642555 and QA 37529641849 are inspected separately;
ordinary CI correctly has no Markdown-only trigger. Durable owner record:
`devguide/archive/complete_distribution_adoption.md`; guard:
`tests/test_distribution_inputs.py`. Complete adoption receipt:
[smonitor_distribution_adoption_45_20261006.json](../rollouts/smonitor_distribution_adoption_45_20261006.json).

Current inventory is **five adopted / six partial / four pending**, six bounded
confirmed deliveries and nine unknown access states. #45 remains partial.
DepDigest #30 and GH Run Receptor #60 are the next independent member reviews.
MolSysMT/MolSysViewer scientific deferrals, active PyUnitWizard OpenFF work and
private OpenCASTp acquisition debt #102 remain independent.

The frozen opt-in `argdigest-core` operator profile still identifies its reviewed
0.14.0 probe. The current 0.15.0 core probe changed and needs explicit profile
review before that optional operator prepares a future call. Actual core native
verification and the component's pre-promotion guard pass for 0.15.0; no copied
engine, silent inventory hash update or generic-profile bypass is used. Track
future operator-profile maintenance in the existing central #92 coordination.

## DepDigest maintained adoption — 2026-10-06

uibcdf/depdigest#30 closes with source implementation
`739c03f860bd019c247eb617c8e8e4e8b28f91b8` and archive
`df72daec1ec51f0c539b6e0413c2caacf91f6b61`. General @2 provider
`1f753e318d8dfa43c5bae1fa127e30ea86fa93b6` explicitly supports reviewed
legacy build-prefix Python, retaining exact public constraints and existing host
contracts/client pins. Provider native 37532615897 executes 370 tests and dependent
coverage successfully. DepDigest maintains twenty reviewed routes, thirteen
resources/generated version, default actual installed public bounds and negative
guards without changing its tested local publisher or original release bytes.

Local owner qualification passes 76 relevant checks, six closing reporting tests,
Ruff/conformance/indexes and disposable test-environment resolution/pip check.
Implementation CI 37533616391 and closing CI 37534007506 each execute the default
route audit and pass 193 tests/five unavailable sibling integration skips; the
new distribution negatives execute. Implementation/closing policy
37533617572/37534008610 and publication governance 37533617359/37534008512 pass.
Prospective candidate bootstrap requires all twelve executed source jobs plus
policy; promotion binds the archive/digest and all thirteen installed smoke jobs
before retaining evidence and invoking same-byte promotion. These future public
paths are guarded, not claimed newly exercised with a new release. Explicit
flexible staging priority and installed public-provider provenance remain.

Original public 0.13.0 source, producer, twelve installed cells, promotion and
SHA-256 `e011d725c8a831ae46cd6b8d114185d04248e32b4d6701c70f988d19cc69f67b`
remain in the prior release receipt; all thirteen current resources additionally
pass read-only archive inspection. Source and historical qualification are kept
separate in [the adoption receipt](depdigest_distribution_adoption_45_20261006.json).
The five informational #39 input hashes are reconciled by explicit route review,
with old/new digests retained; scientific commands/matrices/recovery stay unchanged.

Current registry: **six adopted / five partial / four pending**; six bounded
confirmed public deliveries and nine unknown access states. #45 stays partial,
with uibcdf/gh-run-receptor#60 next. MolSysMT/MolSysViewer scientific deferrals,
active PyUnitWizard OpenFF work, private OpenCASTp #102 and workspace #82 closure
debt remain independent. No new public build/upload/promotion or scientific manual
dispatch was performed.


### GH Run Receptor additive Conda source preparation — 2026-10-06

Owner uibcdf/gh-run-receptor#60 accepted the additional noarch route. Source
`47f125bfd6f3ed3d79d668243527370bd31aafab` prepares recipe, nine frozen schemas,
external `gh>=2.48.0`, generated version, prefix-owned command tests and
immutable shared manual stage/installed/promote wrappers. Accepted provider
`38db709ecc07451ff36ea84573d585f9af6b4df7` passes native governance
`37536963845` (372 tests and dependent coverage). Optional external requirements
retain old consumer behavior; eleven owner notices precede publication.

One recipe, 26 workflow routes and 16 artifact paths are guarded. Full local
source suite passes 580 tests with one explicit installed-only skip. Native
routine `37538410358` executes the 27-route check, passes 580 tests/one skip and
dependent Codecov publication. Source policy `37538411083`, Conda governance
`37538411183` and documentation/Pages `37538410353` succeed. Complete receptor
captures bind all runs to the exact source. Current general conformance passes.

The [preparation receipt](gh_run_receptor_conda_route_60_20261006.json) records source/native evidence, legacy
resource reviews, notices and solver-only probes. The publisher inventory now
records GH Run Receptor's actual shared caller: eight shared publishers. This
is availability of a prepared route, not credential access or public delivery.
The informative CI pilot's three changed inputs were explicitly reviewed and
refrozen at this source; existing full test/event/Python lanes remain unchanged.

The example does not authorize a release. A real owner plan, available
credentials, exact producer file, twelve installed cells and verified public
poststate are pending. The two unbuilt extension source/tag tests remain in
source compatibility and are explicitly deselected only from installed mode.
Runtime CLI subprocesses use safe-path imports. Original GitHub 1.2.0 files,
tags, extension/Action and wheel/sdist publication remain intact within this
work. No package publication, retag or deferred scientific matrix occurs.
Adoption stays **6 adopted / 5 partial / 4 pending**; GH Run Receptor and its
CI/recipe stay partial, with Conda access unknown.


### GH Run Receptor maintained GitHub archive guards — 2026-10-06

Owner uibcdf/gh-run-receptor#60 adds bounded wheel/sdist payload inspection at
`ec42d211b5288db395ca07928e62127d520e55ba`. Before upload and during draft/public verification,
metadata/generated versions, actual Python bounds, mandatory runtime files and
nine frozen schema digests must agree with the reviewed owner inventory.
Negative guards retain rejection even when outer file names and recomputed
asset/manifest digests match. Both formats reject unsafe/duplicate paths,
links, truncation and size/count violations without extraction or execution.
The GitHub publisher input hash is explicitly reviewed/refreshed; the three
informative CI pilot inputs and all other workflow hashes remain applicable.

The qualified source suite passes **627 tests / one explicit installed-only
skip**, with 27-route preflight, Ruff 0.16.5 (192 files), local guide lifecycle
and source conformance passing. Native exact-source routine `37541128876`
executes that preflight and 627 tests/one skip, retains measured coverage and
passes dependent Codecov publication. Policy `37541129763` and Conda governance
`37541129670` succeed. All three complete receptor captures bind source/jobs/steps.
Docs/Pages is outside this push's path filters; no publication or manual
compatibility matrix is dispatched. Existing public 1.2.0 wheel/sdist bytes pass
the new read-only check without rebuilding, replacing or retagging them.

The [sanitized receipt](gh_run_receptor_archive_guards_60_20261006.json) separates this evidence from the
first Conda release plan, credentials, producer archive, twelve native installed
cells and independent public poststate. Adoption remains **6 adopted / 5 partial /
4 pending**. GHR stays partial and Conda access unknown. A missing generic
wheel/sdist SDK profile is reported to central #45 for a future second consumer;
GHR's project-specific identity/resource validator remains owner-local. Existing
workspace #82 and private-acquisition #102 debt is retained.

## LinDelINT maintained inputs — 2026-10-06

Owner uibcdf/lindelint#13 delivers current controls at
`c4418a77d04da51f7a7ad061f24707c94ff028a7`, with fixed SDK
`38db709ecc07451ff36ea84573d585f9af6b4df7`. All sixteen routes are reviewed:
one noarch recipe, seven environments and eight workflows. Six generated
environments derive runtime requirements from metadata; development selects
Python 3.14 and source/docs preflight checks actual installed public bounds.
The unused counterpart fixture is explicitly resolved-package scope. The
maintainer removed unused scikit-learn from future runtime packaging/production,
retaining development/tests/docs. Registered consumer ElastNetMT received
prospective notice in uibcdf/elastnetmt#18; adoption and integration remain separate.

The resource inventory now includes thirteen tracked runtime files plus the
generated version. Sixteen owner negative guards exercise actual shared checks
for missing/weakened requirements, insufficient installed/source versions,
missing resources, stale embedded version and unreviewed workflows/candidate plans.
Build/promotion require the real committed owner plan and maintained executed gate
profile. The eight-cell installed descriptor requires all four provenance/science
steps and retains the whole scientific selection. Original producer/file identity
stays separate from an optional newer administrative qualification commit.

Native corrected CI [37544339221](https://github.com/uibcdf/lindelint/actions/runs/37544339221)
passes independent governance and all eight Linux/macOS arm64 Python 3.11–3.14
source cells (**13 scientific tests each**). Policy
[37544339763](https://github.com/uibcdf/lindelint/actions/runs/37544339763) and Conda
governance [37544339940](https://github.com/uibcdf/lindelint/actions/runs/37544339940)
pass. The shared native verifier confirms all eleven required jobs/steps and
stable exact-head attempts; full Receptor captures corroborate native results.
Initial control commit `349a2f5ae9f5fc17ed9a4b5c58007a5d05be9e42` had a real
owner lint integration failure: Ruff traversed the new SDK's starter template.
The initial failed result is preserved. Excluding the transient SDK fixes that
failure, with a controlled local file revert reproducing it.

Public-route review finds eighteen historical Conda files (latest 0.2.0) and no
GitHub release assets. Documentation distinguishes those observations from current
noarch/Python 3.14 qualification. The Python badge is retained until #14 admission.
No new version, build, upload, installed scientific dispatch or promotion occurred.
Source CI/recipe is now **ready**, whole adoption **partial**, access **unknown**.
The real release plan, exact original staged file, eight installed cells, same-byte
promotion and clean public delivery remain component-owned prerequisites.
The [receipt](lindelint_distribution_45_20261006.json) separates these domains.
Totals remain **6 adopted / 5 partial / 4 pending**. Next owner review:
uibcdf/elastnetmt#18, preserving active component work and #82/#102 debt.

## ElastNetMT resource/publication checkpoint — 2026-10-06

Source `e360e329ea3dc44f231fdb7611b133142439a9d4` in
uibcdf/elastnetmt#18 adopts accepted SDK
`38db709ecc07451ff36ea84573d585f9af6b4df7` for all four shared wrappers.
The complete inventory protects 36 tracked core/add-on payload files; eight
installed cells require all four exact-file/provenance/science steps. The
unusable illustrative plan describes all twelve existing required source jobs.
Optional newer administrative qualification preserves the original producer
commit and file digest. Nine negative/positive owner tests pass locally and in
independent hosted governance. Exact-head policy
[37546924920](https://github.com/uibcdf/elastnetmt/actions/runs/37546924920) and
Conda governance
[37546925021](https://github.com/uibcdf/elastnetmt/actions/runs/37546925021)
pass; the native verifier and complete Receptor captures corroborate them.

Source CI [37546924003](https://github.com/uibcdf/elastnetmt/actions/runs/37546924003)
retains the scientific failures and uncompleted cells recorded in the
[receipt](elastnetmt_distribution_controls_45_20261006.json). Linux 3.11 and
3.12 each fail the known trajectory/CuPy test while 34 tests pass. No successful
complete source watermark or installed artifact qualification is inferred.
Required metadata, source pins, scientific job/triggers/recovery, environments
and the existing moving-current Viewer add-on probe are preserved.

The existing add-on development contract
[37546924060](https://github.com/uibcdf/elastnetmt/actions/runs/37546924060)
passes its native executed installation/verification steps. Its success remains
separate from immutable installed-artifact qualification.

The fixed Git and Python-specific routes expose the shared capability need in
uibcdf/molsyssuite#107. Its [proposal](../archive/support_immutable_vcs_dependency_routes.md)
awaits the maintainer's direction before changing the API or installation
transport. Runtime environment/helper controls remain unfinished. Conda/PyPI
HTTP 404 and empty GitHub release assets are bounded public observations; no
real release version, plan, build, upload, installed dispatch or promotion is
selected. Whole adoption/CI recipe remain **partial**, access **unknown**.
Totals remain **6 adopted / 5 partial / 4 pending**. Existing #82/#102 debt and
the independent PharmacophoreMT dependency-manifest gap remain tracked.

## Optional Git/context resolution and first consumer — 2026-10-07

Shared uibcdf/molsyssuite#107 resolves optional @3 at immutable SDK
`2d32048457c6d37093ae509f5626d00a5cda121b`: 394 hosted central tests, 65 focused
cases, documented reusable parsing/provenance/context operations and eight
registered client handoffs. Existing @1/@2 contracts/pins retain their behavior.
See the archived record and the component-facing dependency-route API guide.

ElastNetMT #18 adopts at `ba6428105107cd97481cb4f353c01d973f5a9190`, preserving
scientific pins/steps/triggers/recovery. Eighteen routes, thirteen source records,
two unchanged actual manifests and seven contexts are guarded; sixteen owner
archive/source tests pass. Native CI 37579435066 successfully executes installed
context checks on Linux Python 3.11–3.14 with printed Git/version receipts. Policy
37579435796 and Conda governance 37579435740 pass, as does the separate current
Viewer probe 37579435142. Mac results remain pending at acquisition; known older
minor CuPy science fails. No successful complete source watermark is claimed.

Member review stays partial/CI-recipe partial/access unknown. Legacy broadcaster/
environment helpers and source-free actual checks still need review; complete
successful release science, real plan/access/original installed artifact/public
proof remain component-owned. No scientific failure is hidden or repaired, package
publication attempted or primary clone updated. The dated adoption receipt records
these bounds. Existing #82/#102 and the independent PharmacophoreMT graph gap
remain tracked; totals remain **6 adopted / 5 partial / 4 pending**. Continue #18
helper controls, then PharmacophoreMT and TopoMT.


## Current review and LinDelINT pre-publication adoption — 2026-10-08

Read-only current-main, owner issue and official public-route review finds no
new Conda delivery evidence for the six previously partial components. Five
public package endpoints return HTTP 404; LinDelINT still exposes the same
eighteen historical files through 0.2.0, with every coordinate/version/digest/
label tuple unchanged. The bounded GitHub release inventories supply no new
Conda qualification. These are public observations, not claims about private
staging or credential access. Current PharmacophoreMT scientific changes,
GH Run Receptor runtime changes and DockingMT coverage remain distinct from
new distribution artifact evidence.

The existing [Member review contract](../python_distribution_policy.md#member-review)
permits governance adoption before a first new public release with ready CI/
recipe, truthful installation scope and explicitly unknown access. LinDelINT
already has these executed controls. Its record's requirement to publish before
closing governance was stricter than that contract and is corrected in owner
uibcdf/lindelint#13, archived at `6314597cc7589986ff6b4c987dd6f996eb66d7c5`.
No shared policy or future publication/admission gate changes.
The still-open #14 guide now explicitly owns future delivery at
`a2443ca9f87a0b744451301a4103a7a210b50959`; only that pending record changes,
and final exact-head policy 37806575107 passes independently verified
conformance/lint/format steps without rerunning science.

Fresh independent acquisition verifies the original exact source `c4418a77`,
workflow/push event/attempt, complete job inventories and eleven mandatory
actually executed source/control jobs. The CI inventory's scheduled/manual
backlog job is inapplicable for that push and remains skipped; no recovery debt
is cleared. Nine reviewed input hashes match current pre-closeout main
`1a65d75`; its entire delta contains only synchronized guides. Final documentation
head `6314597` changes only devguide paths and passes exact-head manual policy
37805680870, conformance/lint/format and complete required job/step verification.
Three local reporting tests and generated-index checks pass in the qualified
Python 3.14.7 environment. Original route/resource/candidate negative guards
remain unchanged and relevant. No scientific rerun or artifact operation.

Disposition: **seven adopted / five partial / three pending**; publication
access remains **six confirmed / nine unknown**. Future real release plan,
authorized access, complete candidate science, original staged noarch file,
eight installed Linux/macOS arm64 Python 3.11–3.14 cells/four mandatory steps,
same-byte promotion, independent public clean installation and Python admission
remain open in uibcdf/lindelint#14. Historical files do not prove current noarch
or Python 3.14 delivery; support badge/provider pins remain unchanged.

| Owner | Current follow-up |
| --- | --- |
| uibcdf/gh-run-receptor#60 | Complete route-specific readiness/compatibility evidence; first Conda version, real plan, credentials and delivery remain developer-owned. Existing GitHub release evidence is separate. |
| uibcdf/topomt#78 / uibcdf/topomt#16 | Component-owned environment/scientific readiness and future candidate/delivery. No stability deadline or forced release; coverage deferral is separately #69 / TopoMT #81. |
| uibcdf/pharmacophoremt#10 / uibcdf/pharmacophoremt#23 | Review actual environment/current source prerequisites and future candidate/installed/public evidence; ongoing scientific work remains owner-local. |
| uibcdf/elastnetmt#18 / uibcdf/elastnetmt#19 | Retain source/scientific readiness gaps and environment evidence; future candidate/installed/public admission remains owner work. |
| uibcdf/dockingmt#47 / uibcdf/dockingmt#30 | Complete route-specific candidate readiness before the developer's first real Conda delivery; accepted #22 coverage does not qualify an archive. |
| uibcdf/lindelint#14 | Governance #13 is complete; actual next noarch delivery and Python admission remain open. |

The remaining partial classifications are not blanket demands to publish merely
to adopt governance; assess the actual readiness gaps and claimed routes under
the same existing contract. MolSysMT/Viewer review deferrals, OpenCASTp privacy
#102 and workspace #82 remain unchanged. Receipt:
[distribution_receiving_45_20261008.json](../rollouts/distribution_receiving_45_20261008.json).
