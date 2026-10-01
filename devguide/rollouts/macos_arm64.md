# macOS Apple Silicon source adoption

Decision: uibcdf/molsyssuite#59. Inspected 2026-10-01 at the immutable member
sources below. Intel macOS is retired from prospective support. Historical
artifacts, benchmark examples and negative-test fixtures remain unchanged.
This source inventory is not a new installed-package/runtime certificate.

The active workflows and developer build inputs inspected contain no enabled
`osx-64` publication target, Intel runner or `x86_64-apple` build target.
Legacy action inputs explicitly set `platform_osx-64: false`. Standard
`macos-latest` and `macos-15` runners are arm64 according to
[GitHub's runner reference](https://docs.github.com/en/actions/reference/runners/github-hosted-runners)
(accessed 2026-10-01); their labels do not establish executed test evidence.
MolSysMT's generic provenance reader still recognizes historical `osx-64`
records; current candidate selection and installed gates exclude that platform.

Machine-readable authority: `policies.python-ci.macos-architectures = ["arm64"]`
in `suite.toml`. Existing member CI review claims and their honest partial states
remain intact. The offline CI-policy validator rejects adding Intel to this set.
Every registered member receives the canonical component-facing boundary through
`MOLSYSSUITE_GUIDE.md`; current explicit support pages also state or link it.

| Member | Inspected source | Local review owner | Remaining evidence / scope |
| --- | --- | --- | --- |
| uibcdf/smonitor | `16f3470b0bf5e71385eea3fc4bb8284606efe13d` | uibcdf/smonitor#33 | Common boundary; local installed/platform review remains open. |
| uibcdf/argdigest | `909d0787ecdc6bbd5659b2d5fe53db032d32a70b` | uibcdf/argdigest#21 | Common boundary; local installed/platform review remains open. |
| uibcdf/depdigest | `f1e72303ff9cc346a815da6746fbce6298a8db1b` | uibcdf/depdigest#21 | Common boundary; local installed/platform review remains open. |
| uibcdf/pyunitwizard | `9849366bed56f6ad39540ad20673d16ffa36c4db` | uibcdf/pyunitwizard#91 | Common boundary; local installed/platform review remains open. |
| uibcdf/pytest-receptor | `9b88575736699b7e53f708d628b69266f480605c` | uibcdf/pytest-receptor#11 | Common boundary; local installed/platform review remains open. |
| uibcdf/gh-run-receptor | `0f2e68cc62198064042994a9587c0a0a0938fa42` | uibcdf/gh-run-receptor#52 | Common boundary; local installed/platform review remains open. |
| uibcdf/molsysmt | `243bcc5ceb8d5a9ec9aa7357c17529f2c8fb6e3e` | uibcdf/molsysmt#185 | Explicit README boundary; four-platform candidate gates; future exact-candidate evidence remains required. |
| uibcdf/molsysviewer | `1954dd1604c838d783833e9a45f7d4f5ffb19536` | uibcdf/molsysviewer#116 | Explicit README boundary; four-platform candidate gates; future exact-candidate evidence remains required. |
| uibcdf/topomt | `9c63c6adec4cfa292fc8f985927127c1648964a3` | uibcdf/topomt#58 | Common noarch wrappers target osx-arm64; installed execution remains component-owned. |
| uibcdf/pharmacophoremt | `3d12fe705d2234fb5a5a8f6a0a78959f8b303760` | uibcdf/pharmacophoremt#9 | Common noarch wrappers target osx-arm64; installed execution remains component-owned. |
| uibcdf/elastnetmt | `ea6e31bab2bafc0a2c26aee67bf72ffeddc86355` | uibcdf/elastnetmt#17 | Common noarch wrappers target osx-arm64; installed execution remains component-owned. |
| uibcdf/dockingmt | `46ea64bbfd899cb5905cb303f3a2c145a095ebf5` | uibcdf/dockingmt#21 | Common boundary; local installed/platform review remains open. |
| uibcdf/ackredit | `1466bc26f5e3f71bc08e619ac018c2b8295323a8` | uibcdf/ackredit#74 | Common boundary; local installed/platform review remains open. |
| uibcdf/lindelint | `b0e0405a27b7a507123d0f15d59bf69a8e49a540` | uibcdf/lindelint#12 | Common noarch wrappers target osx-arm64; installed execution remains component-owned. |
| uibcdf/molsys-ai | `1e510567828d2126f243c22c697e644bccee056e` | uibcdf/molsyssuite#59 | Governed subsystem; no Python package/platform claim; common boundary applies if a claim is added. |

## Delivery and remaining ownership

MolSysMT and MolSysViewer already carry the explicit boundary in their READMEs
and prospective four-platform package gates. Their prior 20-cell five-platform
release evidence remains dated history; a future 16-cell four-platform candidate
requires fresh evidence at that candidate. This rollout does not rerun their
scientific suites or claim optional Qt-host compatibility on macOS.

PyUnitWizard, ArgDigest and GH Run Receptor current support pages are being
qualified explicitly as Apple Silicon. Other members have no current explicit
Intel promise in the inspected public support/build surfaces; their common
boundary is supplied by the canonical guide. Local CI reviews retain ownership
of complete installed/runtime/platform-claim evidence. Incubating components may
claim no supported platforms. MolSysViewer's Linux-only standalone Qt-host
boundary remains in uibcdf/molsysviewer#97; it is not a reason to claim macOS Qt
support. UIBCDF Qt-fork observation remains uibcdf/molsyssuite#57.

Reconsideration starts with a concrete user need in a MolSysSuite issue, names
component owners, costs and proposed evidence, and requires an explicit support
decision. No historical download or fork deletion is part of this retirement.
