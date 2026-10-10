# Native ABI3 Conda integration

Owner: uibcdf/molsyssuite#113. This implements the existing
[distribution policy](python_distribution_policy.md) and
[publication contract](conda_publication_policy.md). It is an optional SDK route
for members bundling CPython stable-ABI extensions. It adds no scientific suite
to routine internal pushes and does not change an existing noarch caller or pin.
Components own their native build, binary/resource validation and science.

ABI3 remains platform-specific. The source recipe uses
`build.python_version_independent: true` and host `python`/`python-abi3` at its
reviewed floor, as described by
[conda-build](https://docs.conda.io/projects/conda-build/en/stable/resources/define-metadata.html#python-version-independent-packages).
CPython with the GIL is the applicable ABI; this does not promise PyPy or
free-threaded CPython support. The source recipe must not declare `build.noarch`.
Conda may nevertheless emit Python relocation metadata in a native archive;
the artifact's actual subdir, dependencies and extension bytes are independent
checks. Do not reject legitimate relocation metadata merely because its key
contains `noarch`.

## Independently reusable recipe audit

`devtools/scripts/native_conda.py` provides:

- `inspect_recipe_dependencies(root, recipe_path, plan_path, abi3_minimum,
  aliases=None, environment_from_plan=None)`: inspect committed inputs and return
  their SHA-256 values with bounded declaration evidence;
- `inspect_rendered_dependencies(recipe, project, plan, abi3_minimum,
  aliases=None)`: compare an already rendered mapping. The caller owns its
  binding to the reviewed source, platform, build configuration and renderer.

Both reuse the existing release-plan validator and requirement comparison.
The second operation can inspect an actual conda-build rendering; neither
operation runs conda-build, imports the component, resolves dependencies,
checks native bytes or authorizes publication.

The first operation integrates with dependency-routes `@2` and `@3`:

```toml
[[recipes]]
path = "devtools/conda-build/meta.yaml"
kind = "native-abi3-dependencies"
plan = "devtools/conda-build/release_plan.toml"
abi3_minimum = "3.11"
reason = "Reviewed first native ABI3 route; installed gates remain separate"
```

The plan uses the accepted `molsyssuite.conda-plan@1` contract and
`profile = "native-abi3"`. This initial bounded recipe profile requires:

- one package/output matching project and plan name, version and build number;
- no source `noarch` declaration or skipped build;
- `python_version_independent: true`;
- the same advertised numeric Python and runtime dependency ranges as metadata;
- host `python` and `python-abi3` restricted to the reviewed minimum minor;
- an ABI3 minimum matching the advertised Python floor, and every declared
  installed minor inside that advertised range;
- no runtime `python_abi` pin that restricts installation to one minor.

This recipe kind deliberately does not accept `resources`, `resource_inventory`
or `python_build_section` from noarch inventories: native layout/resource gates
belong to their explicit component adapter and must not be inferred as executed.

Explicit Conda-name aliases retain their existing bounds. The renderer reads
only plan-derived version/build environment inputs. Existing
`environment_from_plan` mappings can translate those names. It understands
`compiler('c'/'cxx'/'fortran'/'rust')`, `PKG_HASH`, `PKG_BUILDNUM` and `PYTHON`
only as declaration placeholders. It does not select a compiler, calculate
the real package hash or execute a build script. Conditional selectors,
unknown macros and multiple outputs require per-platform rendered review
through the second API and a documented, tested local integration or a provider
extension. Do not discard selectors to manufacture a passing declaration.

The returned scope is `declared-native-abi3-dependencies`, with
`qualification = "declared-only"` and `native_bytes_verified = false`.
An outer `@2`/`@3` installed-context check may additionally verify actual
dependency versions/provenance; it still does not upgrade native byte evidence.
An example plan is usable for offline preparation, not a real release decision.

Run the existing CLI before expensive builds:

```bash
python .molsyssuite/devtools/scripts/dependency_routes.py --root . --declared-only
```

Actual resolved bounds/context checks remain the default CLI behavior for
`@2`/`@3`; select the reviewed `--context` for `@3`. Pin and verify a clean
provider checkout. Preserve discovery of all active recipes/environments/
workflows and their existing drift guards. Historical fixtures renamed to
`meta.noarch.yaml.txt` are not active recipes; a workflow that executes one
still needs route review and cannot claim current native publication.

## Compose the existing general release operations

The noarch reusable build/installed/promotion workflows remain inapplicable to
native payloads. A reviewed component-owned adapter can compose these general
operations instead. These are reusable primitives, not a qualified ElastNetMT
publisher or an automatically admitted native artifact:

| Boundary | Existing operation | Evidence still owned by the component |
| --- | --- | --- |
| Exact source gates | `preflight_conda_release.py`, including `gate_jobs` | Committed decision, actual source/test jobs and required steps |
| Native build | `uibcdf/action-build-and-upload-conda-packages@8da628d9b393e184c3bf3722708b19dcfbf7ef0a` | ABI3 configuration, build/test tools, native runner and archive validator |
| Exact staging upload | `uibcdf/action-build-and-upload-conda-packages/upload@1aa2011f902a1a9d533564572245bb29f6862e86` | Validated file, full candidate SHA, coordinate/digest and staging-only control |
| Installed run acquisition | `verify_installed_matrix.py` / `.github/actions/verify-installed-matrix` | Exact files in every claimed cell, native/resource checks and complete science |
| Immutable label promotion | `uibcdf/action-build-and-upload-conda-packages/promote@8a1f203c2cfe51acd63de7452117b4b6e9d609f4` | Successful acquired candidate/installed evidence bound to the entire inventory |
| Independent public observation | `verify_public_conda.py` / `.github/actions/verify-public-conda` | Complete original inventory, followed by clean public installation |
| Final receipt semantics | `conda_release_contract.validate_transition` | Acquired originals, not a manually asserted successful JSON |

Pin the central operations to the qualified full provider commit handed off in
the owning issue. The listed publisher action pins retain the established route;
this work does not adopt action v2.3.0 or withdrawal capabilities. Their source
contracts accept exact native subdirs; source inspection alone does not certify
the component's execution or publisher credentials.

### Build and staging

For the initial native compatibility surface select `route = "staged"`, retain
`new_compatibility_surface = true` and the required installed gate. Run the
general builder with `upload: false`, `platform_host: true`,
`platform_all: false` on each native runner. Do not use `conda convert` to claim
a native architecture. Commit the ABI3 build configuration and bind its digest
and actual toolchain to the producer receipt. Keep recipe tests enabled.

Collect `built_paths`; require exactly one file for each planned subdir. Inspect
each archive before uploading: package/version/build/subdir, runtime bounds and
ABI3 run exports, supported CPython/GIL ABI, exactly the intended extensions,
architecture/linkage, generated version and all inventoried resource bytes.
These checks and their negatives are component-owned. A passing source wheel
or sdist check does not validate a Conda archive.

Use the exact upload adapter only after the archive validator passes, with
`artifact`, `package-spec = owner/package/version/subdir/filename`,
`expected-sha256`, `candidate-sha` and `label: staging`. It seals and hashes the
local file, rejects an occupied coordinate under any label and checks registry
poststate. Retain each producer/file/upload receipt and the original archive
with attempt/platform-qualified names. A failed or uncertain upload is diagnosed
read-only before considering any retry.

### Installed artifacts

Use a component-owned manual installed workflow whose source is the candidate
for this initial native composition. Prepare verifies all producer receipts,
source SHA, registry staging labels and original digests; each cell downloads,
hashes and installs its own platform file into a clean compatible environment.
Run outside both the source checkout and any editable provider directories.
Check required dependencies, distribution/import origins, generated versions,
resources and native bytes before and after the complete installed science.
Record which single platform file the cell used and the full qualified inventory.
These checks are required again for Conda even if the earlier wheel matrix passes.
Required dependencies must resolve through the qualified public route, or the
explicit staged counterpart inventory in a coupled plan. A fixed Git installation
can establish source compatibility but cannot substitute for public dependency
closure or for the native file being qualified.

The generic verifier requires a literal preparation job and explicit required
step names for all declared platform × Python jobs. Use its `job_template` when
local job names differ. For Linux x86_64/macOS arm64 × Python 3.11–3.14 this means
eight executed installed cells and two immutable platform files. Overall green,
skipped science, an environment solve or import-only evidence is insufficient.
The matrix verifier proves native job/step execution; file/resource/scientific
receipts supply their separate facts. Acquire them and fail before promotion
when any identity, cell or required step disagrees.

The existing cross-source recovery binding is limited to one noarch `.tar.bz2`
file. It must not be reused for a different qualification SHA with two native
files. Such recovery needs a reviewed provider extension/equivalent and its
own negative tests; retaining original producer identities is mandatory.

### Promotion and public receipts

Immediately before mutation, reacquire exact-source gates and installed run
evidence, validate all original file receipts and their complete matrix, and
recheck both staged coordinates/digests. Promote each original file individually
with `from-label: staging`, `to-label: main`; keep per-file receipts distinct.
The generic promoter changes labels and never rebuilds or uploads replacement
bytes. Preserve staging labels. If one promotion fails, inspect the current
labels/digests; do not rebuild either file or replace a successful coordinate.

The promoter's raw `uibcdf.conda-promotion@1` receipts do not contain the source
SHA or complete inventory. A reviewed adapter binds them to the already checked
producer and installed receipts and assembles the suite promotion receipt.
Do not treat their `status` field alone as candidate admission.
Independently verify the full original inventory through the public API and
solver indexes. Feed the acquired source gates, installed cells, promotion
receipts and public observations to `validate_transition`. Clean public-channel
installation follows separately before advertising availability.

## Initial receiving owner and unresolved qualification

ElastNetMT's native work is owned by uibcdf/elastnetmt#26; its distribution review
is uibcdf/elastnetmt#18. Its source work is active, historical noarch callers are
suspended and no real candidate/version has been selected. This SDK addition
allows preparation of a native recipe without weakening a noarch guard.
Local native adapters, negative archive/resource checks, real installed Conda
evidence and authorized publication remain owner acceptance criteria. They are
tracked in uibcdf/molsyssuite#113; declaration availability does not close them.

The existing bounded exception route in the distribution/publication policies
remains applicable. Other native minimums, render engines, architectures or
recovery shapes require explicit review; a successful guessed interpretation
is not an exception. No package or remote tag is produced by this integration.
