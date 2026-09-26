"""Load MolSysSuite-owned member policy without fetching MOLI."""

from __future__ import annotations

import copy
import re
from pathlib import Path

import tomllib

ROOT = Path(__file__).resolve().parents[2]
MEMBER_POLICIES = {
    "repository-badges": (),
    "python": ("requires-python", "development-version", "ci-versions"),
    "python-ci": (
        "routine-python",
        "routine-events",
        "routine-os",
        "full-matrix-frequency",
        "full-matrix-os",
        "baseline-os",
        "optional-os",
        "claimed-non-linux-frequency",
        "release-installed-matrix",
        "manual-dispatch",
    ),
    "python-quality": (
        "formatter",
        "linter",
        "test-runner",
        "ruff-version",
        "target-version",
        "required-lint-rules",
    ),
    "python-support-libraries": ("libraries", "review-field"),
    "python-developer-tools": ("tools", "review-field"),
    "python-distribution": (
        "primary-public-channel",
        "third-party-channel",
        "pypi-route",
        "review-field",
    ),
    "release-version": ("format", "pattern", "public-prereleases"),
    "zenodo-archival": (),
}


def effective_registry(suite: dict[str, object]) -> dict[str, object]:
    """Return the suite's normative member registry with derived parser values."""

    effective = copy.deepcopy(suite)
    governance = effective["governance"]
    owner = governance["repository"]
    if governance.get("engineering-baseline-owner") != owner:
        raise ValueError(
            "suite.toml: MolSysSuite must own its member engineering baseline"
        )
    policies = effective["policies"]
    for name, required in MEMBER_POLICIES.items():
        policy = policies[name]
        if policy.get("owner") != owner:
            raise ValueError(f"suite.toml: {name} must be owned by {owner}")
        if any(
            key in policy for key in ("inheritance", "upstream-policy", "suite-profile")
        ):
            raise ValueError(
                f"suite.toml: {name} still delegates member policy to MOLI"
            )
        missing = [key for key in required if key not in policy]
        if missing:
            raise ValueError(
                f"suite.toml: {name} lacks local values: {', '.join(missing)}"
            )

    transition = policies["python"].get("transition", {})
    for key in ("target-requires-python", "target-ci-versions"):
        if key not in transition:
            raise ValueError(f"suite.toml: python.transition lacks local {key}")

    release = policies["release-version"]
    pattern = release["pattern"]
    if (
        not isinstance(pattern, str)
        or not pattern.startswith("^")
        or not pattern.endswith("$")
    ):
        raise ValueError("suite.toml: release-version pattern must be anchored")
    try:
        if re.fullmatch(pattern, "1.2.3") is None or re.fullmatch(pattern, "01.2.3"):
            raise ValueError(
                "suite.toml: release-version pattern must accept canonical X.Y.Z"
            )
    except re.error as error:
        raise ValueError("suite.toml: release-version pattern is invalid") from error
    release["versioningit-pattern"] = f"^(?P<version>{pattern[1:-1]})$"
    return effective


def load_effective_registry() -> dict[str, object]:
    suite = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
    return effective_registry(suite)
