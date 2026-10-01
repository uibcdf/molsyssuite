---
summary: Share optional-engine boundary semantics and adoption evidence across members.
issue: uibcdf/molsyssuite#62
status: resolved
opened: 2026-09-30
closed: 2026-10-01
verification: measured
area: [governance, dependencies, compatibility]
guard:
normative: devguide/optional_engine_integration.md
blocked_by: []
supersedes: []
---

# Shared optional engine contract

**Reported:** 2026-09-30, following TopoMT optional-engine consumer work.
**Status:** Resolved; shared policy, guide distribution, provider publication and
TopoMT availability migration are verified. Broad member reviews retain their own
issue ownership and the maintainer-requested core execution deferral.

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
- [x] Verify an installable public provider release carrying the new capability.
- [x] Record consumer dependency floors, installed evidence and adoption decisions
  under member reviews; migrate TopoMT's temporary fpocket availability handling
  after the provider release and preserve its custom command/error contract.

The normative record guards the policy decision. Existing starter generation and
offline registry/report checks verify that the new guidance is generated and linked
without acquiring dependencies. They do not test engine execution or science.

## Local implementation issues

- uibcdf/depdigest#22: provider publication and optional-engine adoption.
- uibcdf/topomt#56 and uibcdf/topomt#15: applicable consumer/support-library review;
  the fpocket migration is verified against provider #22; broader reviews remain open.
- uibcdf/molsysmt#244 and uibcdf/molsysviewer#110: existing ecosystem reviews,
  retained for member-specific follow-up. MolSysViewer constructor adaptation is
  a future local decision; the current signature accepts provider keywords.

The core execution-review deferral remains in force. Other consumers use their
existing ecosystem review only when a concrete optional boundary is introduced.

## Dependencies and risks

At the initial coordination stage, provider release blocked replacing executable
compatibility handling in public consumers; the measured resolution below clears
that block. New source-only capabilities require controlled CI pins and explicit
limits. Optional-engine environments and constructor contracts vary; unreviewed
rewrites could break clean import or established callers. This policy supplies
per-route evidence and exception requirements rather than speculative migration.

The initially scheduled coordination review was 2026-10-30, or earlier when #22
published the capability; the 2026-10-01 resolution below completes that review.
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

## Component-facing guide rollout

The maintainer requested that the common recipe be required wherever the optional
boundary applies. `MOLSYSSUITE_GUIDE.md` now summarizes those circumstances,
provider/consumer responsibilities, independent evidence and bounded exceptions.
All fifteen registered consumers receive its byte-identical copy through the central
synchronizer. Publication and remote-copy verification are recorded below as they
complete; this guidance distribution does not itself certify runtime adoption.


## Resolution and measured rollout: 2026-10-01

The shared contract is accepted, linked from ecosystem/starter guidance and
required by the component-facing guide at applicable optional boundaries.
Canonical `MOLSYSSUITE_GUIDE.md` commit `ec36b13` has SHA-256
`0cafc8dd3cd7624888aed171f9b7c14ca98f3ab8522965ac88e2fe13b426f4a5`.
All fifteen consumer root copies match, distributed through the canonical
synchronizer. Direct documentation commits preserve each component's skipped-CI
recovery debt; no scientific full matrix was claimed from these pushes.

