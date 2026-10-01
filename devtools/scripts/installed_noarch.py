"""Download and qualify one reviewed noarch artifact outside a source checkout."""

from __future__ import annotations

import argparse
import hashlib
import importlib
import importlib.metadata
import json
import platform
import re
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen

import tomllib

try:
    from devtools.scripts.noarch_conda import (
        ContractError,
        inspect_artifact,
        inspect_recipe,
        local_path,
        promotion_descriptor,
    )
except ModuleNotFoundError:
    from noarch_conda import (
        ContractError,
        inspect_artifact,
        inspect_recipe,
        local_path,
        promotion_descriptor,
    )

RUNNERS = {
    "linux-64": "ubuntu-latest",
    "linux-aarch64": "ubuntu-24.04-arm",
    "osx-arm64": "macos-15",
    "win-64": "windows-latest",
}
IDENTITIES = {
    "linux-64": ("linux", {"x86_64", "amd64"}),
    "linux-aarch64": ("linux", {"aarch64", "arm64"}),
    "osx-arm64": ("darwin", {"arm64", "aarch64"}),
    "win-64": ("win32", {"amd64", "x86_64"}),
}


def prepare(
    root: Path, plan: dict, inventory: dict, candidate: str, filename: str, digest: str
) -> dict:
    """Bind an explicit dispatch to the plan, source and full installed matrix."""
    checkout = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=root, text=True
    ).strip()
    if not re.fullmatch(r"[0-9a-f]{40}", candidate) or checkout != candidate:
        raise ContractError(
            "installed qualification needs the exact reviewed checkout SHA"
        )
    descriptor = promotion_descriptor(root, plan, inventory, digest)
    if filename != descriptor["filename"]:
        raise ContractError(
            "selected installed file differs from the reviewed coordinate"
        )
    profile = json.loads(descriptor["profile"])
    if (
        profile["prepare_job"] != "installed / prepare"
        or profile["job_template"] != "installed / {platform} · Python {python}"
        or profile["required_steps"]
        != ["Install exact artifact", "Validate installed files", "Run installed tests"]
    ):
        raise ContractError(
            "installed descriptor differs from this reusable workflow's executed jobs/steps"
        )
    if any(target not in RUNNERS for target in plan["test_platforms"]):
        raise ContractError("installed target needs a reviewed runner profile")
    matrix = {
        "include": [
            {"platform": target, "python": python, "runner": RUNNERS[target]}
            for target in plan["test_platforms"]
            for python in plan["python_versions"]
        ]
    }
    return dict(
        descriptor,
        matrix=json.dumps(matrix),
        candidate_sha=candidate,
        sha256=digest,
        build_number=plan["build_number"],
    )


def download(directory: Path, plan: dict, digest: str) -> Path:
    """Download a bounded immutable coordinate and verify bytes before install."""
    if not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise ContractError("download requires an exact artifact digest")
    filename = f"{plan['package']}-{plan['version']}-py_{plan['build_number']}.tar.bz2"
    target = directory / filename
    url = f"https://api.anaconda.org/download/uibcdf/{plan['package']}/{plan['version']}/noarch/{filename}"
    directory.mkdir(parents=True, exist_ok=True)
    size, calculated = 0, hashlib.sha256()
    with urlopen(url, timeout=30) as response, target.open("wb") as stream:
        while contents := response.read(1024 * 1024):
            size += len(contents)
            if size > 1024**3:
                raise ContractError("artifact download exceeds 1 GiB")
            calculated.update(contents)
            stream.write(contents)
    if calculated.hexdigest() != digest:
        raise ContractError("downloaded bytes differ from the installed-gate digest")
    return target


def verify_installed(
    root: Path, plan: dict, inventory: dict, artifact: Path, target: str, python: str
) -> dict:
    """Verify platform, distribution, runtime import, resources and launchers."""
    if (
        target not in plan["test_platforms"]
        or python not in plan["python_versions"]
        or target not in IDENTITIES
    ):
        raise ContractError("installed cell is not in the reviewed matrix")
    system, architectures = IDENTITIES[target]
    if (
        sys.platform != system
        or platform.machine().lower() not in architectures
        or f"{sys.version_info.major}.{sys.version_info.minor}" != python
    ):
        raise ContractError(
            "interpreter/architecture differs from the declared installed cell"
        )
    distribution = importlib.metadata.distribution(plan["package"])
    if distribution.version != plan["version"]:
        raise ContractError("installed distribution version differs from the candidate")
    prefix, source = Path(sys.prefix).resolve(), root.resolve()
    filename = f"{plan['package']}-{plan['version']}-py_{plan['build_number']}.tar.bz2"
    with artifact.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    records = list((prefix / "conda-meta").glob("*.json"))
    if not records:
        raise ContractError("installed Conda provenance is missing")
    found = False
    for record_path in records:
        record = json.loads(record_path.read_text())
        url = urlparse(record.get("url", ""))
        if record.get("name") == plan["package"]:
            found = True
            if (
                record.get("version") != plan["version"]
                or record.get("build") != f"py_{plan['build_number']}"
                or record.get("sha256") != digest
                or url.hostname != "conda.anaconda.org"
                or url.path != f"/uibcdf/label/staging/noarch/{filename}"
            ):
                raise ContractError(
                    "installed Conda coordinate/digest is not the exact staged file"
                )
        elif (
            url.scheme != "https"
            or url.hostname != "conda.anaconda.org"
            or url.path.split("/")[1:2] not in (["uibcdf"], ["conda-forge"])
            or "/label/" in url.path
        ):
            raise ContractError(
                "installed dependency is not from an ordinary declared public channel"
            )
    if not found:
        raise ContractError("installed candidate Conda record is missing")
    with tarfile.open(artifact, "r:bz2") as archive:
        for name in inventory["required_paths"]:
            path = Path(
                distribution.locate_file(name.removeprefix("site-packages/"))
            ).resolve()
            if (
                not path.is_relative_to(prefix)
                or path.is_relative_to(source)
                or not path.is_file()
            ):
                raise ContractError(
                    "installed resource is missing, editable or outside its environment"
                )
            with archive.extractfile(name) as original, path.open("rb") as installed:
                if (
                    hashlib.file_digest(original, "sha256").hexdigest()
                    != hashlib.file_digest(installed, "sha256").hexdigest()
                ):
                    raise ContractError(
                        f"installed resource differs from the exact artifact: {name}"
                    )
    module = importlib.import_module(
        inventory.get("import_name", plan["package"].replace("-", "_"))
    )
    module_path = Path(module.__file__).resolve()
    if (
        not module_path.is_relative_to(prefix)
        or module_path.is_relative_to(source)
        or module.__version__ != plan["version"]
    ):
        raise ContractError("runtime import is from source or has a stale version")
    metadata = tomllib.loads(local_path(root, "pyproject.toml").read_text())
    for command in metadata["project"].get("scripts", {}):
        executable = shutil.which(command)
        if not executable or not Path(executable).resolve().is_relative_to(prefix):
            raise ContractError(
                "installed console launcher is missing or outside its environment"
            )
    return {
        "state": "verified",
        "platform": target,
        "python": python,
        "version": plan["version"],
    }


