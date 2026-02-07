# MolSysSuite Development Tools

This directory contains the tools and configurations for managing the MolSysSuite environments and distributing the suite via Conda meta-packages.

## 1. Directory Structure

*   `conda-envs/`: YAML files to create local Conda environments manually.
*   `conda-build/`: Conda-build recipes for the official meta-packages.
*   `scripts/`: Utility scripts, including the `molsys-dev-setup` tool.

---

## 2. Conda Meta-packages

To ensure reproducibility and streamline the onboarding process, we use **Conda Meta-packages** on the `uibcdf` Anaconda channel.

### A. molsyssuite (Production/User)
Designed for end-users who need a stable environment.
*   **Installation:** `conda create -n molsys -c uibcdf molsyssuite`
*   **Content:** Core suite packages (`molsysmt`, `molsysviewer`, etc.) and their mandatory dependencies.

### B. molsyssuite-dev (Development)
Designed for lab members contributing to the codebase.
*   **Installation:** `conda create -n molsys-dev -c uibcdf molsyssuite-dev`
*   **Content:** All third-party dependencies (testing, documentation, etc.) required for development, but *not* the suite libraries themselves (to allow local editable installs).

---

## 3. Setting up the Development Environment

You can create or update your development environment using the `molsyssuite-dev.yaml` file located in `devtools/conda-envs/`.

### A. Creating the environment from scratch
```bash
conda env create -n <env_name> -f devtools/conda-envs/molsyssuite-dev.yaml
```

### B. Updating an existing environment (from outside)
If the environment already exists, use the `update` command with `--prune` to keep it synchronized:
```bash
conda env update -n <env_name> -f devtools/conda-envs/molsyssuite-dev.yaml --prune
```

### C. Updating the environment (already activated)
If you are already inside the activated environment:
```bash
conda env update -f devtools/conda-envs/molsyssuite-dev.yaml --prune
```

---

## 4. Developer Workflow: Linking Local Repositories

After setting up the environment, you need to link your local clones of the suite's repositories (e.g., `molsysmt`, `molsysviewer`) in editable mode.

### Running the setup script

**Option 1: Using the CLI tool (Recommended once installed)**
Once the `molsyssuite-dev` meta-package is installed in your environment:
```bash
molsys-dev-setup ~/repos@uibcdf/
```

**Option 2: Running locally (Before the meta-package is published)**
If you are setting up the suite for the first time or the meta-package is not yet installed:
```bash
python devtools/scripts/molsys_dev_setup.py ~/repos@uibcdf/
```

> **Note:** Replace `~/repos@uibcdf/` with the actual path where your repository clones are located.

---

## 4. Automation

Any changes to the recipes in `conda-build/` will trigger a GitHub Action to build and upload the new versions of the meta-packages to the `uibcdf` Anaconda channel.