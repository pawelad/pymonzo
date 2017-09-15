# -*- coding: utf-8 -*-
"""
pymonzo utils
"""
from __future__ import unicode_literals

from six import iteritems


class CommonMixin(object):
    """
    Common class mixin that implements sensible defaults
    """
    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.__dict__ == other.__dict__
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        data = ', '.join([
            '{}={}'.format(k, v) for k, v in iteritems(self.__dict__)
            if not k.startswith('_')
        ])
        return '{}({})'.format(self.__class__.__name__, data)

    def __repr__(self):
        return '{}({})'.format(self.__class__, self.__dict__)
