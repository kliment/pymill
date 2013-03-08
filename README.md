This library provides access to the Paymill API from a Python application.

It depends on [Requests](http://docs.python-requests.org/en/latest/), so you'll need to install that first.
The latest version of Requests reportedly works on Google App Engine.

Example of usage:

	import pymill
	p=pymill.Pymill("YOUR PRIVATE KEY GOES HERE")
	for i in p.getcards()["data"]:
		print i["id"] #show IDs for all stored cards
	
	card=p.newcard("token from Paymill bridge goes here")["data"] #store a credit card
	print card
	transaction=transact(230, payment=card["id"])["data"] #Charge card with 2 Euros and 30 Cents
	print transaction
	ref=refund(transaction["id"],30) #refund 30 cents
	print ref

Read the source to see all the functions implemented.

Here is the automatically generated help for this module:

    class Pymill
     |  These are the parameters each object type contains
     |  
     |  Payment:
     |  id: unique payment method ID
     |  type: creditcard or debit
     |  client: id of associatied client (optional)
     |  created_at: unixtime
     |  updated_at: unixtime
     |  (For credit cards only)
     |  card_type: visa, mastercard, (maybe one day american express)
     |  country: country the card was issued in
     |  expire_month: (2ch)
     |  expire_year: (4ch)
     |  card_holder: name of cardholder
     |  last4: last 4 digits of card
     |  (For debit accounts only)
     |  code: the sorting code of the bank
     |  account: a partially masked account number
     |  holder: name of the account holder
     |  
     |  Preauthorization:
     |  id: unique preauthorization ID
     |  amount: amount preauthorized in CENTS
     |  status: open, pending, closed, failed, deleted, or preauth
     |  livemode: true or false depending on whether the transaction is real or in test mode
     |  payment: a credit card payment method object (see above)
     |  client: if a preset client (see below) was used to make the transaction. Otherwise null
     |  created_at: unixtime
     |  updated_at: unixtime
     |  
     |  Transaction:
     |  id: unique transaction ID
     |  amount: amount charged in CENTS
     |  status: open, pending, closed, failed, partial_refunded, refunded, or preauthorize (closed means success)
     |  description: user-selected description of the transaction
     |  livemode: true or false depending on whether the transaction is real or in test mode
     |  payment: a payment method object (see above)
     |  preauthorization: the preauthorization associated with this transaction (optional)
     |  created_at: unixtime
     |  updated_at: unixtime
     |  
     |  Refund:
     |  id: unique refund ID
     |  transaction: The unique transaction ID of the transaction being refunded
     |  amount: amount refunded in CENTS
     |  status: open, pending or refunded
     |  description: user-selected description of the refund
     |  livemode: true or false depending on whether the transaction is real or in test mode
     |  created_at: unixtime
     |  updated_at: unixtime
     |  
     |  Client:
     |  id: unique id for this client
     |  email: client's email address (optional)
     |  description: description of this client (optional)
     |  created_at: unix timestamp identifying time of creation
     |  updated_at: unix timestamp identifying time of last change
     |  payment: list of cc or debit objects
     |  subscription: subscription object (optional)
     |  
     |  Offer:
     |  id: unique offer identifier
     |  name: freely controllable offer name
     |  amount: The amount, in CENTS, to be charged every time the offer period passes. Note that ODD values will NOT work in test mode.
     |  interval: "week", "month", or "year". The client will be charged every time the interval passes
     |  trial_period_days: Number of days before the first charge. (optional)
     |  
     |  Subscription:
     |  id: unique subscription identifier
     |  offer: unique offer identifier
     |  livemode: true or false depending on whether the transaction is real or in test mode
     |  cancel_at_period_end: true if subscription is to be cancelled at the end of current period, false if to be cancelled immediately
     |  created_at: unix timestamp identifying time of creation
     |  updated_at: unix timestamp identifying time of last change
     |  canceled_at: unix timestamp identifying time of cancellation(optional)
     |  interval: "week", "month", or "year". The client will be charged every time the interval passes
     |  clients: array of client objects
     |  
     |  Methods defined here:
     |  
     |  __init__(self, privatekey)
     |      Initialize a new paymill interface connection. Requires a private key.
     |  
     |  cancelsubafter(self, sid, cancel=True)
     |      Cancels a subscription after its interval ends
     |      sid: string Unique subscription id
     |      cancel: If True, the subscription will be cancelled at the end of its interval. Set to False to undo.
     |      
     |      Returns: a dict with a member "data" which is a dict representing a subscription
     |  
     |  cancelsubnow(self, sid)
     |      Cancel a subscription immediately. Pending transactions will still be charged.
     |      sid: Unique subscription id
     |      
     |      Returns: a dict with an member "data"
     |  
     |  delcard(self, cardid)
     |      Delete a stored CC
     |      cardid: Unique id for the CC to be deleted
     |      
     |      Returns: a dict with an member "data" containing an empty array
     |  
     |  delclient(self, cid)
     |      Delete a stored client
     |      cid: Unique id for the client to be deleted
     |      
     |      Returns: a dict with an member "data" containing an empty array
     |  
     |  deloffer(self, oid)
     |      Delete a stored offer. May only be done if no subscriptions to this offer are active.
     |      oid: Unique id for the offer to be deleted
     |      
     |      Returns: a dict with an member "data" containing an empty array
     |  
     |  exportclients(self)
     |      Export all stored clients in CSV form
     |      
     |      Returns: the contents of the CSV file
     |  
     |  getcarddetails(self, cardid)
     |      Get the details of a credit card from its id.
     |      cardid: string Unique id for the credit card
     |      
     |      Returns: a dict with a member "data" containing a dict representing a CC
     |  
     |  getcards(self)
     |      List all stored cards.
     |      
     |      Returns: a dict with a member "data" which is an array of dicts, each representing a CC or debit card
     |  
     |  getclientdetails(self, cid)
     |      Get the details of a client from its id.
     |      cid: string Unique id for the client
     |      
     |      Returns: a dict with a member "data" which is a dict representing a client
     |  
     |  getclients(self)
     |      List all stored clients.
     |      
     |      Returns: a dict with a member "data" which is an array of dicts, each representing a client
     |  
     |  getofferdetails(self, oid)
     |      Get the details of an offer from its id.
     |      oid: string Unique id for the offer
     |      
     |      Returns: a dict with a member "data" which is a dict representing an offer
     |  
     |  getoffers(self)
     |      List all stored offers.
     |      
     |      Returns: a dict with a member "data" which is an array of dicts, each representing an offer
     |  
     |  getpreauth(self)
     |      List all preauthorizations.
     |      
     |      Returns: a dict with a member "data" which is an array of dicts, each representing a preauthorization
     |  
     |  getpreauthdetails(self, preid)
     |      Get details on a preauthorization.
     |      preid: string Unique id for the preauthorization
     |      
     |      Returns: a dict representing a preauthorization
     |  
     |  getrefdetails(self, refid)
     |      Get the details of a refund from its id.
     |      refid: string Unique id for the refund
     |      
     |      Returns: a dict with a member "data" which is a dict representing a refund
     |  
     |  getrefs(self)
     |      List all stored refunds.
     |      
     |      Returns: a dict with a member "data" which is an array of dicts, each representing a refund
     |  
     |  getsubdetails(self, sid)
     |      Get the details of a subscription from its id.
     |      sid: string Unique id for the subscription
     |      
     |      Returns: a dict with a member "data" which is a dict representing a subscription
     |  
     |  getsubs(self)
     |      List all stored subscriptions.
     |      
     |      Returns: a dict with a member "data" which is an array of dicts, each representing a subscription
     |  
     |  gettrans(self)
     |      List all transactions.
     |      
     |      Returns: a dict with a member "data" which is an array of dicts, each representing a transaction
     |  
     |  gettransdetails(self, tranid)
     |      Get details on a transaction.
     |      tranid: string Unique id for the transaction
     |      
     |      Returns: a dict representing a transaction
     |  
     |  newcard(self, token, client=None)
     |      Create a credit card from a given token.
     |      token: string Unique credit card token
     |      client: A client id number (optional)
     |      
     |      Returns: a dict with a member "data" containing a dict representing a CC
     |  
     |  newclient(self, email=None, description=None)
     |      Creates a new client.
     |      email: client's email address
     |      description: description of this client (optional)
     |      
     |      Returns: a dict with a member "data" which is a dict representing a client.
     |  
     |  newdebit(self, code, account, holder, client=None)
     |      Create a debit card from account data.
     |      code: A bank sorting code
     |      account: The account number
     |      holder: The name of the account holder
     |      client: A client id number (optional)
     |      
     |      
     |      Returns: a dict with a member "data" containing a dict representing a debit card
     |  
     |  newoffer(self, amount, interval='month', currency='eur', name=None)
     |      Creates a new offer
     |      amount: The amount in cents that are to be charged every interval
     |      interval: MUST be either "week", "month" or "year"
     |      currency: Must be "eur" if given (optional)
     |      name: A name for this offer
     |      
     |      Returns: a dict with a member "data" which is a dict representing 
     |          an offer, or None if the amount is 0 or the interval is invalid
     |  
     |  newsub(self, client, offer, payment)
     |      Subscribes a client to an offer
     |      client: The id of the client
     |      offer: The id of the offer
     |      payment: The id of the payment instrument used for this offer
     |      
     |      Returns: a dict with a member "data" which is a dict representing a subscription
     |  
     |  preauth(self, amount=0, currency='eur', description=None, token=None, client=None, payment=None)
     |      Preauthorize a transaction (reserve value a card). You must provide an amount, and exactly one funding source.
     |      The amount is in cents, and the funding source can be a token or a payment id.
     |      amount: The amount (in CENTS) to be charged. For example, 240 will charge 2 euros and 40 cents, NOT 240 euros.
     |      currency: ISO4217 (optional)
     |      token: A token generated by the paymill bridge js library
     |      payment: A payment method id number. Must represent a credit card, not a debit payment.
     |      
     |      Returns: None if one of the required parameters is missing. A dict with a member "data" containing a preauthorization dict otherwise.
     |  
     |  refund(self, tranid, amount, description=None)
     |      Refunds an already performed transaction.
     |      tranid: string Unique transaction id
     |      amount: The amount in cents that are to be refunded
     |      description: A description of the refund (optional)
     |      
     |      Returns: a dict with a member "data" which is a dict representing a refund, or None if the amount is 0
     |  
     |  transact(self, amount=0, currency='eur', description=None, token=None, client=None, payment=None, preauth=None, code=None, account=None, holder=None)
     |      Create a transaction (charge a card or account). You must provide an amount, and exactly one funding source.
     |      The amount is in cents, and the funding source can be a payment method id, a token, a preauthorization or a direct debit account.
     |      amount: The amount (in CENTS) to be charged. For example, 240 will charge 2 euros and 40 cents, NOT 240 euros.
     |      currency: ISO4217 currency code (optional)
     |      description: A short description of the transaction (optional)
     |      token: A token generated by the paymill bridge js library
     |      client: A client id number (optional)
     |      payment: A payment method id number (credit card id or debit account id)
     |      preauth: A preauthorization id number
     |      code: If paying by debit, the bank sorting code
     |      account: If paying by debit, the account number
     |      holder: If paying by debit, the name of the account holder
     |      
     |      Returns: None if one of the required parameters is missing. A dict with a member "data" containing a transaction dict otherwise.
     |  
     |  updateclient(self, cid, email, description=None)
     |      Updates the details of a client.
     |      cid: string Unique client id
     |      email: The email of the client
     |      description: A description of the client (optional)
     |      
     |      Returns: a dict with a member "data" which is a dict representing a client
     |  
     |  updateoffer(self, oid, name)
     |      Updates the details of an offer. Only the name may be changed
     |      oid: string Unique offer id
     |      name: The new name of the offer
     |      
     |      Returns: a dict with a member "data" which is a dict representing an offer


