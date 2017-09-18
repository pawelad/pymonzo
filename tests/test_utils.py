# -*- coding: utf-8 -*-
"""
Test 'pymonzo.utils' file
"""
from __future__ import unicode_literals

import pytest
import six

from pymonzo.utils import CommonMixin


class ExampleClass(CommonMixin):
    """Just a dummy test class"""
    pass


class TestCommonMixin:
    """
    Test `utils.CommonMixin` class
    """
    klass = CommonMixin
    data = {
        '_hidden': 1,
        'foo': 'foo',
        'bar': True,
    }

    @pytest.fixture
    def test_instances(self):
        """Helper fixture for initialing test class instances"""
        a = CommonMixin()
        a.__dict__.update(**self.data)

        b = CommonMixin()
        b.__dict__.update(**self.data)

        c = ExampleClass()
        c.__dict__.update(**self.data)

        return a, b, c

    def test_class_eq_method(self, test_instances):
        """Test class `__eq__` method"""
        a, b, _ = test_instances

        assert a == b

    def test_class_ne_method(self, test_instances):
        """Test class `__ne__` method"""
        a, b, c = test_instances

        assert a != c
        assert b != c

        a.__dict__.update(baz=True)

        assert a != b

    def test_class_str_method(self, test_instances):
        """Test class `__str__` method"""
        a, b, c = test_instances
        str_a = str(a)
        str_b = str(b)
        str_c = str(c)

        assert 'CommonMixin' in str_a
        assert 'CommonMixin' in str_b
        assert 'ExampleClass' in str_c

        # We don't know the `__dict__` order so let's do it in parts
        parts = ['foo=foo', 'bar=True']

        for part in parts:
            assert part in str_a
            assert part in str_b
            assert part in str_c

    def test_class_repr_method(self, test_instances):
        """Test class `__repr__` method"""
        a, b, c = test_instances
        repr_a = repr(a)
        repr_b = repr(b)
        repr_c = repr(c)

        assert "<class 'pymonzo.utils.CommonMixin'>" in repr_a
        assert "<class 'pymonzo.utils.CommonMixin'>" in repr_b
        assert "<class 'tests.test_utils.ExampleClass'>" in repr_c

        if six.PY2:
            # We don't know the `__dict__` order so let's do it in parts
            parts = ["u'_hidden': 1", "u'foo': u'foo'", "u'bar': True"]

            for part in parts:
                assert part in repr_a
                assert part in repr_b
                assert part in repr_c
        else:
            # We don't know the `__dict__` order so let's do it in parts
            parts = [
                "'_hidden': 1", "'foo': 'foo'", "'bar': True",
            ]

            for part in parts:
                assert part in repr_a
                assert part in repr_b
                assert part in repr_c
