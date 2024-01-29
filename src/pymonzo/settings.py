"""pymonzo settings related code."""

import json
import os
import sys
from functools import partial
from pathlib import Path
from typing import Dict, Union

from pydantic_settings import BaseSettings, SettingsConfigDict

if sys.version_info < (3, 11):
    from typing_extensions import Self
else:
    from typing import Self


class PyMonzoSettings(BaseSettings):
    """pymonzo settings schema.

    Attributes:
        client_id: OAuth client ID.
        client_secret: OAuth client secret.
        token: OAuth access token. For more information see
            [`pymonzo.MonzoAPI.authorize`][].
    """

    model_config = SettingsConfigDict(env_prefix="pymonzo_")

    client_id: str
    client_secret: str
    token: Dict[str, Union[str, int]]

    @classmethod
    def load_from_disk(cls, settings_path: Path) -> Self:
        """Load pymonzo settings from disk.

        Arguments:
            settings_path: Settings file path.

        Returns:
            Loaded pymonzo settings.
        """
        with open(settings_path) as f:
            settings = json.load(f)

        return cls(**settings)

    def save_to_disk(self, settings_path: Path) -> None:
        """Save pymonzo settings on disk.

        Arguments:
            settings_path: Settings file path.
        """
        # Make sure the file is not publicly accessible
        # Source: https://github.com/python/cpython/issues/73400
        os.umask(0o077)
        with open(settings_path, "w", opener=partial(os.open, mode=0o600)) as f:
            f.write(self.model_dump_json(indent=2))
