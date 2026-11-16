"""Generate the official TypeScript source/admin scaffold without a Python package."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

if __package__:
    from . import (
        agent_instructions,
        bootstrap_component,
        repository_badges,
        suite_policy,
    )
else:
    import agent_instructions
    import bootstrap_component
    import repository_badges
    import suite_policy

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "devtools/templates/typescript_component"


def render_stage(
    target: Path,
    repository: str,
    description: str,
    policy: dict,
    *,
    admission_sha: str | None = None,
) -> Path:
    """Render supplied registry data; provider fixtures do not certify publication."""
    member = next((m for m in policy["members"] if m["repository"] == repository), None)
    if member is None or "typescript-package" not in member.get("capabilities", []):
        raise ValueError(
            "TypeScript generation requires a registered TypeScript capability"
        )
    if not description.strip() or any(c in description for c in ('"', "\n", "\\")):
        raise ValueError("description must be one plain nonempty line")
    if target.is_symlink() or (
        target.exists() and (not target.is_dir() or any(target.iterdir()))
    ):
        raise FileExistsError("TypeScript destination must be empty and unaliased")
    values = {
        "name": member["name"],
        "repository": repository,
        "description": description,
        "suite_instructions": agent_instructions.render_entry(),
        "policy_release": policy["governance"]["policy-release"],
        "admission_input": f"    with:\n      admission_sha: {admission_sha}"
        if admission_sha
        else "",
    }
    tokens = {
        "__COMPONENT_NAME__": "name",
        "__REPOSITORY__": "repository",
        "__DESCRIPTION__": "description",
        "__SUITE_INSTRUCTIONS__": "suite_instructions",
        "__POLICY_RELEASE__": "policy_release",
        "__ADMISSION_INPUT__": "admission_input",
    }
    shutil.copytree(
        TEMPLATE,
        target,
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns("node_modules", "dist", "__pycache__", "*.pyc"),
    )
    bootstrap_component.render_template(target, values, tokens)
    for source, destination in (
        (ROOT / "LICENSE", target / "LICENSE"),
        (ROOT / "MOLSYSSUITE_GUIDE.md", target / "MOLSYSSUITE_GUIDE.md"),
    ):
        shutil.copy2(source, destination)
    readme = target / "README.md"
    readme.write_text(
        readme.read_text().replace(
            f"# {member['name']}\n",
            f"# {member['name']}\n\n"
            + repository_badges.render_snippet(policy, repository),
            1,
        )
    )
    findings = agent_instructions.check(target, policy, repository)
    if findings:
        raise ValueError(
            "TypeScript instruction routes: " + "; ".join(f.message for f in findings)
        )
    # No dependency install or executable package script is run by generation.
    return target


def bootstrap(
    target: Path,
    repository: str,
    description: str,
    *,
    admission_sha: str | None = None,
    offline: bool = False,
) -> Path:
    live = suite_policy.load_effective_registry()
    if (
        not offline
        and suite_policy.published_policy_target()["release"]
        != live["governance"]["policy-release"]
    ):
        raise ValueError("starter target differs from latest published policy")
    policy = bootstrap_component.published_policy(live["governance"]["policy-release"])
    if admission_sha:
        policy = suite_policy.apply_admission(
            policy, suite_policy.admission_at_commit(ROOT, admission_sha), repository
        )
    return render_stage(
        target, repository, description, policy, admission_sha=admission_sha
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--description", required=True)
    parser.add_argument("--admission-sha")
    parser.add_argument("--offline-policy-target", action="store_true")
    args = parser.parse_args()
    try:
        target = bootstrap(
            args.target,
            args.repository,
            args.description,
            admission_sha=args.admission_sha,
            offline=args.offline_policy_target,
        )
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        print(error, file=sys.stderr)
        return 2
    print(
        json.dumps(
            {
                "created": str(target),
                "repository": args.repository,
                "scope": "source/admin scaffold only; actual owner, science and public receiving pending",
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
