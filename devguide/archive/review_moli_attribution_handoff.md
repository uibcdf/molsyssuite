---
summary: Review portable attribution exchange with MOLI while retaining owner semantics.
issue: uibcdf/molsyssuite#76
status: resolved
opened: 2026-10-03
closed: 2026-10-04
verification: measured
area: [governance, attribution, compatibility]
guard:
normative: devguide/ackredit_client_policy.md
blocked_by: []
supersedes: []
---

# Portable attribution handoff to MOLI

## What

uibcdf/moli#36 requests the suite's review of bibliography, observed resource
use, historical versions, acquisition outcomes and saved readers. Ackredit
owns the portable provider payload; the suite owns optional member adoption.
Sabueso owns knowledge/source records and its selected required dependency.
Nextia owns project interpretation, and MOLI/Recorda owns project execution
correlation and persistence. Central coordination does not transfer ownership.

## How

The existing accepted optional-client policy already requires result-bound
original records, reference reuse, application-owned workflow sessions,
evaluated-empty provenance, honest failures, detached readers and published
dependency evidence. Review of the public 0.9.0 contract and a synthetic
installed-provider exercise finds no API gap for the requested exchange.

| Requested behavior | Provider capability and owner obligation |
| --- | --- |
| Two results reuse references and contribute to a workflow | `capture` observes each result independently; `get_attribution` snapshots the application session. Session ID subtraction is unnecessary and insufficient. |
| Original bibliography and software versions | `items`, use `context` and capture `context` retain detached original records. Hosts supply accurate original producer/version context; readers do not replace it with current metadata. |
| Empty or failed acquisition and incomplete attribution | Empty payloads and extensible JSON context are supported. The host owns operation outcomes and completeness; a capture can preserve completed child credits through an exception without certifying success. |
| Result identity, historical source references and correlation | Host-owned wrappers retain original owner-issued pins and operation/result links. They are outside Ackredit's fixed top-level structure; this review chooses no shared key vocabulary. |
| Saved read without new credit | `Attribution.from_dict`/`from_json` detach records without registration, tracking, DOI enrichment or producer-engine imports. |
| Terms, source support and project Evidence | Those meanings remain outside the provider's validation and bibliography. Their respective owners make explicit decisions. |

The maintainer accepts the compatible clarification below in the central
optional policy. The provider's canonical guide and API remain unchanged.

## Why

Portable bibliography is usable across projects only when consumers retain its
original scope and meaning. A valid attribution payload does not prove complete
source observation, successful science, permission to copy content or a project
interpretation. Keeping the authority explicit avoids silently assigning these
responsibilities to Ackredit or making it mandatory for every suite member.

## What is measured and what is assumed

`devguide/examples/ackredit_moli_boundary.py` runs outside the repository using
the retained normal public-channel Ackredit 0.9.0 installation. It exercises
two detached results with reused resource/software references, a completed
empty fixture operation, an actual deliberate failed attempt, workflow credit,
saved JSON and a separate reader session without new credit. A separate fresh
process also reads the saved records with networking prohibited and no producer
engines. This is a synthetic administrative contract exercise, with no source
access or scientific result. It implements no Nextia/Recorda integration.

The artifact is `noarch/ackredit-0.9.0-py_0.tar.bz2`, SHA-256
`37661090f6ad19a74b8155d8a4d4b4a068c9099f4ceba0743b3abfe887e97fe1`.
The environment is retained, not freshly solved for this review; its Conda
record, runtime version, non-editable import origin and dependency closure
are rechecked. Historical installed/public qualification remains in
`devguide/rollouts/ackredit_python314_admission_51.json`.

Source review: Ackredit `40f930a852e3fe4517ba0a6d32d7dabc8624d285` retains
byte-identical provider/contract/guide inputs relative to the inspected
`de209caddd618042183884239ffb395e3d21a615`. Inspecting source tests does not
claim they were executed in this review. Existing guard:
`uibcdf/ackredit#75`, `tests/test_attribution_contract.py`.

