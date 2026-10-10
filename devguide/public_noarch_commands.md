# Receiving commands from an existing public noarch file

This optional MolSysSuite operation belongs to
[uibcdf/molsyssuite#47](https://github.com/uibcdf/molsyssuite/issues/47).
It fills missing installed console-command evidence for an **existing public
file**, without rebuilding it or executing scientific tests. Command receiving
does not establish full installed-suite qualification, Python admission, GUI
behavior or publication permission.

## Inputs and supported profile

Select an exact public UIBCDF package/version/noarch/filename/SHA-256 coordinate.
The bounded archive profile is `noarch: python`, `py_N.tar.bz2`, with explicit
console commands in `info/link.json`. The file must already have the public
`main` label and be solver-visible with the expected digest. Native builds,
`.conda` archives and files without console commands need another reviewed
profile; they are not silently converted.

The optional reusable/manual workflow
`.github/workflows/verify-public-noarch-commands.yaml` takes `package`, `version`,
`filename`, `sha256`, a JSON `platforms` list and a selected `python` minor.
Platforms are `linux-64`/Ubuntu, `osx-arm64`/macos-15 and `win-64`/Windows;
Python is 3.11–3.14, default 3.14. Select only the member's claimed platforms
and minors. One selected minor is not evidence for the other minors. Pin the
workflow to the immutable implementation commit when calling it externally.

## What executes

`devtools/scripts/public_noarch_commands.py` exposes independently reusable
`matrix`, `inspect_archive`, `verify_cell`, `verify_commands` and `receive`
operations. It reuses the existing public coordinate/index verifier,
digest-checking downloader and native Conda command resolver. The existing
scientific installer and publication workflows are unchanged.

Each receiving cell:

1. Rejects a wrong explicit active prefix, interpreter, platform or source
   working directory before installation.
2. Verifies the exact public label/index and downloads digest-matching bytes
   into a private temporary directory; archive metadata is read without
   extraction. Embedded identity, noarch type, dependencies and unique command
   targets must agree.
3. Solves the archive's declared dependencies using only ordinary public
   `uibcdf`, then `conda-forge`, with strict priority; installs the exact public
   URL. It neither enables staging for dependency solving nor invokes a build.
4. Verifies the installed Conda file URL/digest, distribution version/console
   metadata, launcher prefix and imported command-module origin/bytes.
5. Executes every declared console launcher with the literal argument `--help`,
   outside source, without a command shell or inherited Python source paths.
   Each must exit zero within 30 seconds; retained stdout/stderr evidence is
   size and digest, with a 64 KiB limit per stream after execution.

The workflow runs in disposable hosted environments. Local `receive` explicitly
installs into `--prefix`, which must be its current interpreter's `sys.prefix`.
Use a **separate disposable Conda environment**, never the shared development
environment. The environment belongs to the caller and is not deleted by the
tool. Downloads/output handles are tool-owned and close on success or failure;
the explicit output receipt belongs to the caller. Hosted job environments
remain under the runner's lifecycle. A failure does not promise environment
rollback or establish successful scientific recovery.

## Evidence and limits

The receipt is `molsyssuite.public-noarch-commands@1`. A verified receipt includes
the coordinate, actual platform/minor/prefix, exact installed record, command
target/origins, exit status and output digests. Handled failures exit nonzero
and retain `state=unverified`; bootstrap failures can leave no receipt. Pair
receipts with independently verified native run/attempt/source/job/step and
artifact ZIP identities. The original producer identity stays in its existing
release receipt; the new workflow source identifies the receiving tool, not a
new producer or rebuilt package.

Existing full installed-matrix verification rejects this workflow/title/job
inventory and requires its original scientific steps. A command-only receipt
cannot replace any release gate. No consumer pin migration, blanket dependency
upgrade or new mandatory push job follows from this optional tool.

Regression checks: `tests/test_public_noarch_commands.py`. They execute a real
synthetic help command and reject missing/foreign launchers, failed/timed-out
commands, wrong bytes/records/imports/metadata, unsafe archive dependencies and
wrong platform/prefix. They also protect temporary download cleanup and
rejection by the existing installed-matrix verifier. Actual platform receiving
remains separately recorded in #47.


## Qualified initial use

The immutable implementation is
`a64ae03761ef9107286319ce5c9be5bb2573ff57`. Its first actual receiving run
[37836714027](https://github.com/uibcdf/molsyssuite/actions/runs/37836714027)
verifies SMonitor 0.19.0 py_1 on the three supported platforms with Python 3.14.
The [receiving receipt](rollouts/noarch_commands_receiving_47_20261008.json)
retains native and original artifact identities. A caller can select those same
existing bytes explicitly:

```yaml
jobs:
  commands:
    uses: uibcdf/molsyssuite/.github/workflows/verify-public-noarch-commands.yaml@a64ae03761ef9107286319ce5c9be5bb2573ff57
    with:
      package: smonitor
      version: '0.19.0'
      filename: smonitor-0.19.0-py_1.tar.bz2
      sha256: 4b876b4993b1e2caeed40851402a931f3b245ed7c1916d9483d81bc90274e31c
      platforms: '["linux-64", "osx-arm64", "win-64"]'
      python: '3.14'
```

Choose the reviewed coordinate and claimed profile for the actual component.
The example requests command receiving; it does not prepare a release or grant
publication permission. There is no automatic consumer adoption.

## MolSysViewer receiving

[Run 38029890702](https://github.com/uibcdf/molsyssuite/actions/runs/38029890702)
verifies all three commands from the existing public
`molsysviewer-0.24.0-py_1.tar.bz2` on Linux and macOS arm64 with Python 3.14.
Its SHA-256 is
`e31dfb114ab2e49f22b372992d0201455b91849f2631d0165b802069e13abeaa`.
The [receiving receipt](rollouts/viewer_noarch_commands_receiving_47_20261010.json)
separates original producer identity from receiving source and retains both
native artifact ZIP identities and all six command results. The receiving
workflow and reviewed helpers are unchanged from the accepted implementation.
Prior Windows evidence uses these same public bytes on Python 3.13. This closes
the remaining platform-command gap in #47; GUI, scientific suites, other minors
and public-release qualification remain separate.
