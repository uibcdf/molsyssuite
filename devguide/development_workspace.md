# Local development workspace

## Applicability and ownership

Routine Python development and local tests use Python 3.14 under the accepted
[Python policy](python_policy.md). For the eligible MolSysSuite cohort, the team's
default Linux x86_64 environment is `molsyssuite@uibcdf_3.14`, created from
`devtools/conda-envs/molsyssuite-dev-py314.yaml`. MolSysSuite owns that recipe,
integration checks and member guidance under `uibcdf/molsyssuite#82`.

A development environment supplies dependencies; an editable installation
connects a local clone to its Python interpreter. It does not publish that clone
or certify a release. Member implementation and scientific qualification remain
component-owned. The Linux profile does not establish macOS or Windows evidence.

## Create and verify the environment

From the MolSysSuite clone, with Conda available:

```bash
conda env create --file devtools/conda-envs/molsyssuite-dev-py314.yaml
conda activate 'molsyssuite@uibcdf_3.14'
python -c 'import sys; assert sys.version_info[:2] == (3, 14); print(sys.executable, sys.prefix)'
```

Use an explicit prefix if needed and activate the same path. Bootstrap inspection
of the recipe/source inventory can precede environment creation; development tests
run only after selecting the verified 3.14 interpreter. Do not presume a named
environment exists on every host or alter an unrelated active environment.

The recipe uses public `uibcdf` and `conda-forge` packages and the coherent official
Qt 6.11.2 family. It declares the in-environment build tools. MolSysMT also needs
a working Rust/Cargo toolchain; check `cargo --version` before installing. Follow
the [environment instructions](../devtools/conda-envs/README.md) for the historical
Qt rollback route; that route stays in a separate environment.

## Connect the participating local clones

Inspect each local clone's branch, commit and unrelated changes before deliberate
updates. Never update or replace a colleague's clone as a side effect of installing
it. The reusable `development_environment.py` operations select the complete
registry-derived cohort and reject missing or Python-incompatible sources:

```bash
python devtools/scripts/development_environment.py profile
python devtools/scripts/development_environment.py sources --workspace ..
python devtools/scripts/development_environment.py install --workspace ..
python devtools/scripts/development_environment.py runtime --workspace ..
```

These commands assume sibling local clones. `sources` inspects Git identity,
commit, dirty state and Python metadata without installing or updating them.
`install` uses the current Python interpreter with `--no-deps --no-build-isolation`
and one `--editable` entry per eligible source, then runs `python -m pip check`.
`runtime` verifies the actual source import origins, editable metadata and the
official Qt runtime. Receipts name the selected source revisions; editable builds
may generate version files, and dirty state stays visible.

For a single participating component, after provisioning its complete compatible
Conda dependency closure:

```bash
python -m pip install --no-deps --editable /absolute/path/to/local-clone
python -m pip check
```

Use `--no-build-isolation` when the component needs declared tools from that
environment for its native build. `--no-deps` prevents pip from silently replacing
the Conda dependency solution. `--editable` is the valid pip option.

Ordinary Python source edits are visible without reinstalling. Dependency or
metadata changes, entry points and compiled extensions can require deliberate
reinstallation or rebuilding. Verify imports from a neutral directory as well;
the current directory must not hide a different installed package.

## Run the selected tests

After activation and interpreter/dependency/import verification, run tests in the
owning component with the same interpreter:

```bash
python -m pytest --receptor=llm tests/path/to/relevant_tests.py
```

Select the relevant tests under the accepted [CI policy](python_ci_policy.md) and
component instructions. Full suites, GUI/display requirements and deferred
scientific checks retain their existing scope; source integration adds no full
suite to every internal push. Keep supported older minors in compatibility and
release matrices. A successful environment import is not an executed test suite.

## Current cohort, exclusions and cross-domain work

`development_environment.py profile` derives the cohort from `suite.toml`; use it
instead of keeping a second hardcoded installer list. On 2026-10-03 native
[run 37135810313](https://github.com/uibcdf/molsyssuite/actions/runs/37135810313)
created the public-channel environment, installed all fourteen eligible sources,
passed dependency closure and verified their actual editable origins and Qt on
Python 3.14.7. Exact source revisions and limits are in
`devguide/rollouts/development_workspace_82.json`.

On 2026-10-10, private-member access recovery under uibcdf/molsyssuite#102
qualified the fourteen current registered source revisions in a fresh public-
channel environment: [run 38036460703](https://github.com/uibcdf/molsyssuite/actions/runs/38036460703)
executes checkout, editable installation, dependency closure and source/official
Qt imports successfully on Linux/Python 3.14. Public receipts retain only actual
phase results and the fourteen immutable source identities; private metadata,
raw logs and source are not uploaded. The exact cohort and limits are in
`devguide/rollouts/private_member_audit_recovery_102_20261010.json`.
This fresh hosted result does not update a caller's existing environment or
clear its seven accepted dependency conflicts under #82; local import origins
and closure still require the checks above. No scientific or browser/GUI suite,
macOS/Windows qualification or public package admission is inferred.

| Scope | Current state | Owner / next condition |
| --- | --- | --- |
| Fourteen eligible Python members | Measured joint Linux editable/dependency/import integration | Their recorded source revisions; later source changes still need the probe |
| TopoMT | Outside the current authorized cohort; not a claim that its metadata excludes 3.14 | `uibcdf/topomt#16`, `uibcdf/molsyssuite#51`: review integration authorization and verify it in the shared environment |
| MolSys-AI umbrella | Registered repository without an installable Python package capability | No pip installation of the umbrella; subsystem packages retain their own ownership |
| Sabueso | Direct MOLI Python component, outside suite membership and this fourteen-member receipt | `uibcdf/moli#40`, `uibcdf/sabueso#109`: qualify its complete current dependency/import closure together with the suite sources |

The target is every participating installable member in a compatible shared
development session. A new source admission can change the planned cohort before
its integration probe succeeds; authorization and observed joint integration are
separate facts. The latest successful receipt qualifies only its recorded cohort
and revisions. A failure stays visible and belongs to the owning compatibility
issue; do not silently omit a source or relax its Python requirements.

A member not yet integrated uses its own compatible Conda/Python 3.14 environment
while tracking the affected member/operation, reason, owning issue, responsible
maintainer, interim controls, review/expiry date and exit condition. Any older
interpreter follows the bounded migration exception in the Python policy. A
new-member generated environment is a bootstrap, not joint integration evidence.

For Sabueso or another direct MOLI component, coordinate through its owner and
MOLI #40. Review the current source/dependency requirements before connecting it
to a shared environment; verify its editable origin and combined dependency
closure. Do not add it to `suite.toml` merely to share an environment, copy the
suite recipe into MOLI, or infer its inclusion from a guide update. Record exact
suite and external source revisions, any missing dependency/provider capability
and the actual integration outcome. A separately installed Sabueso environment
does not establish its joint compatibility with this cohort.

No editable profile, Conda solver result, guide copy or import receipt substitutes
for public artifact installation, full scientific execution or GUI qualification.
