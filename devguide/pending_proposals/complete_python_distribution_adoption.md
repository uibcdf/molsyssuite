---
summary: Complete evidence-backed member adoption of the suite distribution policy.
issue: uibcdf/molsyssuite#45
status: partial
opened: 2026-09-24
closed:
verification: inspected
area: [governance, distribution, compatibility]
guard: tests/test_python_distribution_status.py
normative: devguide/python_distribution_policy.md
blocked_by: []
supersedes: []
---

# Python distribution member adoption

**Reported:** 2026-09-24; initial source baseline 2026-10-01; registry and
PyUnitWizard, Ackredit and Pytest Receptor release evidence reconciled 2026-10-06.
**Status:** Partial. Accepted suite policy, inventory validator and onboarding exist;
member-owned route adoption and publication-readiness evidence remain incomplete.

## What

Complete and record adoption of the accepted distribution contract in every
registered Python component, with truthful route applicability and bounded exceptions.

## How

Use `suite.toml`'s separate adoption, CI/recipe and publication-access fields.
Inspect required metadata, maintained recipes, runtime environments and source
routes; review local early/negative dependency checks, generated resources for
each claimed artifact, immutable publication and independent public poststate.
Record member-owned implementation/evidence rather than equating synchronized
guides with adoption. Reuse the existing repository and publication checkers.

The [dated rollout](../rollouts/python_distribution.md) preserves the initial 14 immutable
source identities, bounded audit results and component gaps, with dated updates
for the current 15-member Python inventory. The maintainer
authorized adapting the four legacy publishers now and migrating them to noarch
Python. See [the common route](../noarch_conda_workflow.md).

## Why

A passing general repository checker does not establish the entire distribution
contract. The source baseline finds omitted recipe requirements, weak environment
floors, unbounded recipe Python claims, outdated upload routes and artifact-specific
review gaps. Central policy ownership makes those adoption gaps visible without
assigning component scientific repairs to MolSysSuite.

## What is measured and what is assumed

All 14 initially inspected member snapshots pass the general repository checker.
The initial publisher-profile audit reported 26 findings in nine repositories,
three conforming publisher repositories and two with no publisher. Results are
bounded source observations, not installed-artifact evidence or a new defect
diagnosis for each custom workflow. Four delivered noarch migrations now have member-owned partial/partial/unknown
reviews in the initial delivery. The current registry has 15 Python reviews:
four adopted, seven partial and four pending. ArgDigest, Ackredit, Pytest
Receptor and PyUnitWizard have completed their owner route/guard reviews in
uibcdf/argdigest#28, uibcdf/ackredit#108, uibcdf/pytest-receptor#38 and
uibcdf/pyunitwizard#114;
their dated adoption receipts below preserve source and artifact evidence
separately. PyUnitWizard retains verified 0.28.1 evidence and its maintained
general-contract adoption below. Publication access
is confirmed only for six observed authorized Conda deliveries; the other
nine access states remain unknown, including GH Run Receptor's official Conda
route. SMonitor, DepDigest and GH Run Receptor have member-owned
partial reviews in uibcdf/smonitor#35, uibcdf/depdigest#30
and uibcdf/gh-run-receptor#60 respectively. See the
dated rollout for
full implementation identities and exact-source administrative runs.

Viewer#106 reports a completed working-tree audit, but that implementation is
absent from the inspected remote-main SHA. Its closure is recorded as incoming
evidence rather than silently credited to the inspected tree.

## Alternatives and refuted paths

- Updating a MOLI pin alone is no longer member adoption. MolSysSuite owns the
  member rules; the original issue's inheritance description is historical.
- Passing guide or general source checks is insufficient route evidence.
- Rebuilding an artifact cannot substitute for exact-file label promotion.
- Requiring full scientific runs for ordinary internal development pushes would
  contradict the accepted phased CI policy and the user's current work scope.
- Conda publication is not inferred for components documenting other supported
  routes or only source development.

## Shared dependency preflight proposal, 2026-10-06

