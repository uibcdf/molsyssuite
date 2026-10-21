"""Explicit unshipped helper/data inputs for serial installed tests (#117).

No owner or staging parent is added to Python paths. This is origin/input
validation for trusted tests, not a sandbox or installed artifact qualification.
"""

from __future__ import annotations

import hashlib
import importlib
import importlib.machinery
import importlib.util
import json
import keyword
import re
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path, PurePosixPath
from tempfile import TemporaryDirectory

try:
    from devtools.scripts.noarch_conda import ContractError
except ModuleNotFoundError:
    from noarch_conda import ContractError

SCHEMA = "molsyssuite.installed-test-support@1"
MAX_FILES = 1024
MAX_FILE_BYTES = 64 * 1024 * 1024
MAX_TOTAL_BYTES = 256 * 1024 * 1024
CONTEXT_FIELDS = (
    "candidate_sha", "qualification_sha", "provider_sha", "filename", "sha256",
    "run_id", "run_attempt",
)


def _identifier(value: object) -> bool:
    return isinstance(value, str) and bool(
        re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", value)
    ) and not keyword.iskeyword(value)


def _relative(value: object) -> PurePosixPath:
    if not isinstance(value, str) or not value or len(value) > 4096:
        raise ContractError("test support needs bounded literal relative paths")
    path = PurePosixPath(value)
    if (
        not path.parts or path.is_absolute() or path.as_posix() != value or ".." in path.parts
        or any(ord(c) < 32 or c in '\\:<>"|?*' for c in value)
        or any(part.endswith((" ", ".")) or re.fullmatch(
            r"(?i:con|prn|aux|nul|com[1-9]|lpt[1-9])", part.split(".")[0]
        ) for part in path.parts)
    ):
        raise ContractError("test support path is not portable or escapes its owner")
    return path


