# Durable contributor and agent instructions

This policy applies to MolSysSuite and every repository registered in `suite.toml`,
including incubating members and governed subsystems. MolSysSuite owns this member
contract under uibcdf/molsyssuite#66; MOLI owns cross-platform working contracts.

## From a finding to an accepted instruction

Report actionable defects, missing capabilities and improvements through the
[reporting protocol](reporting_protocol.md) and
[cross-component feedback route](cross_component_feedback.md). Keep technical
behavior, reproductions, API constraints and workarounds in the owning issue,
implementation, regression tests and maintained technical documentation.

An investigation warrants an `AGENTS.md` instruction only when normal repository
review accepts a lasting action for contributors or agents across future tasks.
State the action, its applicability and the policy or maintained document that
owns its rationale. Put the accepted instruction in the change that settles it,
or leave an owned adoption issue when placement requires separate work. A defect
does not automatically require an instruction or another issue.

For example, a failing launcher belongs in its packaging issue and test; an
accepted requirement to verify installed launchers before release belongs in
release guidance and can be routed from contributor instructions. A one-time
traceback, package version or command result is evidence, not a durable rule.

## Placement and authority

Accepted separation and all-member rollout: uibcdf/molsyssuite#149.

- `MOLSYSSUITE_GUIDE.md` is the mandatory synchronized common-instruction layer,
  routing every accepted policy in `suite.toml`. Within their stated scope its
  common rules prevail over root and nested local instructions. Local additions
  refine repository/scientific contracts; a conflicting deviation needs the
  owning policy's bounded exception. Stricter specialized gates remain local.
- Root `AGENTS.md` starts with the small mandatory read/follow and scoped-precedence
  entry emitted by `agent_instructions.render_entry()`. It routes reusable-tool
  ownership and durable instructions into the common guide and requires
  `devguide/AGENTS.md`. The remaining file contains local commands, source-layout
  constraints, accepted scientific/product invariants and other local actions.
  Do not duplicate global CI, release, feedback, resource or tool-use policies.
- Nested `AGENTS.md` refines directory-specific local behavior under that common
  layer. Keep `devguide/AGENTS.md`, the actual reporting protocol/index commands,
  specialized documentation rules and current/history distinctions. A local
  precedence statement cannot reverse the common layer.
- Read current maintained guidance and relevant queues first. Archive indexes
  orient; individual historical records answer a stated question. Preserve
  archived claims and append dated corrections.
- Only registered canonical guides synchronize byte for byte. Root/nested files
  remain owner-local and can evolve without copying an entire shared template.
  Write maintained repository artifacts in English, preserve human work and
  confidentiality, and do not infer science/publication from structural checks.

The required entry is intentionally small and stable. Run the shared generator
for new components and its checker after adapting an existing repository. Retain
all applicable local scientific gates, dependency environments, and runtime/GUI
limits. Route missing reusable capabilities to their owners with consumer evidence.
Human authorization and higher-priority session instructions retain their authority;
this precedence does not introduce another permission request for authorized work.

The canonical summary links the full policy inventory; a new accepted policy must
have an active canonical route. Semantic review separately checks contradictory
local commands or prohibitions, actual ownership and applicable exceptions.
Examples such as a W0-only issue ban or ask-before-every-commit default must not
silently defeat normal authorized issue feedback or the principal-maintainer route.

## Feedback beyond one member

Propose a potentially shared working rule in `uibcdf/molsyssuite`, linking the
incident, accepted local action, evidence of relevance to other members,
affected scope and exceptions. Propose a cross-MOLI contract in `uibcdf/moli`;
linked platform and suite issues must each own distinct work. Upstream acceptance
does not silently change member obligations: MolSysSuite reviews its own policy,
starter path, rollout and checks.

The contributor-instruction part of uibcdf/molsyssuite#65 was accepted on
2026-10-10: surface actionable findings, including uncertain and nonblocking
ones, and explicitly offer their owning issue to the human collaborator at a
natural pause. Follow
[the canonical feedback action](../MOLSYSSUITE_GUIDE.md#human-facing-issue-feedback).
Existing authority to report the same work remains valid without another approval
round. A declined or deferred human disclosure does not authorize publishing that
human's material; retain only an authorized sanitized disposition. The universal
reporting commitment continues to govern otherwise authorized actionable findings.

Use the same root/nested routes, starter and registered exception mechanism.
Platform-wide adoption is coordinated with uibcdf/moli#34; MolSysSuite owns this
accepted member instruction. The scientist-facing pilot, opt-in verified-fix
notifications and automatic task retries remain pending in #65. Instruction
adoption alone cannot close that full objective or certify scientific behavior.

## Mechanical conformance and adoption

`devtools/scripts/agent_instructions.py` checks file presence and explicit active
routes, required reading, scoped precedence and missing local targets. It rejects
optional, negated, quoted or fenced stand-ins for the mandatory entry. The component-guide audit calls the same checker; central governance
checks this repository. It proves routing, not scientific validity or the quality
of the prose. A reviewer must assess instruction relevance and local compatibility.

The versioned starter kit creates both instruction files from the first commit;
generation validates the common instruction routes. Existing-member adoption is
recorded in `devguide/rollouts/working_instructions.md`, separately from scientific
CI results and versioned Python policy callers. This administrative audit does not
require a scientific full suite or a blanket caller upgrade. The guide audit can
write a bounded `molsyssuite.component-guide-audit@1` receipt with registered
repository, exact Git source, three input digests and finding codes. It includes
no instruction contents/private paths and rejects uncommitted audited inputs.
Trusted hosted audits retain these receipts independently from test/publication
artifacts. Final common-guide and component delivery evidence remains in the
current rollout receipt.

## Exceptions

A member unable to provide the common files/routes records a
`[[working-instruction-exceptions]]` entry in `suite.toml`: `repository`, owning
`issue`, `owner`, `reason`, `removal-condition` and ISO `expires-on`. Use a member
issue for local implementation, or a central issue for shared rollout work.
The checker honors only complete, unique, unexpired exceptions for registered
members. Expired or malformed entries fail governance validation. The rollout
must show the exception and next action; an exception is not completed adoption.
