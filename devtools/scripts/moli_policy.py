"""Resolve inherited engineering values from an immutable MOLI checkout."""

from __future__ import annotations

import copy
import os
import re
import subprocess
from pathlib import Path

import tomllib

ROOT = Path(__file__).resolve().parents[2]
POLICY_NAMES = {
    "repository-badges": "repository_badges",
    "python": "python",
    "python-ci": "python_ci",
    "python-quality": "python_quality",
    "release-version": "release_version",
    "zenodo-archival": "zenodo_archival",
}


def _moli_root() -> Path:
    configured = os.environ.get("MOLI_POLICY_ROOT")
    return Path(configured).resolve() if configured else ROOT.parent / "moli"


def load_moli_registry(suite: dict[str, object]) -> dict[str, object]:
    """Read the exact MOLI revision recorded by the suite registry."""

    reference = str(suite["governance"]["platform-policy-ref"])
    if re.fullmatch(r"[0-9a-f]{40}", reference) is None:
        raise ValueError("suite.toml: platform-policy-ref must be a full commit SHA")
    root = _moli_root()
    if not root.is_dir():
        raise ValueError(f"MOLI policy checkout is missing: {root}")
    committed = subprocess.run(
        ["git", "-C", str(root), "show", f"{reference}:moli.toml"],
        capture_output=True,
        check=False,
    )
    if committed.returncode != 0:
        raise ValueError(
            f"MOLI policy checkout does not contain pinned commit {reference}; "
            "fetch it from uibcdf/moli"
        )
    moli = tomllib.loads(committed.stdout.decode("utf-8"))
    if moli.get("schema_version") != "0.3":
        raise ValueError("MOLI policy checkout has an unsupported registry schema")
    if (
        moli.get("components", {}).get("molsyssuite", {}).get("repository")
        != suite["governance"]["repository"]
    ):
        raise ValueError(
            "MOLI policy checkout does not register this delegated component"
        )
    return moli


def effective_registry(suite: dict[str, object]) -> dict[str, object]:
    """Combine MOLI baseline values with MolSysSuite-only adoption data."""

    moli = load_moli_registry(suite)
    effective = copy.deepcopy(suite)
    local_policies = effective["policies"]
    for local_name, upstream_name in POLICY_NAMES.items():
        local = local_policies[local_name]
        if (
            local.get("owner") != "uibcdf/moli"
            or local.get("upstream-policy") != upstream_name
        ):
            raise ValueError(
                f"suite.toml: {local_name} does not identify its MOLI owner and policy"
            )
        upstream = moli["policies"][upstream_name]
        if upstream.get("status") != "accepted":
            raise ValueError(f"MOLI policy {upstream_name} is not accepted")
        if local.get("applies-to") != upstream.get("applies_to"):
            raise ValueError(
                f"suite.toml: {local_name} changes MOLI policy applicability"
            )
        local["upstream-normative"] = upstream["normative"]
        for key, value in upstream.items():
            if key in {"status", "applies_to", "normative", "transition"}:
                continue
            local_key = key.replace("_", "-")
            if local_key in local:
                raise ValueError(
                    f"suite.toml: {local_name}.{local_key} duplicates a MOLI value"
                )
            local[local_key] = copy.deepcopy(value)

    local_transition = local_policies["python"]["transition"]
    upstream_transition = moli["policies"]["python"]["transition"]
    if local_transition.get("status") != upstream_transition.get("status"):
        raise ValueError("suite.toml: Python transition status differs from MOLI")
    for key in ("target_requires_python", "target_ci_versions"):
        local_key = key.replace("_", "-")
        if local_key in local_transition:
            raise ValueError(
                f"suite.toml: python.transition.{local_key} duplicates MOLI"
            )
        local_transition[local_key] = copy.deepcopy(upstream_transition[key])

    release = local_policies["release-version"]
    pattern = release["pattern"]
    if (
        not isinstance(pattern, str)
        or not pattern.startswith("^")
        or not pattern.endswith("$")
    ):
        raise ValueError("MOLI release-version pattern must be anchored")
    release["versioningit-pattern"] = f"^(?P<version>{pattern[1:-1]})$"
    return effective


def load_effective_registry() -> dict[str, object]:
    suite = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
    return effective_registry(suite)
