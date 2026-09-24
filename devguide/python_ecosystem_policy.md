# Python ecosystem adoption profile

This is the MolSysSuite member profile for the [effective MOLI support-library
policy](https://github.com/uibcdf/moli/blob/6a91433bd38582980d0781474be6a80c58f48886/devguide/policies/python_support_libraries_policy.md)
and [effective MOLI developer-tools
policy](https://github.com/uibcdf/moli/blob/6a91433bd38582980d0781474be6a80c58f48886/devguide/policies/python_developer_tools_policy.md).
Their applicability and general requirements are read from the pinned MOLI registry;
MolSysSuite does not redefine them. This profile is normative for registered members
carrying the `python-package` capability. Its rollout belongs to
`uibcdf/molsyssuite#6`.

## Member review and evidence

The `[[python-ecosystem-reviews]]` records in `suite.toml` track each member's review
of the two inherited policies independently. `pending` means the review under the
new snapshot has not been recorded; it does not claim that a library or tool is
absent. `partial`, `adopted`, and `excepted` use the meanings in MOLI's policies.
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
existing [GH Run Receptor dogfooding profile](gh_run_receptor_policy.md) adds
suite-specific readiness and active-use evidence without changing MOLI's general
inspection rule.
