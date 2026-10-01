---
summary: Require modular reusable tools across MolSysSuite components
issue: uibcdf/molsyssuite#61
status: resolved
opened: 2026-09-30
closed: 2026-10-01
verification: measured
area: [governance, architecture]
guard: tests/test_modular_tools_policy.py
normative: devguide/modular_reusable_tools.md
blocked_by: []
supersedes: []
---

# Require modular reusable tools across MolSysSuite components

**Reported:** 2026-09-30, from the maintainer's modular-design decision in
`uibcdf/molsysmt#261` and request to make it explicit across MolSysSuite.
**Status:** Resolved on 2026-10-01. The accepted common rule, guide summary,
root instructions, starter kit and routing audit are published. All fifteen
registered members have adopted the instruction and synchronized guide; final
hosted audits pass. Architectural source review and its execution limits are
recorded separately from contributor-routing checks.

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


## Policy implementation and review: 2026-10-01

The maintainer authorized completing this proposal after the issue review.
`devguide/modular_reusable_tools.md` is accepted in `suite.toml` for all registered
repositories, prospectively at relevant new/changed capabilities. The canonical
suite guide summarizes the rule; central and starter `AGENTS.md` explicitly route
it through `MOLSYSSUITE_GUIDE.md#modular-reusable-tools`. Fifteen member instructions
are prepared in clean isolated checkouts. Canonical synchronization requires its
source commit before consumer distribution; the first attempted pre-commit sync
correctly rejected the uncommitted guide. No consumer copy was edited manually.

The existing component-guide audit now checks this active root route in its named
section, rejecting an orphan link, comments and fenced examples. This is delivery
verification only. Nine regression tests had five failures and one registry error
before implementation; all nine now pass, including starter generation with no
runtime dependencies. All 164 central unittest checks and offline governance pass;
Ruff lint/format for the changed Python files and whitespace checks pass.
The pinned member policy caller checks, scientific CI and environments are unchanged.

Architectural review is separate from that mechanical route audit:

| Provider/tool and actual consumer | Inspected evidence and limit |
| --- | --- |
| uibcdf/molsysmt `1d66bf1247ed450e40a4d2d18fc6d0501a8bbb20`: `structure.get_principal_axes` → `structure.align_principal_axes` | The public general tool is exported by structure, documents selection/frame/weights/type, output shapes, axis ordering and degenerate-input meaning. The consumer imports and calls it, then applies its own alignment requirements. This is source review of standalone contract and real reuse; no scientific execution or new performance claim is made. |
| uibcdf/depdigest released `0da46d9ff31fbe2f92e4e667a32868aebe840b39`: `check_dependency` → uibcdf/topomt `0fbaa32dc74100e8fb04e2c06e7ee29093cd3fc9` fpocket runner | The supported provider checks actual executable availability and owns truthful installer hints. The consumer calls it and retains execution/output/error translation. The accepted previous publication evidence under uibcdf/molsyssuite#62 is installed/public provider matrices and nine consumer availability cases in each of six hosted cells (36829466420). Those earlier checks are recorded evidence, not new scientific measurements for this policy. |

These examples demonstrate within-component and cross-component supported tool
reuse without prescribing new scientific algorithms or globally changing backend
language. Scientific fidelity and missing domain capabilities stay with component
teams and their issues, including the motivating uibcdf/molsysmt#261.

Initial isolated-member preflight and final publication/adoption identities follow
below. Original component worktrees, including the ArgDigest untracked artifact
and TopoMT generated version modification, remain preserved. MolSysMT/MolSysViewer
execution-review deferrals remain in force.

## Member publication inventory: 2026-10-01

All fifteen registered members publish the explicit root instruction and the
byte-identical guide sourced from central commit
`7b1ef24a39ac78aed95dd495b11a26493c610189`. Guide SHA256:
`8999301c5e8a9193a75bf530527da88529da7e74f1ff87c57370cf3c54faaf5c`. Distribution used only `sync_vendored_guides.py`.

