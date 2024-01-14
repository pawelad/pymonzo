"""Test `pymonzo.utils` module."""
from datetime import datetime

import pytest
from freezegun import freeze_time

from pymonzo.utils import empty_str_to_none, n_days_ago


@pytest.mark.parametrize(
    ("today", "n", "output"),
    [
        (datetime(2024, 1, 14), 5, datetime(2024, 1, 9)),
        (datetime(2024, 1, 14), 10, datetime(2024, 1, 4)),
        (datetime(2024, 1, 14), 15, datetime(2023, 12, 30)),
    ],
)
def test_n_days_ago(today: datetime, n: int, output: datetime) -> None:
    """Should subtract passed number of days from today's date."""
    with freeze_time(today):
        assert n_days_ago(n) == output


@pytest.mark.parametrize(
    ("s", "output"),
    [
        ("", None),
        ("Lorem ipsum", "Lorem ipsum"),
        ("TEST", "TEST"),
    ],
)
def test_empty_str_to_none(s: str, output: str) -> None:
    """Should return `None` if string is empty, do nothing otherwise."""
    assert empty_str_to_none(s) == output
