---
summary: Shared devguide guard semantics are not verifiable across components.
issue: uibcdf/molsyssuite#26
status: active
opened: 2026-09-19
closed:
severity: medium
verification: reproduced
area: [governance, testing, automation]
guard:
normative:
blocked_by: []
supersedes: []
---

# Shared devguide guard semantics are not verifiable across components

**Reported:** 2026-09-19, after MolSysMT issue `uibcdf/molsysmt#197` showed that
its validator accepts an existing test file followed by a nonexistent pytest node.
The subsequent wave-1 audit found incompatible weaker interpretations in every
other stabilized member.
**Status:** Active. The common contract and central negative cases are being implemented;
the six-member rollout remains open.

## What

Define one honest suite-wide meaning for the `guard` field used to resolve a
developer-guide defect report. A guard must identify a runnable regression target
in the owning repository. Automation must verify that the target is mechanically
addressable, while the policy must state plainly that the causal relationship
between the target and the reported defect remains a reviewer-owned judgement.

The current shared protocol says that a resolved defect names "a test or automated
check" and member guides commonly call it "the test that fails if the defect
returns." No common rule defines how that target is addressed, what a validator
actually proves, or how non-pytest guards participate.

## How

Adopt a layered contract rather than pretending one syntactic check proves intent.

### 1. Common semantic contract

`guard` is a stable, locally runnable target that is expected to fail when the
reported defect is reintroduced. It carries two distinct claims:

1. **Addressability**, mechanically checked: the declared runner understands the
   selector and can resolve it to one or more tests or checks.
2. **Relevance**, reviewed: the selected assertion exercises the failure mechanism
   described by the report.

Passing addressability must never be described as automated proof of relevance.
A validator cannot infer causal protection from a path or test name.

### 2. Python profile

For pytest-based repositories, retain the existing compact scalar syntax and give
it an exact meaning:

- `tests/path/test_module.py` selects the complete module;
- `tests/path/test_module.py::test_name` selects one function;
- `tests/path/test_module.py::TestClass::test_name` selects one method;
- a parametrized suffix is permitted only when the repository can resolve that
  collected node reliably.

The local closure check must reject a missing file and a missing node. Whether it
uses targeted pytest collection, a cached collection inventory, or a sound static
index is an implementation choice; checking only the substring before `::` is not
conforming. A whole-file guard remains legitimate when the module collectively
protects one cross-cutting contract.

### 3. Non-pytest profiles

Rust, workflow, documentation, and repository-conformance guards need a documented
local selector understood by their runner. Do not introduce arbitrary shell command
strings into front matter: they are unsafe, non-portable, and difficult to validate.
If scalar `guard` becomes ambiguous across profiles, add a small structured form with
a runner kind and target only after inventorying real cases. Do not design a universal
schema from hypothetical runners.

### 4. Relevance evidence at closure

The resolving report explains why the named guard would fail. Prefer one of these
forms of evidence, in descending strength:

- the reproducer failed before the fix and became the regression test;
- a controlled revert or mutation makes the guard fail;
- an existing test contains the assertion over the repaired failure mechanism;
- when a destructive or impractical mutation is inappropriate, the resolution
  records the reviewer rationale explicitly.

This evidence belongs in the report's resolution, not in a free-text front-matter
field that a generator can satisfy with boilerplate. High-risk defects may adopt a
stricter mutation requirement through a profile rule; the universal policy should
not claim that every causal relationship is machine-provable.

### 5. Conformance and rollout

Add shared negative cases for:

- missing guard target;
- existing file with a missing pytest node;
- unsupported selector syntax;
- a resolved defect with neither `guard` nor `normative`.

Keep one explicit counterexample showing the automation boundary: an existing but
unrelated node is mechanically addressable and therefore requires review, not a
fabricated semantic validator. The central conformance gate should verify that each
applicable member rejects the common negative cases through its documented local
command.

Adopt the rule prospectively. Existing archived records are historical evidence and
must not be rewritten en masse. File-level guards remain valid runnable targets.
Repositories should correct stale or fictitious historical selectors when encountered,
and a separate audit may be opened if evidence shows material archive debt.

## Why

The reporting lifecycle is a shared policy already adopted by the six wave-1
repositories. A report marked `resolved` is used as durable evidence that a defect
cannot silently return. Today the same `guard` field has different enforceable meanings,
and several implementations accept values that name no runnable test at all.

This is an integrity defect in release governance, not a product-runtime defect, so the
severity is medium. It matters more as machine-generated contributions increase: a
generator will reliably satisfy the exact shape a validator checks, including an empty
shape that never protects the reported behavior.

## What is measured and what is assumed

**Inspected on 2026-09-19:**

| Repository | Current enforceable meaning |
| --- | --- |
| MolSysSuite | resolved requires a nonempty `guard` or `normative`; neither target is resolved |
| SMonitor | `ROOT / guard` must exist, so a pytest `::node` selector is treated as a literal path |
| ArgDigest | resolved requires a nonempty `guard` or `normative`; no target resolution |
| DepDigest | resolved requires a nonempty `guard` or `normative`; no target resolution |
| PyUnitWizard | resolved requires a nonempty `guard` or `normative`; no target resolution |
| MolSysMT | the substring before the first `::` must name an existing file in a test tree; the node is ignored |
| MolSysViewer | the offline reporting tests inspect open queues; resolved archive guards are not validated |

