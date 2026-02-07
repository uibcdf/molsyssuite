# MolSysSuite Environment Management: Conda Meta-packages

To ensure reproducibility and streamline the onboarding process for the lab, we have adopted **Conda Meta-packages** on our Anaconda channel as the primary method for environment distribution, replacing static .yml files.

---

## 1. What are Meta-packages?
A meta-package is a Conda package that contains no source code itself but serves as a container for dependencies.
* **Atomic Installation:** Install the entire stack with a single command.
* **Version Control:** Ensures compatibility between internal packages (e.g., A, B, and C).
* **Entry Points:** Provides unified CLI commands for the lab.

---

## 2. Defined Meta-packages

### A. molsyssuite (Production/User)
Designed for end-users who need a stable environment to run simulations and analysis.
* **Content:** Core suite packages (e.g., PharmacophoreMT) and their **hard dependencies** (mandatory).
* **Goal:** A lightweight, reliable environment for daily research use.

### B. molsyssuite-dev (Development)
Designed for lab members contributing to the codebase.
* **Content:** All hard and **soft dependencies** (e.g., testing frameworks, documentation builders, optional scientific libraries).
* **Automation:** Includes a dedicated script to link local git repositories to the environment.

---

## 3. Entry Points

**Entry Points** are command-line aliases created by Conda during installation. They map a simple terminal command to a specific Python function within the package.

### Why we use them:
* **Abstraction:** Users don't need to know the internal file structure to run a tool.
* **Efficiency:** Instant access to utility scripts from any directory.
* **Automated Setup:** Specifically for developers, the molsys-dev-setup command automates the linking of local code.

**Example for molsyssuite-dev:**
The command molsys-dev-setup is included to scan the local workspace for suite repositories and install them in **editable mode**:

```bash
# Internal logic executed by the script:
pip install --no-deps --editable <path_to_local_repo>
```

---

## 4. Implementation Example (meta.yaml)

```yaml
package:
  name: molsyssuite-dev
  version: "2026.02.0"

requirements:
  run:
    - python >=3.12
    - numpy
    - rdkit
    - pytest       # Soft dependency (Testing)
    - sphinx       # Soft dependency (Documentation)
    - molsys-ai    # Core library

build:
  entry_points:
    - molsys-dev-setup = molsys_dev_tools.scripts:setup_editable_repos
```

---

## 5. Usage Workflow

### For General Users:
```bash
conda create -n molsys -c uibcdf molsyssuite
```

### For Developers:
```bash
# 1. Create the environment with all dependencies
conda create -n molsys-dev -c uibcdf molsyssuite-dev
conda activate molsys-dev

# 2. Automatically link your local repositories
molsys-dev-setup
```
