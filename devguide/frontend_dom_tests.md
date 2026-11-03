# Optional frontend DOM-test pattern

This reference is available to components with JavaScript panels or scientific
addons. Adoption is optional and owner-reviewed under MolSysSuite #161. The
Python starter supplies a [review worksheet](../devtools/templates/python_component/devguide/frontend_dom_review.md),
without installing Node tools or enabling a frontend workflow. An existing
qualified frontend route can remain in use.

MolSysViewer owns generic widget/comm, lifecycle and rendering contracts. The
scientific component owns its panel states, action meanings and assertions;
molecular operations remain with their molecular provider. A DOM test exercises
the consumer interface without implementing those providers in a test harness.

## Reviewed examples and their qualification

| Example | Actual boundary | Recorded qualification |
| --- | --- | --- |
| [DockingMT addon panels](https://github.com/uibcdf/dockingmt/blob/94f42e152c403353fa4654631f4e0c2b14ddd042/devtools/frontend/README.md) | Node 26 native runner, jsdom 30.1.3, shipped literal `_ESM` modules and a minimal widget-model double. Python 3.14 extracts literals without scientific imports. | Eleven input hashes, two unchanged runtime trees and seven unchanged scientific/publication workflows verified. Local owner reports 21 DOM cases and 78 selected Python cases, including six protocol/module cases. Exact [hosted DOM run](https://github.com/uibcdf/dockingmt/actions/runs/41711369065), attempt 1, has its required setup/install/test steps independently verified. |
| [MolSysViewer frontend units](https://github.com/uibcdf/molsysviewer/blob/15e0459d6d2beb59e11f89f4c4a896109baef706/molsysviewer/js/package.json) | Node 22, esbuild unit bundle, native runner and separately validated c8 source reports. | [Prior bounded coverage receiving](rollouts/viewer_js_source_coverage_69_45_20261103.json) verifies successful JS/report steps and original hosted bytes while the enclosing Python workflow fails. |

These profiles retain their own Node versions, flags, dependencies and scope.
DockingMT uses experimental VM modules and records the warning; this reference
does not establish a universal Node/jsdom baseline. MolSysViewer is comparison
evidence, not a second consumer of the DockingMT DOM harness. There is no shared
DOM executor, composite action or general harness to install from MolSysSuite.

## Adopting the pattern

Record an owning issue, source/artifact identity, commands, actual tool versions,
selected assertions and limits in the component. Use the worksheet when useful.
Keep these controls when adapting the example:

1. **Execute production code.** Import the actual frontend module or extract its
   supported literal source without translating or editing it. Refuse missing,
   ambiguous or unsupported declarations. Do not maintain a second production
   implementation inside tests. Bind extracted bytes to the actual widget/module
   with a meaningful owner-local contract check.
2. **Bind backend examples.** Compare protocol fixtures with real production
   backend states in an existing suitable Python lane. Cover absent values,
   zero versus unknown, identity versus display/rank, units and action meaning.
   A hand-written JSON fixture alone cannot certify backend compatibility.
3. **Keep the double small.** Implement only the used model attributes/events
   and outgoing-message surface. Assert state updates and user actions,
   unsupported/error states, repeated mounting, independent instances and owned
   subscription cleanup. Label the double; it cannot certify the real comm layer.
4. **Isolate test tools.** Commit a private development-only package and lockfile,
   select a reviewed Node/Python profile and use deterministic installation.
   DockingMT's selected route uses `npm ci --ignore-scripts --no-audit --no-fund`.
   A component needing install/build scripts reviews them explicitly. Keep Node
   packages out of scientific runtime requirements and distribution payloads.
5. **Propagate failures.** Run the real test command directly, preserving its
   nonzero status. DOM handler errors must fail tests too. Optional adoption does
   not mean converting a failed executed gate to success. Add the job to the
   owning CI contract with its applicable events; retain PR/full/recovery,
   scientific and publication obligations.
6. **Own resource cleanup.** Close each context/window and run returned cleanup
   callbacks on success and failure, including failed setup where applicable.
   Verify listener/resource isolation and report cleanup errors. Avoid unnecessary
   browser/server/kernel launches. Retain useful failures with their owner,
   purpose and review trigger; follow the [temporary-resource policy](temporary_resources.md).
7. **Record what ran.** Bind Git source, workflow/run/attempt, actual job/steps,
   tool/lock identities and evidence. A configured workflow is not execution;
   local tests do not qualify hosted execution. Use GH Run Receptor first and
   native facts for exact acceptance. Keep test counts, coverage and whole-CI
   outcomes distinct.

Third-party Node/jsdom test tools do not create registered-member graph edges.
Review actual suite-provider relationships through the existing dependency
inventory, and preserve the component's qualified scientific source routes.

## Source and installed identities

The reviewed DockingMT DOM route executes source modules. Its six Python
contract cases compare four generated backend examples and two actual widget
modules. A separate private installed-wheel result does not automatically bind
the source DOM run to that archive.

To claim installed frontend coverage, identify the exact original archive/digest,
install normally in a controlled receiver, and load the installed modules or
verify their bytes against the executed extraction. Refuse source overlays and
editable substitutions; record addon/provider origins and generated-resource
identity. Keep source harnesses separate from production import paths. Actual
installed scientific/platform/public gates retain their owning release contract.

## Illustrative separate workflow

The following uses the reviewed DockingMT Node-26 profile and directory contract.
It becomes executable only after a component supplies and reviews that package,
lockfile and meaningful tests. Adapt paths, tool/action revisions and event scope
to the owner; this is not a generated active workflow or a reusable workflow call.
Its Python tool is for standard-library extraction. Production backend fixture
checks stay in the component's appropriate Python environment/lane.

```yaml
name: Addon DOM
on:
  push:
  pull_request:
  workflow_dispatch:
permissions:
  contents: read
jobs:
  addon-dom:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-python@v6
        with:
          python-version: "3.14"
      - uses: actions/setup-node@v6
        with:
          node-version: "26"
          cache: npm
          cache-dependency-path: devtools/frontend/package-lock.json
      - name: Install locked development-only DOM tools
        working-directory: devtools/frontend
        run: npm ci --ignore-scripts --no-audit --no-fund
      - name: Execute shipped addon JavaScript in the test DOM
        working-directory: devtools/frontend
        run: npm test
```

Use the [immutable consumer workflow](https://github.com/uibcdf/dockingmt/blob/94f42e152c403353fa4654631f4e0c2b14ddd042/.github/workflows/addon-frontend.yml)
for its complete context. Reuse qualified local tooling where it already meets
the assertions. Copying this example does not establish executed adoption.

## Evidence boundaries and future reuse

DOM state, click/change handling and emitted messages can pass without a real
widget comm round trip, browser integration, layout/rendered pixels, camera or
clipping behavior. They do not establish C6, human acceptance, scientific
correctness or public release admission. Retain those existing owner gates and
explicit deferrals. Unit counts do not imply source coverage or a new percentage
threshold. Generated example states do not authorize scientific recalculation.

Extract shared executable infrastructure only when a second concrete consumer
establishes compatible inputs, outputs, module/loading contracts and lifecycle
requirements. Review the actual reusable operation in its owner, retain local
scientific assertions and qualify replacements before removing a working local
route. Merely having JavaScript in two repositories is insufficient.
