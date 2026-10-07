---
summary: Qualify immutable VCS dependency installations in the shared source-route preflight.
issue: uibcdf/molsyssuite#107
status: active
opened: 2026-10-06
closed:
verification: inspected
area: [governance, compatibility, distribution, tooling]
guard: tests/test_dependency_route_contexts.py
normative:
blocked_by: []
supersedes: []
---

# Immutable VCS dependency qualification

**Reported:** 2026-10-06 during uibcdf/elastnetmt#18 / central #45.
**Status:** Principal maintainer accepted the optional general Git/context route
on continuation. Shared @3 implementation and qualification are in progress;
existing source pins/transport and scientific scope remain preserved.

## What

The accepted dependency-route tool must be able to audit real supported consumer
installations without weakening their requirements or needlessly changing their
scientific inputs. ElastNetMT's current fixed Git installations and Python-specific
source selections are outside the tool's existing directory-only source profile.
Add an optional general contract or explicitly migrate those installations while
preserving their selected commits, versions and scientific test scope.

## How

At accepted SDK `38db709ecc07451ff36ea84573d585f9af6b4df7`,
`dependency_routes._source` accepts only `pip-no-deps-directory`; it checks one
clean checkout per required provider, then installed directory provenance and
version. `validate_source_version` additionally rejects metadata without explicit
version constraints. CLI declaration-only mode still calls the source checker.
These are inspected bounded implementation limits, not scientific failures.

ElastNetMT source `ef9d04b5975b2b49439bd7d9c2bda43c9fc348e5` has ten required
runtime dependencies without invented scientific API floors. Its current routes:

| Consuming scope | Existing installation inputs |
| --- | --- |
| Python 3.11/3.12 source CI | `devtools/requirements/controlled_suite_dependencies.txt`: SMonitor, DepDigest, PyUnitWizard, ArgDigest, LinDelINT full Git revisions over the Conda bootstrap |
| Python 3.13 source CI | Same file plus a separately pinned MolSysMT `3bcfaf4d50df6c84ebd14505790ed5221543e5de`; specialized scientific environment |
| Python 3.14 source CI | `devtools/requirements/controlled_suite_dependencies_py314.txt`: differing LinDelINT revision plus MolSysMT `3eb5afd1de087f775b78d7fa45ad69cca3a02d43` and MolSysViewer `ec4c71e574d798b7c8675b7e7e983da878ce9889` |
| Documentation | Public Conda dependencies, no fixed sibling source substitutions |
| Current Viewer add-on probe | Python 3.13 fixed core providers followed by an intentionally current `molsysviewer.git@main` installation |

The ordinary shared runtime channel profile accepts uibcdf/conda-forge (and
nodefaults in @2); current specialized environments also retain ambermd. Some
required packages are deliberately replaced after Conda bootstrap. The current
profile prohibits simultaneously declaring a provider as Conda and source-supplied.
Those realities need explicit classification, not silent filtering or blanket
exemptions. The exact source files and scientific CI have been retained in the
independent resource/publication work.

Recommended design: optionally bind each consuming environment/Python context
to its reviewed source manifest; validate repository/full commit and actual
installed Git provenance/version, preserving every declared metadata bound.
Any explicitly reviewed source overlay retains its bootstrap and final-provider
identity separately. Extended channels have a stated purpose and priority mode.
Declaration-only evidence validates inputs but cannot certify actual installation.
An unbounded required dependency still needs valid installed identity/version;
the audit must not invent an API floor to accommodate itself.

The existing directory and source-free contracts remain compatible. The
accepted implementation adds optional @3 context/Git support; no existing
consumer schema or immutable pin is automatically migrated. Independently useful parsing/provenance
operations belong to MolSysSuite, with public contracts and tests; consumers keep
their selected pins, contexts and invocation policy locally.

## Why

Transport changes, forced dependency floor decisions or removal of scientific
bootstrap packages can disturb active component development. The shared tool is
the owner of parsing/provenance comparison, while the consumer owns scientific
input selection. A reusable optional profile supplies trustworthy early evidence
without making every component use the same installation method.

## What is measured and what is assumed

The implementation and cited source/workflow/environment files were inspected.
The shared profile's rejection rules are explicit in its code and maintained
documentation. Nine independent owner archive/descriptor tests pass with SDK
38db709 under Python 3.14.7, but they do not qualify these VCS/context routes.
At initial inspection, no scientific run, installed VCS qualification,
credential probe or real package build had been performed. The later isolated
Git provenance check below is separate from full consumer qualification.

