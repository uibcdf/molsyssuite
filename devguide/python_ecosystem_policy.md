# Python ecosystem member policy

MolSysSuite owns the support-library and developer-tool rules for registered
members carrying the `python-package` capability. `suite.toml` names the four
support libraries and two developer tools. Its rollout belongs to
`uibcdf/molsyssuite#6`. A MOLI policy revision does not change these member
requirements without a MolSysSuite decision and policy release.

## Applicability and behavior

Review each boundary and use the corresponding library where it exists:

- **ArgDigest** for nontrivial public argument constraints, normalization and
  validation; ordinary Python type errors alone do not justify a dependency.
- **DepDigest** for optional, heavy or backend-specific dependencies whose
  availability and loading need user-facing explanation.
- **SMonitor** for diagnostics users need to see, including recoverable failures
  and incomplete operations; scientific outcomes and provenance remain data.
- **PyUnitWizard** for physical quantities needing parsing, conversion or
  dimensional checks. Obtain exchanged quantities through its shared registry
  and codec, rather than a separate Pint registry. The member owns its schema,
  scientific meaning and migration. MolSysSuite remains bound by the
  [MOLI quantity integrity contract](https://github.com/uibcdf/moli/blob/main/devguide/policies/quantity_integrity_policy.md).

Do not add an unused library merely to satisfy an inventory. A bootstrap
provider may keep a boundary local when a required reverse dependency would
make a runtime cycle. Its review must show both published dependency edges,
the local behavior and diagnostics, clean installation and import order, and a
reassessment condition. Optional extras do not excuse a required dependency
cycle.

Optional engines follow the [optional engine integration contract](optional_engine_integration.md)
when such a boundary exists. It separates provider/method identity, access route,
availability, diagnostics and consumer result evidence. Adoption preserves local
APIs and environments and has explicit member-owned exceptions; provider guide
distribution alone does not establish runtime adoption.

Optional scientific attribution follows the
[Ackredit client policy](ackredit_client_policy.md). Keep provider loading deferred,
contribute to application-owned sessions and preserve detached result provenance.
Ackredit owns its canonical guide and portable API; a pilot or synchronized guide
does not certify published compatibility or runtime adoption in other members.

PyUnitWizard's process-wide unit policy must not be overwritten on import or
first use. Authority runs from an explicit operation parameter, through an
explicit local context and the application's chosen policy, to factory defaults.
Only a member needing session standard units may initialize the suite's shared
baseline once when no policy is active; it cannot replace an application choice.
Persisted units and fixed-unit scientific results use explicit operation-boundary
conversions, with tests under a non-default policy. The shared suite baseline
and migration are tracked in [MolSysSuite #18](https://github.com/uibcdf/molsyssuite/issues/18).

For development, use a published Pytest Receptor release with `--receptor=llm`
when an agent runs pytest, and `--receptor=ci` in pytest CI logs. Pin the exact
published CI version. The receptor cannot alter tests, exit status or CI coverage.
If it cannot run on a supported Python minor, record a bounded exception and
run the required tests with native pytest.

Use a published GH Run Receptor release for first inspection of Actions runs;
GitHub's run, job and step conclusions remain authoritative. Use native
`gh run view` when receptor evidence is incomplete or disagrees. A receptor
result alone cannot approve a release. Pin an exact reviewed commit for
unreleased experiments and report defects in the provider repository. These
tools are development infrastructure, not member runtime dependencies.

## Member review and evidence

The `[[python-ecosystem-reviews]]` records in `suite.toml` track each member's review
of the two suite policies independently. `pending` means the review under the
new snapshot has not been recorded; it does not claim that a library or tool is
absent. `partial` records gaps; `adopted` requires evidence for every applicable
boundary without implying that all libraries are dependencies; `excepted`
requires a bounded exception.
An `adopted` claim requires member-specific implementation and test evidence. The
member's review issue links that evidence; the inventory also requires an evidence
entry. Any non-pending state requires a member-local review issue. A bounded
exception records its reason, owner, removal condition, and expiry in the member
record.

Run `python devtools/scripts/python_ecosystem_status.py` for the current declared
state and `--format json` for automation. The offline governance validator checks
that every Python member has one valid review record. Use `--require-adopted` only
when assessing completion of this rollout; pending reviews are expected during
phased adoption. Guide-copy and versioned policy-caller adoption remain separate
live checks under `devguide/adoption_lifecycle.md`.

## Suite-specific coordination

Member repositories own their dependency choices, tests, CI changes, and local
exceptions. MolSysSuite schedules reviews, records evidence and bounded exceptions,
and synchronizes canonical integration guides with its registered consumers. The
existing [GH Run Receptor dogfooding policy](gh_run_receptor_policy.md) adds
readiness and active-use evidence.
