# Shared noarch Python publication workflow

Coordination: uibcdf/molsyssuite#45. Normative rules:
[Python distribution](python_distribution_policy.md) and
[Conda publication](conda_publication_policy.md). This capability applies to a
member preparing or changing a qualifying Conda publication route. Existing
native publishers retain their reviewed profiles. Ordinary internal push CI is
outside this capability.

## When to use `noarch: python`

Use it when the installed artifact contains Python modules and architecture
independent resources, with identical runtime payload and dependency declarations
on every claimed OS/interpreter. Third-party native dependencies supply their own
platform artifacts and do not alone disqualify the Python consumer. Browser
bundles, schemas and data can qualify when their bytes are platform independent.

Bundled extensions, native executables, interpreter ABI bindings, fixed OS paths,
or selectors changing runtime payload/dependencies need a native or reviewed
local profile. A dependency bundle without Python code uses the metapackage
profile. See the [Conda metadata reference](https://docs.conda.io/projects/conda-build/en/stable/resources/define-metadata.html)
for noarch installation and selector constraints.

One file does not certify an OS or Python minor. Keep the component's actual
claimed installed matrix and resource/launcher checks. The first migration from
per-platform files to noarch requires staging and installed qualification. Preserve
historical artifacts; never replace their bytes. Choose an additive build/version.

## Shared implementation and applicability

Qualifying new or changed routes use these reusable workflows or a documented
reviewed tested equivalent implementing their gates. A bounded policy exception
names the rule, owner issue, reason, interim controls, owner, expiry and removal
condition. Special component conditions do not weaken another component's gates.

- `.github/workflows/publish-noarch-conda.yaml`: build exactly once, run recipe
  tests, inspect the file **before** upload, then upload those exact bytes to
  staging or an eligible automatic direct release.
- `.github/workflows/promote-noarch-conda.yaml`: verify an existing installed
  matrix, promote the same file by digest and independently verify public label
  and solver index. It never rebuilds or repeats scientific tests.
- `devtools/scripts/noarch_conda.py`: shared early recipe/resource, embedded
  version and archive checks. It makes no publication or install claim.

Pin callers to a reviewed **full MolSysSuite commit**, explicitly map the existing
member secret to `ANACONDA_TOKEN`, and grant only `contents: read` and `actions:
read`. The workflows check out their own implementation through
[`job.workflow_sha`](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts#job-context),
which identifies the workflow defining the current job on GitHub.com.

The initial adapter supports setuptools/versioningit, canonical X.Y.Z versions,
a single `py_BUILD.tar.bz2` file, literal recipe requirements and resource paths.
Other backends, conditional dependencies or formats need a reviewed extension or
local equivalent. Exact-file upload belongs to the build/upload provider under
[uibcdf/action-build-and-upload-conda-packages#45](https://github.com/uibcdf/action-build-and-upload-conda-packages/issues/45).
Producer observations, independent public evidence and installed evidence remain
separate. An uncertain poststate never authorizes repeating a mutation to get green.

## Committed member inputs

Keep recipe and inventory in `devtools/conda-build/`. A
`release_plan.example.toml` is an onboarding example, **not** a release decision.
Before a candidate, fill and commit `release_plan.toml` from the
[versioned template](templates/conda_release_plan.toml): exact version, immutable
build number, decision owner/date, route conditions and actual platform/Python
sets. Do not embed a commit's own hash in itself.

The adapter requires `gate_jobs` for **every** required native workflow. Name the
source scientific jobs and executed test steps. A green recovery probe with
skipped science cannot authorize an upload. Example of one cell:

```toml
[gate_jobs.".github/workflows/CI.yaml"]
"Test on ubuntu-latest, Python 3.13" = ["Run tests"]
```

Declare every required source-CI cell. Preflight independently queries native
run/source/attempt/job/step facts; unrelated decision jobs may intentionally skip.

`resources.toml` names `version_file`, literal noarch `required_paths` and a
review rationale. Include runtime data/schemas/bundles. A version module generated
by the declared versioningit target may be absent in source. After candidate CI
verification, the helper freezes static project metadata and that module **only
in the ephemeral build checkout**. This generalizes SMonitor's existing static
version release preparation; it never changes maintained source or remote tags.

Declare `build.noarch: python`, `string: py_BUILD`, Python/dependency constraints
matching `pyproject.toml`, and exact console entry points when present. Use host
Python/pip/setuptools/versioningit and `python -m pip install --no-deps
--no-build-isolation .`; Conda provides dependencies. Build tools are not runtime
requirements unless runtime code uses them. Ordinary channels are `uibcdf`, then
`conda-forge`, with strict priority. Do not convert or fan out this one archive.

## Staging and installed qualification

Dispatch the build wrapper with full candidate SHA and reviewed version. Manual
upload requires a staged plan; the first noarch migration uses staging. Eligible
direct plans cannot publish manually; staged plans cannot use the automatic direct
release route. Missing plan, CI evidence or resource stops before uploading.
Credential access stays unknown until an authorized maintainer confirms it.

The component owns its installed scientific gate and test selection. Before
promotion, commit the gate workflow and an `installed_gate` table in
`resources.toml`: `workflow`, `platforms`, `python_versions`, `prepare_job`,
`job_template`, `required_steps`. Sets must equal the release plan. It must install
the exact staged file, check SHA-256 and installed identity/resources/launchers
outside the source checkout, and execute the complete declared scientific
selection in every cell. Editable/source sibling installs do not prove public closure.

The native installed run title must be exactly:

```text
Installed PACKAGE-VERSION-py_BUILD.tar.bz2 SHA256
```

Run at the same candidate SHA as source gates. Dispatch promotion with that SHA,
version, digest and existing installed run ID. The common verifier requires all
jobs and test steps to succeed at the same attempt; missing, skipped, failed,
duplicate or raced evidence fails closed. Scientific failures prevent that
candidate's promotion and stay with the component team.

For later ordinary releases, a reviewed direct plan is allowed only when every
staging condition is false and dependencies resolve publicly. The release wrapper
passes the full tagged SHA; preflight checks tag/checkout and all-label version
absence. Upload seals and verifies the exact artifact and never overwrites an
occupied coordinate. Source, artifact, producer, promotion, installed and public
receipts are retained separately.

Configuration and offline example-plan checks prove administrative readiness only.
Record a build, installed or public claim only after it actually occurs.
