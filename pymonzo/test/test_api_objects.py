# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from abc import ABCMeta
from datetime import datetime

from pymonzo import api_objects
from pymonzo.test import sample_api_responses


def test_monzo_object():
    """Test `MonzoObject`"""
    assert isinstance(api_objects.MonzoObject, ABCMeta)
    assert hasattr(api_objects.MonzoObject, '_required_keys')


def test_monzo_account():
    """Test `MonzoAccount`"""
    monzo_account = api_objects.MonzoAccount(
        data=sample_api_responses.ACCOUNTS_API_RESPONSE['accounts'][0]
    )

    assert monzo_account
    assert isinstance(monzo_account.created, datetime)


def test_monzo_balance():
    """Test `MonzoBalance`"""
    monzo_balance = api_objects.MonzoBalance(
        data=sample_api_responses.BALANCE_API_RESPONSE
    )

    assert monzo_balance


def test_monzo_transaction():
    """Test `MonzoTransaction`"""
    transaction = api_objects.MonzoTransaction(
        data=sample_api_responses.TRANSACTION_API_RESPONSE['transaction']
    )

    assert transaction

    if transaction.settled:
        assert isinstance(transaction.settled, datetime)

    if transaction.merchant:
        assert isinstance(transaction.merchant, api_objects.MonzoMerchant)
        assert isinstance(transaction.merchant.created, datetime)
