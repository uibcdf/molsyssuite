"""Resolve runtime roots and check loaded imports without importing optional addons."""

from __future__ import annotations

import sys
from pathlib import Path, PurePosixPath

try:
    from devtools.scripts.noarch_conda import ContractError
except ModuleNotFoundError:
    from noarch_conda import ContractError


def _import_name(value: object) -> bool:
    return isinstance(value, str) and all(
        part.isidentifier() for part in value.split(".")
    )


def runtime_import_roots(inventory: dict, default_import: str) -> tuple[str, ...]:
    """Cover the primary import and Python roots in the reviewed resource inventory.

    An optional explicit import_roots list may add namespace roots, but cannot
    remove the primary import or roots owning declared Python files. Data-only
    paths do not imply an import. Legacy inventories retain their primary root.
    """
    primary = inventory.get("import_name", default_import)
    if not _import_name(primary):
        raise ContractError("installed primary import needs a Python module name")
    required = [primary]
    paths = inventory.get("required_paths", [])
    if not isinstance(paths, list) or any(not isinstance(p, str) for p in paths):
        raise ContractError("installed import roots need a literal resource inventory")
    for path in paths:
        parts = PurePosixPath(path).parts
        if not parts or parts[0] != "site-packages" or ".." in parts:
            raise ContractError("installed import resources must stay in site-packages")
        if len(parts) >= 2 and parts[-1].endswith((".py", ".pyi")):
            name = PurePosixPath(parts[1]).stem if len(parts) == 2 else parts[1]
            if not _import_name(name):
                raise ContractError(
                    "Python payload needs an explicit valid import root"
                )
            if name not in required:
                required.append(name)
    roots = inventory.get("import_roots", required)
    if (
        not isinstance(roots, list)
        or not roots
        or len(roots) > 64
        or any(not _import_name(name) for name in roots)
        or len(roots) != len(set(roots))
    ):
        raise ContractError(
            "import_roots needs unique Python module names (at most 64)"
        )
    if not set(required).issubset(roots):
        raise ContractError(
            "import_roots cannot omit primary or declared Python payload"
        )
    return tuple(roots)


def check_installed_imports(roots: tuple[str, ...], prefix: Path, source: Path) -> dict:
    """Check loaded roots/descendants and every package search location.

    Origins must resolve inside the installed prefix and outside the source
    checkout, including symlink targets and namespace-package paths. Unloaded
    optional integrations are not imported or claimed as tested. This is runtime
    origin evidence, not an archive-byte check or tamper-proof attestation.
    """
    if (
        not isinstance(roots, (tuple, list))
        or not roots
        or len(roots) > 64
        or any(not _import_name(name) for name in roots)
        or len(roots) != len(set(roots))
    ):
        raise ContractError("installed import check needs declared module roots")
    prefix, source = prefix.resolve(), source.resolve()
    checked = []
    for name, module in tuple(sys.modules.items()):
        if not any(name == root or name.startswith(root + ".") for root in roots):
            continue
        filename = getattr(module, "__file__", None)
        locations = []
        if filename:
            locations.append(filename)
        package_paths = getattr(module, "__path__", ())
        try:
            if isinstance(package_paths, (str, bytes)):
                raise TypeError("package locations need separate paths")
            locations.extend(package_paths)
            if not locations:
                raise TypeError("loaded module has no file or package origin")
            resolved = [Path(location).resolve() for location in locations]
        except (TypeError, ValueError, OSError) as error:
            raise ContractError(
                f"loaded runtime import has no valid origin: {name}"
            ) from error
        if any(
            not path.is_relative_to(prefix) or path.is_relative_to(source)
            for path in resolved
        ):
            raise ContractError(
                f"runtime import is outside the installed environment or from source: {name}"
            )
        checked.append(name)
    return {
        "state": "verified-loaded-imports",
        "roots": list(roots),
        "loaded": sorted(checked),
    }
