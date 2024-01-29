"""Test `pymonzo.settings` module."""

import json
from pathlib import Path

from polyfactory.factories.pydantic_factory import ModelFactory

from pymonzo.settings import PyMonzoSettings


class PyMonzoSettingsFactory(ModelFactory[PyMonzoSettings]):
    """Factory for `PyMonzoSettings` schema."""


class TestPyMonzoSettings:
    """Test `PyMonzoSettings` class."""

    def test_load_from_disk(self, tmp_path: Path) -> None:
        """Settings are loaded from disk."""
        # Save manually
        settings = {
            "client_id": "TEST_CLIENT_ID",
            "client_secret": "TEST_CLIENT_SECRET",
            "token": {
                "access_token": "TEST_ACCESS_TOKEN",
            },
        }

        settings_path = tmp_path / ".pymonzo-test"
        with open(settings_path, "w") as f:
            json.dump(settings, f, indent=4)

        # Load
        loaded_settings = PyMonzoSettings.load_from_disk(settings_path)

        # TODO: Why does `mypy` fail here with
        #   `Argument 1 to "PyMonzoSettings" has incompatible type`
        assert loaded_settings == PyMonzoSettings(**settings)  # type: ignore

    def test_save_to_disk(self, tmp_path: Path) -> None:
        """Settings are saved to disk."""
        # Save
        settings = PyMonzoSettingsFactory.build()

        settings_path = tmp_path / ".pymonzo-test"
        settings.save_to_disk(settings_path)

        # Load manually
        with open(settings_path) as f:
            loaded_settings = json.load(f)

        assert loaded_settings == settings.model_dump(mode="json")
