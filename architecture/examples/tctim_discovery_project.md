# Example — TcTIM Selective Inhibition

```yaml
discovery_project:
  id: project:tctim-selective-inhibition
  name: TcTIM selective inhibition

  framing:
    focus: Selective molecular intervention on TcTIM
    goal: Develop a selective inhibition strategy with reduced activity against human TIM

  entities:
    - ref: sabueso:protein:TcTIM
      roles: [target]
    - ref: sabueso:protein:HsTIM
      roles: [selectivity_reference]

  questions:
    - id: Q1
      text: Are there exploitable intervention sites in TcTIM that differ from HsTIM?
      status: open

  hypotheses:
    - id: H1
      statement: The TcTIM dimer interface contains parasite-specific allosteric intervention sites.
      status: active
      related_questions: [Q1]
      evidence_for: [E1]
      evidence_against: []

  strategies:
    - id: S1
      description: Compare TcTIM and HsTIM structural ensembles for persistent topographic and dynamical differences.
      status: accepted
      addresses: [Q1, H1]

  campaigns:
    - id: C1
      purpose: Comparative ensemble characterization of candidate intervention sites
      status: completed
      strategy_refs: [S1]
      capability_requests: [praxis:identify_selective_intervention_sites@0.1]
      run_refs: [R1]

  runs:
    - id: R1
      protocol_ref: praxis:comparative_dynamic_sites@0.1
      status: completed
      artifact_refs: [A1, A2]
      result_refs: [RES1]

  observations:
    - id: O1
      statement: Pocket P3 persists in the TcTIM ensemble and is substantially reduced in the HsTIM reference ensemble.
      derived_from: [RES1]
      informs: [H1]

  evidence:
    - id: E1
      statement: Comparative topographic/dynamical analysis supports differential accessibility of P3.
      basis: [O1, RES1]
      relation: supports
      subject_refs: [H1]

  decisions:
    - id: D1
      statement: Advance P3/interface strategy to deeper characterization.
      status: active
      basis: [E1]
```

## What this tests
- target is a role, not a root type;
- Sabueso references are external;
- Campaign invokes Praxis;
- Run binds an exact Protocol version;
- Observation and Evidence are distinct;
- no separate Claim object is required.
