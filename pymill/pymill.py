# -*- coding: utf-8 -*-


from datetime import datetime, timedelta
import logging
import time
import re

import requests


logger = logging.getLogger(__name__)


class PaymillObject(object):
    """ABC for all Paymill data objects"""

    @classmethod
    def _check_field(cls, field_name):
        if not field_name in dir(cls):
            logger.debug("New/undocumented field '%s'", field_name)

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.iteritems():
            self._check_field(key)
            setattr(self, key, value)

    def __str__(self):
        if hasattr(self, 'id'):
            return self.id
        return super(PaymillObject, self).__str__()

    def __repr__(self):
        result = str(type(self)) + "\n"
        for key in dir(self):
            if callable(getattr(self, key)):
                continue
            if key.startswith("__"):
                continue
            result = result + "\t%s: %s\n" %(str(key), str(getattr(self, key)))
        return result
    

class Payment(PaymillObject):
    id = None
    """unique payment method ID"""

    type = None
    """creditcard or debit"""

    client = None
    """id of associatied client (optional)"""

    card_type = None
    """visa or mastercard (for credit cards only)"""

    country = None
    """country the card was issued in (For credit cards only)"""

    expire_month = None
    """2 digits (For credit cards only)"""

    expire_year = None
    """4 digitis (For credit cards only)"""

    card_holder = None
    """name of cardholder (For credit cards only)"""

    last4 = None
    """last 4 digits of card (For credit cards only)"""

    code = None
    """the sorting code of the bank (For debit accounts only)"""

    account = None
    """a partially masked account number (For debit accounts only)"""

    holder = None
    """name of the account holder (For debit accounts only)"""

    created_at = None
    """unix timestamp identifying time of creation"""

    updated_at = None
    """unix timestamp identifying time of last change"""


class Preauthorization(PaymillObject):
    id = None
    """unique preauthorization ID"""

    amount = None
    """amount preauthorized in CENTS"""

    status = None
    """open, pending, closed, failed, deleted, or preauth"""

    livemode = None
    """true or false depending on whether the transaction is real or in test mode"""

    payment = None
    """a credit card payment method object (see above)"""

    client = None
    """if a preset client (see below) was used to make the transaction. Otherwise null"""

    created_at = None
    """unix timestamp identifying time of creation"""

    updated_at = None
    """unix timestamp identifying time of last change"""


class Transaction(PaymillObject):
    id = None
    """unique transaction ID"""

    amount = None
    """amount charged in CENTS"""

    status = None
    """open, pending, closed, failed, partial_refunded, refunded, or preauthorize (closed means success)"""

    description = None
    """user-selected description of the transaction"""

    livemode = None
    """true or false depending on whether the transaction is real or in test mode"""

    payment = None
    """a payment method object (see above)"""

    preauthorization = None
    """the preauthorization associated with this transaction (optional)"""

    created_at = None
    """unix timestamp identifying time of creation"""

    updated_at = None
    """unix timestamp identifying time of last change"""


class Refund(PaymillObject):
    id = None
    """unique refund ID"""

    transaction = None
    """The unique transaction ID of the transaction being refunded"""

    amount = None
    """amount refunded in CENTS"""

    status = None
    """open, pending or refunded"""

    description = None
    """user-selected description of the refund"""

    livemode = None
    """true or false depending on whether the transaction is real or in test mode"""

    created_at = None
    """unix timestamp identifying time of creation"""

    updated_at = None
    """unix timestamp identifying time of last change"""


class Client(PaymillObject):
    id = None
    """unique id for this client"""

    email = None
    """client's email address (optional)"""

    description = None
    """description of this client (optional)"""

    payment = None
    """list of cc or debit objects"""

    subscription = None
    """subscription object (optional)"""

    created_at = None
    """unix timestamp identifying time of creation"""

    updated_at = None
    """unix timestamp identifying time of last change"""


class Offer(PaymillObject):
    id = None
    """unique offer identifier"""

    name = None
    """freely controllable offer name"""

    amount = None
    """The amount, in CENTS, to be charged every time the offer period passes. Note that ODD values will NOT work in test mode."""

    interval = None
    """Format: number DAY|WEEK|MONTH|YEAR Example: 2 DAY. The client will be charged every time the interval passes"""

    trial_period_days = None
    """Number of days before the first charge. (optional)"""


