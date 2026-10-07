"""Explicit source/Conda contexts for the optional dependency-routes@3 contract."""

from __future__ import annotations

import hashlib
import re

from packaging.requirements import Requirement
from packaging.utils import canonicalize_name
from packaging.version import Version

from devtools.scripts import dependency_constraints as contracts
from devtools.scripts import source_provenance as provenance
from devtools.scripts.noarch_conda import ContractError, local_path

SCHEMA = "molsyssuite.dependency-routes@3"


def reason(record: dict) -> None:
    if not isinstance(record.get("reason"), str) or not record["reason"].strip():
        raise ContractError("source/context needs an explicit review reason")


def unique(values: list, description: str) -> list:
    if (
        not isinstance(values, list)
        or any(not isinstance(v, str) for v in values)
        or len(values) != len(set(values))
    ):
        raise ContractError(f"duplicate/invalid {description}")
    return values


def describe(root, inventory, requirements) -> tuple[dict, dict, list]:
    """Validate all declarations independently of the current installed context."""
    sources, contexts, inputs = {}, {}, {}
    for record in inventory.get("source_routes", []):
        reason(record)
        identity, name = record.get("id"), canonicalize_name(record["name"])
        if (
            not isinstance(identity, str)
            or not re.fullmatch(r"[A-Za-z0-9_.-]+", identity)
            or identity in sources
        ):
            raise ContractError("duplicate/invalid source id")
        if record.get("install") not in {"pip-no-deps-git", "pip-no-deps-directory"}:
            raise ContractError("@3 source needs an explicit Git/directory profile")
        if record["install"] == "pip-no-deps-directory" and "input" in record:
            raise ContractError("directory source cannot claim a Git input manifest")
        role = "required-runtime" if name in requirements else "integration"
        if record.get("role") != role:
            raise ContractError(
                "source role differs from required/integration metadata"
            )
        sources[identity] = {
            **record,
            "name": name,
            "url": provenance.repository_url(record["url"]),
            "commit": provenance.full_commit(record["commit"]),
        }
    for record in inventory.get("source_inputs", []):
        reason(record)
        path = record["path"]
        if path in inputs:
            raise ContractError("duplicate source input")
        data = local_path(root, path).read_bytes()
        if hashlib.sha256(data).hexdigest() != record.get("sha256"):
            raise ContractError(f"{path}: reviewed source input changed")
        lines = [
            line.strip()
            for line in data.decode().splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]
        observed = [provenance.parse_git_requirement(line) for line in lines]
        selected = [s for s in sources.values() if s.get("input") == path]

        def matches(item, source):
            return (
                item["repository"] == source["url"]
                and item["commit"] == source["commit"]
                and item["name"] in {None, source["name"]}
            )

        if (
            not observed
            or len(observed) != len(selected)
            or any(sum(matches(item, s) for s in selected) != 1 for item in observed)
            or any(sum(matches(item, s) for item in observed) != 1 for s in selected)
        ):
            raise ContractError(f"{path}: source manifest and inventory differ")
        inputs[path] = record
    if any(s.get("input") and s["input"] not in inputs for s in sources.values()):
        raise ContractError("source references an unreviewed input")
    used = set()
    for record in inventory.get("contexts", []):
        reason(record)
        identity = record.get("name")
        if (
            not isinstance(identity, str)
            or not re.fullmatch(r"[A-Za-z0-9_.-]+", identity)
            or identity in contexts
        ):
            raise ContractError("duplicate/invalid context name")
        minor = record.get("python_minor", "")
        if not re.fullmatch(r"\d+\.\d+", minor):
            raise ContractError("context needs a complete Python minor")
        selected = unique(record.get("sources", []), "context sources")
        if not set(selected) <= set(sources):
            raise ContractError("context names an unreviewed source")
        names = [sources[s]["name"] for s in selected]
        if len(set(names)) != len(names):
            raise ContractError("context selects two revisions of one provider")
        overlays = unique(record.get("overlays", []), "context overlays")
        if any(canonicalize_name(n) != n for n in overlays) or not set(overlays) <= set(
            names
        ):
            raise ContractError("context names an unreviewed overlay")
        if overlays and not record.get("overlay_reason", "").strip():
            raise ContractError(
                "source overlays need their bootstrap/final review reason"
            )
        contexts[identity] = record
        used.update(selected)
    runtime = {
        e["path"] for e in inventory.get("environments", []) if e["kind"] == "runtime"
    }
    if not contexts or {c.get("environment") for c in contexts.values()} != runtime:
        raise ContractError("contexts must cover exactly all runtime environments")
    if used != set(sources):
        raise ContractError("source inventory includes unused providers")
    if not sources and not inventory.get("source_reason", "").strip():
        raise ContractError("absence of sources needs a review reason")
    return sources, contexts, list(inputs.values())


