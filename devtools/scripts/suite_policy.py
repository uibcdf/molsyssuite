"""Load MolSysSuite-owned member policy without fetching MOLI."""

from __future__ import annotations

import copy
import re
import subprocess
from pathlib import Path

import tomllib

ROOT = Path(__file__).resolve().parents[2]
MEMBER_POLICIES = {
    "repository-badges": (),
    "python": ("requires-python", "development-version", "ci-versions"),
    "python-ci": (
        "review-table",
        "routine-python",
        "routine-events",
        "routine-os",
        "pull-request-test-level",
        "skip-ci-recovery",
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


def registry_at_commit(root: Path, commit: str) -> dict[str, object]:
    """Read committed registry data, never files or code from its working tree."""
    if re.fullmatch(r"[0-9a-f]{40}", commit) is None:
        raise ValueError("admission_sha must be a full lowercase 40-character commit")
    try:
        resolved = subprocess.check_output(
            ["git", "-C", str(root), "rev-parse", f"{commit}^{{commit}}"],
            text=True,
            stderr=subprocess.PIPE,
            timeout=30,
        ).strip()
        if resolved != commit:
            raise ValueError("admission identity is not the requested commit")
        text = subprocess.check_output(
            ["git", "-C", str(root), "show", f"{commit}:suite.toml"],
            text=True,
            stderr=subprocess.PIPE,
            timeout=30,
        )
        registry = tomllib.loads(text)
    except (subprocess.SubprocessError, tomllib.TOMLDecodeError) as error:
        raise ValueError("cannot read the committed admission registry") from error
    if registry.get("governance", {}).get("repository") != "uibcdf/molsyssuite":
        raise ValueError("admission registry must belong to uibcdf/molsyssuite")
    return registry


def apply_admission(policy: dict, admission: dict, repository: str) -> dict:
    """Add only the requested identity/classification; keep all frozen rules."""
    wanted = repository.casefold()
    candidates = [
        row
        for row in admission.get("members", [])
        if str(row.get("repository", "")).casefold() == wanted
    ]
    if len(candidates) != 1:
        raise ValueError("admission must register the requested member exactly once")
    result = copy.deepcopy(policy)
    if any(str(row["repository"]).casefold() == wanted for row in policy["members"]):
        return result
    source = candidates[0]
    name = source.get("name")
    if (
        not isinstance(name, str)
        or re.fullmatch(r"[a-z][a-z0-9-]*", name) is None
        or wanted != f"uibcdf/{name}"
        or any(str(row["name"]).casefold() == name for row in policy["members"])
    ):
        raise ValueError("admission has an invalid or conflicting member identity")
    classification = policy["policies"]["member-classification"]
    row = {"name": name, "repository": f"uibcdf/{name}"}
    for key, vocabulary in (
        ("role", "roles"),
        ("membership", "memberships"),
        ("maturity", "maturities"),
        ("development-mode", "development-modes"),
    ):
        value = source.get(key)
        if not isinstance(value, str) or value not in classification[vocabulary]:
            raise ValueError(f"admission {key} is outside the frozen vocabulary")
        row[key] = value
    capabilities = source.get("capabilities")
    if (
        not isinstance(capabilities, list)
        or not capabilities
        or any(not isinstance(value, str) for value in capabilities)
        or len(capabilities) != len(set(capabilities))
        or any(value not in classification["capabilities"] for value in capabilities)
    ):
        raise ValueError("admission capabilities are outside the frozen vocabulary")
    row["capabilities"] = list(capabilities)
    result["members"].append(row)
    return result


def admission_at_commit(root: Path, commit: str) -> dict:
    """Require admission data from published central main history."""
    registry = registry_at_commit(root, commit)
    try:
        origin = (
            subprocess.check_output(
                ["git", "-C", str(root), "remote", "get-url", "origin"],
                text=True,
                stderr=subprocess.PIPE,
                timeout=30,
            )
            .strip()
            .removesuffix(".git")
        )
        if origin not in {
            "https://github.com/uibcdf/molsyssuite",
            "git@github.com:uibcdf/molsyssuite",
            "ssh://git@github.com/uibcdf/molsyssuite",
        }:
            raise ValueError("admission must come from the central repository")
        subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "merge-base",
                "--is-ancestor",
                commit,
                "refs/remotes/origin/main",
            ],
            check=True,
            capture_output=True,
            timeout=30,
        )
    except subprocess.SubprocessError as error:
        raise ValueError(
            "admission commit must be published in central main history; fetch that history"
        ) from error
    return registry
