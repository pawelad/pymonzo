"""
pymonzo API client code.
"""
import webbrowser
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import structlog
from authlib.integrations.httpx_client import OAuth2Client

from pymonzo.accounts import AccountsResource
from pymonzo.balance import BalanceResource
from pymonzo.pots import PotsResource
from pymonzo.settings import PyMonzoSettings
from pymonzo.transactions import TransactionsResource
from pymonzo.utils import get_authorization_response
from pymonzo.whoami import WhoAmIResource

log = structlog.get_logger()


class MonzoAPI:
    """
    Monzo API client.

    Docs:
        https://docs.monzo.com/
    """

    api_url = "https://api.monzo.com"
    authorization_endpoint = "https://auth.monzo.com/"
    token_endpoint = "https://api.monzo.com/oauth2/token"  # nosec B105
    settings_path = Path.home() / ".pymonzo"

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        token: Optional[dict] = None,
    ) -> None:
        """
        Initialize Monzo API client and load pymonzo config file.
        """
        if all([client_id, client_secret, token]):
            self._settings = PyMonzoSettings(
                client_id=client_id,
                client_secret=client_secret,
                token=token,
            )
        else:
            try:
                self._settings = PyMonzoSettings.load_from_disk(self.settings_path)
            except FileNotFoundError:
                raise ValueError(
                    "You either need to run "
                    "`MonzoAPI.authorize(client_id, client_secret)` to get and save "
                    "the authorization token or explicitly pass the client_id, "
                    "client_secret and token arguments."
                )

        self.session = OAuth2Client(
            client_id=self._settings.client_id,
            client_secret=self._settings.client_secret,
            token=self._settings.token,
            authorization_endpoint=self.authorization_endpoint,
            token_endpoint=self.token_endpoint,
            update_token=self.update_token,
            base_url=self.api_url,
        )

        # Add resources
        self.whoami = WhoAmIResource(client=self).whoami
        self.accounts = AccountsResource(client=self)
        self.balance = BalanceResource(client=self)
        self.pots = PotsResource(client=self)
        self.transactions = TransactionsResource(client=self)

    @classmethod
    def authorize(
        cls,
        client_id: str,
        client_secret: str,
        *,
        save_to_disk: bool = True,
        redirect_uri: str = "http://localhost:6600/pymonzo",
    ) -> dict:
        """
        Use OAuth 2 workflow to authorize and get the access token.
        """
        client = OAuth2Client(client_id, client_secret, redirect_uri=redirect_uri)
        url, state = client.create_authorization_url(cls.authorization_endpoint)

        log.msg(f"Please visit this URL to authorize: {url}")
        webbrowser.open(url)

        # Start a webserver and wait for the callback
        parsed_url = urlparse(redirect_uri)
        assert parsed_url.hostname is not None
        assert parsed_url.port is not None
        authorization_response = get_authorization_response(
            host=parsed_url.hostname,
            port=parsed_url.port,
        )

        token = client.fetch_token(
            cls.token_endpoint,
            authorization_response=authorization_response,
        )

        # Save config locally
        if save_to_disk:
            settings = PyMonzoSettings(
                client_id=client_id,
                client_secret=client_secret,
                token=token,
            )
            settings.save_to_disk(cls.settings_path)

        return token

    def update_token(self, token: dict, **kwargs):
        """
        Update settings with refreshed token and save to disk.
        """
        self._settings.token = token
        self._settings.save_to_disk(self.settings_path)
