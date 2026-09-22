# MolSysSuite — Design Principles and Invariants

1. **AI independence.** Reproducible science must work without MOLI/MolSys-AI/LLM.
2. **Multiple abstraction levels.** Discovery → Capability → Protocol → API.
3. **Capabilities do not hide APIs.** Expert/direct access remains first-class.
4. **Controlled capability promotion.** Experimental workflow → formalized Protocol → validation/generalization → versioned Capability.
5. **Explicit provenance.** Track scientifically relevant inputs, versions, parameters, seeds, transformations, Artifacts, Results, Evidence and Decisions.
6. **Separate state from action.** DiscoveryProject = state; DiscoveryEngine = action.
7. **Artifact, Result and Evidence are not synonyms.** Raw outputs do not silently become conclusions.
8. **Entity and project role are separate.** Molecule ≠ Candidate.
9. **Human agency is representable.** Important choices can require explicit review/approval and preserve authorization.
10. **Compose; do not unnecessarily reimplement.** Integrate strong external scientific engines/libraries.
11. **Protect domain boundaries.** Sabueso=known knowledge; Modeling=calculation; Praxis=know-how; Nextia=discovery; MolSys-AI=intelligence.
12. **Discovery improves the platform.** It may create both new knowledge and new reusable methods.
13. **Conceptual flow is not mandatory dependency flow.** KNOW→MODEL→DO→DISCOVER is explanatory, not a rigid pipeline.
14. **Deterministic core, intelligent edge.** Deterministic/reproducible execution belongs in scientific layers; open-ended interpretation/planning may be provided by humans/MOLI.
15. **No hidden scientific decisions.** Selection criteria, thresholds, rankings and project Decisions should be explicit enough to audit when they materially affect conclusions.
