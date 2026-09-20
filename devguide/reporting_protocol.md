# Reporting protocol

This document is normative for every repository registered in `suite.toml`. It governs
the relationship between GitHub issues, the developer-guide bug and proposal queues,
and the permanent archive of resolved records.

It adopts the repository-independent vocabulary proven in MolSysMT and MolSysViewer.
Repository-specific validators, labels and queue layouts may differ; the meanings below
must not.

## Universal rule

**Every queued document must have an issue in the repository that owns the work.**

Every member repository must implement this lifecycle for bugs and proposals. A member
may retain additional local kinds, fields, labels, directories and automation, provided
their semantics do not contradict this common core.

The two records have different jobs:

| Record | Holds | Changes |
| --- | --- | --- |
| developer-guide document | analysis, measurements, alternatives and refuted paths | continuously |
| GitHub issue | state and settled facts needed outside the repository | at opening and closing |

One independently closable theme has one issue and one or more documents. Plans,
inventories, release notes and meeting notes do not enter a queue until split into
closable themes.

## Identity and ownership

The issue reference is the stable identity. Local work uses the owning member's issue;
suite-wide work uses `uibcdf/molsyssuite`. Cross-repository references use
`uibcdf/<repo>#<number>`, never a path into a sibling's developer guide.

The owning `issue` always belongs to the responsible MolSysSuite repository. Dependency
fields such as `blocked_by` and `supersedes` may also use an upstream GitHub identity in
the general form `<owner>/<repository>#<number>`; external dependency does not transfer
ownership of the local report.

Use [`repository_contract.md`](repository_contract.md) to decide whether a theme is
central or local. A central decision may link local implementation issues; it does not
absorb their implementation analysis.

## Front matter

Every queued or archived report starts with:

```yaml
---
summary: One line describing the theme.
issue: uibcdf/<owning-repository>#1
status: open
opened: 2026-09-06
closed:
severity: medium
verification: asserted
area: [governance]
guard:
normative:
blocked_by: []
supersedes: []
---
```

`severity` is required only for bugs and is one of `critical`, `high`, `medium`, `low`.

Statuses are:

- open set: `open`, `active`, `blocked`, `partial`;
- closed set: `resolved`, `withdrawn`, `superseded`.

Verification describes the report's diagnosis, not the maturity of a feature:

- `reproduced`: executed and failed as described;
- `measured`: supported by recorded measurements and their command;
- `inspected`: verified by reading source or configuration;
- `upstream`: confirmed to originate outside the suite repository;
- `asserted`: believed but not yet checked.

Domain-specific evidence vocabularies remain local. A viewer, scientific library and CI
receiver do not prove their capabilities in the same way.

## Filing

1. Decide ownership using `repository_contract.md` and open the owning issue first.
2. Copy the repository's report template into the appropriate queue and fill its front
   matter.
3. Write the expanded What / How / Why analysis and acceptance criteria.
4. Regenerate the queue indexes.
5. Commit the issue and document references together; do not leave a cross-session gap.

The opening issue is telegraphic:

```text
What — the observed defect or proposed outcome
How — reproduction or implementation outline
Why — impact and evidence
Record — devguide/pending_.../<name>.md
```

Incoming issues may remain without a document while awaiting triage. Every queued
document must have an issue; not every issue must acquire a document. Bugs and proposals
remain synchronized by stable issue identity, not by matching titles or paths.

## Closing

A resolved theme requires the outcome, its record and one durable guard:

- a test or automated check named by `guard`; or
- a normative document named by `normative` when the outcome is a policy.

### Guard addressability and relevance

`guard` names a stable, locally runnable target that is expected to fail when the
reported defect is reintroduced. Closure makes two different claims:

- **addressability** is mechanical: the local validator proves that the registered
  runner understands the selector and resolves it to one or more tests or checks;
- **relevance** is reviewed: the resolution explains why the selected assertion
  exercises the failure mechanism described by the report.

Passing addressability never proves relevance. For example, an existing but unrelated
pytest node is mechanically addressable; a reviewer must still reject it as evidence for
the defect. Prefer a reproducer that failed before the fix and became the regression test,
then a controlled revert or mutation, then inspection of an existing assertion over the
repaired mechanism. When mutation is destructive or impractical, record the reviewer
rationale in the resolution.

The default Python profile accepts one safe pytest selector in one of these forms:

```text
tests/path/test_module.py
tests/path/test_module.py::test_name
tests/path/test_module.py::TestClass::test_name
```

`devtools/tests/` is also a valid root. A module selector must resolve to at least one
statically declared test. A node selector must resolve to the named function or class
method; checking only the file before `::` is not sufficient. The common static profile
does not accept globs, comma-separated targets, arbitrary command text or parameter IDs.
A repository may support parameter IDs or generated nodes only through a documented
local resolver that proves their collection. Use the module selector when the whole file
collectively protects one cross-cutting contract.

A non-pytest guard uses a repository-documented local profile that fixes the runner,
allowed roots, selector syntax and addressability check. Do not place shell commands in
front matter. Introduce a structured runner-and-target form centrally only after a real
second syntax cannot be represented safely by a local scalar profile.

These addressability rules apply prospectively to reports resolved on or after
2026-09-20. Historical archives are not invalidated merely because they used file-level
guards or an earlier local syntax. Correct a stale or fictitious historical selector when
it is encountered; open a separate audit if evidence shows broader archive debt.

Set `status` and `closed`, move the record to the repository's archive, regenerate the
index, and close the issue with the decision or fix, user-visible consequence, guard or
normative record, and archived record path. The issue and report must agree on whether
the theme is open or closed.

**Archive, never delete.** The archive may be flat, split into resolved bugs and
proposals, or retain an established equivalent such as `solved_bugs/`; the local
developer guide must document the mapping. In an open document, correct a false claim
in place. In an archived document, append a dated correction and do not edit the
original claim.

## Required local surface

Every member repository provides, either directly or through documented equivalents:

- pending bug and pending proposal queues;
- a permanent resolved-record archive;
- a report template carrying the common front matter;
- a generated index of queued and archived reports;
- an offline validator for identity, metadata, status and index consistency;
- contributor guidance that links this protocol and explains local paths and commands.

The offline validator is the mandatory merge gate. Network synchronization with the
GitHub board is a separate authenticated operation and may be manual or automated, but
it must be performed when filing and closing tracked reports. A temporary rollout may
document missing machinery; it may not redefine the shared meanings.

## Labels

- kind, exactly one: `bug`, `proposal`, `enhancement`, `documentation`;
- state, zero or one: `in-progress`, `blocked`, `partial`;
- triage: `needs-triage` for reports not yet attended.

No state label means open and unstarted. GitHub's closed state represents completion; a
separate `done` label is unnecessary.

## Security

An exploitable finding is not opened as a public issue. Report it through a private
GitHub security advisory. The public protocol resumes after a fix can be disclosed.

## Automated checks

The central repository runs locally:

```bash
python devtools/scripts/devguide_index.py
python devtools/scripts/validate_governance.py
```

Each member exposes equivalent local commands in its contributor guidance. Validators
must remain useful without credentials or network access. A board synchronization check,
when present, complements rather than replaces the offline validator.
