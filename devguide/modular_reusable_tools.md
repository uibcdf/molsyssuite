# Modular reusable tools

## Applicability and ownership

This policy applies to every repository registered in `suite.toml`, including
support libraries, scientific components, developer tools and the governed
MolSys-AI subsystem. Accepted under uibcdf/molsyssuite#61. It governs new or
changed capabilities during relevant development. Existing duplicates discovered
in that work are reported to their owner and given a bounded migration decision.

MolSysSuite owns this common design rule. Each component owns its implementation,
public interfaces, scientific definitions, backend and local validation. The
MolSys-AI umbrella carries the rule to its internal governance; its child
repositories retain their existing subsystem authority.

## Required development practice

1. Before adding a feature, inspect existing tools and identify the owning module
   or component for each needed operation. Specify its inputs, outputs, units,
   index spaces, failure modes and scientific or operational meaning.
2. Reuse an existing supported tool when its contract meets the need. If an
   independently useful operation is missing, implement or extend a documented
   reusable tool in its domain owner, with its own contract and tests.
3. Have consumers call that tool. Keep consumer selection, task interpretation,
   rendering and orchestration in the consumer. Keep implementation helpers
   private behind supported boundaries; publish operations with meaningful
   independent contracts. A helper's existence alone does not require an API or
   another package.
4. When a sibling owns a missing capability, report the consumer evidence to that
   provider and cross-link local work under [cross-component feedback](cross_component_feedback.md).
   Preserve dependency direction and selected optional-route boundaries.
5. Review actual provider and consumer call paths. A general name, new module or
   documentation paragraph alone does not demonstrate reuse. The provider must
   expose the needed contract and the consumer must use it.

An operation can be reusable within one component without becoming shared runtime
code owned centrally. Scientific fidelity and component defects remain with the
component development team. Adoption introduces no general requirement to
refactor historical modules or run scientific suites at every internal push.

## Contracts and compatibility

Document the standalone operation independently of its first feature. State
selection/frame conventions, units and dimensions, indexing/mapping, configuration
authority, optional dependencies, degenerate or empty inputs, supported backends
and relevant provenance. A consumer may rely only on a supported contract.

Preserve published signatures, diagnostic identities and justified environment
profiles during extraction or reuse. An internal shortcut needs verified inputs
under the provider's supported delegation contract. Follow the applicable
ArgDigest, DepDigest, SMonitor and PyUnitWizard canonical guides. Quantity
conversion and serialization retain their explicit units and field meanings.

An intentional scientific-definition or output-schema change belongs in the
owning component's issue and compatibility decision. Register any shared contract
change centrally before requiring it from other components.

## Backend and performance

The provider chooses its supported implementation language and backend. Reuse
existing compiled primitives where appropriate; justify additional compilation
from workload and the component's runtime contract. Rust is an available MolSysMT
backend, not a suite-wide implementation requirement.

Record end-to-end timing and allocation when performance motivates a backend
change. Preserve validation, diagnostics, units and scientific evidence at the
supported boundary. This policy adds no universal benchmark or full-suite CI lane;
follow the existing [CI contract](python_ci_policy.md) and local release gates.

## Contributor routing and new members

Every registered member's root `AGENTS.md` has a `## Modular reusable tools`
section with an explicit development instruction and a link to
`MOLSYSSUITE_GUIDE.md#modular-reusable-tools`. The synchronized guide carries the
common summary and links this normative document. Local stricter conventions
remain local, with the same ownership and exception semantics.

The Python starter kit includes this instruction and the canonical guide. It
acquires no runtime dependency merely from adopting the design policy.

Distribute canonical guides with `sync_vendored_guides.py`. Edit root contributor
instructions locally in isolated clean checkouts, preserving other instructions
and concurrent work. Guide publication and caller policy releases remain separate
under the [adoption lifecycle](adoption_lifecycle.md).

## Evidence and verification

The component-guide audit checks byte identity and the active, explicit root
instruction route. It rejects a missing section, an orphan link in another
section, a commented-out instruction or a fenced example. This check protects
delivery of the instruction; it does not certify modular architecture, scientific
correctness or actual consumer reuse. Compatible historical policy callers keep
their pinned conformance behavior; this guide audit does not change those pins.

Architectural review separately records the provider's standalone contract,
actual consumer call, ownership, source/version and scope of inspection or tests.
Executed compatibility evidence is distinguished from source inspection. Existing
applicable examples may demonstrate the rule without creating new runtime tools.
Pure presence checks must never be presented as architectural acceptance.

The rollout under uibcdf/molsyssuite#61 records every registered member's exact
instruction/guide adoption commit and local/hosted governance results. Member
scientific reviews remain separately owned, including explicitly deferred work.

## Exceptions

A temporary duplication, consumer workaround, incomplete tool contract or
historical migration states the affected operation/rule, provider and consumer
issues, rationale, responsible maintainer or role, impact, interim behavior,
review/expiry date and removal condition. Use the existing issue-backed reporting
and [adoption exception](adoption_lifecycle.md) procedures. Provider maintainers
own triage; the consumer owns evidence and its interim limitation.

The instruction and canonical policy route remain visible while an implementation
exception is active. If delivery of the root instruction itself is temporarily
blocked, record a central coordination issue and an unexpired member exception;
report the audit finding as excepted with that evidence, rather than as passing.
An expired or unrecorded exception requires review before further work relies on
the duplicated capability. No broad maturity or development-status exemption
removes ownership, feedback or compatible public contracts.