| Member | Published main commit |
| --- | --- |
| uibcdf/smonitor | `765fce1f53b25965d47bec1bd2f85e8ae80cdb4c` |
| uibcdf/argdigest | `c0545e1ffba0861a18e1458e0ff5fde756e59e73` |
| uibcdf/depdigest | `beb7579d05f7ffc8728d549ca327e812f1305db4` |
| uibcdf/pyunitwizard | `039617a42a5b4270d29979d53dc3d6ad759027c8` |
| uibcdf/pytest-receptor | `dc12de53a6411df82a8b2d34bc37b48239ce6bb6` |
| uibcdf/gh-run-receptor | `54609d491f4960904acc520d46a274f86d45b467` |
| uibcdf/molsysmt | `e69c8c2864483d96fc24a455937fdb593ec39d1b` |
| uibcdf/molsysviewer | `fec59a6bf5d15c82d75a7b68c7955c03fa82e625` |
| uibcdf/topomt | `60abf106510322af550d81b702a2166a2896bace` |
| uibcdf/pharmacophoremt | `5acaa217188c7e3617ba849f1fab694dc850a29d` |
| uibcdf/elastnetmt | `56c2f0e7ce9494b38eaf9e9a34030c1d753b4cca` |
| uibcdf/dockingmt | `e3b7cdcf37ec31f10c784086d84d6f0a3fcb368e` |
| uibcdf/ackredit | `ad773d23812795865fdc78d29a1dd23fb72efe0b` |
| uibcdf/lindelint | `9a61badf9f5596e1a02c6df457f26d5042777c55` |
| uibcdf/molsys-ai | `5f6b1203a15dac9949c7a6984195aa3ffd872b12` |

Each publication changes only root `AGENTS.md` and `MOLSYSSUITE_GUIDE.md`.
The central offline governance guard passed before each commit. Direct pushes
were authorized by the principal maintainer and carry `[skip ci]`; the common
nightly recovery mechanism retains its existing responsibilities. No product
code, dependency environment, scientific suite or policy caller pin changed.

The isolated preflight passes all fifteen guide/routing audits and full
repository conformance for fourteen members. MolSys-AI has three pre-existing
README findings (`IDENTITY_BADGE`, `POLICY_BADGE`, `LICENSE_BADGE`); its route
and synchronized guide pass. These findings are retained rather than counted
as full umbrella conformance. Its children remain under umbrella governance.

Initial automatic audits 36834386403 (component guides) and 36834386247
(vendored guides) failed before consumer publication. They are deployment-order
observations, not final adoption evidence; final manual audits follow after
all fifteen remote publications.

## Final adoption verification: 2026-10-01

[Component guide audit 36835721376](https://github.com/uibcdf/molsyssuite/actions/runs/36835721376)
passed at central `7b1ef24a39ac78aed95dd495b11a26493c610189`: registry plus
fifteen component jobs, with each actual guide/routing step passing. Native
checkout logs contain every published member SHA in the inventory above and
each checker emits the successful contributor-route result. This verifies the
published source identities, rather than merely the prepared local worktrees.

[Vendored guide audit 36835721190](https://github.com/uibcdf/molsyssuite/actions/runs/36835721190)
passed at the same central commit. Its native source/consumer check reports
that all registered vendored guides match their canonical sources. Existing
policy adoption identities are reported independently; this documentation
rollout does not bump or silently replace pinned policy callers.

[Central offline governance 36834386117](https://github.com/uibcdf/molsyssuite/actions/runs/36834386117)
also passed on the implementation commit. The durable regression module is
`tests/test_modular_tools_policy.py`: it protects the registered applicability,
active contributor route, exact guide content and starter generation. The
normative design/exception contract is `devguide/modular_reusable_tools.md`.

All acceptance criteria are met within their recorded scope. No instruction
delivery exception is needed. MolSys-AI's unrelated badge findings, component
scientific implementation issues and the deferred MolSysMT/MolSysViewer
execution reviews remain with their existing owners. This closure adopts a
prospective engineering rule and its delivery; it does not certify every
historical component algorithm or impose another full-suite CI requirement.
