# Python distribution member policy

MolSysSuite owns member distribution rules, adoption, evidence, bounded
exceptions and coordinated release routes. `suite.toml` specifies the `uibcdf`
Conda channel as the official public route, `conda-forge` for third-party
dependencies, and an optional PyPI route only after published-artifact and
dependency-closure verification. This policy is tracked in
[MolSysSuite #45](https://github.com/uibcdf/molsyssuite/issues/45).

## Package and CI contract

Local development installs a checked-out package with
`pip install --no-deps --editable .` after its Conda environment is prepared;
that is not publication. Keep development and test environments under
`devtools/conda-envs/`. Required runtime dependencies in `pyproject.toml` and
the Conda recipe must agree. A required CI dependency available only through
Conda must be obtained through a resolvable Conda environment. A tracked
full-commit source install of a temporarily unavailable sibling can provide
test evidence, but is not a public installation claim.

Build a public Conda package through a reviewed release of the UIBCDF
build/upload action. Verify the exact candidate, artifact metadata, dependency
closure and clean installation from the claimed public channel before
advertising an installation command or badge. PyPI is optional; pytest-receptor
may use it for pytest-plugin discovery, but a GitHub Release or local pip install
does not prove a public PyPI route. Publish no package until its workflow and
credential access are confirmed by an authorized maintainer. Coordinate
coupled-package staging and promotion under the suite's separate release work.

Use `noarch: python` when the installed Python code and resources are independent
of OS, architecture and interpreter ABI. Third-party native dependencies do not
alone disqualify a Python consumer. Bundled extensions/platform binaries, fixed
OS paths or selectors changing the payload need a native or reviewed local
profile. A dependency-only bundle uses the metapackage profile.

For qualifying new or changed Conda routes, use the
[shared noarch workflow](noarch_conda_workflow.md) or a documented reviewed tested
equivalent; bounded exceptions follow the publication policy. Build one immutable
file once, inspect its embedded version/resources before upload, and qualify the
installed file on every claimed OS/Python cell. The first migration requires
staging. Noarch alone does not prove platform support; installed evidence follows
the [suite CI policy](python_ci_policy.md).
Required Python bounds and runtime dependency names and constraints come from
`pyproject.toml`; optional features belong in optional dependencies. Recipe run
requirements must preserve the same required closure and compatible bounds.
Record intentional Python/Conda name translations and recheck environments and
recipes when a dependency or Python bound changes. A PyPI route requires all
declared runtime dependencies to resolve there for the claimed platforms and
Python minors, or it cannot be advertised.

## Early dependency-contract preflight

Before an expensive candidate build, inventory each maintained Conda recipe,
runtime-bearing development or CI environment, and exact sibling-source route.
Classify a route that does not install the runtime and explain why. A new or
unclassified runtime route fails until reviewed. Compare each route with the
required names, floors, ceilings and Python bounds in `pyproject.toml`; missing
requirements or weaker constraints fail. For a sibling installed from source,
verify its reviewed full commit, install route and installed distribution version
against the public requirement. Solver success alone does not establish that
the minimum version offers the required API.

Run the preflight when metadata or routes change and again for the exact release
candidate. A negative conformance check must reject at least a missing recipe
dependency, a stale environment floor and a source candidate below its public
floor. Report the offending route and constraint; do not silently weaken public
metadata or rewrite hand-maintained recipes. Record the route inventory,
negative evidence and any bounded exception in the member distribution review.
For ordinary Conda environments, list `uibcdf` before `conda-forge` and record
the channel-priority mode. A staging label or overlapping name requires exact
coordinate and installed-source verification; a successful solve alone is not
provenance or publication evidence.

The [shared offline route preflight](dependency_route_preflight.md) is an
available implementation for the documented bounded profile. A member owns
its reviewed inventory and explicitly invokes the pinned tool in its early
CI/candidate route; documented local equivalents and exception mechanisms
remain applicable. Tool availability does not establish member adoption.

## Generated resources in release artifacts

For every claimed public distribution route, inventory generated or vendored
runtime resources and version-bearing payloads, or record reasoned
non-applicability. Examples include compiled extensions, schemas, embedded
data and browser bundles. Check committed inputs early, then build each route
from the exact candidate, inspect its archive for required paths and version
identities, install that artifact cleanly and exercise a path that uses the
resource. Record route, artifact coordinate and digest with the
[candidate receipt](release_version_policy.md#candidate-evidence-lifecycle).
One route's passing result does not certify bytes delivered by another route.
Keep a negative check that rejects a stale embedded version and a missing
resource even when another route passes.

## Immutable Conda files and public poststate

Treat owner/package/version/subdir/filename as an immutable coordinate across
all labels. Record the SHA-256 of the tested candidate. Before upload, query
that exact coordinate under every label. If occupied, do not overwrite or use
`--force`, even if the digest matches; a changed build needs a new build number
or public version. Staging promotion adds a label to the **same tested file and
digest** after verifying source coordinate, label and digest. It does not
rebuild or upload a second file at that coordinate.

After upload or promotion, independently query the public registry, with
bounded retries for propagation, and match public label, coordinate and digest.
Action success alone is not proof of the public poststate. A red verifier is
diagnosed with read-only queries, not another mutation merely to obtain a green
run. After an uncertain response, inspect first; a direct upload may be retried
only after bounded observation confirms the coordinate is still unoccupied.
Conflicting bytes, missing source identity or unresolved state fail closed. A
negative conformance check rejects an occupied coordinate under any label and
changed bytes at the expected public coordinate. Clean installation remains a
separate user-availability gate.

## Member review

The [dated distribution rollout](rollouts/python_distribution.md) records the
current source baseline and incomplete member adoption. Source audit results
and member-owned adoption evidence remain separate.

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
evidence under this suite policy.