| Consumer | Guide commit |
| --- | --- |
| uibcdf/smonitor | 687d66599cf9a7bcbaa9be8cc9af2fc3e30c2762 |
| uibcdf/argdigest | 0defde0d171a7262b54892bbfa15b8d8690f374c |
| uibcdf/depdigest | b6e023859772537c7f7b79ebc3a6a1de294804f0 |
| uibcdf/pyunitwizard | 976bc78deda497f8d4961d49a261703a2a88113e |
| uibcdf/pytest-receptor | 25307b6952a147ca2e9a7370c157bdce69420c21 |
| uibcdf/gh-run-receptor | 30c35eecfaaf2c6d922a41214f9c2829e9db6feb |
| uibcdf/molsysmt | 1d66bf1247ed450e40a4d2d18fc6d0501a8bbb20 |
| uibcdf/molsysviewer | 8ac983aaa777601b2f3c7526736f631638c48839 |
| uibcdf/topomt | fdf85fa6c603d2c456e5634e6ecb5a6ad3203951 |
| uibcdf/pharmacophoremt | d57caf55962cc24aa67520adecf1a7f283d0767c |
| uibcdf/elastnetmt | 587e60bbec8d490b0f56c8b527dc585f94addaef |
| uibcdf/dockingmt | 5efc72e8e8d67994c71a4c6f62e763c66284d478 |
| uibcdf/ackredit | 5fd8e0d9beee12799d71811aeb935a26ba863fbf |
| uibcdf/lindelint | 858a0e523b59830de0c945943106c5227cebee40 |
| uibcdf/molsys-ai | 8797e93e661c620f4e78a4567ab1e205ffb9aef4 |

Hosted vendored audit `36787721831` and component-guide audit `36788852416`
passed; the latter verifies all sixteen repositories including the authority.
Fourteen consumers passed full local repository conformance. MolSys-AI retained
three pre-existing README badge findings; before/after inspection showed only
its guide drift was removed. Those findings do not invalidate its byte-identical
guide and are not claimed resolved by this rollout.

DepDigest stable release `0.12.0` identifies immutable source
`0da46d9ff31fbe2f92e4e667a32868aebe840b39`.
Exact-source matrix `36788849230` and installed-artifact matrix `36823713839`
passed all twelve Linux/macOS/Windows × Python 3.11–3.14 cells, with actual
verification steps inspected. Suite policy `36788753565` passed. Staging producer
`36789413638` and promotion `36824539168` passed; the latter added public `main`
to the same immutable file and retained `staging`. Public file
`noarch/depdigest-0.12.0-py_0.tar.bz2` has SHA-256
`03d5aa569bfeb95bdd253a52e68e59094d9af5a6c4c7bc4ba228d3e36cfb30a3`.
An independent public download matches; a fresh public-channel Linux/Python
3.13.15 environment verified version, off-checkout import, public URL/digest,
optional-engine contract and launcher. The release-event route selection
`36824505071` and documentation publication `36824505069` passed. No tag moved,
file overwritten or failed gate waived. The provider archive is
`devguide/completed_proposals/optional_scientific_engines.md` under
uibcdf/depdigest#22, published in `8ef9a56`.

TopoMT adopted that provider in `1aa25c4`, declared >=0.12.0 in its relevant
runtime manifests, aligned its already declared hard dependency closure and
updated only its controlled DepDigest source pin to the release commit. Its
other pins, special scientific profiles and Python range remain intact. fpocket
availability now checks the actual configured command through DepDigest and
translates only an explicit absence sentinel into the established FpocketError
contract. Provider/import/filesystem/execution failures remain distinct.
Six availability regressions and seven administrative checks passed locally
against both staged and clean public artifacts. Full Ruff lint/format over
383 files and scoped mypy passed. Focused manual workflow `36825125490` passed
all six Linux/macOS × Python 3.11–3.13 cells, checking the exact public artifact
origin/version/URL/digest before the real source runner checks.

The focused workflow does not execute scientific engines or import the heavy
TopoMT orchestration facade. It introduces no per-push full-suite requirement,
branch-protection check or successful scientific-recovery watermark. Broader
TopoMT support-library and scientific work remain under uibcdf/topomt#56/#15
and component-owned defects. MolSysMT/MolSysViewer execution reviews remain
deferred under uibcdf/molsysmt#244 and uibcdf/molsysviewer#110. Future components
apply the contract when an applicable route is introduced or changed; bounded
exceptions and per-route evidence remain mandatory. Those phased member reviews
do not block closure of the delivered shared capability and governance contract.

The normative document is the durable policy guard: it fixes applicability,
ownership, exception rules and independent evidence requirements. Provider and
consumer regression guards protect the implemented availability mechanisms;
central generation/governance checks protect distribution and starter guidance.
