---
summary: One line describing the defect or proposal.
issue: uibcdf/molsyssuite#000
status: open
opened: 2026-01-01
closed:
severity: medium
verification: asserted
area: []
guard:
normative:
blocked_by: []
supersedes: []
---

# Title describing the theme, not its preferred solution

**Reported:** Date and how this surfaced.
**Status:** One line agreeing with the `status` field.

Remove `severity` for a proposal. Keep unknown diagnoses explicit and use
`verification: asserted` until they are checked.

## What

For a bug, paste the smallest reproduction and its observed result. For a proposal,
describe the proposed outcome in one paragraph.

## How

For a bug, identify where it fails or say that the cause is unknown. For a proposal,
describe the design in enough detail to evaluate it.

## Why

State the suite-wide impact and the evidence behind it.

## What is measured and what is assumed

Separate measurements from assumptions. A measurement includes the command and
environment that produced it.

## Alternatives and refuted paths

Record alternatives considered and why they lost. Leave this section explicitly empty if
nothing has been evaluated yet.

## Scope and exclusions

Name the affected profiles and repositories. State what looks related but is excluded.

## Acceptance criteria

List observable conditions required to close the central issue. Identify the future
`guard` or `normative` record.

## Local implementation issues

List only member repositories requiring concrete changes, using stable issue references.

## Dependencies and risks

Put tracked dependencies in `blocked_by`, not only in prose.

## Provenance

Required for measurements: date, host, Python and relevant dependency versions.
