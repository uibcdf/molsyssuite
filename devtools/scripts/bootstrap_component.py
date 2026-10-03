"""Generate a policy-conforming Python MolSysSuite component repository."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

import tomllib

try:
    from devtools.scripts import repository_badges, suite_policy
except ModuleNotFoundError:  # Direct execution from devtools/scripts.
    import repository_badges
    import suite_policy

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "devtools/templates/python_component"
TOKENS = {
    "__COMPONENT_NAME__": "name",
    "__PACKAGE_NAME__": "package",
    "__REPOSITORY__": "repository",
    "__DESCRIPTION__": "description",
    "__RUFF_VERSION__": "ruff_version",
    "__REQUIRES_PYTHON__": "requires_python",
    "__VERSIONINGIT_PATTERN__": "versioningit_pattern",
    "__RUFF_TARGET__": "ruff_target",
    "__RUFF_RULES__": "ruff_rules",
    "__DEV_VERSION__": "dev_version",
    "__CI_VERSIONS__": "ci_versions",
    "__CI_VERSIONS_YAML__": "ci_versions_yaml",
    "__POLICY_RELEASE__": "policy_release",
    "__ADMISSION_INPUT__": "admission_input",
}


def _published_policy(release: str) -> dict:
    """Require a locally available immutable published policy snapshot."""
    if re.fullmatch(r"policy-v[0-9]+\.[0-9]+\.[0-9]+", release) is None:
        raise ValueError("policy release must be a versioned policy tag")
    try:
        commit = subprocess.check_output(
            ["git", "-C", str(ROOT), "rev-parse", f"refs/tags/{release}^{{commit}}"],
            text=True,
            stderr=subprocess.PIPE,
            timeout=30,
        ).strip()
    except subprocess.SubprocessError as error:
        raise ValueError(
            f"published {release} is unavailable; fetch its tag before generation"
        ) from error
    policy = suite_policy.effective_registry(
        suite_policy.registry_at_commit(ROOT, commit)
    )
    if policy["governance"]["policy-release"] != release:
        raise ValueError("published tag does not declare the requested policy release")
    return policy


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
    target: Path,
    repository: str,
    description: str,
    package: str | None = None,
    *,
    admission_sha: str | None = None,
) -> Path:
    """Create and return a new component root, refusing ambiguous destinations."""
    member = _registered_member(repository)
    if member is None:
        raise ValueError(f"{repository!r} must be registered in suite.toml first")
    if "python-package" not in member.get("capabilities", []):
        raise ValueError(f"{repository!r} does not carry the python-package capability")

    component_name = str(member["name"])
    package_name = package or _package_name(component_name)
    if not package_name.isidentifier():
        raise ValueError(f"{package_name!r} is not a valid Python package name")
    if not description.strip() or '"' in description or "\n" in description:
        raise ValueError("description must be one non-empty line without double quotes")
    if target.exists() and (not target.is_dir() or any(target.iterdir())):
        raise FileExistsError(f"destination is not empty: {target}")

    local_policy = suite_policy.load_effective_registry()
    release = str(local_policy["governance"]["policy-release"])
    policy = _published_policy(release)
    if admission_sha is not None:
        if tuple(map(int, release.removeprefix("policy-v").split("."))) < (1, 5, 5):
            raise ValueError(
                "admission_sha requires policy-v1.5.5 or a later feature release"
            )
        policy = suite_policy.apply_admission(
            policy, suite_policy.admission_at_commit(ROOT, admission_sha), repository
        )
    if not any(
        str(row["repository"]).casefold() == repository.casefold()
        for row in policy["members"]
    ):
        raise ValueError(
            f"{repository} is absent from {release}; supply its published --admission-sha"
        )
    values = {
        "name": component_name,
        "package": package_name,
        "repository": repository,
        "description": description,
        "ruff_version": str(policy["policies"]["python-quality"]["ruff-version"]),
        "requires_python": str(policy["policies"]["python"]["requires-python"]),
        "versioningit_pattern": str(
            policy["policies"]["release-version"]["versioningit-pattern"]
        ),
        "ruff_target": str(policy["policies"]["python-quality"]["target-version"]),
        "ruff_rules": ", ".join(
            f'"{rule}"'
            for rule in policy["policies"]["python-quality"]["required-lint-rules"]
        ),
        "dev_version": str(policy["policies"]["python"]["development-version"]),
        "ci_versions": ", ".join(policy["policies"]["python"]["ci-versions"]),
        "ci_versions_yaml": ", ".join(
            f'"{version}"' for version in policy["policies"]["python"]["ci-versions"]
        ),
        "policy_release": release,
        "admission_input": (
            f"    with:\n      admission_sha: {admission_sha}" if admission_sha else ""
        ),
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
    readme = target / "README.md"
    heading = f"# {component_name}\n"
    readme.write_text(
        readme.read_text(encoding="utf-8").replace(
            heading,
            heading + "\n" + repository_badges.render_snippet(policy, repository),
            1,
        ),
        encoding="utf-8",
    )
    shutil.copy2(ROOT / "MOLSYSSUITE_GUIDE.md", target / "MOLSYSSUITE_GUIDE.md")
    # Validate the generated instruction routes from the same provider used by audits.
    try:
        from devtools.scripts import agent_instructions
    except ImportError:
        import agent_instructions
    findings = agent_instructions.check(target, policy, repository)
    if findings:
        raise ValueError(
            "generated instruction routes: " + "; ".join(f.message for f in findings)
        )
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--description", required=True)
    parser.add_argument("--package")
    parser.add_argument("--admission-sha")
    arguments = parser.parse_args()
    try:
        root = bootstrap(
            arguments.target.resolve(),
            arguments.repository,
            arguments.description,
            arguments.package,
            admission_sha=arguments.admission_sha,
        )
    except (FileExistsError, ValueError) as error:
        print(error, file=sys.stderr)
        return 2
    print(f"Created {arguments.repository} starter repository at {root}")
    print("Next: review README.md, run pytest and Ruff, then run check_repository.py.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
