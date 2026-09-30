---
summary: Share optional-engine boundary semantics and adoption evidence across members.
issue: uibcdf/molsyssuite#62
status: partial
opened: 2026-09-30
closed:
verification: inspected
area: [governance, dependencies, compatibility]
guard:
normative: devguide/optional_engine_integration.md
blocked_by: [uibcdf/depdigest#22]
supersedes: []
---

# Shared optional engine contract

**Reported:** 2026-09-30, following TopoMT optional-engine consumer work.
**Status:** Partial; shared policy and starter guidance implemented, release and
member runtime gates remain open.

## What

Coordinate the DepDigest/SMonitor optional-engine recipe and generalize TopoMT's
provider/access distinction into a usable member contract. Applicable members
need truthful availability, selected-route guards, distinct failure semantics
and attributed result boundaries. A common directory tree or scientific model
is not required.

The owning issue existed before this report. Earlier integration evidence lived
in the provider and consumer records; this report supplies central adoption and
policy acceptance without duplicating their scientific analysis.

## How

Register `policies.optional-engine-integration` with phased applicability to
actual optional boundaries. Publish `devguide/optional_engine_integration.md`,
link it from the ecosystem/starter guidance, and generate an unqueued review
worksheet for future Python members. No unused runtime library is added by the kit.

The policy separates method identity from library/CLI/service/files/local access;
preserves existing APIs and environments; assigns availability to DepDigest,
events to SMonitor, execution/results to consumers, and coordination to MolSysSuite.
Exceptions name ownership, interim behavior, removal and dated reassessment.

## Why

TopoMT has already exercised the distinction with Pocketeer, AlphaSpace2, pyCASTA,
fpocket, CASTp services and saved outputs. Its architecture ADR, engine installation
page and provider output checkpoint demonstrate useful shared semantics. Future
members can reuse them without copying provider discovery or TopoMT's classes.

## What is measured and what is assumed

Inspection on 2026-09-30 used fetched remote main, leaving original worktrees intact:

| Repository/source | Inspected evidence and limit |
| --- | --- |
| TopoMT `22acca476570cb269af5ab48bd0c58a6960c5591` | Architecture ADR, third-party installation page, provider output checkpoint, `_depdigest.py`, fpocket runner and dependency/installed-engine guards. Three originals have soft declarations and explicit disabled Conda routes. fpocket still has a local missing-command translation. Tests/source show intended behavior; no new scientific execution or sibling adoption is claimed. |
| DepDigest `4de4c0aa3b96850af2f043e91000977f9d571b18` | Provider-owned guide, optional-engine adoption page, decorator and #22. Executable/disabled-installer extension is on main in `08f8263`. Local tag `0.11.2` predates that extension and its checker lacks the capability. #22 remains open for publication/adoption; no release certification is inferred. |
| MolSysMT `be9600eebfd27de29a3d11ad49f6ad3a01cd3f22` | Existing import-name soft declarations and mapping in `_depdigest.py`, including different import/distribution identities. Full route/execution review remains deferred. |
| MolSysViewer `ef3dd4dcb12b188d5844561cf458d0b53f4de815` | Existing hard bootstrap declarations, small registry mapping and library-first `LibraryNotFoundError(library, caller=None, message=None)` with local catalog rendering. Public constructor migration needs local tests; no message-first rewrite or speculative soft inventory is imposed. Scientific/UI execution review remains deferred. |

The accepted guide distribution is independently resolved by uibcdf/molsyssuite#63:
ten copies at the recorded canonical SHA-256 and hosted audit 36705001882 passed.
It does not establish public release or runtime adoption.

GitHub's DepDigest release inventory lists `0.11.2` (2026-09-26) as the latest
published release at inspection. Its committed checker lacks the extension, so
this is a concrete release gap, not merely absence of a recorded release review.
The central TopoMT support-library evidence is refreshed while retaining `partial`;
its owning open issues and full public-boundary acceptance are not closed by source
inspection.

Historical TopoMT full CI 36700609235 at `507e347` is now **completed/failure**, not
pending. GH Run Receptor 1.0.0 metadata inspection and native GitHub job/step data
agree: all six actual `Run tests` steps failed. These observations do not diagnose
every failure or invalidate the narrower optional-boundary evidence previously
recorded by #62/#22. Product defects remain member-owned.

## Alternatives and refuted paths

- Requiring TopoMT's namespace, output classes or fixed geometry/unit conventions
  would prescribe one component's model to unrelated members. Share semantics.
- Treating package discovery as service/execution/scientific readiness would erase
  distinct failure causes and overstate evidence.
- Counting guide distribution or all-skipped installed comparisons as adoption
  would leave the runtime boundary unverified.
- Replacing established MolSysMT/MolSysViewer contracts now would interfere with
  active development and the explicit scientific-review deferral. Record later gates.
- Adding a full-engine battery to every internal push would contradict the accepted
  CI lane/recovery policy. Members choose justified installed verification routes.

## Scope and exclusions

Central governance, dependency compatibility, examples, starter guidance and
issue/evidence synchronization. Every member can apply the semantics at an actual
boundary; Python-specific provider mechanics apply only to Python members.
Scientific fidelity, native method bugs, UI adapters, service operation and result
schema implementation are owned by component teams.

## Acceptance criteria

- [x] Provider implementation and owned recipe are available in source (#22).
- [x] Canonical guide copies are synchronized (#63).
- [x] Study TopoMT's architecture and provider policies and publish an applicable
  shared contract, including bounded exceptions.
- [x] Put the recipe and a review worksheet in developer/starter guidance.
- [x] Inspect current MolSysMT/MolSysViewer declarations and exception compatibility
  without modifying active work; document deferred execution/migration gates.
- [ ] Verify an installable public provider release carrying the new capability.
- [ ] Record consumer dependency floors, installed evidence and adoption decisions
  under member reviews; migrate TopoMT's temporary fpocket availability handling
  after the provider release and preserve its custom command/error contract.

The normative record guards the policy decision. Existing starter generation and
offline registry/report checks verify that the new guidance is generated and linked
without acquiring dependencies. They do not test engine execution or science.

## Local implementation issues

- uibcdf/depdigest#22: provider publication and optional-engine adoption.
- uibcdf/topomt#56 and uibcdf/topomt#15: applicable consumer/support-library review;
  the fpocket compatibility handling remains linked to provider #22.
- uibcdf/molsysmt#244 and uibcdf/molsysviewer#110: existing ecosystem reviews,
  retained for member-specific follow-up. MolSysViewer constructor adaptation is
  a future local decision; the current signature accepts provider keywords.

The core execution-review deferral remains in force. Other consumers use their
existing ecosystem review only when a concrete optional boundary is introduced.

## Dependencies and risks

Provider release blocks replacing executable compatibility handling in public
consumers. New source-only capabilities require controlled CI pins and explicit
limits. Optional-engine environments and constructor contracts vary; unreviewed
rewrites could break clean import or established callers. This policy supplies
per-route evidence and exception requirements rather than speculative migration.

Next coordination review: 2026-10-30, or earlier when #22 publishes the capability.
The member implementing a compatibility exception must record its own responsible
maintainer and deadline; this central review date does not invent a local approval.

## Provenance

Linux coordination host, Python 3.13.15, 2026-09-30. Commands:
`python devtools/scripts/suite_status.py`, `git show origin/main:<path>` for the
source paths named above, `gh issue view`, and GH Run Receptor/native run inspection.
The original ArgDigest environment artifact and TopoMT version-file modification
were preserved; no neighboring worktree was edited. Historical scientific test
counts in #62/#22 are previous component evidence, not newly executed measurements.

## Central verification

The offline governance guard passed. All 155 existing central unittest checks passed,
including the three starter-kit checks. A fresh generated temporary registered
component contains the review worksheet with its resolved member identity and shared
contract link, and still has no runtime dependencies. `git diff --check` passed.
This verifies guidance generation and governance consistency, not scientific behavior.
