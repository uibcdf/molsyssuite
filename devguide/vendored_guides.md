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

Contributors edit the registered source and run the owning synchronization procedure.
They do not repair a consumer copy locally. Adding or removing a guide or consumer
requires updating the central registry so that the inventory remains executable.

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
