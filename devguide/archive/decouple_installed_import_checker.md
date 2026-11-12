---
summary: Make loaded-import checking reusable without Conda-template dependencies.
issue: uibcdf/molsyssuite#176
status: resolved
opened: 2026-11-11
closed: 2026-11-11
verification: reproduced
area: [tooling, distribution]
guard: tests/test_installed_imports.py
normative:
blocked_by: []
supersedes: []
---

# Minimal loaded-import checker SDK

**Reported:** PharmacophoreMT #159/#189 and BindingMT #74 report the same SDK
coupling and misleading transitive-import diagnostic in central #176.
**Status:** Central implementation and local qualification complete; the owning
issue retains actual published-source/native verification and consumer handoffs.

## What

At central source `dd73824acd023d32769f089dc612879a0eb22454`, importing
`installed_imports` under Python `-I -S` fails before checking any origins.
The repository layout reports missing `noarch_conda`, masking the original
missing `yaml`; the flat scripts layout reports missing `yaml`. Both exit 1.
Existing full-QA callers correctly admitting PyYAML/Jinja2/Packaging remain valid.

## How

Keep `ContractError` defined in `conda_release_contract.py`, preserving its
identity, inheritance, module name and serialization. Import it directly from
`installed_imports.py`. Load PyYAML only at the workflow-analysis/CLI boundary.
Select repository-package versus flat-script imports explicitly, without
catching an unrelated transitive `ModuleNotFoundError` as a layout failure.
No additional SDK file is needed: the minimal route consists of
`installed_imports.py`, `conda_release_contract.py` and `verify_public_conda.py`.

## Why

Origin checking is independently useful in restricted public-reader processes.
It should not acquire recipe rendering dependencies just to share the existing
exception. Both reported consumers retain their corrected full-QA callers;
this provider improvement does not reopen their scientific acceptance.

## What is measured and what is assumed

Executed baseline: the named Python 3.14.7 interpreter imports the unchanged
checker with `-I -S` in both layouts, with the two failures above. New transport
regressions copy the actual three source files into isolated temporary SDKs,
execute real installed/source imports, verify the exact exception identity and
reject masked transitive dependency errors. Four new test methods pass across
both layouts, real origins, transitive diagnostic preservation, deferred YAML
and exception compatibility. The original source fails eight subtest assertions
in three methods; its pre-existing exception identity remains valid. Original
failures are retained separately from the passing corrected run.

## Alternatives and refuted paths

- Copying QA dependencies into every restricted reader preserves current callers
  but does not make the checker independently reusable.
- A new exception module would change the declared file closure and risk changing
  identity/module/serialization. The current owner can remain authoritative.
- Moving the exception to a consumer or weakening origin checks is unnecessary.

## Scope and exclusions

Central checker imports, shared exception loading, regression guards and SDK
documentation. Preserve source/prefix/namespace/symlink refusals, public result
fields, frozen callers, resource identities and installed publication gates.
No component source/pin change, scientific suite, environment refresh, package
publication, policy release or shared-guide redistribution is part of this fix.

## Acceptance criteria

- Both SDK layouts import and check real origins under `-I -S` with stdlib only.
- Existing exception identity and pickle behavior remain; source/shadow and
  namespace/symlink controls retain their behavior.
- Missing transitive dependencies keep their original identity; actual workflow
  analysis still requires PyYAML and reports its absence truthfully.
- Relevant checker, installed/support, recipe and publication tests plus central
  governance checks pass. Publish the central source and exact hosted evidence,
  then hand adoption to the two reporting owners.

## Local implementation issues

Provider fix: uibcdf/molsyssuite#176. PharmacophoreMT #159/#189 and BindingMT #74
retain their own exact SDK receiving/pin decisions; no new implementation issue
is required for this central correction.

## Dependencies and risks

The existing `ContractError` owner also validates Conda plans/transitions and
workflows. Defer only PyYAML loading; preserve those operations and CLI failure
handling. Existing host dependency conflicts remain separate under #82.

## Provenance

2026-11-11 local; Linux; named `molsyssuite@uibcdf_3.14`, Python 3.14.7.
The initial host reports twelve known `pip check` findings. Published Pytest
Receptor 1.2.3 is digest-verified in a task-local target; primary editables and
the shared environment are preserved. Task-owned temporary resources are retired
after durable evidence is saved; other-session/#82 resources remain untouched.

## Resolution and executed evidence

The checker imports the existing exception directly. Both checker and exception
owner select their actual package/script layout explicitly; transitive missing
dependencies propagate with their original identity. PyYAML loads only when
workflow analysis or the publication CLI is invoked. The exception definition
and every checker function AST are unchanged. No new file enters the SDK closure.

Two publication tests now import their own PyYAML parser instead of relying on
an incidental `contract.yaml` export; their publisher/order assertions remain.
The first broad run records 108 passes and three failures: these two incidental
test dependencies and the published-support guard's correct refusal of modified
uncommitted SDK bytes against provider HEAD. The support guard is unchanged.

A clean temporary committed snapshot
`784b3183cff275218e8b15a7baa7c26cbf063624` then passes **111 tests, zero skips**
across the six selected checker/installed/support/recipe/publication modules with
published Pytest Receptor 1.2.3. All three delivered SDK files and both changed
test files match that tested snapshot byte-for-byte. This includes the actual
published-support shell launch with its source/artifact/attempt binding and
resource retirement. The temporary commit is local qualification, not a public
source or package release. Ruff lint/format, report indexes, offline governance,
whitespace and the real central publication CLI pass independently.

[Normalized baseline, source identities and executed results](../rollouts/installed_import_checker_176_20261111.json)
retain original failures, JUnit digests, the exact published receptor wheel and
known host limitations. The guard module tests the original mechanism with real
isolated imports and continues protecting origin refusal behavior; it is not
merely an addressable unrelated test. The SDK contract is documented in
`devguide/noarch_conda_workflow.md#minimal-loaded-import-checker`.

Exact final central commit, required hosted jobs/steps and scoped consumer notices
are retained in [the owning issue](https://github.com/uibcdf/molsyssuite/issues/176).
PharmacophoreMT and BindingMT own any later SDK pin/receiving change. Existing
full-QA routes remain valid; no new scientific execution, environment refresh or
package publication is inferred.
