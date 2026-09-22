# Architecture

| Layer | Question | Component |
|---|---|---|
| Knowledge | What is known? | Sabueso |
| Modeling | What can we represent/model/compute? | MolSysMT, MolSysViewer, TopoMT, ElastNetMT, PharmacophoreMT, DockingMT, ... |
| Capabilities | What do we know how to do reproducibly? | Praxis |
| Discovery | What are we trying to discover and learning? | Nextia |

**KNOW → MODEL → DO → DISCOVER → LEARN** is a narrative, not a mandatory pipeline.

## Roles
- **Sabueso:** knowledge memory.
- **Modeling:** molecular representations and scientific computation.
- **Praxis:** methodological memory (`Capability`, `Protocol`).
- **Nextia:** discovery memory/execution (`DiscoveryProject`, `DiscoveryEngine`).
- **MolSys-AI/MOLI:** optional transversal intelligence.

## Invariants
- Reproducible science works without AI.
- Nextia is graph-shaped, not a rigid state machine.
- Stable references connect graph objects; avoid recursive mega-objects.
- State and execution remain separate.
- Open-ended reasoning and deterministic execution remain separable.
- Failed, conflicting, inconclusive, rejected and superseded states are preserved.
- Discovery may generate both new knowledge and new validated capabilities.

## Abstraction ladder
`Discovery operation → Capability → Protocol → Scientific API`

Humans and MOLI may enter/bypass levels as appropriate.
