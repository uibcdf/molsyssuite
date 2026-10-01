# Quantity boundaries and unit authority

MolSysSuite coordinates uibcdf/molsyssuite#46 and uibcdf/molsyssuite#18.
PyUnitWizard owns quantity interchange design under uibcdf/pyunitwizard#83 and
its `QuantityRecord` implementation under uibcdf/pyunitwizard#82. Components own
scientific schemas and migrations.

## Applicability

Apply this contract to new or changed boundaries that persist physical quantities
or pass them to another component, backend, file, message or frontend. Unitless
utilities record non-applicability. Existing routes are reviewed in the
[adoption inventory](rollouts/quantity_boundaries.md); guide distribution is not
proof of runtime adoption.

## Boundary contract and evidence

- Preserve the physical value and its unit. Use the provider-owned record/codec
  route for general quantity interchange; do not invent another quantity format,
  backend registry, identity passport or value-certification cache. Provider
  format/API choices remain in uibcdf/pyunitwizard#83.
- A fixed-unit numerical protocol may extract a magnitude with explicit
  `get_value(..., to_unit=...)` when its receiving contract declares that unit.
  Never strip a standardized quantity and assume the current session unit is
  the receiver's unit. Do not apply a blanket ban to legitimate unitless values.
- Readers validate their expected field, unit and dimensionality and reject
  missing/inconsistent unit metadata rather than silently guessing a unit.
  Components retain ownership of versioned schema and legacy migration rules.
- Every applicable boundary has a component-owned regression under a non-default
  session policy, such as angstrom and nanosecond, proving physical invariance.
  Cover persistence in a fresh reader, reused quantities, shapes/dtypes and the
  relevant missing/invalid-unit path. Fixed-unit wire routes test the explicit
  target unit. Guards must exercise the actual boundary rather than only a mock.
- New or changed public outputs state whether they are fixed-unit,
  policy-following, backend-preserving or unitless. A fixed-unit output converts
  explicitly; a policy-following output documents that authority.

These are focused compatibility checks for relevant CI/release claims, not a
requirement to run full scientific suites before each internal direct push.
Scientific regressions and repairs remain with component teams.

## Session authority

Precedence is explicit operation parameter, local context, application policy,
then factory default. A member needing the suite baseline initializes it only
when `has_active_policy()` is false. Importing or lazily activating a sibling
must not replace an application choice. All current four scientific bridges use
the shared MolSysMT baseline; PyUnitWizard owns the generic mechanism.

The accepted context mechanism serializes writers in one process. It is not
thread/async-local: unrelated readers can observe a temporary policy. Do not
claim stronger isolation. Fast tracks name exact converters and are registered
idempotently with deterministic conflict diagnostics.

## Provisional provider API and exceptions

The inspected canonical `PYUNITWIZARD_GUIDE.md` documents the `record` form,
`QuantityRecord` and `QuantityRecordBundle`, with the API provisional until its
provider promotion gate. Refer to the
[owning implementation record](https://github.com/uibcdf/pyunitwizard/blob/main/devguide/pending_proposals/quantity_record.md)
and synchronized guide; do not promise unsupported API names or promote a draft
schema into a suite format. Adoption verifies the provider floor and dependency
closure for every claimed Python minor. Editable-source tests are not public
installation evidence.

A route needing an existing fixed schema or pending provider capability records
a reviewed member-owned exception naming the rule, reason, owner and issue,
interim unit-preserving controls, expiry and removal condition. This uses the
[ecosystem exception mechanism](python_ecosystem_policy.md#member-review-and-evidence).
An exception must preserve unit integrity; provisional API status is not permission
to send ambiguous bare numbers. Synchronize guides through the registered script.
