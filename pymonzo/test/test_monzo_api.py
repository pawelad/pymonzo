# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from uuid import uuid4

import pytest
import six
from requests_oauthlib import OAuth2Session

from pymonzo import MonzoAPI
from pymonzo.exceptions import MonzoAPIException
from pymonzo.api_objects import (
    MonzoAccount, MonzoBalance, MonzoTransaction, MonzoMerchant,
)
from pymonzo.monzo_api import (
    MONZO_ACCESS_TOKEN_ENV, MONZO_AUTH_CODE_ENV,
    MONZO_CLIENT_ID_ENV, MONZO_CLIENT_SECRET_ENV,
)


# Fixtures
@pytest.fixture(scope='function')
def monzo():
    """Create a `MonzoAPI` instance"""
    return MonzoAPI(access_token=os.environ.get(MONZO_ACCESS_TOKEN_ENV))


# Tests
@pytest.mark.parametrize('access_token', [
    None,
    os.environ.get(MONZO_ACCESS_TOKEN_ENV),
])
def test_init_access_token(monkeypatch, mocker, access_token):
    """Test initialization with only `access_token` provided"""
    # Make sure that other auth options are invalid
    monkeypatch.delenv(MONZO_AUTH_CODE_ENV, raising=False)
    monkeypatch.delenv(MONZO_CLIENT_ID_ENV, raising=False)
    monkeypatch.delenv(MONZO_CLIENT_SECRET_ENV, raising=False)
    is_file = mocker.patch('os.path.isfile')
    is_file.return_value = False

    monzo = MonzoAPI(access_token=access_token)

    assert monzo
    assert monzo._token['access_token'] == os.environ.get(
        MONZO_ACCESS_TOKEN_ENV
    )
    assert monzo._token['token_type'] == 'Bearer'


@pytest.mark.parametrize('client_id,client_secret,auth_code', [
    (None, None, None),
    (str(uuid4), str(uuid4), str(uuid4)),
])
def test_init_oauth(monkeypatch, mocker, client_id, client_secret, auth_code):
    """
    Test initialization with `client_id`, `client_secret` and `auth_code`
    """
    # Mock request that gets the OAuth token
    mocked_get_oauth_token = mocker.patch.object(MonzoAPI, '_get_oauth_token')
    mocked_get_oauth_token.return_value = {
        'access_token': os.environ.get(MONZO_ACCESS_TOKEN_ENV),
        'token_type': 'Bearer',
    }

    # Make sure that other auth options are invalid
    monkeypatch.delenv(MONZO_ACCESS_TOKEN_ENV, raising=False)
    is_file = mocker.patch('os.path.isfile')
    is_file.return_value = False

    # Set the environment variables
    monkeypatch.setenv(MONZO_CLIENT_ID_ENV, str(uuid4))
    monkeypatch.setenv(MONZO_CLIENT_SECRET_ENV, str(uuid4))
    monkeypatch.setenv(MONZO_AUTH_CODE_ENV, str(uuid4))

    monzo = MonzoAPI(
        client_id=client_id,
        client_secret=client_secret,
        auth_code=auth_code,
    )

    assert monzo
    assert mocked_get_oauth_token.called
    assert mocked_get_oauth_token.call_count == 1


def test_init_no_data(monkeypatch, mocker):
    """Test initialization with no auth data provided"""
    # Make sure that all auth options are invalid
    monkeypatch.delenv(MONZO_ACCESS_TOKEN_ENV, raising=False)
    monkeypatch.delenv(MONZO_AUTH_CODE_ENV, raising=False)
    monkeypatch.delenv(MONZO_CLIENT_ID_ENV, raising=False)
    monkeypatch.delenv(MONZO_CLIENT_SECRET_ENV, raising=False)
    is_file = mocker.patch('os.path.isfile')
    is_file.return_value = False

    with pytest.raises(ValueError):
        MonzoAPI()


def test_init_session(monzo):
    """Test session initialization"""
    assert monzo._session
    assert monzo._session.token
    assert isinstance(monzo._session, OAuth2Session)


def test_init_default_account_id(monzo):
    """Test setting the default account ID on initialization"""
    assert monzo.default_account_id == monzo.accounts()[0].id


def test_raising_exception():
    """Test API error caching and exception raising"""
    with pytest.raises(MonzoAPIException):
        MonzoAPI(access_token=str(uuid4))


def test_whoami(monzo):
    """Test `whoami()` method"""
    whoami = monzo.whoami()

    assert whoami
    assert isinstance(whoami, dict)


def test_accounts(monzo):
    """Test `accounts()` method"""
    accounts = monzo.accounts()

    assert accounts
    assert isinstance(accounts, list)
    assert all([isinstance(i, MonzoAccount) for i in accounts])


def test_balance(monzo):
    """Test `balance()` method"""
    balance = monzo.balance()

    assert balance
    assert isinstance(balance, MonzoBalance)

    # No account ID provided
    with pytest.raises(ValueError):
        monzo.default_account_id = None
        monzo.balance()


def test_transactions(monzo):
    """Test `transactions()` method"""
    transactions = monzo.transactions()

    assert transactions
    assert isinstance(transactions, list)
    assert all([isinstance(t, MonzoTransaction) for t in transactions])

    # Limit results
    assert len(monzo.transactions(limit=5)) == 5

    # Reverse results
    transactions_reverse = monzo.transactions(reverse=True)

    assert transactions_reverse
    assert isinstance(transactions_reverse, list)
    assert all([isinstance(t, MonzoTransaction) for t in transactions_reverse])
    # No easy way to test reverse so lets just make sure it does _something_
    assert transactions is not transactions_reverse

    # No account ID provided
    with pytest.raises(ValueError):
        monzo.default_account_id = None
        monzo.transactions()


def test_transaction(monzo):
    """Test `transaction()` method"""
    transaction_id = monzo.transactions(limit=1)[0].id

    transaction = monzo.transaction(transaction_id=transaction_id)

    assert transaction
    assert isinstance(transaction, MonzoTransaction)

    # Depends on what the latest transaction is and if it has a merchant
    if transaction.merchant:
        assert isinstance(transaction.merchant, six.text_type)

    # Expand merchant
    transaction_expand_merchant = monzo.transaction(
        transaction_id=transaction_id,
        expand_merchant=True,
    )

    assert transaction_expand_merchant
    assert isinstance(transaction_expand_merchant, MonzoTransaction)
    # Depends on what the latest transaction is and if it has a merchant
    if transaction_expand_merchant.merchant:
        assert isinstance(transaction_expand_merchant.merchant, MonzoMerchant)

    # No easy way to test reverse so lets just make sure it does _something_
    assert transaction is not transaction_expand_merchant
