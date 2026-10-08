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
