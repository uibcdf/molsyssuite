# MolSysSuite

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/downloads/)
[![UIBCDF](https://img.shields.io/badge/UIBCDF-Lab-red.svg)](http://uibcdf.org)

MolSysSuite is the **molecular modeling ecosystem of the MOLI platform**. Its
components provide molecular-system representation, interoperability, computation,
analysis, and visualization, supported by reusable scientific Python libraries and
developer tools. Drug design is one application, not the boundary of the suite.

MolSysSuite works directly for scientists and software without requiring an AI agent.
Components may interoperate with MOLI's Scientific Context where useful, while keeping
their own APIs, evidence, and implementation responsibilities.

## Relationship to MOLI

[MOLI Platform Architecture 1.0](https://github.com/uibcdf/moli/blob/main/architecture_1.0/README.md)
defines the wider platform: Scientific Context and MolSysSuite are complementary, with
an optional MOLI Agent for scientific reasoning. MOLI also defines MolSys-AI as a
specialist agent for operating MolSysSuite; it is not a mandatory gateway to the APIs.
Platform architecture and the shared MOLI engineering baseline are maintained in `uibcdf/moli`. This repository owns MolSysSuite-specific governance, member coordination, domain extensions, and rollout/enforcement across the modeling ecosystem.

Architectural concepts do not become MolSysSuite components automatically. The
[`suite.toml`](suite.toml) registry alone identifies the repositories currently
admitted and governed here; neither MOLI Agent nor MolSys-AI is registered as a
MolSysSuite member.

## Registered MolSysSuite components

These are the implemented repositories currently registered in [`suite.toml`](suite.toml).
The roles describe their place in suite governance, not layers of MOLI Architecture
1.0. Registration does not mean every component has reached a stable public API.

| Component | Role | Contribution |
| --- | --- | --- |
| [MolSysMT](https://github.com/uibcdf/molsysmt) | Scientific component | Molecular-system representation and interoperability |
| [MolSysViewer](https://github.com/uibcdf/molsysviewer) | Scientific component | Interactive molecular visualization |
| [TopoMT](https://github.com/uibcdf/topomt) | Scientific component | Molecular topography |
| [PharmacophoreMT](https://github.com/uibcdf/pharmacophoremt) | Scientific component | Pharmacophore modeling |
| [ElastNetMT](https://github.com/uibcdf/elastnetmt) | Scientific component | Elastic-network modeling |
| [DockingMT](https://github.com/uibcdf/dockingmt) | Scientific component | Molecular docking workflows |
| [SMonitor](https://github.com/uibcdf/smonitor) | Support library | Structured diagnostics and telemetry |
| [ArgDigest](https://github.com/uibcdf/argdigest) | Support library | Argument validation and normalization |
| [DepDigest](https://github.com/uibcdf/depdigest) | Support library | Optional-dependency management |
| [PyUnitWizard](https://github.com/uibcdf/pyunitwizard) | Support library | Interoperable physical units |
| [Ackredit](https://github.com/uibcdf/ackredit) | Support library | Scientific attribution and citation support |
| [Pytest Receptor](https://github.com/uibcdf/pytest-receptor) | Developer tool | Compact pytest evidence reports |
| [GH Run Receptor](https://github.com/uibcdf/gh-run-receptor) | Developer tool | GitHub Actions run inspection |
| [Lindelint](https://github.com/uibcdf/lindelint) | Developer tool (auxiliary) | Interpolation support developed for ElastNetMT |

The suite-wide Python baseline is 3.11–3.13; some components have separately admitted
3.14 support. Check each component and the [Python support policy](devguide/python_policy.md)
for its effective range.

## Coordinating the suite

Policies and contracts shared by multiple components are proposed and tracked in the
[MolSysSuite issue board](https://github.com/uibcdf/molsyssuite/issues). Component-local
implementation remains in the component that owns it.

The [`devguide`](devguide/README.md) records the analysis and decisions, while issues are
their stable public identities. The authoritative component registry is
[`suite.toml`](suite.toml). Contributors should read the
[`reporting protocol`](devguide/reporting_protocol.md) before filing or closing
suite-wide work. A new component starts from the versioned
[`component starter kit`](devguide/new_component_starter_kit.md) after its central
admission proposal is accepted.

## Installing components

Choose the components you need from the registered list and follow the installation
instructions in their own repositories. This repository coordinates the suite, inherits applicable MOLI engineering policies, and owns MolSysSuite-specific domain governance; it is not itself a substitute for those component packages.
