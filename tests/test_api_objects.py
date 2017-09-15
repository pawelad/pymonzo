# -*- coding: utf-8 -*-
"""
Test 'pymonzo.api_objects' file
"""
from __future__ import unicode_literals

from datetime import datetime

import pytest
from dateutil.parser import parse as parse_date

from pymonzo import api_objects
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
        assert vars(instance) == expected_data
        assert isinstance(instance.created, datetime)

    def test_class_lack_of_required_keys(self, mocker, data):
        """Test class `__init__` method when data lack one of required keys"""
        mocker.patch.multiple(self.klass, _required_keys='baz')

        with pytest.raises(ValueError):
            self.klass(data=data)


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

        assert vars(instance) == expected_data

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
        assert vars(instance) == expected_data

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
        assert vars(instance) == expected_data
        assert isinstance(instance.created, datetime)

    def test_class_lack_of_required_keys(self, mocker, data):
        """Test class `__init__` method when data lack one of required keys"""
        mocker.patch.multiple(self.klass, _required_keys='baz')

        with pytest.raises(ValueError):
            self.klass(data=data)
