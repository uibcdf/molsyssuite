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

- Root `AGENTS.md` contains repository-wide working actions and explicitly routes
  durable-instruction work through `MOLSYSSUITE_GUIDE.md#durable-working-instructions`.
  It requires reading `devguide/AGENTS.md` for work in that directory.
- Nested `AGENTS.md` contains actions specific to its directory. Every member has
  `devguide/AGENTS.md`, linking `../AGENTS.md`, `reporting_protocol.md` and the
  canonical guide's durable-instruction section. Preserve local report layouts,
  index commands, evidence vocabulary and specialized documentation rules.
- Read current maintained guidance and relevant active queues first. Use archive
  indexes for orientation; open an individual historical record for a stated
  question or current reference. Archived claims do not define current behavior.
- Link authoritative policies instead of copying their complete rules. Root and
  nested instructions remain local files; only registered canonical guides are
  synchronized byte for byte through the suite sync tool.

Existing instructions keep their applicable local scope. This policy is not a
request to rewrite product-specific conventions or sweep every technical fact
out of historical instructions. Correct a concrete stale instruction in its owner.
User authorization and explicit task instructions take precedence over local
workflow defaults; placing an instruction does not add an approval round.

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
routes, rejecting routes hidden in comments or fenced examples and missing local
targets. The component-guide audit calls the same checker; central governance
checks this repository. It proves routing, not scientific validity or the quality
of the prose. A reviewer must assess instruction relevance and local compatibility.

The versioned starter kit creates both instruction files from the first commit;
generation validates the common instruction routes. Existing-member adoption is
recorded in `devguide/rollouts/working_instructions.md`, separately from scientific
CI results and versioned Python policy callers. This administrative audit does not
require a scientific full suite or a blanket caller upgrade.

## Exceptions

A member unable to provide the common files/routes records a
`[[working-instruction-exceptions]]` entry in `suite.toml`: `repository`, owning
`issue`, `owner`, `reason`, `removal-condition` and ISO `expires-on`. Use a member
issue for local implementation, or a central issue for shared rollout work.
The checker honors only complete, unique, unexpired exceptions for registered
members. Expired or malformed entries fail governance validation. The rollout
must show the exception and next action; an exception is not completed adoption.
