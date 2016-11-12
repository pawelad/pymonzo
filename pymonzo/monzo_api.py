from __future__ import absolute_import, division, print_function

import os
from six.moves.urllib.parse import urljoin

import requests


API_URL = 'https://api.monzo.com/'
ENV_VAR = 'MONZO_ACCESS_TOKEN'


class MonzoAPI(object):
    """
    Wrapper for Monzo public API

    Official docs:
        https://monzo.com/docs/
    """
    def __init__(self, access_token=None):
        # If no access token is provided, try to get it
        # from environment variable
        if not access_token and os.environ.get(ENV_VAR):
            access_token = os.environ.get(ENV_VAR)
        elif not access_token and not os.environ.get(ENV_VAR):
            raise ValueError("No access token provided.")
        self._access_token = access_token

        # Init requests session and add auth header
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': 'Bearer {0}'.format(self._access_token),
        })

        # Check the number of accounts, set the account id if there's only one
        if len(self.accounts()) == 1:
            self._account_id = self.accounts()[0]['id']

    def whoami(self):
        """
        Get information about an access token

        Official docs:
            https://monzo.com/docs/#authenticating-requests
        """
        endpoint = '/ping/whoami'
        url = urljoin(API_URL, endpoint)
        response = self.session.get(url)

        return response.json()

    def accounts(self):
        """
        Returns a list of accounts owned by the currently authorised user.

        Official docs:
            https://monzo.com/docs/#list-accounts
        """
        endpoint = '/accounts'
        url = urljoin(API_URL, endpoint)
        response = self.session.get(url)

        return response.json()['accounts']

    def balance(self, account_id=None):
        """
        Returns balance information for a specific account.

        Official docs:
            https://monzo.com/docs/#read-balance
        """
        if not account_id and not self._account_id:
            ValueError("You need to pass the account ID")
        elif not account_id and self._account_id:
            account_id = self._account_id

        endpoint = '/balance'
        url = urljoin(API_URL, endpoint)
        data = {
            'account_id': account_id,
        }
        response = self.session.get(url, params=data)

        return response.json()

    def transactions(self, account_id=None, reverse=True, limit=5):
        """
        Returns a list of transactions on the user’s account.

        Official docs:
            https://monzo.com/docs/#list-transactions
        """
        if not account_id and not self._account_id:
            ValueError("You need to pass the account ID")
        elif not account_id and self._account_id:
            account_id = self._account_id

        endpoint = '/transactions'
        url = urljoin(API_URL, endpoint)
        data = {
            'account_id': account_id,
        }
        response = self.session.get(url, params=data)

        # The API does not allow reversing the list and getting the latest
        # transactions first. To allow a basic query of 'the latest transaction'
        # we need to always get all transactions (i.e. not use the 'limit'
        # parameter) and do the reversing and slicing in Python
        # I send Monzo an email, we'll se how they'll respond
        transactions = response.json()['transactions']
        if reverse:
            transactions.reverse()

        return transactions[limit]

    def transaction(self, transaction_id, expand_merchant=False):
        """
        Returns an individual transaction, fetched by its id.

        Official docs:
            https://monzo.com/docs/#retrieve-transaction
        """
        endpoint = '/transactions/{}'.format(transaction_id)
        url = urljoin(API_URL, endpoint)
        data = {
            'expand[]': 'merchant' if expand_merchant else '',
        }
        response = self.session.get(url, params=data)

        return response.json()['transaction']