def run_tests(root: Path, inventory: dict) -> int:
    """Execute the component's declared selection with imports outside source."""
    selection = inventory.get("installed_tests", {})
    paths, args = selection.get("paths"), selection.get("pytest_args", [])
    if (
        not isinstance(paths, list)
        or not paths
        or any(not isinstance(p, str) or not p for p in paths)
        or not isinstance(args, list)
        or any(not isinstance(arg, str) or not arg or "\n" in arg for arg in args)
    ):
        raise ContractError(
            "installed scientific selection must be declared by the component"
        )
    targets = []
    for relative in paths:
        path = (root / relative).resolve()
        if (
            not path.is_relative_to(root.resolve())
            or not path.exists()
            or Path(relative).is_absolute()
        ):
            raise ContractError("installed test selection escapes its component")
        targets.append(str(path))
    if Path.cwd().resolve().is_relative_to(root.resolve()):
        raise ContractError("installed tests must execute outside the source checkout")
    import pytest

    class InstalledProvenance:
        executed = 0

        def pytest_runtest_logreport(self, report):
            if report.when == "call" and report.outcome in {"passed", "failed"}:
                self.executed += 1

        def check(self):
            prefix = Path(sys.prefix).resolve()
            module_name = inventory.get("import_name", root.name.replace("-", "_"))
            importlib.import_module(module_name)
            for name, module in tuple(sys.modules.items()):
                if name == module_name or name.startswith(module_name + "."):
                    filename = getattr(module, "__file__", None)
                    if filename and (
                        not Path(filename).resolve().is_relative_to(prefix)
                        or Path(filename).resolve().is_relative_to(root.resolve())
                    ):
                        raise ContractError(
                            "scientific tests imported component code outside the installed environment"
                        )

        def pytest_sessionstart(self, session):
            self.check()

        def pytest_sessionfinish(self, session, exitstatus):
            self.check()

    # Import-mode avoids inserting component source while collecting its tests.
    # Hooks verify the actual imports in this same interpreter, before and after.
    guard = InstalledProvenance()
    result = pytest.main(["--import-mode=importlib", *args, *targets], plugins=[guard])
    if result == 0 and guard.executed == 0:
        raise ContractError("installed selection executed no tests")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("prepare", "download", "verify", "tests"))
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--candidate-sha")
    parser.add_argument("--filename")
    parser.add_argument("--sha256")
    parser.add_argument("--directory", type=Path)
    parser.add_argument("--platform")
    parser.add_argument("--python")
    parser.add_argument("--github-output", type=Path)
    args = parser.parse_args()
    try:
        root = args.root.resolve()
        plan, inventory = inspect_recipe(
            root,
            "devtools/conda-build/release_plan.toml",
            "devtools/conda-build/resources.toml",
        )
        if args.operation == "prepare":
            result = prepare(
                root, plan, inventory, args.candidate_sha, args.filename, args.sha256
            )
        elif args.operation == "download":
            artifact = download(args.directory, plan, args.sha256)
            result = inspect_artifact(artifact, plan, inventory)
        elif args.operation == "verify":
            artifact = args.directory / args.filename
            proof = inspect_artifact(artifact, plan, inventory)
            if proof["sha256"] != args.sha256:
                raise ContractError(
                    "local installed artifact differs from the declared digest"
                )
            result = dict(
                proof,
                **verify_installed(
                    root, plan, inventory, artifact, args.platform, args.python
                ),
            )
        else:
            return run_tests(root, inventory)
        if args.github_output:
            with args.github_output.open("a") as stream:
                for key, value in result.items():
                    stream.write(f"{key}={value}\n")
        print(json.dumps(result, sort_keys=True))
        return 0
    except (
        ValueError,
        OSError,
        KeyError,
        TypeError,
        tarfile.TarError,
        subprocess.CalledProcessError,
    ) as error:
        print(f"Installed noarch gate rejected: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
