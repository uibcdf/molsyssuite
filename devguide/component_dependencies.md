# MolSysSuite component dependencies

Generated from `suite.toml`; edit the registry and run
`python devtools/scripts/dependency_graph.py --write`. Check with `--check`.
See [the dependency graph policy](dependency_graph_policy.md) for scope, evidence,
selectors and exception profiles. Arrows mean **consumer requires provider**.
This inventory is inspected source, not installed compatibility certification.

## Required runtime graph

```mermaid
flowchart TD
  n0["ackredit"]
  n1["argdigest"]
  n2["depdigest"]
  n3["dockingmt"]
  n4["elastnetmt"]
  n5["gh-run-receptor"]
  n6["lindelint"]
  n7["molsys-ai"]
  n8["molsysmt"]
  n9["molsysviewer"]
  n10["opencastp"]
  n11["pharmacophoremt"]
  n12["pytest-receptor"]
  n13["pyunitwizard"]
  n14["smonitor"]
  n15["topomt"]
  n0 --> n1
  n0 --> n2
  n0 --> n14
  n1 --> n2
  n1 --> n14
  n2 --> n14
  n3 --> n1
  n3 --> n2
  n3 --> n8
  n3 --> n13
  n3 --> n14
  n4 --> n1
  n4 --> n2
  n4 --> n6
  n4 --> n8
  n4 --> n13
  n4 --> n14
  n6 --> n1
  n6 --> n2
  n6 --> n13
  n6 --> n14
  n8 --> n1
  n8 --> n2
  n8 --> n9
  n8 --> n13
  n8 --> n14
  n9 --> n1
  n9 --> n2
  n9 --> n8
  n9 --> n13
  n9 --> n14
  n10 --> n13
  n11 --> n1
  n11 --> n8
  n11 --> n13
  n13 --> n1
  n13 --> n2
  n13 --> n14
  n15 --> n1
  n15 --> n2
  n15 --> n8
  n15 --> n13
  n15 --> n14
```

## Provider-first layers

A bracketed group is one strongly connected unit; its members have no safe
internal topological order. Layers do not authorize releases or replace #27.

| Layer | Components / coordinated units |
| --- | --- |
| 1 | gh-run-receptor; molsys-ai; pytest-receptor; smonitor |
| 2 | depdigest |
| 3 | argdigest |
| 4 | ackredit; pyunitwizard |
| 5 | lindelint; [molsysmt, molsysviewer]; opencastp |
| 6 | dockingmt; elastnetmt; pharmacophoremt; topomt |

Runtime cycles: molsysmt, molsysviewer.

## All typed direct relationships

| Consumer | Kind | Providers |
| --- | --- | --- |
| ackredit | ci-tooling | gh-run-receptor |
| ackredit | documentation-tooling | argdigest, depdigest, smonitor |
| ackredit | runtime | argdigest, depdigest, smonitor |
| ackredit | test-tooling | argdigest, depdigest, pytest-receptor, smonitor |
| argdigest | ci-tooling | gh-run-receptor |
| argdigest | documentation-tooling | depdigest, smonitor |
| argdigest | runtime | depdigest, pyunitwizard (optional: all, pyunitwizard), smonitor |
| argdigest | test-tooling | depdigest, pytest-receptor, pyunitwizard, smonitor |
| depdigest | ci-tooling | gh-run-receptor |
| depdigest | documentation-tooling | smonitor |
| depdigest | runtime | smonitor |
| depdigest | test-tooling | pytest-receptor, smonitor |
| dockingmt | ci-tooling | gh-run-receptor |
| dockingmt | runtime | argdigest, depdigest, molsysmt, molsysviewer (optional: viewer), pyunitwizard, smonitor |
| dockingmt | test-tooling | depdigest, pytest-receptor, pyunitwizard, smonitor |
| elastnetmt | ci-tooling | gh-run-receptor |
| elastnetmt | documentation-tooling | lindelint, molsysmt, pyunitwizard |
| elastnetmt | runtime | argdigest, depdigest, lindelint, molsysmt, pyunitwizard, smonitor |
| elastnetmt | test-tooling | molsysmt, pytest-receptor, pyunitwizard |
| gh-run-receptor | test-tooling | pytest-receptor |
| lindelint | ci-tooling | gh-run-receptor |
| lindelint | documentation-tooling | argdigest, depdigest, pyunitwizard, smonitor |
| lindelint | runtime | argdigest, depdigest, pyunitwizard, smonitor |
| lindelint | test-tooling | argdigest, depdigest, pyunitwizard, smonitor |
| molsysmt | ci-tooling | gh-run-receptor |
| molsysmt | documentation-tooling | argdigest, depdigest, pyunitwizard, smonitor |
| molsysmt | runtime | argdigest, depdigest, molsysviewer, pyunitwizard, smonitor |
| molsysmt | test-tooling | pytest-receptor |
| molsysviewer | ci-tooling | gh-run-receptor |
| molsysviewer | documentation-tooling | argdigest, depdigest, molsysmt, pyunitwizard, smonitor |
| molsysviewer | runtime | argdigest, depdigest, molsysmt, pyunitwizard, smonitor |
| molsysviewer | test-tooling | argdigest, depdigest, molsysmt, pytest-receptor, pyunitwizard, smonitor |
| opencastp | ci-tooling | gh-run-receptor |
| opencastp | runtime | pyunitwizard |
| opencastp | test-tooling | pytest-receptor, pyunitwizard |
| pharmacophoremt | ci-tooling | gh-run-receptor |
| pharmacophoremt | documentation-tooling | molsysmt, pyunitwizard |
| pharmacophoremt | runtime | argdigest, molsysmt, pyunitwizard |
| pharmacophoremt | test-tooling | molsysmt, pytest-receptor, pyunitwizard |
| pytest-receptor | ci-tooling | gh-run-receptor |
| pyunitwizard | ci-tooling | gh-run-receptor |
| pyunitwizard | documentation-tooling | depdigest, smonitor |
| pyunitwizard | runtime | argdigest, depdigest, smonitor |
| pyunitwizard | test-tooling | argdigest, depdigest, pytest-receptor, smonitor |
| smonitor | ci-tooling | gh-run-receptor |
| smonitor | test-tooling | pytest-receptor |
| topomt | ci-tooling | gh-run-receptor |
| topomt | documentation-tooling | argdigest, depdigest, molsysmt, pyunitwizard, smonitor |
| topomt | runtime | argdigest, depdigest, molsysmt, molsysviewer (optional: viewer), pyunitwizard, smonitor |
| topomt | test-tooling | argdigest, depdigest, molsysmt, pytest-receptor, pyunitwizard, smonitor |

Only observed direct relationships are recorded. In particular, a synchronized
guide copy, optional import or platform architecture reference does not create a
package dependency. MolSys-AI is a governed subsystem without a Python manifest;
its child implementation repositories are outside this registered-member graph.
