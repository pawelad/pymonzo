# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import shelve

import requests
from requests_oauthlib import OAuth2Session
from six.moves.urllib.parse import urljoin

from pymonzo.api_objects import MonzoAccount, MonzoBalance, MonzoTransaction
from pymonzo.exceptions import MonzoAPIException


API_URL = 'https://api.monzo.com/'
PYMONZO_REDIRECT_URI = 'https://github.com/pawelad/pymonzo'

MONZO_ACCESS_TOKEN_ENV = 'MONZO_ACCESS_TOKEN'
MONZO_AUTH_CODE_ENV = 'MONZO_AUTH_CODE'
MONZO_CLIENT_ID_ENV = 'MONZO_CLIENT_ID'
MONZO_CLIENT_SECRET_ENV = 'MONZO_CLIENT_SECRET'

TOKEN_FILE_NAME = '.pymonzo-token'
TOKEN_FILE_PATH = os.path.join(os.path.expanduser('~'), TOKEN_FILE_NAME)


class MonzoAPI(object):
    """
    Base class that smartly wraps official Monzo API.

    Official docs:
        https://monzo.com/docs/
    """
    default_account_id = None

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
        # If no values are passed, try to get them from environment variables
        self._access_token = (
            access_token or os.environ.get(MONZO_ACCESS_TOKEN_ENV)
        )
        self._client_id = (
            client_id or os.environ.get(MONZO_CLIENT_ID_ENV)
        )
        self._client_secret = (
            client_secret or os.environ.get(MONZO_CLIENT_SECRET_ENV)
        )
        self._auth_code = (
            auth_code or os.environ.get(MONZO_AUTH_CODE_ENV)
        )

        # We try to get the access token from:
        # a) explicitly passed 'access_token'
        if access_token:
            self._token = {
                'access_token': self._access_token,
                'token_type': 'Bearer',
            }
        # b) explicitly passed 'client_id', 'client_secret' and 'auth_code'
        elif all([client_id, client_secret, auth_code]):
            self._token = self._get_oauth_token()
        # c) token file saved on the disk
        elif os.path.isfile(TOKEN_FILE_PATH):
            with shelve.open(TOKEN_FILE_PATH) as f:
                self._token = f['token']
        # d) 'access_token' saved as a environment variable
        elif self._access_token:
            self._token = {
                'access_token': self._access_token,
                'token_type': 'Bearer',
            }
        # e) 'client_id', 'client_secret' and 'auth_code' saved as
        # environment variables
        elif all([self._client_id, self._client_secret, self._auth_code]):
            self._token = self._get_oauth_token()
        else:
            raise ValueError(
                "You need to pass (or set as environment variables) either "
                "explicit 'access_token' or all of 'client_id', "
                "'client_secret' and 'auth_code'"
            )

        # Create a session with newly acquired token
        self._session = OAuth2Session(
            client_id=client_id,
            token=self._token,
            auto_refresh_url=urljoin(API_URL, '/oauth2/token'),
            auto_refresh_kwargs={
                'grant_type': 'refresh_token',
                'client_id': self._client_id,
                'client_secret': self._client_secret,
            },
            token_updater=self._save_token_on_disk,
        )

        # Set the default account ID if there is only one available
        if len(self.accounts()) == 1:
            self.default_account_id = self.accounts()[0].id

    @staticmethod
    def _save_token_on_disk(token):
        """Helper function that saves passed token on disk"""
        with shelve.open(TOKEN_FILE_PATH) as f:
            f['token'] = token

    def _get_oauth_token(self):
        """
        Get Monzo access token via OAuth2 `authorization_code` grant type.

        Official docs:
            https://monzo.com/docs/#acquire-an-access-token
        """
        endpoint = '/oauth2/token'
        url = urljoin(API_URL, endpoint)

        oauth = OAuth2Session(
            client_id=self._client_id,
            redirect_uri=PYMONZO_REDIRECT_URI,
        )

        token = oauth.fetch_token(
            token_url=url,
            code=self._auth_code,
            client_secret=self._client_secret,
        )

        self._save_token_on_disk(token)

        return token

    def _get_response(self, method, endpoint, params=None):
        """
        Helper method for wading API requests, mainly for catching errors
        in one place.

        :param method: valid HTTP method
        :type method: str
        :param endpoint: API endpoint
        :type endpoint: str
        :param params: extra parameters passed with the request
        :type params: dict
        :returns: API response
        :rtype: Response
        """
        url = urljoin(API_URL, endpoint)
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

    def accounts(self):
        """
        Returns a list of accounts owned by the currently authorised user.

        Official docs:
            https://monzo.com/docs/#list-accounts

        :returns: list of Monzo accounts
        :rtype: list of MonzoAccount
        """
        endpoint = '/accounts'
        response = self._get_response(
            method='get', endpoint=endpoint,
        )

        accounts = response.json()['accounts']

        return [MonzoAccount(data=account) for account in accounts]

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
        if not account_id and not self.default_account_id:
            raise ValueError("You need to pass account ID")
        elif not account_id and self.default_account_id:
            account_id = self.default_account_id

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
        if not account_id and not self.default_account_id:
            raise ValueError("You need to pass account ID")
        elif not account_id and self.default_account_id:
            account_id = self.default_account_id

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
