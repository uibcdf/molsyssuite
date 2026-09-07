"""Check or synchronize the canonical MolSysSuite guide in member repositories."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import tomllib

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "MOLSYSSUITE_GUIDE.md"


def _registered_names() -> set[str]:
    policy = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
    return {str(member["name"]).casefold() for member in policy["members"]}


def _default_targets() -> list[Path]:
    names = _registered_names()
    return sorted(
        (path for path in ROOT.parent.iterdir() if path.name.casefold() in names),
        key=lambda path: path.name.casefold(),
    )


def process(targets: list[Path], write: bool) -> list[str]:
    expected = SOURCE.read_bytes()
    registered = _registered_names()
    errors: list[str] = []
    for target in targets:
        root = target.resolve()
        if root.name.casefold() not in registered:
            errors.append(f"{root}: not a registered member directory")
            continue
        destination = root / SOURCE.name
        if destination.is_file() and destination.read_bytes() == expected:
            continue
        if write:
            destination.write_bytes(expected)
            print(f"wrote {destination}")
        else:
            errors.append(f"{destination}: missing or different")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("targets", nargs="*", type=Path)
    parser.add_argument("--write", action="store_true")
    arguments = parser.parse_args()
    targets = arguments.targets or _default_targets()
    errors = process(targets, arguments.write)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    action = "synchronized" if arguments.write else "current"
    print(f"MolSysSuite component guides are {action} in {len(targets)} repositories.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
