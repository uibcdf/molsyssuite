# Member classification

This document is normative for the classification of repositories registered in
`suite.toml`. Each field answers one question. Values from different fields must not be
combined into a single cohort or inferred from one another.

## Role

`role` identifies the member's primary function and supplies its public MolSysSuite
identity. It has exactly one value:

- `scientific-component`: a user-facing tool for scientific work;
- `support-library`: a reusable runtime capability consumed by other components;
- `developer-tool`: a tool for development, testing, CI, publishing or maintenance;
- `specialist-subsystem`: a governed subsystem that provides a coherent specialized capability through multiple internally coordinated repositories.

A role does not assert maturity, priority or implementation technology.

## Membership

`membership` describes the member's relationship to the suite:

- `primary`: a principal component whose needs inform suite-wide planning;
- `auxiliary`: a UIBCDF component that supports the suite without blocking its principal
  milestones.

Both values identify fully governed MolSysSuite members. `auxiliary` does not mean
external, unmaintained or exempt from common policy.

## Maturity

`maturity` records the strength of the component's current public contracts:

- `incubating`: scope, architecture or public API may still change substantially;
- `stabilizing`: the component is consolidating its API, tests, documentation and release
  discipline;
- `stable`: documented public contracts carry an explicit compatibility and maintenance
  commitment.

A version number alone does not establish maturity. Moving a member to `stable` requires
a deliberate registry change with repository evidence.

## Development mode

`development-mode` records the expected kind of ongoing work, independently of maturity:

- `active`: feature development and maintenance may both continue;
- `maintenance`: planned work is primarily corrective, compatibility or security
  maintenance.

A stable component may use either mode. Maintenance mode is not deprecation and does not
weaken existing support commitments.

## Capabilities

`capabilities` is a non-empty list of technical properties that activate concrete common
policies. A value must not be added only as a descriptive label.

The current vocabulary contains:

- `python-package`: activates the common Python version, Ruff, pytest, packaging and Python starter-kit rules;
- `governed-subsystem`: identifies a member that owns an internal registry/governance layer. It activates subsystem-boundary validation rather than implying that all internal repositories are MolSysSuite members.

Additional capabilities are accepted only together with a policy or automated behavior
that consumes them. Scientific purpose belongs to `role`; auxiliary membership belongs
to `membership`; neither is a capability.

## Initiatives

An initiative records temporary coordinated work and is not a member classification.
`initiatives.stabilization.priority-members` currently identifies SMonitor, ArgDigest,
DepDigest, PyUnitWizard, MolSysMT and MolSysViewer as the first repositories on which the
suite is concentrating stabilization work.

Initiative statuses are `planned`, `active`, `paused`, `completed` and `cancelled`.
Completing or reprioritizing an initiative must not silently change any member's role,
membership, maturity, development mode or capabilities.

## Current conservative assignment

The registry marks TopoMT, PharmacophoreMT, ElastNetMT, Ackredit and DockingMT as
`incubating` and the other members as `stabilizing`. No member is declared `stable`
without a separate evidence-backed decision. Lindelint is the only `auxiliary` member.
Every current member is in active development. Package members carry the `python-package` capability; MolSys-AI is a primary incubating `specialist-subsystem` carrying `governed-subsystem` and governs its Server, Client, and Agent repositories internally. Ackredit is a primary support library and DockingMT is a primary scientific
component; neither belongs to the stabilization priority list or the Python 3.14
transition cohort, so their current range remains Python 3.11--3.13.

Historical reports may retain terms such as “wave 1” or “infrastructure cohort” because
they record the vocabulary used at the time. New policy, tooling and planning records use
the independent fields defined here.
