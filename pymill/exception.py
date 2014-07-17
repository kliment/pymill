import logging
logger = logging.getLogger(__name__)


def get_api_exception(json_data):
    """
    Tries to load a subclass of a APIException based on the json_data from the failed api call.

    :Parameters:
     - `json_data` - dict containing the exception

    :Returns:
        a APIException for all unclassified exceptions or a subclass of a APIException
    """
    # note: if you see a exception that is not catched here add your own subclass of APIException
    # and add a test in tests.test_exceptions

    response_exception, error = json_data.get("exception", ""), json_data.get("error", False)

    # loop over all APIException classes
    for cls in APIException.__subclasses__():
        if cls.response_exception == response_exception:
            # if the response_message equals the msg in json_data, return it
            return cls(error) if error else cls(response_exception)

    logger.debug("Unclassified exception encountered: %s [%s]" % (response_exception, error))
    # we have no special exception for this, return a plain APIException with the json data.
    return APIException(json_data)


class PymillException(Exception):
    """
    Base Exception for all interactions with pymill
    """
    pass


class OfferException(PymillException):
    """
    Raised if a new_offer call is has invalid parameters
    """
    pass


class PreauthException(PymillException):
    """
    Raised if preauthorize is called with a token _and_ a payment
    """
    pass


class APIException(PymillException):
    """
    Baseclass of all exceptions that can happen during an APICall
    """
    response_exception = None


class SubscriptionAlreadyConnected(APIException):
    """
    Raised if a client is already connected to this subscription
    """
    response_exception = "subscription_already_connected"


class TokenNotFound(APIException):
    """

    """
    response_exception = "token_not_found"


class SubscriptionNotFound(APIException):
    """
    Raised if the subscription can not be found
    """
    response_exception = "subscription_not_found"


class ClientNotFound(APIException):
    """
    Raised if the client can not be found
    """
    response_exception = "client_not_found"


class PaymentNotFound(APIException):
    """
    Raised if the payment can not be found
    """
    response_exception = "not_found_payment"


class OfferNotFound(APIException):
    """
    Raised if the offer can not be found
    """
    response_exception = "offer_not_found"


class TransactionNotFound(APIException):
    """
    Raised if the transaction can not be found
    """
    response_exception = "transaction_not_found"


class PreauthorizationNotFound(APIException):
    """
    Raised if the preauthorization can not be found
    """
    response_exception = "preauthorization_not_found"


class RefundNotFound(APIException):
    """
    Raised if the refund can not be found
    """
    response_exception = "refund_not_found"


class WebhookNotFound(APIException):
    """
    Raised if the webhook can not be found
    """
    response_exception = "webhook_not_found"