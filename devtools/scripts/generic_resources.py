"""Receive a bounded generic ESM/declaration payload without Python installation."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import tarfile
from pathlib import Path, PurePosixPath

if __package__:
    from .conda_release_contract import VERSION, ContractError, validate_plan
else:
    from conda_release_contract import VERSION, ContractError, validate_plan


def inspect_payload(files: dict[str, bytes], package: str, version: str) -> dict:
    """Require complete exact file hashes, public entries and no native/Python payload."""
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", package):
        raise ContractError("generic package identity is not canonical")
    prefix = f"share/{package}/"
    if (
        not files
        or len(files) > 10000
        or sum(map(len, files.values())) > 256 * 1024 * 1024
    ):
        raise ContractError("generic resource payload exceeds its bounded profile")
    if any(not name.startswith(prefix) for name in files):
        raise ContractError(
            "generic files must stay below the declared share resource root"
        )
    payload = {name.removeprefix(prefix): data for name, data in files.items()}
    for name, data in payload.items():
        path = PurePosixPath(name)
        if (
            path.is_absolute()
            or ".." in path.parts
            or str(path) != name
            or "\\" in name
        ):
            raise ContractError("generic resource path is not canonical")
        if (
            path.suffix.lower()
            in {
                ".py",
                ".pyc",
                ".so",
                ".pyd",
                ".dll",
                ".dylib",
                ".exe",
                ".node",
                ".a",
                ".lib",
            }
            or data[:4]
            in {
                b"\x7fELF",
                b"\xfe\xed\xfa\xce",
                b"\xce\xfa\xed\xfe",
                b"\xfe\xed\xfa\xcf",
                b"\xcf\xfa\xed\xfe",
                b"\xca\xfe\xba\xbe",
            }
            or data.startswith(b"MZ")
        ):
            raise ContractError(
                "generic profile cannot conceal native or Python payload"
            )
    try:
        manifest = json.loads(payload["asset-manifest.json"])
        metadata = json.loads(payload["package.json"])
        rows = manifest["files"]
    except (KeyError, TypeError, ValueError) as error:
        raise ContractError("generic asset/package metadata is unavailable") from error
    if (
        not isinstance(manifest, dict)
        or not isinstance(metadata, dict)
        or not isinstance(rows, list)
    ):
        raise ContractError("generic asset metadata has invalid shape")
    if (
        not VERSION.fullmatch(version)
        or manifest.get("version") != version
        or metadata.get("version") != version
        or metadata.get("name") != "@uibcdf/" + package
    ):
        raise ContractError("generic package, manifest and candidate identities differ")
    if (
        manifest.get("schemaVersion") != 1
        or manifest.get("package") != package
        or metadata.get("type") != "module"
        or not metadata.get("license")
        or "LICENSE" not in payload
    ):
        raise ContractError(
            "generic ESM payload needs schema, license and module identity"
        )
    if metadata.get("devDependencies"):
        raise ContractError("development tooling cannot become generic runtime payload")
    expected = {}
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"path", "sha256"}:
            raise ContractError("asset manifest needs exact path/hash rows")
        name, digest = row["path"], row["sha256"]
        if (
            not isinstance(name, str)
            or name in expected
            or not re.fullmatch(r"[0-9a-f]{64}", str(digest))
        ):
            raise ContractError("asset paths/hashes are ambiguous")
        expected[name] = digest
    actual = {
        name: hashlib.sha256(data).hexdigest()
        for name, data in payload.items()
        if name != "asset-manifest.json"
    }
    if expected != actual:
        raise ContractError("complete asset manifest differs from actual payload bytes")
    exports = metadata.get("exports", {})
    if isinstance(exports, dict) and "." in exports:
        exports = exports["."]
    if not isinstance(exports, dict):
        raise ContractError("generic public exports must name import and types")
    for key, suffix in (("import", ".js"), ("types", ".d.ts")):
        entry = exports.get(key, "")
        if (
            not isinstance(entry, str)
            or not entry.startswith("./")
            or not entry.endswith(suffix)
            or entry[2:] not in actual
        ):
            raise ContractError(
                "generic public entry point is missing or outside exact assets"
            )
    return {
        "schema": "molsyssuite.generic-resources@1",
        "state": "verified",
        "package": package,
        "version": version,
        "files": actual,
        "resource_root": prefix.removesuffix("/"),
        "scope": "asset identity only; execute the independent installed consumer and native host gates separately",
    }


def inspect_prefix(prefix: Path, package: str, version: str) -> dict:
    """Receive a relocated installed resource root without executing package code."""
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", package):
        raise ContractError("generic package identity is not canonical")
    prefix = prefix.resolve()
    root = prefix / "share" / package
    if not root.is_dir() or root.is_symlink() or root.resolve() != root:
        raise ContractError("installed generic resource root is unavailable")
    files = {}
    paths = list(root.rglob("*"))
    if (
        len(paths) > 10000
        or sum(p.stat().st_size for p in paths if p.is_file()) > 256 * 1024 * 1024
    ):
        raise ContractError("installed generic inventory exceeds bounds")
    for path in paths:
        if path.is_symlink():
            raise ContractError("generic payload cannot use symlink aliases")
        if path.is_file():
            files[path.relative_to(prefix).as_posix()] = path.read_bytes()
    return inspect_payload(files, package, version)


def inspect_artifact(path: Path, plan: dict) -> dict:
    """Inspect one original noarch generic tar.bz2 with no extraction or code execution."""
    validate_plan(plan)
    if plan["profile"] != "generic-resources":
        raise ContractError("generic inspector needs its explicit artifact profile")
    name = f"{plan['package']}-{plan['version']}-res_{plan['build_number']}.tar.bz2"
    if path.name != name:
        raise ContractError("generic archive differs from its exact coordinate")
    files = {}
    with tarfile.open(path, "r:bz2") as archive:
        members = archive.getmembers()
        if (
            len(members) > 10000
            or len({m.name for m in members}) != len(members)
            or sum(m.size for m in members) > 256 * 1024 * 1024
        ):
            raise ContractError(
                "generic archive inventory is duplicated or exceeds bounds"
            )
        for member in members:
            p = PurePosixPath(member.name)
            if (
                p.is_absolute()
                or ".." in p.parts
                or "\\" in member.name
                or str(p) != member.name
                or not (member.isfile() or member.isdir())
            ):
                raise ContractError("generic archive has unsafe or linked members")
            if member.isfile():
                files[member.name] = archive.extractfile(member).read()
        try:
            index = json.loads(files["info/index.json"])
        except (KeyError, ValueError) as error:
            raise ContractError("generic archive metadata is unavailable") from error
        if not isinstance(index, dict):
            raise ContractError("generic archive metadata must be an object")
        if "info/link.json" in files:
            try:
                link = json.loads(files["info/link.json"])
                noarch = link.get("noarch", {}) if isinstance(link, dict) else None
            except ValueError as error:
                raise ContractError("generic install metadata is malformed") from error
            if not isinstance(noarch, dict) or noarch.get("type") not in (
                None,
                "generic",
            ):
                raise ContractError(
                    "generic install metadata contradicts noarch generic"
                )
        expected = {
            "name": plan["package"],
            "version": plan["version"],
            "build": f"res_{plan['build_number']}",
            "build_number": plan["build_number"],
            "subdir": "noarch",
            "noarch": "generic",
        }
        if any(index.get(k) != v for k, v in expected.items()) or any(
            re.match(r"(?:python|python_abi)(?:\s|$)", str(dep))
            for dep in index.get("depends", [])
        ):
            raise ContractError(
                "generic archive identity/noarch/runtime profile differs"
            )
    result = inspect_payload(
        {k: v for k, v in files.items() if not k.startswith("info/")},
        plan["package"],
        plan["version"],
    )
    result.update(filename=name, sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prefix", type=Path)
    parser.add_argument("--package", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = inspect_prefix(args.prefix.resolve(), args.package, args.version)
    except (OSError, ValueError, TypeError, tarfile.TarError) as error:
        print(f"generic resource receiving failed: {error}")
        return 1
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(result, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
