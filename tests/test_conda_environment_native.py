"""Opt-in native qualification; synthetic transactions, never scientific Python.

Set MOLSYSSUITE_MAMBA_116 to an explicit Mamba 2.9.0 executable. All archives,
HTTP metadata, caches and target prefixes belong to a managed private directory.
"""

from __future__ import annotations

import functools
import hashlib
import http.server
import io
import json
import os
import platform
import subprocess
import tarfile
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

from devtools.scripts import conda_environment_tools as tools
from tests import test_conda_environment_tools as owner_fixtures


def write_channel(root: Path, names: list[tuple[str, str]]) -> dict:
    """Build minimal real control archives and metadata without external tools."""
    packages = {}
    noarch = root / "noarch"
    noarch.mkdir(parents=True, exist_ok=True)
    for name, version in names:
        index = {
            "name": name, "version": version, "build": "control_0",
            "build_number": 0, "depends": [], "subdir": "noarch",
            "noarch": "generic",
        }
        filename = f"{name}-{version}-control_0.tar.bz2"
        marker = f"share/molsyssuite-channel-control/{name}.txt"
        with tarfile.open(noarch / filename, "w:bz2") as archive:
            for path, payload in {
                "info/index.json": json.dumps(index),
                "info/files": marker + "\n",
                marker: "Synthetic channel qualification; not a runtime package.\n",
            }.items():
                data = payload.encode()
                entry = tarfile.TarInfo(path)
                entry.size = len(data)
                archive.addfile(entry, io.BytesIO(data))
        data = (noarch / filename).read_bytes()
        packages[filename] = {
            **index, "size": len(data), "md5": hashlib.md5(data).hexdigest(),
            "sha256": hashlib.sha256(data).hexdigest(),
        }
    for subdir, contents in (("noarch", packages), ("linux-64", {})):
        directory = root / subdir
        directory.mkdir(exist_ok=True)
        metadata = {"info": {"subdir": subdir}, "packages": contents,
                    "packages.conda": {}, "repodata_version": 1}
        for filename in ("repodata.json", "current_repodata.json"):
            (directory / filename).write_text(json.dumps(metadata))
    return packages


