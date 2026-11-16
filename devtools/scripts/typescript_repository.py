"""Inspect the TypeScript package boundary without manufacturing Python metadata."""

from __future__ import annotations

import json
import re
from pathlib import Path

if __package__:
    from . import suite_policy
else:
    import suite_policy

CALLER_PREFIX = suite_policy.TYPESCRIPT_CALLER_PREFIX
VERSION = re.compile(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\Z")


def check(root: Path, repository: str, policy: dict) -> list[str]:
    """Return structural findings; executed owner/product gates stay independent."""
    errors = []
    try:
        manifest = json.loads((root / "package.json").read_text())
        lock = json.loads((root / "package-lock.json").read_text())
        config = json.loads((root / "tsconfig.json").read_text())
    except (OSError, ValueError):
        return ["TypeScript package/lock/compiler configuration is unavailable"]
    if (
        not isinstance(manifest, dict)
        or not isinstance(lock, dict)
        or not isinstance(config, dict)
    ):
        return ["TypeScript package/lock/compiler configuration must be objects"]
    expected_name = "@uibcdf/" + repository.rsplit("/", 1)[-1]
    if manifest.get("name") != expected_name or manifest.get("type") != "module":
        errors.append("package needs its registered scoped name and ESM type")
    version = manifest.get("version", "")
    if not isinstance(version, str) or VERSION.fullmatch(version) is None:
        errors.append("package version must be canonical X.Y.Z")
    packages = lock.get("packages", {})
    if not isinstance(packages, dict) or not isinstance(packages.get("", {}), dict):
        return ["TypeScript lock package inventory is malformed"]
    locked = packages.get("", {})
    if any(
        row.get("name") != expected_name or row.get("version") != version
        for row in (lock, locked)
    ):
        errors.append("package and lock identities differ")
    required = {
        "typecheck": "tsc",
        "format:check": "prettier",
        "test": "node --test",
        "pack:check": None,
        "pack:conda:check": None,
        "check:reports": None,
        "check:version": None,
    }
    scripts = manifest.get("scripts", {})
    if not isinstance(scripts, dict):
        return ["TypeScript scripts must be a mapping"]
    for name, operation in required.items():
        value = scripts.get(name, "")
        if (
            not isinstance(value, str)
            or not value.strip()
            or (operation and operation not in value)
        ):
            errors.append(f"missing applicable native command: {name}")
    dev = manifest.get("devDependencies", {})
    settings = policy.get("policies", {}).get("typescript", {})
    if not isinstance(dev, dict) or not isinstance(scripts, dict):
        return ["TypeScript scripts/development dependencies must be mappings"]
    for name in ("typescript", "prettier"):
        selected = dev.get(name, "")
        if not isinstance(selected, str) or VERSION.fullmatch(selected) is None:
            errors.append(f"development {name} must be exactly pinned")
        if selected != settings.get(name, selected):
            errors.append(f"development {name} differs from the qualified policy tool")
    if locked.get("devDependencies") != dev:
        errors.append("lock root does not preserve development tool pins")
    options = config.get("compilerOptions", {})
    if not isinstance(options, dict) or options.get("strict") is not True:
        errors.append("TypeScript compiler must enable strict checks")
    engines = manifest.get("engines", {})
    engine = engines.get("node", "") if isinstance(engines, dict) else ""
    if re.fullmatch(r">=24(?:\.0(?:\.0)?)?", str(engine)) is None:
        errors.append("reviewed Node baseline requires engines.node >=24")
    if not manifest.get("types") or not manifest.get("exports"):
        errors.append("public ESM and declaration entry points must be explicit")
    if not (root / "LICENSE").is_file():
        errors.append("source license is missing")
    # Common latest-policy checks parse real YAML callers separately; this branch
    # proves applicability of the TypeScript gate, never a Python substitute.
    documents = [
        p.read_text()
        for p in sorted((root / ".github/workflows").glob("*"))
        if p.is_file() and p.suffix in {".yml", ".yaml"}
    ]
    try:
        refs = suite_policy.policy_caller_releases(documents, prefixes=(CALLER_PREFIX,))
    except (TypeError, ValueError):
        refs = []
    if refs != [policy["governance"]["policy-release"]]:
        errors.append("actual immutable current TypeScript policy caller is required")
    return errors
