# MolSysSuite — Canonical Scientific Workflow

## Motivating input
> “MOLI, vamos a diseñar un inhibidor selectivo para TcTIM.”

This pharmacological example is canonical but not restrictive.

## 1. Intent and project creation
MOLI interprets the natural-language intent and proposes structured project information. A human can confirm/edit it before Nextia creates/updates the DiscoveryProject.

Example:
- Objective: selective TcTIM inhibition.
- Reference/off-target: human TIM.

## 2. Questions before methods
The project should not jump directly to docking. Questions decompose the Objective:
- What is already known about TcTIM inhibition?
- How conserved is the catalytic site relative to human TIM?
- Are alternative parasite-specific intervention sites present?

## 3. Hypotheses and strategies
Examples:
- H1: catalytic-site selectivity is achievable.
- H2: the dimer interface contains exploitable parasite-specific sites.
- Strategy S2: investigate allosteric/interface selectivity before initiating compound screening.

## 4. Knowledge acquisition
Sabueso supplies structured existing knowledge: identifiers, structures, annotations, ligands, mutations, interactions and literature-linked facts.

## 5. From project need to Capability
DiscoveryEngine identifies an executable need associated with a Question/Hypothesis/Strategy.

Example Capability:
`identify_selective_intervention_sites(target, reference)`

## 6. Protocol and Campaign
Praxis provides an appropriate Protocol, e.g. `dynamic_comparative_sites_v1`.

Nextia creates a project-specific Campaign that applies that Protocol to the selected TcTIM/HsTIM systems/ensembles.

**Protocol = reusable method. Campaign = this project's execution of work.**

## 7. Execution
DiscoveryEngine coordinates the Campaign. The Protocol may compose:
`Sabueso → MolSysMT → TopoMT → ElastNetMT → analysis`

Execution produces Artifacts and structured Results with provenance.

## 8. Evidence
Explicit analysis/criteria convert Results into Evidence relevant to the project.

Examples:
- E17: pocket P3 persists across the target ensemble.
- E22: the corresponding cavity is substantially reduced in human TIM.
- E31: the region is dynamically coupled to functionally relevant residues.

Evidence may support, contradict or leave a Hypothesis unresolved.

## 9. Interpretation and decision
MOLI may synthesize evidence and expose uncertainty. Humans may accept, reject or modify proposals. Material project choices are recorded as Decisions with rationale/evidence available at that time.

## 10. Iteration
New Questions, Hypotheses, Strategies, Campaigns, Candidates and Experiments follow.

## Direct access remains possible
- known inhibitors → Sabueso;
- show pockets → TopoMT + MolSysViewer;
- compare sites → Praxis Capability;
- continue project → Nextia;
- bespoke residue/distance calculation → direct Modeling API.

## Methodological learning
If no suitable Capability exists, MOLI/humans may compose direct APIs into an experimental workflow. After formalization, testing and scientific validation, it may become a Praxis Protocol/Capability.
