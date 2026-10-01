"""Query typed suite dependencies and generate their maintained human view."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import tomllib

try:
    from devtools.scripts import agent_instructions
    from devtools.scripts.check_repository import _required_sibling_dependencies
except ImportError:
    import agent_instructions
    from check_repository import _required_sibling_dependencies

ROOT = Path(__file__).resolve().parents[2]
VIEW = ROOT / "devguide/component_dependencies.md"
KINDS = {"runtime", "test-tooling", "ci-tooling", "documentation-tooling"}


def validate(policy: dict) -> list[str]:
    graph = policy.get("dependency-graph", {})
    errors: list[str] = []
    if graph.get("schema-version") != 1:
        errors.append("dependency graph requires schema-version 1")
    if not isinstance(graph.get("edges"), list):
        return errors + ["dependency graph edges must be a list"]
    names = {m["name"] for m in policy["members"]}
    seen: set[tuple] = set()
    for edge in graph.get("edges", []):
        if (
            not isinstance(edge, dict)
            or set(edge)
            - {"consumer", "provider", "kind", "optional", "evidence", "extras"}
            or not all(
                isinstance(edge.get(k), str) for k in ("consumer", "provider", "kind")
            )
        ):
            errors.append("dependency edge has invalid fields or endpoint types")
            continue
        key = (edge.get("consumer"), edge.get("provider"), edge.get("kind"))
        if key in seen:
            errors.append(f"duplicate dependency edge: {key}")
        seen.add(key)
        if key[0] not in names or key[1] not in names:
            errors.append(f"unknown dependency endpoint: {key}")
        if key[0] == key[1]:
            errors.append(f"self dependency edge: {key}")
        if key[2] not in KINDS:
            errors.append(f"unknown dependency kind: {key}")
        if not isinstance(edge.get("optional"), bool):
            errors.append(f"dependency optional must be boolean: {key}")
        evidence = edge.get("evidence", [])
        if (
            not isinstance(evidence, list)
            or not evidence
            or not all(
                isinstance(e, str)
                and re.fullmatch(
                    r"uibcdf/[A-Za-z0-9_.-]+@[0-9a-f]{40}:[A-Za-z0-9_./-]+", e
                )
                and ".." not in e.split(":", 1)[1].split("/")
                for e in evidence
            )
        ):
            errors.append(f"dependency needs immutable source evidence: {key}")
        extras = edge.get("extras", [])
        if (
            not isinstance(extras, list)
            or len(extras) != len(set(extras))
            or not all(isinstance(e, str) and e for e in extras)
        ):
            errors.append(f"dependency extras must be unique names: {key}")
        if key[2] == "runtime" and edge.get("optional") and not extras:
            errors.append(f"optional runtime edge requires named extras: {key}")
    exceptions = dict(
        policy,
        **{
            "working-instruction-exceptions": policy.get(
                "dependency-manifest-exceptions", []
            )
        },
    )
    errors.extend(
        error.replace("working instruction exception", "dependency manifest exception")
        for error in agent_instructions.validate_exceptions(exceptions)
    )
    return errors


def _closure(nodes: set[str], adjacency: dict[str, set[str]]) -> set[str]:
    result = set(nodes)
    pending = list(nodes)
    while pending:
        for target in adjacency[pending.pop()]:
            if target not in result:
                result.add(target)
                pending.append(target)
    return result


def strongly_connected(adjacency: dict[str, set[str]]) -> list[list[str]]:
    """Return deterministic Tarjan components; cycles remain single ordered units."""
    indices: dict[str, int] = {}
    low: dict[str, int] = {}
    stack: list[str] = []
    active: set[str] = set()
    groups: list[list[str]] = []

    def visit(node: str) -> None:
        indices[node] = low[node] = len(indices)
        stack.append(node)
        active.add(node)
        for target in sorted(adjacency[node]):
            if target not in indices:
                visit(target)
                low[node] = min(low[node], low[target])
            elif target in active:
                low[node] = min(low[node], indices[target])
        if low[node] == indices[node]:
            group: list[str] = []
            while True:
                target = stack.pop()
                active.remove(target)
                group.append(target)
                if target == node:
                    break
            groups.append(sorted(group))

    for node in sorted(adjacency):
        if node not in indices:
            visit(node)
    return sorted(groups)


def query(
    policy: dict,
    *,
    kinds: set[str] | None = None,
    include_optional: bool = False,
    consumers: list[str] | None = None,
    providers: list[str] | None = None,
    cohort: str | None = None,
) -> dict:
    errors = validate(policy)
    if errors:
        raise ValueError("; ".join(errors))
    kinds = {"runtime"} if kinds is None else kinds
    if not kinds or not kinds <= KINDS:
        raise ValueError("unknown or empty dependency kind selection")
    names = {m["name"] for m in policy["members"]}
    edges = [
        e
        for e in policy["dependency-graph"]["edges"]
        if e["kind"] in kinds and (include_optional or not e["optional"])
    ]
    adjacency = {n: set() for n in names}
    reverse = {n: set() for n in names}
    for e in edges:
        adjacency[e["consumer"]].add(e["provider"])
        reverse[e["provider"]].add(e["consumer"])
    seeds = set(consumers or []) | set(providers or [])
    if not seeds <= names:
        raise ValueError("unknown member selector: " + ", ".join(sorted(seeds - names)))
    if cohort:
        if cohort == "python-3.14":
            seeds.update(
                c["name"]
                for c in policy["policies"]["python"]["transition"]["components"]
            )
        elif cohort in policy.get("initiatives", {}):
            seeds.update(policy["initiatives"][cohort]["priority-members"])
        else:
            raise ValueError("unknown cohort: " + cohort)
    if providers:
        seeds.update(_closure(set(providers), reverse))
    selected = _closure(seeds, adjacency) if seeds else names
    adjacency = {n: adjacency[n] & selected for n in selected}
    edges = sorted(
        [e for e in edges if e["consumer"] in selected and e["provider"] in selected],
        key=lambda e: (e["consumer"], e["kind"], e["provider"]),
    )
    groups = strongly_connected(adjacency)
    group_by_node = {n: i for i, g in enumerate(groups) for n in g}
    dependencies = {
        i: {group_by_node[p] for n in g for p in adjacency[n]} - {i}
        for i, g in enumerate(groups)
    }
    layers: list[list[list[str]]] = []
    remaining = set(dependencies)
    while remaining:
        ready = sorted(i for i in remaining if not dependencies[i] & remaining)
        if not ready:
            raise ValueError("invalid strongly connected condensation")
        layers.append([groups[i] for i in ready])
        remaining.difference_update(ready)
    return {
        "schema": "molsyssuite.dependencies@1",
        "direction": "consumer-to-provider",
        "kinds": sorted(kinds),
        "include_optional": include_optional,
        "members": sorted(selected),
        "edges": edges,
        "components": groups,
        "cycles": [g for g in groups if len(g) > 1],
        "layers": layers,
    }


def manifest_findings(
    policy: dict, workspace: Path, selected: list[str] | None = None
) -> list[str]:
    """Compare declared required and optional runtime relationships, without imports."""
    errors = validate(policy)
    if errors:
        return errors
    names = {m["name"] for m in policy["members"]}
    if selected and not set(selected) <= names:
        return ["unknown manifest member selector"]
    edges = policy["dependency-graph"]["edges"]
    for member in policy["members"]:
        if selected and member["name"] not in selected:
            continue
        if "python-package" not in member["capabilities"]:
            continue
        name, repository = member["name"], member["repository"]
        if any(
            e.get("repository") == repository
            for e in policy.get("dependency-manifest-exceptions", [])
        ):
            continue
        manifest = workspace / name / "pyproject.toml"
        if not manifest.is_file():
            errors.append(
                f"{repository}: missing static manifest; record an owned exception"
            )
            continue
        try:
            project = tomllib.loads(manifest.read_text())
        except (OSError, tomllib.TOMLDecodeError) as error:
            errors.append(f"{repository}: invalid manifest: {error}")
            continue
        if "dependencies" in project.get("project", {}).get("dynamic", []):
            errors.append(
                f"{repository}: dynamic dependencies require an explicit owned profile"
            )
            continue
        declared = set(_required_sibling_dependencies(project, policy, repository))
        recorded = {
            e["provider"]
            for e in edges
            if e["consumer"] == name and e["kind"] == "runtime" and not e["optional"]
        }
        if declared != recorded:
            errors.append(
                f"{repository}: required runtime mismatch; missing={sorted(declared - recorded)}, extra={sorted(recorded - declared)}"
            )
        extras = project.get("project", {}).get("optional-dependencies", {})
        for extra, requirements in extras.items():
            declared_extra = _required_sibling_dependencies(
                {"project": {"dependencies": requirements}}, policy, repository
            )
            for provider in declared_extra:
                if not any(
                    e["consumer"] == name
                    and e["provider"] == provider
                    and extra in e.get("extras", [])
                    for e in edges
                ):
                    errors.append(
                        f"{repository}: unrecorded extra relationship {extra}: {provider}"
                    )
        for edge in edges:
            if (
                edge["consumer"] != name
                or edge["kind"] != "runtime"
                or not edge["optional"]
            ):
                continue
            for extra in edge["extras"]:
                candidate = {"project": {"dependencies": extras.get(extra, [])}}
                if edge["provider"] not in _required_sibling_dependencies(
                    candidate, policy, repository
                ):
                    errors.append(
                        f"{repository}: optional runtime {edge['provider']} absent from extra {extra}"
                    )
    return errors


def view_findings(policy: dict, target: Path = VIEW) -> list[str]:
    if not target.is_file() or target.read_text() != render(policy):
        return ["generated component dependency graph is stale"]
    return []


def render(policy: dict) -> str:
    data = query(policy)
    full = query(policy, kinds=KINDS, include_optional=True)
    text = "# MolSysSuite component dependencies\n\nGenerated from `suite.toml`; edit the registry and run\n`python devtools/scripts/dependency_graph.py --write`. Check with `--check`.\nSee [the dependency graph policy](dependency_graph_policy.md) for scope, evidence,\nselectors and exception profiles. Arrows mean **consumer requires provider**.\nThis inventory is inspected source, not installed compatibility certification.\n\n## Required runtime graph\n\n```mermaid\nflowchart TD\n"
    ids = {n: "n" + str(i) for i, n in enumerate(data["members"])}
    for n in data["members"]:
        text += f'  {ids[n]}["{n}"]\n'
    for e in data["edges"]:
        text += f"  {ids[e['consumer']]} --> {ids[e['provider']]}\n"
    text += "```\n\n## Provider-first layers\n\nA bracketed group is one strongly connected unit; its members have no safe\ninternal topological order. Layers do not authorize releases or replace #27.\n\n| Layer | Components / coordinated units |\n| --- | --- |\n"
    for i, layer in enumerate(data["layers"], 1):
        text += (
            f"| {i} | "
            + "; ".join("[" + ", ".join(g) + "]" if len(g) > 1 else g[0] for g in layer)
            + " |\n"
        )
    text += (
        "\nRuntime cycles: "
        + ("; ".join(", ".join(g) for g in data["cycles"]) or "none")
        + ".\n\n## All typed direct relationships\n\n| Consumer | Kind | Providers |\n| --- | --- | --- |\n"
    )
    grouped: dict[tuple, list[str]] = {}
    for e in full["edges"]:
        suffix = (
            " (optional: " + ", ".join(e["extras"]) + ")"
            if e["optional"] and e["kind"] == "runtime"
            else ""
        )
        grouped.setdefault((e["consumer"], e["kind"]), []).append(
            e["provider"] + suffix
        )
    for (consumer, kind), providers in sorted(grouped.items()):
        text += f"| {consumer} | {kind} | " + ", ".join(providers) + " |\n"
    text += "\nOnly observed direct relationships are recorded. In particular, a synchronized\nguide copy, optional import or platform architecture reference does not create a\npackage dependency. MolSys-AI is a governed subsystem without a Python manifest;\nits child implementation repositories are outside this registered-member graph.\n"
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kind", action="append", choices=sorted(KINDS | {"all"}))
    parser.add_argument("--include-optional", action="store_true")
    parser.add_argument("--consumer", action="append")
    parser.add_argument("--provider", action="append")
    parser.add_argument("--cohort")
    parser.add_argument("--json", action="store_true")
    view = parser.add_mutually_exclusive_group()
    view.add_argument("--write", action="store_true")
    view.add_argument("--check", action="store_true")
    parser.add_argument(
        "--workspace",
        type=Path,
        help="audit current member manifests without imports or network",
    )
    parser.add_argument(
        "--manifest-member",
        action="append",
        help="limit the manifest audit to a registered member",
    )
    args = parser.parse_args()
    policy = tomllib.loads((ROOT / "suite.toml").read_text())
    try:
        if (args.write or args.check) and (
            args.kind
            or args.consumer
            or args.provider
            or args.cohort
            or args.include_optional
        ):
            raise ValueError(
                "the generated view is global; use selectors only for queries"
            )
        if args.workspace:
            findings = manifest_findings(policy, args.workspace, args.manifest_member)
            if findings:
                raise ValueError("\n".join(findings))
        elif args.manifest_member:
            raise ValueError("--manifest-member requires --workspace")
        if args.write or args.check:
            expected = render(policy)
            if args.write:
                VIEW.write_text(expected)
            elif not VIEW.is_file() or VIEW.read_text() != expected:
                raise ValueError("generated dependency view is stale")
            print("Generated dependency view is current.")
        else:
            kinds = (
                KINDS
                if args.kind and "all" in args.kind
                else set(args.kind or ["runtime"])
            )
            data = query(
                policy,
                kinds=kinds,
                include_optional=args.include_optional,
                consumers=args.consumer,
                providers=args.provider,
                cohort=args.cohort,
            )
            if args.json:
                print(json.dumps(data, indent=2))
            else:
                for i, layer in enumerate(data["layers"], 1):
                    print(
                        f"{i}: "
                        + "; ".join(
                            "[" + ", ".join(g) + "]" if len(g) > 1 else g[0]
                            for g in layer
                        )
                    )
    except (ValueError, KeyError, OSError) as error:
        print(error)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
