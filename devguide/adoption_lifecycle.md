# Guide and policy adoption lifecycle

This document is normative for every repository registered in `suite.toml`. Accepted by
`uibcdf/molsyssuite#34`.

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

- `current`: observed content or caller equals the requirement;
- `stale`: an older or different value is present;
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
rollout. `--check` returns nonzero for every state except `current` and `excepted`.
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
7. Close the rollout only when every affected record is `current` or has an explicit,
   unexpired exception with a tracking issue and removal condition.

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
