---
summary: Admit compatible Mamba 2 updates and notify excluded upstream major releases.
issue: uibcdf/molsyssuite#116
status: active
opened: 2026-10-13
closed:
verification: inspected
area: [governance, tooling, compatibility]
guard: tests/test_upstream_release_watch.py
normative: devguide/conda_environment_tools.md
blocked_by: []
supersedes: []
---

# Ongoing Mamba compatibility and major-release notices

**Reported:** Principal maintainer identified the risk of permanent exact-version
admission after the first #116 delivery and requested notification when Mamba 3 appears.
**Status:** Implementing the accepted follow-up; hosted qualification is pending.

## What

The first delivery `69c9ad4d0c3fcc2ec9cc5a601e82826593d3d723` admitted only Mamba
2.9.0 for exclusive creation. The new reviewed boundary is stable `>=2.9.0,<3`,
Linux x86_64 creation. New minor/patch versions are accepted as compatible and
observed during use; version-specific executed evidence is not inferred from the
range. Configured behavior, source inputs, scientific/publication contracts and
all other unsupported manager/platform/update routes remain unchanged.

## How

The existing operator records actual manager version, range and qualification
scope. Baseline and latest admitted Conda versions execute the same native guard
on relevant changes, manual dispatch and weekly. Actual positive/negative,
warm-cache and archive-digest controls produce retained version-specific receipts.
A separate trusted-main job queries the official latest stable GitHub release,
including excluded majors. It creates one proposal per excluded major through the
reusable release watcher, respecting existing open/closed owner decisions.
Monitoring/release failures remain visible; there is no automatic major admission.

## Why

An exact baseline need not pin the future ecosystem. Explicit range assumptions,
periodic executed controls and a durable major-release notice keep compatibility
review actionable without adding scientific suites or changing component releases.

## What is measured and what is assumed

Official GitHub latest release inspected 2026-10-13: stable Mamba 2.9.0, published
2026-08-07. Mamba 3 is a hypothetical future control, not an existing stable release.
Local interpreter: qualified Python 3.14.7, both editable receptor origins verified;
accepted seven #82 dependency conflicts retained. The original native baseline
receipt remains unchanged. No future Mamba version has been executed locally.

First hosted monitor `38438697842` at `96ba69b` successfully executes the official
release observer; both native jobs stop at import because the new public tools
environment omitted Jinja2, an existing SDK dependency. No native pass or artifact
qualification is inferred. The workflow now declares Jinja2 explicitly; recovery
requires actual new-head hosted execution, not the observer's administrative pass.

## Alternatives and refuted paths

- Exact-only admission was initially safe but can remain stale without review.
- Unbounded `>=2.9.0` would admit future major contracts without a review boundary.
- Declaring every admitted minor tested would manufacture evidence.
- A log-only major warning can be missed; a central owning issue provides follow-up.
- Repeated issues or reopening closed decisions would ignore human dispositions.

## Scope and exclusions

Shared channel SDK compatibility, administrative CI and authorized central release
notices. No scientific component changes, active environment changes, member pin
rollout, publication plan, runtime floor or common scientific gate.

## Acceptance criteria

1. Stable compatible 2.x updates admitted, older/major/prerelease bounds guarded.
2. Native baseline/latest selected in actual hosted CI, with exact version receipts.
3. Stable current release makes no notification; simulated Mamba 3 produces a
   structured owning notice without a real fabricated issue. Existing and closed
   decisions remain idempotent; invalid identity/API state fails before mutation.
4. Weekly/manual/main monitoring and restricted issue-write permissions documented.
5. Immutable provider and verified hosted checkpoint handed to the actual consumer.

## Local implementation issues

uibcdf/pharmacophoremt#10/#23 own adoption and installed/public validation.
No consumer migration is performed. Candidate reuse remains distinct for
uibcdf/elastnetmt#18, uibcdf/lindelint#13 and uibcdf/topomt#78.

## Dependencies and risks

Weekly GitHub scheduling may be delayed; this does not promise immediate notification.
The bounded 2.x range is a compatibility assumption subject to observed CI/runtime
failures. Major review stays a deliberate owner decision. Existing closed follow-ups
are not reopened, including deferred/rejected releases. GitHub API/token availability
and notification permissions are explicitly operational requirements.

## Provenance

Original implementation and native receipt: shared `69c9ad4`; official release:
https://github.com/mamba-org/mamba/releases/tag/2.9.0. Existing workflow installation
route reuses `mamba-org/setup-micromamba@v3.2.1`. New controls reuse the owned SDK and
native test fixture; upstream watching belongs to an independently reusable operation,
not scientific code or a new third-party Action.
