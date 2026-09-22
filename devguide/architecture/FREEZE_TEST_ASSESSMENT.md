# Freeze-Test Assessment

## DiscoveryProject schema
The two examples fit the same conceptual schema without introducing domain-specific root concepts.

### Findings
- `Focus + Goal` works in both design and mechanistic science.
- `Target` works naturally as a role where appropriate and disappears where not.
- Candidate can be absent.
- Campaign-before-Hypothesis is representable.
- Observation is necessary.
- stable references cleanly separate Sabueso/Modeling/Praxis/Nextia.
- versioned Protocol references solve historical reproducibility at the conceptual level.

## Claim
A separate `Claim` object was deliberately tested by omission.

For current examples:
- `Observation` represents what was noticed;
- `Evidence` represents interpreted support/contradiction/information;
- `Hypothesis` represents a testable proposition;
- `Decision` represents a project choice.

No irreducible role remained for Claim. Therefore **Claim should not be part of Architecture 1.0 core**. It remains a future extension if real use cases demonstrate a missing epistemic object.

## Praxis schema
Capability/Protocol separation remains clean.

A Protocol can explicitly reference exact implementations and versions while Capability remains semantic. This supports multiple protocols, deterministic selection policies, and MOLI/human selection when judgment is needed.

## Remaining implementation questions
These do not threaten the architecture:
- exact serialization format;
- graph database vs relational/document storage;
- identifier syntax;
- relation vocabulary;
- candidate-collection naming;
- event system;
- maturity-state details;
- cross-project sharing.

## Freeze recommendation
The conceptual architecture has survived:
1. diverse scientific-domain stress tests;
2. operational/epistemic stress tests;
3. concrete schema instantiation in a drug-design and a non-design mechanistic project.

No test required a fifth column, AI dependence, or a new top-level domain abstraction.

**Recommendation: freeze MolSysSuite Architecture 1.0 at the conceptual level.**

Implementation APIs and schemas should remain versioned and evolvable beneath that frozen conceptual architecture.
