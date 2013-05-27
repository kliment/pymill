This library provides access to the Paymill API from a Python application.

It depends on [Requests](http://docs.python-requests.org/en/latest/), and thereby should also work on Google App Engine.

Example of usage:
```python
import pymill
p = pymill.Pymill("YOUR PRIVATE KEY GOES HERE")

# show IDs for all stored cards
for card in p.getcards():
    print card 

# create new card, run transaction on it and refund part of that again
card = p.newcard("token from Paymill bridge goes here")
transaction = p.transact(230, payment=card)
ref = p.refund(transaction, 30)
```

Find the remaining documentation at http://pymill.readthedocs.org.
