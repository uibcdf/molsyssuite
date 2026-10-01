# Optional engine integration contract

This policy is owned by MolSysSuite under
[uibcdf/molsyssuite#62](https://github.com/uibcdf/molsyssuite/issues/62).
It applies when a registered member exposes an optional external method, tool,
accelerator or service. A member without such a boundary records non-applicability
in its ecosystem review; it does not acquire unused dependencies or empty adapters.
The Python-specific rules below apply to Python members. Adoption is phased through
member issues and the existing support-library reviews in `suite.toml`.

## Basis and responsibilities

The contract builds on TopoMT's separation of method identity and access backend,
its optional-engine guards, and its preservation of original provider evidence:

- [architecture decision at 22acca4](https://github.com/uibcdf/topomt/blob/22acca476570cb269af5ab48bd0c58a6960c5591/devguide/third_party_architecture_adr.md);
- [user routes and requirements at that source](https://github.com/uibcdf/topomt/blob/22acca476570cb269af5ab48bd0c58a6960c5591/docs/content/user/third_party_engines.md);
- [provider output checkpoint at that source](https://github.com/uibcdf/topomt/blob/22acca476570cb269af5ab48bd0c58a6960c5591/devguide/provider_pocket_output_checkpoint.md).

These are design and component evidence, not certification of every engine or
consumer. MolSysSuite generalizes the boundary semantics. Module layout, public
parameter names, result classes and scientific comparisons remain component-owned.

| Owner | Responsibility |
| --- | --- |
| DepDigest | Dependency declarations, availability discovery, conditional guards and truthful installation hints/inventory. |
| SMonitor | Diagnostic events, catalogs and rendering. |
| Consumer member | Backend selection, configuration, execution, conversions, input/output identity, compatibility and scientific validation. |
| MolSysSuite | Shared contract, applicability, exceptions, guide synchronization and coordinated adoption evidence. |

Use the provider-owned `DEPDIGEST_GUIDE.md` and `SMONITOR_GUIDE.md` where registered.
Change their canonical sources and distribute with `sync_vendored_guides.py`.
This central policy complements those guides; it is not another vendored API guide.
Provider limitations follow [cross-component feedback](cross_component_feedback.md).

## Separate identity, access and readiness

Document which method/provider the user selects and how it is accessed. The same
method may have several routes with independent dependencies and evidence:

| Access route | Availability boundary | Other failures and evidence |
| --- | --- | --- |
| Python library | Import name of the selected optional library; lazy loading. | Distribution version, transitive imports, native ABI, adapter execution and scientific result. |
| Local executable | The actual configured command/path in the current execution environment. | Permissions, version/build identity, exit status, output parsing and scientific result. |
| Remote service | Required local client dependencies and explicit service configuration. | Network, authentication, service state and submitted-job outcome. |
| Persisted results | Readable input artifacts and parser dependencies. | Format/version, completeness, attribution and faithful interpretation. |
| Local implementation | Its own dependencies and declared method semantics. | Component tests and separately evidenced comparison with the original. |

Backend names in this table describe semantics; existing components may retain
their own names and APIs. Guard only the selected route. A loader for saved results
does not require the original engine or network. A local implementation does not
inherit a requirement on the original engine solely for sharing its method family.

Selecting an unavailable engine must not silently choose another scientific
method or implementation. An API that intentionally selects automatically must
document its selection rule and expose the actual choice in results/provenance.
Compatibility aliases and defaults need a member-owned migration decision before
changing; publishing this policy does not rewrite them.

## Python dependency declarations and guards

Keep an optional engine out of mandatory package dependencies when only a selected
route uses it. If providing an extra, document exactly what it installs, including
auxiliary libraries and omitted originals. Keep mandatory dependency manifests,
test environments and distribution recipes aligned under the
[distribution policy](python_distribution_policy.md).

Use import names as Python keys in `_depdigest.py`, with real distribution names
for installer routes. New integrations declare both routes explicitly; `None`
disables a route. Preserve legacy omission behavior during controlled migration.
For example, these declarations come from the DepDigest provider recipe:

```python
LIBRARIES = {
    "pocketeer": {"type": "soft", "pypi": "pocketeer", "conda": None},
    "fpocket": {
        "type": "soft",
        "kind": "executable",
        "executable": "fpocket",
        "pypi": None,
        "conda": "fpocket",
        "channel": "conda-forge",
    },
}
```

The executable and explicit-disabled-route extension is published in
[DepDigest 0.12.0](https://github.com/uibcdf/depdigest/releases/tag/0.12.0), tracked
by [uibcdf/depdigest#22](https://github.com/uibcdf/depdigest/issues/22).
Consumers using this capability must require DepDigest >=0.12.0 in their relevant
runtime manifests and verify clean installation. The accepted release passed
exact-source and installed-artifact matrices before its same digest-verified Conda
file was promoted to the public `uibcdf` channel. TopoMT adopted it at its fpocket
boundary with custom-command and public-error regression evidence under
[uibcdf/topomt#56](https://github.com/uibcdf/topomt/issues/56).
A controlled full-commit CI source pin may support integration work under
[CI dependency resolution](ci_dependency_resolution.md); it does not establish a
public installation route. Existing consumers retain tracked compatibility until
the published capability and their own migration evidence are available.

For a Python adapter, put the guard at the external execution boundary and the
import inside it:

```python
from depdigest import dep_digest


@dep_digest("pocketeer")
def analyze_with_pocketeer(system):
    import pocketeer

    return pocketeer.find_pockets(system)
```

The example assumes input already prepared for that upstream API; actual conversion
belongs to the consumer. A conditional guard may cover an explicit installed/source
route, but does not implement source loading. Keep explicit source-checkout routes
isolated and record their identity; normal installed-engine verification must prove
that a sibling/source checkout is not shadowing the installed distribution.

A static executable declaration guards its declared command. If an API accepts a
custom command/path, the check and execution must use the same supplied value;
availability of the default command proves nothing about that override. DepDigest
discovery must not install software, launch an engine, or contact a service.

## Diagnostics and error compatibility

An absent requested dependency needs a useful diagnostic naming the requirement,
caller, supported installation route and component documentation. Disabled installer
routes must not reappear as inferred commands in messages or inventories.

Consumer exception types keep their public catch contract and accept the provider's
documented library/caller/message construction. Catalog exceptions and warnings
must render and reconstruct through their documented `args` contract; use
message-first construction when extending SMonitor catalog classes. Adapting an
established constructor is component work, with regression evidence before migration.

Preserve transitive import failures, invalid configuration, subprocess errors,
service errors and parser errors at their own boundaries, with their causes.
Discoverability of a package or command does not prove version compatibility,
successful execution or scientific correctness. Diagnostics describe operational
conditions; scientific measurements and provenance belong in returned/stored data.

## Results and inter-component compatibility

When another member consumes engine results, publish the supported result boundary
and its versioning/migration policy. Record, as applicable:

- the actual method, access route and provider distribution/build/service identity;
- the submitted inputs, selection/frame and mapping to the consumer's source indices;
- relevant parameters, original outputs or durable artifact references;
- the original meaning, units and provenance of reported measurements;
- transformations, compatibility adjustments and consumer-derived results.

Follow the shared quantity contract through
[the ecosystem policy](python_ecosystem_policy.md). An application-defined score
retains its attribution; a shared physical concept may retain a neutral name while
its estimator and source stay explicit. Missing data is distinguishable from zero
or an available empty collection. Do not present a derived proxy as original output
or infer equivalence from an access adapter.

TopoMT's `ProviderRun`, detached outputs, pocket geometry and nanometer conventions
are local implementations. Other members may meet the contract with their existing
schemas. A universal result class, directory tree or fixed unit is not required by
this policy. Provider-specific fidelity and scientific tolerances belong to the
component team; receiving members own their integration evidence.

## Verification and CI applicability

Record separately the following evidence; passing one category does not pass others:

1. **Availability contract:** import and collect with optional engines absent;
   requesting an absent route gives usable guidance; unrelated routes remain usable;
   disabled installers, custom commands and transitive errors retain their semantics.
2. **Installed adapter:** execute against the actual installed provider distribution
   or identified binary; record versions/platform/inputs and compare with a direct
   upstream invocation. Component developers choose scientifically relevant fields
   and tolerances. Mocked transport or a source checkout does not certify that route.
3. **Remote and file routes:** deterministic saved-fixture parsing and controlled
   transport tests are separate from live service reachability and job completion.
4. **Consumer exchange:** the receiving member verifies its declared result interface,
   identities, quantities and accepted transformations.

An ordinary environment may skip tests whose original engine is absent, with an
explicit reason. It must retain absence and independence guards. The designated
installed-engine verification must fail if its declared engine or usable version is
missing, shadowed or never exercised; an all-skipped run is not adoption evidence.
Record those gates in the local review. Optional-engine validation follows the
[CI lane policy](python_ci_policy.md) and each member's justified environment and
schedule; this contract adds no full-engine battery to every internal push.

An absent optional library may justify skipping its installed comparison. A present
library failing on a transitive import, incompatible version or calculation requires
an owning defect and truthful failure/exception evidence; broad `ImportError` skips
must not erase that distinction.

## Adoption and exceptions

Use the starter kit's `devguide/optional_engine_review.md` worksheet or a documented
local equivalent. For each applicable route, record owner issue, source/release
requirements, declarations, diagnostics, independent evidence and next gate. Link
the member's existing support-library review instead of creating duplicate themes.
Source integration, guide synchronization, public release and consumer adoption are
independent states. Mark adoption only for the boundaries supported by evidence.

The starter includes guidance only; it acquires runtime libraries when a real boundary
is implemented. Existing member APIs and repository tooling migrate through their
own issues. Active MolSysMT/MolSysViewer scientific execution reviews remain deferred
under the maintainer's decision; that deferral does not certify their runtime adoption.

A bootstrap dependency cycle, unavailable provider release, platform limitation or
legacy public error contract may need an exception. Record the specific rule/route,
reason, owning member/provider issues, interim behavior and evidence, responsible
maintainer, removal condition and an expiry or dated review deadline. Exceptions
are bounded, searchable and reassessed in the member review. They cannot silently
change a selected scientific method or claim evidence that was not obtained.
