---
summary: A published policy snapshot cannot recognize members admitted after its registry froze.
issue: uibcdf/molsyssuite#73
status: partial
opened: 2026-10-02
closed:
severity: medium
verification: inspected
area: [governance, tooling, ci]
guard:
normative:
blocked_by: []
supersedes: []
---

# New-member admission and immutable engineering rules

## What and current evidence

OpenCASTp's official generated policy-v1.5.2 caller failed in run 37055145913
at source `c9a6f65ea6a7b76924f21df17c88830e745ca561`: the historical registry
did not contain its accepted central admission. A current-source bootstrap
could pass, but that did not prove adoption of the published gate.

The immediate member failure is now restored by an actual published snapshot:
OpenCASTp run 37156204129 at `f642e126e315846850faed4e68092ab3d84f8988`
passes the official `policy / conformance` job and executed conformance, Ruff
and formatting steps. Native referenced-workflow facts identify
`check-python-repository.yaml@policy-v1.5.4`; annotated tag object
`fe3fa73bc9def7331e349bc723bab7e635c34f04` peels to policy source
`e459ea0e8ac6aa8017e17a2f171c50d122b9e0b7`, which contains OpenCASTp.
This is governance evidence, not scientific qualification or public distribution.

## Why the general defect remains

`check_repository.py` loads engineering policy and membership from the same
bundled `suite.toml`; `bootstrap_component.py` generates its published caller
from the current policy release. A member admitted after that release can
again be missing from its immutable registry. The official starter therefore
needs an explicit admission-compatible route rather than an unexplained
current-main workaround. Existing policies must remain immutable.

## Accepted decision — 2026-10-03

The maintainer selected **separate immutable admission evidence**. The optional
`admission_sha` is a full lowercase central commit SHA reachable from the fetched
`origin/main` of `uibcdf/molsyssuite`. The gate checks out that repository explicitly,
reads only committed `suite.toml` data and executes only its frozen policy code.

Only the requested missing member is appended. Imported fields are `name`,
`repository`, `role`, `membership`, `maturity`, `development-mode` and `capabilities`.
Identity must be unique and classifications must use the frozen policy vocabulary.
No engineering policy, exception, review, guide relationships, other admissions,
Zenodo override or source code is imported. Existing member rows remain untouched.
Special requirements still need a reviewed policy profile or bounded exception;
the admission input cannot grant them. No input preserves the ordinary frozen gate.

The official starter reads the locally fetched published policy tag before writing
files. A current registration missing from that snapshot requires its published
`--admission-sha`, which is retained verbatim in the generated thin caller. Missing
policy tags or unaccepted admission references stop generation before any files.

Feature release `policy-v1.5.5` preserves Python/CI/publication baseline values and
explicitly keeps `policy-v1.5.4` compatible for existing transition members. Old tags
are unchanged. Existing OpenCASTp needs no migration to restore its already passing
1.5.4 gate. Later admissions can keep this feature policy frozen and change only
their reviewed admission commit. No scientific tests or internal push changes arise.

## Acceptance and owner handoff

- Record the chosen route and its precise admission/engineering boundary.
- Add an owning-tool regression with a new registration absent from an older
  policy, plus controls preventing unreviewed rule/exception drift.
- Qualify the versioned starter and published gate through native conformance
  before claiming delivery; retain historical failing runs.
- Communicate applicability and retire any obsolete bootstrap exception through
  uibcdf/opencastp#3 without absorbing its scientific/CI coverage work.

This report remains partial pending hosted qualification and delivery of the
implemented contract. Related starter/admission coordination is
uibcdf/molsyssuite#70. Source and native facts were inspected on 2026-10-03.
