---
summary: Login-shell logout overwrites a successful public Conda verification exit.
issue: uibcdf/molsyssuite#48
status: active
opened: 2026-09-25
closed:
severity: medium
verification: reproduced
area: [governance, release]
guard:
normative:
blocked_by: []
supersedes: []
---

# Successful Conda verification reported as failed

**Reported:** Coordinated MolSysMT 0.22.4 / MolSysViewer 0.23.4 promotion.
**Status:** Shared verifier extraction and consumer adoption in progress.

## What

Six promotion actions and their receipts passed, while the final verifier printed
the matching public URL and returned 1. This did not justify another upload.
Original runs: Viewer 36128473826; MT 36128498551, 36128498646, 36128498419,
36128498721 and 36128498399. Installed-pair gate: MT 36121427459, 20/20.

## How

The historical workflow uses `bash -l {0}`, `set -euo pipefail` and an explicit
`exit 0` after the Python check succeeds. A noninteractive login shell executes
`.bash_logout` on that explicit exit. The Ubuntu logout script calls
`clear_console -q` at shell level 1; without a console it fails. With `errexit`,
the successful verifier therefore exits 1 during logout.

On 2026-10-01 a subprocess using the existing local logout file, `SHLVL=0` in
its inherited environment, and `bash --login -xc` printed `verified`, traced
`exit 0` followed by `clear_console -q`, and returned 1. The non-login shell
returned 0. No home files or user configuration were modified. Historical
native logs show the matching URL immediately followed by exit 1; their lack
of shell tracing does not independently expose the runner's logout commands.

The common verifier runs in a non-login shell and uses anonymous, bounded HTTP
reads of Anaconda release metadata and the public solver index. Promotion
credentials and mutations remain component-owned. Exact inventories allow
independent rechecks of all files in a coupled pair.

## Why

Copied shell verifiers affect multiple components and obscure release state.
A producer receipt, public label, solver index and installed-pair test prove
different facts. The shared read-only boundary preserves those distinctions.

## What is measured and what is assumed

The logout failure is locally reproduced. Original native logs establish the
same observable symptom. Prior independent public checks remain historical
evidence; fresh hosted shared-verifier results will be appended separately.

## Alternatives and refuted paths

Repeating promotion to get a green badge risks unnecessary mutation and does
not repair verification. Waiving the red step fails to establish public state.
Changing user logout files would hide a dependency on host shell configuration.

## Scope and exclusions

Shared Conda verification and local workflow routing in MolSysMT, MolSysViewer
and DepDigest. No new releases, uploads, promotions or scientific test execution.

## Acceptance criteria

- Tested shared exact-file verifier with bounded propagation retries.
- All six historical public files independently verified with the shared tool.
- Both affected consumers call a pinned common provider and retain evidence.
- Read-only recheck workflows remain separate from promotion.
- Local workflow guards protect adoption; shared guard protects exit and identity.

## Local implementation issues

Existing context: uibcdf/molsysmt#246, uibcdf/molsysviewer#105.
Provider adoption: uibcdf/molsysmt#275 and uibcdf/molsysviewer#133;
DepDigest adoption will be recorded before its changes.

## Dependencies and risks

Policy acceptance and publication routing are coordinated in uibcdf/molsyssuite#27.
Index propagation remains bounded and never changes immutable file identity.

## Provenance

2026-10-01; local Linux workspace; Python 3.13; native Bash subprocess;
historical workflow source c32fb4a688321737a7a15c6b17f91f0c68558d8c and GitHub
Actions native log for uibcdf/molsysviewer run 36128473826.

## 2026-10-01 shared-provider validation

The common provider's ten governance tests pass, including CLI success status,
both archive formats, two-source identity/digest contradictions, bounded retries,
complete pair inventories and the non-login shell regression guard. The full
central administrative suite passes 188 tests. Command:
`python -m unittest discover -s tests -q`.

The common CLI independently rechecked all six original public files:
`python devtools/scripts/verify_public_conda.py --inventory <exact-inventory.json>
--output <evidence.json> --attempts 2 --interval 1`. All six had matching `main`
labels, solver-index identities/build numbers and SHA-256 digests. No package
bytes were uploaded, relabeled or rebuilt. This establishes registry/index state,
not a new installed-pair scientific result.
