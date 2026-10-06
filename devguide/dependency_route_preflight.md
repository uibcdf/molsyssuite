# Offline dependency-route preflight

Owner: [MolSysSuite #45](https://github.com/uibcdf/molsyssuite/issues/45).
Initial consumer: [Ackredit #108](https://github.com/uibcdf/ackredit/issues/108).
This is an explicitly invoked tool. Its availability is separate from
member adoption; publishers and versioned policy callers do not invoke it automatically.

`devtools/scripts/dependency_routes.py` provides `audit(root, inventory_path,
source_roots=...)` and an equivalent command. It reuses the existing
`noarch_conda.inspect_recipe` and `required_constraints`; it does not copy their
recipe/resource checks or change the publisher's behavior.

```bash
python devtools/scripts/dependency_routes.py --root /path/to/component
```

The default inventory is `devtools/dependency_routes.toml`. An explicit
`--inventory` selects another committed relative path. Required dependencies and
Python constraints come only from the member's `pyproject.toml`. Invocations
require the existing noarch tool's PyYAML, Jinja2 and packaging dependencies.
No member import, install, solver, network request or file mutation occurs.
The original `@1` contract below is preserved. The general successor described
later additionally reads installed distribution metadata by default in its CLI.

## Inventory contract

The root needs `schema = "molsyssuite.dependency-routes@1"` and a nonempty
`reason`. Every route needs a relative `path` and a nonempty review `reason`.
Inventoried files must exactly cover the bounded discovery profile:

- recipes: `devtools/**/meta.yaml` and `devtools/**/recipe.yaml`;
- environments: `devtools/conda-envs/*.yaml` and `*.yml`;
- workflows: `.github/workflows/*.yaml` and `*.yml`.

New, missing, duplicate or escaping paths fail. Other layouts and recipe engines
need an explicit provider extension or a reviewed local profile; they are not
silently interpreted. An inventory records applicability, not a second version list.

```toml
schema = "molsyssuite.dependency-routes@1"
reason = "Reviewed member source/runtime routes"
source_routes = []
source_reason = "Required runtime providers are acquired from public Conda"

[[recipes]]
path = "devtools/conda-build/meta.yaml"
kind = "shared-noarch"
plan = "devtools/conda-build/release_plan.toml"
resources = "devtools/conda-build/resources.toml"
reason = "The one reviewed noarch artifact route"

[[environments]]
path = "devtools/conda-envs/development_env.yaml"
kind = "runtime"
channel_priority = "strict"
python_minor = "3.14"
reason = "Routine source development narrows the supported Python range"

[[environments]]
path = "devtools/conda-envs/build_env.yaml"
kind = "build-only"
reason = "Build bootstrap; the recipe supplies its own runtime environment"

[[workflows]]
path = ".github/workflows/CI.yaml"
sha256 = "REPLACE_WITH_THE_REVIEWED_WORKFLOW_SHA256"
reason = "Test environment followed by pip --no-deps source installation"
```

Recipes delegate to the shared noarch preflight, including declared resources,
Python/run constraints and console commands. Runtime environments must carry
every required dependency with exactly the metadata constraints, unless an
inventoried source route supplies it. Exact comparison conservatively rejects
stronger as well as weaker dependency constraints for explicit review. Extras
and optional features do not satisfy a missing required dependency.

Runtime channels must be `uibcdf`, then `conda-forge`, and the inventory records
`channel_priority = "strict"`. Workflow review establishes how priority is
actually selected. The inventory flag alone is not solver evidence.

Python normally preserves exactly `requires-python`. A reviewed `python_minor`
may narrow simple `>=`/`<` metadata bounds to a whole minor. Both Conda
`python=3.14` and `python >=3.14,<3.15` express that selection; a minor that
crosses a metadata bound is rejected. Other Conda match expressions, conditional
requirements and Python constraint forms fail for an owned profile.

`build-only` and `resolved-package` are reviewed exclusions with explicit reasons.
The latter means the published package is installed with normal dependency
resolution; it does not prove the package is available. Review that actual route
and retain installed evidence separately.

Every workflow is recorded with the SHA-256 of its complete reviewed bytes.
Any change, including a new source installation inside an existing job, requires
renewed route review before updating its hash. Hashes are conservative drift
guards, not an interpreter of arbitrary shell commands or evidence of execution.
They intentionally also flag unrelated workflow edits. Do not automatically
refresh hashes in CI; inspect the changed route first. Classify reusable jobs,
build-only jobs, artifact readers and receiving fixtures explicitly in `reason`.

## Required source providers

When a required dependency is supplied from a checkout, add `[[source_routes]]`
with `name`, a reviewed full lowercase `commit`, `install =
"pip-no-deps-directory"`, and a reason. Its runtime environment lists the name
in `source_supplied`, and must not simultaneously declare the Conda requirement.
Call the tool in the interpreter into which that clean checkout was installed:

```bash
python devtools/scripts/dependency_routes.py --root /path/to/consumer \
  --source-root provider=/path/to/reviewed/provider
```

The checker reads the checkout's Git identity/cleanliness, installed distribution
version and `direct_url.json` directory provenance. It rejects a different commit,
dirty source, missing distribution, wrong installed origin or a version outside
the consumer's public floor/ceiling. It does not claim native-byte integrity,
import correctness or executed scientific compatibility. Wheels with a separate
producer receipt, VCS URLs, other source providers and conditional routes need
their own reviewed profile. A source route is test evidence, not public delivery.

`validate_source_version(requirement, version)` is an independently reusable
metadata check. `audit` adds actual source/provenance checks. Their guards live
in `tests/test_dependency_routes.py`, including omitted recipe dependencies,
weakened environment floors/ceilings, source versions below public floors,
changed workflows and narrowed Python bounds.

## Consumer adoption and limits

Pin the shared checkout to an accepted full commit. A consumer owns its inventory
and thin invocation, while this repository owns parsing/comparison and negative
guards. Run before expensive builds, when metadata/routes change, and for an exact
candidate. Use `--receptor=llm` for local pytest, `--receptor=ci` for hosted pytest,
and GH Run Receptor for Actions inspection.

Passing source-route checks does not certify a new artifact, publication,
clean installation, secret availability, API stability or another member's adoption.
Retain existing producer/archive/installed/public receipts. Ackredit, Pytest
Receptor and PyUnitWizard have related owner issues; other members remain
candidate consumers until their layouts and actual routes are reviewed.

## Provider review — 2026-10-06

The existing proposal in uibcdf/molsyssuite#105 was reviewed under the principal
maintainer's standing direct-commit authorization. Its immutable tool commit is
`43b9f94bf5ab0ec3f54a4b2ca5b23b791d6af0bc`; integration retains those commits
and the independently published ArgDigest environment correction. Twenty-one
focused provider route/recipe tests, Ruff, offline governance and generated
indexes pass in `molsyssuite@uibcdf_3.14` on Python 3.14.7.

The supplied profile deliberately requires exact dependency constraints and
reviewed whole-minor Python narrowing. It is not a general Conda solver or shell
interpreter. Unsupported Conda expressions and stronger dependency constraints
need explicit review or a provider-owned profile; this does not change the shared
policy's allowance for justified component conditions. Workflow hashes retain
the reviewed installation-route boundary and must not be refreshed blindly.

Ackredit #108/#110 prepared the first invocation at this exact pin. ArgDigest #28
is the next reviewed consumer; Pytest Receptor #38 and PyUnitWizard #114 retain
their existing notices and owner decisions. Acceptance of the provider alone
does not merge the Ackredit proposal, close these reviews, certify current
artifacts or activate another scientific suite.

## General route contract (`@2`)

Prepared under the principal maintainer's general-design direction for
uibcdf/pyunitwizard#114 and central #45. This is a general route model, with no
component-specific bypass. The original `@1` schema, output and default behavior
remain available; existing consumers retain their immutable provider pin.

Use `schema = "molsyssuite.dependency-routes@2"`. Exact file discovery, inventory
reasons, source identities/provenance and workflow hashes retain the earlier
rules. A runtime environment records its `purpose`:

| Purpose | Dependency and Python obligation |
| --- | --- |
| `production` | Preserve the advertised numeric release range. |
| `development`, `test`, `documentation`, `optional-runtime` | Select an equal or narrower compatible numeric release range; any narrowing needs `narrowing_reason`. |

Every required dependency remains mandatory. A reason cannot excuse a missing
name, weaker lower bound, wider upper bound or empty/contradictory range. Optional
providers cannot satisfy an omitted required provider. The comparator proves
interval inclusion rather than testing one sampled version. It never duplicates
the component's public version requirements in the inventory.

```toml
[[environments]]
path = "devtools/conda-envs/openff_env.yaml"
kind = "runtime"
purpose = "optional-runtime"
channel_priority = "strict"
narrowing_reason = "Owner-qualified backend/provider/interpreter selection; owning issue and evidence"
reason = "Installs the consumer and its complete required public dependencies"
```

Runtime public channels remain `uibcdf`, then `conda-forge`. A trailing
`nodefaults` is accepted as an explicit exclusion of defaults. Strict priority
still requires actual workflow review; the inventory does not configure a solver.
Separately reviewed exact-file staging provenance is recorded in its workflow
review, not treated as an ordinary public runtime environment.

### Conda expressions and proof boundaries

`dependency_constraints.conda_requirement` retains the original expression,
selector kind and build string. Numeric version-prefix selectors such as
`provider=0.14.0` and exact version/build selectors such as
`provider=0.14.0=py_0` are distinct. Their release-domain interval representation
is used only for comparison; recipe/environment bytes are never rewritten.
The behavior follows the reviewed [Conda MatchSpec contract](https://docs.conda.io/projects/conda/en/stable/dev-guide/api/conda/models/match_spec/)
and [CEP 29](https://conda.org/learn/ceps/cep-0029/).

The interval proof supports numeric release versions with `>=`, `>`, `<=`, `<`,
exact equality, whole-segment prefixes and compatible-release bounds. Unsupported
unions, exclusions, regular expressions, conditional/source/extra requirements
and non-release bounds fail for explicit review. This bounded grammar applies
equally to every component. Whole-segment prefixes do not match a different
segment such as Python 3.140 for a 3.14 selection.

Conda prefix selectors can admit non-release versions. Consequently a proof over
numeric releases alone does not qualify a resolved environment. Actual installed
public floors/ceilings are a separate mandatory check: for example, an installed
`0.14.0.dev1` fails a public `>=0.14.0` floor even when the selector admits it.
No prerelease/local version is silently converted to a release for this check.

`dependency_constraints.compare_requirements` owns the general declared-range
operation. `check_installed(project, version_for=..., python_version=...)` checks
the active interpreter and actual required distribution versions with the public
metadata. It does not prove transitive dependency closure, import origins, the
installed build selector, native bytes or scientific behavior. Those gates remain
separate, including required source-directory provenance and exact-file evidence.

### Recipe dependencies and publisher independence

`noarch_conda.render_recipe` reuses the existing sandbox and accepts explicit
rendering inputs. `inspect_recipe_dependencies` checks package identity, noarch,
required run constraints and host Python without requiring a particular publisher
plan schema. The full shared `inspect_recipe` retains its independent release
identity, resources, entry-point and artifact checks.

For a local noarch publisher use a recipe of kind `noarch-dependencies`, with
`plan` pointing to its committed context file containing numeric `version` and
nonnegative integer `build_number`. An optional `environment_from_plan` maps
explicit uppercase recipe variables to those two fields. No process environment
or credentials are read implicitly. The tool records
`scope = "declared-noarch-dependencies"`; it does not qualify a local publication,
resource inventory or version identity. Those retained owner guards must be
reviewed separately before claiming whole-policy adoption.

### Invocation and truthful results

The `audit` API remains an offline declaration review. For `@2`, its receipt
states `proof_domain = "numeric-release-versions"`,
`qualification = "declared-only"` and `installed_check_required = true`.
It includes narrowed names and original selectors/build strings per route.

The CLI checks installed public bounds **by default for `@2`**, before allowing
the normal invocation to pass. Use it in the resolved interpreter before tests
and exact-candidate builds. Successful output states
`qualification = "declared-and-installed-public-bounds"` and records actual
versions. A missing distribution or wrong floor/ceiling fails with the original
nonzero outcome.

`--declared-only` explicitly selects an offline review with a visibly incomplete
qualification. It must not replace the default invocation in the owner CI or
publication gate. `--check-installed` also offers the actual-version check to an
explicit `@1` invocation; the original `@1` default is unchanged.

Provider regression guards are `tests/test_dependency_constraints.py`,
`tests/test_dependency_routes.py` and `tests/test_noarch_conda.py`. Candidate
availability, notice delivery, owner invocation/adoption, source CI and public
artifact qualification remain separate states. No policy tag, publisher pin or
consumer invocation is automatically migrated by this additive delivery.
