# MolSysSuite

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/downloads/)
[![UIBCDF](https://img.shields.io/badge/UIBCDF-Lab-red.svg)](http://uibcdf.org)

## Mission

MolSysSuite is **a unified ecosystem for computational molecular science, molecular
engineering, and molecular discovery**. It connects scientific knowledge, molecular
modeling, reproducible methods, and discovery work while preserving interoperability,
provenance, and scientific control. Drug design is one application of this broader
ecosystem, not its defining scope.

The suite supports interactive scientific work as well as reproducible automation.
Its scientific workflows must remain usable without AI.

## Conceptual architecture

[MolSysSuite Architecture 1.0](devguide/architecture/README.md) defines four conceptual
layers. They describe scientific responsibilities, not a mandatory linear pipeline or
the governance classification of repositories.

| Layer | Guiding question | Architectural association |
| --- | --- | --- |
| Knowledge | What is known? | Sabueso, the knowledge memory |
| Modeling | What can be represented, modeled, computed, analyzed, and visualized? | MolSysSuite modeling tools |
| Capabilities | What do we know how to do reproducibly? | Praxis, the methodological memory |
| Discovery | What are we investigating and learning? | Nextia, the discovery memory and execution layer |

**MolSys-AI and MOLI** represent optional intelligence across all four layers. They
are not a required top level or the "brain" of a linear hierarchy; scientific work
and deterministic execution must remain possible without an LLM.

Praxis and Nextia are part of the frozen conceptual architecture, but they are **not
yet implemented or admitted MolSysSuite components**. Their architectural names do not
assert that repositories exist. Conceptual associations alone never grant membership;
the registry below is the authority for the current suite.

## Implemented and registered components

The following repositories are the current governed members in [`suite.toml`](suite.toml).
Their `role` values classify real repositories for governance and are separate from the
four conceptual layers. Registration does not imply that every component is stable.

| Component | Registered role | Contribution |
| --- | --- | --- |
| [SMonitor](https://github.com/uibcdf/smonitor) | Support library | Structured diagnostics and telemetry |
| [ArgDigest](https://github.com/uibcdf/argdigest) | Support library | Argument validation and normalization |
| [DepDigest](https://github.com/uibcdf/depdigest) | Support library | Optional-dependency management |
| [PyUnitWizard](https://github.com/uibcdf/pyunitwizard) | Support library | Interoperable physical units |
| [Ackredit](https://github.com/uibcdf/ackredit) | Support library | Scientific attribution and citation support |
| [Pytest Receptor](https://github.com/uibcdf/pytest-receptor) | Developer tool | Compact, evidence-preserving pytest reports |
| [GH Run Receptor](https://github.com/uibcdf/gh-run-receptor) | Developer tool | GitHub Actions run inspection |
| [Lindelint](https://github.com/uibcdf/lindelint) | Developer tool (auxiliary) | Interpolation support developed for ElastNetMT |
| [MolSysMT](https://github.com/uibcdf/molsysmt) | Scientific component | Molecular-system representation and interoperability |
| [MolSysViewer](https://github.com/uibcdf/molsysviewer) | Scientific component | Interactive molecular visualization |
| [TopoMT](https://github.com/uibcdf/topomt) | Scientific component | Molecular topography |
| [PharmacophoreMT](https://github.com/uibcdf/pharmacophoremt) | Scientific component | Pharmacophore modeling |
| [ElastNetMT](https://github.com/uibcdf/elastnetmt) | Scientific component | Elastic-network modeling |
| [DockingMT](https://github.com/uibcdf/dockingmt) | Scientific component | Molecular docking workflows |

---

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

## 📦 Installation

Installation concerns the implemented software above, not every concept in Architecture
1.0. Components may be installed individually using their repository instructions. To
get the suite environment including JupyterLab:

```bash
conda install molsyssuite -c uibcdf -c conda-forge
```

Or for the latest development version:

```bash
conda install molsyssuite-dev -c uibcdf -c conda-forge
```
