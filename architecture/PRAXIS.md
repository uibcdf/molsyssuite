# Praxis

Praxis is MolSysSuite's **methodological memory**.

## Capability
Semantic scientific ability: **WHAT we know how to do**.

A Capability should eventually describe:
- identity/version;
- scientific intent;
- input/output contracts;
- applicability/preconditions;
- available Protocols;
- validation status/evidence;
- limitations;
- maturity/deprecation state.

Examples: compare binding sites, identify selective intervention sites, characterize allosteric networks, evaluate mutations, screen compounds, analyze assays.

## Protocol
Reproducible implementation: **HOW a Capability is performed**.

A Protocol may specify inputs, prerequisites, tool versions, parameters, steps, outputs, checks, provenance, and cost/fidelity characteristics.

Multiple Protocols may implement one Capability.

## Composition
Capabilities may plausibly compose Capabilities; Protocols may call APIs and perhaps other Capabilities. Exact composition rules remain open and must preserve provenance and avoid hidden recursion.

## Protocol selection
May depend on applicability, validation status, resources, cost/time, requested fidelity and project policy.

Deterministic policy may be executed by DiscoveryEngine. Open-ended scientific judgment belongs to humans/MOLI.

## Lifecycle
Conceptual maturity:
`experimental → reviewed → validated → deprecated/superseded`

Exact states are not frozen.

## Evolution
`scientific need → APIs → ad-hoc workflow → formalized Protocol → validation/generalization → Capability`

MOLI may help compose; it does not certify.
