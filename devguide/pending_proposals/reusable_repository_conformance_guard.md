---
summary: A central read-only guard measures repository conformance with suite policy.
issue: uibcdf/molsyssuite#5
status: active
opened: 2026-09-06
closed:
verification: measured
area: [governance, tooling, ci]
guard:
normative:
blocked_by: []
supersedes: []
---

# Suite policy has no repository conformance guard

**Reported:** 2026-09-06, after adopting policy version 1.0.
**Status:** Active; tests define the required read-only audit behavior before implementation.

## What

Provide one central command that reports whether a member checkout follows the policies
applicable to its registered profiles. Make the same command callable by a minimal reusable
GitHub workflow.

## How

Read `suite.toml`, identify the member by repository, and inspect its checkout without
writing to it. For Python libraries, check package metadata, Ruff baseline, active legacy
gates and CI minors. For every member, check the pointer to central governance. Report all
independent findings in one run rather than stopping at the first.

## Why

Eleven repositories cannot be kept aligned reliably by prose review. A central audit turns
the policy into an observable contract without adding a package dependency to members or
copying validation code.

## What is measured and what is assumed

The fixture suite covers a conforming Python member, five simultaneous violations, an
unregistered repository and byte-for-byte preservation of the inspected checkout.

An initial read-only run over all eleven local checkouts found no unexpected crash and
reported all repositories independently. `pytest-receptor` and `gh-run-receptor` need only
the governance pointer under the current checks; the other members also have one or more
Python, Ruff or legacy-tool findings. These results validate the reporting path but belong
to the rollout rather than to this checker's acceptance.

## Alternatives and refuted paths

- Copying the checker into every member was rejected because the copies would drift.
- Centralizing each member's installation and tests immediately was rejected because
  dependency environments differ and the pilot has not established a safe common subset.
- Fixing findings automatically was rejected because the guard must be read-only.

## Scope and exclusions

This theme implements inspection and reusable invocation. It does not change member
repositories, install their dependencies or assert scientific correctness.

## Acceptance criteria

- Positive and negative fixture tests define behavior before implementation.
- The checker reads policy from `suite.toml` and never writes into the target.
- All independent findings are returned in one run with stable codes.
- The reusable workflow contains no member-specific installation logic.
- The command needs only Python's standard library.

## Local implementation issues

None. Pilot adoption will be tracked separately.

## Dependencies and risks

Static inspection of YAML without a YAML dependency is intentionally conservative. The CI
check only verifies presence of supported version literals; execution remains the evidence
that a workflow actually works.

## Provenance

Measured on 2026-09-06 with Python 3.13.15:

```bash
python devtools/scripts/check_repository.py ../<member> --repository uibcdf/<member>
python -m unittest discover -s tests -v
```
