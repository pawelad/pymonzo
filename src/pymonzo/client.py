"""
Monzo API related code
"""
import json
import webbrowser
from pathlib import Path
from typing import List, Optional
from urllib.parse import urljoin

from authlib.integrations.httpx_client import OAuth2Client
from httpx import HTTPStatusError, Response

from pymonzo import schemas
from pymonzo.exceptions import MonzoAPIError
from pymonzo.utils import get_authorization_response


class MonzoAPI:
    """
    Monzo API client.

    Docs:
        https://docs.monzo.com/
    """

    api_url = "https://api.monzo.com/"
    authorization_endpoint = "https://auth.monzo.com/"
    token_endpoint = "https://api.monzo.com/oauth2/token"
    config_path = str(Path.home() / ".pymonzo")

    _cached_accounts = None
    _cached_pots = None

    def __init__(self) -> None:
        """
        Initialize Monzo API client and load pymonzo config file.
        """
        config = self._get_config()

        if not config:
            raise ValueError("You need to run 'MonzoAPI.authorize()' first.")

        token = config["token"]
        client_id = config["client_id"]
        client_secret = config["client_secret"]

        self._session = OAuth2Client(
            client_id=client_id,
            client_secret=client_secret,
            token=token,
            authorization_endpoint=self.authorization_endpoint,
            token_endpoint=self.token_endpoint,
        )

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

    def _get_response(
        self, method: str, endpoint: str, params: Optional[dict] = None
    ) -> Response:
        """
        Helper method to handle HTTP requests and catch API errors
        """
        url = urljoin(self.api_url, endpoint)

        response = getattr(self._session, method)(url, params=params)

        try:
            response.raise_for_status()
        except HTTPStatusError as e:
            raise MonzoAPIError(f"Something went wrong: {e}")

        return response

    def whoami(self) -> schemas.MonzoWhoAmi:
        """
        Return information about the access token.

        Docs:
            https://docs.monzo.com/#authenticating-requests
        """
        endpoint = "/ping/whoami"
        response = self._get_response(method="get", endpoint=endpoint)

        who_am_i = schemas.MonzoWhoAmi(**response.json())

        return who_am_i

    def accounts(self, refresh: bool = False) -> List[schemas.MonzoAccount]:
        """
        Return a list of user accounts.

        It's often used when deciding whether to require explicit account ID
        or use the only available one, so we cache the response by default.

        Docs:
            https://docs.monzo.com/#list-accounts
        """
        if not refresh and self._cached_accounts:
            return self._cached_accounts

        endpoint = "/accounts"
        response = self._get_response(method="get", endpoint=endpoint)

        accounts = [
            schemas.MonzoAccount(**account) for account in response.json()["accounts"]
        ]
        self._cached_accounts = accounts

        return accounts

    def balance(self, account_id: Optional[str] = None) -> schemas.MonzoBalance:
        """
        Return balance information for passed account.

        For ease of use, it allows not passing an account ID if the user has only
        one account.

        Docs:
            https://docs.monzo.com/#read-balance
        """
        if not account_id:
            if len(self.accounts()) == 1:
                account_id = self.accounts()[0].id
            else:
                raise ValueError("You need to pass an account ID")

        endpoint = "/balance"
        params = {"account_id": account_id}
        response = self._get_response(method="get", endpoint=endpoint, params=params)

        balance = schemas.MonzoBalance(**response.json())

        return balance

    def pots(self, refresh: bool = False) -> List[schemas.MonzoPot]:
        """
        Return a list of user pots.

        Docs:
            https://monzo.com/docs/#pots
        """
        if not refresh and self._cached_pots:
            return self._cached_pots

        endpoint = "/pots"
        response = self._get_response(method="get", endpoint=endpoint)

        pots = [schemas.MonzoPot(**pot) for pot in response.json()["pots"]]
        self._cached_pots = pots

        return pots

    def transaction(
        self, transaction_id: str, *, expand_merchant: bool = False
    ) -> schemas.MonzoTransaction:
        """
        Return single transaction.

        Docs:
            https://docs.monzo.com/#retrieve-transaction
        """
        endpoint = f"/transactions/{transaction_id}"
        params = {}
        if expand_merchant:
            params["expand[]"] = "merchant"

        response = self._get_response(method="get", endpoint=endpoint, params=params)

        transaction = schemas.MonzoTransaction(**response.json()["transaction"])

        return transaction

    def transactions(
        self, account_id: Optional[str] = None, limit: Optional[int] = None
    ) -> List[schemas.MonzoTransaction]:
        """
        Return a list of passed account transactions.

        Docs:
            https://docs.monzo.com/#list-transactions
        """
        if not account_id:
            if len(self.accounts()) == 1:
                account_id = self.accounts()[0].id
            else:
                raise ValueError("You need to pass an account ID")

        endpoint = "/transactions"
        params = {"account_id": account_id}
        if limit:
            params["limit"] = limit
        response = self._get_response(method="get", endpoint=endpoint, params=params)

        transactions = [
            schemas.MonzoTransaction(**transaction)
            for transaction in response.json()["transactions"]
        ]

        return transactions
