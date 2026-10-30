---
summary: Prefer justified dependency bounds with separate reproducible and latest-public evidence.
issue: uibcdf/molsyssuite#137
status: partial
opened: 2026-10-30
closed:
verification: inspected
area: [governance, dependencies, compatibility]
guard:
normative: devguide/python_distribution_policy.md
blocked_by: []
supersedes: []
---

# Runtime bounds and dependency qualification

**Reported:** Maintainer-requested independent evaluation following Recorda #35.
**Status:** General >=X rule accepted by the principal maintainer; normative publication, guide delivery and owner receiving are in progress.

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

The principal maintainer accepted the general `>=X` rule on 2026-10-30, with
component-specific restrictions only for justified incompatibilities. The
authoritative accepted wording is now in
[the distribution policy](../python_distribution_policy.md#runtime-dependency-version-bounds).
The following was the reviewed recommendation preceding that decision:

> Declare the minimum provider version that supplies the consumed capability.
> Do not add an upper bound solely because a future minor is untested. Retain or
> add bounds/exclusions for a concrete incompatible API/ABI or scientific/runtime
> contract, with owning evidence and a reassessment trigger. An upstream documented
> compatibility boundary can justify a restriction before a local failure occurs.
> Metadata permits installation; only recorded exact-version tests establish
> qualified compatibility. Unknown future behavior is not certified.

Owner adoption follows the accepted normative scope. The evaluation identified
the following controls; new shared automation begins informatively rather than
becoming an additional universal gate:

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

Accepted common engineering criterion for registered Python members, with
component-specific implementation and justified conditions. No mandatory new
provider floor, optional engine, CI platform, publication or stability deadline.
Canonical guide/starter and current registry now carry the accepted criterion;
existing immutable policy tags are not moved. Actual component metadata changes
remain owner-reviewed. Public source compatibility and native ABI
rules retain their independent owners.

## Acceptance criteria

- General >=X criterion accepted; preserve justified exceptions and current CI cadence.
- Reconcile normative distribution wording, common guide and
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


## Accepted implementation — 2026-10-30

The human decision requires `provider>=X` as the general runtime rule, with
component-specific upper bounds/exclusions only for justified incompatibility.
The canonical guide, distribution policy, starter route/README and current
registry record it. Existing validators already accept that range; no new
publisher, weakened checker or mandatory per-push full suite is introduced.
Source publication precedes official registered guide distribution. Explicit
member bound reviews and genuine incompatibilities remain distinct from guide
receipt. This coordination stays partial until owning receiving is accounted for.


Local checks for accepted source: existing instruction, generation and official
synchronizer tests pass **33 tests** in Python 3.14.7, using the named shared
environment and `--receptor=llm`. Regenerated indexes and offline governance pass.
These checks validate delivery/instruction machinery, not consumer compatibility.


## Common delivery and owner routes — 2026-10-30

Canonical source `3feec0e6534200820a53fd4b131609ce38b653f9` is published.
All seventeen registered guide-only commits are published; committed-input
byte/routing checks pass. The official starter copies the same accepted guide,
with its local README action; immutable automated policy tags stay unchanged.
[Delivery and inspected declaration inventory](../rollouts/runtime_version_rule_137_20261030.json)
keeps public source/input identities separate from private member evidence.

The inspected metadata identifies required declarations without an inclusive
floor in eight public components; a current public runtime ceiling in MolSysMT
also needs owner classification. Inspection does not prove a cap is unjustified
or establish a safe API floor. Optional runtime features and exact tooling pins
retain their distinct review scopes.

New closable owner tasks cover previously completed review contexts:
PyUnitWizard #134, MolSysMT #524, MolSysViewer #285 and LinDelINT #18.
Existing TopoMT #78, PharmacophoreMT #10, ElastNetMT #18 and DockingMT #47
carry their applicable floor reviews; private OpenCASTp #2 retains its actual
restriction and private evidence review. Other existing owner contexts received
the rule and preserve prior valid floor/compatibility evidence without mechanical
rewrites. The non-Python MolSys-AI umbrella receives the common guide but has no
Python runtime-metadata requirement. All seventeen destinations are accounted for.

MolI #76 received the accepted criterion/rationale; its direct-component rollout
remains independently owned. No component metadata, scientific implementation,
public artifact or release decision is changed by this central delivery. Keep
#137 partial for actual owner dispositions/receiving; policy acceptance and
instruction distribution are complete, not a remaining decision.
