# MolSysSuite

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/downloads/)
[![UIBCDF](https://img.shields.io/badge/UIBCDF-Lab-red.svg)](http://uibcdf.org)

MolSysSuite is the **molecular modeling ecosystem and a first-class component of the MOLI platform**. Its components provide molecular-system representation, interoperability, computation, analysis, and visualization, supported by reusable scientific Python libraries and developer tools.

## Relationship to MOLI

[MOLI Platform Architecture 1.0](https://github.com/uibcdf/moli/blob/main/architecture_1.0/README.md) defines the platform umbrella and owns platform-wide architecture, cross-component contracts, and the shared engineering baseline.

MolSysSuite has **delegated internal governance**: this repository governs its member registry, modeling-ecosystem contracts, component admission/classification, coordinated rollouts, collective validation, and domain-specific extensions.

```text
MOLI
  └── MolSysSuite              MOLI component
        │
        ├── inherits MOLI engineering baseline
        ├── adds modeling-domain governance
        │
        ├── MolSysMT
        ├── MolSysViewer
        ├── TopoMT
        ├── PharmacophoreMT
        ├── ElastNetMT
        ├── DockingMT
        ├── ...
        └── MolSys-AI
```

A MolSysSuite member therefore follows, as applicable: **MOLI engineering governance + MolSysSuite domain governance + repository-local rules**.

## Registered MolSysSuite components

The authoritative member registry is [`suite.toml`](suite.toml). Registration does not imply a stable public API.

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
| [MolSys-AI](https://github.com/uibcdf/molsys-ai) | Specialist subsystem | AI subsystem specialized in understanding and operating MolSysSuite |

The stable MOLI Python baseline is inherited by MolSysSuite. `suite.toml` additionally records member-specific transition/admission state and MolSysSuite rollout evidence.

## Governance

Shared modeling-domain work is proposed and tracked in the [MolSysSuite issue board](https://github.com/uibcdf/molsyssuite/issues). Component-local implementation remains in the owning repository. Contracts between MolSysSuite as a component and other MOLI components belong to MOLI governance.

The [`devguide/`](devguide/README.md) records suite-domain decisions, rollout state, collective evidence, and long-lived technical guidance. [`MOLSYSSUITE_GUIDE.md`](MOLSYSSUITE_GUIDE.md) is synchronized into members.

Engineering policies inherited from MOLI may have MolSysSuite **profiles** containing stricter domain requirements, transition machinery, historical inventories, or member-specific enforcement. Such profiles do not redefine the upstream MOLI baseline.

## Installing components

Choose the components you need from the registered list and follow their own installation instructions. This repository coordinates the modeling ecosystem; it is not a substitute for its packages.