class Subscription(PaymillObject):
    id = None
    """unique subscription identifier"""

    offer = None
    """unique offer identifier"""

    livemode = None
    """true or false depending on whether the transaction is real or in test mode"""

    cancel_at_period_end = None
    """true if subscription is to be cancelled at the end of current period, false if to be cancelled immediately"""

    canceled_at = None
    """unix timestamp identifying time of cancellation(optional)"""

    interval = None
    """ "week", "month", or "year". The client will be charged every time the interval passes"""

    payment = None
    """Payment which is used to pay for the subscription"""

    client = None
    """Client who owns this subscription"""

    next_capture_at = None
    """Unix timestamp of next charge"""

    trial_start = None
    """Unix timestamp when the trial period starts"""

    trial_end = None
    """Unix timestamp when the trial period ends"""

    created_at = None
    """unix timestamp identifying time of creation"""
    
    updated_at = None
    """unix timestamp identifying time of last change"""


class Webhook(PaymillObject):
    id = None
    """unique identifier of this webhook"""

    url = None
    """the url of the webhook"""

    livemode = None
    """boolean. you can create webhook for live or test mode"""

    event_types = None
    """array of event_types"""


def dict_without_none(**kwargs):
    """Creates a dictionary without the keys associated with None"""
    
    result = {}
    for key, value in kwargs.iteritems():
        if value in (None, str(None), ''):
            continue
        result[key] = value
    return result


