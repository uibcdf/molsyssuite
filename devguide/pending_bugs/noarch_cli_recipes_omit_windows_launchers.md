---
summary: Noarch Conda recipes can omit launchers declared by Python project metadata.
issue: uibcdf/molsyssuite#47
status: partial
opened: 2026-09-24
closed:
severity: medium
verification: inspected
area: [distribution, conda, tooling]
guard: tests/test_governance.py::RepositoryConformanceTests::test_noarch_recipe_requires_every_project_script_launcher
normative: devguide/python_distribution_policy.md
blocked_by: []
supersedes: []
---

# Noarch Conda recipes omit Windows launchers

**Reported:** 2026-09-24 after an installed SMonitor command was absent on Windows.
**Status:** Partial. The shared guard is published and actual frozen callers
already enforce it. DepDigest and MolSysViewer owner repairs are closed;
MolSysViewer's exact public Windows launchers are independently verified.
DepDigest's exact public 0.13.0 file now has independently verified installed
`--help` in all twelve original Linux/macOS/Windows Python 3.11–3.14 cells.
SMonitor's exact public command receiving and Viewer's remaining Linux/macOS
command evidence remain incomplete before central closure.

## What

Some members declare console commands in `pyproject.toml` but omit corresponding
`build.entry_points` from their `noarch: python` Conda recipes. Conda therefore does
not create the Windows command launchers. A Linux-only recipe `test.commands` step can
pass despite this defect.

## How

The central repository checker compares every `[project.scripts]` name and callable
target with the recipe's `build.entry_points` list for members with a noarch Python
recipe. It rejects missing, extra, duplicate and target-mismatched entries. Member
recipes then adopt the missing entries and prove each command from an installed Conda
artifact on every claimed platform.

## Why

Users installing a published package on Windows can receive a successful installation
without its advertised command. A source checkout, pip install or Linux build test does
not establish that the Conda launcher exists on Windows.

## What is measured and what is assumed

On 2026-09-26, the current SMonitor recipe already declared its `smonitor` launcher.
DepDigest's published `origin/main` recipe omitted `depdigest`; MolSysViewer's current
recipe omitted `molsysviewer`, `molsysviewer-qt`, and `molsysviewer-server`. Their
`pyproject.toml` files declared those commands. This is source inspection, not a new
Windows installed-artifact run. The original Windows failure and package metadata are
recorded in the owning issue.

On 2026-09-26, MolSysSuite commit `1289da1` published the checker and distribution
rule directly to `main`. DepDigest commit `34d8e76` published its recipe and staged
install gate directly to `main`. MolSysViewer commit `62a0dcce` published only the
issue-backed developer-guide report; its recipe and Windows gate remain on
`uibcdf/molsysviewer#101` for its developers to resolve. At that point, these
source changes alone did not establish a repaired public Conda artifact.

