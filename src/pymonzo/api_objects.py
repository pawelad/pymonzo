# -*- coding: utf-8 -*-
"""
Monzo API objects related code
"""
from __future__ import unicode_literals

import six
from dateutil.parser import parse as parse_date

from pymonzo.utils import CommonMixin


class MonzoObject(CommonMixin):
    """
    Base class for all Monzo API objects
    """
    _required_keys = []

    def __init__(self, data):
        """
        Takes Monzo API response data and maps the keys as class properties.
        It requires certain keys to be present to make sure we got the response
        we wanted.

        :param data: response from Monzo API request
        :type data: dict
        """
        missing_keys = [
            k for k in self._required_keys
            if k not in data
        ]
        if missing_keys:
            raise ValueError(
                "Passed data doesn't have all required keys "
                "(missing keys: {})".format(','.join(missing_keys))
            )

        self._raw_data = data.copy()
        data_copy = data.copy()

        # Take care of parsing non-standard fields
        self._parse_special_fields(data_copy)

        # Map the rest of the fields automatically
        self.__dict__.update(**data_copy)

    def _parse_special_fields(self, data):
        """
        Helper method that parses special fields to Python objects
        """
        pass


class MonzoAccount(MonzoObject):
    """
    Class representation of Monzo account
    """
    _required_keys = ['id', 'description', 'created']

    def _parse_special_fields(self, data):
        """
        Helper method that parses special fields to Python objects

        :param data: response from Monzo API request
        :type data: dict
        """
        self.created = parse_date(data.pop('created'))


class MonzoBalance(MonzoObject):
    """
    Class representation of Monzo account balance
    """
    _required_keys = ['balance', 'currency', 'spend_today']


class MonzoTransaction(MonzoObject):
    """
    Class representation of Monzo transaction
    """
    _required_keys = [
        'account_balance', 'amount', 'created', 'currency', 'description',
        'id', 'merchant', 'metadata', 'notes', 'is_load',
    ]

    def _parse_special_fields(self, data):
        """
        Helper method that parses special fields to Python objects

        :param data: response from Monzo API request
        :type data: dict
        """
        self.created = parse_date(data.pop('created'))

        if data.get('settled'):  # Not always returned
            self.settled = parse_date(data.pop('settled'))

        # Merchant field can contain either merchant ID or the whole object
        if (data.get('merchant') and
                not isinstance(data['merchant'], six.text_type)):
            self.merchant = MonzoMerchant(data=data.pop('merchant'))


class MonzoMerchant(MonzoObject):
    """
    Class representation of Monzo merchants
    """
    _required_keys = [
        'address', 'created', 'group_id', 'id',
        'logo', 'emoji', 'name', 'category',
    ]

    def _parse_special_fields(self, data):
        """
        Helper method that parses special fields to Python objects

        :param data: response from Monzo API request
        :type data: dict
        """
        self.created = parse_date(data.pop('created'))