The first consumer supplies actual need; generic usability for other components
is a design target. A source installation receipt is not an archive/native-byte,
import, scientific or public-delivery proof. Current source-only or private
providers retain their existing evidence limitations.

## Alternatives and refuted paths

- **Accepted:** preserve current transport and add shared VCS/context support.
  A directory transport migration was not selected; it
  still needs explicit context/unbounded-metadata handling; it is not a claim
  that changing transport alone completes the whole dependency audit.
- Do not add scientific minimum versions merely because a checker requires one.
- Do not refresh source pins, remove bootstrap dependencies or relabel routes as
  build-only/resolved-package to make the audit appear complete.
- Do not treat a moving development probe as immutable candidate qualification.
- Do not substitute passing resource/administrative checks for source science.

## Scope and exclusions

Shared declaration/provenance checking and optional context classification.
No scientific API repair, latest-provider migration, MolSysMT/MolSysViewer full
suite, new release version, package publication or permission change. Ordinary
internal pushes and complete PR/candidate gates retain the accepted CI policy.

## Acceptance criteria

- Principal maintainer settles transport/profile direction.
- Shared documented operations check immutable repository/commit, installed
  source provenance/version and exact selected context; default supported
  consumers preserve their behavior and pinned contracts.
- Guards reject moving/wrong commits, wrong repository, absent/false installed
  provenance, below-floor versions, wrong context, missing/weakened required
  requirements and unexplained overlay/channel drift.
- Declaration-only output cannot be mistaken for installed qualification; valid
  metadata without a version floor is not silently changed.
- Provider notice identifies current SDK/publisher consumers from the inventories
  before release/rollout, separating availability, adoption and tested artifacts.
- Consumer invocation is independently qualified and limitations remain explicit.

Expected future guard owner: `tests/test_dependency_routes.py`, supplemented by
focused provenance/context tests. Closure needs executed relevant guards and
reviewed normative documentation; neither is claimed by the current proposal.

## Local implementation issues

uibcdf/elastnetmt#18 is the first consumer. Central #45 coordinates member
adoption. Other existing shared-input consumers remain candidates for this
optional profile until their owning review accepts it.

## Dependencies and risks

Installed metadata alone cannot prove archive/native integrity or source feature
semantics. The current Viewer development route and supported scientific input
variants must stay distinguishable. Unqualified source-only dependencies must not
be advertised as public Conda delivery. Existing workspace #82 and private-access
#102 debt remain outside the new profile's acceptance.

## Provenance

2026-10-06, Linux x86_64, `molsyssuite@uibcdf_3.14`, Python 3.14.7;
primary editable Receptor libraries preserved. Fixed provider SHA and consumer
SHA above identify inspected code; no primary component clone was changed.

## Accepted implementation checkpoint

The maintainer accepted general support on continuation. Independently reusable
Git parsing/provenance operations live in `devtools/scripts/source_provenance.py`;
context/overlay/channel declarations in `dependency_route_contexts.py`. @3 is an
explicit opt-in through the existing audit API/CLI, with declared-only and actual
installed-context results kept distinct. Existing @1/@2 guards pass unchanged.

An isolated temporary pip --no-deps installation of the actual ElastNetMT SMonitor
pin `4b5e5c5a46e3c8a4dc46461ce72937f9a7dfbdae` produces PEP 610 Git metadata and
version `0.16.0+20.g4b5e5c5`; the new check accepts that exact identity. No primary
editable provider installation was replaced. This single-provider check is not
a qualification of all ElastNetMT contexts, science or any published artifact.

Provider notice precedes publication in #107/#45 and ElastNetMT #18. Current
registered adoption owners are Ackredit #108, Pytest Receptor #38, PyUnitWizard
#114, SMonitor #35, DepDigest #30, ArgDigest #28, LinDelINT #13 and GH Run
Receptor #60. Existing pins need no migration for this optional capability.
Hosted provider evidence and first consumer invocation remain to be recorded.

Focused provider checks pass all 65 dependency/recipe/provenance cases on Python
3.14.7, including 22 new Git/context guards. Ruff and offline governance pass.
Prospective handoffs were delivered to all eight inventoried owners; exact links
and the real Git probe are in
`devguide/rollouts/source_context_preflight_107_20261006.json`.
