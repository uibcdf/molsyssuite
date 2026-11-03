---
summary: Align Python license metadata, build-tool capabilities and owner distribution evidence.
issue: uibcdf/molsyssuite#162
status: partial
opened: 2026-11-03
closed:
verification: reproduced
area: [governance, packaging, compatibility]
guard: tests/test_starter_distribution.py::StarterDistributionTests::test_generated_sdist_and_rebuilt_wheel_include_declared_license
normative: devguide/python_license_metadata.md
blocked_by: []
supersedes: []
---

# License metadata and compatible build tools

**Reported:** DockingMT #47 build warnings and a maintainer-requested shared review.
**Status:** Partial. Central starter/reference and owner routing are complete.
Thirteen open owner routes request explicit confirmations; three already-compatible
source observations need no new task. Actual owner/distribution receiving remains.

## What

Provide a compatible PEP 639 migration pattern, preserving actual licenses and
notices. Repair the canonical seed before generating more legacy declarations.
Source metadata, actual backend capability, real archive inclusion and public
receiving are separate facts.

## How

The existing starter used a legacy MIT table, Setuptools >=68 and generated no
LICENSE. Its real wheel regression fails with no License-Expression. The repair
uses an SPDX MIT string, explicit LICENSE field and tested >=77.0.3 backend floor;
both no-build-isolation Conda fixtures agree. The generator retains the seed's
actual MIT notice and copyright. No existing component notice is replaced.

The [technical reference](../python_license_metadata.md) links official sources,
describes backend-specific adoption and actual wheel/sdist payload checks, and
routes owner review. Setuptools gained the fields in 77.0.0; 77.0.3 is a reviewed
patch baseline tested for the seed. Existing compatible >=77.0 declarations are
not automatically rejected for differing from that patch baseline. No new global
checker, policy release or automatic legacy-member migration is introduced.

## Why

Modern builds can succeed while masking an underdeclared backend minimum.
Deprecated metadata and absent explicit source fields do not by themselves prove
an archive defect. A coherent seed and actual built-distribution regression protect
future repositories without assigning scientific fixes to central governance.

## What is measured and what is assumed

- Fifteen public member pyprojects and one private-owner metadata route are
  recorded at exact fetched source commits: four modern compatible declarations,
  two modern/pre-feature-minimum declarations and nine legacy forms. This is not
  a fresh package audit or a universal license choice.
- Existing specific reviews are MolSysMT #541, Viewer #292 and Ackredit #135;
  DockingMT #47 now has modern owner source `251e7560`. The later routing receipt
  below commissions the remaining applicable reviews without rewriting that
  earlier source-inventory snapshot.
- A real generated Git fixture fails before repair. After repair, its sdist,
  wheel and wheel rebuilt from the sdist contain the expected SPDX fields and
  exact inherited notice bytes on current Setuptools 84.0.0/Python 3.14.7.
- An independent venv without scientific site packages installs the recorded
  tool wheels, fixes the backend to exactly 77.0.3, passes the same three archive
  checks and has clean tool dependency closure. It is build-only receiving on
  Linux/Python 3.14.7, not all supported runtime minors/platforms.
- Initial /tmp tool installation stopped on quota before building. A separate
  owned ignored workspace fixture succeeds. Neither touched the shared prefix;
  both disposable fixtures are retired after useful proof is retained.
- Forty selected central tests and changed-module Ruff pass. No member archive
  is built, rebuilt, uploaded or relabeled; all artifacts are synthetic fixtures.

## Alternatives and refuted paths

| Choice | Disposition |
| --- | --- |
| Repair only member declarations | Incomplete: the seed would continue generating old metadata. |
| Force the newest exact Setuptools everywhere | Unnecessary: use a compatible minimum and actual frozen build evidence. |
| Replace all licenses with the starter's MIT | Rejected: owners retain their actual choice and third-party notices. |
| Source existence or modern build proves all archive/floor behavior | Rejected: inspect real payload and deliberately test a minimum separately. |
| Correct seed plus conditional migration reference/owner receiving | Implemented centrally; component adoption remains local. |

