"""Run trusted member audits with ephemeral HTTPS credentials and bounded output.

Credentials come from SUITE_REPOSITORIES_READ_TOKEN, never from command arguments.
The credential helper serves only registered repositories on https://github.com.
Private-output mode discards child output and emits a status-only public receipt.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

import tomllib

ROOT = Path(__file__).resolve().parents[2]
TOKEN_VARIABLE = "SUITE_REPOSITORIES_READ_TOKEN"


def registered_repositories() -> set[str]:
    registry = tomllib.loads((ROOT / "suite.toml").read_text())
    return {member["repository"] for member in registry["members"]}


def credential_response(request: str, token: str, repositories: set[str]) -> str:
    """Answer Git's credential protocol only for an allowed HTTPS repository."""
    fields = dict(line.split("=", 1) for line in request.splitlines() if "=" in line)
    path = fields.get("path", "").removesuffix(".git")
    if (
        fields.get("protocol") != "https"
        or fields.get("host") != "github.com"
        or path not in repositories
        or not token
        or any(character in token for character in "\r\n")
    ):
        return ""
    return f"username=x-access-token\npassword={token}\n\n"


def git_environment(environment: dict[str, str]) -> dict[str, str]:
    """Disable stored helpers and supply an environment-only credential helper."""
    result = dict(environment)
    # Do not inherit a cached credential, prompt, or another command-line config.
    for key in list(result):
        if key.startswith("GIT_CONFIG_") or key in {"GIT_ASKPASS", "SSH_ASKPASS"}:
            result.pop(key)
    helper = (
        f"!{shlex.quote(sys.executable)} "
        f"{shlex.quote(str(Path(__file__).resolve()))} credential"
    )
    result.update(
        GIT_TERMINAL_PROMPT="0",
        GIT_CONFIG_COUNT="3",
        GIT_CONFIG_KEY_0="credential.helper",
        GIT_CONFIG_VALUE_0="",
        GIT_CONFIG_KEY_1="credential.helper",
        GIT_CONFIG_VALUE_1=helper,
        GIT_CONFIG_KEY_2="credential.useHttpPath",
        GIT_CONFIG_VALUE_2="true",
    )
    return result


def public_source_heads(path: Path) -> list[dict[str, str]]:
    """Publish only already-registered identities and immutable source commits."""
    sources = json.loads(path.read_text())["sources"]
    repositories = registered_repositories()
    heads = []
    seen = set()
    for source in sources:
        repository, sha = source["repository"], source["sha"]
        if (
            repository not in repositories
            or repository in seen
            or not isinstance(sha, str)
            or re.fullmatch(r"[0-9a-f]{40}", sha) is None
        ):
            raise ValueError("invalid registered source identity")
        seen.add(repository)
        heads.append({"repository": repository, "sha": sha})
    if not heads:
        raise ValueError("empty source inventory")
    return heads


def run_audit(
    command: list[str],
    *,
    authenticate_git: bool = False,
    private_output: bool = False,
    receipt: Path | None = None,
    source_inventory: Path | None = None,
) -> int:
    """Propagate a real command result without publishing private child output."""
    if not command:
        raise ValueError("an audit command is required")
    environment = dict(os.environ)
    if authenticate_git:
        environment = git_environment(environment)
    else:
        environment.pop(TOKEN_VARIABLE, None)
    result = {"status": "failure", "returncode": 1}
    try:
        completed = subprocess.run(
            command,
            env=environment,
            stdout=subprocess.DEVNULL if private_output else None,
            stderr=subprocess.DEVNULL if private_output else None,
            check=False,
        )
        result["returncode"] = completed.returncode
        result["status"] = "success" if completed.returncode == 0 else "failure"
        if completed.returncode == 0 and source_inventory is not None:
            result["sources"] = public_source_heads(source_inventory)
    except (OSError, ValueError, KeyError, TypeError):
        # Exceptions may contain private paths or source; never echo their text.
        result.update(status="failure", returncode=1)
    if receipt is not None:
        receipt.parent.mkdir(parents=True, exist_ok=True)
        receipt.write_text(json.dumps(result, indent=2) + "\n")
    if private_output:
        print(f"Member audit: {result['status']} (exit {result['returncode']}).")
    return result["returncode"] if result["returncode"] >= 0 else 1


def main() -> int:
    if sys.argv[1:2] == ["credential"]:
        # Git invokes get/store/erase. Never persist a token on store/erase.
        if sys.argv[2:3] == ["get"]:
            print(
                credential_response(
                    sys.stdin.read(),
                    os.environ.get(TOKEN_VARIABLE, ""),
                    registered_repositories(),
                ),
                end="",
            )
        return 0
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--git-credentials", action="store_true")
    parser.add_argument("--private-output", action="store_true")
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--source-inventory", type=Path)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        parser.error("an audit command is required after --")
    return run_audit(
        command,
        authenticate_git=args.git_credentials,
        private_output=args.private_output,
        receipt=args.receipt,
        source_inventory=args.source_inventory,
    )


if __name__ == "__main__":
    raise SystemExit(main())
