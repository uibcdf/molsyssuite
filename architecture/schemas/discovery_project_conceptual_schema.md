# DiscoveryProject — Conceptual Schema

This is a conceptual contract, not a frozen serialization format.

```yaml
discovery_project:
  id: string
  schema_version: string
  name: string

  framing:
    focus: string
    goal: string

  entities:
    - ref: stable-reference
      roles: [string]

  questions:
    - id: string
      text: string
      status: open|resolved|superseded
      related_to: [stable-reference]

  hypotheses:
    - id: string
      statement: string
      status: active|supported|challenged|rejected|superseded
      related_questions: [ref]
      evidence_for: [ref]
      evidence_against: [ref]
      supersedes: [ref]

  strategies:
    - id: string
      description: string
      status: proposed|accepted|rejected|superseded
      addresses: [ref]

  campaigns:
    - id: string
      purpose: string
      status: planned|running|completed|partial|failed|inconclusive|cancelled
      strategy_refs: [ref]
      capability_requests: [ref]
      run_refs: [ref]

  experiments:
    - id: string
      purpose: string
      status: string
      run_refs: [ref]

  runs:
    - id: string
      protocol_ref: versioned-ref
      status: planned|running|completed|partial|failed|cancelled
      input_refs: [ref]
      artifact_refs: [ref]
      result_refs: [ref]
      provenance_ref: ref

  artifacts:
    - id: string
      kind: string
      location: uri-or-reference
      checksum: optional-string

  results:
    - id: string
      kind: string
      value_or_ref: any
      derived_from: [ref]

  observations:
    - id: string
      statement: string
      derived_from: [ref]
      generates_questions: [ref]
      informs: [ref]

  evidence:
    - id: string
      statement: string
      basis: [ref]
      relation: supports|contradicts|informs
      subject_refs: [ref]

  candidates:
    - id: string
      entity_or_design_ref: ref
      status: string
      related_hypotheses: [ref]
      evidence_refs: [ref]

  candidate_collections:
    - id: string
      collection_ref: ref
      selection_history: [ref]

  decisions:
    - id: string
      statement: string
      status: active|superseded
      rationale: string
      basis: [ref]
      supersedes: [ref]
      approval_refs: [ref]

  external_knowledge:
    - id: string
      source_ref: versioned-or-snapshotted-ref
      used_by: [ref]

  provenance:
    records: [...]
```

## Graph semantics

The lists above are storage-oriented views over a graph. Objects are independently identifiable and connected through stable references. No ordering among Question, Hypothesis, Campaign, Observation, Evidence, and Decision is mandatory.

## Claim decision

The freeze test intentionally omits a separate `Claim` object.

`Observation.statement`, `Evidence.statement`, `Hypothesis.statement`, and `Decision.statement` already cover four distinct epistemic roles:

- observed phenomenon;
- interpreted support/contradiction;
- testable proposition;
- project choice.

If future use cases require durable assertions that are neither observations, evidence, nor hypotheses, `Claim` can be introduced later without changing the four-column architecture.
