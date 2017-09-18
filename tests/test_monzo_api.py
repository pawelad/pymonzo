# -*- coding: utf-8 -*-
"""
Test 'pymonzo.monzo_api' file
"""
from __future__ import unicode_literals

import os
import shelve
import tempfile
from contextlib import closing
from shelve import DbfilenameShelf
from uuid import uuid4

import pytest
import six
from six.moves.urllib.parse import urljoin

from pymonzo import MonzoAPI
from pymonzo.api_objects import (
    MonzoAccount, MonzoBalance, MonzoTransaction, MonzoMerchant,
)
from pymonzo import config


class TestMonzoAPI:
    """
    Test `monzo_api.MonzoAPI` class
    """

    @pytest.fixture(scope='session')
    def monzo(self):
        """Helper fixture that returns a `MonzoAPI` instance"""
        return MonzoAPI(access_token='explicit_access_token')

    @pytest.fixture
    def mocked_monzo(self, mocker):
        """Helper fixture that returns a mocked `MonzoAPI` instance"""
        mocker.patch('pymonzo.monzo_api.OAuth2Session')
        mocker.patch('pymonzo.monzo_api.MonzoAPI._save_token_on_disk')

        client_id = 'explicit_client_id'
        client_secret = 'explicit_client_secret'
        auth_code = 'explicit_auth_code'

        monzo = MonzoAPI(
            client_id=client_id,
            client_secret=client_secret,
            auth_code=auth_code,
        )

        return monzo

    def test_class_initialization(self, monkeypatch, mocker):
        """Test class `__init__` method"""
        access_token = 'explicit_access_token'
        client_id = 'explicit_client_id'
        client_secret = 'explicit_client_secret'
        auth_code = 'explicit_auth_code'
        monkeypatch.setenv(config.MONZO_ACCESS_TOKEN_ENV, 'env_access_token')
        monkeypatch.setenv(config.MONZO_CLIENT_ID_ENV, 'env_client_id')
        monkeypatch.setenv(config.MONZO_CLIENT_SECRET_ENV, 'env_client_secret')
        monkeypatch.setenv(config.MONZO_AUTH_CODE_ENV, 'env_auth_code')

        # When we provide all variables both explicitly and via environment
        # variables, the explicit 'access token' should take precedence
        mocker.patch('os.path.isfile', return_value=True)
        mocked_oauth2_session = mocker.patch('pymonzo.monzo_api.OAuth2Session')
        expected_token = {
            'access_token': 'explicit_access_token',
            'token_type': 'Bearer',
        }

        monzo = MonzoAPI(
            access_token=access_token, client_id=client_id,
            client_secret=client_secret, auth_code=auth_code,
        )

        assert monzo._access_token == 'explicit_access_token'
        assert monzo._client_id is None
        assert monzo._client_secret is None
        assert monzo._auth_code is None
        assert monzo._token == expected_token
        mocked_oauth2_session.assert_called_once_with(
            client_id=None,
            token=expected_token,
        )

        # Don't pass 'access_token' explicitly
        mocked_oauth2_session = mocker.patch('pymonzo.monzo_api.OAuth2Session')
        mocked_get_oauth_token = mocker.patch(
            'pymonzo.monzo_api.MonzoAPI._get_oauth_token'
        )
        expected_token = mocked_get_oauth_token.return_value

        monzo = MonzoAPI(
            client_id=client_id,
            client_secret=client_secret,
            auth_code=auth_code,
        )

        assert monzo._access_token is None
        assert monzo._client_id == 'explicit_client_id'
        assert monzo._client_secret == 'explicit_client_secret'
        assert monzo._auth_code == 'explicit_auth_code'
        assert monzo._token == expected_token
        mocked_get_oauth_token.assert_called_once_with()
        mocked_oauth2_session.assert_called_once_with(
            client_id='explicit_client_id',
            token=expected_token,
        )

        # Don't pass anything explicitly and the token file exists
        mocked_oauth2_session = mocker.patch('pymonzo.monzo_api.OAuth2Session')
        mocker.patch('os.path.isfile', return_value=True)
        mocked_shelve_file = mocker.MagicMock(spec=DbfilenameShelf)
        mocked_shelve_open = mocker.patch('shelve.open')
        mocked_shelve_open.return_value = mocked_shelve_file
        expected_token = mocked_shelve_file['token']

        monzo = MonzoAPI()

        assert monzo._access_token is None
        assert monzo._client_id is None
        assert monzo._client_secret is None
        assert monzo._auth_code is None
        assert monzo._token == expected_token
        mocked_get_oauth_token.assert_called_once_with()
        mocked_oauth2_session.assert_called_once_with(
            client_id=None,
            token=expected_token,
        )

        # Don't pass anything explicitly, the token file doesn't exist
        # and 'access_token' environment variable exists
        mocked_oauth2_session = mocker.patch('pymonzo.monzo_api.OAuth2Session')
        mocker.patch('os.path.isfile', return_value=False)

        expected_token = {
            'access_token': 'env_access_token',
            'token_type': 'Bearer',
        }

        monzo = MonzoAPI()

        assert monzo._access_token == 'env_access_token'
        assert monzo._client_id is None
        assert monzo._client_secret is None
        assert monzo._auth_code is None
        assert monzo._token == expected_token
        mocked_oauth2_session.assert_called_once_with(
            client_id=None,
            token=expected_token,
        )

        # Don't pass anything explicitly, the token file doesn't exist
        # and 'access_token' environment variable doesn't exist
        monkeypatch.delenv(config.MONZO_ACCESS_TOKEN_ENV)
        mocked_oauth2_session = mocker.patch('pymonzo.monzo_api.OAuth2Session')
        mocked_get_oauth_token = mocker.patch(
            'pymonzo.monzo_api.MonzoAPI._get_oauth_token'
        )
        expected_token = mocked_get_oauth_token.return_value

        monzo = MonzoAPI()

        assert monzo._access_token is None
        assert monzo._client_id == 'env_client_id'
        assert monzo._client_secret == 'env_client_secret'
        assert monzo._auth_code == 'env_auth_code'
        assert monzo._token == expected_token
        mocked_get_oauth_token.assert_called_once_with()
        mocked_oauth2_session.assert_called_once_with(
            client_id='env_client_id',
            token=expected_token,
        )

        # None of the above
        monkeypatch.delenv(config.MONZO_CLIENT_ID_ENV)

        with pytest.raises(ValueError):
            MonzoAPI(
                auth_code=auth_code, client_id=client_id,
            )

    def test_class_save_token_on_disk_method(self):
        """Test class `_save_token_on_disk` method"""
        config.TOKEN_FILE_PATH = os.path.join(
            tempfile.gettempdir(), 'pymonzo_test',
        )
        token = {
            'foo': str(uuid4()),
            'bar': 1,
            'baz': False,
        }

        MonzoAPI._save_token_on_disk(token)

        with closing(shelve.open(config.TOKEN_FILE_PATH)) as f:
            assert f['token'] == token

    def test_class_get_oauth_token_method(self, mocker, mocked_monzo):
        """Test class `_get_oauth_token` method"""
        mocked_fetch_token = mocker.MagicMock()
        mocked_oauth2_session = mocker.patch('pymonzo.monzo_api.OAuth2Session')
        mocked_oauth2_session.return_value.fetch_token = mocked_fetch_token
        mocked_save_token_on_disk = mocker.patch(
            'pymonzo.monzo_api.MonzoAPI._save_token_on_disk'
        )

        token = mocked_monzo._get_oauth_token()

        assert token == mocked_fetch_token.return_value

        mocked_oauth2_session.assert_called_once_with(
            client_id=mocked_monzo._client_id,
            redirect_uri=config.PYMONZO_REDIRECT_URI,
        )
        mocked_fetch_token.assert_called_once_with(
            token_url=urljoin(mocked_monzo.api_url, '/oauth2/token'),
            code=mocked_monzo._auth_code,
            client_secret=mocked_monzo._client_secret,
        )
        mocked_save_token_on_disk.assert_called_once_with(
            mocked_fetch_token.return_value
        )

    def test_class_refresh_oath_token_method(self, mocker, mocked_monzo):
        """Test class `_refresh_oath_token` method"""
        mocked_requests_post_json = mocker.MagicMock()
        mocked_requests_post = mocker.patch('pymonzo.monzo_api.requests.post')
        mocked_requests_post.return_value.json = mocked_requests_post_json
        mocked_save_token_on_disk = mocker.patch(
            'pymonzo.monzo_api.MonzoAPI._save_token_on_disk'
        )

        token = mocked_monzo._refresh_oath_token()

        assert token == mocked_requests_post_json.return_value

        mocked_requests_post.assert_called_once_with(
            urljoin(mocked_monzo.api_url, '/oauth2/token'),
            data={
                'grant_type': 'refresh_token',
                'client_id': mocked_monzo._client_id,
                'client_secret': mocked_monzo._client_secret,
                'refresh_token': mocked_monzo._token['refresh_token'],
            }
        )
        mocked_requests_post_json.assert_called_once_with()
        mocked_save_token_on_disk.assert_called_once_with(
            mocked_requests_post_json.return_value
        )

    @pytest.mark.vcr()
    def test_class_whoami_method(self, monzo):
        """Test class `whoami` method"""
        whoami = monzo.whoami()

        assert whoami
        assert isinstance(whoami, dict)

        assert 'authenticated' in whoami
        assert 'client_id' in whoami
        assert 'user_id' in whoami

    @pytest.mark.vcr()
    def test_class_accounts_method(self, monzo):
        """Test class `accounts` method"""
        accounts = monzo.accounts()

        assert accounts
        assert isinstance(accounts, list)
        assert all([isinstance(i, MonzoAccount) for i in accounts])

    @pytest.mark.vcr()
    def test_class_balance_method(self, monzo):
        """Test class `balance` method"""
        balance = monzo.balance()

        assert balance
        assert isinstance(balance, MonzoBalance)

    @pytest.mark.vcr()
    def test_class_transactions_method(self, monzo):
        """Test class `transactions` method"""
        transactions = monzo.transactions()

        assert transactions
        assert isinstance(transactions, list)
        assert all([isinstance(t, MonzoTransaction) for t in transactions])

        # Non-revered results
        transactions_asc = monzo.transactions(reverse=False)

        assert transactions_asc
        assert isinstance(transactions_asc, list)
        assert all([
            isinstance(t, MonzoTransaction) for t in transactions_asc
        ])

        assert transactions == list(reversed(transactions_asc))

        # Limit results
        transactions_limit = monzo.transactions(limit=5)

        assert transactions_limit
        assert isinstance(transactions_limit, list)
        assert all([
            isinstance(t, MonzoTransaction)
            for t in transactions_limit
        ])
        assert len(transactions_limit) == 5

    @pytest.mark.vcr()
    def test_class_transaction_method(self, monzo):
        """Test class `transaction` method"""
        transaction_id = 'tx_REDACTED7'

        transaction = monzo.transaction(transaction_id=transaction_id)

        assert transaction
        assert isinstance(transaction, MonzoTransaction)
        assert isinstance(transaction.merchant, six.text_type)

        # Expand merchant
        transaction_expand_merchant = monzo.transaction(
            transaction_id=transaction_id,
            expand_merchant=True,
        )

        assert transaction_expand_merchant
        assert isinstance(transaction_expand_merchant, MonzoTransaction)
        assert isinstance(transaction_expand_merchant.merchant, MonzoMerchant)
