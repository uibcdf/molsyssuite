# Component dependency graph

This policy applies to relationships between repositories registered in
`suite.toml`, under uibcdf/molsyssuite#30. The suite owns coordination; component
manifests, scientific contracts and releases retain their local authority.

## Registry and direction

`[dependency-graph]` schema version 1 records direct edges. **Consumer requires
provider** is the edge direction; provider-first processing follows it in reverse.
Each edge names registered member names, one bounded kind, an `optional` boolean
and immutable inspected source evidence (`uibcdf/repo@<full SHA>:relative/path`).
The same consumer/provider may have several distinct kinds; the same typed edge
may not be duplicated. Do not add transitive closure edges merely because a path
exists. Explicit direct requirements remain direct even when a transitive path
also exists. Third-party packages and guide-copy relationships are outside this graph.

| Kind | Meaning and source |
| --- | --- |
| `runtime` | Component package requirement declared in metadata. Required edges match `project.dependencies`; optional runtime edges name the enabling `extras`. |
| `test-tooling` | Dependencies of an actual test/QA environment, extra or workflow bootstrap; they do not widen public runtime requirements. |
| `ci-tooling` | Workflow or operator tools for CI inspection/operation, supported by actual configuration, instructions or recorded operator use. |
| `documentation-tooling` | Registered packages explicitly acquired by a documentation environment or extra. Ordinary prose references are not edges. |

Multiple source references on one edge preserve distinct declarations. Evidence
is an inspected snapshot, not an assertion of installed compatibility, an active
support claim or package availability. A guide's presence alone is not tool use.
The initial inventory includes all 15 members and 14 static Python manifests;
MolSys-AI's umbrella is a governed subsystem without a Python package. Its
unregistered child repositories are not invented as members or runtime edges.

## Queries and coordinated units

Use the offline shared tool:

```bash
python devtools/scripts/dependency_graph.py
python devtools/scripts/dependency_graph.py --cohort python-3.14
python devtools/scripts/dependency_graph.py --cohort stabilization --json
python devtools/scripts/dependency_graph.py --consumer elastnetmt
python devtools/scripts/dependency_graph.py --provider pyunitwizard --json
python devtools/scripts/dependency_graph.py --kind all --include-optional --json
```

Default queries include required runtime edges only. `--kind` is repeatable;
`all` selects all four kinds. Optional runtime edges participate only with
`--include-optional`. Consumer/cohort queries retain prerequisite closure, so
an order never silently omits a required provider. Provider queries include
transitively affected consumers and their prerequisites. Cohorts are registered
initiatives or `python-3.14` (the explicit transition roster); unknown selectors fail.
With no selector all registered members are present, including isolated tools.

JSON schema `molsyssuite.dependencies@1` returns typed edges, strongly connected
components, cycles and provider-first layers. Each layer contains groups, not
an arbitrary linear ordering. A multi-member group is one coordinated unit:
the MolSysMT–MolSysViewer required runtime cycle has no safe internal topological
order. A plan must use the [Conda publication contract](conda_publication_policy.md)
and exact candidate evidence to resolve publication cycles. Graph layers do not
authorize releases, replace bootstrap review or prove scientific correctness.

## Maintenance and conformance

After an affected component changes direct dependencies or development profiles,
update the registry with reviewed immutable source evidence and regenerate
[the human view](component_dependencies.md):

```bash
python devtools/scripts/dependency_graph.py --write
python devtools/scripts/dependency_graph.py --check
python devtools/scripts/dependency_graph.py --workspace /path/to/member-checkouts
```

The global generated view cannot be written with query selectors. Central offline
governance rejects malformed/duplicate/self/unknown edges, invalid evidence,
invalid exceptions and stale generated documentation. A separate read-only
manifest audit checks live static required runtime edges and declared extra
relationships from clean member checkouts, without imports, package installation
or scientific tests. Missing, dynamic or invalid Python manifests fail that audit.
Member metadata is authoritative for actual package dependencies; discrepancies
require correcting the registry or reporting the component defect to its owner.
Tooling role and instruction relevance remain reviewed facts, not automatic
inferences from a package name in arbitrary prose.

## Exceptions and conditional relationships

Named optional extras describe conditional runtime dependencies without making
them unconditional. A package with dynamic metadata or another manifest format
needs a reviewed local profile or a bounded `[[dependency-manifest-exceptions]]`
entry: `repository`, owning `issue`, `owner`, `reason`, `removal-condition`, ISO
`expires-on`. The suite validator uses the existing owned-exception validator;
unknown/duplicate members, foreign issue owners, missing fields or expiry fail.
An exception skips that member's static comparison only; it does not remove its
edges, suppress graph validation or certify compatibility. Record the measured
source and next action in the owning issue. Non-Python governed subsystems have
no Python-manifest obligation; new actual relationships still require typed edges.
