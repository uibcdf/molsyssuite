# Offline dependency-route preflight

Owner: [MolSysSuite #45](https://github.com/uibcdf/molsyssuite/issues/45).
Initial consumer: [Ackredit #108](https://github.com/uibcdf/ackredit/issues/108).
This is an additive tool proposal for owner review, not completed member adoption
or a new automatically enforced publisher policy.

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
