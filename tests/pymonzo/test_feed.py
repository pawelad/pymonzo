"""Test `pymonzo.feed` module."""

import httpx
import pytest
import respx
from polyfactory.factories.pydantic_factory import ModelFactory
from pytest_mock import MockerFixture

from pymonzo import MonzoAPI
from pymonzo.feed import FeedResource, MonzoBasicFeedItem

from .test_accounts import MonzoAccountFactory


class MonzoBasicFeedItemFactory(ModelFactory[MonzoBasicFeedItem]):
    """Factory for `MonzoBasicFeedItem` schema."""


@pytest.fixture(scope="module")
def feed_resource(monzo_api: MonzoAPI) -> FeedResource:
    """Initialize `FeedResource` resource with `monzo_api` fixture."""
    return FeedResource(client=monzo_api)


class TestFeedResource:
    """Test `FeedResource` class."""

    @pytest.mark.respx(base_url=MonzoAPI.api_url)
    def test_create_respx(
        self,
        mocker: MockerFixture,
        respx_mock: respx.MockRouter,
        feed_resource: FeedResource,
    ) -> None:
        """Correct API response is sent, API response is parsed into expected schema."""
        feed_item = MonzoBasicFeedItemFactory.build()

        account = MonzoAccountFactory.build()
        mocked_get_default_account = mocker.patch.object(
            feed_resource.client.accounts,
            "get_default_account",
        )
        mocked_get_default_account.return_value = account

        params = {
            "account_id": account.id,
            "type": "basic",
            "params[title]": feed_item.title,
            "params[image_url]": feed_item.image_url,
            "params[body]": feed_item.body,
        }
        optional_params = {
            "params[background_color]": feed_item.background_color,
            "params[title_color]": feed_item.title_color,
            "params[body_color]": feed_item.body_color,
        }
        for key, value in optional_params.items():
            if value is not None:
                params[key] = str(value)

        mocked_route = respx_mock.post("/feed", params=params).mock(
            return_value=httpx.Response(200, json={})
        )

        feed_create_response = feed_resource.create(feed_item=feed_item)

        mocked_get_default_account.assert_called_once_with()
        mocked_get_default_account.reset_mock()

        assert feed_create_response == {}
        assert mocked_route.called

        # Explicitly passed account ID and URL
        account_id = "TEST_ACCOUNT_ID"
        url = "TEST_URL"

        params = {
            "account_id": account_id,
            "type": "basic",
            "url": url,
            "params[title]": feed_item.title,
            "params[image_url]": feed_item.image_url,
            "params[body]": feed_item.body,
        }
        optional_params = {
            "params[background_color]": feed_item.background_color,
            "params[title_color]": feed_item.title_color,
            "params[body_color]": feed_item.body_color,
        }
        for key, value in optional_params.items():
            if value is not None:
                params[key] = str(value)

        mocked_route = respx_mock.post("/feed", params=params).mock(
            return_value=httpx.Response(200, json={})
        )

        feed_create_response = feed_resource.create(
            feed_item=feed_item,
            account_id=account_id,
            url=url,
        )

        mocked_get_default_account.assert_not_called()
        mocked_get_default_account.reset_mock()

        assert feed_create_response == {}
        assert mocked_route.called
