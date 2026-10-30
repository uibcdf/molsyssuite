---
summary: Diagnose the OpenCL unlink hook selecting the caller's active prefix.
issue: uibcdf/molsyssuite#139
status: partial
opened: 2026-10-24
closed:
severity: high
verification: reproduced
area: [development, tooling, resources]
guard:
normative: devguide/temporary_resources.md
blocked_by: []
supersedes: []
---

# Transaction prefix and active-prefix unlink hooks

**Reported:** PharmacophoreMT #64, original retirement on 2026-10-24.
**Status:** Central diagnosis and bounded mitigation evidence complete on
2026-10-30; the package hook correction remains upstream-owned. The principal
maintainer will commission work outside MolSysSuite. No external issue identity
is invented; add its real identity here when available. #139 remains partial.

## Original evidence

The immutable PharmacophoreMT source
`cca31420cecb64c21bfeeff735d02fa2e443e9ce` retains the original mixed hook-output/
JSON log. Its 48,749 compressed bytes have SHA-256
`bcdf730b9396784c9d74306df8a2ff22121e5a80830e599beb830fd1d57b38ad`;
the 360,242 decompressed bytes have SHA-256
`b49804e295e7d6d9f897ce7c5036913828db6c822c2385c7f903c7bcb09b5d8a`.
Both sizes/digests were independently checked before bounded decompression.

Native JSON reports success and 325 UNLINK entries. The original list includes
`ocl-icd-system` 1.0.0, build 1, public linux-64 archive SHA-256
`cb0ce5ce5ede1be2fd9edf88abd3ce3e6c2b7397c0283d623e4d8ccf96a1ed09`.
Its hook attempted to remove the active shared environment's OpenCL vendor file;
that file was absent. This is evidence of an attempted external mutation, not
successful deletion in the original shared environment. The later scoped-tree
retirement reported by PharmacophoreMT does not repair the native hook.

## Mechanism and ownership

The existing local package cache contains this one-line pre-unlink hook:

```sh
rm "${CONDA_PREFIX}"/etc/OpenCL/vendors/${PKG_NAME}|| true
```

Its SHA-256 is
`a865ed2329ab82391908f90b1df75fe9957b038849b4c3f4e7aa59174ae7d6d9`.
The [current feedstock hook](https://github.com/conda-forge/ocl-icd-system-feedstock/blob/eeb71dd886dddf614604b7761bf3f99536890c55/recipe/pre-unlink.sh)
uses the same active-prefix variable.

[Mamba 2.9.0's invocation](https://github.com/mamba-org/mamba/blob/2676ec2050f7dd5b8a524287526f50a8a4fb9652/libmamba/src/core/link.cpp#L674)
sets `PREFIX` to the transaction target and uses an extended parent environment;
it does not replace `CONDA_PREFIX` in that environment map. Thus a correct native
transaction prefix does not make the hook's chosen variable correct. The hook
also masks unlink failure with `|| true`. The inspected sources plus original
log explain the observed path without asserting that Mamba selected the wrong
transaction target or that every package hook has this defect.

`development_environment.py` owns profile/bootstrap/install/reinstall/runtime
operations, not environment retirement. There is no central removal call to
patch, and this is not a PharmacophoreMT molecular-code defect. The concrete
package-source correction belongs to **conda-forge/ocl-icd-system-feedstock**.
Mamba maintainers may additionally review inherited activation context, but a
Mamba product bug is not established merely by this package's variable choice.

## Executed owned-sentinel experiment

Python 3.14.7 in the named `molsyssuite@uibcdf_3.14` environment created a managed
temporary directory containing two fake prefixes. Each held its own vendor-file
sentinel. Only `/bin/sh` and the hook fixture were executed with controlled
`PATH`, `PKG_NAME`, `PREFIX` and `CONDA_PREFIX`; no Conda/Mamba removal or actual
shared-prefix operation occurred.

| Case | Hook prefix | Caller sentinel | Target sentinel | Exit |
| --- | --- | --- | --- | ---: |
| Original hook; inherited active context | Caller `CONDA_PREFIX`, separate target `PREFIX` | Removed | Preserved | 0 |
| Original hook; explicit target context | Both variables identify target | Preserved | Removed | 0 |
| Transaction-prefix hook fixture | Required `PREFIX`, inherited caller `CONDA_PREFIX` | Preserved | Removed | 0 |

The third fixture used `rm "${PREFIX:?}/etc/OpenCL/vendors/${PKG_NAME}" || true`;
it is a controlled hypothesis, not an accepted or published upstream patch.
Both sentinel trees were task-owned and managed cleanup removed the fixture.
This reproduces the hook's wrong-prefix selection and validates two bounded
contexts, not an end-to-end corrected native transaction or hostile-code sandbox.

## Existing controls and remaining work

The accepted resource policy already requires preserving caller/shared resources,
checking ownership and reporting cleanup errors. Keep native success/target-prefix
facts separate from hook diagnostics. For a disposable prefix already proven
task-owned and inactive, reviewed scoped filesystem retirement avoids executing
uninstall hooks; check symlinks, receipts, human changes, mounts and retained
outputs first. It does not run package cleanup or certify global Conda registry/
cache hygiene. Do not turn this into a broad path/age-based cleaner.

Target-bound environment variables explain this hook, but do not constrain
arbitrary hook code or justify running native removal against the real shared
environment. No production hook/cache/environment is edited by this analysis.
No new general cleanup API or universal layout requirement is introduced.

Upstream receiving still needs a real provider issue, reviewed hook correction
and package build, then an owned native transaction test with a separate caller
sentinel. Preserve original failure evidence and record the new build identity;
do not rewrite historical package bytes. The central issue cannot claim that
provider work complete. Its normative reference records existing controls, not
a regression guard for an upstream patch that has not been delivered.

## Maintainer handoff

Open in `conda-forge/ocl-icd-system-feedstock`: **pre-unlink uses active
CONDA_PREFIX instead of the transaction PREFIX**. Include the exact 1.0.0 build-1
coordinate/hash, hook/source links, Mamba 2.9.0 context and the three owned
sentinel outcomes above. Request a target-prefix-aware hook with an empty-prefix
guard, review of the companion post-link assumptions, and an unchanged-caller
sentinel regression in native receiving. Avoid requesting a Mamba upgrade or
changing the shared environment as an unverified remedy.

Component scientific evidence, original artifacts, primary worktrees and the
known twelve named-workspace dependency findings retain their separate owners.
