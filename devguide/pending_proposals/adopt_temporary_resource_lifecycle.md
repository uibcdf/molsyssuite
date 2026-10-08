---
summary: Adopt owner-controlled temporary resource cleanup across suite members.
issue: uibcdf/molsyssuite#104
status: partial
opened: 2026-10-06
closed:
verification: inspected
area: [governance, tooling]
guard:
normative: devguide/temporary_resources.md
blocked_by: []
supersedes: []
---

# Temporary resource lifecycle and member adoption

**Reported:** Ackredit qualification inventory on 2026-10-06.
**Status:** policy-v1.5.8 published; all sixteen registered guides delivered
and exact administrative gates passed. Component tool lifecycle and retrospective
owner reviews remain pending; this coordination issue stays partial.

## What

The initial report measured 65.7 GiB in /tmp and 96% root-disk use. Disposable
environments/caches dominated several retained Ackredit resources. The principal
maintainer clarified that useful evidence may remain in /tmp, without relocation.
Resources must be removed when their usefulness ends.

## How

The accepted temporary_resources.md text applies to all registered members.
The normative policy, canonical guide and root/starter instructions are published
under policy-v1.5.8; the registered copies have been delivered.
Use existing registry/synchronizer for byte-identical guide delivery. Record
source delivery independently of applicable tool lifecycle and historical cleanup.
Prefer managed temporary directories and retain caller-owned outputs/environments.

## Why

Unowned obsolete outputs can exhaust the shared filesystem. Blanket age/prefix
cleanup can destroy active/human work. Shared policy establishes an owned lifecycle,
without a separate global cleaner or new mandatory scientific test gate.

## What is measured and what is assumed

The initial issue retains dated disk/resource measurements. On 2026-10-07, all
five specifically named example paths are absent; removal attribution is unknown.
The filesystem now reports 52% used/about 54 GiB available. This is a bounded
observation, not a complete /tmp inventory or a claim this task reclaimed space.
Shared tools use managed qualification fixtures/temporary manifests; the existing
Conda-tool failure-propagation/cleanup test protects the manifest lifecycle.
Hosted runner disposal and artifact retention are inspected, not newly executed.
Component-owned tools require separate review when applicable.

## Alternatives and refuted paths

No whole-machine temporary cleaner, compulsory evidence relocation, fixed-age
expiry or copied per-component cleanup framework. Reuse existing lifecycle tools;
report missing provider capabilities with concrete consumer evidence.

## Scope and exclusions

Policy, registry, canonical guide, contributor/starter instructions and maintained
sixteen-member rollout. No scientific dispatch, environment removal, existing
package reconstruction, credentials change or deletion of another session's work.
Publish policy-v1.5.8 for the new shared rule. Existing caller pins remain
compatible; this introduces no new blocking scientific or CI-pattern gate.

## Acceptance criteria

- Accepted policy states applicability, cleanup/retention and bounded exceptions.
- Deliver byte-identical guide copies from the registered canonical source.
- Keep tool inspection/executed cleanup and actual source delivery separate.
- Retrospective resources receive owner review; preserve active/needed evidence.
- Coordinate with uibcdf/moli#61 and leave incomplete owner reviews visible.

## Local implementation issues

The rollout identifies every registered guide consumer. Existing distribution/CI
owner issues receive the adoption handoff; new local defects belong with each
component. Ackredit supplies the initial resource case; MOLI #61 owns its platform
coordination. Temporarily private OpenCASTp retains #102's access decisions.

## Dependencies and risks

Primary clones may contain active work. Use isolated committed snapshots for guide
updates and only the canonical synchronizer. A guide delivery does not prove all
scientific/documentation/build tools comply. Needed temporary evidence is ordinary
retention; a missing lifecycle implementation has an owned bounded exception.

## Provenance

2026-10-07 Linux x86_64; molsyssuite@uibcdf_3.14, Python3.14.7.
Existing seven #82 conflicts and eligible local receptor origins unchanged.
No unrelated directories or environments are cleaned by the adoption record.

## Publication authorization — 2026-10-07

The principal maintainer approved publishing policy-v1.5.8 and delivering all
sixteen registered guide copies. The previous draft-only checkpoint is
bffffcd5fe478d3f62f2c49af9024a6c4bd6c84d. The prepared version transition,
agent instructions and Conda lifecycle tests pass: 156 existing tests and the
offline governance guard. Python 3.14.7 and the two local editable receptors
are verified; seven existing dependency conflicts remain tracked in #82.
Advance notices identify the same policy impact and the component review owner.
Publication and exact delivery evidence are retained in the rollout receipt.
Guide synchronization alone will not close the pending tool lifecycle reviews.

## Publication and delivery evidence — 2026-10-07

