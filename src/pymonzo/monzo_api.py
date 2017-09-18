# -*- coding: utf-8 -*-
"""
Monzo API related code
"""
from __future__ import unicode_literals

import os
import shelve
from contextlib import closing

import requests
from oauthlib.oauth2 import TokenExpiredError
from requests_oauthlib import OAuth2Session
from six.moves.urllib.parse import urljoin

from pymonzo.api_objects import MonzoAccount, MonzoBalance, MonzoTransaction
from pymonzo import config
from pymonzo.exceptions import MonzoAPIException
from pymonzo.utils import CommonMixin


class MonzoAPI(CommonMixin):
    """
    Base class that smartly wraps official Monzo API.

    Official docs:
        https://monzo.com/docs/
    """
    api_url = 'https://api.monzo.com/'

    _access_token = None
    _client_id = None
    _client_secret = None
    _auth_code = None

    _cached_accounts = None

    def __init__(self, access_token=None, client_id=None, client_secret=None,
                 auth_code=None):
        """
        We need Monzo access token to work with the API, which we try to get
        in multiple ways detailed below. Basically you need to either pass
        it directly, pass your client ID, client secret and OAuth 2 auth code
        or have the token already saved on the disk from previous OAuth 2
        authorization.

        We then create an OAuth authorised session and get the default
        account ID if there's only one available.

        :param access_token: your Monzo access token
        :type access_token: str
        :param client_id: your Monzo client ID
        :type client_id: str
        :param client_secret: your Monzo client secret
        :type client_secret: str
        :param auth_code: your Monzo OAuth 2 auth code
        :type auth_code: str
        """
        # Lets get the access token from:
        # a) explicitly passed 'access_token'
        if access_token:
            self._access_token = access_token
            self._token = {
                'access_token': self._access_token,
                'token_type': 'Bearer',
            }
        # b) explicitly passed 'client_id', 'client_secret' and 'auth_code'
        elif all([client_id, client_secret, auth_code]):
            self._client_id = client_id
            self._client_secret = client_secret
            self._auth_code = auth_code

            self._token = self._get_oauth_token()
        # c) token file saved on the disk
        elif os.path.isfile(config.TOKEN_FILE_PATH):
            with closing(shelve.open(config.TOKEN_FILE_PATH)) as f:
                self._token = f['token']
        # d) 'access_token' saved as a environment variable
        elif os.getenv(config.MONZO_ACCESS_TOKEN_ENV):
            self._access_token = os.getenv(config.MONZO_ACCESS_TOKEN_ENV)

            self._token = {
                'access_token': self._access_token,
                'token_type': 'Bearer',
            }
        # e) 'client_id', 'client_secret' and 'auth_code' saved as
        # environment variables
        elif (os.getenv(config.MONZO_CLIENT_ID_ENV) and
                os.getenv(config.MONZO_CLIENT_SECRET_ENV) and
                os.getenv(config.MONZO_AUTH_CODE_ENV)):
            self._client_id = os.getenv(config.MONZO_CLIENT_ID_ENV)
            self._client_secret = os.getenv(config.MONZO_CLIENT_SECRET_ENV)
            self._auth_code = os.getenv(config.MONZO_AUTH_CODE_ENV)

            self._token = self._get_oauth_token()
        else:
            raise ValueError(
                "To authenticate and use Monzo public API you need to pass "
                "(or set as environment variables) either "
                "the access token or all of client ID, client secret "
                "and authentication code. For more info see "
                "https://github.com/pawelad/pymonzo#authentication"
            )

        # Create a session with the acquired token
        self._session = OAuth2Session(
            client_id=self._client_id,
            token=self._token,
        )

    @staticmethod
    def _save_token_on_disk(token):
        """Helper function that saves passed token on disk"""
        with closing(shelve.open(config.TOKEN_FILE_PATH)) as f:
            f['token'] = token

    def _get_oauth_token(self):
        """
        Get Monzo access token via OAuth2 `authorization code` grant type.

        Official docs:
            https://monzo.com/docs/#acquire-an-access-token

        :returns: OAuth 2 access token
        :rtype: dict
        """
        url = urljoin(self.api_url, '/oauth2/token')

        oauth = OAuth2Session(
            client_id=self._client_id,
            redirect_uri=config.PYMONZO_REDIRECT_URI,
        )

        token = oauth.fetch_token(
            token_url=url,
            code=self._auth_code,
            client_secret=self._client_secret,
        )

        self._save_token_on_disk(token)

        return token

    def _refresh_oath_token(self):
        """
        Refresh Monzo OAuth 2 token.

        Official docs:
            https://monzo.com/docs/#refreshing-access

        :returns: OAuth 2 access token
        :rtype: dict
        """
        url = urljoin(self.api_url, '/oauth2/token')
        data = {
            'grant_type': 'refresh_token',
            'client_id': self._client_id,
            'client_secret': self._client_secret,
            'refresh_token': self._token['refresh_token'],
        }

        token_response = requests.post(url, data=data)
        token = token_response.json()

        self._save_token_on_disk(token)

        return token

    def _get_response(self, method, endpoint, params=None):
        """
        Helper method to handle HTTP requests and catch API errors

        :param method: valid HTTP method
        :type method: str
        :param endpoint: API endpoint
        :type endpoint: str
        :param params: extra parameters passed with the request
        :type params: dict
        :returns: API response
        :rtype: Response
        """
        url = urljoin(self.api_url, endpoint)

        try:
            response = getattr(self._session, method)(url, params=params)
        except TokenExpiredError:
            # For some reason 'requests-oauthlib' automatic token refreshing
            # doesn't work so we do it here semi-manually
            self._token = self._refresh_oath_token()

            self._session = OAuth2Session(
                client_id=self._client_id,
                token=self._token,
            )

            response = getattr(self._session, method)(url, params=params)

        if response.status_code != requests.codes.ok:
            raise MonzoAPIException(
                "Something wrong happened: {}".format(response.json())
            )

        return response

    def whoami(self):
        """
        Get information about the access token.

        Official docs:
            https://monzo.com/docs/#authenticating-requests

        :returns: access token details
        :rtype: dict
        """
        endpoint = '/ping/whoami'
        response = self._get_response(
            method='get', endpoint=endpoint,
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

        endpoint = '/accounts'
        response = self._get_response(
            method='get', endpoint=endpoint,
        )

        accounts_json = response.json()['accounts']
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

        endpoint = '/balance'
        response = self._get_response(
            method='get', endpoint=endpoint,
            params={
                'account_id': account_id,
            },
        )

        return MonzoBalance(data=response.json())

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

        endpoint = '/transactions'
        response = self._get_response(
            method='get', endpoint=endpoint,
            params={
                'account_id': account_id,
            },
        )

        # The API does not allow reversing the list or limiting it, so to do
        # the basic query of 'get the latest transaction' we need to always get
        # all transactions and do the reversing and slicing in Python
        # I send Monzo an email, we'll se how they'll respond
        transactions = response.json()['transactions']
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
        endpoint = '/transactions/{}'.format(transaction_id)

        data = dict()
        if expand_merchant:
            data['expand[]'] = 'merchant'

        response = self._get_response(
            method='get', endpoint=endpoint, params=data,
        )

        return MonzoTransaction(data=response.json()['transaction'])
