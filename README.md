This library provides access to the Paymill API from a Python application.

It depends on [Requests](http://docs.python-requests.org/en/latest/), and thereby should also work on Google App Engine.

Example of usage:
```python
import pymill
p = pymill.Pymill("YOUR PRIVATE KEY GOES HERE")
for card in p.getcards():
    print card["id"] # show IDs for all stored cards

card = p.newcard("token from Paymill bridge goes here") # store a credit card
transaction = p.transact(230, payment=card["id"]) # charge card with 2 Euros and 30 Cents
ref = p.refund(transaction["id"],30) # refund 30 cents
```

Find the remaining documentation at http://pymill.readthedocs.org.
