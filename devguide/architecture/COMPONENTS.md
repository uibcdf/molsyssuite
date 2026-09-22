# MolSysSuite — Component Responsibilities

## Sabueso — Knowledge
Mission: structure, normalize and trace what is already known about molecular entities. Core concepts include `Card`, `Deck`, `EvidenceStore`.

Non-goal: project hypotheses, campaigns, candidates, project decisions and discovery execution.

## Modeling
- MolSysMT — molecular-system representation/interoperability.
- MolSysViewer — interactive exploration/visualization.
- TopoMT — molecular topography.
- ElastNetMT — elastic-network/dynamical/network analysis.
- PharmacophoreMT — pharmacophore models/workflows.
- DockingMT — docking workflows/engine integration.

## Praxis — Capabilities
Mission: encode reusable scientific know-how.

### Capability
Semantic scientific ability: **what can be done**. It defines meaning, inputs, outputs and prerequisites without unnecessarily fixing one implementation.

### Protocol
Versioned reproducible implementation: **how it is done**. It may specify tools/versions, parameters, seeds, steps, outputs, quality criteria and provenance.

A Capability may have multiple Protocols. A discoverable Capability/Protocol registry is expected, but its implementation is not frozen.

## Nextia — Discovery
Mission: represent and execute structured molecular discovery investigations.

### DiscoveryProject
Machine-readable scientific state, manipulable without an LLM. Likely objects: Objective, Question, Hypothesis, Strategy, Evidence, Candidate, Campaign, Experiment, Decision, Artifact reference and Provenance.

### DiscoveryEngine
Deterministic execution/orchestration: project lifecycle, task/campaign execution, Praxis invocation, direct tool invocation where allowed, validation, artifact/result registration, provenance, state transitions, resumability/replay and approval gates.

Non-goal: ownership of open-ended scientific interpretation or LLM reasoning.

## MolSys-AI — Intelligence
Optional agentic infrastructure: model backends, context, RAG, planning support, tool/capability access and agent infrastructure.

## MOLI — Scientific agent
Primary scientist-facing agent. MOLI may interpret intent, inspect projects, propose questions/hypotheses, expose uncertainty, invoke all layers, interpret results and compose experimental workflows when a Capability is missing.

MOLI is not DiscoveryEngine and is not required for Nextia.
