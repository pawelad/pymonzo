# -*- coding: utf-8 -*-
"""
Test 'pymonzo.api_objects' file
"""
from __future__ import unicode_literals

from datetime import datetime

import pytest
from dateutil.parser import parse as parse_date

from pymonzo import api_objects, MonzoAPI
from pymonzo.api_objects import MonzoAccount, MonzoPot
from pymonzo.utils import CommonMixin


class TestMonzoObject:
    """
    Test `api_objects.MonzoObject` class
    """
    klass = api_objects.MonzoObject
    data = {
        'foo': 'foo',
        'bar': 'bar',
    }

    @pytest.fixture(scope='session')
    def instance(self):
        """Simple fixture that returns initialize object"""
        return self.klass(data=self.data)

    def test_class_inheritance(self, instance):
        """Test class inheritance"""
        assert isinstance(instance, api_objects.MonzoObject)
        assert isinstance(instance, CommonMixin)

    def test_class_properties(self, instance):
        """Test class properties"""
        assert self.klass._required_keys == []
        assert instance._required_keys == []

    def test_class_initialization(self, instance):
        """Test class `__init__` method"""
        assert instance._raw_data == self.data
        assert instance.foo == 'foo'
        assert instance.bar == 'bar'

    def test_class_lack_of_required_keys(self, mocker):
        """Test class `__init__` method when data lack one of required keys"""
        mocker.patch.multiple(self.klass, _required_keys='baz')

        with pytest.raises(ValueError):
            self.klass(data=self.data)


class TestMonzoAccount:
    """
    Test `api_objects.MonzoAccount` class
    """
    klass = api_objects.MonzoAccount

    @pytest.fixture(scope='session')
    def data(self, accounts_api_response):
        """Simple fixture that returns data used to initialize the object"""
        return accounts_api_response['accounts'][0]

    @pytest.fixture(scope='session')
    def instance(self, data):
        """Simple fixture that returns initialize object"""
        return self.klass(data)

    def test_class_inheritance(self, instance):
        """Test class inheritance"""
        assert isinstance(instance, api_objects.MonzoAccount)
        assert isinstance(instance, api_objects.MonzoObject)

    def test_class_properties(self, instance):
        """Test class properties"""
        expected_keys = ['id', 'description', 'created']
        assert self.klass._required_keys == expected_keys
        assert instance._required_keys == expected_keys

    def test_class_initialization(self, instance, data):
        """Test class `__init__` method"""
        expected_data = data.copy()

        assert instance._raw_data == data
        del instance._raw_data

        expected_data['created'] = parse_date(expected_data['created'])

        orig_instance_vars = vars(instance)
        instance_vars = orig_instance_vars.copy()
        # Don't inspect private variables
        for k in orig_instance_vars.keys():
            if k.startswith('_'):
                instance_vars.pop(k)

        assert instance_vars == expected_data
        assert isinstance(instance.created, datetime)

    def test_class_lack_of_required_keys(self, mocker, data):
        """Test class `__init__` method when data lack one of required keys"""
        mocker.patch.multiple(self.klass, _required_keys='baz')

        with pytest.raises(ValueError):
            self.klass(data=data)