Sabueso's current uibcdf/sabueso#108 reports public 0.12.0 plus subsequent
unreleased source expansions. That is owner-reported receiving evidence,
not independent suite certification of its latest code. MOLI's original #36
record still describes provider delivery as pending; our handoff will supply
the current published-provider evidence and leave its update with MOLI.

## Accepted policy clarification — 2026-10-04

For members exchanging detached attribution with another component or project,
keep original result/source identities, observed producer/software versions,
bibliography, contextual uses and explicit gaps or failures. Preserve saved
records without new acquisition, credit or silent replacement by current
metadata. The host owns result/operation links and completeness outside the
provider payload. Source support, source-stated terms, permission decisions,
execution history and project Evidence retain their respective owners; a
valid citation record alone establishes none of those decisions. Required
dependencies chosen by external consumers do not change the suite's optional
profile. This establishes no universal wrapper, status enumeration or new
provider API.

The maintainer selects adding this compatible clarification to
`devguide/ackredit_client_policy.md`. The alternative was to retain the policy
and return only the review to MOLI. No component scientific code changes.

## Alternatives and refuted paths

A universal wrapper/schema would standardize provisional component semantics
without a demonstrated need. Adding mandatory status fields to
`ackredit.attribution@1` would contradict its released structural contract.
Session differences would lose references reused across results. Replaying
acquisitions or rerunning scientific suites is unnecessary for this review.

## Scope and exclusions

Existing public portable API and the suite's semantic handoff. No component
implementation, dependency, guide copy, package, access or policy-pin changes.
General action rollout, provisional function declarations under #97, broad
member runtime adoption and MOLI's full acceptance exercise remain separate.

## Acceptance criteria

- Record the maintainer's policy clarification decision and semantic review.
- Return the suite review, runnable synthetic exercise, immutable evidence and
  owner-local follow-ups to uibcdf/moli#36 and uibcdf/ackredit#75.
- Preserve public delivery, guide synchronization and runtime adoption as
  separate claims. Route any concrete new provider need to its owner.
- Leave Nextia/Recorda interpretation, persistence and the full platform
  acceptance exercise with MOLI; do not claim their implementation here.

## Local implementation issues

uibcdf/ackredit#75 owns the released contract; uibcdf/ackredit#22 owns its
public file. No new provider implementation defect is found.
uibcdf/sabueso#108 owns consumer observation and its local sidecars.
uibcdf/moli#36 owns the shared platform exercise and semantic coordination;
uibcdf/moli#18 owns execution-record integration.

## Dependencies and risks

LMMV owns the suite decision and handoff. Prospective Nextia/Recorda consumers
must determine their own minimum link/status requirements under MOLI #36.
The synthetic wrapper is example-local and cannot be cited as an accepted
shared wire format or complete source bibliography.

## Resolution — 2026-10-04

The maintainer accepts the compatible clarification in the existing optional
client policy. The public-provider exercise, fresh saved reader and reviewed
source contract cover the suite portion. Actionable prepublication reviews are
returned to MOLI #36, Ackredit #75, Sabueso #108 and the six registered client
owners; exact notice links are retained in the primary receipt. No new provider
implementation need is found.

The maintained normative guard is `devguide/ackredit_client_policy.md`.
The suite coordination can close independently of MOLI's remaining platform
exercise and member scientific/runtime adoption. Applicable exact-commit
hosted governance is recorded in the closing delivery; successful central
checks do not recover the OpenCASTp audits pending under #102.

## Provenance

2026-10-04, Linux/Python 3.14.7, public Ackredit 0.9.0 build py_0. Commands,
environment/artifact checks, reviewed source hashes and bounded results are
retained in `devguide/rollouts/ackredit_moli_handoff_76_20261004.json`.
Original member clones remain unchanged; suite status reports the original
Ackredit clone clean and 79 commits behind. The detached review clone is used
only for pinned source reads, not as a qualified routine development workspace.
