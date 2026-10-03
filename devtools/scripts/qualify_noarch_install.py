"""Qualify real Conda solving and exact installation using frozen channel fixtures."""

from __future__ import annotations

import argparse
import functools
import http.server
import importlib.metadata
import json
import os
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

import yaml

if not __package__:
    sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    from devtools.scripts._release_http import read_json
    from devtools.scripts.installed_noarch import (
        download,
        install_artifact,
        verify_installed,
    )
    from devtools.scripts.noarch_conda import ContractError, inspect_recipe
    from devtools.scripts.verify_public_conda import verify_snapshot
except ModuleNotFoundError:
    from _release_http import read_json
    from installed_noarch import download, install_artifact, verify_installed
    from noarch_conda import ContractError, inspect_recipe
    from verify_public_conda import verify_snapshot

PACKAGE = "pytest-receptor"
OLD_VERSION = "1.2.0"
OLD_DIGEST = "fc9613fb825aed00fcec12312fd90dc8e7807fe1bfedaeda4f2b0bbbcf9b2006"
NEW_VERSION = "1.2.1"
NEW_DIGEST = "77bf3694bc903f606d4323b88e3bb3aea9628618036b53073f5a5dbd5dbc73cb"
SOURCE = "6c4686c55ee5e004160ba4c36a499ff7e5c8a64b"


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        """Keep HTTP fixture logging out of evidence output."""


def write_index(directory: Path, subdir: str, records: dict) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    document = {
        "info": {"subdir": subdir},
        "packages": records,
        "packages.conda": {},
        "repodata_version": 1,
        "removed": [],
    }
    for filename in ("repodata.json", "current_repodata.json"):
        (directory / filename).write_text(json.dumps(document) + "\n")


