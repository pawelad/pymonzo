"""
Monzo API related code
"""
import json
import webbrowser
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin

from authlib.integrations.httpx_client import OAuth2Client
from httpx import HTTPStatusError, Response

from pymonzo.api_objects import MonzoAccount, MonzoBalance, MonzoPot, MonzoTransaction
from pymonzo.exceptions import MonzoAPIError
from pymonzo.utils import get_authorization_response


class MonzoAPI:
    """
    Monzo API client.

    Official docs:
        https://monzo.com/docs/
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

    def whoami(self):
        """
        Get information about the access token.

        Official docs:
            https://monzo.com/docs/#authenticating-requests

        :returns: access token details
        :rtype: dict
        """
        endpoint = "/ping/whoami"
        response = self._get_response(
            method="get",
            endpoint=endpoint,
        )

        return response.json()

    def accounts(self, refresh=False):
        """
        Returns a list of accounts owned by the currently authorised user.
        It's often used when deciding whether to require explicit account ID
        or use the only available one, so we cache the response by default.

        Official docs:
            https://monzo.com/docs/#list-accounts

        :param refresh: decides if the accounts information should be refreshed
        :type refresh: bool
        :returns: list of Monzo accounts
        :rtype: list of MonzoAccount
        """
        if not refresh and self._cached_accounts:
            return self._cached_accounts

        endpoint = "/accounts"
        response = self._get_response(
            method="get",
            endpoint=endpoint,
        )

        accounts_json = response.json()["accounts"]
        accounts = [MonzoAccount(data=account) for account in accounts_json]
        self._cached_accounts = accounts

        return accounts

    def balance(self, account_id=None):
        """
        Returns balance information for a specific account.

        Official docs:
            https://monzo.com/docs/#read-balance

        :param account_id: Monzo account ID
        :type account_id: str
        :raises: ValueError
        :returns: Monzo balance instance
        :rtype: MonzoBalance
        """
        if not account_id:
            if len(self.accounts()) == 1:
                account_id = self.accounts()[0].id
            else:
                raise ValueError("You need to pass account ID")

        endpoint = "/balance"
        response = self._get_response(
            method="get",
            endpoint=endpoint,
            params={
                "account_id": account_id,
            },
        )

        return MonzoBalance(data=response.json())

    def pots(self, refresh=False):
        """
        Returns a list of pots owned by the currently authorised user.

        Official docs:
            https://monzo.com/docs/#pots

        :param refresh: decides if the pots information should be refreshed.
        :type refresh: bool
        :returns: list of Monzo pots
        :rtype: list of MonzoPot
        """
        if not refresh and self._cached_pots:
            return self._cached_pots

        endpoint = "/pots/listV1"
        response = self._get_response(
            method="get",
            endpoint=endpoint,
        )

        pots_json = response.json()["pots"]
        pots = [MonzoPot(data=pot) for pot in pots_json]
        self._cached_pots = pots

        return pots

    def transactions(self, account_id=None, reverse=True, limit=None):
        """
        Returns a list of transactions on the user's account.

        Official docs:
            https://monzo.com/docs/#list-transactions

        :param account_id: Monzo account ID
        :type account_id: str
        :param reverse: whether transactions should be in in descending order
        :type reverse: bool
        :param limit: how many transactions should be returned; None for all
        :type limit: int
        :returns: list of Monzo transactions
        :rtype: list of MonzoTransaction
        """
        if not account_id:
            if len(self.accounts()) == 1:
                account_id = self.accounts()[0].id
            else:
                raise ValueError("You need to pass account ID")

        endpoint = "/transactions"
        response = self._get_response(
            method="get",
            endpoint=endpoint,
            params={
                "account_id": account_id,
            },
        )

        # The API does not allow reversing the list or limiting it, so to do
        # the basic query of 'get the latest transaction' we need to always get
        # all transactions and do the reversing and slicing in Python
        # I send Monzo an email, we'll se how they'll respond
        transactions = response.json()["transactions"]
        if reverse:
            transactions.reverse()

        if limit:
            transactions = transactions[:limit]

        return [MonzoTransaction(data=t) for t in transactions]

    def transaction(self, transaction_id, expand_merchant=False):
        """
        Returns an individual transaction, fetched by its id.

        Official docs:
            https://monzo.com/docs/#retrieve-transaction

        :param transaction_id: Monzo transaction ID
        :type transaction_id: str
        :param expand_merchant: whether merchant data should be included
        :type expand_merchant: bool
        :returns: Monzo transaction details
        :rtype: MonzoTransaction
        """
        endpoint = "/transactions/{}".format(transaction_id)

        data = dict()
        if expand_merchant:
            data["expand[]"] = "merchant"

        response = self._get_response(
            method="get",
            endpoint=endpoint,
            params=data,
        )

        return MonzoTransaction(data=response.json()["transaction"])
