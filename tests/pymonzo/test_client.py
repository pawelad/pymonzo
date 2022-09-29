"""Test `pymonzo.client` module."""
import pytest


@pytest.mark.skip()
class TestMonzoAPI:
    """Test `MonzoAPI` class."""

    def test_init(self) -> None:
        """Client is initialized with settings loaded from disk."""

    def test_init_with_arguments(self) -> None:
        """Client is initialized with settings from passed arguments."""

    def test_authorize(self) -> None:
        """Auth flow is executed to get API access token."""
