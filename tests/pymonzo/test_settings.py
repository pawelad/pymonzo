"""
Test 'pymonzo.settings' module.
"""
import codecs
import json
import os
import tempfile

import pytest


@pytest.mark.skip
class TestPyMonzoSettings:
    """
    Test 'settings.PyMonzoSettings' class.
    """

    def test_load_from_disk(self) -> None:
        pass

    def test_save_to_disk(self) -> None:
        pass

    def test_class_save_token_on_disk_method(self, monzo) -> None:
        """Test class `_save_token_on_disk` method"""
        path = os.path.join(
            tempfile.gettempdir(),
            "pymonzo_test",
        )

        monzo._token = {
            "foo": "UNICODE",
            "bar": 1,
            "baz": False,
        }

        expected_token = monzo._token.copy()
        expected_token.update(client_secret=monzo._client_secret)

        monzo._save_token_on_disk()

        with codecs.open(path, "r", "utf-8") as f:
            assert json.load(f) == expected_token
