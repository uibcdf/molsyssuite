# MolSysSuite — Architectural Rationale

This document preserves *why* the architecture has its current form.

## Why four columns?
Capabilities did not fit cleanly inside Modeling or Discovery.

- Modeling asks what can be represented/computed.
- Capabilities ask what scientific task can be performed reproducibly.
- Discovery asks why that task is needed now and what it means for the investigation.

A separate Capabilities layer removes this tension.

## Why Sabueso is not Discovery
Sabueso represents **what is known about an entity**. DiscoveryProject represents **what we are learning in this investigation**. Adding hypotheses, campaigns, candidates and project decisions to Sabueso would mix entity knowledge with project state.

## Why Praxis exists
Scientific APIs provide primitives; scientists often think in semantic tasks. `identify_selective_intervention_sites` may compose Sabueso, MolSysMT, TopoMT and ElastNetMT. Praxis captures this reusable know-how while preserving direct API access.

## Why Capability and Protocol differ
A Capability can remain scientifically stable while implementations evolve. Several Protocols may implement it with different engines, assumptions, data availability, cost or accuracy.

## Why Strategy, Campaign and Protocol differ
- Strategy: project-level approach — *why/where are we going?*
- Campaign: project-specific coordinated work — *what are we executing in this project?*
- Protocol: reusable reproducible method — *how is a task performed?*

This separation prevents Nextia project logic from leaking into Praxis methodology.

## Why Nextia is independent of MolSys-AI
DiscoveryProject is structured state and DiscoveryEngine is reproducible orchestration. Neither inherently requires an LLM. Keeping Nextia independent protects reproducibility and allows normal Python/Jupyter use.

## Why MolSys-AI is transversal
MOLI may query Sabueso, use raw Modeling APIs, invoke Praxis, or operate on Nextia. Confining it to Discovery would be artificial.

## Why MOLI works at multiple levels
High-level semantic interfaces improve efficiency; full APIs preserve scientific expressivity. MOLI must be able to descend when no Capability exists or when expert-level control is required.

## Why MOLI may help create Capabilities
A novel scientific need may require an ad-hoc composition of APIs. If useful and generalizable, that workflow can be formalized as a Protocol and, after validation, exposed as a Capability. This is methodological learning, not autonomous self-certification.

## Why Artifact, Result and Evidence differ
A file/trajectory/pose set is an Artifact. A computed measurement or summarized outcome is a Result. Evidence is the scientifically interpreted observation that bears on a Question/Hypothesis. Keeping these distinct prevents raw computational output from masquerading as a conclusion.

## Why Molecule and Candidate differ
A molecular entity exists independently. Candidate is a project role. The same molecule may be a Candidate in multiple projects for different purposes/status/evidence.

## Three memories
- Sabueso — **knowledge memory:** What is known?
- Praxis — **methodological memory:** What do we know how to do?
- DiscoveryProject — **discovery memory:** What have we learned here?

MOLI can reason across all three.

## Why the cycle is not a pipeline
KNOW→MODEL→DO→DISCOVER is explanatory. Real work is graph-like: Praxis may consume Sabueso directly; Nextia may call direct APIs; Modeling may be used standalone. The architecture must preserve this flexibility.
