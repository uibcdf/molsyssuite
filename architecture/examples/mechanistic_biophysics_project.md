# Example — Mechanistic Biophysics Without Candidates

```yaml
discovery_project:
  id: project:protein-x-atp-coupling
  name: ATP-dependent conformational coupling

  framing:
    focus: ATP-dependent conformational dynamics of protein X
    goal: Understand how ATP binding is coupled to domain closure

  entities:
    - ref: system:protein-x
      roles: [system_of_interest]
    - ref: entity:ATP
      roles: [ligand]

  questions:
    - id: Q1
      text: What conformational processes distinguish apo and ATP-bound ensembles?
      status: open

  campaigns:
    - id: C1
      purpose: Exploratory apo/holo ensemble analysis
      status: completed
      capability_requests: [praxis:compare_conformational_ensembles@0.1]
      run_refs: [R1]

  observations:
    - id: O1
      statement: ATP-bound trajectories show recurrent coupling between loop L and domain D.
      derived_from: [RES1]
      generates_questions: [Q2]

  questions:
    - id: Q2
      text: Does loop L mediate ATP-to-domain-D communication?
      status: open

  hypotheses:
    - id: H1
      statement: Loop L is a major mediator of ATP-dependent domain coupling.
      status: active
      related_questions: [Q2]
      evidence_for: []

  strategies:
    - id: S1
      description: Test dynamical-network coupling and perturb loop-L residues.
      status: accepted
      addresses: [H1]
```

## What this tests
- Candidate is absent;
- Campaign can precede Hypothesis;
- Observation can generate Question;
- project is not pharmacology-specific;
- Focus + Goal remain natural;
- graph semantics are required.
