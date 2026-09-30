---
summary: Require modular reusable tools across MolSysSuite components
issue: uibcdf/molsyssuite#61
status: active
opened: 2026-09-30
closed:
verification: inspected
area: [governance, architecture]
guard:
normative:
blocked_by: []
supersedes: []
---

# Require modular reusable tools across MolSysSuite components

**Reported:** 2026-09-30, from the maintainer's modular-design decision in
`uibcdf/molsysmt#261` and request to make it explicit across MolSysSuite.
**Status:** Active proposal; the central rule and coordinated adoption remain
pending. Preparing this record does not declare every member compliant.

## What

Establish a shared design rule: a reusable capability identified while
implementing a feature becomes a documented general-purpose tool in its
owning module or component, available to other workflows through a supported
boundary. Existing tools are reused or extended before adding another
implementation. Every registered component's root AGENTS.md explicitly
requires this practice and routes contributors to the canonical policy.

## How

### Proposed engineering rule

1. Before implementing a feature, inspect existing tools in the component
   and relevant providers. Identify the scientific operation, its inputs,
   outputs, units, index spaces, and ownership.
2. A missing operation with meaningful standalone use is designed as a
   general tool in the appropriate domain, even when the first need arises
   in one feature. Supply its own contract, documentation, and tests. The
   consumer calls that tool rather than embedding a duplicate algorithm.
3. When ownership belongs to a sibling, report the need in that provider and
   link the consumer requirement under the existing feedback protocol.
   Preserve dependency direction and optional-dependency boundaries. A
   reusable operation does not belong in a viewer merely because a rendering
   feature first revealed the need.
4. Keep feature-specific scientific criteria and orchestration in the
   consumer. Internal implementation helpers may remain private behind a
   supported general tool; export only operations with a meaningful user
   contract. Do not turn every helper into a public API or create a new
   package solely to satisfy this rule.
5. Reuse compiled primitives and implement further heavy work in the
   provider's supported backend when warranted. Rust is an available choice
   in MolSysMT, not a mandated language for every suite member. Measure
   end-to-end time and allocation, preserve scientific behavior, and keep
   public validation and provenance at clear boundaries.
6. A temporary duplication or local workaround names its provider issue,
   reason, responsible owner, expiry/review date, and removal condition.
   Apply the existing tracked-exception policy; do not silently fork tools.

This rule is prospective. An existing duplication found during relevant work
is reported to its owner; adopting the rule does not require an unbounded
rewrite of every historical module before another feature can proceed.

### Concrete motivating examples

| Need discovered in a consumer | General owner and contract |
| --- | --- |
| Interaction detection needs hydrophobic atom typing | MolSysMT physchem, with a named typing definition. Existing residue hydrophobicity scales do not themselves provide atom typing. |
| Ring or charged-group geometry needs a compact periodic participant | MolSysMT pbc. Reuse existing covalent reconstruction and define any missing compactness/image contract there. |
| Pi-pi needs a plane and a planarity measurement | MolSysMT structure, reusing geometric principal axes and defining degenerate-input behavior. |
| A viewer or docking pipeline needs a generic molecular analysis | The molecular-analysis provider; the consumer owns presentation or task-specific interpretation. |

The reusable tool and its consumer must agree on scientific meaning and
evidence. For example, compacting a component does not automatically encode
its internal lattice shifts in a downstream interaction result. A reusable
tool must expose the information its supported consumers need, or state its
limit explicitly.

### Proposed root AGENTS.md instruction

The following is a draft for adaptation to local documentation conventions,
with the same semantics in every registered member:

> Before adding a feature, inspect existing general tools and identify the
> owning domain or MolSysSuite provider for each required capability. When
> an operation is useful independently or by other workflows, implement or
> extend it as a documented general-purpose tool in that owner, with its own
> contract and tests; have the feature call it. Keep feature-specific criteria
> in the consumer and internal helpers behind supported boundaries. Report
> missing sibling capabilities to the provider and link the consumer need.
> Follow the modular-tool policy routed through MOLSYSSUITE_GUIDE.md, including
> its dependency, performance, and tracked-exception requirements.

Keep the complete rule in one normative central document. The synchronized
guide carries the concise instruction and link; member AGENTS.md files
contain an explicit instruction plus that canonical route, not independently
maintained copies of a long policy.

### Adoption plan

1. Review and accept the canonical policy, applicability to all registered
   members, and exception mechanism. Decide its registry/publication route
   through the existing policy machinery.
2. Update the canonical component-facing guide, the central AGENTS.md, and
   the new-component starter kit. Distribute synchronized guides through
   the existing guide synchronization tool.
3. Generate a rollout inventory from suite.toml. Inspect each member's
   instructions, add the local routing requirement, and record exact-commit
   adoption evidence. Component edits preserve local rules and working state.
