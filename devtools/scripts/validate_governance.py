"""Validate MolSysSuite governance records without network access."""

from __future__ import annotations

import sys

import tomllib

try:
    from devtools.scripts import adoption_status, audit_zenodo, devguide_index
    from devtools.scripts.devguide_reports import ROOT, validate_all
except ImportError:
    import adoption_status
    import audit_zenodo
    import devguide_index
    from devguide_reports import ROOT, validate_all


def _validate_registry() -> list[str]:
    path = ROOT / "suite.toml"
    if not path.exists():
        return ["suite.toml is missing"]
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    members = data.get("members", [])
    names = [member.get("name") for member in members]
    repositories = [member.get("repository") for member in members]
    policies = data.get("policies", {})
    classification = policies.get("member-classification", {})
    accepted_values = {
        "role": set(classification.get("roles", [])),
        "membership": set(classification.get("memberships", [])),
        "maturity": set(classification.get("maturities", [])),
        "development-mode": set(classification.get("development-modes", [])),
    }
    accepted_capabilities = set(classification.get("capabilities", []))
    if len(names) != len(set(names)):
        errors.append("suite.toml: member names must be unique")
    if len(repositories) != len(set(repositories)):
        errors.append("suite.toml: member repositories must be unique")
    for member in members:
        name = member.get("name")
        if member.get("repository") != f"uibcdf/{name}":
            errors.append(f"suite.toml: repository does not match member {name!r}")
        for field, accepted in accepted_values.items():
            if member.get(field) not in accepted:
                errors.append(
                    f"suite.toml: member {name!r} has unknown {field} "
                    f"{member.get(field)!r}"
                )
        capabilities = member.get("capabilities", [])
        if not capabilities:
            errors.append(f"suite.toml: member {name!r} has no capabilities")
        unknown = set(capabilities) - accepted_capabilities
        if unknown:
            errors.append(
                f"suite.toml: member {name!r} has unknown capabilities "
                + ", ".join(sorted(unknown))
            )

    for initiative_name, initiative in data.get("initiatives", {}).items():
        if initiative.get("status") not in {
            "planned",
            "active",
            "paused",
            "completed",
            "cancelled",
        }:
            errors.append(
                f"suite.toml: initiative {initiative_name!r} has invalid status"
            )
        priority_members = initiative.get("priority-members", [])
        if len(priority_members) != len(set(priority_members)):
            errors.append(
                f"suite.toml: initiative {initiative_name!r} repeats priority members"
            )
        unknown = set(priority_members) - set(names)
        if unknown:
            errors.append(
                f"suite.toml: initiative {initiative_name!r} has unknown members "
                + ", ".join(sorted(unknown))
            )

    for name, policy in policies.items():
        if policy.get("status") != "accepted":
            errors.append(f"suite.toml: policy {name!r} is not accepted")
        if not policy.get("applies-to"):
            errors.append(f"suite.toml: policy {name!r} has no applicability selector")
        for selector in policy.get("applies-to", []):
            if selector.startswith("capability:"):
                capability = selector.removeprefix("capability:")
                if capability not in accepted_capabilities:
                    errors.append(
                        f"suite.toml: policy {name!r} selects unknown capability "
                        f"{capability!r}"
                    )
        issue = policy.get("issue", "")
        if not issue.startswith("uibcdf/molsyssuite#"):
            errors.append(f"suite.toml: policy {name!r} has no central issue")
        normative = policy.get("normative", "")
        if not normative or not (ROOT / normative).is_file():
            errors.append(
                f"suite.toml: policy {name!r} has no existing normative record"
            )
    python_policy = policies.get("python", {})
    transition = python_policy.get("transition", {})
    if transition:
        if transition.get("status") != "active":
            errors.append("suite.toml: Python transition must be active")
        if transition.get("issue") != "uibcdf/molsyssuite#29":
            errors.append("suite.toml: Python transition has no owning issue")
        if not transition.get("target-requires-python"):
            errors.append("suite.toml: Python transition has no target range")
        if "3.14" not in transition.get("target-ci-versions", []):
            errors.append("suite.toml: Python transition does not test Python 3.14")
        components = transition.get("components", [])
        component_names = [component.get("name") for component in components]
        if len(component_names) != len(set(component_names)):
            errors.append("suite.toml: Python transition components must be unique")
        by_name = {member.get("name"): member for member in members}
        for component in components:
            name = component.get("name")
            member = by_name.get(name)
            if member is None or "python-package" not in member.get("capabilities", []):
                errors.append(
                    f"suite.toml: Python transition component {name!r} is not a Python member"
                )
            if component.get("state") not in {"authorized", "admitted"}:
                errors.append(
                    f"suite.toml: Python transition component {name!r} has invalid state"
                )
            if not str(component.get("issue", "")).startswith(f"uibcdf/{name}#"):
                errors.append(
                    f"suite.toml: Python transition component {name!r} has no local issue"
                )
    zenodo_policy = policies.get("zenodo-archival", {})
    inventory_path = ROOT / str(zenodo_policy.get("inventory", ""))
    if not inventory_path.is_file():
        errors.append("suite.toml: Zenodo policy has no existing inventory")
    else:
        inventory = tomllib.loads(inventory_path.read_text(encoding="utf-8"))
        errors.extend(audit_zenodo.validate_inventory(data, inventory))
    errors.extend(adoption_status.validate_exceptions(data))
    return errors


def validate() -> list[str]:
    _, errors = validate_all()
    errors.extend(_validate_registry())
    try:
        stale = devguide_index.process(check=True)
    except ValueError as error:
        errors.extend(str(error).splitlines())
    else:
        errors.extend(f"{path}: generated index is stale" for path in stale)

    for route in (ROOT / "AGENTS.md", ROOT / "devguide" / "README.md"):
        if "reporting_protocol.md" not in route.read_text(encoding="utf-8"):
            errors.append(
                f"{route.relative_to(ROOT)}: does not route to the reporting protocol"
            )
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("Governance validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Governance validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
