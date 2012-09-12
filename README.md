This library provides access to the Paymill API from a Python application.

It depends on pycurl, so you'll need to install that first.

Example of usage:

	import pymill
	p=pymill.Pymill("YOUR PRIVATE KEY GOES HERE")
	for i in p.getcards()["data"]:
		print i["id"]
	
	card=p.newcard("token from Paymill bridge goes here")["data"] #store a credit card
	print card
	transaction=transact(230, card=card["id"])["data"] #Charge card with 2 Euros and 30 Cents
	print transaction
	ref=refund(transaction["id"],30) #refund 30 cents
	print ref

Read the source to see all the functions implemented.
