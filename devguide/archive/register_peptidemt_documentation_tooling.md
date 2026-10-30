---
summary: Register the two explicit PeptideMT documentation-tooling dependencies.
issue: uibcdf/molsyssuite#156
status: resolved
opened: 2026-10-29
closed: 2026-10-30
verification: measured
area: [governance, dependencies, documentation]
guard: tests/test_dependency_graph.py
normative: devguide/dependency_graph_policy.md
blocked_by: []
supersedes: []
---

# PeptideMT documentation acquisition receiving

**Reported:** New docs fixture following investigator D37 acceptance, 2026-10-29.
**Status:** Central registration and bounded documentation receiving complete.

## What and why

PeptideMT's documentation environment explicitly installs DepDigest and SMonitor.
The graph already records its runtime/test relationships; those do not replace
direct documentation acquisition. Under the accepted graph policy, register
two additional `documentation-tooling`, `optional=false` edges. Third-party
Sphinx/MyST/theme packages are outside the member graph.

## Source and executed evidence

The owner originally handed off `bb4f5a9beb0519cea47a7751dc2637a3f4f33b1a`;
the final documentation/receipt source is
`b872f32965f50ccec64c46659176ca8c8acf727c`. Its docs environment is byte-identical
to the first source. The workflow adds only checkout `fetch-depth: 0` to recover
the actual development version; it retains the same dependency acquisition.

After initial inspection with the existing published GH Run Receptor 1.0.0
extension, the shared verifier independently binds run **40912249092**, attempt 1,
source, push event, `.github/workflows/docs.yml`, sole build job and every required
executed step. Candidate install, installed-origin/closure checks, strict HTML,
memory-input doctests and preview upload all succeed. The six doctests are an
owner-reported count; their native step execution is independently verified.

Both graph edges cite the exact environment and workflow paths at the final
source. [Receiving receipt](../rollouts/peptidemt_docs_tooling_156_20261030.json)
retains their SHA-256 values and the native job/step identities. The existing
graph module guard protects valid typed relationships and keeps tooling edges
out of the default runtime view; the generated human view is regenerated and
checked. No new test merely duplicates these two inventory rows.

## Scope and acceptance

Existing runtime/test/CI edges, project dependencies, extras and member
classification are unchanged. Central receiving reads committed inputs and
native evidence; it edits no component source, rebuilds no documentation,
downloads no scientific assets, executes no model and deploys no website.
Native preview-upload success is not independent HTML artifact-content validation.
D37 acceptance, predictor qualification and SMonitor #54 remain separately owned
in PeptideMT #6. #151/#152 remain completed with their original evidence.

The central offline guard, affected graph regressions and generated view pass;
final exact-head administrative CI is linked from the issue closeout. The named
Python 3.14.7 workspace retains its twelve pre-existing dependency-closure
findings; these metadata checks do not certify joint scientific compatibility.
