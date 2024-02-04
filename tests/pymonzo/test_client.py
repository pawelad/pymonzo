"""Test `pymonzo.client` module."""

import json
import types
from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from pymonzo.accounts import AccountsResource
from pymonzo.attachments import AttachmentsResource
from pymonzo.balance import BalanceResource
from pymonzo.client import MonzoAPI
from pymonzo.feed import FeedResource
from pymonzo.pots import PotsResource
from pymonzo.transactions import TransactionsResource
from pymonzo.webhooks import WebhooksResource


class TestMonzoAPI:
    """Test `MonzoAPI` class."""

    def test_init(self, tmp_path: Path, mocker: MockerFixture) -> None:
        """Client is initialized with settings loaded from disk."""
        settings_path = tmp_path / "pymonzo_test"
        MonzoAPI.settings_path = settings_path

        # Settings file doesn't exist
        with pytest.raises(ValueError, match=r"You need to run `MonzoAPI\.authorize.*"):
            MonzoAPI()

        # Settings file exists but is empty
        with open(settings_path, "w") as f:
            f.write("")

        with pytest.raises(ValueError, match=r"You need to run `MonzoAPI\.authorize.*"):
            MonzoAPI()

        # Settings file exists
        settings = {
            "client_id": "TEST_CLIENT_ID",
            "client_secret": "TEST_CLIENT_SECRET",
            "token": {
                "access_token": "TEST_ACCESS_TOKEN",
            },
        }

        with open(settings_path, "w") as f:
            json.dump(settings, f, indent=4)

        mocked_OAuth2Client = mocker.patch("pymonzo.client.OAuth2Client")  # noqa

        monzo_api = MonzoAPI()

        assert monzo_api._settings.model_dump() == settings
        assert monzo_api.session is mocked_OAuth2Client.return_value

        mocked_OAuth2Client.assert_called_once_with(
            client_id=settings["client_id"],
            client_secret=settings["client_secret"],
            token=settings["token"],
            authorization_endpoint=monzo_api.authorization_endpoint,
            token_endpoint=monzo_api.token_endpoint,
            token_endpoint_auth_method="client_secret_post",  # noqa
            update_token=monzo_api._update_token,
            base_url=monzo_api.api_url,
        )

        # This is a shortcut to the underlying method
        assert isinstance(monzo_api.whoami, types.MethodType)

        assert isinstance(monzo_api.accounts, AccountsResource)
        assert monzo_api.accounts.client is monzo_api

        assert isinstance(monzo_api.attachments, AttachmentsResource)
        assert monzo_api.attachments.client is monzo_api

        assert isinstance(monzo_api.balance, BalanceResource)
        assert monzo_api.balance.client is monzo_api

        assert isinstance(monzo_api.feed, FeedResource)
        assert monzo_api.feed.client is monzo_api

        assert isinstance(monzo_api.pots, PotsResource)
        assert monzo_api.pots.client is monzo_api

        assert isinstance(monzo_api.transactions, TransactionsResource)
        assert monzo_api.transactions.client is monzo_api

        assert isinstance(monzo_api.webhooks, WebhooksResource)
        assert monzo_api.webhooks.client is monzo_api

    def test_init_with_arguments(self, mocker: MockerFixture) -> None:
        """Client is initialized with settings from passed arguments."""
        client_id = "EXPLICIT_TEST_CLIENT_ID"
        client_secret = "EXPLICIT_TEST_CLIENT_SECRET"  # noqa
        token = {"access_token": "EXPLICIT_TEST_ACCESS_TOKEN"}

        mocked_OAuth2Client = mocker.patch("pymonzo.client.OAuth2Client")  # noqa

        monzo_api = MonzoAPI(
            client_id=client_id,
            client_secret=client_secret,
            token=token,
        )

        assert monzo_api._settings.model_dump() == {
            "client_id": client_id,
            "client_secret": client_secret,
            "token": token,
        }
        assert monzo_api.session is mocked_OAuth2Client.return_value

        mocked_OAuth2Client.assert_called_once_with(
            client_id=client_id,
            client_secret=client_secret,
            token=token,
            authorization_endpoint=monzo_api.authorization_endpoint,
            token_endpoint=monzo_api.token_endpoint,
            token_endpoint_auth_method="client_secret_post",  # noqa
            update_token=monzo_api._update_token,
            base_url=monzo_api.api_url,
        )

        # This is a shortcut to the underlying method
        assert isinstance(monzo_api.whoami, types.MethodType)

        assert isinstance(monzo_api.accounts, AccountsResource)
        assert monzo_api.accounts.client is monzo_api

        assert isinstance(monzo_api.attachments, AttachmentsResource)
        assert monzo_api.attachments.client is monzo_api

        assert isinstance(monzo_api.balance, BalanceResource)
        assert monzo_api.balance.client is monzo_api

        assert isinstance(monzo_api.feed, FeedResource)
        assert monzo_api.feed.client is monzo_api

        assert isinstance(monzo_api.pots, PotsResource)
        assert monzo_api.pots.client is monzo_api

        assert isinstance(monzo_api.transactions, TransactionsResource)
        assert monzo_api.transactions.client is monzo_api

        assert isinstance(monzo_api.webhooks, WebhooksResource)
        assert monzo_api.webhooks.client is monzo_api

    def test_authorize(self, tmp_path: Path, mocker: MockerFixture) -> None:
        """Auth flow is executed to get API access token."""
        settings_path = tmp_path / "pymonzo_test"
        MonzoAPI.settings_path = settings_path

        client_id = "TEST_CLIENT_ID"
        client_secret = "TEST_CLIENT_SECRET"  # noqa
        redirect_uri = "http://localhost:666/pymonzo"
        url = "TEST_URL"
        state = "TEST_STATE"
        test_token = {"access_token": "TEST_TOKEN"}

        mocked_OAuth2Client = mocker.patch("pymonzo.client.OAuth2Client")  # noqa
        mocked_create_authorization_url = (
            mocked_OAuth2Client.return_value.create_authorization_url
        )
        mocked_create_authorization_url.return_value = url, state
        mocked_fetch_token = mocked_OAuth2Client.return_value.fetch_token
        mocked_fetch_token.return_value = test_token

        mocked_open = mocker.patch("pymonzo.client.webbrowser.open")

        mocked_get_authorization_response_url = mocker.patch(
            "pymonzo.client.get_authorization_response_url"
        )

        token = MonzoAPI.authorize(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
        )

        mocked_OAuth2Client.assert_called_once_with(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            token_endpoint_auth_method="client_secret_post",  # noqa
        )

        mocked_create_authorization_url.assert_called_once_with(
            MonzoAPI.authorization_endpoint
        )

        mocked_open.assert_called_once_with(url)

        mocked_get_authorization_response_url.assert_called_once_with(
            host="localhost",
            port=666,
        )

        mocked_fetch_token.assert_called_once_with(
            url=MonzoAPI.token_endpoint,
            authorization_response=mocked_get_authorization_response_url.return_value,
        )

        assert token == test_token

        # Settings are saved to disk
        with open(settings_path) as f:
            loaded_settings = json.load(f)

        assert loaded_settings == {
            "client_id": client_id,
            "client_secret": client_secret,
            "token": token,
        }

    def test_update_token(self, tmp_path: Path, monzo_api: MonzoAPI) -> None:
        """Settings are updated and saved to the disk."""
        # TODO: For some reason this doesn't work:
        #   `save_to_disk_spy = mocker.spy(monzo_api._settings, "save_to_disk")`
        settings_path = tmp_path / "pymonzo_test"
        new_token = {"access_token": "NEW_TEST_TOKEN"}

        monzo_api._settings.save_to_disk(settings_path)

        monzo_api.settings_path = settings_path
        monzo_api._update_token(new_token)

        assert monzo_api._settings.token == new_token

        with open(settings_path) as f:
            loaded_settings = json.load(f)

        assert loaded_settings["token"] == new_token
