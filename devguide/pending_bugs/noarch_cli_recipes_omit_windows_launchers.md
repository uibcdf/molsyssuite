---
summary: Noarch Conda recipes can omit launchers declared by Python project metadata.
issue: uibcdf/molsyssuite#47
status: active
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
**Status:** Active; DepDigest's public Conda repair is verified and its local
issue is closed. MolSysViewer's component fix belongs to its developers, and
the shared policy release and adoption remain pending.

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

No upload or rebuild is needed to implement the checker. MolSysViewer's
existing public Conda artifact still requires a new build coordinate and
independent installed-artifact evidence; its source recipe alone cannot repair
it. A new required shared policy tag must follow review of the affected
members and their caller compatibility.

## Provenance

Inspected clean or preserved sibling checkouts after `suite_status.py` fetched their
remotes on host `nauta`, Python 3.13.14, 2026-09-26. DepDigest's local branch was
15 commits behind `origin/main`, so its published recipe was read with `git show`.
