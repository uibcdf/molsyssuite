# Nextia — DiscoveryEngine

Deterministic execution/orchestration operating on DiscoveryProjects.

## Responsibilities
- validate requested-operation prerequisites;
- request/invoke Praxis Capabilities;
- select Protocol under explicit deterministic policy or accept a selected Protocol;
- instantiate Runs;
- register status, failures, retries, Artifacts, Results and provenance;
- update graph relations;
- manage Campaign execution;
- enforce configured approval gates;
- preserve execution history.

## Non-responsibilities
The Engine does not inherently:
- invent hypotheses through opaque LLM reasoning;
- silently reinterpret Evidence;
- certify Capabilities;
- erase contradictory history;
- make decisions beyond configured authority.

## Protocol selection
Automatic selection is appropriate when explicit constraints determine the choice. If scientific judgment is required, request human/MOLI input.

## First-class non-success states
- failed Run;
- partial Run;
- invalid input;
- unavailable resource;
- incompatible Protocol;
- inconclusive Campaign;
- contradictory Results;
- cancelled/rejected action.

## Approval gates
Possible gates: expensive computation, Candidate promotion, Strategy acceptance, experimental action, Protocol/Capability promotion.

## Events
An event model may later expose `run_started`, `artifact_registered`, etc. It is not frozen.
