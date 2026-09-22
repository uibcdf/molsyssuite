# Nextia

Nextia represents and executes structured scientific discovery and is fully usable without an LLM.

## DiscoveryProject
Persistent, machine-readable scientific state/history.

Groups:
- framing: Focus, Goal, entities/systems + roles;
- reasoning: Questions, Hypotheses, Strategies;
- execution context: Campaigns, Experiments, Runs/references;
- outputs: Artifacts, Results, Observations, Evidence;
- design space: Candidates and collections;
- governance: Decisions, approvals/rejections, provenance, history.

Objects have stable identities and graph relations.

## DiscoveryEngine
Deterministic execution/orchestration.

Responsibilities:
- validate prerequisites;
- request/invoke Praxis Capabilities;
- select/accept Protocol under explicit policy;
- instantiate Runs;
- register status/failure/retry/Artifacts/Results/provenance;
- update graph relations;
- manage Campaign execution;
- enforce approval gates;
- preserve history.

It does not inherently invent hypotheses via opaque LLM reasoning, silently reinterpret Evidence, certify Capabilities, erase contradictions, or exceed configured authority.

## Graph-shaped science
Valid paths include:
- Question → Hypothesis → Campaign → Evidence
- Campaign → Observation → Question → Hypothesis
- Evidence → Decision → new Question
- conflicting Evidence → revised Hypothesis

No sequence is mandatory.

## Non-success is first-class
Failed, partial, cancelled, incompatible, inconclusive, contradictory, rejected, and superseded outcomes remain represented.
