"""Receive console commands from one exact public noarch file; no scientific gate."""

from __future__ import annotations

import argparse
import hashlib
import importlib
import importlib.metadata
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    from devtools.scripts.verify_public_conda import (
        VerificationError,
        validate_coordinate,
        verify_public,
    )
except ModuleNotFoundError:
    from verify_public_conda import (
        VerificationError,
        validate_coordinate,
        verify_public,
    )

RUNNERS = {
    "linux-64": "ubuntu-latest",
    "osx-arm64": "macos-15",
    "win-64": "windows-latest",
}
IDENTITIES = {
    "linux-64": ("linux", {"x86_64", "amd64"}),
    "osx-arm64": ("darwin", {"arm64", "aarch64"}),
    "win-64": ("win32", {"amd64", "x86_64"}),
}


def verify_cell(target: str, python: str, prefix: Path) -> None:
    """Reject a wrong prefix/platform/interpreter before any installation."""
    if target not in IDENTITIES:
        raise ValueError("unsupported receiving platform")
    system, architectures = IDENTITIES[target]
    if (
        sys.platform != system
        or platform.machine().lower() not in architectures
        or f"{sys.version_info.major}.{sys.version_info.minor}" != python
        or prefix.resolve() != Path(sys.prefix).resolve()
        or Path.cwd().resolve().is_relative_to(Path(__file__).resolve().parents[2])
    ):
        raise ValueError(
            "use the explicit active prefix and actual cell outside source"
        )


def matrix(platforms: list[str]) -> dict:
    """Resolve a selected subset of the documented three-platform profile."""
    if (
        not isinstance(platforms, list)
        or not 1 <= len(platforms) <= len(RUNNERS)
        or any(not isinstance(item, str) or item not in RUNNERS for item in platforms)
        or len(platforms) != len(set(platforms))
    ):
        raise ValueError("platforms need a unique nonempty supported list")
    return {
        "include": [{"platform": item, "runner": RUNNERS[item]} for item in platforms]
    }


def inspect_archive(artifact: Path, coordinate: dict) -> dict:
    """Inspect a digest-bound public tar.bz2, without extracting its payload."""
    validate_coordinate(**coordinate)
    if coordinate["subdir"] != "noarch" or not re.fullmatch(
        re.escape(f"{coordinate['package']}-{coordinate['version']}-")
        + r"py_[0-9]+\.tar\.bz2",
        coordinate["filename"],
    ):
        raise ValueError("command receiving supports noarch py_N tar.bz2 files")
    with artifact.open("rb") as stream:
        if hashlib.file_digest(stream, "sha256").hexdigest() != coordinate["sha256"]:
            raise ValueError("downloaded archive digest differs")
    with tarfile.open(artifact, "r:bz2") as archive:
        docs = {}
        for name in ("info/index.json", "info/link.json"):
            members = [item for item in archive.getmembers() if item.name == name]
            if len(members) != 1 or not members[0].isfile() or members[0].size > 65536:
                raise ValueError("archive identity metadata is missing or ambiguous")
            with archive.extractfile(members[0]) as stream:
                docs[name] = json.load(stream)
    index, link = docs["info/index.json"], docs["info/link.json"]
    if (
        not isinstance(index, dict)
        or not isinstance(link, dict)
        or not isinstance(link.get("noarch"), dict)
    ):
        raise TypeError("archive metadata needs identity objects")
    build = coordinate["filename"][
        len(f"{coordinate['package']}-{coordinate['version']}-") : -8
    ]
    if (
        index.get("name") != coordinate["package"]
        or index.get("version") != coordinate["version"]
        or index.get("build") != build
        or index.get("build_number") != int(build[3:])
        or type(index.get("build_number")) is not int
        or index.get("subdir") != "noarch"
        or index.get("noarch") != "python"
        or link.get("noarch", {}).get("type") != "python"
    ):
        raise ValueError("archive identity or noarch type differs")
    dependencies = index.get("depends")
    if (
        not isinstance(dependencies, list)
        or not 1 <= len(dependencies) <= 100
        or any(
            not isinstance(item, str)
            or not item
            or len(item) > 256
            or any(c in item for c in "\r\n:/")
            or item.startswith("-")
            for item in dependencies
        )
    ):
        raise ValueError("dependencies need bounded ordinary Conda specs")
    entries = link["noarch"].get("entry_points")
    if not isinstance(entries, list) or not 1 <= len(entries) <= 64:
        raise ValueError("archive needs explicit console entry points")
    scripts = {}
    for entry in entries:
        match = re.fullmatch(
            r"([A-Za-z0-9][A-Za-z0-9_.-]*)\s*=\s*"
            r"([A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*:[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*)",
            entry if isinstance(entry, str) else "",
        )
        if not match or match[1] in scripts:
            raise ValueError("console entry points are invalid or duplicated")
        scripts[match[1]] = match[2]
    return {"build": build, "dependencies": dependencies, "scripts": scripts}


