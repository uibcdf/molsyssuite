# Nextia — DiscoveryProject

A persistent, machine-readable representation of the scientific state/history of an investigation.

## Groups
**Framing:** Focus, Goal, entities/systems + roles.  
**Reasoning:** Questions, Hypotheses, Strategies, provisional Claims.  
**Execution context:** Campaigns, Experiments, Runs/references.  
**Outputs:** Artifacts, Results, Observations, Evidence.  
**Design space:** Candidates and candidate/design collections.  
**Governance:** Decisions, approvals/rejections, provenance, history.

## Graph model
Objects are independently identifiable and related by references.

This enables:
- one Evidence item informing multiple Hypotheses;
- one Candidate participating in multiple Campaigns;
- project branching;
- shared entities across projects;
- superseding without deletion;
- contradictory evidence;
- historical reconstruction.

## Not hypothesis-first
Valid paths include:
- Question → Hypothesis → Campaign → Evidence
- Campaign → Observation → Question → Hypothesis
- Evidence → Decision → new Question
- Observation → Strategy change
- conflicting Evidence → revised Hypothesis

## Historical integrity
Scientifically meaningful previous states should not be silently overwritten. Rejection, failure, contradiction and supersession are information.