Ackredit #108 inspected the existing recipe, repository and adoption tools and
reported the missing all-route constraint check in
[the provider handoff](https://github.com/uibcdf/molsyssuite/issues/45#issuecomment-6012850550).
The additive [dependency-route tool](../dependency_route_preflight.md) reuses
the existing noarch recipe/comparison operations, with provider-owned guards in
`tests/test_dependency_routes.py`. It introduces no automatic publisher or policy
caller rollout. Tool availability, owner acceptance, consumer invocation and
whole-policy adoption remain separate; no member state changes in this proposal.

The provider proposal uibcdf/molsyssuite#105 is now reviewed for direct
integration under the principal maintainer's standing authorization. Its exact
tool commit `43b9f94bf5ab0ec3f54a4b2ca5b23b791d6af0bc` is retained, with
21 passing focused route/recipe guards and documented conservative-profile
limits. The existing Ackredit, Pytest Receptor and PyUnitWizard owner notices
remain; ArgDigest #28 supplies the next concrete inventory/invocation. This
acceptance introduces no automatic publisher or policy-caller rollout and
does not itself complete any member review.

## Scope and exclusions


The 15 currently registered `python-package` members, including OpenCASTp.
MolSys-AI is outside this Python distribution
inventory. The central metapackage profile remains uibcdf/molsyssuite#67.
Scientific algorithms, postponed full scientific execution reviews and new package
publication are outside this administrative work. Existing owner-run release
evidence may be inspected without authorizing another build or execution.

## Acceptance criteria

- Member-facing policy and starter contract remain consistent with the suite-owned
  registry and reference the platform credential procedure once settled.
- Every Python member has a member-owned evidence-backed review of its actual
  dependency, CI, recipe, artifact and claimed public routes, or a bounded exception.
- Access stays unknown until verified without exposing credentials; neither access
  nor public availability is inferred from configuration.
- Offline governance and relevant hosted administrative checks pass.
- Complete adoption is assessed with
  `python devtools/scripts/python_distribution_status.py --require-adopted`.

The registered guard protects inventory coverage and prevents unsupported adopted
states; it does not prove component dependency or artifact correctness.

## Local implementation issues

Current relevant bounded local themes: uibcdf/molsysmt#245,
uibcdf/molsysviewer#101, uibcdf/molsysviewer#106 and uibcdf/ackredit#22.
Noarch migration reviews: uibcdf/topomt#78, uibcdf/pharmacophoremt#10,
uibcdf/elastnetmt#18 and uibcdf/lindelint#13. Provider exact-file upload:
uibcdf/action-build-and-upload-conda-packages#45. A narrow or closed local issue
is not automatically whole-policy adoption.

## Dependencies and risks

uibcdf/moli#8 owns the unresolved credential/access contract; unknown access does
not prevent an honest pre-publication review under the existing policy.
uibcdf/molsyssuite#47 tracks remaining installed Windows launcher evidence.
uibcdf/molsyssuite#59 owns the forward macOS support boundary.
Do not conflate these incomplete themes with a successful public installation.

## Provenance

2026-10-01; Linux, Python 3.13.15; central audit source
`bf3f06165f34ae542f830db57bf35519831224a0`.
Full member identities and repeatable commands are in the rollout record.


## PyUnitWizard release reconciliation — 2026-10-06

Existing uibcdf/pyunitwizard#112 delivers public 0.28.1. The central read-only
review verifies its five exact-source gates (29 required jobs), all 30 installed
cells and source binding, producer and same-file promotion. The public label,
solver index and downloaded archive match the original digest and source;
all eight dependency-route hashes match. Source conformance and the publisher
contract checker pass. Old production dependency floors and absent test NumPy
are corrected in this candidate.

Receipt: [pyunitwizard_distribution_45_20261006.json](../rollouts/pyunitwizard_distribution_45_20261006.json).
The documented local publisher equivalent remains applicable; the generic
shared noarch operator is not used for this orchestration. Archived owner
receipts describe a fresh public install and complete closures. Central work
performs no new install, scientific execution, build or promotion.

Whole-policy adoption remains partial: uibcdf/pyunitwizard#114 owns the formal
review and maintained runnable dependency preflight/negative guards. One-time
negative results in a release receipt do not protect later metadata/route
changes. Identify an existing reusable local equivalent first. Current library
work and the provisional API scope retain their existing boundaries.


## Ackredit and Pytest Receptor reconciliation — 2026-10-06

The current sources pass general repository conformance. Public Ackredit 0.10.1
and Pytest Receptor 1.2.1 independently pass the shared read-only operator:
original producer/source/file binding, all eight Linux/macOS arm64 Python
3.11–3.14 installed cells and main-label/solver-index availability. Their original
source-gate evidence confirms 17 required jobs for Ackredit and 18 for Pytest
Receptor; those historical runs are not repeated here.
Downloaded Conda bytes pass the shared recipe/archive metadata, resources,
version and runtime-constraint checks. Ackredit's packaged citation names 0.10.1.
Pytest Receptor's public PyPI wheel and sdist separately match recorded hashes
and pass its existing release checker. This review runs administrative checks and performs no build, install, solve
or scientific test execution.

Receipts: [Ackredit](../rollouts/ackredit_distribution_45_20261006.json) and
[Pytest Receptor](../rollouts/pytest_receptor_distribution_45_20261006.json).
The original Pytest Receptor tag predates later canonical guide additions;
its historical latest-guide comparison fails, while current main passes.
Retain the historical result and original tag/bytes; it is not current guide drift.

Both member reviews are partial/partial with confirmed access bounded to
observed authorized delivery. Formal route review and maintained dependency
preflight/negative guards remain in uibcdf/ackredit#108 and
uibcdf/pytest-receptor#38. Existing recipe, packaging/resource and installation
page guards are retained; their narrower coverage does not protect all runtime
environment/source constraints. Source routes and build-only profiles must be
classified before introducing new operations; reuse maintained tools first.
Ackredit's ongoing 0.11.0 candidate and contract review remain separate from
this public 0.10.1 evidence. Pytest Receptor's self-test exception is preserved.


## Core providers and GH Run Receptor reconciliation — 2026-10-06

SMonitor, ArgDigest, DepDigest and GH Run Receptor pass current general source
conformance and now have partial member-owned distribution reviews. Existing
public artifacts are inspected without a new build, install, solve or scientific
execution. The [dated rollout](../rollouts/python_distribution.md) and four
receipts preserve route-specific byte, metadata, resource and native evidence.

Concrete remaining work:

- uibcdf/argdigest#28: development, docs and test environments list required
  DepDigest/SMonitor without their metadata floors. The existing shared
  constraint operation rejects six comparisons; recipe and core environment
  preserve the bounds. Existing metadata/recipe/documentation guards do not
  cover those environments. Extend or reuse maintained operations and negative
  guards, then complete the formal route review. Original/current dependency
  inputs match; the successful public 0.14.0 qualification remains intact.
- uibcdf/depdigest#30: all nine release preflight input hashes still match.
  The owner receipt already classifies routes and records one-time negative
  cases. Identify or deliver maintained whole-route dependency/resource
  guards rather than treating the receipt as protection of future changes.
- uibcdf/smonitor#35: retain the local publisher and bounded Windows/Python
  3.13 installed-command smoke at the 0.18.0 producer. Complete claimed
  installed-cell evidence, formal route/resource review and maintained guards.
  Empty required Python dependencies permit reasoned non-applicability for
  sibling-floor tests; optional pytest bridge evidence stays separate.
- uibcdf/gh-run-receptor#60: public GitHub assets/extension are verified, but
  do not imply an official Conda or PyPI route. Review a prospective Conda
  route or bounded exception/local profile; no exception is accepted here.
  Preserve exact schemas and classify archive guards and external `gh`. The
  twelve-cell compatibility workflow builds distinct wheels; previous public
  wheel installation evidence has its own scope under uibcdf/molsyssuite#75.

Member owners decide implementation and release timing. A missing reusable
operation affecting several members belongs back in uibcdf/molsyssuite#45 with
concrete inputs; consumers should not copy a private implementation. No package
bytes, public requirements, source tags, current development worktrees or
internal push permissions are changed by these central adoption records.

## ArgDigest environment correction — 2026-10-06

The six omitted provider bounds reported above are corrected in ArgDigest
`94cffa861146c6520585aefff02523f03e0a9704`, published directly on `main`
under the standing internal authorization. Development, docs and routine-test
environments now preserve `depdigest>=0.11.0` and `smonitor>=0.16.0`.
The existing compatibility module protects all four runtime-bearing
environments, classifies the build-only environment and rejects six absent,
unbounded or weaker-provider mutations. Stronger explicit bounds are accepted.

The regression module reproduced three failing routes before the correction;
afterward all 22 cases pass. Six owner reporting checks, Ruff, owner indexes,
central offline governance and general component conformance also pass. The
local Python 3.14.7 checks are administrative, with the eight previously known
workspace conflicts retained; they do not qualify a scientific installation.
Hosted common policy and publication-policy runs pass on the exact correction.
Routine Linux/Python 3.14.7 CI passes 314 tests with one unavailable sibling
integration skipped, retaining normal fixtures and selection. Exact evidence is retained in the
[correction receipt](../rollouts/argdigest_environment_floors_45_20261006.json).

The original public 0.14.0 file and its original producer/qualification evidence
remain unchanged in the earlier review receipt. This source correction does
not inherit those gates for a new release or dispatch another scientific matrix.
The local durable record is `devguide/pending_proposals/complete_distribution_adoption.md`
in uibcdf/argdigest#28. That issue and the central inventory remain **partial**:
complete applicable-route and maintained preflight review still belong to the owner.

## ArgDigest adoption completed — 2026-10-06

The subsequent owner review completes uibcdf/argdigest#28 at implementation
`ad920c515f7c08b6a85492f6aa2094405683899d`, with its archived report at
`7f93b23cc8da64747d3e4608218d769f5e7cc21f`. The review classifies one recipe,
five environments and eleven workflows and reuses the accepted shared tool
`43b9f94bf5ab0ec3f54a4b2ca5b23b791d6af0bc`, retained in provider integration
`689e226fe22367d39ee9aedbd3c0230b313f4edf` (350 native governance tests pass).

All 17 route checks execute in normal CI before its test job; that same exact
implementation passes 315 tests / one unavailable sibling integration skip and
both hosted policies. The publication decision invokes the pinned operation on
the exact candidate before the unchanged shared publisher. Reviewed exclusions,
Python narrowing and provider/resource negative guards remain explicit. Thirty-six
local administrative checks and six closing-report checks pass; current workspace
dependency findings are retained separately and do not qualify scientific runtime.

The current registry is **one adopted / ten partial / four pending**, with
ArgDigest CI/recipe **ready** and publication access still confirmed only for its
observed authorized 0.14.0 delivery. The original producer/file/full-installed/core/
promotion and owner-measured clean public installation retain their exact identities;
this source review publishes no new archive or compatibility claim. The
[adoption receipt](../rollouts/argdigest_distribution_adoption_45_20261006.json)
preserves implementation, tool, inputs, native gates and earlier dated receipts.
MolSysSuite #45 remains partial for the other fourteen member reviews.

## Ackredit formal adoption — 2026-10-06

The owner independently completed uibcdf/ackredit#108 and merged its existing
proposal #110 at `edd6df2ae3ebe9143ca87043c3ccb94207a4a545`. Central read-only
review of the archived closeout at `61742c40793cb66136a77b2e19516579774c6a81`
passes all 16 routes and general conformance. The accepted shared preflight pin
remains `43b9f94bf5ab0ec3f54a4b2ca5b23b791d6af0bc`; its actual CI invocation,
complete runtime bounds, reviewed exclusions and local/provider negative guards
are retained. Staging requires successful exact-candidate CI before its build.

GH Run Receptor inspection of that closing head verifies seven successful CI
jobs, both hosted policies, the executed 16-route audit and five installed source
cells: 2119 passed and eight skipped in each. The skipped cases remain visible;
these ordinary source cells are separate from the eight-cell public archive
qualification. Owner-measured 0.11.0 producer/file/installed/receiving/promotion
and clean public installation evidence remains in its original immutable receipt.
The independently reviewed 0.10.1 receipt is preserved unchanged.

Ackredit advances to **adopted / ready / confirmed**, with access bounded to
observed authorized deliveries. The current registry is **two adopted / nine
partial / four pending**, six bounded confirmed deliveries and nine unknown
access states. The [adoption receipt](../rollouts/ackredit_distribution_adoption_45_20261006.json)
separates current source adoption, native gates, original public evidence and
owner-measured later delivery. Central API/admission decisions, provisional
evidence APIs, shared-workspace qualification and other members remain separate.
No package rebuild, promotion, scientific matrix dispatch or Windows/PyPI claim
is added. MolSysSuite #45 remains partial for the other thirteen member reviews.

## Pytest Receptor formal adoption — 2026-10-06

uibcdf/pytest-receptor#38 is complete at implementation
`4065003d56d15735fb2bbc5e71ced50d5d988d4c` and archived closeout
`9220984a8402718b93518600ffe035e3f3ff5ec3`. All 13 routes (one recipe, two
environments, ten workflows) pass the accepted shared preflight. Required
metadata bounds, historical 3.13 compatibility, shared routine 3.14 development,
build-only routes and the own-source self-test exception remain explicit.

The audit runs inside the existing required `lint` check before tests, benchmarks
and builds; strict PR protection retains its original 11 source checks. Conda
requires the executed audit step. Future PyPI builds bind their canonical numeric
tag to the checkout and reuse shared verification of the existing ordinary/full
native source jobs before building, retaining a separate source-gate receipt.
Publication itself is not triggered by this adoption review.

Both implementation and closing CI pass all 12 jobs. Every Linux Python
3.11–3.14 / pytest 8–9 cell passes 220 serial and 220 xdist tests without skips;
the audit, packaging, benchmarks, dependent coverage and all three other hosted
governance workflows pass. Forty-five selected local tests and five closing-report
tests pass. The [adoption receipt](../rollouts/pytest_receptor_distribution_adoption_45_20261006.json)
retains input hashes, native identities and original public 1.2.1 evidence.

Pytest Receptor is **adopted / ready / confirmed**. Current totals are **three
adopted / eight partial / four pending**, six bounded confirmed deliveries and
nine unknown access states. Original Conda/PyPI files and clean-install evidence
remain separate from CI's temporary source-wheel smoke. No public release,
registered-archive rebuild/upload/promotion, API/schema/client pin change or
Windows claim is added. The seven current workspace closure findings remain
under #82; #45 remains partial for the other twelve member reviews.

## PyUnitWizard profile review — 2026-10-06

Review of clean owner main `2ab37a525ce99728ad8aee846b4a4f7acc4f1b65`
under uibcdf/pyunitwizard#114 finds one local noarch recipe, nine environments
and twelve workflows. Seven environments carry runtime requirements; build and
setup are bootstrap-only. All eight previously recorded recipe/runtime file
hashes still match the original 0.28.1 review receipt. The recipe preserves the
public required closure; the owner has no required sibling-source install route.

The accepted provider pin `43b9f94bf5ab0ec3f54a4b2ca5b23b791d6af0bc`
cannot yet audit this complete inventory using its default profile:

- Five runtime environments contain ordinary Conda single-equals pins, including
  optional providers and ArgDigest. The PEP 440 parser rejects those expressions;
  Conda version-prefix/build semantics must be preserved rather than mechanically
  substituting `==`.
- The OpenFF profile deliberately selects Python `>=3.12,<3.15` and Pint
  `>=0.24,<0.26`, with `nodefaults` after the two public channels. Its narrower
  Python interval and stronger Pint constraint are outside the default exact
  comparison/whole-minor profile. They are not evidence of weaker public metadata.
- The local release plan and recipe are a reviewed local publisher equivalent.
  `inspect_recipe` rejects the local plan because it lacks the shared plan schema;
  no shared `resources.toml` is present. Requiring that schema would conflate the
  dependency audit with adoption of another publisher.
- Baseline CI, full matrix, release gates, documentation and public-install
  workflows explicitly select strict channel priority. The source OpenFF/storage
  workflows do not explicitly select it; inspect the setup provider's actual
  configuration before claiming priority compliance. The installed staging
  workflow deliberately uses flexible priority with exact-file/public-provider
  checks, and must retain its separate reviewed provenance profile.

### General provider correction — implementation prepared

The principal maintainer requested a general solution and authorized continued
work on that direction. The initial component-profile proposal is replaced by
the [general route contract](../dependency_route_preflight.md#general-route-contract-2).
The successor inventory `molsyssuite.dependency-routes@2` distinguishes route
purposes for every component, while preserving the original `@1` default/API
and immutable consumer pins. There is no PyUnitWizard-specific exemption.

Production environments preserve the advertised numeric release range.
Development, test, documentation and optional-runtime environments may select
a compatible narrower range with a reason. The common comparator proves the
whole numeric release interval, rejects omissions/weaker floors/wider ceilings
and empty ranges, and preserves the original Conda selector and build string.
Unsupported expressions fail for review rather than being silently guessed.

Conda prefixes can also admit non-release versions, so actual installed public
bounds are a separate check. The `@2` CLI performs that check by default; an
explicit `--declared-only` is labelled incomplete and cannot replace a CI or
candidate qualification. This does not claim transitive closure, installed build
provenance, scientific execution or exact-file verification.

Local noarch recipes reuse shared `render_recipe` and
`inspect_recipe_dependencies`, independently of a publisher's plan schema. Their
receipt states dependency-only scope; the owner's version/resource/installed/
public-poststate gates remain required separately. Strict public priority,
`nodefaults`, reviewed staging provenance, source identities and manual workflow
hash review retain their existing distinctions.

Provider tests in `tests/test_dependency_constraints.py`,
`tests/test_dependency_routes.py` and `tests/test_noarch_conda.py` protect the
general contracts and original behavior. An isolated complete 22-route
PyUnitWizard inventory passes declaration review and actual public-bound checks
using the qualified shared interpreter. The new module first failed collection
before implementation and then passed its eight focused regression cases; the
combined local check passes 35 tests. The
[prepared-provider receipt](../rollouts/dependency_contract_general_45_20261006.json)
retains reviewed input/code hashes, outcomes and limits.

Provider publication/native qualification and the owner CI/candidate invocation
remain separate delivery steps. PyUnitWizard has not adopted the prepared tool;
its actual OpenFF/storage priority still needs verification before integration.
The existing release, scientific work and public metadata are preserved.

### Evidence and retained state

Diagnostics ran read-only on Linux with Python 3.14.7 in
`molsyssuite@uibcdf_3.14`, using the existing shared environment-requirement parser,
`required_constraints` and `inspect_recipe`; no consumer import, solve, build or
installation was performed. Both receptor imports resolve to their eligible
primary local clones. The seven current `pip check` findings remain independent
workspace debt under #82. The preflight status found PyUnitWizard clean and
current; other developer worktrees were preserved.

PyUnitWizard remains **partial / partial / confirmed** and central totals remain
**three adopted / eight partial / four pending**. Original 0.28.1 artifact,
producer, thirty installed cells and promotion receipt remain unchanged. No
scientific execution, OpenFF integration change, new publication, API-stability
claim or consumer rollout is authorized by this profile proposal.

The GitHub issue was found closed at 2026-10-06 09:52:23 UTC despite this active
record and subsequent partial-adoption handoffs. Restore its open state and
current summary so board closure does not imply completion of the twelve
remaining reviews; the historical close event is not adoption evidence.

## General provider and PyUnitWizard adoption completed — 2026-10-06

The principal maintainer authorized a general solution after questioning the
component-specific proposal. Accepted additive provider
`20628bd5dba6d759669b0d444fe657eb1edad33f` implements the common route-purpose
contract, bounded Conda selector/build interpretation and actual installed public
bounds. Its native governance passes 364 tests and dependent coverage upload;
74 focused local dependency/publication tests pass. Existing @1 contracts and
ArgDigest/Ackredit/Pytest Receptor pins remain compatible and unchanged; all
three owners received immutable delivery and adoption guidance. This supersedes
the prepared-only state in the earlier profile review, not its historical inputs.

uibcdf/pyunitwizard#114 is resolved at implementation
`d128b37b4339d3b8520678cc9d8924f902d14a7b`, archived closeout
`6cfc9ae5281532d46a09d5059902d49fa7c1d19a`. All 22 routes are maintained;
default installed public-bound checks execute before existing source tests/builds.
Conda, OpenFF/Pint/provider/interpreter conditions remain unchanged. Six developer
environments add parser tooling only; optional public source workflows explicitly
use strict priority. The owner keeps its local publisher. Its future prebuild
operation requires five exact-source native workflows and 29 executed job/step
profiles, with a separate candidate receipt, retaining all existing file gates.

Native ordinary CI 37497852682 executes the audit and passes **785 tests / 19
skips** on Linux/Python 3.14. Implementation policy 37497853464 and closing
policy 37499214277 pass. The documentation-only closing source has no configured
ordinary test trigger; its executable inputs are identical. Forty focused owner
checks, nine closing reporting checks, required Ruff, conformance and indexes
pass. No full/optional scientific matrix is dispatched for this adoption.

The [adoption receipt](../rollouts/pyunitwizard_distribution_adoption_45_20261006.json)
separates these source controls from the earlier unchanged 0.28.1 exact public
file, original source/producer/thirty installed cells/promotion. No archive
rebuild/upload/promotion, public metadata/version/tag, provisional API or
Windows/PyPI claim is added. Primary developer clones and existing workspace
closure debt remain unchanged.

Current registry: **four adopted / seven partial / four pending**, six bounded
confirmed authorized deliveries and nine unknown access states. Central #45
remains partial; SMonitor #35, DepDigest #30 and GH Run Receptor #60 are the next
independent reviews. MolSysMT/MolSysViewer scientific deferrals and private
OpenCASTp acquisition debt #102 remain separate.


## SMonitor maintained-control review prepared — 2026-10-06

The next owner review is uibcdf/smonitor#35. The mandatory remote preflight
finds a clean/current SMonitor primary clone at
`6feac9728cc35d57cbc92f284d7040d7f04cb35b`, including subsequent owner
provider-registration/capture work (#37/#38). Preserve that implementation;
current source adoption cannot certify those APIs using the old public archive.
Other dirty/ahead/behind clones remain intact. Qualified Python 3.14.7 and the
primary receptor imports are verified; seven existing pip-check findings remain
#82 debt.

The local publisher/version/freezer/immutable-coordinate/public-poststate tests
are retained. Required dependencies are empty, so required sibling floor/source
cases are reasoned non-applicability. Optional bridge and collective-source
checks retain distinct evidence. One recipe, five environments and eight
workflows form the current 14-route review. Source-test environments need explicit
supported Python bounds; ordinary docs routes still select defaults in their
workflow condarc despite the reviewed public environment. Early invocation and
maintained route/resource negatives are the implementation scope.

The resource inspection already exists inside the full shared noarch inspector.
Expose it as `inspect_resources` and an optional local `@2` resource inventory,
preserving both schemas and all existing consumers. Two SDK regressions reproduce
the absent public operation; a route regression reproduces its absent explicit
opt-in before implementation. Seventy-seven focused dependency/publication tests
pass, including original full-publisher checks. Provider/owner native qualification
and immutable delivery remain pending at this prepared snapshot.

Original public 0.18.0 digest, producer, Windows/Python 3.13 installed command and
owner Linux/Python 3.14 install evidence remain unchanged. Completing the missing
installed platform cells is a separate scope decision pending with the principal
maintainer; no twelve-cell artifact claim or new publication is inferred here.


The prepared resource provider was published as
`262c1993c39fe8430de3e9a3d87bb6eaf2e7efee`. Native governance 37506200697
executes 367 tests and its dependent coverage upload successfully. Current
ArgDigest/Ackredit/Pytest Receptor @1 inventories still pass (17/16/13 routes),
and PyUnitWizard @2 passes all 22 routes and actual installed bounds. Notices
preceded publication; existing pins are unchanged.

SMonitor's isolated source review passes 14 routes after correcting its resource
inventory to the actual template namespace (no templates/__init__.py is shipped).
Four negative mutations reject missing recipe Python, a weaker/wider environment,
a missing template and wrong generated-version target. The first missing-list
failure identified its route but returned a generic NoneType error; a provider
regression reproduced that before a fail-closed diagnostic now names the missing
public requirements. The extended focused check passes 78 tests. This changes
invalid-input diagnostics only; previous valid contracts remain available.
Owner source invocation and missing installed-file cells remain separate evidence.


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
