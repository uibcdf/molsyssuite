# Guide and policy adoption lifecycle

This document is normative for every repository registered in `suite.toml`. Accepted by
`uibcdf/molsyssuite#34`.

The effective central governance snapshot is the pair recorded in `suite.toml`:
MOLI `6a91433bd38582980d0781474be6a80c58f48886` and MolSysSuite
`policy-v1.4.11`. The MOLI policies linked from the suite adoption profiles point
to that commit. Links to MOLI `main` describe the latest upstream policy and
must not be used as evidence of the effective snapshot.

This live inventory covers guide copies and versioned policy callers. The
newly inherited MOLI support-library and developer-tool policies have a
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
rollout. `--check` returns nonzero for every state except `current`, `compatible` and
`excepted`. For policy records, `expected` names the central release; it is not an
equality requirement. `required-policy-release` in `suite.toml` is the minimum for
the release-version gate. The explicit compatibility lists exclude releases such as
`policy-v1.4.7`, regardless of their version number. Transition members use the
restricted transition-compatible list for inherited Ruff CI coverage, unless their
own workflow supplies both required Ruff commands. The inventory uses the same
release and Ruff CI decisions as `check_repository.py`.
Maintainers run the complete check before declaring a guide publication or required policy
release fully adopted. The scheduled central guide guard remains independently blocking
for byte drift and missing copies.

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
7. Close the rollout when every affected record meets the rollout's recorded target
   and is `current`, `compatible` or has an explicit, unexpired exception with a
   tracking issue and removal condition. A compatible older caller alone does not
   prove adoption of a specifically targeted newer release.

The inventory assigns work to the consumer repository. A member-specific issue is needed
only when adoption requires local design, migration or an exception; a byte-identical copy
alone remains coordinated by the central rollout issue.

## Exceptions

An exception is a top-level `[[adoption-exceptions]]` entry in `suite.toml` with exactly
one `kind` (`guide` or `policy`), registered `repository`, matching `item`, central or
component tracking `issue`, concrete `reason`, ISO `expires-on` date and testable
`removal-condition`. Expired or malformed entries do not suppress a finding.

Exceptions are for bounded inability to adopt, not for leaving a rollout unassigned. A
guide exception names its root filename. A policy exception uses `policy-caller` as the
item. The inventory continues to show the underlying expected and observed values.