class TestMonzoPot:
    """
    Test `api_objects.MonzoPot` class
    """
    klass = api_objects.MonzoPot

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

    @pytest.fixture(scope='session')
    def data(self, pots_api_response):
        """Simple fixture that returns data used to initialize the object"""
        return pots_api_response['pots'][0]

    @pytest.fixture(scope='session')
    def instance(self, data):
        """Simple fixture that returns initialize object"""
        return self.klass(data)

    def test_class_inheritance(self, instance):
        """Test class inheritance"""
        assert isinstance(instance, api_objects.MonzoPot)
        assert isinstance(instance, api_objects.MonzoObject)

    def test_class_properties(self, instance):
        """Test class properties"""
        expected_keys = [
            'id', 'name', 'created', 'style', 'balance', 'currency', 'updated', 'deleted'
        ]
        assert self.klass._required_keys == expected_keys
        assert instance._required_keys == expected_keys

    def test_class_initialization(self, instance, data):
        """Test class `__init__` method"""
        expected_data = data.copy()

        assert instance._raw_data == data
        del instance._raw_data

        expected_data['created'] = parse_date(expected_data['created'])
        orig_instance_vars = vars(instance)
        instance_vars = orig_instance_vars.copy()
        # Don't inspect private variables
        for k in orig_instance_vars.keys():
            if k.startswith('_'):
                instance_vars.pop(k)

        assert instance_vars == expected_data
        assert isinstance(instance.created, datetime)

    def test_class_lack_of_required_keys(self, mocker, data):
        """Test class `__init__` method when data lack one of required keys"""
        mocker.patch.multiple(self.klass, _required_keys='baz')

        with pytest.raises(ValueError):
            self.klass(data=data)

    def test_class_deposit_method(self, mocker, mocked_monzo,
                                  pots_api_response, accounts_api_response):
        """Test class `add` method"""
        mocked_get_response = mocker.patch(
            'pymonzo.monzo_api.MonzoAPI._get_response',
        )
        mocked_get_response.return_value.json.return_value = pots_api_response['pots'][0]

        accounts_json = accounts_api_response['accounts']
        pots_json = pots_api_response['pots']

        mocked_monzo._cached_accounts = [
            MonzoAccount(data=account, context=mocked_monzo) for account in accounts_json
        ]
        mocked_monzo._cached_pots = [
            MonzoPot(data=pot, context=mocked_monzo) for pot in pots_json
        ]

        pot = mocked_monzo.pots()[0]

        expected_result = pot
        expected_result.balance = 50000

        result = pot.deposit(37655, mocked_monzo._cached_accounts[0], "abc")

        mocked_get_response.assert_called_once_with(
            method='put',
            endpoint='/pots/'+mocked_monzo._cached_pots[0].id+'/deposit',
            body={
                'source_account_id': mocked_monzo._cached_accounts[0].id,
                'amount': 37655,
                'dedupe_id': "abc",
            },
        )

        assert result is None
        assert pot == expected_result

    def test_class_withdraw_method(self, mocker, mocked_monzo,
                                   pots_api_response, accounts_api_response):
        """Test class `add` method"""
        mocked_get_response = mocker.patch(
            'pymonzo.monzo_api.MonzoAPI._get_response',
        )
        mocked_get_response.return_value.json.return_value = pots_api_response['pots'][0]

        accounts_json = accounts_api_response['accounts']
        pots_json = pots_api_response['pots']

        mocked_monzo._cached_accounts = [
            MonzoAccount(data=account, context=mocked_monzo) for account in accounts_json
        ]
        mocked_monzo._cached_pots = [
            MonzoPot(data=pot, context=mocked_monzo) for pot in pots_json
        ]

        pot = mocked_monzo.pots()[0]

        expected_result = pot
        expected_result.balance = 2500

        result = pot.withdraw(9845, mocked_monzo._cached_accounts[0], "abc")

        mocked_get_response.assert_called_once_with(
            method='put',
            endpoint='/pots/'+mocked_monzo._cached_pots[0].id+'/withdraw',
            body={
                'destination_account_id': mocked_monzo._cached_accounts[0].id,
                'amount': 9845,
                'dedupe_id': "abc",
            },
        )

        assert result is None
        assert pot == expected_result


class TestMonzoBalance:
    """
    Test `api_objects.MonzoBalance` class
    """
    klass = api_objects.MonzoBalance

    @pytest.fixture(scope='session')
    def data(self, balance_api_response):
        """Simple fixture that returns data used to initialize the object"""
        return balance_api_response

    @pytest.fixture(scope='session')
    def instance(self, data):
        """Simple fixture that returns initialize object"""
        return self.klass(data)

    def test_class_inheritance(self, instance):
        """Test class inheritance"""
        assert isinstance(instance, api_objects.MonzoBalance)
        assert isinstance(instance, api_objects.MonzoObject)

    def test_class_properties(self, instance):
        """Test class properties"""
        expected_keys = ['balance', 'currency', 'spend_today']
        assert self.klass._required_keys == expected_keys
        assert instance._required_keys == expected_keys

    def test_class_initialization(self, instance, data):
        """Test class `__init__` method"""
        expected_data = data.copy()

        assert instance._raw_data == expected_data
        del instance._raw_data

        orig_instance_vars = vars(instance)
        instance_vars = orig_instance_vars.copy()
        # Don't inspect private variables
        for k in orig_instance_vars.keys():
            if k.startswith('_'):
                instance_vars.pop(k)

        assert instance_vars == expected_data

    def test_class_lack_of_required_keys(self, mocker, data):
        """Test class `__init__` method when data lack one of required keys"""
        mocker.patch.multiple(self.klass, _required_keys='baz')

        with pytest.raises(ValueError):
            self.klass(data=data)


