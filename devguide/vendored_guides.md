# Vendored integration-guide policy

This document is normative for repositories carrying the `python-library` profile in
`suite.toml`. Accepted by `uibcdf/molsyssuite#12`.

## One owner and exact consumer copies

Every shared integration guide has one canonical repository and path registered in
`suite.toml`. The canonical repository owns its content, review and formatting. Each
listed consumer carries the guide at the repository root as a byte-identical copy.

The canonical file includes this synchronized-content marker and its full GitHub source
path; synchronization copies that header together with the rest of the document:

```text
SYNCHRONIZED MOLSYSSUITE GUIDE — DO NOT EDIT COMPONENT COPIES.
Canonical source: https://github.com/uibcdf/<owner>/blob/main/<path>
```

Contributors edit the registered source in its owning repository. Distribution is a
suite-level operation because `suite.toml`, rather than an individual provider, owns the
complete source-to-consumer topology. They do not repair a consumer copy locally or
maintain a separate synchronization script in every provider. Adding or removing a guide
or consumer requires updating the central registry so that the inventory remains
executable.

From a workspace containing the registered repositories as sibling checkouts, use the
central command in check mode first:

```bash
python devtools/scripts/sync_vendored_guides.py
```

The command reports missing or different copies without modifying them. After reviewing
the canonical changes, synchronize every registered relationship explicitly:

```bash
python devtools/scripts/sync_vendored_guides.py --write
```

Use repeatable selectors for a bounded rollout. A guide selector is its registered root
filename; a repository selector accepts either its member name or full repository ID:

```bash
python devtools/scripts/sync_vendored_guides.py \
  --guide SMONITOR_GUIDE.md --repository pyunitwizard --write
```

The synchronizer validates all selected sources, markers, and consumer checkouts before
writing any copy. Write mode also queries each owner's remote `main`: it refuses a source
checkout whose guide has uncommitted changes or whose `HEAD` is not the published remote
revision. It likewise refuses to overwrite a differing consumer copy when that path has
local Git changes. This prevents an apparently synchronized but stale provider checkout
from downgrading current consumers and protects unpublished contributor work.

Content review and validation remain the guide owner's responsibility; central
synchronization does not make MolSysSuite the content owner. Commit and publish the
canonical guide first, update its local checkout with `git pull --ff-only`, then use the
central write command. The older `sync_component_guide.py` command remains a focused
compatibility entry point for `MOLSYSSUITE_GUIDE.md`, but new automation should use the
registry-driven command.

## Formatter boundary

The owner may format the canonical source with its own configuration. Every consumer
lists the exact root filename under `[tool.ruff].extend-exclude`; Ruff therefore neither
formats nor lints the synchronized copy with host-specific settings. Canonical sources
under `standards/` remain in the owner's Ruff scope.

An explicit path is required for each registered guide. A blanket Markdown exclusion is
not sufficient because repository-owned Markdown snippets should still receive local
checks. Authors should keep fenced code readable at the suite's common widths, but that
is a portability aid rather than a substitute for the ownership boundary.

## Verification

The repository conformance guard checks that every registered copy present in a Python
member is marked and explicitly excluded from Ruff. The cross-repository synchronization
guard checks the complete inventory from `suite.toml`, including missing files and exact
byte equality with each registered source.

This separates two different questions: the host repository proves it will not rewrite
foreign content, while the suite proves that the foreign content has not drifted.

## Exceptions

A temporary exception names the consumer, guide, tracking issue, reason and removal
condition. Different host formatter settings are expected and are not grounds for an
exception; they are the reason this policy exists.
