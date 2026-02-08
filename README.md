# MolSysSuite

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/downloads/)
[![UIBCDF](https://img.shields.io/badge/UIBCDF-Lab-red.svg)](http://uibcdf.org)

## 💊 Mission

In **Drug Design**, the ability to rapidly prototype, visualize, and analyze complex molecular interactions is crucial. **MolSysSuite** provides a reproducible and interoperable framework that scales from local Jupyter experimentation to high-throughput autonomous pipelines, ensuring that the physics and the data remain consistent across the entire workflow.

It handles molecular systems through a modular, "agent-first" architecture that addresses common challenges in scientific Python—such as fragmentation, heavy dependencies, and inconsistent units—by decoupling infrastructure from domain-specific tools. The suite is optimized for interactive analysis in **Jupyter Notebooks** and is designed to be natively consumed by **AI Agents**, providing the necessary introspective metadata and structured diagnostics for autonomous experimentation.

---

## 🏗️ The Ecosystem

MolSysSuite is built on a layered architecture where each component serves a specific purpose, from low-level infrastructure to high-level analysis and intelligence.

### [MolSysMT](https://github.com/uibcdf/molsysmt) — "The Core"
The orchestrating heart of the suite: a molecular manipulation and analysis library that acts as a **universal translator**. It unifies the fragmented molecular dynamics ecosystem, allowing users to convert and operate models from MDAnalysis, MDTraj, or OpenMM with a single, consistent syntax.

### [PyUnitWizard](https://github.com/uibcdf/pyunitwizard) — "The Physics Bridge"
An essential component that solves the eternal problem of physical units in Python. It acts as an **agnostic adapter** between libraries (Pint, OpenMM.unit, Unyt), ensuring that magnitudes are always correct and compatible. Its lightweight design makes it critical for real interoperability.

### [ArgDigest](https://github.com/uibcdf/argdigest) — "The Gatekeeper"
An advanced argument auditing and normalization tool that **professionalizes scientific APIs**. By separating validation logic from business code, it protects functions from incorrect inputs and enables AI agents to understand how to use the libraries through introspection.

### [DepDigest](https://github.com/uibcdf/depdigest) — "The Optimizer"
The intelligent solution to **"bloat" in scientific software**. It manages optional dependencies via lazy loading, allowing MolSysSuite to integrate dozens of heavy external libraries without penalizing startup time or memory until the functionality is actually required.

### [SMonitor](https://github.com/uibcdf/smonitor) — "The Black Box"
A centralized **telemetry and diagnostic system** that standardizes error and event communication. It structures logs and exceptions for both humans and machines, providing unique error codes and rich context for rapid debugging and agent self-correction.

### [Sabueso](https://github.com/uibcdf/sabueso) — "The Bloodhound"
A sophisticated **biomolecular knowledge aggregator** that tracks and normalizes data from public databases (UniProt, PDB, ChEMBL, PubChem). Its engine generates structured **Cards** with a rigorous **evidence tracking** system, ensuring every biological property in your drug design workflows has a clear and auditable provenance.

### [MolSysViewer](https://github.com/uibcdf/molsysviewer) — "The Lens"
A modern, lightweight **molecular visualizer** designed for the Jupyter ecosystem. Built on standard web technologies (Mol*), it offers high-quality 3D visualization that integrates natively into analysis workflows as an independent widget.

### [TopoMT](https://github.com/uibcdf/topomt) — "The Cartographer"
Specialized in the **topographic and geometric analysis** of molecular surfaces. It provides advanced tools to detect and characterize cavities, pockets, and tunnels, enabling a deep understanding of the structural features that govern molecular recognition and transport.

### [ElasNetMT](https://github.com/uibcdf/elasnetmt) — "The Resonator"
Dedicated to **Elastic Network Models (ENM)** and large-scale protein dynamics. It bridges the gap between static structures and functional movements by computing normal modes and fluctuations, helping identify the essential flexibility of biological macromolecules.

### [MolSys-AI](https://github.com/uibcdf/molsys-ai) — "The Brain"
A vanguard component bridging the gap between **LLMs and scientific software**. More than a chatbot, it provides the infrastructure (RAG server, agent API) that allows autonomous assistants to design and execute computational experiments using the entire suite.

---

## 📦 Installation

The suite can be installed as a whole or as individual components. To get the production-ready suite including JupyterLab:

```bash
conda install molsyssuite -c uibcdf -c conda-forge
```

Or for the latest development version:

```bash
conda install molsyssuite-dev -c uibcdf -c conda-forge
```