class TestMonzoTransaction:
    """
    Test `api_objects.MonzoTransaction` class
    """
    klass = api_objects.MonzoTransaction

    @pytest.fixture(scope='session')
    def data(self, transaction_api_response):
        """Simple fixture that returns data used to initialize the object"""
        return transaction_api_response['transaction']

    @pytest.fixture(scope='session')
    def instance(self, data):
        """Simple fixture that returns initialize object"""
        return self.klass(data)

    def test_class_inheritance(self, instance):
        """Test class inheritance"""
        assert isinstance(instance, api_objects.MonzoTransaction)
        assert isinstance(instance, api_objects.MonzoObject)

    def test_class_properties(self, instance):
        """Test class properties"""
        expected_keys = [
            'account_balance', 'amount', 'created', 'currency', 'description',
            'id', 'merchant', 'metadata', 'notes', 'is_load',
        ]

        assert self.klass._required_keys == expected_keys
        assert instance._required_keys == expected_keys

    def test_class_initialization(self, instance, data):
        """Test class `__init__` method"""
        expected_data = data.copy()

        assert instance._raw_data == expected_data
        del instance._raw_data

        expected_data['created'] = parse_date(expected_data['created'])
        expected_data['settled'] = parse_date(expected_data['settled'])
        expected_data['merchant'] = api_objects.MonzoMerchant(
            data=expected_data['merchant']
        )

        orig_instance_vars = vars(instance)
        instance_vars = orig_instance_vars.copy()
        # Don't inspect private variables
        for k in orig_instance_vars.keys():
            if k.startswith('_'):
                instance_vars.pop(k)

        assert instance_vars == expected_data

        assert isinstance(instance.created, datetime)
        assert isinstance(instance.settled, datetime)
        assert isinstance(instance.merchant, api_objects.MonzoMerchant)

    def test_class_lack_of_required_keys(self, mocker, data):
        """Test class `__init__` method when data lack one of required keys"""
        mocker.patch.multiple(self.klass, _required_keys='baz')

        with pytest.raises(ValueError):
            self.klass(data=data)


class TestMonzoMerchant:
    """
    Test `api_objects.MonzoMerchant` class
    """
    klass = api_objects.MonzoMerchant

    @pytest.fixture(scope='session')
    def data(self, transaction_api_response):
        """Simple fixture that returns data used to initialize the object"""
        return transaction_api_response['transaction']['merchant']

    @pytest.fixture(scope='session')
    def instance(self, data):
        """Simple fixture that returns initialize object"""
        return self.klass(data)

    def test_class_inheritance(self, instance):
        """Test class inheritance"""
        assert isinstance(instance, api_objects.MonzoMerchant)
        assert isinstance(instance, api_objects.MonzoObject)

    def test_class_properties(self, instance):
        """Test class properties"""
        expected_keys = [
            'address', 'created', 'group_id', 'id',
            'logo', 'emoji', 'name', 'category',
        ]

        assert self.klass._required_keys == expected_keys
        assert instance._required_keys == expected_keys

    def test_class_initialization(self, instance, data):
        """Test class `__init__` method"""
        expected_data = data.copy()

        assert instance._raw_data == expected_data
        del instance._raw_data

        expected_data['created'] = parse_date(expected_data['created'])
        orig_instance_vars = vars(instance)
        instance_vars = orig_instance_vars.copy()
        # Don't inspect private variables
        for k in orig_instance_vars.keys():
            if k.startswith('_'):
                instance_vars.pop(k)

        assert instance_vars == expected_data
        assert isinstance(instance.created, datetime)

    def test_class_lack_of_required_keys(self, mocker, data):
        """Test class `__init__` method when data lack one of required keys"""
        mocker.patch.multiple(self.klass, _required_keys='baz')

        with pytest.raises(ValueError):
            self.klass(data=data)
