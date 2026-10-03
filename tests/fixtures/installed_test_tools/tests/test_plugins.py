"""A dummy installed consumer really exercises both component-specific plugins."""

import sys
from pathlib import Path

import installed_tools_fixture
import pytest

_attempts = 0


def test_real_subtests(subtests):
    for value in (1, 2):
        with subtests.test(value=value):
            assert installed_tools_fixture.increment(value) == value + 1
    assert (
        Path(installed_tools_fixture.__file__)
        .resolve()
        .is_relative_to(Path(sys.prefix).resolve())
    )


@pytest.mark.flaky(reruns=1)
def test_real_rerun():
    global _attempts
    _attempts += 1
    if _attempts == 1:
        pytest.fail("Exercise the installed rerun plugin once")
    assert _attempts == 2
