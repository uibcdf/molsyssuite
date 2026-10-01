# Conda staging, publication and independent verification

## Applicability and profiles

This shared contract, coordinated in uibcdf/molsyssuite#27, applies when a member
publishes Conda packages or participates in a coordinated Conda release. It adds
no scientific suite to ordinary internal development pushes. Components retain
their recipes, supported targets, dependencies, tokens and release decisions.

Choose a topology from the artifacts actually distributed:

- `native-abi3`: one native file per claimed subdir; test every claimed platform
  and supported Python minor with the installed artifacts.
- `noarch-python`: build one file once; test installation on the claimed
  platforms/Python minors, including command launchers and packaged resources.
- `metapackage`: one dependency bundle; test dependency resolution and its actual
  installed capabilities. A metadata-only package does not inherit another
  component's scientific suite.

A profile does not require a particular component name, OS matrix or scientific
test vocabulary. ABI, architecture, resource and launcher checks stay local.
New artifact kinds require an explicit central contract extension or exception.

## Candidate identity and the pre-tag decision

Commit the reviewed release decision before tagging. Record the canonical X.Y.Z
version, route, reason, responsible maintainer, artifact subdirs, supported test
platforms/Python minors, required native workflows and objective route conditions.
The versioned template is `devguide/templates/conda_release_plan.toml`; an
equivalent local plan is allowed when its checked fields have the same meaning.

The final tag commit supplies the candidate's full 40-character SHA. Record it in
the runtime receipt with matching checkout/tag SHAs and native gate run IDs. A
commit cannot contain its own hash: do not introduce a recursive plan requirement.
Staging an untagged commit may create an ephemeral local tag for version discovery;
it never moves or creates a remote public tag automatically.

Every new applicable release checks its committed plan and evidence with
`conda_release_contract.py` or a reviewed, tested local equivalent. Gate acquisition
must independently query native GitHub status/head SHA; passing a handwritten
evidence JSON file is not proof that a gate ran. A receptor summary cannot
authorize publication on its own.

## Route selection

Staging is mandatory if an installed candidate/pair must pass before the first
public file, the release adds an unvalidated compatibility surface, a coupled
set must be validated together, or a version already has any registered files.
This includes new architectures, Python/ABI support, native code, resources,
launchers and dependency changes whose compatibility needs pre-public evidence.

Direct publication is allowed when all dependencies are already publicly
resolvable, no required pre-public installed gate remains, every exact-source
gate passes, and a fresh all-label Anaconda release query conclusively returns
404 for the version. A response error, malformed metadata or existing staging
file cannot establish absence. Being pure Python or a patch release alone does
not justify direct publication.

Keep the automatic `release: released` direct route for eligible candidates.
Manual builds are staging-only, even for internal maintainers. Existing staged
files of a version are promoted exactly; they are never rebuilt and reuploaded
under the same coordinate. Normal pushes, PRs and schedules use public dependency
channels; staging is an explicit manual integration route.

The ordinary direct route is not atomic with GitHub Release publication: a
released source may temporarily precede a Conda package. This is acceptable only
where the pre-tag plan records that ordinary direct publication meets all gates;
the receipt and independent post-publication verification still control any
claim that Conda publication completed. Coupled pre-public gates use staging.

## Staging, installed gates and immutable promotion

Staging normally runs recipe tests. A first producer in a real dependency cycle
may use `--no-test` only with an issue-backed bootstrap exception specifying the
cycle, exact candidate, responsible maintainer, counterpart test and expiry.
The counterpart's complete installed gate must pass before public promotion.
Public builds and promotions never use `--no-test`.

Record every exact owner/package/version/subdir/filename, build number and SHA-256.
The installed matrix identifies the tested files and their counterpart inventory,
runs outside source/editable checkouts, and proves all claimed cells executed.
Do not substitute a hard-coded historical job count for the declared current
platform × Python matrix. A noarch build is not an interpreter build matrix.

Promote immutable validated bytes from `staging` to `main`, dependency first and
then consumer as recorded in the coordinated plan. Retain source labels and
verify the target label. Repairs use an additive build number. Rollback restores
the reviewed label set or selects a corrected additive build; it never deletes
or overwrites a published coordinate or moves a public tag.

## Evidence boundaries and shared units

The shared units have independently usable versioned contracts:

1. `devtools/scripts/conda_release_contract.py` validates decision/evidence
   semantics and audits objective publication workflow controls. It never
   publishes and does not acquire or certify scientific evidence.
2. `.github/workflows/check-conda-publication.yaml` runs that administrative
   conformance audit against a caller checkout; pin it to an immutable provider.
   `devtools/scripts/preflight_conda_release.py` acquires successful native runs
   at the exact candidate SHA and the fresh all-label query for a direct route;
   its `molsyssuite.conda-preflight@1` receipt cannot establish post-public state.
3. `.github/actions/verify-public-conda` checks an exact file's public main label,
   identity, subdir, build number and SHA-256 against both Anaconda metadata and
   the solver index. Its `evidence-path` output is independent public evidence.
4. `.github/workflows/verify-public-conda.yaml` and the CLI
   `devtools/scripts/verify_public_conda.py` recheck an explicit complete JSON
   inventory without invoking a promotion. Each coordinate has exactly
   `package`, `version`, `subdir`, `filename` and `sha256`. This permits exact
   coupled-pair rechecks, including historical targets.
5. `.github/actions/verify-installed-matrix` and
   `devtools/scripts/verify_installed_matrix.py` check an existing native run's
   exact source/workflow/pair title, attempt, every declared job/cell and required
   successful installed-evidence steps. The descriptor supplies platform/Python
   sets, preparation job, required step names and an optional job-name template.
   `.github/workflows/verify-installed-matrix.yaml` rechecks historical evidence
   without executing scientific tests. Mixed attempts, incomplete inventories,
   failed/skipped cells or steps, and a rerun during acquisition all fail closed.

Pin shared publisher actions to a reviewed release or full commit; use full
commits for the central verifier/guard. Retain producer evidence and promotion
receipts with `always()` when the action exposes a path, including failed runs.
Preserve independent public evidence separately. The read-only verifier needs
no registry token, package download or Conda installation. It uses a non-login
shell: login logout hooks caused the false red in uibcdf/molsyssuite#48.

`molsyssuite.public-conda@1` reports `verified` only when every declared coordinate
matches both sources. A mismatch, ambiguous record, unavailable service or
exhausted propagation window exits nonzero with `unverified` evidence. The
default six attempts are 15 seconds apart; requests time out after 20 seconds,
responses are capped at 16 MiB, and attempts/interval are bounded to 12/30 seconds.
Only propagation/temporary HTTP conditions are retried; contradictions fail
immediately. Rerun only the read-only boundary after a verifier/index failure.

Producer events, promotion receipts, public API labels, solver indexes and
installed-package/pair tests prove separate facts. Native workflow conclusions
and independently queried channel state remain authoritative. Inspect compact
`gh-run-receptor` evidence first when applicable; request only needed native
details. Never treat a compact summary as an upload permission.

## Adoption and exceptions

The policy is prospective for new/changed release work. Historical published
artifacts and exact-tag workflows are preserved. Existing local route validators
may remain when they implement this contract; central reuse is required for the
shared independent verifier as those workflows are changed.

The lightweight publication conformance guard is separate from existing pinned
Python policy callers. Adoption of this guard does not silently change a
historical `policy-vX.Y.Z` gate, require a policy release, or certify scientific
correctness. Its checked invariants include reviewed publisher pins, staging-only
manual builds, exact candidate checkout, public recipe testing, no overwrite,
receipt retention, public ordinary environments and pinned independent verification.
It does not statically prove shell control flow or actual release readiness.
It recognizes the suite's build/promotion actions; custom publisher implementations
need a reviewed profile extension or a tested local equivalent. Decision/evidence
JSON validation checks the acquired inputs and never substitutes for independent
native/API acquisition. The central preflight supplies that separate acquisition.

A bounded exception states the affected rule/profile, owner issue, rationale,
interim controls, responsible maintainer, review/expiry and removal condition.
Missing or expired exceptions require correction before the next affected
publication. Component maturity alone is not an exception. The central
metapackage publisher's explicit migration exception is recorded in
`devguide/rollouts/conda_publication.md`; it may not claim full conformance.

Maintain the adoption inventory separately from normative acceptance. Every
component uses the synchronized `MOLSYSSUITE_GUIDE.md` policy route and checks
applicability before preparing an affected release.
