# Guide and policy adoption lifecycle

This document is normative for every repository registered in `suite.toml`. Accepted by
`uibcdf/molsyssuite#34`, with latest-policy adoption required by #201 from
2026-11-15 onward.

The current central member-policy release is recorded in `suite.toml`; each
member's effective automated policy is the release pinned by its caller.
Every registered member must adopt the latest published policy release or have
an explicitly accepted, owned, unexpired exception. A compatible older release
retains its historical execution contract and is still pending current-policy
adoption. This applies to scientific/support/developer/auxiliary members and
non-Python umbrellas; capability-specific rules retain their applicability.
The central repository participates through its live registry, validators and
exact-source governance CI rather than inventing a member self-caller. The recorded
MOLI commit is platform-contract context for MolSysSuite as a component, not a
source of member engineering values. Historical member checks remain
reproducible through their called suite policy release.

This live inventory covers guide copies and versioned policy callers. The
suite support-library and developer-tool policies have a
separate member review inventory in `suite.toml`, displayed by
`devtools/scripts/python_ecosystem_status.py`. A current guide or compatible
caller does not establish adoption of those policies.

## Two independent adoption records

A synchronized guide and a versioned policy caller are separate contracts. A prose-only
guide publication never requires a policy pin change. A new required policy release never
implies that a guide copy was reviewed or synchronized. The central inventory therefore
emits one record per guide-to-consumer relationship and one policy-caller record per
applicable member.

Each record carries the consumer repository as its adoption owner, the expected source or
release, the observed copy or caller, exact content revisions where applicable, its state
and one next action. The canonical guide repository still owns guide content; the consumer
owns reviewing and adopting that content in its repository.

The accepted states are:

- `current`: a guide copy matches its source, or a policy caller pins the central
  policy release;
- `compatible`: a policy caller uses another release admitted by the same minimum
  release gate and member-specific Ruff CI rules as the repository checker;
- `stale`: a guide copy differs, or a policy caller is not admitted;
- `missing`: the required local surface is absent;
- `excepted`: a non-current record has a registered, unexpired exception;
- `unavailable`: the source or consumer checkout could not be inspected.

`compatible` describes capability compatibility, not successful latest-policy
adoption. Under the live #201 rule, policy `--check` accepts only `current` or
`excepted`. Frozen registries without the new rule retain their earlier behavior.
`unavailable` is incomplete evidence, never success. An exception does not make a stale
copy current; it makes the bounded deviation visible until its expiry.

## Live inventory

From the MolSysSuite checkout, with member repositories as siblings, run:

```bash
python devtools/scripts/adoption_status.py ..
```

The default output is a reviewable line per record. JSON is available for automation:

```bash
python devtools/scripts/adoption_status.py .. --format json
```

Use repeatable `--kind guide`, `--kind policy` and `--repository` selectors for a bounded
rollout. `--check` requires current policy adoption or an accepted exception;
guide records retain their byte-level criteria. All members and a separate
`central-governance` row are included. For policy records, `expected` names the
latest target and is an equality requirement for actual reusable-job callers.
Comments, examples and nested workflow backups cannot manufacture a caller.
Malformed/ambiguous YAML remains unavailable. `required-policy-release` is the minimum for
the release-version gate. The explicit compatibility lists exclude releases such as
`policy-v1.4.7`, regardless of their version number. Transition members use the
restricted transition-compatible list for suite Ruff CI coverage, unless their
own workflow supplies both required Ruff commands. The inventory uses the same
release and Ruff CI decisions as `check_repository.py`.
The current source checker separately reports `LATEST_POLICY` for a non-current
caller or missing/ambiguous declaration, including non-Python members. This live
rule does not rewrite an immutable historical checker or its compatibility set.

For a live qualification, additionally resolve all official policy tags and
retain bounded source identities:

```bash
python devtools/scripts/adoption_status.py .. --kind policy \
  --verify-published-policy --check --receipt policy-adoption.json
```

The authoritative tag target must agree with `governance.policy-release`;
transport failure, no valid tags or a newer published release means unknown or
pending reconciliation, never automatic acceptance or a tag move. Offline
inventory checks use the declared cached target and do not claim fresh remote
verification. Source records and workflow hashes do not by themselves prove
executed conformance or adoption of every semantic requirement. Qualify receiving
from fresh committed default-branch sources and retain owner gate evidence.
Maintainers run the complete check before declaring a guide publication or required policy
release fully adopted. The scheduled central guide guard remains independently blocking
for byte drift and missing copies.

The separate `audit-policy-adoption.yaml` workflow enforces the live target on
trusted main/tag events, a weekly schedule and explicit administrative dispatch.
It retains a bounded receipt even when target verification fails. Its rollout
result is independent of policy-definition qualification: a new immutable policy
can be qualified and published before its consumers migrate to it. An incomplete
rollout cannot be reported as adopted, and does not require weakening the guard
or moving historical tags to qualify a later definition.

## Publication-to-adoption procedure

1. Publish and validate a canonical guide in its owner repository, or publish the
   immutable central policy release.
2. Open or update one central rollout issue. Record the affected consumers, the source
   revision or required release, and the reason adoption is needed.
3. Refresh the registered checkouts and run the inventory. Do not infer adoption from an
   issue, a planned commit or a locally edited copy.
4. Prepare reviewable consumer changes. Guide copies come only from
   `sync_vendored_guides.py`; policy callers change only when that policy release is part
   of the rollout. Never couple the two mechanically.
5. Run the consumer's local checks and the central targeted checks. Preserve unrelated
   failures as prior debt rather than claiming the rollout caused or repaired them.
6. Commit and publish each consumer change, then repeat the live inventory against the
   published default branches.
7. Close the rollout when every affected record meets the latest published target
   and is `current` or has an explicit, unexpired exception with a
   tracking issue and removal condition. A compatible older caller alone does not
   prove adoption of a specifically targeted newer release.

Each policy rollout has a linked owning implementation issue for every member
and MolSysSuite itself. Include the previous/target release and immutable source,
actual policy callers and other reusable pins, guide/local-instruction scope,
required input changes (including admission SHA), relevant executed checks and
precisely pending evidence. Keep independently qualified scientific/installed
SDK pins unless their actual contract changes. A version edit is not a new
scientific or public-package qualification. A guide-only copy remains separately
coordinated; guide availability does not add runtime dependencies.

Every later policy publication repeats this inventory/handoff/receiving process.
New components start from the latest published policy using the official starter
and valid separate admission. Its CLI checks the remote target before writes;
`--offline-policy-target` is an explicit fixture route and cannot certify latest
publication. Never create a policy release merely to add a member. #201 starts
with the already published policy-v1.5.12; older compatible callers are not
retroactively described as failing their original qualification.

## Exceptions

An exception is a top-level `[[adoption-exceptions]]` entry in `suite.toml` with exactly
one `kind` (`guide` or `policy`), registered `repository`, matching `item`, central or
component tracking `issue`, concrete `reason`, ISO `expires-on` date and testable
`removal-condition`. Expired or malformed entries do not suppress a finding.

Exceptions are for bounded inability to adopt, not for leaving a rollout unassigned. A
guide exception names its root filename. A policy exception uses `policy-caller` as the
item. The inventory continues to show the underlying expected and observed values.