def verify_commands(
    coordinate: dict,
    inspected: dict,
    artifact: Path,
    target: str,
    python: str,
    prefix: Path,
) -> dict:
    """Verify the actual installed file/origins, then execute all declared help commands."""
    verify_cell(target, python, prefix)
    if inspect_archive(artifact, coordinate) != inspected:
        raise ValueError("command selection differs from exact archive metadata")
    prefix = prefix.resolve()
    provider = Path(__file__).resolve().parents[2]
    if prefix != Path(sys.prefix).resolve() or Path.cwd().resolve().is_relative_to(
        provider
    ):
        raise ValueError("use the explicit active prefix outside provider source")
    record_path = (
        prefix
        / "conda-meta"
        / (f"{coordinate['package']}-{coordinate['version']}-{inspected['build']}.json")
    )
    record = json.loads(record_path.read_text())
    url = f"https://conda.anaconda.org/uibcdf/noarch/{coordinate['filename']}"
    if any(
        record.get(key) != value
        for key, value in {
            "name": coordinate["package"],
            "version": coordinate["version"],
            "build": inspected["build"],
            "subdir": "noarch",
            "sha256": coordinate["sha256"],
            "url": url,
        }.items()
    ):
        raise ValueError("installed Conda record differs from exact public file")
    distribution = importlib.metadata.distribution(coordinate["package"])
    entries = list(distribution.entry_points.select(group="console_scripts"))
    if (
        distribution.version != coordinate["version"]
        or len(entries) != len(inspected["scripts"])
        or {item.name: item.value for item in entries} != inspected["scripts"]
    ):
        raise ValueError("installed distribution version or command metadata differs")
    outcomes = []
    environment = dict(os.environ, PYTHONSAFEPATH="1")
    environment.pop("PYTHONPATH", None)
    environment.pop("PYTHONHOME", None)
    with tarfile.open(artifact, "r:bz2") as archive:
        for entry in entries:
            module = importlib.import_module(entry.value.split(":", 1)[0])
            origin = Path(module.__file__).resolve()
            if not origin.is_relative_to(prefix) or origin.is_relative_to(provider):
                raise ValueError("command module is outside installed prefix")
            relative = entry.value.split(":", 1)[0].replace(".", "/")
            relative += "/__init__.py" if origin.name == "__init__.py" else ".py"
            if origin != Path(distribution.locate_file(relative)).resolve():
                raise ValueError("command module differs from distribution origin")
            with (
                archive.extractfile("site-packages/" + relative) as original,
                origin.open("rb") as installed,
            ):
                if (
                    hashlib.file_digest(original, "sha256").digest()
                    != hashlib.file_digest(installed, "sha256").digest()
                ):
                    raise ValueError(
                        "installed command module differs from original archive"
                    )
            launcher = shutil.which(entry.name)
            if not launcher or not Path(launcher).resolve().is_relative_to(prefix):
                raise ValueError(
                    "command launcher is missing or outside installed prefix"
                )
            # Private output handles close even when the command fails or times out.
            with tempfile.TemporaryFile() as stdout, tempfile.TemporaryFile() as stderr:
                result = subprocess.run(
                    [launcher, "--help"],
                    env=environment,
                    stdout=stdout,
                    stderr=stderr,
                    timeout=30,
                    check=False,
                )
                outputs = {}
                for name, stream in (("stdout", stdout), ("stderr", stderr)):
                    stream.seek(0)
                    data = stream.read(65537)
                    if len(data) > 65536:
                        raise ValueError("command output exceeds receiving bound")
                    outputs[name] = {
                        "bytes": len(data),
                        "sha256": hashlib.sha256(data).hexdigest(),
                    }
                if result.returncode != 0:
                    raise ValueError(
                        f"installed command {entry.name} --help failed ({result.returncode})"
                    )
            outcomes.append(
                {
                    "command": entry.name,
                    "target": entry.value,
                    "launcher": launcher,
                    "module_origin": str(origin),
                    "exit_code": result.returncode,
                    **outputs,
                }
            )
    return {
        "platform": target,
        "python": python,
        "prefix": str(prefix),
        "commands": outcomes,
        "installed_record": {
            key: record[key] for key in ("name", "version", "build", "sha256", "url")
        },
    }


