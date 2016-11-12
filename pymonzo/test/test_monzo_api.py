# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
from uuid import uuid4

import pytest

from pymonzo import MonzoAPI
from pymonzo.monzo_api import MONZO_ACCESS_TOKEN


# Fixtures
@pytest.fixture(scope='function')
def monzo_api():
    """Create a MonzoAPI instance"""
    return MonzoAPI()


# Tests
def test_init_access_token(monkeypatch):
    """Test access token initializing in MonzoAPI"""
    # Get access token from environment variable
    assert MonzoAPI(access_token=None)

    # Pass access token explicitly
    access_token = os.environ['MONZO_ACCESS_TOKEN']
    monzo_api = MonzoAPI(access_token=access_token)
    assert monzo_api
    assert monzo_api._access_token == access_token

    # Incorrect access token
    with pytest.raises(ValueError):
        monkeypatch.undo()
        monkeypatch.delenv(MONZO_ACCESS_TOKEN, raising=False)
        MonzoAPI(access_token=str(uuid4()))

    # Incorrect access token from environment variable
    with pytest.raises(ValueError):
        monkeypatch.undo()
        monkeypatch.setenv(MONZO_ACCESS_TOKEN, str(uuid4()))
        MonzoAPI()

    # No access token
    with pytest.raises(ValueError):
        monkeypatch.undo()
        monkeypatch.delenv(MONZO_ACCESS_TOKEN, raising=False)
        MonzoAPI()


def test_init_session(monzo_api):
    """Test default account ID initializing in MonzoAPI"""
    assert monzo_api.session
    assert 'Authorization' in monzo_api.session.headers


def test_init_default_account_id(monzo_api):
    """Test default account ID initializing in MonzoAPI"""
    assert monzo_api.default_account_id == monzo_api.accounts()[0]['id']

    # Passing default account ID explicitly
    account_id = monzo_api.accounts()[0]['id']
    monzo_api = MonzoAPI(default_account_id=account_id)
    assert monzo_api.default_account_id == account_id


def test_whoami(monzo_api):
    """Test MonzoAPI.whoami() method"""
    assert monzo_api.whoami()


def test_accounts(monzo_api):
    """Test MonzoAPI.accounts() method"""
    assert monzo_api.accounts()


def test_balance(monzo_api):
    """Test MonzoAPI.balance() method"""
    assert monzo_api.balance()

    # No account ID provided
    with pytest.raises(ValueError):
        monzo_api.default_account_id = None
        monzo_api.balance()


def test_transactions(monzo_api):
    """Test MonzoAPI.transactions() method"""
    transactions = monzo_api.transactions()
    assert transactions

    # Limit results
    assert len(monzo_api.transactions(limit=5)) == 5

    # No real way to test reverse, but make sure it does _something_
    transactions_reverse = monzo_api.transactions(reverse=True)
    assert transactions is not transactions_reverse

    # No account ID provided
    with pytest.raises(ValueError):
        monzo_api.default_account_id = None
        monzo_api.transactions()


def test_transaction(monzo_api):
    """Test MonzoAPI.transaction() method"""
    transaction_id = monzo_api.transactions(limit=1)[0]['id']

    transaction = monzo_api.transaction(transaction_id=transaction_id)
    assert transaction

    transaction_expand_merchant = monzo_api.transaction(
        transaction_id=transaction_id, expand_merchant=True,
    )
    assert transaction_expand_merchant

    # No real way to test reverse, but make sure it does _something_
    assert transaction is not transaction_expand_merchant