Policy tag policy-v1.5.8 resolves to aba762dde114dfa78e8947cf1fe6e0b66f0d1643;
its immutable annotated tag object is 7cdfa5161d1b6f124ac245e2dec2941574e36014.
The exact-source native governance run
[37675458139](https://github.com/uibcdf/molsyssuite/actions/runs/37675458139)
passes all 428 central tests, publication-control checks and the dependent
coverage upload. Earlier policy tags and consumer workflow pins remain unchanged.

The official synchronizer delivered sixteen byte-identical guide copies through
guide-only direct commits, preserving scientific deferrals. Every member's exact
administrative workflow is verified by source SHA, native workflow, event, jobs
and required executed steps; all sixteen pass. MolSys-AI's umbrella uses its
reporting-only route, without a Python-package or scientific-suite claim.
The central post-delivery guide audit
[37677065843](https://github.com/uibcdf/molsyssuite/actions/runs/37677065843)
passes the fifteen public-member jobs and retains the private OpenCASTp checkout
failure under #102. OpenCASTp's own exact administrative workflow passes; that
neither grants central/public access nor changes the provisional decision.
Initial pre-distribution guide failures remain in native history.

MolSysViewer advanced concurrently; the isolated delivery base was fast-forwarded
to its new source before re-synchronization and rechecking. Primary clones received
no branch/worktree writes or cleanup. Some primary observations changed during
independent component development; the receipt preserves that distinction.
All sixteen task-owned clean isolated clones were removed after exact-commit
preflight, with zero cleanup failures. Small needed receipts/logs may stay in /tmp.

The direct script invocation exposed a shared editable-namespace collision,
subsequently resolved in uibcdf/molsyssuite#111 at source
75f6feb86d8ac4db6fb4a784b89b67e461336988. During delivery the same synchronizer succeeded as
`python -m devtools.scripts.sync_vendored_guides` from its owner root. This
workaround does not change the published tag. The initial automatic dispatch
review rejected the unproven per-caller scope; after inspection of every immutable
workflow and provider, the restricted administrative dispatch was accepted.
No scientific suite, component package build or publisher was dispatched.

The receipt is `devguide/rollouts/temporary_resources_104_20261007.json`.
Guide delivery is complete; applicable component tool lifecycle and retrospective
resource reviews remain with the named owning issues. Administrative evidence
neither clears scientific full-suite debt nor proves every tool cleans correctly.

## Bounded tool review and owner handoff — 2026-10-07

Run `suite_status.py` before reading fetched component sources. This review used
immutable `origin/main` commits, preserving dirty TopoMT/OpenCASTp worktrees and
all other primary clones. It did not run the deferred scientific suites or mutate
the qualified Python 3.14.7 environment and its seven tracked #82 conflicts.

The separate receipt
`devguide/rollouts/temporary_resource_tools_104_20261007.json` records the exact
sixteen source commits, screened paths, bounded central checks and owner issues.
The first pass covers tracked `devtools`, `scripts`, `.github` and `tests` for
explicit temporary-resource/cleanup primitives. It does not exhaustively cover
package runtime, custom caches, implicit engine outputs or every tool. A missing
pattern is not evidence of compliance. Full local review and retrospective
resource ownership remain pending for every component.

Central executable checks pass: `qualify_noarch_install.main` removes its real
managed fixture after successful and failed synthetic qualification callbacks
while preserving the caller's receipt. The existing Conda-tool regression
`tests/test_conda_environment_tools.py::EnvironmentToolsTests::test_create_vectors_strict_priority_cleanup_and_failure_propagation`
passes, proving failure propagation and removal of the temporary manifest with
the manager substituted. No solver or environment creation was executed.
Receipt acquisition is inspected to read bounded ZIP data in memory; installed
artifact directories/prefixes and development workspaces remain caller-owned.
Those operations must not delete caller resources merely because a call ends.
Hosted runner/artifact lifetimes remain inspected rather than newly dispatched.

| Owner finding | Evidence | Required local outcome |
| --- | --- | --- |
| [uibcdf/ackredit#130](https://github.com/uibcdf/ackredit/issues/130) | Actual persistence benchmark string, synthetic callbacks: directory/session remain on both exits; adjacent test cleanup is success-only by inspection. | Manage fixture/writer lifetime without adding setup/teardown to the timed region; protect test failure cleanup. |
| [uibcdf/pyunitwizard#115](https://github.com/uibcdf/pyunitwizard/issues/115) | Actual concurrency child string with synthetic configuration: both exits leave generated client packages. | Manage child resources through both threads and failure/timeout while preserving the cold-interpreter race test. |
| [uibcdf/pytest-receptor#40](https://github.com/uibcdf/pytest-receptor/issues/40) | Actual token harness function deletes a pre-existing synthetic active-run sentinel; both benchmark tools suppress removal errors by inspection. | Isolate/refuse concurrent ownership, preserve reproducible token measurements and expose cleanup failures. |
| [uibcdf/molsysviewer#178](https://github.com/uibcdf/molsysviewer/issues/178) | Inspected two complete Qt child strings and parent calls: `delete=False` HTML has no cleanup. | Keep HTML alive through asynchronous reads, then clean on success/failure; retain deliberate candidate build outputs separately. |

All executed probes were confined to managed private parent directories; every
fixture was removed after observation. Neither the real shared `receptor-bench`
directory nor other sessions' resources were touched. Synthetic callbacks prove
the harness lifecycle, not scientific behavior, library compatibility, Qt runtime
or performance. The four incoming owner issues carry actionable evidence and
acceptance criteria; no component source or local queued record was edited.
They are implementation follow-ups, not accepted exceptions or new suite gates.

Small task-owned probe scripts/results remain in `/tmp` while these findings need
them. No broad cleanup is authorized from this source inspection. Policy-v1.5.8,
guide bytes and all consumer pins remain unchanged. #104 stays partial for owner
fixes and remaining reviews; uibcdf/moli#61 retains its platform work and #102
retains the provisional private-access decision.

## Pytest Receptor benchmark correction — 2026-10-07

The focused implementation in uibcdf/pytest-receptor#40 is published at
e100d65e8f49fdb7a93edb8fe541ff296c16c6e0; its report/index archive is published at
aa1bedd2b6f91abf63fe396f832c4acf7539ed6d. The component-owned record is
`devguide/resolved_bugs/benchmark_resource_ownership.md`; its durable guard is
`tests/test_benchmark_resources.py`.

The token harness keeps its stable physical rootdir and uses atomic `mkdir` to
claim exclusive ownership. It refuses an occupied file/directory without
deleting it, including while another invocation is running. Both harnesses
remove their own fixtures on success/failure and expose removal errors, keeping
a failed child visible in the exception context. Performance uses a managed
TemporaryDirectory with setup/teardown outside the timed child operation.
No new lock service, global cleaner or shared tool is needed.

Twelve local regressions pass; six fail against the original source. They cover
occupied paths, concurrent ownership, both child outcomes, observable cleanup
failure and four real pytest subprocesses with identical rootdir. Five local
reporting tests and affected Ruff checks pass. The existing qualified environment
and editable primary origins were preserved; no local package was reinstalled.

The exact-source native
[Tests 37686778761](https://github.com/uibcdf/pytest-receptor/actions/runs/37686778761)
passes all eight Python 3.11–3.14 / pytest 8–9 combinations, with 232 tests per
ordinary and distributed suite. Actual token/performance benchmark, lint,
packaging/clean-wheel checks and dependent coverage upload also pass. Reporting,
policy and publication-control gates were separately verified by source, event,
workflow, jobs and required executed steps. These are the component's existing
test workflows; no package was uploaded, promoted or released.

The archive commit's final native
[Tests 37687458509](https://github.com/uibcdf/pytest-receptor/actions/runs/37687458509)
and reporting/policy/publication-control gates are also exactly verified. The
owner issue is closed; the clean isolated clone and three fixture roots have
been removed, with zero observed cleanup failures. The tool-review receipt keeps
the original failing-source evidence and the independently verified repair.
The repair affects local developer harnesses outside the installed plugin;
registered guide consumers need no API, guide, version or caller-pin adoption.

Three explicit task-owned local fixture roots were removed after their last use.
Primary clone head/status are verified unchanged, and caller environments
remain intact. Ackredit #130, PyUnitWizard #115,
MolSysViewer #178 and remaining full tool/retrospective owner reviews keep #104
partial. This repair does not establish full component compliance or affect the
provisional OpenCASTp decision in #102.

## Ackredit persistence benchmark correction — 2026-10-07

The focused implementation and archived record in uibcdf/ackredit#130 are
published together at 273fb8bc8fa11307800af8d8b7177a64de2be467. The owner record is
`devguide/archive/benchmark_persistence_resources.md`; the durable module guard is
`tests/test_benchmark_resources.py`.

ExitStack registers writer closure before enabling persistence, closes the writer
while its session still exists and then removes its managed directory. Partial
setup, operation and closure failures also clean; removal failures stay visible
with earlier exception context. Bare/tracked controls and the perf_counter pair
are unchanged; setup/teardown remain outside the timed operation. The adjacent
legacy-session test owns a managed directory through reading and asserting.
Historical performance numbers were not regenerated.

Eight regression cases fail against the original source, with two controls
passing. All ten pass after repair; the original positive legacy-format test and
reporting guard also pass (12 selected tests). Whole-repository Ruff and archive
index checks pass. Synthetic callbacks exercise the actual benchmark string;
no MolSysMT scientific benchmark or deferred suite was executed.

Exact native [CI 37690106374](https://github.com/uibcdf/ackredit/actions/runs/37690106374)
passes its five installed test cells: Linux Python 3.11–3.14 and macOS arm64
Python 3.14, plus Ruff/dependency checks and Sphinx -W. The policy and Conda
publication-control workflows also pass. Source SHA, push event, workflow,
all expected jobs and required executed steps are independently verified in the
tool-review receipt. No package build/upload/promotion workflow was dispatched.
Registered ACKREDIT_GUIDE.md consumers need no API, guide or caller-pin adoption.

The owner issue is closed. Its clean isolated clone and two created fixture roots
were removed; the reporting run never created its named fixture root. No cleanup
failures were observed. Primary Ackredit HEAD/status are verified unchanged,
caller environments and editable receptor origins remain intact, and the seven
existing #82 dependency conflicts remain accepted. Small disposal provenance
stays in /tmp only while central coordination needs it.

The original failing-source screen/probes remain separate from this repair.
PyUnitWizard #115, MolSysViewer #178 and all full tool/retrospective owner reviews
keep #104 partial. The next concrete owner correction is PyUnitWizard #115;
OpenCASTp's provisional access decision in #102 and MOLI #61 are unchanged.

## PyUnitWizard concurrent client correction — 2026-10-07

The focused implementation in uibcdf/pyunitwizard#115 is published at
47972f16affadd51c6101eabfe9cfce32c16ebbf; the final integrated/archive head is
08b31070a737643a0fce5f72992de2b89ac814db, based on fetched
e128e3e2a96e3676d08838158c8d3fd784fcde83. The owner record is
`devguide/solved_bugs/concurrent_client_fixture_ownership.md`; its module guard
is `tests/test_concurrent_registry_resources.py`.

The existing test parent owns a managed directory passed to the cold interpreter.
Its lifetime covers both import threads and subprocess completion or termination;
success, configuration failure, process-start failure and timeout all clean.
Removal errors propagate with an earlier child assertion in exception context.
The two clients' source must remain present during configuration; barriers,
configuration statements, eight attempts and the 300-second timeout are preserved.
No registry behavior, new shared tool or cleaner is introduced.

Six new regressions fail against the original source and pass after repair,
including real cold child processes and a real timeout with the child reaped.
All eight original real race repetitions and nine reporting checks also pass
(23 selected tests). Whole-repository Ruff/index checks pass. Source integration
reruns nine reporting plus nine dependency-route tests; the owner's actual
preflight verifies 22 declared-and-installed public-bound routes with unchanged
provider pin 20628bd5dba6d759669b0d444fe657eb1edad33f.

The initial isolated clone copied primary local main. A real-remote fetch showed
three existing governance commits and the initial non-fast-forward push was
rejected without remote writes. Rebase onto the fetched base and regenerate the
archive index, preserving both #114 and #115. Original harness bytes are identical
in both bases; unchanged lifecycle/race evidence remains applicable. The archive
retains these integration checkpoints; no force push or primary clone edit.

Exact final-head native [CI 37692655957](https://github.com/uibcdf/pyunitwizard/actions/runs/37692655957)
and policy run 37692657280 pass, verified by SHA, push event, workflow, every
expected job and required executed steps. Ordinary CI covers Linux Python 3.14,
import outside checkout, dependency/style checks, the existing test suite and
both Codecov uploads. No optional full-matrix, OpenFF/storage or publication
workflow was dispatched; no new artifact or scientific compatibility claim.
Registered guide/dependency consumers need no API, guide, constraint or pin adoption.

The owner issue is closed. The clean isolated component/provider clones and four
created fixture roots were removed without cleanup failures. Primary PyUnitWizard
HEAD/status, qualified environment, receptor origins and seven existing #82
conflicts are unchanged. Small disposal provenance remains only while #104 needs
it; the original failing-source screen/probes remain distinct from this repair.
MolSysViewer #178 is the remaining concrete finding; all full tool/retrospective
owner reviews also keep #104 partial. MOLI #61 and OpenCASTp #102 are unchanged.

## MolSysViewer Qt HTML correction — 2026-10-07

The focused implementation in uibcdf/molsysviewer#178 is published at
2da28dd8820c758effb54638e626e952c2fc4e48; the final integrated/archive head is
7a95251762bd84f0e9deb31899f82efcff6c0afb on fetched
484686524d4b928fddc96b98db7e01e3821edbc6. The archived owner record is
`devguide/archive/qt_probe_html_ownership.md`, indexed under the existing flat
archive convention. Guard: `tests/test_qt_probe_resources.py`.

The local reusable test helper owns a managed HTML directory in the parent and
passes its path to both existing real Qt child programs. HTML remains present
through asynchronous reads and completion or timeout/termination with the child
reaped. Removal errors propagate; original transport/generation assertions,
curated environment and 90-second timeout remain. Eight lifecycle regressions
fail before repair and pass afterward, covering both probes on success, controlled
failure, real timeout and cleanup failure. Both original real Qt probes pass.
The initial selected scope has 201 passing checks; after integrating the owner's
documentation closures, all 180 current reporting checks pass. Executable helper,
probe, guard and build-script bytes are unchanged by that integration.
Whole-repository Ruff, metadata audit, generated queue indexes and bash syntax
pass. The initial restricted-sandbox socket denial is recorded separately from
the successful unsandboxed real-process evidence; the qualified environment is
unchanged.

The build script documents the invoking task's ownership of printed OUT and
retention through installed qualification, promotion/public verification or failure
diagnosis, followed by owner closeout. This documentation change preserves
original candidate bytes and caller-supplied outputs; no build/publication ran.

Exact final-head native [policy 37695281713](https://github.com/uibcdf/molsysviewer/actions/runs/37695281713)
and [publication controls 37695290087](https://github.com/uibcdf/molsysviewer/actions/runs/37695290087)
pass. Receipts verify SHA, workflow, workflow_dispatch event, all expected jobs
and required executed steps. GitHub rejected the bare SHA dispatch; main was
confirmed at the intended SHA and both native runs independently bind it. The
explicitly authorized skip/manual administrative route leaves full scientific
and browser CI debt in uibcdf/molsysviewer#93 with Diego/Liliana and its existing
scheduled/manual CI.yaml and CI_e2e.yaml recovery. No rendering/framebuffer,
scientific-suite, installed-package or public-artifact qualification is claimed.
Registered dependency consumers require no API, guide, dependency or pin adoption.

The owner issue is closed; all 29 current queued documents agree with its board.
The clean isolated clone and five created fixture roots were removed with zero
cleanup failures. Primary Viewer HEAD/status and caller environments are preserved.
Small disposal provenance remains while #104 needs it. Original dated source-screen
and probe evidence remains distinct from subsequent repairs.

All four concrete findings from the bounded screen are now resolved: Pytest
Receptor #40, Ackredit #130, PyUnitWizard #115 and MolSysViewer #178. All sixteen
full component-tool and retrospective owner reviews still keep #104 partial;
source delivery and these focused corrections do not prove complete compliance.
MOLI #61 and the provisional OpenCASTp #102 access decision remain unchanged.

## GH Run Receptor acquisition correction and review — 2026-10-07

Subsequent source-focused review expands the original corpus-validator screen
to the provider's acquisition core, owner tooling and workflow output custody.
At original c2c952946ccc4c57da0f64dbeec632fc93fb2f70, aborted capture/permission
failure retains unpublished staging; interrupted refresh loses the prior path;
failed/interrupted JSON or binary consumption retains live children/open pipes
and binary interruption leaves partial bytes. These newly reproduced findings
belong to uibcdf/gh-run-receptor#63, separately from the original four findings.

Published source/archive f19fcf94bb2735f61ef79cd9c2629dede715e700 protects
owned staging and restores previous bundle bytes on interruption. The provider's
private `_owned_process` context is reused by JSON and binary transport to reap
failed children and close stdout; interrupted downloads remove partial bytes.
Cleanup failures remain visible. Successful output, CLI exit 130, native GitHub
facts, frozen serialized resources, caller cache identities and public 1.2.0
bytes remain unchanged. No new timeout/retry/signal or global-cleaner policy.

Guard `tests/test_bundle_resources.py` has twenty passing real filesystem/child
resource cases; seventeen fail against the original affected operations, and
three capture controls pass before. All 647 ordinary source checks pass with
one installed-Conda-only skip. The unchanged immutable SDK
38db709ecc07451ff36ea84573d585f9af6b4df7 verifies nine published contract freezes
and 27 declared-and-installed public-bound routes. Ruff, local report lifecycle
and generated indexes pass. Intermediate stale-index and incomplete failing-before
guard observations are retained separately from final success.

Exact [routine/coverage 37733511777](https://github.com/uibcdf/gh-run-receptor/actions/runs/37733511777),
[policy 37733512289](https://github.com/uibcdf/gh-run-receptor/actions/runs/37733512289)
and [Conda controls 37733512337](https://github.com/uibcdf/gh-run-receptor/actions/runs/37733512337)
pass, independently verified by SHA/event/workflow/attempt/all expected jobs and
required executed steps. Routine coverage upload success is not proof of service
processing. No compatibility/installed matrix, real release or science dispatched.

The owner resolution is archived/indexed at
`devguide/archive/resolved_bugs/clean_aborted_bundle_staging_on_interruption_and_permission_failure.md`.
Its maintained `devguide/resource_lifecycle_review.md` distinguishes resource-focused
source inspection, local acquisition proof, hosted results and pending retrospective
owner cleanup. Explicit release/archive/sanitized outputs remain invoking-task-owned.
Fourteen registered dependency consumers received actionable source-only notices
in existing owner issues; no consumer adoption, dependency minimum or guide/pin
change is claimed. Existing public artifacts are not declared repaired.

The owner issue is closed through its local reporting helper and confirmed on the
board. Clean source/SDK clones and eight created fixture roots were removed without
cleanup errors; primary source HEAD/status, caller environments and other/human
resources are preserved. Small disposal provenance remains while #104 needs it.
All five known concrete owner corrections are resolved; full historical resource
review and broader tool qualification keep #104 partial. DepDigest's resource
review is the next proposed component scope. MOLI #61 and provisional OpenCASTp
#102 access remain unchanged; scientific deferrals are preserved.

## DepDigest local environment helper correction — 2026-10-08

Subsequent bounded review at d5a7ac0ae66beaff1ba080e7114bcdd55398c21c
finds an owner-local outcome defect: create/update discard a failed Conda manager
result and shell strings split spaced executable/input paths. No create-manifest
cleanup leak is reproduced; its existing context already cleans correctly.
uibcdf/depdigest#32 resolves this at immutable source/archive
b8cba76f5f83d989d724af6ac8fcb418adcc6052 by passing argument vectors and
propagating the manager status. Caller files/environments stay owned by caller,
including partial failed operations; no rollback/retry/deletion is guessed.

Guard `tests/test_conda_env_helpers.py` executes real controlled children: eight
passing cases, six failed before and two ordinary-success controls passed.
Qualified Python 3.14.7 has 201 passing source tests and five explicitly skipped
collective sibling cases. Initial 196 passes/ten skips are separate: supplying
the unchanged SDK 1f753e318d8dfa43c5bae1fa127e30ea86fa93b6 executes the five
shared-input negative checks. Twenty distribution routes verify declared-and-
installed public bounds. Both helps, Ruff (153 formatted files), report lifecycle
and generated indexes pass; primary editable receptors/environment are unchanged.

Exact native push [CI 37737551830](https://github.com/uibcdf/depdigest/actions/runs/37737551830),
[policy 37737552350](https://github.com/uibcdf/depdigest/actions/runs/37737552350)
and [publication controls 37737552413](https://github.com/uibcdf/depdigest/actions/runs/37737552413)
pass with independently verified source/event/workflow/attempt/jobs/required
executed steps. Upload success does not prove Codecov service processing.
Owner record is archived in `devguide/solved_bugs/propagate_conda_environment_helper_failures.md`;
its current `devguide/resource_lifecycle_review.md` separates inspected custody,
executed helper tests, hosted gates and pending historical review.

Reviewed central `conda_environment_tools.apply_environment` under #108: optional
adoption requires @3/profile, whereas this owner retains qualified @2 routes.
This correction adds no duplicated generator or implicit adoption. Runtime API,
dependency, guide/pin and publisher consumers require no migration or notices
for these provider-local helper calls. No solver, environment mutation, artifact
build/upload/promotion or scientific/installed matrix was invoked.

The owner issue is closed after archived guard and exact native proof. Two clean
owned source/SDK clones plus six created fixture/cache roots were removed with
zero cleanup failures, after exact HEAD/status/single-worktree and primary
preservation checks. Small task provenance remains while #104 needs it. Other
human/task resources and shared environments were preserved. All six known
concrete corrections are resolved; complete historical attribution/cleanup and
broader tool qualification keep #104 partial. Original screen evidence remains
unchanged. MOLI #61, provisional OpenCASTp #102 and scientific deferrals remain.

## SMonitor source-tool custody and outcome review — 2026-10-08

Subsequent review at c7bfb0b69b4f26e140c5b1668db76c3174b3f2b7 reproduces
two owner-local developer-tool failures: catalog loading deletes prior caller
probe modules/reuses stale helpers (uibcdf/smonitor#43), and operability evidence
reports a failed suite/comparison with exit zero (uibcdf/smonitor#44). Existing
load_catalog/main operations own the corrections; no copied helper/framework,
new dependency or runtime/serialized contract is introduced. Fix
84b496263c885599aa8041abb46d93e92d67055d and integrated archive head
7b017d8545ff318c7da20dd4a01f5c8a33870ce2 preserve exact namespace identities
on success/error/interruption and retain useful bundles while returning failure.

Eleven new guards pass after seven failures/four controls against original
operations: six real import-custody cases plus four real tiny-suite CLI cases and
one primary-status precedence control. An initial {} comparison baseline is
accepted by the comparator; the fixture was corrected to malformed JSON and
all eleven before/after cases were rerun. Eighteen focused tests and all 653
ordinary source tests pass in Python 3.14.7, with one absent collective sibling
fixture skip and one intentional resolved-only reporting-rule skip. The unchanged
SDK 25363f2a2c902c04b2cdc8b301a3e1c1ff0c0918 verifies fifteen declared-and-
installed public-bound routes. Both helps, reporting/index checks and complete
Ruff (126 formatted files) pass. Seven accepted #82 environment conflicts remain.

Exact native push [CI 37739447740](https://github.com/uibcdf/smonitor/actions/runs/37739447740),
[QA 37739447711](https://github.com/uibcdf/smonitor/actions/runs/37739447711)
and [policy 37739448476](https://github.com/uibcdf/smonitor/actions/runs/37739448476)
pass independently verified by SHA/event/workflow/attempt/all jobs/executed
required steps. QA actually includes Linux/Python 3.14 sdist/wheel install/CLI
smoke and the collective error path. These are ordinary QA checks, not a complete
public installed-platform matrix. Upload success is not Codecov processing proof.

Both owner defects are closed/archived with relevant guards; the current bounded
resource review is maintained in `devguide/resource_lifecycle_review.md`. Eleven
registered SMONITOR_GUIDE consumers received advance source-tool notices before
publication, then the same notices were updated with immutable head/native proof.
They are candidate operators, not eleven demonstrated source-tool adoptions;
ArgDigest's dated operability workflow is the concrete existing example. No
installed SMonitor dependency, synchronized guide/pin or publisher migration is
required. Runtime signal/catalog/bundle contracts and public bytes are unchanged.

Exact HEAD/clean status/single-worktree and primary preservation checks precede
removal of two isolated source/SDK clones plus seven owned fixture/cache roots.
All nine roots were removed with no cleanup errors; caller/shared environments,
primary editable source and other active/human task work are preserved. Small
provenance remains while #104 needs it. No local solver/environment mutation,
public upload/promotion or deferred scientific suite was invoked. All eight known
concrete corrections are resolved; original dated evidence stays unchanged and
historical owner cleanup/broader qualification keep #104 partial. MOLI #61 and
OpenCASTp #102 remain their separate coordination decisions.

The maintainer requested subsequent review of uibcdf/molsysmt#237 and #244.
That separate receiving reconciliation is now complete: both issues are closed,
and policy-v1.5.9 admits the verified Python 3.14 support using existing exact
source/public-pair evidence. The dated receipt is
`devguide/rollouts/molsysmt_python314_ecosystem_51_20261008.json`.

## ArgDigest bounded tool review — 2026-10-08

Review source 15b1921b6bbe1b4bf4abcb091e91f51d74927325, preserving the
original first-pass screen above. No concrete resource lifecycle defect is
reproduced in the reviewed local operations. Release/install validators retain
caller receipts, prefixes and package inputs; network/file contexts close and
bounded captured child processes are used. The version freezer intentionally
modifies two files in an explicitly supplied build source. Its caller must supply
a disposable build source; this review neither builds nor replaces a package.
Backlog/reporting tools retain caller outputs or maintained indexes. Existing
test fixtures use pytest ownership or finally-based namespace restoration.

All 54 existing backlog/release/install/reporting checks pass with Python 3.14.7
and the isolated ArgDigest source import verified. Six additional executed
lifecycle cases use synthetic files and a real isolated Python child: receipt
verification preserves input files on success/failure; version freezing preserves
unrelated output and rejects an invalid precondition before mutation; the scoped
fresh-import helper restores exact caller module identities and removes new
scoped modules on success/exception. The managed probe fixture is removed.
These are bounded custody observations, not a new complete installed matrix,
scientific integration run or qualification of real public artifacts.

Hosted CI/docs/core and pinned shared publisher/install/promotion callers were
inspected without dispatch. Their provider implementations remain separately
owned; no SDK/workflow pin, recipe, dependency, runtime API or guide changes.
No component source fix or consumer adoption notice is required by this result.
Results and limits are embedded in
`devguide/rollouts/temporary_resource_tools_104_20261007.json`.

The clean exact-source single-worktree clone and pytest fixture root were removed
after proving the primary clone's HEAD/status unchanged. Zero cleanup failures;
caller environments and other active resources are preserved. Small task
provenance remains useful while #104 is active. Broader tool/platform qualification
and retrospective owner attribution remain pending; #104 stays partial. The
private OpenCASTp and deferred scientific decisions retain their own scope.


## LinDelINT bounded lifecycle and registered resource closeout — 2026-10-08

Reviewed immutable current LinDelINT `a2443ca9f87a0b744451301a4103a7a210b50959`
without component edits, package installs, provider-pin changes or science.
The maintained create/update helpers use managed YAML and checked literal argv
with strict priority; the legacy creator delegates. Owner environments remain
caller-owned, including failures; documented explicit update pruning must not
be applied to the shared ecosystem environment. The broadcaster check is
read-only over owner-selected documents; the recipe/unrelated files remain
caller-owned. Wheel inspection closes its ZIP without extraction/deletion.
Backlog/reporting tools retain explicit output custody; hosted CI/docs/release
runner/provider ownership is inspected, not newly dispatched.

Twelve real CLI lifecycle cases pass: create/update success, failing/unavailable
manager and visible cleanup-reporting faults (eight); synthetic wheel success/
missing-resource outcomes (two); generated-environment check success/drift
(two). Fake manager only: no real Conda/Mamba operation, solver, environment
creation/update or actual partial-prefix qualification. Cleanup reporting is
injected after actual disposal, not a real permissions failure. Temporary
manifest/probe directories disappear; input bytes and caller evidence survive.
Five existing backlog tests, three reporting tests, current indexes and the
non-mutating generation check pass with Python 3.14.7. No concrete lifecycle
defect is reproduced; no new test framework or source repair is introduced.

The exact clean single-worktree source clone, managed probe fixture and owned
pytest fixture root are removed with zero observed cleanup failures. Primary
LinDelINT HEAD/status, qualified environment and editable receptor origins are
preserved; seven accepted #82 conflicts remain. Broader scientific runtime,
actual manager/backend/platform and historical attribution remain unqualified.
The original 2026-10-07 screen is preserved separately from this bounded review.

A read-only check covers **55 explicit paths already registered** in the two
#104 receipts, not a global age/prefix search. **54 are already absent**,
including all five initial named examples; their deletion attribution remains
unknown and this task claims no historical disk recovery. The one present
resource is our `/tmp/molsyssuite104-guide-rollout`: five regular JSON files,
102,731 payload bytes. Its TASK_OWNER declares #104 and permits retirement once
follow-ups no longer need the duplicated delivery metadata. All sixteen source/
guide/native delivery identities match the committed canonical receipt; current
helper/history work does not need those old duplicate stages. No source, script,
package, environment, clone, symlink or unrelated output exists in that directory.
Explicit fuser checks show no open user, and file inode/mtime/digest/complete
entry checks pass immediately before removal. The five files and directory are
removed; durable source/native/notice evidence and original dated claims remain
committed. Other resources are not deleted or credited to this cleanup.

Receipt: [resource_receiving_104_20261008.json](../rollouts/resource_receiving_104_20261008.json).
#104 remains partial for broader tool/platform/runtime qualification and
retrospective owner review beyond these explicit records. All eight known
concrete defects remain resolved. MOLI #61, private OpenCASTp #102, source-only
LinDelINT distribution adoption #45 and scientific deferrals retain their scope.
Small current-task closeout metadata is retained only until central exact-head
CI and issue handoff, then removed.

## ElastNetMT and PharmacophoreMT environment-tool review — 2026-10-08

This additive bounded review uses ElastNetMT source
`d26b6bc8299befb8c01b196eb1bbaf2e24759eee` and PharmacophoreMT source
`cdf79fdd725d2ec383103e4940073abface26e4b`. Their original dated first-pass
screens remain unchanged. ElastNetMT's local operator loads dependency contracts
from fixed SDK `2d32048457c6d37093ae509f5626d00a5cda121b`; PharmacophoreMT's
entry points delegate to shared environment tools at
`8f00e6d9de943b6e4710ea62936e2ebea00fad24`. No pin or component source changes.

All **47 existing checks pass** in qualified Python 3.14.7: ElastNetMT has
14 environment, five backlog and three reporting tests; PharmacophoreMT has
eight environment, five backlog, three reporting and nine evidence-reader tests.
Both non-mutating environment generators and report indexes pass. SDK loaders
verify exact commits, clean provider tools and import origin. Existing #82
dependency findings remain accepted; no new dependency-closure success is claimed.

**Sixteen actual CLI lifecycle cases pass**, eight per component: create/update
with success, manager exit 17, unavailable manager and cleanup exception. Only
private recording executables run; update targets task-owned synthetic active
prefixes, never the shared development environment. The manager observes the
temporary YAML while present and strict channel priority. YAML directories are
absent after return; original manifests, caller prefix sentinels and output
receipts outside the scratch directory survive. Failure exits are visible.
The cleanup exception is injected **after successful real disposal**, and proves
error reporting, not an operating-system removal failure. The managed probe
fixture is removed after its final use, with no cleanup failures.

ElastNetMT keeps its documented local update `--prune`; the fixed shared operator
does not prune. This review introduces no migration or common pruning rule.
PharmacophoreMT's evidence reader checks local compressed/uncompressed identities
and preserves original failed/unknown scientific fields; passing those nine tests
grants no scientific acceptance. Source inspection distinguishes managed scratch
directories in scientific validators/benchmarks from persistent caller report and
`--artifacts` destinations. Those calculations and hosted component callers were
not executed; their platform/runtime evidence remains pending.

Receipt: [environment_resource_receiving_104_20261008.json](../rollouts/environment_resource_receiving_104_20261008.json).
Central commit `f10833d1b5f870cfc364a0b22891a8072abea1c6` passes native
run [37839464460](https://github.com/uibcdf/molsyssuite/actions/runs/37839464460).
Its exact SHA/workflow/event/attempt, both jobs and required executed steps are
independently verified. This is administrative evidence, including coverage
upload; it grants no component scientific or platform qualification.
All four clean exact-source/single-worktree source/SDK clones and both selected
pytest fixture roots are removed after explicit ownership/activity checks, with
zero cleanup failures. Primary HEAD/status are unchanged before and after
retirement. Small metadata remains only until final CI and issue handoff.
Caller environments and other tasks are preserved. No concrete defect is reproduced,
so no component fix or adoption request follows. #104 stays partial for broader
applicable tool/platform/runtime qualification and retrospective owner review;
the eight resolved owner defects, MOLI #61 and private OpenCASTp #102 retain
their separate status. No real manager, solver, scientific suite, build,
publication or promotion was invoked.

## TopoMT memory profiling and MolSys-AI umbrella review — 2026-10-08

TopoMT source `1ad2610634b16f9ae1d30ebc29323c09af012593` reproduces a
development resource defect: the memory profiler overwrites a caller-side
`profile_memory_1crn.pdb`, leaves the extracted file after success/failure and
leaves owned tracemalloc active after a failed build. The actual-tool reproducer
uses inert scientific substitutes and a synthetic ZIP. This is resource custody,
independent of TopoMT's early scientific maturity.

Owner issue **uibcdf/topomt#95** is repaired and archived at
`74191c225850e5e54cc40bc278d077388f2d4057`. Managed scratch encloses the extracted
PDB's last use; `finally` releases only tracing started by the measurement.
Caller files, report destinations and existing tracing survive. Eight guards
pass; seven failed before repair and the caller-tracing control already passed.
All 24 selected administrative checks pass with scientific conftest disabled,
plus affected-source Ruff and current indexes/non-mutating environment generator.
The initial 15-case invocation omitted `--noconftest`; its result is superseded
and supplies no scientific or administrative qualification here.

Exact manual native CI [37841619267](https://github.com/uibcdf/topomt/actions/runs/37841619267),
policy [37841622269](https://github.com/uibcdf/topomt/actions/runs/37841622269),
publication controls [37841624822](https://github.com/uibcdf/topomt/actions/runs/37841624822)
and Ruff [37841626057](https://github.com/uibcdf/topomt/actions/runs/37841626057)
pass with SHA/workflow/event/attempt/jobs/required executed steps verified.
CI's aggregate log reports all 34 devtool tests passing; the exact discovered
source has 18 distribution, eight environment and eight new resource guards.
Individual method names are not printed. The internal direct push uses a
conditional skip and explicit `probe_backlog=true` administrative route; the
scientific matrix job is independently observed skipped. Full-suite debt remains
with Diego/Liliana and existing nightly/manual recovery; these checks do not
clear it or qualify scientific stability, Python support or public artifacts.
No runtime API, measurement formula/field, dependency, SDK/policy pin or guide
change; the local helper needs no shared-provider consumer migration.

MolSys-AI umbrella source `ec27c78e179e2f85cf3ff541829ed5fbd1d467e6` has three
passing reporting tests and current indexes. Its three administrative scripts
close file contexts; checks preserve caller files and explicit generation writes
maintained caller indexes. No scratch lifecycle defect is reproduced. Five actual
CLI cases preserve inputs for valid/invalid/missing resource catalogs and
current/stale report-index checks. Eight further TopoMT environment CLI cases
exercise create/update success, manager failure, unavailable manager and cleanup
error with private recording executables and synthetic active prefixes. All
13 cases pass; their managed fixture is removed. Cleanup-reporting exceptions
are injected after real disposal, not actual permissions failures.

The umbrella's documented strict resource-catalog check exits 1 because its
talk/paper records contain placeholder dates, years and repositories. This is
recorded separately in **uibcdf/molsys-ai#6**, not claimed as a clean catalog or
a resource leak. Lifecycle receiving belongs to existing uibcdf/molsys-ai#5;
child server/client/agent implementations and historical owner cleanup are
excluded from this umbrella review.

Receipt: [topo_ai_resource_receiving_104_20261008.json](../rollouts/topo_ai_resource_receiving_104_20261008.json).
All nine concrete lifecycle owner corrections are now resolved. #104 remains
partial for broader applicable tools/platform/runtime and retrospective owner
review. All three clean exact-source/single-worktree clones and both created
pytest fixture roots are removed after verified owner delivery and explicit
ownership/activity checks; zero cleanup failures. Small metadata remains only
until exact central CI/handoff. Primary TopoMT's
existing modified version file, other primary sources, shared environment and
active work remain preserved. Existing seven #82 dependency findings and private
OpenCASTp #102 retain their scope. No full scientific suite, solver, package
build/upload/promotion or global temporary-resource cleanup was invoked.


## 2026-10-08: bounded DockingMT developer-tool receiving

Current DockingMT source `8da5bbcede2101c3f4b0e058cd5b0711a8522cc9`
reproduces a caller resource defect in the optional result-export memory sample:
its unconditional `tracemalloc.stop()` terminates tracing already owned by a
caller, on both return and failure. **uibcdf/dockingmt#48** is resolved at
`03281126e658d5b39aa5369b09e1bb40a8211134`. The helper now starts/stops only
tracing it owns. Two of five isolated stdlib-only regression guards fail before
the repair; all five pass afterwards. They execute locally, with an inert result
and no scientific imports. Selected administrative checks pass 15 tests with
`--noconftest`, plus affected-source Ruff and current reporting indexes.

The actual profiler parent also passes six lifecycle cases using private real
Python children and inert summary bookkeeping: success, worker failure, invalid
JSON, cleanup-reporting error after actual disposal, output failure and retained
failed mismatch report. Scratch is removed, children are awaited/reaped and
caller inputs/evidence preserved. Real engines, scientific equivalence, native
interruption and real OS deletion failures are not qualified. Qualification,
replay, preparation, distribution fixtures and hosted-call custody receive only
the source review described in the receipt; no scientific execution is inferred.

Exact manual [policy](https://github.com/uibcdf/dockingmt/actions/runs/37844136940),
[publication controls](https://github.com/uibcdf/dockingmt/actions/runs/37844138766)
and [backlog probe](https://github.com/uibcdf/dockingmt/actions/runs/37844141027)
pass with source/workflow/event/attempt/jobs and required executed steps
independently verified. Those gates do not execute the new local regressions.
The scientific matrix is independently observed skipped (`probe_backlog=true`);
full-suite debt remains with dprada/LMMV and existing nightly/manual recovery
under uibcdf/dockingmt#30 and #104. No runtime API, timing formula, dependencies,
SDK/policy pins, guides or release change; no shared consumer migration needed.

Receipt: [docking_resource_receiving_104_20261008.json](../rollouts/docking_resource_receiving_104_20261008.json).
All ten known concrete lifecycle corrections are now resolved. #104 remains
partial for broader applicable tools/platform/runtime and retrospective owner
review. Task-owned resource retirement is recorded in the receipt. Primary
DockingMT and other active worktrees, the shared environment and the seven
existing #82 dependency findings remain preserved.

Both clean exact-source/single-worktree clones and both owned pytest fixture
roots were retired after durable receiving and activity/ownership checks; zero
cleanup failures. Three concurrently created, untracked DockingMT conformer
files are preserved byte-for-byte. Small task metadata remains until exact
central CI and the #104 handoff.


## 2026-10-08: bounded receptor developer-tool receiving

Pytest Receptor source `98f34db82a50260d1eed0517f2d824d0ef064e91`
reproduces a second developer benchmark lifecycle defect: failure or interruption
of `wait4` leaves its direct owned process alive while enclosing scratch can
be removed. **uibcdf/pytest-receptor#41** is resolved at
`5fe7d98f4a4a6f7f2bca1f250427ad48178c73a2`. The exceptional path now
kills/reaps the child before re-raising; ordinary time/RSS/status calculations
remain unchanged. Two real-private-child guards fail before repair and two
success/nonzero controls already pass; all four pass afterwards. The proof
covers direct POSIX children with injected wait faults, not descendants, actual
OS faults or Windows RSS. Selected local resource/reporting checks pass 21
cases with conftest disabled; affected Ruff and report indexes pass.

Exact manual [reporting](https://github.com/uibcdf/pytest-receptor/actions/runs/37846098228),
[policy/Ruff](https://github.com/uibcdf/pytest-receptor/actions/runs/37846103059)
and [publication controls](https://github.com/uibcdf/pytest-receptor/actions/runs/37846106950)
pass with SHA/workflow/event/attempt/jobs and required executed steps independently
verified. These hosted administrative gates do not execute the four new guards.
The authorized conditional skip avoids full benchmark and package build runs
for this resource-only tranche; routine/compatibility/benchmark/build debt stays
with dprada/LMMV and existing weekly/manual recovery. No plugin/public/serialized
API, dependency, measurement formula, guide, pin or release changes.

GH Run Receptor source `cb202db78f539e1185ba03de26e57233ad5c9e80`
passes 31 selected existing acquisition-resource, public-validator and capture
benchmark tests plus current report indexes. Six actual-validator-parent cases
use private real stdlib-only children returning synthetic reports/native facts:
success, acquisition failure, invalid JSON, native mismatch, replay interruption
and cleanup-reporting failure after actual disposal. Owned scratch is removed
and caller evidence preserved. No live GitHub/actual CLI corpus or real OS
deletion-failure claim follows. Source review of other maintained scripts and
hosted callers remains separate; no new concrete defect reproduced, no component
change. Existing uibcdf/gh-run-receptor#63 receives this bounded handoff.

Receipt: [receptor_resource_receiving_104_20261008.json](../rollouts/receptor_resource_receiving_104_20261008.json).
All eleven known concrete lifecycle corrections are resolved; #104 remains
partial for broader applicable tools/platform/runtime and retrospective owner
review. No scientific suite, real manager, complete benchmark, package
build/upload/promotion or global cleanup is executed. Primary editable installs,
shared environment and seven accepted #82 findings keep their scope. Task-owned
resource retirement is recorded separately in the receipt.

Both clean exact-source/single-worktree clones and all three owned pytest fixture
roots are removed after durable receiving and ownership/activity checks, zero
cleanup failures. Both primary receptor HEAD/status values remain unchanged;
small metadata is retained only until exact central CI and the #104 handoff.
