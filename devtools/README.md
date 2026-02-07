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

## 3. Developer Workflow

After creating and activating the `molsyssuite-dev` environment, you need to link your local clones of the suite's repositories.

### Using `molsys-dev-setup`

The `molsyssuite-dev` package installs a CLI tool called `molsys-dev-setup`. This tool automates the `pip install -e . --no-deps` command for all suite repositories.

**Usage:**

```bash
# 1. Activate the environment
conda activate molsys-dev

# 2. Run the setup (it searches in the current and parent directories by default)
molsys-dev-setup

# Optional: specify a path where your repositories are located
molsys-dev-setup ~/repos/uibcdf
```

---

## 4. Automation

Any changes to the recipes in `conda-build/` will trigger a GitHub Action to build and upload the new versions of the meta-packages to the `uibcdf` Anaconda channel.