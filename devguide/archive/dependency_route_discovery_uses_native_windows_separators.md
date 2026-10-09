---
summary: Shared dependency route discovery compares Windows separators with portable inventory paths.
issue: uibcdf/molsyssuite#112
status: resolved
opened: 2026-10-09
closed: 2026-10-09
severity: medium
verification: reproduced
area: [governance, packaging]
guard: tests/test_dependency_routes.py::DependencyRoutesTests::test_windows_discovery_matches_portable_inventory_and_retains_refusals
normative: dependency_route_preflight.md
blocked_by: []
supersedes: []
---

# Dependency route discovery on Windows

**Reported:** Original SMonitor scheduled CI exposed during uibcdf/molsyssuite#39
reconciliation on 2026-10-09.
**Status:** Provider source correction and regression complete; optional native
receiving remains uibcdf/smonitor#46.

## What

SMonitor schedule 37935661439 at
`7ed94f1677965b0281c883dda784fd480be42c29` uses shared SDK
`25363f2a2c902c04b2cdc8b301a3e1c1ff0c0918`. All four Windows Python
3.11–3.14 jobs fail `Check distribution inputs` before installation/tests:

```text
unclassified/missing routes:
  new=['devtools\\conda-build\\meta.yaml']
  missing=['devtools/conda-build/meta.yaml']
```

Four Linux and four macOS test cells succeed, but the overall schedule fails;
it cannot clear full-matrix debt. This is a shared administrative identity
comparison, not a diagnosed scientific defect.

## How

`dependency_routes.py::_files` used `str(path.relative_to(root))`, rendering
native backslashes on Windows. The inventory uses portable relative paths.
The operation now uses `as_posix()` for discovered identities. Actual filesystem
reads, root containment, inventory membership, requirements and exact workflow
byte hashes retain their existing contracts. Existing @1/@2/@3 and directory
profiles use the same operation; no new field or broad path waiver is added.

The audit-level regression reads real recipe/environment/workflow files while
only discovery renders relative paths through `PureWindowsPath`. It fails on
the original provider with the same observed mismatch, then passes after the
correction. In that same scenario, a newly unclassified environment and a changed
workflow digest still fail. This guard is relevant to the actual failure
mechanism and remains a local addressable pytest node.

## Why

Supported Windows source routes are blocked before package tests by the shared
provider. Registered distribution reviews identify twelve current preflight
clients/candidates. SMonitor is the demonstrated Windows consumer; notice to
another member does not assert that it invokes this operation on Windows.

## Measurements and limits

Qualified Linux `molsyssuite@uibcdf_3.14`, Python 3.14.7; both Receptors import
from the original local editable clones. The seven accepted #82 dependency
closure findings remain unchanged. Before correction, the new regression fails.
After correction, 46 route/context/constraint tests pass, plus applicable Ruff
lint/format and offline governance. No component science, solver, installation
or package operation is performed. Native central publication evidence is verified
and handed off in the owning issue after the unskipped commit.

The regression proves Windows path semantics over the real audit, not actual
native Windows receiving or a public artifact. SMonitor #46 must review the
accepted immutable SDK against its caller, then retain executed native Windows
preflight evidence before claiming that source route recovered. Current pins
remain unchanged, as do original public 0.19.0 bytes and their installed receipts.

## Alternatives and refuted paths

Rewriting inventory paths to backslashes breaks portable identities and hides
missing routes on other operating systems. Ignoring membership/hash failures
weakens validation. Rebuilding or republishing a package does not repair this
source tool. No change to scientific selection or broad SDK rollout is needed.

## Scope and acceptance

Provider discovery, reproduced audit regression, retained negative controls,
central native governance and immutable optional handoff complete this source
correction. Actual consumer adoption/native runs remain separately owned.
No new CI pilot gate/cohort, policy version, artifact, dependency minimum,
credential operation or mandatory consumer migration follows. Shared notices
precede provider publication; their exact URLs and bounds are retained in
[the receiving receipt](../rollouts/ci_receiving_and_portable_routes_39_112_20261009.json).

## Coordination and provenance

- uibcdf/molsyssuite#112 owns shared correction.
- uibcdf/smonitor#46 owns demonstrated Windows receiving.
- uibcdf/molsyssuite#39 owns actual CI review and informational pilot.
- uibcdf/molsyssuite#45 retains distribution governance/artifact distinctions.

Primary clones, caller-owned environment, scientific deferrals, active PyUnitWizard
OpenFF work and private OpenCASTp #102 remain unchanged. Historical dated evidence
is retained; source qualification does not certify later runtime or clear debt.


## Receiving follow-up — 2026-10-09

SMonitor #46 deliberately adopts accepted SDK `6d6172d` in all paired preflight
callers. Native first recovery 37994715796 proves portable discovery is corrected
but Windows checkout CRLF conversion trips the retained exact-workflow-byte gate.
The owning checkout now pins LF workflow bytes, with an actual Git regression
failing before and passing after. Source `57bcf31` full matrix 37995139887
independently verifies all twelve Linux/macOS arm64/Windows Python3.11–3.14
preflights and source test cells. This supplements the original Linux source
regression with actual native receiving evidence; other SDK clients keep their
existing pins and independent adoption decisions. Failed executions and original
public 0.19.0 qualification retain their scope. Receipt:
[Windows receiving](../rollouts/smonitor_portable_preflight_receiving_39_46_20261009.json).
