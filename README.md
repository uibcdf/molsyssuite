# MolSysSuite

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/downloads/)
[![Governance tests](https://github.com/uibcdf/molsyssuite/actions/workflows/validate_governance.yaml/badge.svg?branch=main)](https://github.com/uibcdf/molsyssuite/actions/workflows/validate_governance.yaml)
[![Codecov](https://codecov.io/gh/uibcdf/molsyssuite/branch/main/graph/badge.svg)](https://app.codecov.io/gh/uibcdf/molsyssuite)
[![UIBCDF](https://img.shields.io/badge/UIBCDF-Lab-red.svg)](http://uibcdf.org)

MolSysSuite is the **molecular modeling ecosystem and a first-class component of the MOLI platform**. Its components provide molecular-system representation, interoperability, computation, analysis, and visualization, supported by reusable scientific Python libraries and developer tools.

Coverage measures `devtools/scripts` in the parent process of the existing
Linux/Python 3.13 test lane. Child process
coverage is not combined. The badge shows the last accepted `main` report and
can lag lightweight or `[skip ci]` pushes; it does not establish coverage of later
commits or scientific consumer suites. See the [coverage reporting contract](devguide/repository_badges.md#central-administrative-coverage-producer).

## Relationship to MOLI

[MOLI Platform Architecture 1.0](https://github.com/uibcdf/moli/blob/main/architecture_1.0/README.md) defines the platform umbrella and its cross-component contracts. MOLI governs MolSysSuite as a platform component.

MolSysSuite has **delegated internal governance**: this repository is the normative owner of its members' engineering and modeling policies, registry, admission, rollouts and collective validation.

```text
MOLI
  └── MolSysSuite              MOLI component
        │
        ├── owns member engineering baseline
        ├── owns modeling-domain governance
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

A MolSysSuite member follows **MolSysSuite member governance + repository-local rules**. MolSysSuite as a unit remains bound by its platform contracts with MOLI.

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
| [OpenCASTp](https://github.com/uibcdf/opencastp) | Support library (auxiliary, incubating) | Independent local CASTp numerical reconstruction in development |
| [Pytest Receptor](https://github.com/uibcdf/pytest-receptor) | Developer tool | Compact pytest evidence reports |
| [GH Run Receptor](https://github.com/uibcdf/gh-run-receptor) | Developer tool | GitHub Actions run inspection |
| [Lindelint](https://github.com/uibcdf/lindelint) | Developer tool (auxiliary) | Interpolation support developed for ElastNetMT |
| [MolSys-AI](https://github.com/uibcdf/molsys-ai) | Specialist subsystem | AI subsystem specialized in understanding and operating MolSysSuite |

The stable member Python baseline, transitions and admission state are recorded in `suite.toml` and decided by MolSysSuite.

## Governance

Shared modeling-domain work is proposed and tracked in the [MolSysSuite issue board](https://github.com/uibcdf/molsyssuite/issues). Component-local implementation remains in the owning repository. Contracts between MolSysSuite as a component and other MOLI components belong to MOLI governance.

The [`devguide/`](devguide/README.md) records suite-domain decisions, rollout state, collective evidence, and long-lived technical guidance. [`MOLSYSSUITE_GUIDE.md`](MOLSYSSUITE_GUIDE.md) is synchronized into members.

`suite.toml` and the [MolSysSuite policies](devguide/README.md) are the source of member rules. Values may initially match MOLI's direct-component policies; changing a MOLI policy does not silently change a member rule.

## Installing components

Choose the components you need from the registered list and follow their own installation instructions. This repository coordinates the modeling ecosystem; it is not a substitute for its packages.

For opt-in development with Python 3.14 and local component checkouts, see the
[central Conda environment recipe and editable-install guide](devtools/conda-envs/README.md).
This environment is not a suite-wide Python 3.14 support claim.
