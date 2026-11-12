# Complete GitHub inventories

Owner: MolSysSuite, uibcdf/molsyssuite#171. Normative action:
[remote inventory completeness](reporting_protocol.md#remote-inventory-completeness).

## Standalone operation

`devtools.scripts.github_inventory.acquire_inventory(repository, resource)`
returns a `GitHubInventory` for an explicit GitHub.com `OWNER/REPOSITORY` and
resource `issues` or `labels`. It is reusable independently of either current
consumer and uses Python's standard library. Its native transport requires `gh`
supporting `api --paginate --slurp` and ordinary read access to that scope.
It performs no write, issue notification, source checkout or scientific import.

```python
from devtools.scripts.github_inventory import acquire_inventory

inventory = acquire_inventory("uibcdf/molsyssuite", "issues")
states = {record["number"]: record["state"] for record in inventory.records}
summary = inventory.summary()
```

The issues route requests every state, normalizes open/closed state strings and
filters PRs by key presence, including an empty `pull_request` mapping. Blank or
null issue bodies remain valid. Labels retain their original fields; identity
uniqueness is case-insensitive. Duplicate issue numbers or label identities are
refused rather than silently overwritten.

The default transport invokes native `gh api --hostname github.com --paginate
--slurp` with `per_page=100` and `state=all` for issues. Native pagination must
finish successfully before records are returned. A supplied `request` callable
accepts these argument tokens and returns decoded JSON after successful native
acquisition; failure must raise. It is an acquisition boundary, not permission
to supply a partial prefix as complete.

Native transport semantics follow the [GitHub CLI API contract](https://cli.github.com/manual/gh_api)
and the [repository-label REST endpoint](https://docs.github.com/en/rest/issues/labels#list-labels-for-a-repository).

## Completeness, failures and bounds

Only a successful, validated nonempty outer page list yields an inventory.
`[[]]` is a valid empty result; `[]`, malformed pages, failed transport, invalid
record identities/states/bodies or duplicate identities yield
`InventoryUnavailable` (a `ValueError`). Consumers must retain unknown/partial
evidence and must not turn the exception into an empty inventory.

The reviewed retention bounds are 100 pages, 100 records per requested page and
16 MiB of captured/normalized JSON. Exceeding a bound refuses the result; no
partial records authorize absence or a mutation. These response checks do not
claim a streaming peak-memory limit. Native acquisition is timed out at 60 s;
there is no automatic retry or search-index fallback.

`summary()` carries schema `molsyssuite.github-inventory@1`, complete scope,
repository/resource, page and retained-record counts, PR exclusions and SHA-256
of normalized complete page JSON. It omits issue bodies and rows. This binds the
observed traversal, not a frozen board, inaccessible content or server identity.
Never infer later state or another endpoint from this receipt.

## Actual consumers and compatibility

- `component_issue_labels._list_labels` acquires every label before determining
  conformant/missing/stale relations. It no longer silently stops at 1,000.
- `upstream_release_watch.deliver_notice` uses the complete validated issue-only
  inventory before deduplication. Closed human decisions are respected, PR
  markers do not impersonate issues, and unavailable acquisition permits no
  duplicate-prone creation. Mutation/authorization remain in that owner operation.

`tests/test_github_inventory.py` covers actual consumer regressions beyond the
old cap, transport flags, later pages/mixed states, closed notices and PRs,
empty/failed/malformed/over-bound responses and mutation refusal. Existing
watcher and label-policy guards remain. No member pin, package requirement,
scientific API or release selection is changed by provider availability.

The existing MolSysMT issue reconciler and MolSysViewer board reader already
use paginated REST issue acquisition. They retain owner qualification; this
central SDK is not a mandate to import a private member implementation or
replace working owner-local tooling. Source-level label-cap findings have their
own member receiving routes, MolSysMT #724 and GH Run Receptor #85 under #171,
separate from their earlier issue fixes.
