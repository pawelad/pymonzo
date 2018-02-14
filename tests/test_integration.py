# -*- coding: utf-8 -*-
"""
Monzo integration tests. Made possible with the awesome VCR.py library.
"""
from __future__ import unicode_literals

import pytest
import six

from pymonzo import MonzoAPI
from pymonzo.api_objects import (
    MonzoAccount, MonzoBalance, MonzoTransaction, MonzoMerchant,
)
from pymonzo.api_objects import MonzoPot


class TestMonzoAPIIntegration:
    """
    Monzo API integration tests.
    """
    @pytest.fixture(scope='session')
    def monzo(self):
        """Helper fixture that returns a `MonzoAPI` instance"""
        return MonzoAPI(access_token='explicit_access_token')

    @pytest.mark.vcr()
    def test_whoami_method(self, monzo):
        """Test class `whoami` method"""
        whoami = monzo.whoami()

        assert whoami
        assert isinstance(whoami, dict)

        assert 'authenticated' in whoami
        assert 'client_id' in whoami
        assert 'user_id' in whoami

    @pytest.mark.vcr()
    def test_accounts_method(self, monzo):
        """Test class `accounts` method"""
        accounts = monzo.accounts()

        assert accounts
        assert isinstance(accounts, list)
        assert all([isinstance(i, MonzoAccount) for i in accounts])

    @pytest.mark.vcr()
    def test_pots_method(self, monzo):
        """Test class `pots` method"""
        pots = monzo.pots()

        assert pots
        assert isinstance(pots, list)
        assert all([isinstance(i, MonzoPot) for i in pots])

    @pytest.mark.vcr()
    def test_balance_method(self, monzo):
        """Test class `balance` method"""
        balance = monzo.balance()

        assert balance
        assert isinstance(balance, MonzoBalance)

    @pytest.mark.vcr()
    def test_transactions_method(self, monzo):
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
    def test_transaction_method(self, monzo):
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
