"""
pymonzo settings related code.
"""
import json
from pathlib import Path

from pydantic import BaseSettings


class PyMonzoSettings(BaseSettings):
    """
    pymonzo settings schema.
    """

    client_id: str
    client_secret: str
    token: dict

    class Config:
        env_prefix = "pymonzo_"

    @classmethod
    def load_from_disk(cls, settings_path: Path) -> "PyMonzoSettings":
        """
        Load pymonzo settings from disk.
        """
        with open(settings_path, "r") as f:
            settings = json.load(f)

        return cls(**settings)

    def save_to_disk(self, settings_path: Path) -> None:
        """
        Save pymonzo config on disk.
        """
        with open(settings_path, "w") as f:
            json.dump(self.dict(), f, indent=4)
