# Optional engine integration review

This is an unqueued worksheet for __REPOSITORY__. It makes no implementation or
adoption claim. If there is no optional-engine boundary, record non-applicability
and its source rationale in the component's ecosystem review.

When a concrete change is needed, open the owning issue first and create its report
using the local [reporting protocol](reporting_protocol.md). Link that issue here.
Do not add unused runtime dependencies to fill this worksheet.

## Shared references

- [MolSysSuite optional engine contract](https://github.com/uibcdf/molsyssuite/blob/main/devguide/optional_engine_integration.md)
- [DepDigest provider recipe](https://github.com/uibcdf/depdigest/blob/main/docs/content/user/optional-engines.md)
- [MolSysSuite ecosystem policy](https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_ecosystem_policy.md)
- [MolSysSuite CI policy](https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_ci_policy.md)

Use synchronized provider guides when registered for this member. Verify published
provider versions before claiming clean public installation. DepDigest's executable
and explicit disabled-installer extension is tracked in uibcdf/depdigest#22;
source availability alone is not release evidence.

## Route inventory

Add one row for each implemented route. Names and directory layout remain local.

| Method/provider | Access route and public selector | Requirement/import/command/service | Actual pip/Conda routes or disabled routes | Owner issue and status |
| --- | --- | --- | --- | --- |

Distinguish original Python libraries, executables, services, saved files and local
implementations. Document extras' actual contents. An unavailable selected route
must not silently switch methods. An intentional automatic selection exposes the
actual choice and its rule.

## Evidence per route

Record commands/selectors, source commit, environment, result and limits for:

- package import/test collection and unrelated routes with the engine absent;
- the requested-route error, truthful installation hint and exception compatibility;
- internal import/execution failures distinct from absence;
- installed distribution or binary identity, including custom command paths;
- direct upstream comparison on the same submitted input, with component-owned
  fields/tolerances and an installed gate that fails on missing/shadowed engines;
- deterministic file/transport tests separately from actual live service execution;
- receiving-component interface evidence, when another member consumes the result.

Identify the CI route/schedule that supplies installed-engine evidence. Ordinary
absence skips cannot establish adoption; present-but-broken engines need an owning
defect. Preserve the component's full/routine lanes and environment constraints.

## Result boundary and compatibility

Document the schema/API version, actual provider/backend, input selection/frame and
source-index mapping, artifact retention, quantities/definitions, transformations
and receiving members. Distinguish unavailable values from zero or empty results.
Record any compatibility adjustments and their removal conditions.

## Exceptions and next gates

For each exception, name the affected rule/route, reason, owner and provider issues,
interim behavior/evidence, responsible maintainer, removal condition and dated
review deadline. Keep guide distribution, source integration, public release and
consumer runtime adoption as separate states. Review this worksheet when an
optional route or result contract changes.
