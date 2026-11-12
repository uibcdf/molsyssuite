"""Generate explicit suite dependency hints without guessing public availability."""

from __future__ import annotations

import argparse
import json
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def dependency_hint(registry: dict, channels: dict, name: str) -> dict:
    """Return DepDigest-compatible routes for a registered Python member.

    This deliberately handles suite providers only. Third-party routes and local
    source/editable installation remain caller-owned and unchanged.
    """
    members = {
        member["name"]: member
        for member in registry["members"]
        if "python-package" in member.get("capabilities", [])
    }
    exceptions = channels.get("active-pypi-exceptions")
    if (
        channels.get("schema") != 1
        or channels.get("suite-channel") != "uibcdf"
        or not isinstance(exceptions, list)
        or not all(isinstance(item, str) for item in exceptions)
        or len(set(exceptions)) != len(exceptions)
        or not set(exceptions).issubset(members)
    ):
        raise ValueError("invalid reviewed suite channel inventory")
    if name not in members:
        raise ValueError(
            "select a registered Python member; external routes are separate"
        )
    return {
        "pypi": name if name in exceptions else None,
        "conda": name,
        "channel": channels["suite-channel"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("member")
    args = parser.parse_args()
    try:
        hint = dependency_hint(
            tomllib.loads((ROOT / "suite.toml").read_text()),
            tomllib.loads((ROOT / "devguide/package_channels.toml").read_text()),
            args.member,
        )
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps(hint, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
