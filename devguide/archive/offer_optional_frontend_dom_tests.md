---
summary: Offer an optional production-bound DOM-test reference and starter worksheet.
issue: uibcdf/molsyssuite#161
status: resolved
opened: 2026-11-03
closed: 2026-11-03
verification: inspected
area: [tooling, frontend, governance]
guard:
normative: devguide/frontend_dom_tests.md
blocked_by: []
supersedes: []
---

# Optional frontend DOM-test reference

**Reported:** DockingMT #60 supplied its first concrete addon DOM-test route.
**Status:** Resolved for the optional central reference/catalogue/starter scope.
Component implementation and actual comm/browser/scientific/release gates retain
their owners. A shared executable harness is outside this completed scope.

## What

Make a reviewed frontend-test pattern discoverable to scientific addons without
copying their scientific assertions or imposing a Node library/version on every
member. The principal maintainer accepted proceeding with this optional reference.

## How

`devguide/frontend_dom_tests.md` documents the production-code loading, protocol
fixture drift, small model-double, locked development tools, failing status and
context-cleanup controls. It includes an illustrative workflow whose steps match
the actual qualified DockingMT profile. Source and installed identity, test/coverage
outcomes and real comm/browser/pixels/C6 remain explicit separate claims.

The shared catalogue and starter guide link the reference. Every newly generated
Python starter has an unqueued `devguide/frontend_dom_review.md` worksheet linked
from its README. No frontend boundary means no adoption work. Generation creates
no Node package, lockfile or active frontend workflow. The unchanged common guide
already routes contributors to the shared catalogue; no guide synchronization,
policy release or consumer workflow/pin migration is needed.

## Why

DockingMT's Python scientific jobs did not execute panel JavaScript. Its local
route demonstrates meaningful production-panel assertions. A common reference
helps future addons receive that boundary while preserving MolSysViewer's generic
widget/comm/lifecycle/rendering ownership and molecular-provider responsibilities.

## What is measured and what is assumed

- DockingMT `94f42e152c403353fa4654631f4e0c2b14ddd042`: all eleven reported
  input hashes match; both runtime trees and seven scientific/publication workflows
  match its previous checkpoint. Private development package/lock agree on jsdom
  30.1.3 and Node-26 profile. The experimental VM-module warning is retained.
- The owner reports 21 DOM and 78 selected Python cases, including four backend
  example and two actual widget-module identity cases. They were not rerun centrally.
- GHR first inspection and independent native verification accept run 41711369065,
  attempt 1, exact source/workflow/push, sole job 126179984377 and actual setup,
  locked installation and test-command steps. A separate hosted TAP count is not
  claimed. Other scientific/full-matrix workflows are not certified by this job.
- MolSysViewer `15e0459d6d2beb59e11f89f4c4a896109baef706` supplies a contrasting
  Node-22/esbuild/native-runner route, with prior bounded JS source-coverage evidence.
  This is not a second consumer of the DockingMT DOM harness.
- Actual disposable starter generation resolves the repository token and local
  README worksheet link, preserves the two default Python workflows and generates
  no npm package/lock. The documented workflow parses and its steps equal the
  qualified consumer's steps. This is generation/reference validation, not a new
  component admission or frontend execution.

## Alternatives and refuted paths

| Choice | Outcome |
| --- | --- |
| Optional documented pattern and generated worksheet | Accepted: useful now, preserving owner profiles and actual claims. |
| Shared mandatory Node/jsdom version or frontend gate | Rejected for this scope: requirements and frontend boundaries differ. |
| Extract a generic harness/action from one consumer | Deferred until a second concrete caller establishes compatible contracts. |
| Treat DOM success as real comm/rendering/scientific acceptance | Rejected: those boundaries are not executed by the model double. |

## Scope and exclusions

Central reference, catalogue and future starter worksheet only. No scientific
implementation, component code/guide/caller change, dependency graph edge, package
build or upload, fresh browser/installed qualification, every-push full suite or
environment switch is introduced. Existing local tools can remain qualified.

## Acceptance criteria

- [x] Inspect immutable consumer evidence and contrast existing Viewer tooling.
- [x] Publish an optional reference with code/fixture identity, cleanup and clear limits.
- [x] Make it discoverable from catalogue/starter and generate its worksheet.
- [x] Exercise real starter generation and preserve normal Python-only outputs.
- [x] Keep ownership, notices and exact local/native evidence in a durable receipt.

## Local implementation issues

DockingMT #60 owns its actual DOM route and browser receiving; #50 owns useful
retained resources, reviewed 2026-11-10. #30/#47 retain public distribution.
No migration issue is commissioned in other components. A future general harness
requires its own concrete provider/consumer proposal.

## Dependencies and risks

A copied workflow can pass against stale fixtures or test-only reimplementations;
the reference requires meaningful owner checks before adoption claims. Different
tool versions and source/installed module loading need their own qualification.
The pattern's availability does not assert that every addon has adopted it.

## Provenance

Named Python 3.14.7 administrative checks, read-only exact Git objects, existing
qualified GHR and native Actions evidence. Advance notices precede publication in
central #161 and DockingMT #60. [Review/generation/native receipt](../rollouts/frontend_dom_pattern_161_20261103.json).
Thirty-nine existing instruction/modular-tool/CI/starter-policy tests pass with
Pytest Receptor. Actual generation/example checks, generated indexes, offline
governance, central Conda administrative controls and whitespace checks pass.
The normative optional reference guards closure; no universal enforcement is added.
