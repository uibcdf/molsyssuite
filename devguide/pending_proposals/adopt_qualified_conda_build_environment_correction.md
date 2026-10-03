---
summary: Adopt the qualified Conda build executable correction in shared publishers.
issue: uibcdf/molsyssuite#78
status: partial
opened: 2026-10-03
closed:
verification: measured
area: [governance, packaging, ci]
guard: tests/test_conda_release_contract.py::CondaReleaseContractTests::test_shared_noarch_build_uses_qualified_active_environment_provider
normative:
blocked_by: []
supersedes: []
---

# Conda build executable correction

## What

The shared noarch publisher pins build action
`8a1f203c2cfe51acd63de7452117b4b6e9d609f4` (v2.2.2). Named publisher environments
contain conda-build, while the activation shell function can still invoke the
base manager, which cannot discover that plugin. Ackredit staging run
[37109889925](https://github.com/uibcdf/ackredit/actions/runs/37109889925)
and Pytest Receptor staging run
[37111808160](https://github.com/uibcdf/pytest-receptor/actions/runs/37111808160)
failed before producing an archive. The provider owns the fix as
uibcdf/action-build-and-upload-conda-packages#46, with fixture qualification in
uibcdf/action-build-and-upload-conda-packages#47; MOLI coordination is uibcdf/moli#38.

## How

The provider publishes the qualified correction at immutable
`8da628d9b393e184c3bf3722708b19dcfbf7ef0a`. The actual compilation and conversion
steps use `command conda` to select the executable on the activated environment's
PATH. Build/mambabuild, conversion options, recipe tests, outputs, failure
propagation and upload controls remain covered by the provider's regression
`tests/test_compilation_environment.py`.

The reviewed adoption is a build-action pin change in
`.github/workflows/publish-noarch-conda.yaml`. The central metapackage publisher
uses a separate micromamba profile and is outside this reproduced
named-environment repair. Its two build steps need their own qualification
before an adoption claim. The separate exact-file
upload and promotion pins serve other operations and do not need replacement
merely because the compilation executable changed. Consumers adopt a newly
published immutable shared workflow source; existing policy tags remain immutable.

## Why

This is a reusable provider capability, not a scientific package defect. Both
real consumers reproduce the same executable boundary. A local orchestration
workaround in uibcdf/pytest-receptor#34 should be retired after the qualified
shared route is adopted and actually builds the component's exact candidate.
Publication access, installed scientific gates and public delivery remain local.

## Measured provider evidence — 2026-10-03

Native [37115921728](https://github.com/uibcdf/action-build-and-upload-conda-packages/actions/runs/37115921728)
passes four real build cells at the exact correction commit: Linux named and
base, macOS ARM named and Windows named. Every cell executes the recipe tests,
archive inspection and retained upload-free producer evidence. Native
[37115921702](https://github.com/uibcdf/action-build-and-upload-conda-packages/actions/runs/37115921702)
passes unit tests plus Linux/Windows multi-variant build and installed-import
checks, with explicit installed interpreter, prefix and module-origin assertions.
The production diff changes the two executable invocations. These are provider
qualification receipts; they are not shared-caller or scientific artifact receipts.

## Scope and decisions

The user requested review of #78 after the Python-policy rollout. Review is
complete and the immutable provider source is qualified for adoption. The
existing uibcdf/molsyssuite#81 change is merged directly into published main at
`2a2a459cc3795bb92766fffa0fe28f4d80f01ad4`, with a regression protecting the
selected qualified build source. Hosted governance 37125099269 passes. Caller
rollout and real shared-route integration are still pending.
No registry upload, promotion, component release or scientific test execution
has been performed by this review. The existing publisher's administrative/build
Python 3.13 is a tool runtime and is separate from the 3.14 routine package-test
baseline; no unsupported scientific platform claim is inferred from it.

## Acceptance criteria

- Adopt the reviewed immutable build-action source in applicable shared callers.
- Protect the selected compilation pin and existing publication controls with
  the maintained workflow guards.
- Verify the actual shared named-environment route with recipe tests and
  inspected archives, without public publication during qualification.
- Record component caller adoption and their owner issues; retain their full
  installed/public gates before closing their delivery work.
- Retire the temporary Pytest Receptor orchestration only after the shared route
  replaces it and passes for the selected exact candidate.

## Maintainer work order — 2026-10-03

After the current policy rollout, attend uibcdf/molsyssuite#78, then resolve
uibcdf/molsyssuite#81 as explicitly requested by the maintainer. The latter is
the prepared shared noarch build-reference change; review its exact source and
checks before adoption. Coordination review does not close #78 before its
publication/adoption handoff is actually complete.

## Consumer handoff

The maintainer explicitly requested notifying affected components to review and
adopt the correction. Notify their existing publication owner issues with the
published full shared-workflow commit, old and new references, provider receipts,
local validation steps and an actual exact-candidate staging requirement. A
notification is not an adoption receipt. No heavy component suite is triggered
by this coordination step.

The authoritative observed publisher/consumer list is now
`devguide/rollouts/conda_publishers.json`, registered in `suite.toml` and queryable
through `python_distribution_status.py --publisher-kind shared-noarch`.
uibcdf/molsyssuite#79 owns the maintained inventory and broader notice guidance.
The table below retains this particular correction's handoff checkpoint.

| Consumer | Publication owner | Current shared source |
| --- | --- | --- |
| Ackredit | uibcdf/ackredit#22 | `4010595a2ed756b20114730c6a91561a16d7be2f` |
| Pytest Receptor | uibcdf/pytest-receptor#32 | `5a90853d4ac147f7b831cfc37f9f5defd87c190a` |
| TopoMT | uibcdf/topomt#78 | `42e4de425871c125ef058842075c39e50fc6ac64` |
| PharmacophoreMT | uibcdf/pharmacophoremt#10 | `42e4de425871c125ef058842075c39e50fc6ac64` |
| ElastNetMT | uibcdf/elastnetmt#18 | `42e4de425871c125ef058842075c39e50fc6ac64` |
| LinDelINT | uibcdf/lindelint#13 | `42e4de425871c125ef058842075c39e50fc6ac64` |

Pytest Receptor uibcdf/pytest-receptor#34 was withdrawn on 2026-10-03: the local
base-plugin workaround was examined but never adopted. Its main retains the
thin shared caller. There is no deployed fork to retire.

## Integration checks — 2026-10-03

All six observed shared consumers have been notified in their existing owner
issues. The implementation and notice handoff are complete; member review,
caller adoption and executed exact-candidate staging remain pending.

- [uibcdf/ackredit#22](https://github.com/uibcdf/ackredit/issues/22#issuecomment-5969542148): notice published with the immutable shared source and component-owned verification requirements.
- [uibcdf/pytest-receptor#32](https://github.com/uibcdf/pytest-receptor/issues/32#issuecomment-5969546951): notice published with the immutable shared source and component-owned verification requirements.
- [uibcdf/topomt#78](https://github.com/uibcdf/topomt/issues/78#issuecomment-5969551229): notice published with the immutable shared source and component-owned verification requirements.
- [uibcdf/pharmacophoremt#10](https://github.com/uibcdf/pharmacophoremt/issues/10#issuecomment-5969551629): notice published with the immutable shared source and component-owned verification requirements.
- [uibcdf/elastnetmt#18](https://github.com/uibcdf/elastnetmt/issues/18#issuecomment-5969552736): notice published with the immutable shared source and component-owned verification requirements.
- [uibcdf/lindelint#13](https://github.com/uibcdf/lindelint/issues/13#issuecomment-5969553119): notice published with the immutable shared source and component-owned verification requirements.

uibcdf/molsyssuite#81 is merged by the direct published integration at
`2a2a459cc3795bb92766fffa0fe28f4d80f01ad4`. Native governance
[37125099269](https://github.com/uibcdf/molsyssuite/actions/runs/37125099269)
passes its 273 central tests on the configured Python 3.14 lane. The later
inventory addition passes 275 local tests, without component scientific suites.

The merged source passes the offline governance guard and 273 central unittest
tests on local Python 3.13.15. The added regression rejects the previously
failing provider pin and preserves upload-free single-file building and the
separately qualified exact-upload provider pins. Hosted governance uses Python
3.14 and will qualify the published integration.

The installed actionlint reports the existing `job.workflow_sha` context as
unknown; that checkout expression predates this change and executed successfully
in the affected source preflights. No workflow-linter success is claimed.

## Local implementation issues

uibcdf/ackredit#22, uibcdf/ackredit#75 and uibcdf/ackredit#80 own its artifact and
public delivery. uibcdf/pytest-receptor#32 and uibcdf/pytest-receptor#34 own its
release and temporary workaround. uibcdf/molsyssuite#80 retains the second
consumer reproduction. Other publisher profiles require individual inspection.

## Provenance

Read provider #46, the exact production diff and native run/job/step JSON on
2026-10-03. Source and hosted evidence are pinned to the full commit above.
