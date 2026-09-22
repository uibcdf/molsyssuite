# Praxis — Capability / Protocol Conceptual Schema

Not a frozen serialization format.

```yaml
capability:
  id: string
  version: string
  name: string
  scientific_intent: string
  inputs:
    - semantic_type: string
      required: bool
  outputs:
    - semantic_type: string
  preconditions: [...]
  protocols:
    - versioned-ref
  validation:
    status: experimental|reviewed|validated|deprecated
    evidence_refs: [...]
  limitations: [...]
  metadata: {...}

protocol:
  id: string
  version: string
  capability_ref: versioned-ref
  applicability:
    conditions: [...]
  inputs: [...]
  steps:
    - id: string
      action: api-call|capability-call|transform|validation
      implementation_ref: versioned-ref
      parameters: {...}
  outputs: [...]
  checks: [...]
  provenance_requirements: [...]
  resource_profile:
    cost_class: optional
    fidelity_class: optional
  status: experimental|reviewed|validated|deprecated
```

## Semantics

Capability answers **WHAT scientific task can be performed?**

Protocol answers **HOW is that task performed reproducibly?**

A Capability may have multiple Protocols. Protocol selection can be deterministic when explicit applicability/policy suffices; otherwise human/MOLI judgment is requested.

## Composition

This freeze test permits a Protocol step to call:
- a scientific API;
- a transformation/validator;
- another Capability.

Recursive composition must be detectable and prohibited unless explicitly supported in a future design.
