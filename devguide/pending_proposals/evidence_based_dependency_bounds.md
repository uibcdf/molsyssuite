---
summary: Prefer justified dependency bounds with separate reproducible and latest-public evidence.
issue: uibcdf/molsyssuite#137
status: active
opened: 2026-10-30
closed:
verification: inspected
area: [governance, dependencies, compatibility]
guard:
normative:
blocked_by: []
supersedes: []
---

# Runtime bounds and dependency qualification

**Reported:** Maintainer-requested independent evaluation following Recorda #35.
**Status:** Reviewable recommendation; no suite policy or member bounds adopted.

## What

Avoid excluding every next provider minor merely because it has not been tested.
Permit runtime floors without a speculative ceiling when the consumed contract
supports that choice. Retain justified API/ABI, Python, scientific, platform and
optional-provider restrictions. Separate the package's permitted installation
range from the exact environments actually qualified.

## How

The existing distribution contract already accepts declared floors with or
without ceilings. Its preflight preserves whatever reviewed constraints the
owner declares in metadata, recipes, environments and pinned source routes.
Neither `python_distribution_policy.md` nor `ci_dependency_resolution.md`
requires an automatic next-minor ceiling. A checker relaxation or new publisher
is therefore not justified by this evaluation.

Proposed accepted text for the dependency-contract section, after human decision:

> Declare the minimum provider version that supplies the consumed capability.
> Do not add an upper bound solely because a future minor is untested. Retain or
> add bounds/exclusions for a concrete incompatible API/ABI or scientific/runtime
> contract, with owning evidence and a reassessment trigger. An upstream documented
> compatibility boundary can justify a restriction before a local failure occurs.
> Metadata permits installation; only recorded exact-version tests establish
> qualified compatibility. Unknown future behavior is not certified.

Adoption by each owner would include:

1. Identify the consumed contract and API floor. Inspect meaningful lowest-version
   coverage or record its explicit owner/limit; do not infer a floor from a solver.
2. Preserve exact source/version/build/digest and dependency-closure evidence for
   release qualification and historical reproductions. Test constrained oldest
   supported inputs separately from a freely resolved newer closure.
3. For a widened/minimum-only range, maintain a scheduled/manual latest-public
   compatibility route using the consumer's relevant installed contract tests,
   real provider origins and `pip check`/equivalent. Reuse existing cadence where
   appropriate. Start new shared automation as an informative pilot, not a new
   required full scientific suite on each internal push. Record an owned bounded
   adoption gap when the route cannot yet run; no unexecuted compatibility claim.
4. Report an observed provider/consumer failure in the owning issue with exact
   selected versions and reproduction. Keep the failure visible; fix the owning
   contract or add an evidenced bound. Do not auto-release a consumer, silently
   downgrade the report, or mechanically rewrite all manifests.

All current required PR/admission/release gates and exact-byte publication
controls remain due. Metadata changes require component review and applicable
tests; existing qualified public files and tags remain immutable. No general
environment refresh, change to optionality or automatic consumer pin upgrade is
part of adoption. MolI #76 independently owns the platform decision.

## Why

Recorda 0.3.2's ceilings excluded ArgDigest 0.17 / SMonitor 0.22 even though its
owner's subsequent receiving found compatible runtime behavior. Public 0.3.3
now uses minimum-only requirements. Central #142 independently verifies that
release's native gates, exact public bytes, all fifteen runtime files and
declared dependencies. This is evidence for that consumer/cohort, not proof
that all scientific or native dependencies tolerate unknown versions.

The shared caller's old Recorda/Praxis sources still have five obsolete ceilings;
their owner fixes are complete, but #135 retains actual refresh/closure receiving.
Do not confuse this stale local state with a failure of public 0.3.3.

## What is measured and what is assumed

- Existing normative dependency/CI rules were inspected; they preserve declared
  constraints and do not require automatic next-minor caps.
- #130/#142 receive two exact Recorda files; no new compatibility suite was run.
- Python support remains >=3.11,<3.15. It is independent of this proposal.
- PyUnitWizard 0.29.0's baseline/public Pint closure and optional OpenFF profile
  have distinct bounds. OpenFF's Pint <0.26 and Python 3.12–3.14 profile are
  retained; this proposal does not broaden that scientific contract.
- Native ABI bounds and Conda run exports are not speculative Python caps.
- A latest-public lane detects only cases it executes. It cannot prove all
  versions, combinations, scientific definitions or future releases.

## Alternatives and refuted paths

| Route | Benefit | Cost / limitation |
| --- | --- | --- |
| Automatic ceiling at every next minor | Prevents selection beyond an owner's reviewed band | Repeated metadata-only releases and solver conflicts even for compatible providers; stale installations remain excluded. |
| Remove every upper bound | Maximum resolver freedom | Can violate documented ABI, optional-provider and scientific contracts; rejected. |
| Justified bounds plus separate exact/latest evidence (recommended) | Preserves concrete constraints and reproducibility while allowing compatible updates | Needs explicit owner contract review and maintained latest-public diagnostics; no blanket future guarantee. |

Pre-1.0 provider version numbers alone do not establish a compatibility contract.
A concrete documented unstable boundary can justify narrowing; neither universal
trust nor universal next-minor exclusion follows from the version prefix.

## Scope and exclusions

Proposed common engineering criterion for registered Python members, with
component-specific implementation and justified conditions. No mandatory new
provider floor, optional engine, CI platform, publication or stability deadline.
No edit to components, immutable policy tags, canonical guide or starter is made
until the criterion is accepted. Public source compatibility and native ABI
rules retain their independent owners.

## Acceptance criteria

- Human decision on the common criterion and staged/informative CI adoption.
- If accepted, reconcile normative distribution/CI wording, common guide and
  official starter, and distribute only through the registered guide route.
- Use existing owner reviews for actual bounds/monitoring adoption; preserve
  special profiles and exact candidate/public artifact evidence.

## Local implementation issues

Recorda #35/#37 are already complete under MolI ownership. No member bounds
change is commissioned by this proposal. Central receiving is #142; caller
refresh is #135. MolI-wide evaluation remains uibcdf/moli#76.

## Dependencies and risks

Latest-public observation must not replace frozen release qualification, make
optional dependencies mandatory, or activate deferred scientific suites. A
permissive range can select a breaking future release; the route must make
failures actionable rather than claiming a future guarantee.

## Provenance and primary references

2026-10-30; source inspection and Recorda/PyUnitWizard release receiving in the
named Python 3.14.7 environment. External references were read only; no external
issue/PR was created:

- [PyPA: package requirements versus complete environment pins](https://packaging.python.org/en/latest/discussions/install-requires-vs-requirements/)
  distinguishes minimal requirements/known incompatible versions from exact
  environment reproduction. It does not prescribe every suite CI choice here.
- [Conda-forge: ABI pinning and run exports](https://conda-forge.org/docs/maintainer/pinning_deps/)
  explains concrete compiled compatibility constraints; those are preserved.

The recommendation is MolSysSuite's proposed decision inferred from its own
requirements and observed cohorts, not a claim that those references mandate it.
