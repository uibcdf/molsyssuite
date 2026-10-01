# MolSysSuite developer guide

This directory contains **MolSysSuite member governance**, coordinated rollout state, collective evidence, and long-lived technical guidance for the molecular-modeling ecosystem.

MolSysSuite is a first-class component of MOLI with delegated internal governance.

## Governance layering

```text
MOLI
  └── platform contracts for MolSysSuite as a component
       MolSysSuite
         ├── normative engineering and modeling policies for members
         ├── adoption / rollout decisions
         └── member conformance machinery and policy releases
                  ↓
             component-local implementation
```

The policies in this directory are normative for registered members according to `suite.toml`. Some values initially match MOLI's direct-component policies, but future changes require a MolSysSuite decision and policy release. MOLI revisions cannot silently change member rules.

MolSysSuite-specific normative material includes member classification, admission/lifecycle, modeling dependency rules, collective validation, suite initiatives, and domain-specific coordination.

Before filing or closing work, read `reporting_protocol.md` and `repository_contract.md`. The authoritative member registry is `../suite.toml`.

Current work remains under `pending_bugs/` and `pending_proposals/`; closed records remain under `archive/`. Coordinated adoption programs remain under `rollouts/`.

New MolSysSuite components use the suite starter kit after central admission. The starter kit reads the MolSysSuite member baseline from `suite.toml`.

Members exposing optional external engines follow the
[optional engine integration contract](optional_engine_integration.md), derived
from TopoMT and the DepDigest/SMonitor provider recipe. Applicability, exceptions
and evidence are recorded per boundary; component architecture and scientific
validation remain local.

The governance validator and member conformance checker read `suite.toml`
locally. They do not need a neighboring MOLI checkout. The recorded MOLI commit
identifies platform-contract context for MolSysSuite itself; it does not supply
member engineering values.

Accepted contributor and agent actions follow the
[durable working-instruction policy](working_instructions_policy.md).
Read [AGENTS.md](AGENTS.md) for developer-guide work; technical findings stay in
their owning issues, tests and maintained technical documentation.

The [generated component dependency graph](component_dependencies.md) shows
typed direct relationships, provider-first layers and coordinated cycles. Follow
[its policy](dependency_graph_policy.md) for queries, metadata comparison and
maintenance; edit `suite.toml` and regenerate the view instead of editing the diagram.

Reusable capabilities follow the [modular reusable tools policy](modular_reusable_tools.md).
It assigns general operations to their domain owner, keeps consumer-specific criteria
local and requires explicit root contributor routing, reviewed reuse and bounded exceptions.
