import pytest
from pymill.exception import get_api_exception, APIException, SubscriptionAlreadyConnected, TokenNotFound, \
    SubscriptionNotFound, ClientNotFound, PaymentNotFound, OfferNotFound, TransactionNotFound, \
    PreauthorizationNotFound, RefundNotFound, WebhookNotFound


def test_api_exception():

    with pytest.raises(APIException):
        raise get_api_exception({"exception": "Foo", "error": "bar"})


def test_subscription_already_connected():

    with pytest.raises(SubscriptionAlreadyConnected):
        raise get_api_exception({"exception": "subscription_already_connected", "error": "Foo"})


def test_token_not_found():

    with pytest.raises(TokenNotFound):
        raise get_api_exception({"exception": "token_not_found", "error": "Foo"})


def test_subscription_not_found():

    with pytest.raises(SubscriptionNotFound):
        raise get_api_exception({"exception": "subscription_not_found", "error": "Foo"})


def test_client_not_found():

    with pytest.raises(ClientNotFound):
        raise get_api_exception({"exception": "client_not_found", "error": "Foo"})


def test_not_found_payment():

    with pytest.raises(PaymentNotFound):
        raise get_api_exception({"exception": "not_found_payment", "error": "Foo"})


def test_offer_not_found():

    with pytest.raises(OfferNotFound):
        raise get_api_exception({"exception": "offer_not_found", "error": "Foo"})


def test_transaction_not_found():

    with pytest.raises(TransactionNotFound):
        raise get_api_exception({"exception": "transaction_not_found", "error": "Foo"})


def test_preauthorization_not_found():

    with pytest.raises(PreauthorizationNotFound):
        raise get_api_exception({"exception": "preauthorization_not_found", "error": "Foo"})


def test_refund_not_found():

    with pytest.raises(RefundNotFound):
        raise get_api_exception({"exception": "refund_not_found", "error": "Foo"})


def test_webhook_not_found():

    with pytest.raises(WebhookNotFound):
        raise get_api_exception({"exception": "webhook_not_found", "error": "Foo"})