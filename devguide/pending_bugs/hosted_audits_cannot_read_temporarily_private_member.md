---
summary: Track hosted cross-repository audits blocked while OpenCASTp is temporarily private.
issue: uibcdf/molsyssuite#102
status: partial
opened: 2026-10-04
closed:
severity: medium
verification: reproduced
area: [governance, automation, compatibility]
guard:
normative:
blocked_by: []
supersedes: []
---

# Hosted audits cannot read a temporarily private member

## What

The maintainer confirms OpenCASTp's private visibility is intentional and
temporary. The five cross-repository audits triggered by registry commit
`a3a376e451a0882e209cdc3af0787d1e59ee8198` fail acquiring that registered
source or its labels. Central governance passes independently. No scientific
or component implementation defect is inferred from these access failures.

## How

GitHub's authenticated repository metadata reports `uibcdf/opencastp` private.
Published GH Run Receptor 1.2.0 first inspects the failed native runs; their
failed-step logs corroborate the access limitation:

| Audit | Native run | Executed failure |
| --- | --- | --- |
| Component labels | [37230243819](https://github.com/uibcdf/molsyssuite/actions/runs/37230243819) | Repository-scoped token cannot resolve OpenCASTp. |
| Vendored guides | [37230243826](https://github.com/uibcdf/molsyssuite/actions/runs/37230243826) | Unauthenticated clone cannot acquire HTTPS credentials. |
| Joint development environment | [37230243818](https://github.com/uibcdf/molsyssuite/actions/runs/37230243818) | Same source-fetch failure before installation/runtime qualification. |
| Component guides | [37230243839](https://github.com/uibcdf/molsyssuite/actions/runs/37230243839) | OpenCASTp checkout returns Not Found. |
| Dependency manifests | [37230243829](https://github.com/uibcdf/molsyssuite/actions/runs/37230243829) | OpenCASTp checkout returns Not Found. |

The source-fetch jobs use unauthenticated clones or the central repository's
checkout token; the label audit uses its `GITHUB_TOKEN`. No cross-repository
read secret is currently configured. Private-member access is not implied by
registered membership or a past successful joint-environment receipt.

## Why

Removing the member or claiming these unexecuted checks pass would misstate
coverage. Changing a private repository's visibility is a maintainer decision.
The intentional temporary restriction remains; current access failures stay
visible until their recovery is executed and verified.

## Accepted temporary scope and recovery

Responsible maintainer: LMMV. Review by 2026-10-11. Keep OpenCASTp registered
and private, and track the five audits as pending due to access. This is a
temporary availability limitation, not a successful audit, joint integration
or waiver of admission/release gates.

When public visibility returns, execute and inspect the five affected audits
against a recorded central head, including actual joint source/install/runtime
checks. If privacy lasts longer, explicitly review a narrowly scoped read
credential route. This record creates no credential, changes no visibility,
omits no member and alters no workflow to hide a failure.

## Acceptance criteria

- Preserve the access-failure runs and central/member ownership links.
- Resolve temporary access through the maintainer's chosen route.
- Execute and inspect the five affected audits on a recorded central head.
- Retain failed, skipped or unavailable member checks as such until recovery.

## Local implementation issues

uibcdf/molsyssuite#82 owns joint development evidence;
uibcdf/molsyssuite#39 owns the independent CI review;
uibcdf/opencastp#3 owns the component's CI review. No component source repair
is requested by this central access record.

## Provenance

2026-10-04, Linux; administrative native GitHub metadata/log inspection with
published GH Run Receptor 1.2.0. No private source is copied into this public
record. No scientific suite, credential mutation or visibility change occurs.
