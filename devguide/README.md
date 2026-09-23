# MolSysSuite developer guide

This directory contains **MolSysSuite domain governance**, coordinated rollout state, collective evidence, and long-lived technical guidance for the molecular-modeling ecosystem.

MolSysSuite is a first-class component of MOLI with delegated internal governance.

## Governance layering

```text
MOLI
  ├── platform/scientific governance
  └── shared engineering baseline
            ↓ inherited
       MolSysSuite
         ├── modeling-domain governance
         ├── adoption / rollout profiles
         └── member conformance machinery
                  ↓
             component-local rules
```

Some policies in this directory predate MOLI governance and remain here as **MolSysSuite adoption profiles** because they contain member transitions, historical inventories, stricter domain requirements, or executable conformance machinery. Their headers identify the upstream MOLI owner where applicable.

MolSysSuite-specific normative material includes member classification, admission/lifecycle, modeling dependency rules, collective validation, suite initiatives, and domain-specific coordination.

Before filing or closing work, read `reporting_protocol.md` and `repository_contract.md`. The authoritative member registry is `../suite.toml`.

Current work remains under `pending_bugs/` and `pending_proposals/`; closed records remain under `archive/`. Coordinated adoption programs remain under `rollouts/`.

New MolSysSuite components use the suite starter kit after central admission. The starter kit must satisfy inherited MOLI engineering policy as well as MolSysSuite-specific requirements.

