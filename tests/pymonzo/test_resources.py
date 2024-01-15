"""Test `pymonzo.resources` module."""
import httpx
import pytest
import respx

from pymonzo import MonzoAPI
from pymonzo.exceptions import MonzoAccessDenied, MonzoAPIError
from pymonzo.resources import BaseResource


@pytest.fixture(scope="module")
def base_resource(monzo_api: MonzoAPI) -> BaseResource:
    """Initialize `BaseResource` resource with `monzo_api` fixture."""
    return BaseResource(client=monzo_api)


class TestBaseResource:
    """Test `BaseResource` class."""

    def test__get_response(
        self, respx_mock: respx.MockRouter, base_resource: BaseResource
    ) -> None:
        """Correct request is sent, response errors are raised."""
        params = {
            "foo": "TEST_FOO",
            "bar": "TEST_BAR",
            "n": "42",
        }
        data = {"response": "TEST_RESPONSE"}

        mocked_route = respx_mock.post("/foo/bar", params=params).mock(
            return_value=httpx.Response(200, json=data)
        )

        response = base_resource._get_response(
            method="post",
            endpoint="/foo/bar",
            params=params,
        )

        assert response.json() == data
        assert mocked_route.called

        # HTTP 403
        mocked_route = respx_mock.get("/http403").mock(return_value=httpx.Response(403))

        with pytest.raises(
            MonzoAccessDenied,
            match=r"Monzo API access denied \(HTTP 403 Forbidden\). .*",
        ):
            base_resource._get_response(method="get", endpoint="/http403")

        assert mocked_route.called

        # HTTP 404 with JSON response
        mocked_route = respx_mock.get("/http404").mock(
            return_value=httpx.Response(
                404,
                json={"code": "404", "message": "Error message"},
            )
        )

        with pytest.raises(MonzoAPIError, match=r"Error message \(404\)"):
            base_resource._get_response(method="get", endpoint="/http404")

        assert mocked_route.called

        # HTTP 500
        mocked_route = respx_mock.get("/http500").mock(return_value=httpx.Response(500))

        with pytest.raises(MonzoAPIError, match=r"Something went wrong: .*"):
            base_resource._get_response(method="get", endpoint="/http500")

        assert mocked_route.called
