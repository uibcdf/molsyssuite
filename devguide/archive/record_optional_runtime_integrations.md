---
summary: Record reviewed conditional runtime integrations without inventing package extras.
issue: uibcdf/molsyssuite#204
status: resolved
opened: 2026-11-15
closed: 2026-11-15
verification: reproduced
area: [governance, dependency-graph]
guard: tests/test_dependency_graph.py
normative: devguide/dependency_graph_policy.md
blocked_by: []
supersedes: []
---

# Conditional runtime integrations in the typed graph

## What, how and why

BindingMT c09c6f90302e3b726371b1869afa33749235179c supplies a soft DepDigest
TopoMT declaration and actual lazy guarded public-owner calls, with no package
extra or qualified published minimum. The existing `runtime` graph kind correctly
requires package metadata/extras; forcing this relation into it either refuses
or invents an installable requirement. The bounded #195 source receiving requires
an honest source relationship without changing that package contract.

Add `runtime-integration` to the existing graph's bounded kinds. It must remain
optional and carry no named extras. Immutable actual availability/call evidence
establishes relevance by review; incidental imports/prose alone are insufficient.
Default required-runtime queries and strict package manifest/extra audits retain
their exact behavior. Explicit optional kind/all queries and the generated human
view expose the distinction. No parallel registry or graph implementation is added.

## Causal controls and actual receiving

Two new controls fail before the extension because the new kind is unknown;
one invalid-form control already refuses. All sixteen graph cases pass after
repair. The new tests preserve default queries, explicit optional filtering,
readable package-extra/source-route distinctions and refusal of required/fake-extra
integration claims. A real missing package edge still fails manifest comparison.
Historical unknown-kind, package optional-extra drift and source-evidence guards
remain in the same module.

The [source/receiving receipt](../rollouts/native_interface_owner_receiving_195_20261115.json)
records the exact BindingMT→TopoMT edge, unchanged before/after required-runtime
query and successful actual immutable BindingMT static manifest audit. It does
not import any component or claim an installed/public provider pairing. Source
SDK/runtime, native-builder and scientific limits remain the original owners'.

## Boundaries and closure

This is current central inventory/tooling under #30/#195. Historical policy tags,
existing frozen member callers, package extras/dependencies and science do not
change. New shared frozen member engineering/capability vocabulary would require
its own qualified policy snapshot; this central query kind is not a member
capability or an admission overlay. No new package minimum, component release,
scientific campaign, wholesale integration inventory or common-guide rollout is
selected. Preserve primary/human work and the #82 prefix pause.

After focused controls, lint/index/offline governance and exact-source central
native core receiving, archive this finite graph extension. #195 remains partial
for actual consumer acceptance; closing #204 cannot close that larger work.

## Resolution

The representation extension and actual immutable BindingMT integration are
implemented. Three new semantic controls retain two initial failures; all sixteen
graph cases and the complete 157-case graph/governance selection pass with
published Pytest Receptor 1.2.3. Ruff lint/format, generated graph/indexes and
offline governance pass. The causal guard exercises the previously refused query
and generated view, optional filtering and unweakened package-manifest failure.
Exact-source native receiving and the actual task-resource retirement are recorded
in #204 before remote closure. #195 stays partial for actual consumer acceptance.