def receive(coordinate: dict, target: str, python: str, prefix: Path) -> dict:
    """Install into the explicitly selected disposable prefix; never publish a package."""
    try:
        from devtools.scripts.installed_noarch import conda_command, download
    except ModuleNotFoundError:
        from installed_noarch import conda_command, download
    validate_coordinate(**coordinate)
    if prefix.resolve() != Path(sys.prefix).resolve() or python not in {
        "3.11",
        "3.12",
        "3.13",
        "3.14",
    }:
        raise ValueError(
            "receiving needs an explicit active prefix and supported Python"
        )
    matrix([target])
    verify_cell(target, python, prefix)
    public_url = verify_public(**coordinate)
    match = re.fullmatch(
        re.escape(f"{coordinate['package']}-{coordinate['version']}-")
        + r"py_([0-9]+)\.tar\.bz2",
        coordinate["filename"],
    )
    if not match or coordinate["subdir"] != "noarch":
        raise ValueError("receiving needs a noarch py_N tar.bz2 coordinate")
    # Only task-owned downloaded files are disposable; the explicit environment is caller-owned.
    with tempfile.TemporaryDirectory(prefix="public-noarch-commands-") as temporary:
        artifact = download(
            Path(temporary),
            {
                "package": coordinate["package"],
                "version": coordinate["version"],
                "build_number": int(match[1]),
            },
            coordinate["sha256"],
        )
        inspected = inspect_archive(artifact, coordinate)
        arguments = [
            *conda_command(),
            "install",
            "--yes",
            "--prefix",
            str(prefix),
            "--override-channels",
            "--strict-channel-priority",
            "-c",
            "uibcdf",
            "-c",
            "conda-forge",
        ]
        subprocess.run(
            [*arguments, f"python={python}", *inspected["dependencies"]], check=True
        )
        subprocess.run([*arguments, public_url], check=True)
        proof = verify_commands(coordinate, inspected, artifact, target, python, prefix)
    return {
        "schema": "molsyssuite.public-noarch-commands@1",
        "state": "verified",
        "coordinate": coordinate,
        "public_url": public_url,
        **proof,
        "scope": "Installed console --help only; not full installed/scientific/release qualification",
        "temporary_download_removed": True,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="operation", required=True)
    selected = commands.add_parser("matrix")
    selected.add_argument("--platforms", required=True)
    run = commands.add_parser("receive")
    for key in ("package", "version", "subdir", "filename", "sha256"):
        run.add_argument("--" + key, required=True)
    for key in ("platform", "python", "prefix", "output"):
        run.add_argument("--" + key, required=True)
    args = parser.parse_args(argv)
    if args.operation == "matrix":
        print(json.dumps(matrix(json.loads(args.platforms))))
        return 0
    report = {"schema": "molsyssuite.public-noarch-commands@1", "state": "unverified"}
    try:
        coordinate = {
            key: getattr(args, key)
            for key in ("package", "version", "subdir", "filename", "sha256")
        }
        report = receive(coordinate, args.platform, args.python, Path(args.prefix))
        code = 0
    except (
        VerificationError,
        ImportError,
        ValueError,
        OSError,
        KeyError,
        TypeError,
        tarfile.TarError,
        subprocess.SubprocessError,
    ) as error:
        report["error"] = str(error)[:1000]
        code = 1
    Path(args.output).write_text(json.dumps(report, indent=2) + "\n")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
