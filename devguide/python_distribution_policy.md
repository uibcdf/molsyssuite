# Python distribution adoption profile

MolSysSuite inherits the [effective MOLI Python distribution policy](https://github.com/uibcdf/moli/blob/15b38fbe17b6ee9fa9aac2a8e21b80d76a8da70f/devguide/policies/python_distribution_policy.md)
and the corresponding values in the pinned `moli.toml`. MOLI owns the general Conda,
optional verified PyPI, dependency metadata, environment, recipe, CI and release
contract. MolSysSuite owns member adoption, evidence, bounded exceptions and any
coordinated release route needed for coupled packages. This profile is tracked in
[MolSysSuite #45](https://github.com/uibcdf/molsyssuite/issues/45).

## Member review

Every registered `python-package` member has one
`[[python-distribution-reviews]]` entry in `suite.toml`. `pending` means no
policy-grade review under this snapshot has been recorded; it does not assert that
the member lacks a recipe, package or CI route. `partial` identifies a documented
gap, `adopted` requires linked evidence for each route the member actually claims,
and `excepted` requires reason, owner, removal condition and expiry. A member may
adopt the policy before its first public release when its CI and recipe are ready,
it makes no premature installation claim, and publication access remains explicitly
unknown until confirmed.

Each record separately shows `ci-recipe` readiness
(`pending`, `partial`, `ready`, `excepted`) and
`publication-access` (`unknown`, `confirmed`, `unavailable`,
`not_applicable`). `unknown` is an honest access state; it is never inferred
from the presence of a workflow. An adopted review needs ready CI/recipe evidence
or a bounded exception. Actual publication and clean-install claims still require
member-owned evidence. Credential access follows the future MOLI #8 decision.

The member review should name intended user channels, runtime dependency parity
between `pyproject.toml` and recipe, environment and recipe paths, required CI
route, candidate and public package evidence when relevant, and any exception.
Run `python devtools/scripts/python_distribution_status.py` for the inventory or
add `--require-adopted` to assess rollout completion. This is separate from
guide-copy and policy-caller adoption.

## Starter and release handoff

The generated starter uses committed `devtools/conda-envs/` files for development
and CI and installs only the local component with pip `--no-deps`. Add every
required runtime dependency to the metadata and environments; add the matching
Conda recipe requirements before publication. A full-commit source route for a
temporarily unavailable sibling is test evidence only. Before the first public
Conda release, add and verify `devtools/conda-build/` and a reviewed workflow
invoking `uibcdf/action-build-and-upload-conda-packages`. Keep upload credentials
in CI secrets; access and communication are tracked in [MOLI #8](https://github.com/uibcdf/moli/issues/8).
Do not announce an installation command or badge until a clean public-channel
installation passes.

## Console commands in noarch Conda recipes

For a registered `python-package` member with a
`devtools/conda-build/meta.yaml` recipe declaring `build.noarch: python`, the
recipe's `build.entry_points` must match `[project.scripts]` in `pyproject.toml`:
each command name and callable target appears exactly once, with no extra commands.
This is a MolSysSuite member profile for [issue #47](https://github.com/uibcdf/molsyssuite/issues/47).
The shared repository checker enforces this against the recipe's literal build block;
it does not require a recipe before a member's first Conda release or apply the rule
to platform-specific builds.

The recipe's Linux build test is insufficient evidence for a Windows launcher. A
member claiming Windows support must exercise each command's `--help` from its
installed Conda artifact on Windows, as well as from every other claimed platform.
The owning member records the installed-artifact result before claiming the repaired
Conda package works there. Existing public artifacts are not repaired by changing the
source recipe; they need a new immutable build coordinate and release evidence.

A temporary exception uses that member's `[[python-distribution-reviews]]` entry with
`state = "excepted"`, a member-owned `review-issue`, reason, owner, future
`expires-on` date, and a testable `removal-condition`. The checker suppresses only
this entry-point finding while that exception is complete and unexpired; the central
distribution inventory still reports the member as excepted.

MolSysSuite's coupled-package staging and promotion choices remain in
[the coordinated release work](https://github.com/uibcdf/molsyssuite/issues/27).
An isolated member release can use a suitable route with its own exact-candidate
evidence under the inherited MOLI baseline.
