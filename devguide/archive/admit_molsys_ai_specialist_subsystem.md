---
summary: Admit MolSys-AI as the governed specialist subsystem of MolSysSuite.
issue: uibcdf/molsyssuite#43
status: resolved
opened: 2026-09-23
closed: 2026-10-01
verification: measured
area: [governance, membership]
guard: tests/test_governance.py::GovernanceTests::test_molsys_ai_is_registered_as_specialist_subsystem
normative: devguide/repository_contract.md
blocked_by: []
supersedes: []
---

# Admit MolSys-AI as a governed specialist subsystem

**Status:** Resolved after reviewing existing implementation on 2026-10-01.

## What

Admit uibcdf/molsys-ai with role `specialist-subsystem`, primary membership,
incubating maturity and `governed-subsystem` capability. Server, Client and Agent
remain internal repositories governed by the umbrella rather than separate suite
members. The issue preceded this reconstruction of its closure record.

## How

`suite.toml` already records the role, capability, internal governance owner
`uibcdf/molsys-ai` and internal registry `molsys-ai.toml`. Its root instructions
require the canonical suite guide and its own subsystem guide. The shared
classification validator and component-label vocabulary support this role.

## Why

The ecosystem has one responsible AI subsystem boundary and a clear route for
cross-component governance without absorbing child implementations centrally.

## What is measured and what is assumed

Inspected suite registry and exact member source
`8797e93e661c620f4e78a4567ab1e205ffb9aef4`. The existing regression checks every
admission field, including internal owner/registry and the absence of a Python
package capability. Local reporting adoption is independently resolved under
uibcdf/molsys-ai#2. Three pre-existing README badge findings remain; admission
closure does not certify every umbrella resource, badge or child implementation.

## Alternatives and refuted paths

Admitting the three child repositories separately would duplicate the umbrella's
internal governance. The accepted registry keeps their responsibility internal.

## Scope and exclusions

Suite admission/classification and governance routing. Product functionality,
internal migration and child releases remain with MolSys-AI.

## Acceptance criteria

The registered role/capability and internal authority match the accepted issue;
root contributor routing and the suite regression are present. All are met.

## Local implementation issues

uibcdf/molsys-ai#2 records the separately completed reporting lifecycle.

## Dependencies and risks

Membership does not imply stable product contracts or Python-package admission.
The guard directly reads and asserts the relevant registry fields, so removing
the member or changing its role/capability/owner makes it fail.

## Provenance

2026-10-01, coordination host, Python 3.13.15. `suite_status.py`, registry and root
instruction inspection, and the named existing governance regression. Original
member worktrees are preserved; this closure introduces no runtime change.
