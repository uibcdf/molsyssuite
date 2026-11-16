# Generic Conda resource profile

Accepted under uibcdf/molsyssuite#199, extending the
[common publication contract](conda_publication_policy.md). The initial
`generic-resources` profile receives architecture-independent JavaScript ESM,
declarations and resources under `$PREFIX/share/<package>`. It is distinct from
`noarch-python` and a dependency-only metapackage. The initial shared inspector
supports one original `.tar.bz2`, `noarch: generic`, build `res_<number>`; other
archive/payload kinds need reviewed tested receiving rather than a renamed profile.

## Original bytes and installed identities

Bind a canonical source/tag/version, exact Conda coordinate and SHA-256 through
the existing plan, producer, staging, native gate and independent public controls.
Every declared workflow names its actual required jobs/steps. New compatibility
surfaces use staging; original staged bytes are promoted without rebuilding.
Local build/layout/administrative fixtures authorize no package upload.

Use `generic_resources.inspect_artifact` on the original archive and
`inspect_prefix` on the actual installed/relocated resource root. The package
JSON and asset manifest must agree with candidate identity, expose exact import
and declaration entries and retain the license. The complete manifest binds
every resource by SHA-256; missing, additional, changed, duplicate, linked or
escaping paths refuse receiving. No native binary, site-packages, Python payload
or development tooling may be concealed in this profile. Keep runtime dependency
closure explicit; a browser-only asset does not acquire a Python/Node runtime
requirement merely because build/tests use those tools.

The asset identity receiver does not execute scientific or consumer code. A
separate independent installed consumer must import the actual installed ESM,
receive declarations/resources/version and relocation, and run the meaningful
owner controls from outside source clones. Browser/Qt/other hosts and both
scientific surfaces require their own finite receiving. Prefix smoke checks and
synthetic fixtures cannot establish those wider results.

## Runtime cells and promotion

The additive plan profile uses nonempty `runtime_versions` such as `node24`
with actual `test_platforms`; `python_versions` is absent or empty. Do not invent
Python minors to make an installed matrix look populated. Existing Python/ABI
profiles retain their unchanged mandatory Python matrix.

Every generic installed cell binds candidate, original inventory, runtime,
successful native consumer and the schema `molsyssuite.generic-resources@1` asset
receipt. It includes exact package/version/resource root/file hashes,
`candidate_sha`, `artifact_sha256`, the actual `node_version` matching its runtime
cell and `consumer = passed` only after execution.
The contract refuses omitted/duplicate/failed/wrong-runtime cells, changed bytes
and an identity-only receipt without consumer evidence. The same requirement
holds for any later eligible direct route; recipe success alone does not bypass
this profile's installed matrix.

Receipt validation alone is not independent execution evidence. The owner route
must use native exact-source/attempt/job/step acquisition and digest-checked
attempt-qualified artifacts under the common contract. Reuse the existing
builder/uploader/promotion provider and independent public verifier, with a
documented tested local adapter for this artifact kind. Python-only noarch SDKs
remain Python-only; do not silently substitute a generic profile into them.

The central provider fixture, adversarial guards and a real private fixture
archive qualify the engineering mechanism only. MolSysSketcher's original
component archive, installed visual consumers, platform claims and public release
remain owner-local follow-up under #199. No private 0.0.0 bootstrap artifact is
a selected component release.
