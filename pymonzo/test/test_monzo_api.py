# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

import pytest
from requests_oauthlib import OAuth2Session

from pymonzo import MonzoAPI
from pymonzo.monzo_api import MONZO_ACCESS_CODE_ENV


# Fixtures
@pytest.fixture(scope='function')
def monzo_api():
    """Create a `MonzoAPI` instance"""
    return MonzoAPI()


# Tests
@pytest.mark.parametrize('access_token', [
    None,
    os.environ.get(MONZO_ACCESS_CODE_ENV),
])
def test_init_access_token(access_token):
    """Test initialization with provided `access_token`"""
    monzo_api = MonzoAPI(access_token=access_token)

    assert monzo_api
    assert monzo_api._token['access_token'] == os.environ.get(
        MONZO_ACCESS_CODE_ENV
    )
    assert monzo_api._token['token_type'] == 'Bearer'


def test_init_no_data(monkeypatch):
    """Test initialization with no `access_token`"""
    monkeypatch.delenv(MONZO_ACCESS_CODE_ENV, raising=False)

    with pytest.raises(ValueError):
        MonzoAPI()


def test_init_authorization_code(mocker, monkeypatch):
    """
    Test initialization with `client_id`, `client_secret` and `auth_code`
    """
    mocked_get_oauth_token = mocker.patch.object(MonzoAPI, '_get_oauth_token')
    mocked_get_oauth_token.return_value = {
        'access_token': os.environ.get(MONZO_ACCESS_CODE_ENV),
        'token_type': 'Bearer',
    }

    monkeypatch.delenv(MONZO_ACCESS_CODE_ENV, raising=False)

    MonzoAPI(
        client_id='MONZO_CLIENT_ID',
        client_secret='MONZO_CLIENT_SECRET_ENV',
        auth_code='MONZO_AUTH_CODE_ENV',
    )

    assert mocked_get_oauth_token.called
    assert mocked_get_oauth_token.call_count == 1


def test_init_session(monzo_api):
    """Test session initialization"""
    assert monzo_api.session
    assert monzo_api.session.token
    assert isinstance(monzo_api.session, OAuth2Session)


def test_init_default_account_id(monzo_api):
    """Test setting the default account ID on initialization"""
    assert monzo_api.default_account_id == monzo_api.accounts()[0]['id']


def test_whoami(monzo_api):
    """Test `whoami()` method"""
    assert monzo_api.whoami()


def test_accounts(monzo_api):
    """Test `accounts()` method"""
    assert monzo_api.accounts()


def test_balance(monzo_api):
    """Test `balance()` method"""
    assert monzo_api.balance()

    # No account ID provided
    with pytest.raises(ValueError):
        monzo_api.default_account_id = None
        monzo_api.balance()


def test_transactions(monzo_api):
    """Test `transactions()` method"""
    transactions = monzo_api.transactions()
    assert transactions

    # Limit results
    assert len(monzo_api.transactions(limit=5)) == 5

    # No easy way to test reverse so lets just make sure it does _something_
    transactions_reverse = monzo_api.transactions(reverse=True)
    assert transactions is not transactions_reverse

    # No account ID provided
    with pytest.raises(ValueError):
        monzo_api.default_account_id = None
        monzo_api.transactions()


def test_transaction(monzo_api):
    """Test `transaction()` method"""
    transaction_id = monzo_api.transactions(limit=1)[0]['id']

    transaction = monzo_api.transaction(transaction_id=transaction_id)
    assert transaction

    transaction_expand_merchant = monzo_api.transaction(
        transaction_id=transaction_id, expand_merchant=True,
    )
    assert transaction_expand_merchant

    # No easy way to test reverse so lets just make sure it does _something_
    assert transaction is not transaction_expand_merchant
