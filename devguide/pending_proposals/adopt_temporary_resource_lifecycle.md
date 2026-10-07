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
