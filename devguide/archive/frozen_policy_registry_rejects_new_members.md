---
summary: A published policy snapshot cannot recognize members admitted after its registry froze.
issue: uibcdf/molsyssuite#73
status: resolved
opened: 2026-10-02
closed: 2026-10-04
severity: medium
verification: reproduced
area: [governance, tooling, ci]
guard: tests/test_suite_policy.py::ImmutableAdmissionTests::test_generated_admitted_member_passes_frozen_checker_and_retains_sha_in_caller
normative: devguide/new_component_starter_kit.md
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

The implementation and scoped hosted qualification are delivered.
Related starter/admission coordination is
uibcdf/molsyssuite#70. Source and native facts were inspected on 2026-10-03.


## Resolution and delivery — 2026-10-04

Feature source `7a8df7e699952b3647228b38409b488bc2e61ad0` is published as
`policy-v1.5.5`; hosted governance run 37160195310 passes all 304 central tests.
The official generator was also run against that real locally published tag
and central admission `2a0b223afe78aa089ea27fb1042e4c85ca8f5921`, then its
output passed the checker. This real invocation uses an already registered
member; absence in a frozen registry is exercised separately by the regression.

OpenCASTp manual wrapper `4bff51f4c1e1dfb1d33a6af33e556832674ef8ea`, on
reviewed source `f642e126e315846850faed4e68092ab3d84f8988`, ran published
policy-v1.5.5 in native [37161230920](https://github.com/uibcdf/opencastp/actions/runs/37161230920).
Both ordinary and explicit-admission conformance jobs pass. The explicit job
actually validates the input, checks out central data, verifies published main
ancestry and executes conformance; both execute Ruff and formatting. It does
not change OpenCASTp main's caller or execute science. The regression's frozen
fixture first returns UNREGISTERED, refuses generation without admission,
then generates a pinned caller and passes conformance with admission. Removing
the missing-member overlay makes this assertion fail. Companion tests protect
committed data/main ancestry and prohibit rule, exception or classification drift.

The official synchronizer delivered the canonical guide to all 16 registered
consumers; their guide/instruction routes pass. Documentation-only commits
with [skip ci] are published for each, retaining their existing workflow callers.
`devguide/rollouts/immutable_admission_73.json` records those commits, hashes
and the qualified gate. Existing 1.5.4 callers retain compatibility, including
MolSysMT and MolSysViewer. Their active developer clones and scientific suites
are untouched. Notice/obsolete bootstrap handoff is in uibcdf/opencastp#3, which
remains open for its component CI/scientific coverage scope.

The next official new-component admission must provide its own reviewed central
commit if absent from its chosen feature policy; it need not publish new rules.
No fabricated new member was added to the real registry to obtain this evidence.

Native referenced-workflow evidence resolves to annotated tag object
`00885245bafe745a8e4466d9aab76720eb4bbca3`, independently peeled to the
accepted immutable policy source above. Both the tag object and source commit
are retained in the delivery record; they are different Git identities.
