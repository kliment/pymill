#! /usr/bin/env python
# -*- coding: utf-8 -*-
#pymill.py

import pycurl2 as pycurl
import cStringIO
import json


class Pymill():
    """
    These are the parameters each object type contains

    Card:
    id: unique card ID
    card_type: visa, mastercard, (maybe one day american express)
    country: country the card was issued in
    expire_month: (2ch)
    expire_year: (4ch)
    card_holder: name of cardholder
    last4: last 4 digits of card
    created_at: unixtime
    updated_at: unixtime

    Transaction:
    id: unique transaction ID
    amount: amount charged in EuroCENTS
    status: open, pending, closed or refunded
    description: user-selected description of the transaction
    livemode: true or false depending on whether the transaction is real or in test mode
    creditcard: a card object (see above)
    clients: if a preset client (see below) was used to make the transaction. Otherwise null
    created_at: unixtime
    updated_at: unixtime

    Refund:
    id: unique refund ID
    transaction: The unique transaction ID of the transaction being refunded
    amount: amount refunded in EuroCENTS
    status: open, pending or refunded
    description: user-selected description of the refund
    livemode: true or false depending on whether the transaction is real or in test mode
    created_at: unixtime
    updated_at: unixtime

    Client:
    id: unique id for this client
    email: client's email address (optional)
    description: description of this client (optional)
    created_at: unix timestamp identifying time of creation
    updated_at: unix timestamp identifying time of last change
    creditcard: cc object (optional)
    subscription: subscription object (optional)

    Offer:
    id: unique offer identifier
    name: freely controllable offer name
    amount: The amount, in EuroCENTS, to be charged every time the offer period passes. Note that ODD values will NOT work in test mode.
    interval: "week", "month", or "year". The client will be charged every time the interval passes
    trial_period_days: Number of days before the first charge. (optional)
    """

    def __init__(self, privatekey):
        """
        Initialize a new paymill interface connection. Requires a private key.
        """
        self.c = pycurl.Curl()
        self.c.setopt(pycurl.NOSIGNAL, 1)
        self.c.setopt(pycurl.CONNECTTIMEOUT, 30)
        self.c.setopt(pycurl.USERPWD, '%s:' % (privatekey,))
        self.bridge = "https://api.paymill.de/v2/"

    def _post(self, url, params=(), cr='GET'):
        """
        Posts a request with parameters to a given url
        url: The URL of the entity to post to.
        params: a tuple of (name, value) tuples of parameters

        Returns None
        """
        self.c.setopt(self.c.URL, url)
        if params is not ():
            p = str("&".join([i[0] + "=" + i[1] for i in params]))
            print p
            if cr == 'GET':
                self.c.setopt(pycurl.CUSTOMREQUEST, "POST")
            else:
                self.c.setopt(pycurl.CUSTOMREQUEST, cr)
            self.c.setopt(self.c.POSTFIELDS, p)
        else:
            self.c.setopt(pycurl.CUSTOMREQUEST, cr)
        self.c.perform()

    def _apicall(self, url, params=(), cr="GET", ch=None):
        """
        Call an API endpoint.
        url: The URL of the entity to post to.
        params: a tuple of (name, value) tuples of parameters
        cr: The request type to be made. If parameters are passed, this will be ignored and treated as POST

        Returns a dictionary object populated with the json returned.
        """
        if ch is not None:
            self.c.setopt(pycurl.HTTPHEADER, ch)
        buf = cStringIO.StringIO()
        self.c.setopt(self.c.WRITEFUNCTION, buf.write)
        self._post(url, params, cr=cr)
        s = buf.getvalue()
        buf.close()
        if ch is not None:
            return s
        return json.loads(s)

    def newcard(self, token):
        """
        Create a credit card from a given token.
        token: string Unique credit card token

        Returns: a dict with a member "data" containing a dict representing a CC
        """
        return self._apicall(self.bridge + "payments", (("token", token),))

    def getcarddetails(self, cardid):
        """
        Get the details of a credit card from its id.
        cardid: string Unique id for the credit card

        Returns: a dict with a member "data" containing a dict representing a CC
        """
        return self._apicall(self.bridge + "payments/" + str(cardid), cr='GET')

    def getcards(self):
        """
        List all stored cards.

        Returns: a dict with a member "data" which is an array of dicts, each representing a CC
        """
        return self._apicall(self.bridge + "payments")

    def delcard(self, cardid):
        """
        Delete a stored CC
        cardid: Unique id for the CC to be deleted

        Returns: a dict with an member "data" containing an empty array
        """
        return self._apicall(self.bridge + "payments/%s" % (str(cardid),), cr="DELETE")

    def transact(self, amount=0, currency="eur", description=None, token=None, client=None, payment=None):
        """
        Create a transaction (charge a card). You must provide an amount, and exactly one funding source.
        The amount is in Eurocents, and the funding source can be a client, a token.
        amount: The amount (in Euro CENTS) to be charged. For example, 240 will charge 2 euros and 40 cents, NOT 240 euros.
        currency: Must be "eur" if given (optional)
        description: A short description of the transaction (optional)
        token: A token generated by the paymill bridge js library
        client: A client id number

        Returns: None if one of the required parameters is missing. A dict with a member "data" containing a transaction dict otherwise.
        """

        p = []
        if token is not None:
            p += [("token", token)]
        elif client is not None:
            p += [("client", client)]
        elif payment is not None:
            p += [("payment", payment)]
        else:
            return None
        if amount == 0:
            return None
        if description is not None:
            p += [("description", description)]
        p += [("amount", str(amount))]
        p += [("currency", currency)]
        return self._apicall(self.bridge + "transactions", tuple(p))

    def gettrandetails(self, tranid):
        """
        Get details on a transaction.
        tranid: string Unique id for the transaction

        Returns: a dict representing a transaction
        """
        return self._apicall(self.bridge + "transactions/" + str(tranid))

    def gettrans(self):
        """
        List all transactions.

        Returns: a dict with a member "data" which is an array of dicts, each representing a transaction
        """
        return self._apicall(self.bridge + "transactions/")

    def refund(self, tranid, amount, description=None):
        """
        Refunds an already performed transaction.
        tranid: string Unique transaction id
        amount: The amount in cents that are to be refunded
        description: A description of the refund (optional)

        Returns: a dict with a member "data" which is a dict representing a refund, or None if the amount is 0
        """
        if amount == 0:
            return None
        p = [("amount", str(amount))]
        if description is not None:
            p += [("description", description)]
        return self._apicall(self.bridge + "refund/" + str(tranid), tuple(p))

    def getrefdetails(self, refid):
        """
        Get the details of a refund from its id.
        refid: string Unique id for the refund

        Returns: a dict with a member "data" which is a dict representing a refund
        """
        return self._apicall(self.bridge + "refunds/" + str(refid))

    def getrefs(self):
        """
        List all stored refunds.

        Returns: a dict with a member "data" which is an array of dicts, each representing a refund
        """
        return self._apicall(self.bridge + "refunds/")

    def newclient(self, email, description=None):
        """
        Creates a new client.
        email: client's email address
        description: description of this client (optional)

        Returns: a dict with a member "data" which is a dict representing a client.
        """
        p = [("email", str(email))]
        if description is not None:
            p += [("description", description)]
        return self._apicall(self.bridge + "clients", tuple(p))

    def getclientdetails(self, cid):
        """
        Get the details of a client from its id.
        cid: string Unique id for the client

        Returns: a dict with a member "data" which is a dict representing a client
        """
        return self._apicall(self.bridge + "clients/" + str(cid))

    def updateclient(self, cid, email, description=None):
        """
        Updates the details of a client.
        cid: string Unique client id
        email: The email of the client
        description: A description of the client (optional)

        Returns: a dict with a member "data" which is a dict representing a client
        """
        p = [("email", str(email))]
        if description is not None:
            p += [("description", description)]
        return self._apicall(self.bridge + "clients/" + str(cid), tuple(p), cr='PUT')

    def delclient(self, cid):
        """
        Delete a stored client
        cid: Unique id for the client to be deleted

        Returns: a dict with an member "data" containing an empty array
        """
        return self._apicall(self.bridge + "clients/%s" % (str(cid),), cr="DELETE")

    def getclients(self):
        """
        List all stored clients.

        Returns: a dict with a member "data" which is an array of dicts, each representing a client
        """
        return self._apicall(self.bridge + "clients/")

    def exportclients(self):
        """
        Export all stored clients in CSV form

        Returns: the contents of the CSV file
        """
        return self._apicall(self.bridge + "clients/", ch=["Accept: text/csv"])

    def newoffer(self, amount, interval="month", currency="eur", name=None):
        """
        Creates a new offer
        amount: The amount in cents that are to be charged every interval
        interval: MUST be either "week", "month" or "year"
        currency: Must be "eur" if given (optional)
        name: A name for this offer

        Returns: a dict with a member "data" which is a dict representing
            an offer, or None if the amount is 0 or the interval is invalid
        """
        if amount == 0:
            return None
        p = [("amount", str(amount))]
        if interval not in ["week", "month", "year"]:
            return None
        p += [("interval", str(interval))]
        if name is not None:
            p += [("name", name)]
        return self._apicall(self.bridge + "offers", tuple(p))

    def getofferdetails(self, oid):
        """
        Get the details of an offer from its id.
        oid: string Unique id for the offer

        Returns: a dict with a member "data" which is a dict representing an offer
        """
        return self._apicall(self.bridge + "offers/" + str(oid))

    def updateoffer(self, oid, name):
        """
        Updates the details of an offer. Only the name may be changed
        oid: string Unique offer id
        name: The new name of the offer

        Returns: a dict with a member "data" which is a dict representing an offer
        """
        p = [("name", str(name))]
        return self._apicall(self.bridge + "offers/" + str(oid), tuple(p))

    def deloffer(self, oid):
        """
        Delete a stored offer. May only be done if no subscriptions to this offer are active.
        oid: Unique id for the offer to be deleted

        Returns: a dict with an member "data" containing an empty array
        """
        return self._apicall(self.bridge + "offers/%s" % (str(oid),), cr="DELETE")

    def getoffers(self):
        """
        List all stored offers.

        Returns: a dict with a member "data" which is an array of dicts, each representing an offer
        """
        return self._apicall(self.bridge + "offers/")

    def newsub(self, client, offer):
        """
        Subscribes a client to an offer
        client: The id of the client
        offer: The id of the offer

        Returns: a dict with a member "data" which is a dict representing a subscription
        """
        p = [("offer", str(offer)), ("token", str(client))]
        return self._apicall(self.bridge + "subscriptions", tuple(p))

    def getsubdetails(self, sid):
        """
        Get the details of a subscription from its id.
        sid: string Unique id for the subscription

        Returns: a dict with a member "data" which is a dict representing a subscription
        """
        return self._apicall(self.bridge + "subscriptions/" + str(sid))

    def cancelsubafter(self, sid, cancel=True):
        """
        Cancels a subscription after its interval ends
        sid: string Unique subscription id
        cancel: If True, the subscription will be cancelled at the end of its interval. Set to False to undo.

        Returns: a dict with a member "data" which is a dict representing a subscription
        """
        if cancel:
            p = [("cancel_at_period_end", "true")]
        else:
            p = [("cancel_at_period_end", "false")]
        return self._apicall(self.bridge + "subscriptions/" + str(sid), tuple(p))

    def cancelsubnow(self, sid):
        """
        Cancel a subscription immediately. Pending transactions will still be charged.
        sid: Unique subscription id

        Returns: a dict with an member "data"
        """
        return self._apicall(self.bridge + "subscriptions/%s" % (str(sid),), cr="DELETE")

    def getsubs(self):
        """
        List all stored subscriptions.

        Returns: a dict with a member "data" which is an array of dicts, each representing a subscription
        """
        return self._apicall(self.bridge + "subscriptions/")

if __name__ == "__main__":
    p = Pymill("YOURPRIVATEKEYHERE")
    cc = (p.getcards())["data"][0]["id"]
    print p.getcarddetails(cc)
    #print p.transact(amount=300,card=cc,description="pymilltest")
