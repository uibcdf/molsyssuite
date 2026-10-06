---
summary: Qualify immutable VCS dependency installations in the shared source-route preflight.
issue: uibcdf/molsyssuite#107
status: open
opened: 2026-10-06
closed:
verification: inspected
area: [governance, compatibility, distribution, tooling]
guard:
normative:
blocked_by: []
supersedes: []
---

# Immutable VCS dependency qualification

**Reported:** 2026-10-06 during uibcdf/elastnetmt#18 / central #45.
**Status:** Design decision pending with the principal maintainer; no shared API
or source-installation route has been changed.

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

The existing directory and source-free contracts remain compatible. Decide the
schema/API after inspecting those contracts and tests; this proposal chooses no
new schema version or consumer pin. Independently useful parsing/provenance
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
No new scientific run, installed VCS qualification, credential probe or real
package build was performed for this proposal.

The first consumer supplies actual need; generic usability for other components
is a design target. A source installation receipt is not an archive/native-byte,
import, scientific or public-delivery proof. Current source-only or private
providers retain their existing evidence limitations.

## Alternatives and refuted paths

- **Pending:** preserve current transport and add shared VCS/context support
  (recommended), or migrate CI installs to reviewed local directories. The latter
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
