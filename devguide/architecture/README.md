# MolSysSuite Architecture 1.0

**Status: conceptual baseline frozen.**

This is the repository-ready granular documentation package. It freezes conceptual responsibilities and boundaries, not implementation APIs or storage.

## Governance boundary

This directory is the normative source for conceptual layers and their relationships.
The top-level [`suite.toml`](../../suite.toml) is separately authoritative for existing,
admitted and governed repositories; its `[architecture]` table identifies this version
without duplicating the layer model. Architectural names do not imply an implemented
or admitted repository.

Praxis and Nextia are defined here but are not yet registered components. If their
repositories are created, each must follow the normal MolSysSuite admission process.
The anticipated initial classification is `scientific-component`, `primary`,
`incubating`, `active`, and `python-package`, subject to the evidence and decision at
admission. These repository fields are independent of the Knowledge, Modeling,
Capabilities, and Discovery layers; see
[`member_classification.md`](../member_classification.md).

## Reading order
1. VISION.md
2. ARCHITECTURE.md
3. COMPONENTS.md
4. CONCEPTS.md
5. DESIGN_PRINCIPLES.md
6. PRAXIS.md
7. NEXTIA.md
8. NEXTIA_PROJECT.md
9. NEXTIA_ENGINE.md
10. MOLSYS_AI_AND_MOLI.md
11. SCIENTIFIC_WORKFLOW.md
12. RATIONALE.md
13. DECISIONS.md
14. APPENDIX_ARCHITECTURE_STRESS_TESTS.md
15. APPENDIX_OPERATIONAL_EPISTEMIC_STRESS_TESTS.md
16. FREEZE_TEST_ASSESSMENT.md
17. OPEN_QUESTIONS.md
18. FUTURE_DIRECTIONS.md

Supporting conceptual schemas, concrete freeze examples, and editable Mermaid diagrams are included in subdirectories.