DepDigest `0.11.1-py_0` from commit `456ae6b7bcce1402c6504e2cf74d3721f2dcd39e`
passed the [staged producer run](https://github.com/uibcdf/depdigest/actions/runs/36229720222)
and [12/12 clean installed-package cells](https://github.com/uibcdf/depdigest/actions/runs/36229868929),
including Windows/Python 3.11–3.14. Annotated tag `0.11.1` and a stable GitHub
Release identify that SHA. [Promotion run `36230598357`](https://github.com/uibcdf/depdigest/actions/runs/36230598357)
added `main` to the same file with SHA-256
`bc54290422dc8af90d7d9f75f64fc12ece6b5da78e04dc66a3b7ddf2882799fa`.
An independent Anaconda query found one file with `staging` and `main` labels
and that digest. A fresh Linux/Python 3.13 public-channel installation
verified the exact record and ran the installed `depdigest --help` command.
`uibcdf/depdigest#19` closed after its permanent report and guard were published.

## Alternatives and refuted paths

Checking only `test.commands` was rejected because Linux build tests can run commands
that Conda does not install on Windows. Requiring a noarch recipe from every Python
member was rejected because some members have not reached first Conda publication.
Matching command names alone was rejected because a launcher can target the wrong
callable.

## Scope and exclusions

The shared guard applies to registered Python package members with a noarch Python
recipe under `devtools/conda-build/meta.yaml`. Platform-specific builds and members
without a recipe are outside this rule. Installed-artifact evidence and release
coordinates remain member-owned.

## Acceptance criteria

- The suite distribution profile states the noarch console-command contract and its
  tracked, expiring exception path.
- The shared checker rejects missing, extra, duplicate and wrong-target launchers.
- DepDigest and MolSysViewer recipes adopt their declared scripts, with local guards.
- Each affected member verifies the installed commands on every claimed platform,
  including Windows where claimed, before claiming the public package is repaired.
- The shared policy release and caller adoption are coordinated without breaking
  unrelated member checks.

## Local implementation issues

- `uibcdf/smonitor#26` — original SMonitor repair; its current recipe has the entry.
- `uibcdf/depdigest#19` — resolved; public build `0.11.1-py_0` verified.
- `uibcdf/molsysviewer#101` — three MolSysViewer launchers and installed evidence.

## Dependencies and risks

No upload or rebuild is needed to implement the checker or inspect existing
evidence. Viewer's original missing-launcher file is historical: the additive
public 0.24.0-py_1 repair is verified on Windows below. The current frozen
callers already enforce recipe parity; no new policy tag is needed for this
receiving review. Missing platform command execution remains distinct from
source recipe repair and installed launcher existence.

## Provenance

Inspected clean or preserved sibling checkouts after `suite_status.py` fetched their
remotes on host `nauta`, Python 3.13.14, 2026-09-26. DepDigest's local branch was
15 commits behind `origin/main`, so its published recipe was read with `git show`.

## 2026-10-01 historical public Viewer artifact

Read-only consumer verification run 36860171883 independently verified the
main label, solver index and exact digest of public Viewer 0.23.4-py_5. Its
separate Windows installed-launcher job failed with `ValueError: Missing
installed launcher: molsysviewer`. This is fresh installed-artifact evidence for
uibcdf/molsysviewer#101, not a failure of the common public verifier (#48).
The overall workflow remains failure. Source recipe changes alone do not repair
that immutable historical artifact; a component-owned additive repair remains.

## Receiving checkpoint — 2026-10-08

`uibcdf/molsysviewer#101` is closed with an additive public repair:
`molsysviewer-0.24.0-py_1.tar.bz2`, SHA-256
`e31dfb114ab2e49f22b372992d0201455b91849f2631d0165b802069e13abeaa`,
source `1a4c97a58b68b69f3a836546c9e4ac6187c3efa2`.
Independent native verification of
[37693319370](https://github.com/uibcdf/molsysviewer/actions/runs/37693319370)
checks its exact source/workflow/event/attempt, both required jobs and executed
steps. The public receipt's original artifact ZIP digest is verified before
reading its main-label, solver-index and exact-file result. The Windows/Python
3.13 job installs those exact bytes and runs all three advertised commands with
`--help` outside the checkout. This does not certify GUI/browser behavior.

Current source recipes match project scripts for SMonitor, DepDigest and
MolSysViewer. Their actual frozen callers (`policy-v1.5.4`, `policy-v1.5.4`,
`policy-v1.5.7`, respectively) already contain the shared entry-point guard;
no policy repin is required. Six central noarch recipe regression cases pass.
The historical missing-launcher artifact remains historical; it is not replaced.

The Windows proof does not certify installed command execution on Linux/macOS.
The broader platform acceptance above remains explicit, so #47 stays partial.
No new component suite or installed matrix was dispatched. Receipt:
[noarch_launcher_receiving_47_20261008.json](../rollouts/noarch_launcher_receiving_47_20261008.json).


## DepDigest installed-command reconciliation — 2026-10-08

Independent native review of original producer source
`df771e00e886fd9b12915adf54c1bd75c4b5476c` and
[installed run 37194436139](https://github.com/uibcdf/depdigest/actions/runs/37194436139)
verifies the current attempt, exact source/workflow/event, all thirteen jobs and
all mandatory executed producer/install/verification steps. All twelve
Linux/macOS/Windows Python 3.11–3.14 cells actually call the original
`verify_staged_install.py installed` operation outside the source checkout.

Source review of that exact operation proves that it verifies the installed
Conda coordinate/digest and runtime import prefix before unconditionally calling
`verify_launcher(prefix)`. That function resolves the actual `depdigest` launcher
inside the installed environment, executes `[launcher, "--help"]` as an argument
list with a timeout and requires exit zero. The successful step is consequently
command execution evidence, not merely command existence or generic suite success.
Workflow and helper source digests are retained in the receiving receipt.

The independently queried current public label and solver index identify the
same original file `depdigest-0.13.0-py_0.tar.bz2`, SHA-256
`e011d725c8a831ae46cd6b8d114185d04248e32b4d6701c70f988d19cc69f67b`.
No package or tests were reexecuted, and no current-source/architecture promise
is inferred from the historical macos-latest routing. This completes DepDigest's
claimed-platform command-evidence contribution to #47, without reopening its
closed local defect or changing its publication gates.

## SMonitor remaining receiving boundary — 2026-10-08

The original source `f604b940ab281df4554869fdd24f796ea6d42c27` and
[producer run 37520722817](https://github.com/uibcdf/smonitor/actions/runs/37520722817)
independently verify both jobs and the mandatory staged build and Windows
installed-command steps. The Windows job installs the named uploaded coordinate
and executes `smonitor --help`. Its script does not directly check the installed
digest/import prefix. The separate generic installed matrix verifies exact
provenance and launcher existence; it does not execute that command's help.
Those two claims are retained separately rather than silently upgrading the
Windows smoke to an exact digest-bound command receipt.

Current public registry/index still verifies `smonitor-0.19.0-py_1.tar.bz2`,
SHA-256 `4b876b4993b1e2caeed40851402a931f3b245ed7c1916d9483d81bc90274e31c`.
A recipe's Linux build command and an installed launcher-existence check do not
supply the missing Linux/macOS installed help evidence. No SMonitor command
failure is reproduced by this audit; the gap is receiving evidence.

### Accepted next bounded operation — implementation pending hosted receiving

The principal maintainer accepted an optional shared receiving operation to
install the **existing public file** in disposable hosted environments and verify its exact digest, Conda
record, distribution/launcher origins, actual platform/interpreter and each
advertised `--help` exit status outside source. Begin with SMonitor's Linux,
macOS arm64 and Windows commands on Python 3.14. This provides the remaining
claimed-platform command evidence, not a new full Python-minor scientific matrix.

The operation would use existing coordinate/public verification and installation
primitives where their contracts apply, with its own reusable command-receiving
contract and negative checks. No candidate build, package reconstruction, upload,
promotion, new publication permission, consumer pin rollout or scientific suite
would follow. Existing full installed/scientific release gates must continue to
reject command-only receipts. The alternative owner handoff was not selected. Implementation and hosted
receiving retain separate evidence; tool availability alone does not complete
the missing command qualification. The accepted operation is documented in
[public noarch command receiving](../public_noarch_commands.md).

[Exact native/source/public receiving receipt](../rollouts/noarch_commands_receiving_47_20261008.json).
#47 remains partial; Viewer scientific/browser suites retain their deferral.

Implementation guards execute twelve focused cases, including actual synthetic
launcher outcomes, exact byte/origin refusal and command-only rejection by the
existing full installed-matrix verifier. Existing installed/scientific SDK
operations and consumer pins remain unchanged. Advance notice is delivered to
the three original CLI owners; no source adoption or runtime migration is
requested by this central pilot.