class Pymill(object):
    """Central entrance point to the Paymill API"""

    def __init__(self, privatekey):
        """Initialize a new paymill interface connection. Requires a private key."""
        self.session = requests.Session()
        self.session.auth = (privatekey, "")
        self.session.verify = False

    def _api_call(self, url, params={}, method="GET", headers=None, parse_json=True, return_type=None):
        """Call an API method.

        :Parameters:
         - `url` - The URL of the entity to post to.
         - `params` - a dictionary of parameters
         - `method` - The request type to be made. If parameters are passed, this will be ignored and treated as POST
         - `headers` - HTTP headers to be added to the request

        :Returns:
            a dictionary object populated with the json returned.
        """
        request = {'GET': self.session.get, 'DELETE': self.session.delete, 'PUT': self.session.put, 'POST': self.session.post}[method]
        if len(params) > 0 and not method in ('DELETE', 'PUT'):
            request = self.session.post
        response = request(url, params=params, headers=headers)

        if parse_json:
            if return_type is None:
                return response.json()
            else:
                json_data = response.json()
                if 'data' in json_data:
                    if isinstance(json_data['data'], dict):
                        return return_type(**json_data['data'])
                    else:
                        return [return_type(**x) for x in json_data['data']]
                else:
                    raise Exception(json_data)
        else:
            return response.text

    def new_debit_card(self, code, account, holder, client=None):
        """Create a debit card from account data.

        :Parameters:
         - `code` - A bank sorting code
         - `account` - The account number
         - `holder` - The name of the account holder
         - `client` - A client id number (optional)

        :Returns:
            a dict with a member "data" containing a dict representing a debit card
        """
        return self._api_call("https://api.paymill.com/v2/payments/", dict_without_none(code=str(code), account=str(account), holder=str(holder), type='debit', client=str(client)), return_type=Payment)

    def new_card(self, token, client=None):
        """Create a card from a given token.

        :Parameters:
         - `token` - string Unique credit card token
         - `client` - A client id number (optional)

        :Returns:
            a dict with a member "data" containing a dict representing a card
        """
        return self._api_call("https://api.paymill.com/v2/payments", dict_without_none(token=str(token), client=str(client)), return_type=Payment)

    def get_card(self, card_id):
        """Get the details of a card from its ID.

        :Parameters:
         - `card_id` - ID for the card

        :Returns:
            a dict with a member "data" containing a dict representing a card
        """
        return self._api_call("https://api.paymill.com/v2/payments/" + str(card_id), return_type=Payment)

    def get_cards(self):
        """List all stored cards.

        :Returns:
            a dict with a member "data" which is an array of dicts, each representing a card
        """
        return self._api_call("https://api.paymill.com/v2/payments/", return_type=Payment)

    def delete_card(self, card_id):
        """Delete a stored card
        
        :Parameters:
         - `card_id` - ID for the card to be deleted
        """
        self._api_call("https://api.paymill.com/v2/payments/" + str(card_id), method="DELETE")

    def transact(self, amount=0, currency="eur", description=None, token=None, client=None, payment=None, preauth=None, code=None, account=None, holder=None):
        """Create a transaction (charge a card or account). You must provide an amount, and exactly one funding source.
        
        The amount is in cents, and the funding source can be a payment method id, a token, a preauthorization or a direct debit account.

        :Parameters:
         - `amount` - The amount (in CENTS) to be charged. For example, 240 will charge 2 euros and 40 cents, NOT 240 euros.
         - `currency` - ISO4217 currency code (optional)
         - `description` - A short description of the transaction (optional)
         - `token` - A token generated by the paymill bridge js library
         - `client` - A client id number (optional)
         - `payment` - A payment method id number (credit card id or debit account id)
         - `preauth` - A preauthorization id number
         - `code` - If paying by debit, the bank sorting code
         - `account` - If paying by debit, the account number
         - `holder` - If paying by debit, the name of the account holder

        :Returns:
            None if one of the required parameters is missing. A dict with a member "data" containing a transaction dict otherwise.
        """
        if amount == 0:
            return None

        parameters = dict_without_none(amount=str(amount), currency=str(currency), client=str(client), description=str(description))

        # figure out mode of payment

        if payment is None and (code is not None and
                                account is not None and
                                holder is not None):
            parameters['payment'] = str(self.new_debit_card(code, account, holder, client))
        elif payment is not None:
            parameters['payment'] = str(payment)
        elif token is not None:
            parameters['token'] = str(token)
        elif preauth is not None:
            parameters["preauthorization"] = str(preauth)
        else:
            return None

        return self._api_call("https://api.paymill.com/v2/transactions/", parameters, return_type=Transaction)

    def get_transaction(self, transaction_id):
        """Get details on a transaction.

        :Parameters:
         - `transaction_id` - ID for the transaction

        :Returns:
            a dict representing a transaction
        """
        return self._api_call("https://api.paymill.com/v2/transactions/" + str(transaction_id), return_type=Transaction)

    def get_transactions(self):
        """List all transactions.

        :Returns:
            a dict with a member "data" which is an array of dicts, each representing a transaction
        """
        return self._api_call("https://api.paymill.com/v2/transactions/", return_type=Transaction)

    def refund(self, transaction_id, amount, description=None):
        """Refunds an already performed transaction.

        :Parameters:
         - `transaction_id` - string Unique transaction id
         - `amount` - The amount in cents that are to be refunded
         - `description` - A description of the refund (optional)

        :Returns:
            a dict with a member "data" which is a dict representing a refund, or None if the amount is 0
        """
        if amount == 0:
            return None

        return self._api_call("https://api.paymill.com/v2/refunds/" + str(transaction_id), dict_without_none(amount=str(amount), description=str(description)), return_type=Refund)

    def get_refund(self, refund_id):
        """Get the details of a refund from its ID.
        
        :Parameters:
         - `refund_id` - ID for the refund

        :Returns:
            a dict with a member "data" which is a dict representing a refund
        """
        return self._api_call("https://api.paymill.com/v2/refunds/" + str(refund_id), return_type=Refund)

    def get_refunds(self):
        """List all stored refunds.

        :Returns:
            a dict with a member "data" which is an array of dicts, each representing a refund
        """
        return self._api_call("https://api.paymill.com/v2/refunds/", return_type=Refund)

    def preauthorize(self, amount=0, currency="eur", description=None, token=None, client=None, payment=None):
        """Preauthorize a transaction (reserve value a card). You must provide an amount, and exactly one funding source.
        
        The amount is in cents, and the funding source can be a token or a payment id.
        
        :Parameters:
         - `amount` - The amount (in CENTS) to be charged. For example, 240 will charge 2 euros and 40 cents, NOT 240 euros.
         - `currency` - ISO4217 (optional)
         - `token` - A token generated by the paymill bridge js library
         - `payment` - A payment method id number. Must represent a credit card, not a debit payment.

        :Returns:
            None if one of the required parameters is missing. A dict with a member "data" containing a preauthorization dict otherwise.
        """
        if amount == 0:
            return None
        if payment is None and token is None:
            raise Exception("Please only provide token _or_ payment")
        if (not payment is None) and (not token is None):
            return None

        return self._api_call("https://api.paymill.com/v2/preauthorizations/", dict_without_none(amount=str(amount), currency=str(currency), payment=str(payment), token=str(token)), return_type=Preauthorization)

    def get_preauthorization(self, preauthorization_id):
        """Get details on a preauthorization.

        :Parameters:
         - `preauthorization_id` - ID of the preauthorization

        :Returns:
            a dict representing a preauthorization
        """
        return self._api_call("https://api.paymill.com/v2/preauthorizations/" + str(preauthorization_id), return_type=Preauthorization)

    def get_preauthorizations(self):
        """List all preauthorizations.

        :Returns:
            a dict with a member "data" which is an array of dicts, each representing a preauthorization
        """
        return self._api_call("https://api.paymill.com/v2/preauthorizations/", return_type=Preauthorization)

    def new_client(self, email=None, description=None):
        """Creates a new client.

        :Parameters:
         - `email` - client's email address
         - `description` - description of this client (optional)

        :Returns:
            a dict with a member "data" which is a dict representing a client.
        """
        parameters = dict_without_none(description=unicode(description), email=str(email))
        if len(parameters) == 0:
            return None
        return self._api_call("https://api.paymill.com/v2/clients", parameters, return_type=Client)

    def get_client(self, client_id):
        """Get the details of a client from its ID.
        
        :Parameters:
         - `client_id` - ID of the client

        :Returns:
            a dict with a member "data" which is a dict representing a client
        """
        return self._api_call("https://api.paymill.com/v2/clients/" + str(client_id), return_type=Client)

    def update_client(self, client_id, email, description=None):
        """Updates the details of a client.

        :Parameters:
         - `client_id` - ID of the client
         - `email` - The email of the client
         - `description` - A description of the client (optional)

        :Returns:
            a dict with a member "data" which is a dict representing a client
        """
        parameters = dict_without_none(description=unicode(description), email=str(email))
        if len(parameters) == 0:
            return None
        return self._api_call("https://api.paymill.com/v2/clients/" + str(client_id), parameters, method="PUT", return_type=Client)

    def delete_client(self, client_id):
        """Delete a stored client
        
        :Parameters:
         - `client_id` - ID of the client to be deleted
        """
        return self._api_call("https://api.paymill.com/v2/clients/" + str(client_id), method="DELETE", return_type=Client)

    def get_clients(self):
        """List all stored clients.

        :Returns:
            a dict with a member "data" which is an array of dicts, each representing a client
        """
        return self._api_call("https://api.paymill.com/v2/clients/", return_type=Client)

    def export_clients(self):
        """Export all stored clients in CSV form

        :Returns:
            the contents of the CSV file
        """
        return self._api_call("https://api.paymill.com/v2/clients/", headers={"Accept": "text/csv"}, parse_json=False)

    def new_offer(self, amount, interval="month", currency="eur", name=None):
        """Creates a new offer

        :Parameters:
         - `amount` - The amount in cents that are to be charged every interval
         - `interval` - Format: number DAY|WEEK|MONTH|YEAR Example: 2 DAY
         - `currency` - Must be an ISO_4217 formatted currency, "EUR" by default
         - `name` - A name for this offer

        :Returns:
            a dict with a member "data" which is a dict representing an offer, or None if the amount is 0 or the interval or currency is invalid
        """
        if amount == 0:
            return None
        if not str(amount).isdigit():
            raise ValueError, "amount is not a number"
        if '.' in str(amount):
            raise ValueError, "amount is not an integer"

        interval_re = re.compile(r'^[0-9]*\ ?(DAY|WEEK|MONTH|YEAR)$', flags=re.I)
        if not re.findall(interval_re, interval):
            raise ValueError, "Format: number DAY|WEEK|MONTH|YEAR Example: 2 DAY"

        return self._api_call("https://api.paymill.com/v2/offers", dict_without_none(amount=str(amount), currency=str(currency), interval=str(interval), name=str(name)), return_type=Offer)

    def get_offer(self, offer_id):
        """Get the details of an offer from its ID.

        :Parameters:
         - `offer_id` - ID ofr the offer

        :Returns:
            a dict with a member "data" which is a dict representing an offer
        """
        return self._api_call("https://api.paymill.com/v2/offers/" + str(offer_id), return_type=Offer)

    def update_offer(self, offer_id, name):
        """Updates the details of an offer. Only the name may be changed

        :Parameters:
         - `offer_id` - string Unique offer id
         - `name` - The new name of the offer

        :Returns:
            a dict with a member "data" which is a dict representing an offer
        """
        return self._api_call("https://api.paymill.com/v2/offers/" + str(offer_id), {'name': str(name)}, return_type=Offer)

    def delete_offer(self, offer_id):
        """Delete a stored offer. May only be done if no subscriptions to this offer are active.
        
        :Parameters:
         - `offer_id` - ID of the offer to be deleted
        """
        self._api_call("https://api.paymill.com/v2/offers/" + str(offer_id), method="DELETE")

    def get_offers(self):
        """List all stored offers.

        :Returns:
            a dict with a member "data" which is an array of dicts, each representing an offer
        """
        return self._api_call("https://api.paymill.com/v2/offers/", return_type=Offer)

    def new_subscription(self, client, offer, payment, start_at=None):
        """Subscribes a client to an offer
        
        :Parameters:
         - `client` - The id of the client
         - `offer` - The id of the offer
         - `payment` - The id of the payment instrument used for this offer

        :Returns:
            a dict with a member "data" which is a dict representing a subscription
        """
        # convert start_at to unixtime
        real_start_at = start_at
        if isinstance(real_start_at, datetime):
            real_start_at = time.mktime(real_start_at.timetuple())
        
        return self._api_call("https://api.paymill.com/v2/subscriptions", dict_without_none(offer=str(offer), client=str(client), payment=str(payment), start_at=real_start_at), return_type=Subscription)

    def get_subscription(self, subscription_id):
        """Get the details of a subscription from its id.
        
        :Parameters:
         - `subscription_id` - ID of the subscription

        :Returns:
            a dict with a member "data" which is a dict representing a subscription
        """
        return self._api_call("https://api.paymill.com/v2/subscriptions/" + str(subscription_id), return_type=Subscription)

    def update_subscription(self, subscription_id, offer):
        """Change the offer that a subscription is attached to
        
        :Parameters:
         - `subscription_id` - ID of the subscription
         - `offer` - ID of the new offer

        :Returns:
            a dict with a member "data" which represents the subscription
        """
        return self._api_call("https://api.paymill.de/v2/subscriptions/" + str(subscription_id), {'offer': str(offer)}, method="PUT", return_type=Subscription)

    def cancel_subscription_after_interval(self, subscription_id, cancel=True):
        """Cancels a subscription after its interval ends
        
        :Parameters:
         - `subscription_id` - ID of the subscription
         - `cancel` - If True, the subscription will be cancelled at the end of its interval. Set to False to undo.

        :Returns:
            a dict with a member "data" which is a dict representing a subscription
        """
        return self._api_call("https://api.paymill.com/v2/subscriptions/" + str(subscription_id), {'cancel_at_period_end': "true" if cancel else "false"}, method="PUT", return_type=Subscription)

    def cancel_subscription_now(self, subscription_id):
        """Cancel a subscription immediately. Pending transactions will still be charged.
        
        :Parameters:
         - `subscription_id` - ID of the subscription
        """
        return self._api_call("https://api.paymill.com/v2/subscriptions/" + str(subscription_id), method="DELETE", return_type=Subscription)

    def get_subscriptions(self):
        """List all stored subscriptions.

        :Returns:
            a dict with a member "data" which is an array of dicts, each representing a subscription
        """
        return self._api_call("https://api.paymill.com/v2/subscriptions/", return_type=Subscription)

    def new_webhook(self, url, event_types):
        """Create a webhook to react to an event

        :Parameters:
         - `url` - the url for paymill server to Call
         - `event_type` - an array of event types to react to. exemple : ['subscription.deleted','subscription.failed']

        :Returns:
            a dict containing the webhook description
        """
        return self._api_call("https://api.paymill.com/v2/webhooks", {'url': str(url), 'event_types': event_types}, return_type=Webhook)

    def delete_webhook(self, webhook_id):
        """Delete a webhook.

        :Parameters:
         - `webhook_id` - the ID of the webhook to be deleted
        """
        self._api_call("https://api.paymill.com/v2/webhooks/" + str(webhook_id), method="DELETE")

    def get_webhook(self, webhook_id):
        """Get the details of a webhook.
        
        :Parameters:
         - `webhook_id` - the ID of the webhook to be retrieved
        
        :Returns:
            a Webhook instance
        """
        return self._api_call("https://api.paymill.com/v2/webhooks/" + str(webhook_id), return_type=Webhook)

    def get_webhooks(self):
        """List all webhooks.

        :Returns:
            a dict
        """
        return self._api_call("https://api.paymill.com/v2/webhooks/", return_type=Webhook)
        
    def response_code2text(self, response_code):
        """Utility function to convert from response codes in some object to human readable text
        
        :Parameters:
         - `response_code` - response code from data object
        
        :Returns:
            Human readable representation of the issue encountered
        """
        texts = {
                10001:    'General undefined response.',
                10002:    'Still waiting on something.',

                20000:    'General success response.',
                
                40000:    'General problem with data.',
                40100:    'Problem with creditcard data.',
                40101:    'Problem with cvv.',
                40102:    'Card expired or not yet valid.',
                40103:    'Limit exceeded.',
                40104:    'Card invalid.',
                40105:    'expiry date not valid',
                40200:    'Problem with bank account data.',
                40300:    'Problem with 3d secure data.',
                40301:    'currency / amount mismatch',
                40400:    'Problem with input data.',
                40401:    'Amount too low or zero.',
                40402:    'Usage field too long.',
                40403:    'Currency not allowed.',
                
                50000:    'General problem with backend.',
                50001:    'country blacklisted.',
                50100:    'Technical error with credit card.',
                50101:    'Error limit exceeded.',
                50102:    'Card declined by authorization system.',
                50103:    'Manipulation or stolen card.',
                50104:    'Card restricted.',
                50105:    'Invalid card configuration data.',
                50200:    'Technical error with bank account.',
                50201:    'Card blacklisted.',
                50300:    'Technical error with 3D secure.',
                50400:    'Decline because of risk issues.',      
        }
        
        try:
            return texts[response_code]
        except:
            return response_code


if __name__ == "__main__":
    p = Pymill("(your paymill private key)")
    
    # list stored cards
    #for card in p.get_cards():
    #    print repr(card)
    
    # list stored clients
    #for client in p.get_clients():
    #    print repr(client)

    # charge debit card
    #transaction1 = p.transact(amount=300, code="86055500", account="1234512345", holder="Max Mustermann", description="debittest")
    #print repr(transaction1)
    
    # charge credit card
    #transaction2 = p.transact(amount=300, payment=p.get_cards()[0], description="pymilltest")
    #print repr(transaction2)

    # subscribe client to offer
    #client1 = p.new_client("max@figo.me")
    #card1 = p.new_debit_card(code="86055500", account="1234512345", holder="Max Mustermann", client=client1)
    #offer1 = p.get_offers()[0]
    #subscription = p.new_subscription(client1, offer1, card1)
    #print repr(subscription)
    
    # subscribe client to offer, but start later to charge him
    client1 = p.get_client("(some client id)")
    card1 = Payment(**client1.payment[0])
    offer1 = p.get_offers()[0]
    subscription = p.new_subscription(client1, offer1, card1, start_at=(datetime.utcnow() + timedelta(days=15)))
    print repr(subscription)