@unittest.skipUnless(os.environ.get("MOLSYSSUITE_MAMBA_116"), "opt-in native Mamba qualification")
class NativeChannelPolicyTests(unittest.TestCase):
    def test_real_create_inheritance_exclusion_cache_and_declared_archives(self):
        owner = owner_fixtures.EnvironmentToolsTests()
        owner.setUp()
        self.addCleanup(owner.doCleanups)
        source = yaml.safe_load((owner.root / owner.production).read_text())
        source["channels"] = ["uibcdf", "conda-forge", "controlalpha"]
        owner.write(owner.production, yaml.safe_dump(source))
        inventory = owner.root / "devtools/dependency_routes.toml"
        inventory.write_text(inventory.read_text().replace(
            'purpose = "production"',
            'purpose = "production"\nadditional_channels = ["controlalpha"]\n'
            'channel_reason = "Reviewed private qualification channel"', 1))
        before = owner.snapshot()
        outcomes = []
        names = [("python", "3.14.0"), ("pip", "26.0"),
                 ("numpy", "2.4.0"), ("provider", "1.5.0")]
        with tempfile.TemporaryDirectory(prefix="molsyssuite116-native-") as temporary:
            task = Path(temporary)
            channel_root = task / "channels"
            write_channel(channel_root / "controlalpha", [])
            write_channel(channel_root / "uibcdf", [])
            write_channel(channel_root / "conda-forge", [])
            packages = write_channel(channel_root / "controlbeta", names)

            class Handler(http.server.SimpleHTTPRequestHandler):
                def log_message(self, *args):
                    pass

            server = http.server.ThreadingHTTPServer(
                ("127.0.0.1", 0), functools.partial(Handler, directory=str(channel_root)))
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                alias = f"http://127.0.0.1:{server.server_port}"
                rc = task / ".condarc"
                rc.write_text(yaml.safe_dump({
                    "channels": ["controlbeta"], "channel_alias": alias,
                    "channel_priority": "strict", "always_yes": True,
                }))
                with patch.dict(os.environ, {
                    "CONDARC": str(rc), "MAMBARC": str(rc),
                    "MAMBA_ROOT_PREFIX": str(task / "root-prefix"),
                    "CONDA_ENVS_PATH": str(task / "envs"),
                    "CONDA_PKGS_DIRS": str(task / "cache"),
                    "CONDA_OFFLINE": "false", "MAMBA_ALWAYS_YES": "true",
                    "CONDA_ALWAYS_YES": "true",
                }):
                    manager = os.environ["MOLSYSSUITE_MAMBA_116"]
                    observed = tools.observe_channels(manager, dict(os.environ))
                    self.assertEqual("mamba", observed["family"])
                    self.assertEqual("2.9.0", observed["version"])
                    self.assertEqual(["controlbeta"], observed["configuration"]["channels"])

                    def negative(name):
                        with self.assertRaises(subprocess.CalledProcessError):
                            tools.apply_environment(owner.root, owner.production, "3.14",
                                manager=manager, name=name, channel_policy="declared-only")
                        prefix = task / "envs" / name
                        self.assertFalse((prefix / "conda-meta" / "history").exists())
                        outcomes.append({"case": name, "outcome": "refused-by-solver",
                                         "linked_records": 0})

                    # Cold-cache negative, then configured creation warms the
                    # same cache with the inherited archives, then repeat.
                    negative("exclusive-cold")
                    receipt = tools.apply_environment(owner.root, owner.production, "3.14",
                        manager=manager, name="configured")
                    linked = list((task / "envs" / "configured" / "conda-meta").glob("*.json"))
                    self.assertEqual(4, len(linked))
                    coordinates = [json.loads(path.read_text()) for path in linked]
                    for item in coordinates:
                        key = f"{item['name']}-{item['version']}-{item['build']}.tar.bz2"
                        self.assertEqual(packages[key]["sha256"], item["sha256"])
                    self.assertTrue(all(item["url"].startswith(alias + "/controlbeta/")
                                        for item in coordinates))
                    self.assertEqual("unknown", receipt["channel_evidence"]["manager"]["effective"]["state"])
                    outcomes.append({"case": "configured", "outcome": "installed-inherited",
                                     "records": [{k: item[k] for k in ("name", "version", "build", "sha256")}
                                                 for item in coordinates]})
                    negative("exclusive-warm")
                    # Serve identical archive bytes from the declared channel.
                    self.assertEqual(packages, write_channel(channel_root / "controlalpha", names))
                    os.environ["CONDA_PKGS_DIRS"] = str(task / "declared-cache")
                    result = tools.apply_environment(owner.root, owner.production, "3.14",
                        manager=manager, name="exclusive-declared", channel_policy="declared-only")
                    linked = list((task / "envs" / "exclusive-declared" / "conda-meta").glob("*.json"))
                    self.assertEqual(4, len(linked))
                    coordinates = [json.loads(path.read_text()) for path in linked]
                    for item in coordinates:
                        key = f"{item['name']}-{item['version']}-{item['build']}.tar.bz2"
                        self.assertEqual(packages[key]["sha256"], item["sha256"])
                    self.assertTrue(all(item["url"].startswith(alias + "/controlalpha/")
                                        for item in coordinates))
                    self.assertEqual("declared-only", result["channel_evidence"]["policy"])
                    outcomes.append({"case": "exclusive-declared", "outcome": "installed-declared",
                                     "records": [{k: item[k] for k in ("name", "version", "build", "sha256")}
                                                 for item in coordinates]})
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=10)
                self.assertFalse(thread.is_alive())
        self.assertFalse(task.exists())
        # A synthetic Python archive has no executable for Mamba's pip inspect
        # on env remove. Retire the owned directory through its context, then
        # let the native environment inventory prune its absent registrations.
        subprocess.run([manager, "env", "list", "--json"], check=True,
                       capture_output=True, text=True)
        registry = Path.home() / ".conda/environments.txt"
        if registry.exists():
            self.assertNotIn(str(task), registry.read_text())
        self.assertEqual(before, owner.snapshot())
        destination = os.environ.get("MOLSYSSUITE_CHANNEL_RECEIPT_116")
        if destination:
            Path(destination).write_text(json.dumps({
                "schema": "molsyssuite.native-channel-qualification@1",
                "issue": "uibcdf/molsyssuite#116", "manager": "mamba", "version": "2.9.0",
                "platform": "linux", "operation": "create", "offline": False,
                "architecture": platform.machine(),
                "provider_files_sha256": {
                    str(Path(path).relative_to(Path(tools.__file__).resolve().parents[2])):
                        hashlib.sha256(Path(path).read_bytes()).hexdigest()
                    for path in (tools.__file__, __file__)
                },
                "input_channels": source["channels"], "configured_channels": ["controlbeta"],
                "cases": outcomes, "owner_inputs_preserved": True,
                "private_resources_retired": True,
                "native_registrations_retired": True,
                "scope": "SDK/native HTTP transactions with synthetic archives; no real Python/science/public channels",
            }, indent=2) + "\n")
