# Local development workspace

## Applicability and ownership

Routine Python development and local tests use Python 3.14 under the accepted
[Python policy](python_policy.md). For the eligible MolSysSuite cohort, the team's
default Linux x86_64 environment is `molsyssuite_dev@3.14`, created from
`devtools/conda-envs/molsyssuite-dev-py314.yaml`. MolSysSuite owns that recipe,
integration checks and member guidance under `uibcdf/molsyssuite#82`.

A development environment supplies dependencies; an editable installation
connects a local clone to its Python interpreter. It does not publish that clone
or certify a release. Member implementation and scientific qualification remain
component-owned. The Linux profile does not establish macOS or Windows evidence.

## Controlled name migration and future production profiles

Under #175, new suite development environments use `molsyssuite_dev@<python>`;
`<python>` is the actual major.minor. MolI owns `moli_dev@<python>`. Future
`molsyssuite@<python>` and `moli@<python>` production profiles require their own
runtime purposes, package/engine closure, clean install and reproducibility;
these names do not create a production environment or change metapackage names.
The [production-profile design](production_environment_profiles.md) records
purpose, installed artifact/engine closure, qualification and reproducibility
requirements, with implementation explicitly pending.

Preserve the existing `molsyssuite@uibcdf_3.14` prefix and its original receipts.
The #82 shared-prefix pause stays in force. Create a separate replacement from
the reviewed recipe; verify interpreter, native/docs tools, dependency closure,
editable and neutral-directory imports, then check selected notebooks and kernel
interpreter paths before choosing it for work. Audit current hardcoded commands,
paths and kernels; retain historical identities. Do not rename/remove a live
prefix, reuse stale qualification under the new name, or silently reinstall
primary component sources. The legacy prefix remains a transitional route only
for its already recorded scope until an owner authorizes its verified replacement.

The recipe supplies `sphinxcontrib-plantuml`, PlantUML, Java and Graphviz.
`python devtools/scripts/development_environment.py documentation` builds a real
class diagram with prefix-owned tools and checks its SVG. Importing the Python
extension alone does not qualify rendering or the full TopoMT documentation.
MolI #94 owns the corresponding platform naming/design handoff.

## Create and verify the environment

From the MolSysSuite clone, with Conda available:

```bash
conda env create --file devtools/conda-envs/molsyssuite-dev-py314.yaml
conda activate 'molsyssuite_dev@3.14'
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
| Previously qualified fourteen Python members | Measured joint Linux editable/dependency/import integration | Their recorded source revisions; later source changes still need the probe |
| PeptideMT | Authorized; fresh fifteen-member Linux/Python 3.14.10 editable/dependency/import integration passed | `uibcdf/peptidemt#1`, `uibcdf/molsyssuite#146`; [exact sources and scope](rollouts/peptidemt_w0_receiving_146_20261027.json), run 40579262099 |
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


## Current caller refresh — 2026-10-30

The authorized local Recorda/Praxis refresh now installs their clean source
editables as 0.3.3/0.1.1 in `molsyssuite@uibcdf_3.14` (Python 3.14.7).
Isolated-process origins and direct requirements pass; the existing four support
provider versions are unchanged. Five obsolete consumer-ceiling conflicts are
resolved. Seven inherited AmberTools findings still fail `pip check`, so this
caller is not a clean jointly qualified prefix. No other clone, dependency or
scientific suite is changed. [Exact scope and receipt](rollouts/caller_recorda_praxis_refresh_135_20261030.json)
and central #82 retains the actual remaining environment/integration ownership.


The central reinstall enhancement #135 is complete, with its
[archived acceptance review](archive/batch_reinstall_suite_and_moli_auxiliaries.md)
and [current read-only nineteen-source receipt](rollouts/workspace_reinstall_closeout_135_82_20261102.json).
The command remains opt-in and propagates closure failures. Its completion does
not require or imply changing every active clone or certifying this caller prefix.
All seven current declared-requirement findings originate in metadata owned by
AmberTools 26.0, outside the canonical 3.14 recipe. Keep them visible under #82
while preserving the existing environment; external provider correction and
component scientific qualification remain independently owned work.


## Qualified clean alternative — 2026-11-02

A separate prefix created from the unchanged recipe now verifies 405 public
Conda packages, Python 3.14.10, Rust 1.99.1 and official Qt 6.11.2. The existing
operators install and check all fifteen authorized suite snapshots, then the
joint eighteen-source set with Sabueso, Praxis and Recorda. Actual dependency
closure is clean before/after both steps. Python isolated mode verifies every
editable origin and exposed version; the maintained runtime verifier accepts all
eighteen. Both declared Rust extensions load, one controlled receptor test passes
and GHR help succeeds. No scientific, model or GUI/browser suite is executed.