def _digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def support_plan(root: Path, declaration: dict | None, runtime_roots: tuple[str, ...]) -> dict | None:
    """Validate literal source bytes without writes, imports or namespace binding."""
    if declaration is None:
        return None
    if (
        not isinstance(declaration, dict)
        or set(declaration) != {"schema", "namespace", "reason", "files"}
        or declaration.get("schema") != SCHEMA
        or not isinstance(declaration.get("reason"), str)
        or not declaration["reason"].strip()
    ):
        raise ContractError("test support requires the reviewed @1 declaration")
    namespace = declaration.get("namespace")
    if not isinstance(runtime_roots, (tuple, list)) or not runtime_roots or any(
        not isinstance(name, str) or not all(_identifier(p) for p in name.split("."))
        for name in runtime_roots
    ):
        raise ContractError("test support needs declared runtime roots")
    payload_roots = {name.split(".")[0].casefold() for name in runtime_roots}
    reserved = set(sys.stdlib_module_names) | set(sys.builtin_module_names) | {
        "devtools", "tests", "conftest", "pytest", "_pytest",
    } | payload_roots
    if not _identifier(namespace) or namespace.casefold() in {name.casefold() for name in reserved}:
        raise ContractError("test support namespace collides with runtime/SDK/test tools")
    records = declaration.get("files")
    if not isinstance(records, list) or not 1 <= len(records) <= MAX_FILES:
        raise ContractError("test support requires 1..1024 reviewed files")
    root = root.resolve()
    sources, targets, modules, nonpackages, result = set(), set(), set(), set(), []
    total = 0
    for record in records:
        if not isinstance(record, dict) or set(record) != {"source", "target", "sha256"}:
            raise ContractError("test support file needs source, target and SHA-256")
        source, target = _relative(record["source"]), _relative(record["target"])
        digest = record["sha256"]
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise ContractError("test support file needs a full lowercase SHA-256")
        if source.parts[0].casefold().removesuffix(".py") in payload_roots:
            raise ContractError("runtime payload source cannot become test support")
        if source.as_posix().casefold() in sources or target.as_posix().casefold() in targets:
            raise ContractError("test support has duplicate or case-aliased files")
        sources.add(source.as_posix().casefold()); targets.add(target.as_posix().casefold())
        code = target.suffix == ".py"
        if code:
            parts = list(target.with_suffix("").parts)
            if target.parts[0] != namespace or len(parts) < 2 or any(not _identifier(p) for p in parts):
                raise ContractError("test support Python must belong to its namespace")
            if source.suffix != ".py":
                raise ContractError("test support code cannot be disguised data")
            package = parts[-1] == "__init__"
            module = ".".join(parts[:-1] if package else parts).casefold()
            if module in modules:
                raise ContractError("test support module/package target collision")
            modules.add(module)
            if not package:
                nonpackages.add(module)
        elif any(str(path).lower().endswith(tuple(importlib.machinery.all_suffixes()) + (
            ".pyi", ".pth", ".pyd", ".dll", ".so", ".dylib",
        )) for path in (source, target)):
            raise ContractError("test support data cannot expose executable imports")
        actual = root.joinpath(*source.parts)
        if actual.resolve() != actual or not actual.is_file():
            raise ContractError("test support source is missing or a symlink alias")
        size = actual.stat().st_size
        total += size
        if size > MAX_FILE_BYTES or total > MAX_TOTAL_BYTES:
            raise ContractError("test support size needs an owner-reviewed equivalent")
        if _digest(actual) != digest:
            raise ContractError("test support source digest changed")
        result.append({**record, "bytes": size, "kind": "code" if code else "data"})
    if not modules:
        raise ContractError("test support requires declared Python helpers")
    for target in targets:
        if any(parent.as_posix().casefold() in targets for parent in PurePosixPath(target).parents):
            raise ContractError("test support file/directory target collision")
    for name in modules:
        if any(".".join(name.split(".")[:i]) in nonpackages for i in range(1, len(name.split(".")))):
            raise ContractError("test support module/package target collision")
    identity = hashlib.sha256(json.dumps(declaration, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return {"schema": SCHEMA, "namespace": namespace, "reason": declaration["reason"],
            "files": result, "bytes": total, "declaration_sha256": identity}


def _available(namespace: str) -> None:
    if any(name == namespace or name.startswith(namespace + ".") for name in sys.modules):
        raise ContractError("test support namespace is already loaded")
    if importlib.util.find_spec(namespace) is not None:
        raise ContractError("test support namespace is already resolvable")


def check_unshipped_support(namespace: str, payload_paths: list[str]) -> None:
    """Reject the dedicated support namespace in inspected Python payload paths."""
    if not _identifier(namespace):
        raise ContractError("unshipped support needs its dedicated namespace")
    for value in payload_paths:
        path = PurePosixPath(value)
        if path.parts and path.parts[0].casefold().removesuffix(".py") == namespace.casefold():
            raise ContractError("unshipped test support appears in the runtime artifact")


def _binding(root: Path, plan: dict, context: dict | None) -> dict:
    """Retain distinct caller identities; verify supplied source and SDK commits."""
    context = {} if context is None else context
    if not isinstance(context, dict) or set(context) - set(CONTEXT_FIELDS):
        raise ContractError("test support has unsupported binding context")
    result = {key: context.get(key) for key in CONTEXT_FIELDS}
    for key in ("candidate_sha", "qualification_sha", "provider_sha", "sha256"):
        value = result[key]
        if value is not None and (not isinstance(value, str) or not re.fullmatch(
            r"[0-9a-f]{64}" if key == "sha256" else r"[0-9a-f]{40}", value
        )):
            raise ContractError("test support binding needs immutable hashes")
    for key in ("run_id", "run_attempt"):
        if result[key] is not None and (type(result[key]) is not int or result[key] < 1):
            raise ContractError("test support binding needs positive run identity")
    if result["filename"] is not None and (
        not isinstance(result["filename"], str)
        or not re.fullmatch(r"[A-Za-z0-9_.-]+\.tar\.bz2", result["filename"])
    ):
        raise ContractError("test support binding needs a literal archive filename")

    def verify_files(repository: Path, commit: str, paths: list[str]) -> None:
        def git(*args):
            return subprocess.run(["git", "-C", str(repository), *args], check=True,
                                  capture_output=True, text=True, timeout=10).stdout.strip()
        if git("rev-parse", "HEAD") != commit:
            raise ContractError("test support binding differs from the checked-out commit")
        for relative in paths:
            if git("rev-parse", commit + ":" + relative) != git("hash-object", "--no-filters", str(repository / relative)):
                raise ContractError("test support bytes differ from the bound source commit")

    if result["candidate_sha"]:
        verify_files(root, result["candidate_sha"], [record["source"] for record in plan["files"]])
    provider = Path(__file__).resolve().parents[2]
    if result["provider_sha"]:
        verify_files(provider, result["provider_sha"], [
            "devtools/scripts/installed_test_support.py", "devtools/scripts/installed_noarch.py",
            "devtools/scripts/installed_imports.py",
            "devtools/scripts/installed_test_dependencies.py",
        ])
    return {"context": result,
            "source_state": "verified-commit-and-selected-files" if result["candidate_sha"] else "unknown",
            "provider_state": "verified-commit-and-runner-files" if result["provider_sha"] else "unknown",
            "scope": "artifact/qualification/run labels are caller context; not artifact verification"}


class SupportStage:
    """Own one private file tree and package binding; inspect without importing addons."""

    def __init__(self, root: Path, plan: dict, binding: dict):
        self.root, self.plan = root, plan
        self.namespace = plan["namespace"]
        self.package = None
        self.receipt = {
            **plan, "binding": binding, "checks": 0, "loaded": [],
            "staging_path": str(root),
            "state": "preparing", "resources_retired": False, "imports_retired": False,
            "provider_files_sha256": {
                "devtools/scripts/" + name: _digest(Path(__file__).parent / name)
                for name in ("installed_test_support.py", "installed_noarch.py", "installed_imports.py")
                if (Path(__file__).parent / name).is_file()
            },
            "scope": "unshipped test support; no installed/scientific/public artifact qualification",
        }

    def bind(self) -> None:
        _available(self.namespace)
        directory = self.root / self.namespace
        initializer = directory / "__init__.py"
        if initializer.is_file():
            spec = importlib.util.spec_from_file_location(self.namespace, initializer,
                submodule_search_locations=[str(directory)])
        else:
            spec = importlib.machinery.ModuleSpec(self.namespace, loader=None, is_package=True)
            spec.submodule_search_locations = [str(directory)]
        self.package = importlib.util.module_from_spec(spec)
        sys.modules[self.namespace] = self.package
        if initializer.is_file():
            spec.loader.exec_module(self.package)

    def check(self) -> dict:
        code, directories = set(), {self.root / self.namespace}
        for record in self.plan["files"]:
            path = self.root / record["target"]
            if not path.is_file() or path.resolve() != path or _digest(path) != record["sha256"]:
                raise ContractError("staged test support bytes changed or escaped")
            if record["kind"] == "code":
                code.add(path)
                directories.update(parent for parent in path.parents if parent != self.root and parent.is_relative_to(self.root))
        if self.package is not None and sys.modules.get(self.namespace) is not self.package:
            raise ContractError("test support namespace binding changed")
        loaded = []
        for name, module in tuple(sys.modules.items()):
            if name != self.namespace and not name.startswith(self.namespace + "."):
                continue
            filename = getattr(module, "__file__", None)
            paths = getattr(module, "__path__", ())
            if isinstance(paths, (str, bytes)):
                raise ContractError("test support package paths changed")
            try:
                locations = list(paths)
                if (not filename and not locations) or (filename and Path(filename).resolve() not in code):
                    raise ContractError("test support import is outside declared staged code")
                if any(Path(path).resolve() not in directories for path in locations):
                    raise ContractError("test support import is outside its staged package")
            except (TypeError, ValueError, OSError) as error:
                raise ContractError("test support import has invalid staged origin") from error
            loaded.append(name)
        self.receipt.update(state="verified-support", checks=self.receipt["checks"] + 1, loaded=sorted(loaded))
        return self.receipt

    def retire_imports(self) -> None:
        if self.package is not None:
            for name in tuple(sys.modules):
                if name == self.namespace or name.startswith(self.namespace + "."):
                    del sys.modules[name]
        importlib.invalidate_caches()
        self.receipt["imports_retired"] = True


@contextmanager
def staged_support(root: Path, declaration: dict | None, runtime_roots: tuple[str, ...], *, context: dict | None = None):
    """Yield optional support, checking and retiring owned resources on every exit."""
    root = root.resolve()
    plan = support_plan(root, declaration, runtime_roots)
    if plan is None:
        yield None
        return
    _available(plan["namespace"])
    binding = _binding(root, plan, context)
    stage = None
    try:
        with TemporaryDirectory(prefix="molsyssuite-installed-support-") as temporary:
            stage = SupportStage(Path(temporary).resolve(), plan, binding)
            try:
                for record in plan["files"]:
                    source = root.resolve() / record["source"]
                    if source.resolve() != source:
                        raise ContractError("test support source path changed during staging")
                    with source.open("rb") as stream:
                        payload = stream.read(record["bytes"] + 1)
                    if len(payload) != record["bytes"] or hashlib.sha256(payload).hexdigest() != record["sha256"]:
                        raise ContractError("test support source changed during staging")
                    target = stage.root / record["target"]
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(payload)
                stage.check()
                stage.bind()
                stage.check()
                try:
                    yield stage
                finally:
                    stage.check()
            except BaseException:
                stage.receipt["state"] = "failed-support-or-tests"
                raise
            finally:
                stage.retire_imports()
    finally:
        if stage:
            stage.receipt["resources_retired"] = not stage.root.exists()
