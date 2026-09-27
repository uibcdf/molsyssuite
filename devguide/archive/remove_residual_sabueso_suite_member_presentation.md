---
summary: Remove residual presentation of Sabueso as a MolSysSuite member.
issue: uibcdf/molsyssuite#42
status: resolved
opened: 2026-09-23
closed: 2026-09-27
verification: inspected
area: [architecture, documentation]
guard:
normative: devguide/repository_contract.md
blocked_by: []
supersedes: []
---

# Remove residual Sabueso suite-member presentation

## What

MolSysMT's suite overview and its local editorial rule listed Sabueso among
MolSysSuite tools. Copied documentation examples in TopoMT, PyUnitWizard, and
ElastNetMT also named Sabueso where the local package was intended.

## How

MolSysMT now states that Sabueso belongs to MOLI's Scientific Context, removes
it from the suite-member list, and includes DockingMT as a registered scientific
component. Its page-specific agent rule and ecosystem index agree. TopoMT's issue
tracker docstring names TopoMT; the PyUnitWizard and ElastNetMT notebook examples
name their owning packages. The member changes are `molsysmt@f7c24d7`,
`topomt@015cb48`, `pyunitwizard@1509f95`, and `elastnetmt@6705363`.

## Why

The MolSysSuite member registry is authoritative for suite membership.
The repository contract assigns MOLI platform boundaries to MOLI and internal
suite membership to MolSysSuite. Documentation and editorial instructions must
follow that boundary so the error is not reintroduced by later editing.

## Verification

The four member working trees passed Ruff lint and format checks. The changed
notebooks parse as JSON. The targeted documentation no longer presents Sabueso
as a MolSysSuite member; MolSysMT expressly describes its MOLI relationship.
