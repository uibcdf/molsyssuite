"""Public hints preserve explicit unavailable routes and the reviewed exception."""

from __future__ import annotations

import copy
import tomllib
import unittest

from devtools.scripts import package_channels


class PackageChannelTests(unittest.TestCase):
    def setUp(self):
        self.registry = tomllib.loads(
            (package_channels.ROOT / "suite.toml").read_text()
        )
        self.channels = tomllib.loads(
            (package_channels.ROOT / "devguide/package_channels.toml").read_text()
        )

    def test_conda_only_support_providers_disable_inferred_pypi(self):
        for name in ["argdigest", "depdigest", "smonitor", "pyunitwizard"]:
            with self.subTest(member=name):
                self.assertEqual(
                    package_channels.dependency_hint(
                        self.registry, self.channels, name
                    ),
                    {"pypi": None, "conda": name, "channel": "uibcdf"},
                )

    def test_pytest_plugin_keeps_both_reviewed_routes(self):
        self.assertEqual(self.channels["active-pypi-exceptions"], ["pytest-receptor"])
        self.assertEqual(
            package_channels.dependency_hint(
                self.registry, self.channels, "pytest-receptor"
            ),
            {
                "pypi": "pytest-receptor",
                "conda": "pytest-receptor",
                "channel": "uibcdf",
            },
        )

    def test_external_and_non_package_routes_are_not_rewritten(self):
        for name in ["numpy", "vina", "molsys-ai", "unregistered"]:
            with self.subTest(member=name), self.assertRaises(ValueError):
                package_channels.dependency_hint(self.registry, self.channels, name)

    def test_unknown_exception_and_wrong_channel_fail_closed(self):
        for field, value in [
            ("active-pypi-exceptions", ["unregistered"]),
            ("suite-channel", "conda-forge"),
        ]:
            changed = copy.deepcopy(self.channels)
            changed[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                package_channels.dependency_hint(self.registry, changed, "argdigest")
