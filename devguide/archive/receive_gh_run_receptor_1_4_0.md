---
summary: Receive GHR 1.4.0 public bytes, registry evidence and canonical consumer guidance.
issue: uibcdf/molsyssuite#158
status: resolved
opened: 2026-10-29
closed: 2026-10-29
verification: measured
area: [distribution, tooling, compatibility]
guard: tests/test_governance.py::VendoredGuideSynchronizationTests::test_registered_guide_can_be_synchronized_byte_identically
normative: devguide/adoption_lifecycle.md
blocked_by: []
supersedes: []
---

# GH Run Receptor 1.4.0 receiving

**Reported:** Owner release notice and explicit receiving request, 2026-10-29.
**Status:** Resolved. Public delivery, shared refactor and all fifteen guide
adoptions are received; direct MolI consumer review is handed to uibcdf/moli#79.

## What and why

GHR delivered #74 watch-progress clarity and #76 consolidated qualification in
1.4.0. MolSysSuite needed current distribution/access evidence, exact canonical
guide delivery and an actual consumer-pin review. Historical pre-publication
governance did not prove public availability; guide delivery does not upgrade
operator environments or qualify consumer scientific behavior.

## Exact delivery and independent verification

- Product/tag `1.4.0`: `c2d16255868df5e1f5a7eaaa72d71ac8387cef01`.
- Administrative stage/qualification/promotion:
  `4cc619916b705deaf0837531b21dc9aae97f8575`.
- Canonical guide and owner receipt:
  `a60f4c776db3eb8723df1a5d244b5ad030d952be`.
- Public Conda `uibcdf/main`, noarch:
  `gh-run-receptor-1.4.0-py_0.tar.bz2`, SHA-256
  `0d04617887d8935df4197f63c99e927aefb3319b75af4e2cf1042a692f6891d3`.
- Public wheel `gh_run_receptor-1.4.0-py3-none-any.whl`: SHA-256
  `caf4e33e81d3e7fcd3438315f03b35829783fd2a17bb6f1eb797c56fe71eb1e4`.
- Public sdist `gh_run_receptor-1.4.0.tar.gz`: SHA-256
  `953416f20ae949c8999d2cccab99aac632437747f26c8b819b630b9242d64db3`.

The receiving session independently downloaded the published distributions,
checked hashes, API tag/release/asset sizes and checksums, and executed the
owner's bounded archive guards. The shared public verifier accepts both the
Conda main label and solver index; downloaded Conda bytes match the qualified
digest. Nothing was rebuilt, uploaded, promoted or replaced by receiving.

Native source/run/attempt/job/required-step verification covers exact-tag
source/wheel compatibility (40952869892), extension/Action (40952874839),
producer (40953039390), original installed matrix (40953626384), unchanged-file
promotion (40955300448), GitHub publication (40955305570), final complete source
suite/coverage (40960194772), strict docs/Pages (40960194910), policy
(40960195274) and Conda controls (40960195396). Twelve original Conda cells
each execute 650 tests with before/after installed provenance and support
retirement; their native ZIP digests and bounded JSON records were independently
acquired and checked. The original private-refactor matrix and complete assertion
history are separately reconciled in [#144](receive_path_sensitive_installed_helpers.md).

A fresh owned Linux/Python 3.14.7 prefix installs the exact public wheel with
`--no-deps`, outside source clones. Version and installed origin are verified;
unshipped tools are not importable. That installed 1.4.0 receptor is used for
initial native-run inspection, followed by shared exact native verification.
This is one public-wheel installation, not twelve installations of those bytes.

Independent Zenodo receiving confirms version DOI `10.5281/zenodo.23780283`,
concept DOI `10.5281/zenodo.22843377` and one 1,072,180-byte source ZIP with
MD5 `7592f98f31726ee12ad3b763dc73739d`. The wheel/sdist are not claimed as
Zenodo files. No PyPI publication is claimed.

## Canonical guidance and actual consumer adoption

The registered canonical guide SHA-256 is
`e47b04cc90e96ab4039aa9a3b5a8be5025b48574b2636cb19f22c05543ca4ae2`.
The official `sync_vendored_guides.py` distributes it from the published source
to all fifteen registered consumers in clean task-owned clones. Each focused,
unskipped direct commit changes only `GH_RUN_RECEPTOR_GUIDE.md`. Live default
branches carry exact bytes. Each exact adoption has verified native conformance,
lint and format steps; MolSysViewer's additional dependency metadata audit is
also verified. Twelve existing configurations pass the public 1.4.0 parser;
the three absent configurations are not invented.

Source-bound review of tracked workflows, devtools, package metadata and root
requirement/environment inputs finds no executable GHR version/commit pins in
those fifteen consumers. Existing schemas and historical receipts stay intact.
Guide examples now recommend 1.4.0; operator extension installations remain
operator-owned and require an explicit upgrade/version check. No universal
minimum, runtime dependency, policy caller or unrelated provider pin is changed.
Actionable advance notices and exact delivery/native closeout were delivered
to existing registered owner review issues. Direct MolI review uses uibcdf/moli#79;
central closure does not certify its consumers' local adoption.

The registry keeps governance adopted/recipe ready and changes GHR publication
access from unknown to confirmed by this executed delivery. Its registered
publisher row now records the actual immutable `fee3bd8` call. Earlier dated
receipts remain historical evidence, including failed attempts and 1.3.0 bytes.

## Guards, evidence and limits

[Durable receipt](../rollouts/gh_run_receptor_1_4_0_receiving_158_20261029.json)
retains exact source/file/provider identities, native jobs/steps, digest-bound
per-cell receiving, every consumer commit/check/notice and the scoped pin review.
The local guard exercises registry-selected byte-identical synchronization;
it protects the delivery mechanism. The normative adoption lifecycle requires
published copies and explicit rollout targets. Neither alone certifies package
qualification: that claim uses the independently checked native/artifact evidence.

Local shared-provider regressions pass 57 tests in `molsyssuite@uibcdf_3.14`
(Python 3.14.7); provider merge governance/coverage 40920603151 passes. Final
central governance and applicable live audits are linked from the issue closeout.
Primary/dirty clones and the shared environment are preserved; its twelve known
dependency-closure findings remain recorded under #82. Scientific work, source
qualification of consumer packages and original owner artifacts retain their
owners and prior limits. Only common hashes/administrative facts from private
OpenCASTp appear in public receiving. Task-owned temporary resources are removed
after durable closeout under the existing lifecycle policy.
