---
summary: Support committed bounded component test dependencies in shared installed qualification.
issue: uibcdf/molsyssuite#77
status: resolved
opened: 2026-10-03
closed: 2026-10-03
verification: measured
area: [distribution, tooling, ci]
guard: tests/test_installed_noarch.py
normative: devguide/noarch_conda_workflow.md
blocked_by: []
supersedes: []
---

# Component dependencies for installed test qualification

**Reported:** Pytest Receptor 1.2.1 preparation on 2026-10-03.
**Status:** Resolved; immutable implementation and eight hosted dummy cells pass.

## What

The shared installed noarch workflow fixes its tool set and cannot request
Pytest Receptor's maintained `pytest-rerunfailures>=15,<17` and
`pytest-subtests>=0.14,<0.16` integration dependencies. Its historical
`pytest-receptor=1.0.0` tool pin also cannot solve the required Python 3.14 cell.
uibcdf/pytest-receptor#32 uses a local installed wrapper over the shared operations;
the provider owns this missing reusable capability under #77.

## How

An optional `installed_tests.conda_dependencies` list in committed
`devtools/conda-build/resources.toml` extends the shared qualification tools.
`installed_noarch.py tools` validates specs and installs them into the running
interpreter's explicit prefix, preserving the declared Python minor and ordinary
`uibcdf`, `conda-forge` strict channel order. Input is passed as process arguments,
without shell evaluation. The `prepare` operation validates the same list early.

The initial adapter permits public package names with exact versions or explicit
lower/upper version bounds. It rejects paths, URLs, channel qualifiers, markers,
extras, unbounded specs and overriding Python or the tested candidate. The
missing list remains backward compatible. Standard tools use pytest 8/9,
pytest-cov 6/7, pytest-xdist 3 and published Pytest Receptor 1.2.0; when testing
Pytest Receptor itself the candidate supplies that plugin instead of preinstalling
another receptor version. Existing exact artifact, prefix/import, digest/resource,
complete matrix and nonempty execution checks remain unchanged.

## Why

One generic tool set cannot describe every component's tests. The component owns
its scientific selection and tool constraints, while the shared operation keeps
their acquisition reproducible and compatible with installed artifact evidence.
No additional scientific tests are added to routine internal pushes.

## What is measured and what is assumed

The added regressions fail before implementation and pass after it. They cover
the actual consumer specs, unsafe/incomplete declarations, exact prefix/minor,
failure propagation and testing the receptor candidate without an old plugin.
Existing regressions protect source-shadow rejection and zero-execution failure.

The manual `qualify-installed-test-tools.yaml` workflow installs a normally built
dummy consumer outside source in Linux/macOS ARM × Python 3.11–3.14. It executes
both optional plugins and negative source-shadow/collection-only checks in each
cell, retaining declared tools and actual installed closure. These are tool
capability receipts, not staged Conda artifact or component release receipts.
Hosted [37127638411](https://github.com/uibcdf/molsyssuite/actions/runs/37127638411)
passes all eight cells at immutable
`baac208f3f592e00eaf99fa78a879878f98dc141`. Both real-plugin execution and the
source-shadow/collection-only negative step pass in every cell. Native central
governance [37127589232](https://github.com/uibcdf/molsyssuite/actions/runs/37127589232)
passes all 278 tests on configured Python 3.14. Local governance and Ruff pass.

## Alternatives and refuted paths

An uncommitted workflow string would decouple test dependencies from the reviewed
candidate. A complete arbitrary environment file could change interpreter,
channels or the candidate. Unconditionally adding one consumer's plugins to all
members would increase every environment and still miss the next consumer's need.
The local Pytest Receptor wrapper remains a bounded equivalent until its team
reviews the new shared source and verifies its own candidate.

## Scope and exclusions

The extension applies to the shared noarch installed workflow and independently
callable local installed operations. It changes no build/upload/promotion route,
installed descriptor syntax, scientific selection or component release authority.
Other dependency formats require a reviewed extension or documented local
equivalent under the existing publication policy.

## Acceptance criteria

- Resolve committed bounded consumer tools in every declared dummy cell.
- Preserve public channels, exact prefix/minor and installed provenance guards.
- Reject source shadow and collection-only success with real pytest execution.
- Publish immutable shared source and notify uibcdf/pytest-receptor#32 plus other
  registered installed callers. Component artifact/release work remains local.
- Archive with the relevant guard and actual qualification evidence.

## Local implementation issues

uibcdf/pytest-receptor#32 owns replacing its local installed wrapper and the
actual 1.2.1 artifact/release. uibcdf/molsyssuite#78 owns build-reference adoption;
the build correction does not depend on this separate installed-tool extension.

## Dependencies and risks

Solver failures propagate. Constraints may conflict with a candidate's runtime
requirements; component owners must qualify the actual closure. The tool adapter
does not bypass metadata, use sibling source installations or authorize uploads.

## Resolution and durable guard — 2026-10-03

The shared workflow and independent `tools` operation are published at the full
qualified commit above. Candidate-owned bounded dependencies execute in every
dummy matrix cell, with normal non-editable installation and existing runtime
provenance/zero-execution controls. `tests/test_installed_noarch.py` is relevant
because its new tests fail before the extension exists, validate the real
consumer specs and rejected inputs, and inspect the actual command's prefix,
minor, public channels and propagated errors. Its existing tests preserve the
artifact/source/digest and empty-execution failure mechanisms. The hosted dummy
adds actual pytest and solver evidence rather than mocked plugin success.

Member notices go to the publication owner issues listed in the current publisher
inventory. The consumers' actual shared caller changes and staged package
qualification remain owner-local release work; they do not keep this delivered
provider capability open.

## Provenance

### Notice receipt — 2026-10-03

All six existing shared publisher consumers have received the #77 capability
notice in their publication owner issues, with exact implementation and native
qualification references. `devguide/rollouts/installed_test_tools_77.json`
retains those links and the eight passed cell identities. Actual caller/artifact
adoption remains owner-local and is not inferred from the notice.

2026-10-03, Linux workspace, local Python 3.13.15, exact consumer source at
published PR adoption `7851421c7e5385e030f900d100a9766f88045e82` and later merged
main. Native qualification uses ordinary public channels and recorded tool closure.
