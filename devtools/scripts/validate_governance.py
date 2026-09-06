"""Validate MolSysSuite governance records without network access."""

from __future__ import annotations

import sys

import tomllib

try:
    from devtools.scripts import devguide_index
    from devtools.scripts.devguide_reports import ROOT, validate_all
except ImportError:
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
    if len(names) != len(set(names)):
        errors.append("suite.toml: member names must be unique")
    if len(repositories) != len(set(repositories)):
        errors.append("suite.toml: member repositories must be unique")
    for member in members:
        name = member.get("name")
        if member.get("repository") != f"uibcdf/{name}":
            errors.append(f"suite.toml: repository does not match member {name!r}")
        if not member.get("profiles"):
            errors.append(f"suite.toml: member {name!r} has no profiles")
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
