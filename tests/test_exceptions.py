import pytest
from pymill.exception import get_api_exception, APIException, SubscriptionAlreadyConnected, TokenNotFound


def test_api_exception():

    with pytest.raises(APIException):
        raise get_api_exception({"exception": "Foo", "error": "bar"})


def test_subscription_already_connected():

    with pytest.raises(SubscriptionAlreadyConnected):
        raise get_api_exception({"exception": "subscription_already_connected", "error": "Foo"})


def test_token_not_found():

    with pytest.raises(TokenNotFound):
        raise get_api_exception({"exception": "token_not_found", "error": "Foo"})