4. Check newly generated repositories and existing members for discoverable
   routing. These mechanical checks prove instructions are delivered, not
   that implementations actually follow modular architecture.
5. Review concrete provider/consumer examples for the intent of the policy:
   the provider exposes a usable tool, the consumer really uses it, and
   scientific/domain responsibilities remain correctly located. Link local
   implementation issues when actual code changes are needed.
6. Close with the normative policy, adopted instruction/guide evidence for
   all applicable members, and documented outstanding exceptions.

## Why

MolSysSuite aims to provide useful molecular building blocks across clients.
Embedding general chemical, structural, or PBC operations inside individual
detectors obscures ownership, duplicates scientific definitions and tests,
and prevents other pipelines from using those operations conveniently.

The existing [ownership contract](../repository_contract.md),
[feedback policy](../cross_component_feedback.md), and
[starter kit](../new_component_starter_kit.md) already prevent silent sibling
forks and route common needs to providers. They do not yet explicitly require
this within-component general-tool design or its delivery in every member's
AGENTS.md. This proposal complements those rules.

## What is measured and what is assumed

**Inspected:** Central policy and starter instructions at `f6586cc`; the
current MolSysMT planning record under `uibcdf/molsysmt#261`, root contributor
instructions, physchem hydrophobicity, PBC reconstruction, and geometric axes.
The observations concern published/source contracts, not performance results.

**Assumed:** General tools reduce duplication and improve reuse. No quantified
maintenance saving or speedup is asserted. Every member's current AGENTS.md
has not been audited; that inventory is part of the proposed rollout.

## Alternatives and refuted paths

- A rule only in MolSysMT would leave other suite developers without the
  shared requirement requested by the maintainer.
- Repeating a full policy independently in every AGENTS.md invites drift;
  explicit local instructions should point to central authority.
- Exporting every helper or creating a universal utility package makes
  ownership and compatibility harder without establishing useful contracts.
- A keyword/presence check cannot prove scientific decomposition or consumer
  reuse. Automated routing checks need review of actual tools and call paths.
- Mandating Rust for all components ignores existing runtime and language
  contracts. The provider chooses a justified implementation backend.

## Scope and exclusions

Applies to all components registered in suite.toml, including support
libraries where relevant. This is a shared engineering rule and its adoption,
not an interaction detector implementation, a redistribution of all current
domain ownership, or a blanket historical refactoring campaign. External
libraries are references or dependencies, not subjects of this AGENTS rollout.

## Acceptance criteria

- A central normative document defines general-tool design, provider
  ownership, prospective scope, and tracked exceptions.
- The canonical guide and central AGENTS.md route the rule accurately.
- Every applicable registered member's root AGENTS.md contains a discoverable
  instruction with the canonical route, or a reviewed time-bounded exception.
  An inventory records the actual adoption state and evidence.
- The starter kit includes the instruction and its generation check proves
  it survives repository generation.
- Reviews of concrete local tools and consumers show standalone contracts,
  direct reuse, and correct domain ownership. The review evidence distinguishes
  actual implementation from routing/presence checks.
- Guide synchronization, offline governance validation, and applicable
  member gates pass at the recorded commits. The issue stays open until
  adoption is complete or remaining exceptions are explicitly accounted for.

## Local implementation issues

- `uibcdf/molsysmt#261`: ionic analysis with reusable molecular tools; the
  originating local design decision. MolSysMT may adopt the instruction as
  a local maintainer rule while central acceptance remains pending.
- Further member implementation issues are opened only for concrete edits
  or provider changes identified by the rollout, avoiding duplicate reports.

## Dependencies and risks

Use existing [reporting](../reporting_protocol.md) and tracked-exception
semantics. Preserve acyclic provider/consumer dependencies, soft dependency
boundaries, public compatibility, and local contributor conventions. General
tools must not silently change units, indices, chemical assumptions, or
scientific evidence to fit a particular consumer.

The bounded preparation inspected MolSysMT after the required status refresh:
its main had 12 local commits and 5 remote commits not yet integrated, with a
clean worktree. That history is deliberately preserved. Central documentation
is prepared in an isolated checkout from refreshed origin/main; no member
history integration is needed to open this proposal.

## Preparation validation — 2026-09-30

The central offline governance validator and generated-index check pass.
Ruff passes on the governance/index/report scripts. A broader Ruff check of
scripts and tests reports three existing findings in the unchanged
`devtools/scripts/molsys_dev_setup.py` (EXE001, I001, FURB177); checking the
entire tree also encounters the intentionally unsubstituted starter-template
TOML. No Python source or template is changed by this proposal. These checks
do not constitute member adoption or a successful full-suite lint run.
