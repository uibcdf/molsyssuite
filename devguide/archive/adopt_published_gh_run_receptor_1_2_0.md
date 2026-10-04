---
summary: Qualify published GH Run Receptor 1.2.0 and verify existing registered guide adoption.
issue: uibcdf/molsyssuite#75
status: resolved
opened: 2026-10-02
closed: 2026-10-04
verification: measured
area: [tooling, governance, compatibility]
guard:
normative: devguide/gh_run_receptor_policy.md
blocked_by: []
supersedes: []
---

# Published GH Run Receptor 1.2.0 adoption review

## What and why

The provider release notice uibcdf/molsyssuite#75 requested central review of
published 1.2.0, canonical guide synchronization, appropriate caller pins and
observed-version evidence. It also delivers uibcdf/gh-run-receptor#46's timeout
assessment, removing the provider prerequisite for the separate #25 decision.

## How and outcome — 2026-10-04

Immutable release source: `c3df5ad87f7bab95c53be3f7b0b3007f59d7abf3`.
The exact public wheel was downloaded and SHA-256 checked before independent
installation on Python 3.14.7. Version 1.2.0, dependency closure and site-packages
import origin pass. Nine installed v1 schema bytes equal their original frozen
resources; no new serialized schema or compatibility version was introduced.

All fourteen registered canonical guide consumers already have the byte-identical
published 1.2.0 copy. The official synchronization checker confirms them current.
Twelve existing configurations pass the published parser. Ackredit and OpenCASTp
have no repository configuration, so their configured dogfooding readiness is
not inferred. CLI default/generic use, canonical-guide delivery and configured
readiness are distinct; no unused configuration or new consumer gate was added.
No applicable workflow/action pin requiring migration was identified in this
review; this is not an upgrade of every consumer's installed/runtime tool.

Eight existing member run inspections retain their source conclusions through
the installed public wheel. The historical original cancellation fixture,
extracted from the immutable release source, replays with exit 2, native
cancellation and `termination.cause=unknown`; its limit hint remains diagnostic.
The workspace command's separate `1.1.1+22.gc1e2557` development revision was
preserved and explicitly distinguished from the isolated published wheel.
The preliminary #39 inspection provenance is corrected transparently and all
its native outcomes are independently rechecked with public 1.2.0.

Receipt and source/consumer identities:
`devguide/rollouts/gh_run_receptor_1_2_0_75.json`.
Maintained integration inventory: `devguide/rollouts/gh_run_receptor_dogfooding.md`.

## Scope, guard and remaining ownership

The normative controlled-dogfooding policy protects this resolution's boundary:
ready, active and graduated claims are separate; source GitHub conclusions and
native fallback remain authoritative; read-only supplementary use does not
approve a release by itself. The member ecosystem policy requires a published
reader without silently raising a universal minimum or granting sole approval
power. Direct replay, frozen-byte checks and parser checks qualify the actual
public installed tool, not a mock or scientific matrix.

No source/suite dispatch, component scientific test, package upload, producer
contract, Action admission, stronger authority or core scientific migration was
performed. Future operation instrumentation stays in #25 and is explicitly
deferred by the maintainer; the provider's published assessment is complete.
The owning release notice can close without claiming universal runtime pin
migration or creating unrelated configuration work.
