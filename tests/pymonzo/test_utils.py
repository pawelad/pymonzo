"""Test `pymonzo.utils` module."""

from datetime import datetime
from typing import Any

import pytest
from freezegun import freeze_time

from pymonzo.utils import empty_dict_to_none, empty_str_to_none, n_days_ago


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
    ("value", "output"),
    [
        ("", None),
        ("Lorem ipsum", "Lorem ipsum"),
        ("TEST", "TEST"),
        ({"foo": 1, "bar": True}, {"foo": 1, "bar": True}),
        (1, 1),
    ],
)
def test_empty_str_to_none(value: Any, output: Any) -> None:
    """Should return `None` if value is an empty string, do nothing otherwise."""
    assert empty_str_to_none(value) == output


@pytest.mark.parametrize(
    ("value", "output"),
    [
        ({}, None),
        ({"foo": 1, "bar": True}, {"foo": 1, "bar": True}),
        ("", ""),
        ("Lorem ipsum", "Lorem ipsum"),
        (1, 1),
    ],
)
def test_empty_dict_to_none(value: Any, output: Any) -> None:
    """Should return `None` if value is an empty dict, do nothing otherwise."""
    assert empty_dict_to_none(value) == output