def qualify(root: Path, platform: str, python: str, directory: Path) -> dict:
    """Use real old/public bytes and a real exact staged URL; never write a registry."""
    plan, inventory = inspect_recipe(
        root,
        "devtools/conda-build/release_plan.toml",
        "devtools/conda-build/resources.toml",
    )
    checkout = subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "HEAD"], text=True
    ).strip()
    if (
        checkout != SOURCE
        or plan["package"] != PACKAGE
        or plan["version"] != NEW_VERSION
        or plan["build_number"] != 0
    ):
        raise ContractError(
            "qualification fixture needs the reviewed original producer"
        )
    if platform not in {"linux-64", "osx-arm64"} or python not in {
        "3.11",
        "3.12",
        "3.13",
        "3.14",
    }:
        raise ContractError("qualification cell is outside the reviewed fixture matrix")
    directory.mkdir(parents=True, exist_ok=True)
    repodata = read_json("https://conda.anaconda.org/uibcdf/noarch/repodata.json")
    old_name = f"{PACKAGE}-{OLD_VERSION}-py_0.tar.bz2"
    new_name = f"{PACKAGE}-{NEW_VERSION}-py_0.tar.bz2"
    for version, filename, digest in (
        (OLD_VERSION, old_name, OLD_DIGEST),
        (NEW_VERSION, new_name, NEW_DIGEST),
    ):
        release = read_json(
            f"https://api.anaconda.org/release/uibcdf/{PACKAGE}/{version}"
        )
        verify_snapshot(release, repodata, PACKAGE, version, "noarch", filename, digest)
    old_record = repodata["packages"][old_name]
    new_record = repodata["packages"][new_name]
    channel = directory / "channel"
    for label, records in (
        ("", {old_name: old_record}),
        ("label/staging", {new_name: new_record}),
    ):
        for subdir in ("noarch", platform):
            write_index(
                channel / "uibcdf" / label / subdir,
                subdir,
                records if subdir == "noarch" else {},
            )
    download(channel / "uibcdf/noarch", dict(plan, version=OLD_VERSION), OLD_DIGEST)
    archive = download(directory / "candidate", plan, NEW_DIGEST)
    server = http.server.ThreadingHTTPServer(
        ("127.0.0.1", 0), functools.partial(QuietHandler, directory=str(channel))
    )
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    configuration = directory / "frozen-public.yaml"
    configuration.write_text(
        yaml.safe_dump(
            {
                "channel_priority": "strict",
                "custom_channels": {"uibcdf": f"http://127.0.0.1:{server.server_port}"},
            }
        )
    )
    previous = os.environ.get("CONDARC")
    os.environ["CONDARC"] = str(configuration)
    arguments = [
        "conda",
        "install",
        "--yes",
        "--prefix",
        sys.prefix,
        "--override-channels",
        "--strict-channel-priority",
        "-c",
        "uibcdf",
        "-c",
        "conda-forge",
    ]
    try:
        configured = json.loads(
            subprocess.check_output(
                ["conda", "config", "--show", "custom_channels", "--json"], text=True
            )
        )
        expected_channel = f"http://127.0.0.1:{server.server_port}/uibcdf"
        actual_channel = configured.get("custom_channels", {}).get("uibcdf")
        if isinstance(actual_channel, dict):
            actual_channel = f"{actual_channel.get('scheme')}://{actual_channel.get('location')}/{actual_channel.get('name')}"
        if actual_channel not in {
            expected_channel,
            expected_channel.removesuffix("/uibcdf"),
        }:
            raise ContractError(
                f"the isolated frozen channel override was not applied: configured={actual_channel!r}"
            )
        subprocess.run(
            [*arguments, f"python={python}", f"{PACKAGE}=={OLD_VERSION}"], check=True
        )
        if importlib.metadata.version(PACKAGE) != OLD_VERSION:
            raise ContractError("the older public fixture was not actually installed")
        visible = subprocess.run(
            [
                "conda",
                "search",
                "--override-channels",
                "-c",
                "uibcdf/label/staging",
                "--json",
                f"{PACKAGE}=={NEW_VERSION}",
            ],
            check=True,
            capture_output=True,
            text=True,
            timeout=300,
        )
        observed = json.loads(visible.stdout).get(PACKAGE)
        if (
            not isinstance(observed, list)
            or len(observed) != 1
            or observed[0].get("sha256") != NEW_DIGEST
        ):
            raise ContractError(
                "the lower-priority staged fixture is not independently visible"
            )
        masked = subprocess.run(
            [
                *arguments,
                "-c",
                "uibcdf/label/staging",
                "--dry-run",
                "--json",
                f"python={python}",
                f"{PACKAGE}=={NEW_VERSION}",
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=300,
        )
        try:
            failure = json.loads(masked.stdout)
        except ValueError as error:
            raise ContractError(
                "strict-priority negative probe returned no structured solve evidence: "
                f"returncode={masked.returncode}, stdout={masked.stdout[:300]!r}, stderr={masked.stderr[:300]!r}"
            ) from error
        if masked.returncode == 0 or failure.get("exception_name") not in {
            "LibMambaUnsatisfiableError",
            "UnsatisfiableError",
            "PackagesNotFoundError",
        }:
            raise ContractError(
                "the lower-priority staged candidate was not excluded by the real solver: "
                f"returncode={masked.returncode}, result={json.dumps(failure)[:800]}"
            )
        # Frozen catalogs exercise the historical selection failure. The positive
        # provider call uses its actual ordinary channels and real staged URL.
        if previous is None:
            os.environ.pop("CONDARC", None)
        else:
            os.environ["CONDARC"] = previous
        installed = install_artifact(archive, plan, inventory, NEW_DIGEST, python)
        provenance = verify_installed(root, plan, inventory, archive, platform, python)
        # Execute a provider smoke outside both source trees using the real plugin.
        smoke = directory / "test_installed_provider.py"
        smoke.write_text(
            "import importlib.metadata, pathlib, sys\nimport pytest_receptor\ndef test_installed_provider():\n    assert importlib.metadata.version('pytest-receptor') == '1.2.1'\n    assert pathlib.Path(pytest_receptor.__file__).resolve().is_relative_to(pathlib.Path(sys.prefix))\n"
        )
        environment = dict(os.environ)
        environment.pop("PYTHONSAFEPATH", None)
        subprocess.run(
            [
                sys.executable,
                "-P",
                "-m",
                "pytest",
                "--import-mode=importlib",
                "--receptor=ci",
                str(smoke),
            ],
            cwd=directory,
            env=environment,
            check=True,
        )
        return {
            "schema": "molsyssuite.noarch-install-qualification@1",
            "state": "verified",
            "platform": platform,
            "python": python,
            "producer_sha": SOURCE,
            "old_public": {"version": OLD_VERSION, "sha256": OLD_DIGEST},
            "masked_named_solve": {
                "returncode": masked.returncode,
                "exception_name": failure["exception_name"],
            },
            "exact_install": installed,
            "provenance": provenance,
            "scientific_suite_executed": False,
            "registry_mutation_performed": False,
            "fixture_scope": "Frozen local public/staging catalogs use verified real public metadata; exact candidate URL is the real registered staging file. Both real files are now public; no live staging-only release is claimed.",
        }
    finally:
        if previous is None:
            os.environ.pop("CONDARC", None)
        else:
            os.environ["CONDARC"] = previous
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--platform", required=True)
    parser.add_argument("--python", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(
        prefix="noarch-provider-qualification-"
    ) as temporary:
        try:
            result = qualify(
                args.root.resolve(), args.platform, args.python, Path(temporary)
            )
            outcome = 0
        except (
            ValueError,
            KeyError,
            TypeError,
            OSError,
            subprocess.SubprocessError,
        ) as error:
            result = {
                "schema": "molsyssuite.noarch-install-qualification@1",
                "state": "unverified",
                "error": str(error)[:1000],
                "registry_mutation_performed": False,
            }
            outcome = 1
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, separators=(",", ":")))
    return outcome


if __name__ == "__main__":
    raise SystemExit(main())
