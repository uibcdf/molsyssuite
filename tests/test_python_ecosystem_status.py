from __future__ import annotations

import copy
from pathlib import Path

import tomllib

from devtools.scripts import python_ecosystem_status

ROOT = Path(__file__).resolve().parents[1]


def _registry():
    return tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))


def test_review_inventory_covers_every_python_member():
    data = _registry()
    assert python_ecosystem_status.validate(data) == []
    assert len(data["python-ecosystem-reviews"]) == 14


def test_adoption_claim_requires_evidence_and_exception_has_a_bound():
    data = copy.deepcopy(_registry())
    review = data["python-ecosystem-reviews"][0]
    review["review-issue"] = "uibcdf/molsyssuite#6"
    review["developer-tools"] = "adopted"
    review.pop("developer-tools-evidence", None)
    review["support-libraries"] = "excepted"
    for field in ("reason", "owner", "removal-condition", "expires-on"):
        review.pop(f"support-libraries-{field}", None)
    errors = python_ecosystem_status.validate(data)
    assert any("adoption without evidence" in error for error in errors)
    assert any("support-libraries-reason" in error for error in errors)
    assert any("support-libraries-owner" in error for error in errors)
    assert any("support-libraries-removal-condition" in error for error in errors)
    assert any("support-libraries-expires-on" in error for error in errors)
    assert any("needs a member review issue" in error for error in errors)
