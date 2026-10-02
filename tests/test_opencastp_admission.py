"""Guard the explicit ownership and classification of OpenCASTp."""

from pathlib import Path

import tomllib


def test_opencastp_is_an_auxiliary_incubating_support_library():
    root = Path(__file__).resolve().parents[1]
    registry = tomllib.loads((root / "suite.toml").read_text())
    member = next(item for item in registry["members"] if item["name"] == "opencastp")
    assert member["role"] == "support-library"
    assert member["membership"] == "auxiliary"
    assert member["maturity"] == "incubating"
    assert member["development-mode"] == "active"
    assert member["capabilities"] == ["python-package"]
    assert member["zenodo-archival"] == "optional"
    assert (
        "opencastp" not in registry["initiatives"]["stabilization"]["priority-members"]
    )
    for key in (
        "python-ecosystem-reviews",
        "python-distribution-reviews",
        "python-ci-reviews",
    ):
        assert any(item["repository"] == "uibcdf/opencastp" for item in registry[key])
