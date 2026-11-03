---
summary: Invalidate CI pilot selection review when an unbound root pytest configuration appears.
issue: uibcdf/molsyssuite#160
status: resolved
opened: 2026-11-02
closed: 2026-11-02
severity: medium
verification: reproduced
area: [ci, governance, tooling]
guard: tests/test_ci_pilot.py::CIPilotTests::test_unbound_root_pytest_configs_invalidate_selection_review
normative:
blocked_by: []
supersedes: []
---

# Newly discovered pytest configuration must invalidate stale selection review

**Reported:** 2026-11-02 while preparing the separate #39 informational cohort proposal.
**Status:** Reproduced and corrected in the central source reader; the original
three-member cohort remains active. Cohort expansion still needs its own decision.

## What

Adding a new `pytest.ini` with `addopts = -k only_this_subset` to the reviewed
GH Run Receptor file projection leaves all original bound hashes unchanged.
Before the fix, `inspect_pilot` still returns current inputs, all eleven targets
configured and all full-selection matches true. No component source or tests
are changed or executed in that source-only reproducer.

A separate managed dummy project proves the actual failure mechanism: the bound
project configuration runs two trivial tests; a new `pytest.ini` selects one and
deselects the other, while pytest still exits zero. A passing run does not make
the unchanged full-selection review valid.

## How

The reader originally checked only paths already named by the profile. It now
also checks for present root pytest configuration names: `pytest.toml`,
`.pytest.toml`, `pytest.ini`, `.pytest.ini`, `pyproject.toml`, `tox.ini` and
`setup.cfg`. A present unbound file adds an explicit mismatching input with a
reason. Its contents are not read or executed. Recognized names are inspected
from the installed primary pytest configuration reader; discovery is conservative
across the supported pytest 8/9 formats and does not decide which file wins.

That mismatch invalidates lane and scenario selection review through the existing
drift path. The owner must review the real selection and explicitly bind the file;
an actual subset uses the reviewed smoke level/owning issue rather than silently
restoring full. Existing bound files still fail review on content drift or absence.

## Why

Alternative pytest configuration can override the previously bound project
selection. Hashes of known files alone cannot detect a new precedence input.
The informational reader must display that uncertainty before it can be used
to discuss broader enforcement. This changes no required member CI check.

## What is measured and what is assumed

Two new test methods fail before the fix, including six configuration-name
subtests and the real two-test fixture. After the fix, all **43** selected central
pilot/event/inventory/policy tests pass in `molsyssuite@uibcdf_3.14`, Python 3.14.7.
The source reproducer becomes unknown for every affected target/scenario.
Explicit reviewed smoke binding, later content change and file removal also have
regressions. The dummy subprocess disables third-party plugin autoload and caller
pytest/PYTHONPATH overrides; it runs no molecular/component tests.

The actual CLI still accepts all fifteen unchanged current cohort inputs.
The separately proposed six-member catalogue still matches its thirty-three
reviewed inputs; this does not adopt it. Changed-file Ruff lint/format passes.
[Normalized before/after, source, test and notice receipt](../rollouts/ci_pilot_config_invalidation_160_20261102.json).

## Alternatives and refuted paths

- Trust unchanged listed hashes: disproved by the source and actual pytest cases.
- Parse or execute unbound configuration automatically: unnecessary; discovery
  can safely invalidate review until semantic inspection and explicit binding.
- Automatically relabel any new file as full/smoke: would invent a reviewed decision.
- Require a new universal workflow or full suite: unrelated to this source-reader bug.

## Scope and exclusions

Root pytest configuration discovery in the shared central pilot. This is not
general shell interpretation, ancestor-config discovery, a nested/dynamic-hook
manifest or runtime/environment qualification. Those bounded inspection limits
remain explicit; no universal selection or execution proof is claimed.
Existing cohort, registry adoption, workflows, mandatory checks, scientific
deferrals, environments, packages and skip-debt watermarks remain unchanged.

## Acceptance criteria

The recognized root names invalidate unbound review; explicit reviewed bindings
retain level and hash/missing-file controls; real pytest demonstrates the selection
hazard; unchanged current sources remain compatible; no component execution follows.
All criteria pass. The registered guard fails before the fix because every new
unbound root name incorrectly preserves current/full review; it passes afterwards.

## Local implementation issues

This implementation belongs wholly to MolSysSuite. Existing DepDigest #21,
GH Run Receptor #52 and Ackredit #74 receive interpretation notices only; no
component migration or fresh acceptance is required. #39 owns the distinct
broader cohort/enforcement decisions.

## Dependencies and risks

A neutral or ignored root config also conservatively needs review. Semantic
inspection may bind it without changing the reviewed level. Root input names
are bounded and inspect no unbound content. No new runtime dependency is added.

## Provenance

2026-11-02, central Linux/Python 3.14.7 environment. Exact reviewed sources,
installed pytest/Ruff versions, commands and before/after outcomes are in the
receipt. Managed fixture resources self-retire; task-owned source projections,
private status and duplicate logs retire after exact delivery. Primary human
work and the shared prefix are preserved.