def audit_environment(
    environment, content, items, contexts, sources, requirements, python, aliases
) -> list:
    """Keep declared bootstrap selectors and selected final providers separate."""
    if "source_supplied" in environment:
        raise ContractError("@3 source selection belongs to contexts")
    additional = unique(
        environment.get("additional_channels", []), "additional channels"
    )
    if any(
        not re.fullmatch(r"[A-Za-z0-9_-]+", channel)
        or channel in {"uibcdf", "conda-forge", "nodefaults"}
        for channel in additional
    ):
        raise ContractError("additional channels need literal reviewed names")
    if additional and not environment.get("channel_reason", "").strip():
        raise ContractError("additional channels need an explicit review reason")
    channels = ["uibcdf", "conda-forge", *additional]
    if (
        content.get("channels") not in [channels, [*channels, "nodefaults"]]
        or environment.get("channel_priority") != "strict"
    ):
        raise ContractError("runtime channels/strict priority differ from the review")
    purpose = environment.get("purpose")
    if purpose not in {
        "production",
        "development",
        "test",
        "documentation",
        "optional-runtime",
    }:
        raise ContractError("runtime route needs its general purpose")
    installed_names = {canonicalize_name(i.requirement.name) for i in items}
    results = []
    for identity, context in contexts.items():
        if context["environment"] != environment["path"]:
            continue
        minor = context["python_minor"]
        # Existing whole-minor validation remains the common authority.
        contracts.narrow_python(str(Requirement(python).specifier), minor)
        if not any(
            canonicalize_name(i.requirement.name) == "python"
            and i.requirement.specifier.contains(Version(minor), prereleases=True)
            for i in items
        ):
            raise ContractError(f"{identity}: selected Python differs from environment")
        python_item = next(
            i for i in items if canonicalize_name(i.requirement.name) == "python"
        )
        contracts.compare_requirements(
            [
                contracts.RouteRequirement(
                    Requirement(
                        contracts.narrow_python(
                            str(Requirement(python).specifier), minor
                        )[1]
                    ),
                    minor,
                )
            ],
            [str(python_item.requirement)],
            allow_narrowing=True,
            narrowing_reason=context["reason"],
        )
        selected = {sources[s]["name"]: sources[s] for s in context.get("sources", [])}
        overlaps = {
            name
            for name in selected
            if canonicalize_name(aliases.get(name, name)) in installed_names
        }
        if overlaps != set(context.get("overlays", [])):
            raise ContractError(f"{identity}: bootstrap/source overlay drift")
        expected = [
            v for n, v in requirements.items() if n not in selected or n in overlaps
        ]
        narrowed = contracts.compare_requirements(
            items,
            [python, *expected],
            aliases,
            allow_narrowing=purpose != "production",
            narrowing_reason=environment.get("narrowing_reason", ""),
        )
        final = {}
        for required in [python, *expected]:
            name = canonicalize_name(Requirement(required).name)
            if name in overlaps:
                continue
            conda_name = canonicalize_name(aliases.get(name, name))
            final[name] = str(
                next(
                    i
                    for i in items
                    if canonicalize_name(i.requirement.name) == conda_name
                ).requirement.specifier
            )
        context["final_constraints"] = final
        results.append(
            {
                "name": identity,
                "environment": environment["path"],
                "python_minor": minor,
                "sources": context.get("sources", []),
                "overlays": sorted(overlaps),
                "narrowed": narrowed,
                "bootstrap_selectors": [i.original for i in items],
                "final_constraints": final,
            }
        )
    return results


def qualify(
    project,
    contexts,
    sources,
    selected,
    distribution_for,
    python_version,
    source_roots=None,
) -> dict:
    """Require explicit actual context; verify required bounds and every Git origin."""
    if selected not in contexts:
        raise ContractError(
            "installed @3 qualification needs one explicit reviewed context"
        )
    context = contexts[selected]
    directories = {
        identity
        for identity in context.get("sources", [])
        if sources[identity]["install"] == "pip-no-deps-directory"
    }
    roots = source_roots or {}
    if set(roots) != directories:
        raise ContractError("provide exactly the selected directory source IDs/roots")
    if ".".join(str(Version(python_version)).split(".")[:2]) != context["python_minor"]:
        raise ContractError("installed interpreter differs from selected context")
    versions = contracts.check_installed(
        project,
        version_for=lambda n: distribution_for(n).version,
        python_version=python_version,
    )
    for name, specifier in context["final_constraints"].items():
        if not Requirement(name + specifier).specifier.contains(
            Version(versions[name]), prereleases=True
        ):
            raise ContractError(
                f"installed {name} differs from selected environment constraint"
            )
    receipts = []
    for identity in context.get("sources", []):
        source = sources[identity]
        requirement = next(
            (
                v
                for v in project.get("dependencies", [])
                if canonicalize_name(Requirement(v).name) == source["name"]
            ),
            source["name"],
        )
        try:
            distribution = distribution_for(source["name"])
            if source["install"] == "pip-no-deps-directory":
                receipt = provenance.check_directory_install(
                    source, requirement, distribution, roots[identity]
                )
            else:
                receipt = provenance.check_git_install(
                    source, requirement, distribution
                )
        except (ValueError, KeyError, TypeError, OSError) as error:
            raise ContractError(f"source {identity}: {error}") from error
        receipts.append({"id": identity, **receipt})
    return {
        "qualification": "declared-and-installed-context",
        "selected_context": selected,
        "installed_versions": versions,
        "installed_sources": receipts,
    }
