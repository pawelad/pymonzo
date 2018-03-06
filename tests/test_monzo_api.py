# -*- coding: utf-8 -*-
"""
Test 'pymonzo.monzo_api' file
"""
from __future__ import unicode_literals

import codecs
import json
import os
import tempfile

import pytest
from six.moves.urllib.parse import urljoin

from pymonzo import MonzoAPI
from pymonzo import config
from pymonzo.api_objects import MonzoAccount, MonzoBalance, MonzoPot, MonzoTransaction


class TestMonzoAPI:
    """
    Test `monzo_api.MonzoAPI` class.
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
        """
        Test class `__init__` method.
        Quite long and complicated because of the number of possible
        scenarios. Possibly to revisit in the future.
        """
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
        mocked_save_token_on_disk = mocker.patch(
            'pymonzo.monzo_api.MonzoAPI._save_token_on_disk'
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
        mocked_save_token_on_disk.assert_called_once_with()
        mocked_oauth2_session.assert_called_once_with(
            client_id='explicit_client_id',
            token=expected_token,
        )

        # Don't pass anything explicitly and the token file exists
        mocked_oauth2_session = mocker.patch('pymonzo.monzo_api.OAuth2Session')
        mocker.patch('os.path.isfile', return_value=True)
        mocked_open = mocker.patch('codecs.open', mocker.mock_open())
        mocked_json_load = mocker.patch('json.load')
        expected_token = mocked_json_load.return_value

        monzo = MonzoAPI()

        assert monzo._access_token is None
        assert monzo._client_id is expected_token['client_id']
        assert monzo._client_secret is expected_token['client_secret']
        assert monzo._auth_code is None
        assert monzo._token == expected_token
        mocked_open.assert_called_once_with(
            config.TOKEN_FILE_PATH, 'r', 'utf-8',
        )
        mocked_json_load.assert_called_once_with(mocked_open.return_value)
        mocked_get_oauth_token.assert_called_once_with()
        mocked_oauth2_session.assert_called_once_with(
            client_id=expected_token['client_id'],
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
        mocked_save_token_on_disk = mocker.patch(
            'pymonzo.monzo_api.MonzoAPI._save_token_on_disk'
        )
        expected_token = mocked_get_oauth_token.return_value

        monzo = MonzoAPI()

        assert monzo._access_token is None
        assert monzo._client_id == 'env_client_id'
        assert monzo._client_secret == 'env_client_secret'
        assert monzo._auth_code == 'env_auth_code'
        assert monzo._token == expected_token
        mocked_get_oauth_token.assert_called_once_with()
        mocked_save_token_on_disk.assert_called_once_with()
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

    def test_class_save_token_on_disk_method(self, monzo):
        """Test class `_save_token_on_disk` method"""
        config.TOKEN_FILE_PATH = os.path.join(
            tempfile.gettempdir(), 'pymonzo_test',
        )

        monzo._token = {
            'foo': u'UNICODE',
            'bar': 1,
            'baz': False,
        }

        expected_token = monzo._token.copy()
        expected_token.update(client_secret=monzo._client_secret)

        monzo._save_token_on_disk()

        with codecs.open(config.TOKEN_FILE_PATH, 'r', 'utf-8') as f:
            assert json.load(f) == expected_token

    def test_class_get_oauth_token_method(self, mocker, mocked_monzo):
        """Test class `_get_oauth_token` method"""
        mocked_fetch_token = mocker.MagicMock()
        mocked_oauth2_session = mocker.patch('pymonzo.monzo_api.OAuth2Session')
        mocked_oauth2_session.return_value.fetch_token = mocked_fetch_token

        token = mocked_monzo._get_oauth_token()

        assert token == mocked_fetch_token.return_value

        mocked_oauth2_session.assert_called_once_with(
            client_id=mocked_monzo._client_id,
            redirect_uri=config.REDIRECT_URI,
        )
        mocked_fetch_token.assert_called_once_with(
            token_url=urljoin(mocked_monzo.api_url, '/oauth2/token'),
            code=mocked_monzo._auth_code,
            client_secret=mocked_monzo._client_secret,
        )

    def test_class_refresh_oath_token_method(self, mocker, mocked_monzo):
        """Test class `_refresh_oath_token` method"""
        mocked_requests_post_json = mocker.MagicMock()
        mocked_requests_post = mocker.patch('pymonzo.monzo_api.requests.post')
        mocked_requests_post.return_value.json = mocked_requests_post_json
        mocked_save_token_on_disk = mocker.patch(
            'pymonzo.monzo_api.MonzoAPI._save_token_on_disk'
        )

        expected_data = {
            'grant_type': 'refresh_token',
            'client_id': mocked_monzo._client_id,
            'client_secret': mocked_monzo._client_secret,
            'refresh_token': mocked_monzo._token['refresh_token'],
        }

        mocked_monzo._refresh_oath_token()

        assert mocked_monzo._token == mocked_requests_post_json.return_value

        mocked_requests_post.assert_called_once_with(
            urljoin(mocked_monzo.api_url, '/oauth2/token'),
            data=expected_data,
        )
        mocked_requests_post_json.assert_called_once_with()
        mocked_save_token_on_disk.assert_called_once_with()

    def test_class_whoami_method(self, mocker, mocked_monzo):
        """Test class `whoami` method"""
        mocked_get_response = mocker.patch(
            'pymonzo.monzo_api.MonzoAPI._get_response',
        )

        result = mocked_monzo.whoami()

        mocked_get_response.assert_called_once_with(
            method='get', endpoint='/ping/whoami',
        )

        expected_result = mocked_get_response.return_value.json.return_value

        assert result == expected_result

    def test_class_accounts_method(self, mocker, mocked_monzo, accounts_api_response):
        """Test class `accounts` method"""
        mocked_get_response = mocker.patch(
            'pymonzo.monzo_api.MonzoAPI._get_response',
        )
        mocked_get_response.return_value.json.return_value = accounts_api_response

        assert mocked_monzo._cached_accounts is None

        result = mocked_monzo.accounts()

        mocked_get_response.assert_called_once_with(
            method='get', endpoint='/accounts',
        )

        accounts_json = accounts_api_response['accounts']
        expected_result = [
            MonzoAccount(data=account) for account in accounts_json
        ]

        assert result == expected_result
        assert mocked_monzo._cached_accounts == expected_result

        # Calling it again should fetch '_cached_accounts'
        mocked_get_response = mocker.patch(
            'pymonzo.monzo_api.MonzoAPI._get_response',
        )
        mocked_get_response.return_value.json.return_value = accounts_api_response

        result = mocked_monzo.accounts()

        assert mocked_get_response.call_count == 0

        assert result == mocked_monzo._cached_accounts

        # But calling it with 'refresh=True' should do an API request
        mocked_get_response = mocker.patch(
            'pymonzo.monzo_api.MonzoAPI._get_response',
        )
        mocked_get_response.return_value.json.return_value = accounts_api_response

        assert mocked_monzo._cached_accounts is not None

        result = mocked_monzo.accounts(refresh=True)

        mocked_get_response.assert_called_once_with(
            method='get', endpoint='/accounts',
        )

        accounts_json = accounts_api_response['accounts']
        expected_result = [
            MonzoAccount(data=account) for account in accounts_json
        ]

        assert result == expected_result
        assert mocked_monzo._cached_accounts == expected_result

    def test_class_balance_method(self, mocker, mocked_monzo,
                                  balance_api_response, accounts_api_response):
        """Test class `balance` method"""
        mocked_get_response = mocker.patch(
            'pymonzo.monzo_api.MonzoAPI._get_response',
        )
        mocked_get_response.return_value.json.return_value = balance_api_response

        accounts_json = accounts_api_response['accounts']
        mocked_monzo._cached_accounts = [
            MonzoAccount(data=account) for account in accounts_json
        ]

        result = mocked_monzo.balance()

        mocked_get_response.assert_called_once_with(
            method='get',
            endpoint='/balance',
            params={
                'account_id': mocked_monzo._cached_accounts[0].id,
            },
        )

        expected_result = MonzoBalance(balance_api_response)

        assert result == expected_result

        # It should raise an 'ValueError' if there more (or less) then 1 account
        mocked_monzo._cached_accounts = mocked_monzo._cached_accounts * 2

        with pytest.raises(ValueError):
            mocked_monzo.balance()

    def test_class_pots_method(self, mocker, mocked_monzo, pots_api_response):
        """Test class `pots` method"""
        mocked_get_response = mocker.patch(
            'pymonzo.monzo_api.MonzoAPI._get_response',
        )
        mocked_get_response.return_value.json.return_value = pots_api_response

        assert mocked_monzo._cached_pots is None

        result = mocked_monzo.pots()

        mocked_get_response.assert_called_once_with(
            method='get', endpoint='/pots/listV1',
        )

        pots_json = pots_api_response['pots']
        expected_result = [MonzoPot(data=pot) for pot in pots_json]

        assert result == expected_result
        assert mocked_monzo._cached_pots == expected_result

        # Calling it again should fetch '_cached_pots'
        mocked_get_response = mocker.patch(
            'pymonzo.monzo_api.MonzoAPI._get_response',
        )
        mocked_get_response.return_value.json.return_value = pots_api_response

        result = mocked_monzo.pots()

        assert mocked_get_response.call_count == 0

        assert result == mocked_monzo._cached_pots

        # But calling it with 'refresh=True' should do an API request
        mocked_get_response = mocker.patch(
            'pymonzo.monzo_api.MonzoAPI._get_response',
        )
        mocked_get_response.return_value.json.return_value = pots_api_response

        assert mocked_monzo._cached_pots is not None

        result = mocked_monzo.pots(refresh=True)

        mocked_get_response.assert_called_once_with(
            method='get', endpoint='/pots/listV1',
        )

        pots_json = pots_api_response['pots']
        expected_result = [MonzoPot(data=pot) for pot in pots_json]

        assert result == expected_result
        assert mocked_monzo._cached_pots == expected_result

    def test_class_transactions_method(self, mocker, mocked_monzo,
                                       transactions_api_response, accounts_api_response):
        """Test class `transactions` method"""
        mocked_get_response = mocker.patch(
            'pymonzo.monzo_api.MonzoAPI._get_response',
        )
        mocked_get_response.return_value.json.return_value = transactions_api_response

        accounts_json = accounts_api_response['accounts']
        mocked_monzo._cached_accounts = [
            MonzoAccount(data=account) for account in accounts_json
        ]

        result = mocked_monzo.transactions()

        mocked_get_response.assert_called_once_with(
            method='get',
            endpoint='/transactions',
            params={
                'account_id': mocked_monzo._cached_accounts[0].id,
            },
        )

        transactions_json = transactions_api_response['transactions']
        expected_result = [
            MonzoTransaction(data=transaction) for transaction in transactions_json
        ]

        assert result == expected_result

        # It should raise an 'ValueError' if there more (or less) then 1 account
        mocked_monzo._cached_accounts = mocked_monzo._cached_accounts * 2

        with pytest.raises(ValueError):
            mocked_monzo.transactions()

    def test_class_transaction_method(self, mocker, mocked_monzo, transaction_api_response):
        """Test class `transaction` method"""
        mocked_get_response = mocker.patch(
            'pymonzo.monzo_api.MonzoAPI._get_response',
        )
        mocked_get_response.return_value.json.return_value = transaction_api_response

        result = mocked_monzo.transaction('foobar')

        mocked_get_response.assert_called_once_with(
            method='get',
            endpoint='/transactions/foobar',
            params={},
        )

        expected_result = MonzoTransaction(transaction_api_response['transaction'])

        assert result == expected_result

        # With expanded merchant info
        mocked_get_response = mocker.patch(
            'pymonzo.monzo_api.MonzoAPI._get_response',
        )
        mocked_get_response.return_value.json.return_value = transaction_api_response

        result = mocked_monzo.transaction('foobar', expand_merchant=True)

        mocked_get_response.assert_called_once_with(
            method='get',
            endpoint='/transactions/foobar',
            params={
                'expand[]': 'merchant',
            },
        )

        expected_result = MonzoTransaction(transaction_api_response['transaction'])

        assert result == expected_result

    def test_class_create_feed_item_method(self, mocker, mocked_monzo, accounts_api_response):
        """Test class `create_feed_item` method"""
        mocked_get_response = mocker.patch(
            'pymonzo.monzo_api.MonzoAPI._get_response',
        )
        mocked_get_response.return_value.json.return_value = None

        title = "title"
        image_url = "https://example.com/image_url"
        body = "body"
        background_color = "background_color"
        title_color = "title_color"
        body_color = "body_color"
        url = "https://example.com/url"

        mocked_monzo.create_feed_item(accounts_api_response['accounts'][0]['id'], title, image_url,
                                      body, background_color, title_color, body_color, url)

        mocked_get_response.assert_called_once_with(
            method='post',
            endpoint='/feed',
            body={
                'account_id': accounts_api_response['accounts'][0]['id'],
                'type': 'basic',
                'params[title]': title,
                'params[image_url]': image_url,
                'url': url,
                'params[body]': body,
                'params[background_color]': background_color,
                'params[title_color]': title_color,
                'params[body_color]': body_color,
            },
        )
