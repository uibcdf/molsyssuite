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
python devtools/scripts/development_environment.py toolchain
```

Use an explicit prefix if needed and activate the same path. Bootstrap inspection
of the recipe/source inventory can precede environment creation; development tests
run only after selecting the verified 3.14 interpreter. Do not presume a named
environment exists on every host or alter an unrelated active environment.

The recipe uses public `uibcdf` and `conda-forge` packages and the coherent official
Qt 6.11.2 family. It supplies Git, Python build backends and the Conda-forge
Rust/Cargo toolchain with GCC, binutils and Linux sysroot. The Rust activation
package allows `>=1.97.1,<2`; its matching compiler/library dependencies are
resolved by Conda. Activate the environment before building. The `toolchain`
operation verifies prefix/package provenance and compiles and runs C/Rust smoke
programs before any clone installation. Dependencies require no pip bootstrap
or external rustup. For an existing environment, follow the update/reactivation
commands in the environment instructions. Follow
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

For a complete local refresh, including MolI auxiliary Python packages, use:

```bash
python devtools/scripts/development_environment.py reinstall --dry-run
python devtools/scripts/development_environment.py reinstall
```

This opt-in operation derives every installable suite member from `suite.toml`
and the direct Python packages from the local MolI registry. It includes TopoMT
for local reinstallation without expanding the qualified integration cohort;
all selected sources must admit Python 3.14. The command reuses native-toolchain
verification and the batch installer, runs `pip check` and reports versions.
It preserves source revisions, local work and tags; explicit exclusions are
recorded. See the [refresh and Git-version instructions](../devtools/conda-envs/README.md#refresh-every-local-editable-installation)
for alternate workspaces, registry paths and generated-version behavior.

Publishing a new tag does not update installed metadata or a versioningit
generated `_version.py`. Reinstall after the tag is available locally; restart
existing Python processes to refresh cached version values and native code.

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

On 2026-10-22, closed [uibcdf/moli#40](https://github.com/uibcdf/moli/issues/40)
supplies the previously missing joint direct-component receiving: fourteen suite
snapshots plus Sabueso, Praxis and Recorda in one fresh Linux x86_64/Python
3.14.8 environment. The owner verifies editable/neutral-directory imports,
clean closure before and after tests and official Qt 6.11.2. Its selected
operations pass 371 cases (19 handoff, seven Praxis integration/real-MolSysMT/
quantity, 345 Recorda), with zero failures/skips.

The [central receiving receipt](rollouts/joint_workspace_82_20261022.json)
independently checks all seventeen source/metadata identities, unchanged
recipe/probe, 389 Conda input identities, published test-plugin bytes and retained
normalized result consistency. Runtime/native-file/test execution and original
JSONL/JUnit verification remain owner measurements; central did not repeat
science or replay the retired originals. Qualification applies to the recorded
sources, not later primary heads or public artifacts. At that receiving
checkpoint, the caller's twelve findings remained separate from the clean
disposable environment. The later authorized
[Diego host refresh](rollouts/local_workspace_refresh_82_20261022.json)
fast-forwards and reinstalls only Recorda/Praxis, resolving their five stale
ceilings and leaving seven existing external findings. Both neutral-directory
editable origins verify; published pytest-receptor records 345 Recorda and
156 Praxis local passes without failures/skips. The real-MolSysMT module is
explicitly excluded. Editable support providers and primary receptor installs
are preserved; these local results do not replace public-file qualification.
Optional beartype and visible GUI/browser behavior are not qualified.

The later [TopoMT assessment](rollouts/topomt_development_review_82_20261022.json)
checks published `8b2a30e` in a disposable venv inheriting the named host's
existing dependencies. Editable origins, core requirements and eight selected
import/metadata tests pass without adding dependency findings. This is not a
fresh Conda solve or complete expanded-cohort receiving. Installing modifies
the tracked generated version file; restoring it reproduces a metadata/runtime
version mismatch. Existing scheduled CI still fails eight cells, including two
Linux import steps. TopoMT remains outside the authorized profile; provenance
and qualification follow-up belongs to uibcdf/topomt#16. Coverage and scientific
deferrals remain unchanged, and no primary checkout or host install was altered.

| Scope | Current state | Owner / next condition |
| --- | --- | --- |
| Fourteen eligible Python members | Measured joint Linux editable/dependency/import integration | Their recorded source revisions; later source changes still need the probe |
| TopoMT | Outside the current authorized cohort; not a claim that its metadata excludes 3.14 | `uibcdf/topomt#16`, `uibcdf/molsyssuite#51`: review integration authorization and verify it in the shared environment |
| MolSys-AI umbrella | Registered repository without an installable Python package capability | No pip installation of the umbrella; subsystem packages retain their own ownership |
| Sabueso / Praxis / Recorda | Direct MOLI packages; joint seventeen-source receiving is complete for the fixed #40 cohort | Closed `uibcdf/moli#40`; later changed inputs need owner requalification. No suite membership/profile expansion. Recorda public delivery remains `uibcdf/recorda#26`. |

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
