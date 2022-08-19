"""
Monzo API related code
"""
import json
import webbrowser
from pathlib import Path
from typing import Optional

from authlib.integrations.httpx_client import OAuth2Client

from pymonzo.accounts import AccountsResource
from pymonzo.balance import BalanceResource
from pymonzo.pots import PotsResource
from pymonzo.transactions import TransactionsResource
from pymonzo.utils import get_authorization_response
from pymonzo.whoami import WhoAmIResource


class MonzoAPI:
    """
    Monzo API client.

    Docs:
        https://docs.monzo.com/
    """

    api_url = "https://api.monzo.com"
    authorization_endpoint = "https://auth.monzo.com/"
    token_endpoint = "https://api.monzo.com/oauth2/token"
    config_path = str(Path.home() / ".pymonzo")

    _cached_accounts = None
    _cached_pots = None

    def __init__(self) -> None:
        """
        Initialize Monzo API client and load pymonzo config file.
        """
        # Initialize OAuth authenticated session from data saved from disk
        config = self._get_config()

        if not config:
            raise ValueError("You need to run 'MonzoAPI.authorize()' first.")

        self.session = OAuth2Client(
            client_id=config["client_id"],
            client_secret=config["client_secret"],
            token=config["token"],
            authorization_endpoint=self.authorization_endpoint,
            token_endpoint=self.token_endpoint,
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
        redirect_uri: str = "http://localhost:6600/pymonzo",
    ) -> None:
        """
        Use OAuth 2 workflow to authorize and get the access token.
        """
        client = OAuth2Client(client_id, client_secret, redirect_uri=redirect_uri)
        url, state = client.create_authorization_url(cls.authorization_endpoint)

        print(f"Please visit this URL to authorize this application: {url}")
        webbrowser.open(url)

        # Start a webserver and wait for the callback
        authorization_response = get_authorization_response("localhost", 6600)

        token = client.fetch_token(
            cls.token_endpoint, authorization_response=authorization_response
        )

        # Save config locally
        config = {
            "client_id": client_id,
            "client_secret": client_secret,
            "token": token,
        }
        cls._save_config(config)

    @classmethod
    def _get_config(cls) -> Optional[dict]:
        """
        Get pymonzo config from disk. Includes Monzo OAuth app client ID, client secret
        and generated authorization token.
        """
        try:
            with open(cls.config_path, "r") as f:
                config = json.load(f)
        except FileNotFoundError:
            config = None

        return config

    @classmethod
    def _save_config(cls, config: dict) -> None:
        """
        Save pymonzo config on disk. Includes Monzo OAuth app client ID, client secret
        and generated authorization token.
        """
        with open(cls.config_path, "w") as f:
            json.dump(config, f, indent=4)