MolSysMT's validator test currently accepts
`tests/basic/test_get_form_battery.py::test_routes`; no `test_routes` node exists in
that file. This is an executable counterexample, not an inference from source alone.

The audit read the current local `main` checkouts after running
`python devtools/scripts/suite_status.py`. MolSysMT, MolSysViewer, SMonitor, ArgDigest,
and DepDigest were current and clean. PyUnitWizard was one commit behind its fetched
remote; the inspected behavior is therefore a local snapshot and must be reconfirmed
before its implementation issue is filed.

**Assumed:** infrastructure and incubating repositories may carry the same field, but
they were not used to establish this wave-1 defect and do not define its first rollout.

**Not measured:** whether any archived report names an unrelated guard. Mechanical
weakness does not prove historical misuse.

**Reproduced on 2026-09-20:** central test-first cases failed before implementation for
a missing file, an existing file with a missing node, and an unsupported parameterized
selector. The accepted static resolver now distinguishes those cases while deliberately
accepting an addressable unrelated node as a reviewer-owned relevance question.

## Alternatives and refuted paths

- **Treat file existence as the whole contract.** Rejected: it contradicts the shared
  statement that the guard is runnable regression evidence and permits fictitious nodes.
- **Claim automation can prove relevance.** Rejected: an unrelated existing test is
  indistinguishable from a relevant one by its address alone.
- **Require every guard to name one pytest function.** Rejected: a complete module may
  protect a cross-cutting contract, and not every member or guard uses pytest.
- **Add a required `guard_reason` sentence and validate that it is nonempty.** Rejected:
  this checks prose shape rather than intent and is trivially satisfied by boilerplate.
- **Store arbitrary commands in front matter.** Rejected on security, portability, and
  reproducibility grounds.
- **Run full pytest collection once per archived report.** Rejected as a default design:
  it multiplies import and optional-dependency cost and can turn an offline metadata
  validator into a slow environment probe. Targeted or cached collection remains viable.
- **Rewrite every historical report during adoption.** Rejected: archives preserve what
  was known at closure. Prospective enforcement plus evidence-led correction is safer.

## Scope and exclusions

The common semantic rule applies to every repository governed by the shared reporting
lifecycle. The first implementation rollout covers the six stabilization wave-1
members: SMonitor, ArgDigest, DepDigest, PyUnitWizard, MolSysMT, and MolSysViewer.

Covered: guard selector semantics, mechanical addressability, reviewer-owned relevance,
pytest profile behavior, non-pytest extension rules, closure evidence, conformance
negative cases, and migration policy.

Excluded: re-auditing the semantic relevance of every historical guard, optimizing test
runtime, changing the meaning of `normative`, or opening implementation issues in members
before their concrete required change is confirmed against the accepted policy.

## Acceptance criteria

- `devguide/reporting_protocol.md` distinguishes guard addressability from relevance and
  states what automation and review each establish.
- The Python profile defines runnable file, function, class-method, and supported
  parametrized selectors without requiring one function for every defect.
- Non-pytest guards have an extension rule that does not execute arbitrary front-matter
  shell commands.
- Shared conformance cases reject a missing target, missing pytest node, unsupported
  selector, and resolved report with neither guard nor normative.
- The policy contains an explicit counterexample proving that semantic relevance remains
  reviewer-owned.
- The closure record requires evidence explaining why the guard protects the reported
  failure mechanism, with mutation or pre-fix failure preferred where practical.
- Historical archives are not broken merely for using a file-level guard; prospective
  applicability and correction policy are explicit.
- A rollout record shows every wave-1 member adopted, blocked by a stable local issue, or
  covered by a documented exception.
- The accepted rule is summarized in `MOLSYSSUITE_GUIDE.md` and registered as shared
  policy if it becomes independently versioned.

The future normative record is `devguide/reporting_protocol.md`. Central conformance
tests and member-local validator tests will be the executable guards.

## Local implementation issues

- `uibcdf/molsysmt#197` — known local implementation gap and originating evidence;
  it should implement the accepted central contract rather than define shared policy.

Do not open the other five local issues automatically. Reconfirm each checkout against
the accepted selector contract and file only the concrete implementation work that
remains.

## Dependencies and risks

Pytest collection imports test modules and optional dependencies; a mechanically exact
implementation can become too expensive or environment-sensitive if it collects the
entire suite for every report. Static indexing can be fast but must not claim support
for dynamic or parametrized nodes it cannot resolve. The accepted profile must choose an
honest boundary and test its failure modes.

Stricter validation can expose real historical drift. Treat those findings as evidence
for explicit follow-up rather than weakening the new rule or silently rewriting the
archive.

## Provenance

Inspected on Linux, 2026-09-19, from the six stabilization wave-1 checkouts registered
in `suite.toml`. Central repository at `cee7346`; MolSysMT originating report at
`f4e598c1a`. The suite-status result is recorded in this report's measurement section.