## Scope and exclusions

Central seed, generation/distribution guard, technical reference and coordination.
No new license terms, scientific implementation, universal blocking gate, runtime
Python-range change, native tool/versioning migration, publication authorization
or immutable artifact replacement. Private metadata is not republished.

## Acceptance criteria

- [x] Inspect authoritative field/backend support and preserve actual license choices.
- [x] Repair the seed, notice payload and aligned build fixture requirements.
- [x] Add a relevant before-fix real distribution regression.
- [x] Receive wheel/sdist/rebuilt-wheel payloads with current and exact-minimum tools.
- [x] Give every applicable review an owner destination and explicit confirmation request.
- [ ] Receive remaining owner reviews, constraints/exceptions and actual distribution evidence.

## Local implementation issues

All thirteen routes below are open at the current observation. Four focused
issues were created after checking open license/SPDX/PEP titles; the unrelated
DepDigest #40 lazy-import proposal is preserved. Nine existing routes are reused,
including one private owner review. No existing issue body is replaced.

| Component | Review route | Routing |
| --- | --- | --- |
| SMonitor | uibcdf/smonitor#57 | New focused review |
| ArgDigest | uibcdf/argdigest#44 | New focused review |
| DepDigest | uibcdf/depdigest#45 | New focused review |
| PyUnitWizard | uibcdf/pyunitwizard#135 | New focused review |
| MolSysMT | uibcdf/molsysmt#541 | Existing specific finding |
| MolSysViewer | uibcdf/molsysviewer#292 | Existing specific finding |
| Ackredit | uibcdf/ackredit#135 | Existing license review |
| DockingMT | uibcdf/dockingmt#47 | Existing packaging owner |
| TopoMT | uibcdf/topomt#78 | Existing distribution review |
| ElastNetMT | uibcdf/elastnetmt#18 | Existing distribution review |
| LinDelINT | uibcdf/lindelint#14 | Existing future-candidate review |
| PeptideMT | uibcdf/peptidemt#29 | Existing distribution-profile review |
| OpenCASTp | uibcdf/opencastp#2 | Private review; sanitized metadata only |

Each route requests **Review completed**, the exact reviewed commit/scopes,
disposition, actual commands/results and precisely pending qualification. An
owned deferral includes its reason, interim route and dated review or concrete
revisit/removal trigger. Link the result to #162. Delivery, source inspection or
unrelated passing CI is not owner completion. No immediate release, common patch
pin, new mandatory gate, scientific campaign or stability deadline is requested.

Pytest Receptor, GH Run Receptor and PharmacophoreMT already have compatible
modern source declarations in the original inventory. No new review task is
commissioned for them; these observations do not requalify archives or claim
fresh owner confirmation. All sixteen Python members are accounted for.
[Exact destinations/notices and state receipt](../rollouts/license_metadata_owner_routing_162_20261103.json).
Preserve early-maturity and scientific deferrals.

## Dependencies and risks

Owners with another backend/native/versioning profile qualify their actual
compatible tool route. Existing files remain immutable and license classifiers
are removed only as part of a reviewed equivalent metadata transition. Source
presence and legal license choice are not inferred from a passing build.

## Provenance

2026-11-03; named Python 3.14.7, exact Git objects, official Setuptools/PyPA/PEP
documents and isolated synthetic build-tool qualification. [Source/build receipt](../rollouts/license_metadata_starter_162_20261103.json).

## CI fixture correction — 2026-11-03

The new packaging guard initially used the generator's real published-policy
lookup. A clean no-tags, depth-one checkout reproduces a missing policy-tag
failure before distribution construction. Supply the same effective-policy
fixture used by existing starter tests, leaving production immutable-policy and
admission verification unchanged. The same shallow checkout then builds and
verifies its actual sdist, wheel and rebuilt wheel. All license/payload assertions
remain real; no tag fetch or scientific environment is needed for this guard.
[Before/after checkout proof](../rollouts/starter_distribution_ci_fixture_162_20261103.json).