[Normalized source/phase/retention receipt](rollouts/development_candidate_82_20261102.json)
and [dated base manifest](rollouts/development_candidate_82_20261102_base.explicit.txt)
retain the exact engineering scope. The manifest's 405 URL/SHA-256 tuples match
native Conda records and an offline replay dry run; editable source overlays
are separate inputs. This reproduction snapshot is not a new global version pin.
The moving canonical recipe remains unchanged.

The candidate uses independent frozen source copies, so it does not follow
edits to the live primary clones. Its prefix and copies are retained together
for the explicit #82 adoption decision; obsolete owned build caches have been
removed and retained runtime checks pass. The original named environment stays
active and unchanged with its seven findings. A routine-work migration requires
a deliberate prefix/source-relinking review that preserves dirty work; none is
performed automatically. TopoMT authorization, member science/release receiving
and other platform/minor claims retain their existing owners.

The [prepared adoption plan](pending_proposals/default_python_314_editable_workspace.md#controlled-adoption-plan--2026-11-03)
retains the requested routine name `molsyssuite@uibcdf_3.14`. It separates
owner-reviewed source selection, isolated qualification, recovery preparation
and a coordinated switch. It does not authorize replacement of the live prefix.
In-place editable native builds can replace binaries inside a shared clone;
activating another prefix or setting `CARGO_TARGET_DIR` alone does not isolate
that final extension. Keep the qualified candidate and its source copies
available until the adoption or retirement decision.

## Current published-source receiving — 2026-11-03

After the maintainer accepted the published-source route, a second independent
candidate replays the same 405-package Conda base in a fresh prefix. Every native
URL/SHA-256 tuple matches the accepted dated manifest; package files are copied
rather than hard-linked. There is no new dependency solve or unlink transaction.
The source copies bind refreshed published `origin/main` commits for the fifteen
eligible suite packages and Sabueso/Praxis/Recorda. Local unpublished work is not
copied. Five public inputs differ from the first candidate: MolSysMT,
MolSysViewer, PharmacophoreMT, DockingMT and Sabueso.

One actual maintained joint reinstall uses `--no-deps --no-build-isolation` and
explicit TopoMT exclusion. Its built-in native-toolchain checks pass, as do
base/post-install dependency closure, eighteen neutral editable/version checks,
the maintained eighteen-source Qt/runtime verifier, both declared native imports,
one receptor dummy test and installed GHR help. All eighteen copied source trees
are clean after building. Fresh controls still pass after owned Cargo/pip/npm/temp
cache retirement; native extension hashes remain unchanged.
[Exact source/base/result/retention receipt](rollouts/development_current_sources_82_20261103.json).

The original named Python 3.14.7 environment retains its 568-record fingerprint
and the same seven findings in the before/after comparison. Primary native binary
hashes match; Sabueso's owner work changes its primary state concurrently and is
preserved. The previous reference candidate remains separate. The new owner root
basename is `molsyssuite-82-current-hn_lov2l`, alongside the host Conda installation;
its `prefix/` and independent `sources/` stay together for adoption review.
This receiving qualifies installation/basic runtime for those snapshots only.
It does not update primary clones, switch the routine interpreter, execute member
scientific/GUI/model tests, change public admission or resolve TopoMT eligibility.
Next #82 work is the controlled source/window/recovery decision, not a blind
installation of the tested commits into colleagues' working clones.

## Preliminary recovery copy; pause deferred — 2026-11-03

The maintainer selected preparing the backup now and coordinating the pause
later. A private POSIX/PAX archive covers the original named prefix:
13,070,366,720 bytes and 139,769 members, with successful native post-write
verification and a recorded SHA-256. A separate owned archive restore rehearsal
passes at its original fixture path, preserving bytes, permissions, ownership,
timestamps, symlinks, hardlinks and extended attributes. Actual routine-prefix
restoration is unexecuted. The selected declared generated version/native and
egg-info outputs remain separate; sixteen regular-output digests match.
[Bounded recovery/cleanup receipt](rollouts/development_recovery_82_20261103.json).

The original prefix remains active. Advisory process inspection finds Node/Codex
sessions executing from it; the clean suite candidate has no `codex` launcher.
Resolve this host's tool continuity and use an external administrative process
for future replacement after coordinating users. The verified base Python helper
outside that prefix is for filesystem recovery only; routine Python 3.14 and
the requested environment name retain their standing scope.

The protected owner root basename is `molsyssuite-82-recovery-wrcq3p0m`, alongside
the host Conda installation. Retain its private archive, selected generated outputs
and useful manifests/proof for the next #82 decision. The partial file-tree copy,
obsolete scripts/logs/cache and four `/tmp` scripts are retired after review.
This is a live preliminary copy, not a coordinated atomic/quiescent snapshot or
a whole primary-source backup. Refresh/verify it and the source/generated inputs
during the actual pause before replacement; preserve later human changes.
