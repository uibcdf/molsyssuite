"""Generate a policy-conforming Python MolSysSuite component repository."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

import tomllib

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "devtools/templates/python_component"
TOKENS = {
    "__COMPONENT_NAME__": "name",
    "__PACKAGE_NAME__": "package",
    "__REPOSITORY__": "repository",
    "__DESCRIPTION__": "description",
    "__RUFF_VERSION__": "ruff_version",
}


def _registered_member(repository: str) -> dict[str, object] | None:
    policy = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
    wanted = repository.casefold()
    return next(
        (
            member
            for member in policy["members"]
            if str(member["repository"]).casefold() == wanted
        ),
        None,
    )


def _package_name(component_name: str) -> str:
    return re.sub(r"\W+", "_", component_name.replace("-", "_")).strip("_")


def _replace_tokens(root: Path, values: dict[str, str]) -> None:
    for path in sorted(root.rglob("*"), key=lambda item: len(item.parts), reverse=True):
        replacement = path.name
        for token, key in TOKENS.items():
            replacement = replacement.replace(token, values[key])
        if replacement != path.name:
            path.rename(path.with_name(replacement))

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for token, key in TOKENS.items():
            text = text.replace(token, values[key])
        path.write_text(text, encoding="utf-8")


def bootstrap(
    target: Path, repository: str, description: str, package: str | None = None
) -> Path:
    """Create and return a new component root, refusing ambiguous destinations."""
    member = _registered_member(repository)
    if member is None:
        raise ValueError(f"{repository!r} must be registered in suite.toml first")
    if "python-library" not in member.get("profiles", []):
        raise ValueError(f"{repository!r} does not carry the python-library profile")

    component_name = str(member["name"])
    package_name = package or _package_name(component_name)
    if not package_name.isidentifier():
        raise ValueError(f"{package_name!r} is not a valid Python package name")
    if not description.strip() or '"' in description or "\n" in description:
        raise ValueError("description must be one non-empty line without double quotes")
    if target.exists() and (not target.is_dir() or any(target.iterdir())):
        raise FileExistsError(f"destination is not empty: {target}")

    policy = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
    values = {
        "name": component_name,
        "package": package_name,
        "repository": repository,
        "description": description,
        "ruff_version": str(policy["policies"]["python-quality"]["ruff-version"]),
    }
    target.mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        TEMPLATE,
        target,
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns(
            "__pycache__", "*.pyc", ".pytest_cache", ".ruff_cache"
        ),
    )
    _replace_tokens(target, values)
    shutil.copy2(ROOT / "MOLSYSSUITE_GUIDE.md", target / "MOLSYSSUITE_GUIDE.md")
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--description", required=True)
    parser.add_argument("--package")
    arguments = parser.parse_args()
    try:
        root = bootstrap(
            arguments.target.resolve(),
            arguments.repository,
            arguments.description,
            arguments.package,
        )
    except (FileExistsError, ValueError) as error:
        print(error, file=sys.stderr)
        return 2
    print(f"Created {arguments.repository} starter repository at {root}")
    print("Next: review README.md, run pytest and Ruff, then run check_repository.py.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
