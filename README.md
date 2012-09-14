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

Here is the automatically generated help for this module:

<table width="100%" cellspacing=0 cellpadding=2 border=0 summary="heading">
<tr bgcolor="#7799ee">
<td valign=bottom>&nbsp;<br>
<font color="#ffffff" face="helvetica, arial">&nbsp;<br><big><big><strong>pymill</strong></big></big></font></td
><td align=right valign=bottom
><font color="#ffffff" face="helvetica, arial"><a href=".">index</a><br><a href="file:/home/kliment/designs/pymill/pymill.py">/home/kliment/designs/pymill/pymill.py</a></font></td></tr></table>
    <p><tt>#&nbsp;-*-&nbsp;coding:&nbsp;utf-8&nbsp;-*-<br>
#pymill.py</tt></p>
<p>
<table width="100%" cellspacing=0 cellpadding=2 border=0 summary="section">
<tr bgcolor="#aa55cc">
<td colspan=3 valign=bottom>&nbsp;<br>
<font color="#ffffff" face="helvetica, arial"><big><strong>Modules</strong></big></font></td></tr>
    
<tr><td bgcolor="#aa55cc"><tt>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</tt></td><td>&nbsp;</td>
<td width="100%"><table width="100%" summary="list"><tr><td width="25%" valign=top><a href="cStringIO.html">cStringIO</a><br>
</td><td width="25%" valign=top><a href="json.html">json</a><br>
</td><td width="25%" valign=top><a href="pycurl.html">pycurl</a><br>
</td><td width="25%" valign=top></td></tr></table></td></tr></table><p>
<table width="100%" cellspacing=0 cellpadding=2 border=0 summary="section">
<tr bgcolor="#ee77aa">
<td colspan=3 valign=bottom>&nbsp;<br>
<font color="#ffffff" face="helvetica, arial"><big><strong>Classes</strong></big></font></td></tr>
    
<tr><td bgcolor="#ee77aa"><tt>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</tt></td><td>&nbsp;</td>
<td width="100%"><dl>
<dt><font face="helvetica, arial"><a href="pymill.html#Pymill">Pymill</a>
</font></dt></dl>
 <p>
<table width="100%" cellspacing=0 cellpadding=2 border=0 summary="section">
<tr bgcolor="#ffc8d8">
<td colspan=3 valign=bottom>&nbsp;<br>
<font color="#000000" face="helvetica, arial"><a name="Pymill">class <strong>Pymill</strong></a></font></td></tr>
    
<tr bgcolor="#ffc8d8"><td rowspan=2><tt>&nbsp;&nbsp;&nbsp;</tt></td>
<td colspan=2><tt>These&nbsp;are&nbsp;the&nbsp;parameters&nbsp;each&nbsp;object&nbsp;type&nbsp;contains<br>
&nbsp;<br>
Card:<br>
id:&nbsp;unique&nbsp;card&nbsp;ID<br>
card_type:&nbsp;visa,&nbsp;mastercard,&nbsp;(maybe&nbsp;one&nbsp;day&nbsp;american&nbsp;express)<br>
country:&nbsp;country&nbsp;the&nbsp;card&nbsp;was&nbsp;issued&nbsp;in<br>
expire_month:&nbsp;(2ch)<br>
expire_year:&nbsp;(4ch)<br>
card_holder:&nbsp;name&nbsp;of&nbsp;cardholder<br>
last4:&nbsp;last&nbsp;4&nbsp;digits&nbsp;of&nbsp;card<br>
created_at:&nbsp;unixtime<br>
updated_at:&nbsp;unixtime<br>
&nbsp;<br>
Transaction:<br>
id:&nbsp;unique&nbsp;transaction&nbsp;ID<br>
amount:&nbsp;amount&nbsp;charged&nbsp;in&nbsp;EuroCENTS<br>
status:&nbsp;open,&nbsp;pending,&nbsp;closed&nbsp;or&nbsp;refunded<br>
description:&nbsp;user-selected&nbsp;description&nbsp;of&nbsp;the&nbsp;transaction<br>
livemode:&nbsp;true&nbsp;or&nbsp;false&nbsp;depending&nbsp;on&nbsp;whether&nbsp;the&nbsp;transaction&nbsp;is&nbsp;real&nbsp;or&nbsp;in&nbsp;test&nbsp;mode<br>
creditcard:&nbsp;a&nbsp;card&nbsp;object&nbsp;(see&nbsp;above)<br>
clients:&nbsp;if&nbsp;a&nbsp;preset&nbsp;client&nbsp;(see&nbsp;below)&nbsp;was&nbsp;used&nbsp;to&nbsp;make&nbsp;the&nbsp;transaction.&nbsp;Otherwise&nbsp;null<br>
created_at:&nbsp;unixtime<br>
updated_at:&nbsp;unixtime<br>
&nbsp;<br>
Refund:<br>
id:&nbsp;unique&nbsp;refund&nbsp;ID<br>
transaction:&nbsp;The&nbsp;unique&nbsp;transaction&nbsp;ID&nbsp;of&nbsp;the&nbsp;transaction&nbsp;being&nbsp;refunded<br>
amount:&nbsp;amount&nbsp;refunded&nbsp;in&nbsp;EuroCENTS<br>
status:&nbsp;open,&nbsp;pending&nbsp;or&nbsp;refunded<br>
description:&nbsp;user-selected&nbsp;description&nbsp;of&nbsp;the&nbsp;refund<br>
livemode:&nbsp;true&nbsp;or&nbsp;false&nbsp;depending&nbsp;on&nbsp;whether&nbsp;the&nbsp;transaction&nbsp;is&nbsp;real&nbsp;or&nbsp;in&nbsp;test&nbsp;mode<br>
created_at:&nbsp;unixtime<br>
updated_at:&nbsp;unixtime<br>
&nbsp;<br>
Client:<br>
id:&nbsp;unique&nbsp;id&nbsp;for&nbsp;this&nbsp;client<br>
email:&nbsp;client's&nbsp;email&nbsp;address&nbsp;(optional)<br>
description:&nbsp;description&nbsp;of&nbsp;this&nbsp;client&nbsp;(optional)<br>
created_at:&nbsp;unix&nbsp;timestamp&nbsp;identifying&nbsp;time&nbsp;of&nbsp;creation<br>
updated_at:&nbsp;unix&nbsp;timestamp&nbsp;identifying&nbsp;time&nbsp;of&nbsp;last&nbsp;change<br>
creditcard:&nbsp;cc&nbsp;object&nbsp;(optional)<br>
subscription:&nbsp;subscription&nbsp;object&nbsp;(optional)<br>
&nbsp;<br>
Offer:<br>
id:&nbsp;unique&nbsp;offer&nbsp;identifier<br>
name:&nbsp;freely&nbsp;controllable&nbsp;offer&nbsp;name<br>
amount:&nbsp;The&nbsp;amount,&nbsp;in&nbsp;EuroCENTS,&nbsp;to&nbsp;be&nbsp;charged&nbsp;every&nbsp;time&nbsp;the&nbsp;offer&nbsp;period&nbsp;passes.&nbsp;Note&nbsp;that&nbsp;ODD&nbsp;values&nbsp;will&nbsp;NOT&nbsp;work&nbsp;in&nbsp;test&nbsp;mode.<br>
interval:&nbsp;"week",&nbsp;"month",&nbsp;or&nbsp;"year".&nbsp;The&nbsp;client&nbsp;will&nbsp;be&nbsp;charged&nbsp;every&nbsp;time&nbsp;the&nbsp;interval&nbsp;passes<br>
trial_period_days:&nbsp;Number&nbsp;of&nbsp;days&nbsp;before&nbsp;the&nbsp;first&nbsp;charge.&nbsp;(optional)<br>&nbsp;</tt></td></tr>
<tr><td>&nbsp;</td>
<td width="100%">Methods defined here:<br>
<dl><dt><a name="Pymill-__init__"><strong>__init__</strong></a>(self, privatekey)</dt><dd><tt>Initialize&nbsp;a&nbsp;new&nbsp;paymill&nbsp;interface&nbsp;connection.&nbsp;Requires&nbsp;a&nbsp;private&nbsp;key.</tt></dd></dl>

<dl><dt><a name="Pymill-cancelsubafter"><strong>cancelsubafter</strong></a>(self, sid, cancel<font color="#909090">=True</font>)</dt><dd><tt>Cancels&nbsp;a&nbsp;subscription&nbsp;after&nbsp;its&nbsp;interval&nbsp;ends<br>
sid:&nbsp;string&nbsp;Unique&nbsp;subscription&nbsp;id<br>
cancel:&nbsp;If&nbsp;True,&nbsp;the&nbsp;subscription&nbsp;will&nbsp;be&nbsp;cancelled&nbsp;at&nbsp;the&nbsp;end&nbsp;of&nbsp;its&nbsp;interval.&nbsp;Set&nbsp;to&nbsp;False&nbsp;to&nbsp;undo.<br>
&nbsp;<br>
Returns:&nbsp;a&nbsp;dict&nbsp;with&nbsp;a&nbsp;member&nbsp;"data"&nbsp;which&nbsp;is&nbsp;a&nbsp;dict&nbsp;representing&nbsp;a&nbsp;subscription</tt></dd></dl>

<dl><dt><a name="Pymill-cancelsubnow"><strong>cancelsubnow</strong></a>(self, sid)</dt><dd><tt>Cancel&nbsp;a&nbsp;subscription&nbsp;immediately.&nbsp;Pending&nbsp;transactions&nbsp;will&nbsp;still&nbsp;be&nbsp;charged.<br>
sid:&nbsp;Unique&nbsp;subscription&nbsp;id<br>
&nbsp;<br>
Returns:&nbsp;a&nbsp;dict&nbsp;with&nbsp;an&nbsp;member&nbsp;"data"</tt></dd></dl>

<dl><dt><a name="Pymill-delcard"><strong>delcard</strong></a>(self, cardid)</dt><dd><tt>Delete&nbsp;a&nbsp;stored&nbsp;CC<br>
cardid:&nbsp;Unique&nbsp;id&nbsp;for&nbsp;the&nbsp;CC&nbsp;to&nbsp;be&nbsp;deleted<br>
&nbsp;<br>
Returns:&nbsp;a&nbsp;dict&nbsp;with&nbsp;an&nbsp;member&nbsp;"data"&nbsp;containing&nbsp;an&nbsp;empty&nbsp;array</tt></dd></dl>

<dl><dt><a name="Pymill-delclient"><strong>delclient</strong></a>(self, cid)</dt><dd><tt>Delete&nbsp;a&nbsp;stored&nbsp;client<br>
cid:&nbsp;Unique&nbsp;id&nbsp;for&nbsp;the&nbsp;client&nbsp;to&nbsp;be&nbsp;deleted<br>
&nbsp;<br>
Returns:&nbsp;a&nbsp;dict&nbsp;with&nbsp;an&nbsp;member&nbsp;"data"&nbsp;containing&nbsp;an&nbsp;empty&nbsp;array</tt></dd></dl>

<dl><dt><a name="Pymill-deloffer"><strong>deloffer</strong></a>(self, oid)</dt><dd><tt>Delete&nbsp;a&nbsp;stored&nbsp;offer.&nbsp;May&nbsp;only&nbsp;be&nbsp;done&nbsp;if&nbsp;no&nbsp;subscriptions&nbsp;to&nbsp;this&nbsp;offer&nbsp;are&nbsp;active.<br>
oid:&nbsp;Unique&nbsp;id&nbsp;for&nbsp;the&nbsp;offer&nbsp;to&nbsp;be&nbsp;deleted<br>
&nbsp;<br>
Returns:&nbsp;a&nbsp;dict&nbsp;with&nbsp;an&nbsp;member&nbsp;"data"&nbsp;containing&nbsp;an&nbsp;empty&nbsp;array</tt></dd></dl>

<dl><dt><a name="Pymill-exportclients"><strong>exportclients</strong></a>(self)</dt><dd><tt>Export&nbsp;all&nbsp;stored&nbsp;clients&nbsp;in&nbsp;CSV&nbsp;form<br>
&nbsp;<br>
Returns:&nbsp;the&nbsp;contents&nbsp;of&nbsp;the&nbsp;CSV&nbsp;file</tt></dd></dl>

<dl><dt><a name="Pymill-getcarddetails"><strong>getcarddetails</strong></a>(self, cardid)</dt><dd><tt>Get&nbsp;the&nbsp;details&nbsp;of&nbsp;a&nbsp;credit&nbsp;card&nbsp;from&nbsp;its&nbsp;id.<br>
cardid:&nbsp;string&nbsp;Unique&nbsp;id&nbsp;for&nbsp;the&nbsp;credit&nbsp;card<br>
&nbsp;<br>
Returns:&nbsp;a&nbsp;dict&nbsp;with&nbsp;a&nbsp;member&nbsp;"data"&nbsp;containing&nbsp;a&nbsp;dict&nbsp;representing&nbsp;a&nbsp;CC</tt></dd></dl>

<dl><dt><a name="Pymill-getcards"><strong>getcards</strong></a>(self)</dt><dd><tt>List&nbsp;all&nbsp;stored&nbsp;cards.<br>
&nbsp;<br>
Returns:&nbsp;a&nbsp;dict&nbsp;with&nbsp;a&nbsp;member&nbsp;"data"&nbsp;which&nbsp;is&nbsp;an&nbsp;array&nbsp;of&nbsp;dicts,&nbsp;each&nbsp;representing&nbsp;a&nbsp;CC</tt></dd></dl>

<dl><dt><a name="Pymill-getclientdetails"><strong>getclientdetails</strong></a>(self, cid)</dt><dd><tt>Get&nbsp;the&nbsp;details&nbsp;of&nbsp;a&nbsp;client&nbsp;from&nbsp;its&nbsp;id.<br>
cid:&nbsp;string&nbsp;Unique&nbsp;id&nbsp;for&nbsp;the&nbsp;client<br>
&nbsp;<br>
Returns:&nbsp;a&nbsp;dict&nbsp;with&nbsp;a&nbsp;member&nbsp;"data"&nbsp;which&nbsp;is&nbsp;a&nbsp;dict&nbsp;representing&nbsp;a&nbsp;client</tt></dd></dl>

<dl><dt><a name="Pymill-getclients"><strong>getclients</strong></a>(self)</dt><dd><tt>List&nbsp;all&nbsp;stored&nbsp;clients.<br>
&nbsp;<br>
Returns:&nbsp;a&nbsp;dict&nbsp;with&nbsp;a&nbsp;member&nbsp;"data"&nbsp;which&nbsp;is&nbsp;an&nbsp;array&nbsp;of&nbsp;dicts,&nbsp;each&nbsp;representing&nbsp;a&nbsp;client</tt></dd></dl>

<dl><dt><a name="Pymill-getofferdetails"><strong>getofferdetails</strong></a>(self, oid)</dt><dd><tt>Get&nbsp;the&nbsp;details&nbsp;of&nbsp;an&nbsp;offer&nbsp;from&nbsp;its&nbsp;id.<br>
oid:&nbsp;string&nbsp;Unique&nbsp;id&nbsp;for&nbsp;the&nbsp;offer<br>
&nbsp;<br>
Returns:&nbsp;a&nbsp;dict&nbsp;with&nbsp;a&nbsp;member&nbsp;"data"&nbsp;which&nbsp;is&nbsp;a&nbsp;dict&nbsp;representing&nbsp;an&nbsp;offer</tt></dd></dl>

<dl><dt><a name="Pymill-getoffers"><strong>getoffers</strong></a>(self)</dt><dd><tt>List&nbsp;all&nbsp;stored&nbsp;offers.<br>
&nbsp;<br>
Returns:&nbsp;a&nbsp;dict&nbsp;with&nbsp;a&nbsp;member&nbsp;"data"&nbsp;which&nbsp;is&nbsp;an&nbsp;array&nbsp;of&nbsp;dicts,&nbsp;each&nbsp;representing&nbsp;an&nbsp;offer</tt></dd></dl>

<dl><dt><a name="Pymill-getrefdetails"><strong>getrefdetails</strong></a>(self, refid)</dt><dd><tt>Get&nbsp;the&nbsp;details&nbsp;of&nbsp;a&nbsp;refund&nbsp;from&nbsp;its&nbsp;id.<br>
refid:&nbsp;string&nbsp;Unique&nbsp;id&nbsp;for&nbsp;the&nbsp;refund<br>
&nbsp;<br>
Returns:&nbsp;a&nbsp;dict&nbsp;with&nbsp;a&nbsp;member&nbsp;"data"&nbsp;which&nbsp;is&nbsp;a&nbsp;dict&nbsp;representing&nbsp;a&nbsp;refund</tt></dd></dl>

<dl><dt><a name="Pymill-getrefs"><strong>getrefs</strong></a>(self)</dt><dd><tt>List&nbsp;all&nbsp;stored&nbsp;refunds.<br>
&nbsp;<br>
Returns:&nbsp;a&nbsp;dict&nbsp;with&nbsp;a&nbsp;member&nbsp;"data"&nbsp;which&nbsp;is&nbsp;an&nbsp;array&nbsp;of&nbsp;dicts,&nbsp;each&nbsp;representing&nbsp;a&nbsp;refund</tt></dd></dl>

<dl><dt><a name="Pymill-getsubdetails"><strong>getsubdetails</strong></a>(self, sid)</dt><dd><tt>Get&nbsp;the&nbsp;details&nbsp;of&nbsp;a&nbsp;subscription&nbsp;from&nbsp;its&nbsp;id.<br>
sid:&nbsp;string&nbsp;Unique&nbsp;id&nbsp;for&nbsp;the&nbsp;subscription<br>
&nbsp;<br>
Returns:&nbsp;a&nbsp;dict&nbsp;with&nbsp;a&nbsp;member&nbsp;"data"&nbsp;which&nbsp;is&nbsp;a&nbsp;dict&nbsp;representing&nbsp;a&nbsp;subscription</tt></dd></dl>

<dl><dt><a name="Pymill-getsubs"><strong>getsubs</strong></a>(self)</dt><dd><tt>List&nbsp;all&nbsp;stored&nbsp;subscriptions.<br>
&nbsp;<br>
Returns:&nbsp;a&nbsp;dict&nbsp;with&nbsp;a&nbsp;member&nbsp;"data"&nbsp;which&nbsp;is&nbsp;an&nbsp;array&nbsp;of&nbsp;dicts,&nbsp;each&nbsp;representing&nbsp;a&nbsp;subscription</tt></dd></dl>

<dl><dt><a name="Pymill-gettrandetails"><strong>gettrandetails</strong></a>(self, tranid)</dt><dd><tt>Get&nbsp;details&nbsp;on&nbsp;a&nbsp;transaction.<br>
tranid:&nbsp;string&nbsp;Unique&nbsp;id&nbsp;for&nbsp;the&nbsp;transaction<br>
&nbsp;<br>
Returns:&nbsp;a&nbsp;dict&nbsp;representing&nbsp;a&nbsp;transaction</tt></dd></dl>

<dl><dt><a name="Pymill-gettrans"><strong>gettrans</strong></a>(self)</dt><dd><tt>List&nbsp;all&nbsp;transactions.<br>
&nbsp;<br>
Returns:&nbsp;a&nbsp;dict&nbsp;with&nbsp;a&nbsp;member&nbsp;"data"&nbsp;which&nbsp;is&nbsp;an&nbsp;array&nbsp;of&nbsp;dicts,&nbsp;each&nbsp;representing&nbsp;a&nbsp;transaction</tt></dd></dl>

<dl><dt><a name="Pymill-newcard"><strong>newcard</strong></a>(self, token)</dt><dd><tt>Create&nbsp;a&nbsp;credit&nbsp;card&nbsp;from&nbsp;a&nbsp;given&nbsp;token.<br>
token:&nbsp;string&nbsp;Unique&nbsp;credit&nbsp;card&nbsp;token<br>
&nbsp;<br>
Returns:&nbsp;a&nbsp;dict&nbsp;with&nbsp;a&nbsp;member&nbsp;"data"&nbsp;containing&nbsp;a&nbsp;dict&nbsp;representing&nbsp;a&nbsp;CC</tt></dd></dl>

<dl><dt><a name="Pymill-newclient"><strong>newclient</strong></a>(email, description<font color="#909090">=None</font>)</dt><dd><tt>Creates&nbsp;a&nbsp;new&nbsp;client.<br>
email:&nbsp;client's&nbsp;email&nbsp;address<br>
description:&nbsp;description&nbsp;of&nbsp;this&nbsp;client&nbsp;(optional)<br>
&nbsp;<br>
Returns:&nbsp;a&nbsp;dict&nbsp;with&nbsp;a&nbsp;member&nbsp;"data"&nbsp;which&nbsp;is&nbsp;a&nbsp;dict&nbsp;representing&nbsp;a&nbsp;client.</tt></dd></dl>

<dl><dt><a name="Pymill-newoffer"><strong>newoffer</strong></a>(self, amount, interval<font color="#909090">='month'</font>, currency<font color="#909090">='eur'</font>, name<font color="#909090">=None</font>)</dt><dd><tt>Creates&nbsp;a&nbsp;new&nbsp;offer<br>
amount:&nbsp;The&nbsp;amount&nbsp;in&nbsp;cents&nbsp;that&nbsp;are&nbsp;to&nbsp;be&nbsp;charged&nbsp;every&nbsp;interval<br>
interval:&nbsp;MUST&nbsp;be&nbsp;either&nbsp;"week",&nbsp;"month"&nbsp;or&nbsp;"year"<br>
currency:&nbsp;Must&nbsp;be&nbsp;"eur"&nbsp;if&nbsp;given&nbsp;(optional)<br>
name:&nbsp;A&nbsp;name&nbsp;for&nbsp;this&nbsp;offer<br>
&nbsp;<br>
Returns:&nbsp;a&nbsp;dict&nbsp;with&nbsp;a&nbsp;member&nbsp;"data"&nbsp;which&nbsp;is&nbsp;a&nbsp;dict&nbsp;representing&nbsp;<br>
&nbsp;&nbsp;&nbsp;&nbsp;an&nbsp;offer,&nbsp;or&nbsp;None&nbsp;if&nbsp;the&nbsp;amount&nbsp;is&nbsp;0&nbsp;or&nbsp;the&nbsp;interval&nbsp;is&nbsp;invalid</tt></dd></dl>

<dl><dt><a name="Pymill-newsub"><strong>newsub</strong></a>(self, client, offer)</dt><dd><tt>Subscribes&nbsp;a&nbsp;client&nbsp;to&nbsp;an&nbsp;offer<br>
client:&nbsp;The&nbsp;id&nbsp;of&nbsp;the&nbsp;client<br>
offer:&nbsp;The&nbsp;id&nbsp;of&nbsp;the&nbsp;offer<br>
&nbsp;<br>
Returns:&nbsp;a&nbsp;dict&nbsp;with&nbsp;a&nbsp;member&nbsp;"data"&nbsp;which&nbsp;is&nbsp;a&nbsp;dict&nbsp;representing&nbsp;a&nbsp;subscription</tt></dd></dl>

<dl><dt><a name="Pymill-refund"><strong>refund</strong></a>(self, tranid, amount, description<font color="#909090">=None</font>)</dt><dd><tt>Refunds&nbsp;an&nbsp;already&nbsp;performed&nbsp;transaction.<br>
tranid:&nbsp;string&nbsp;Unique&nbsp;transaction&nbsp;id<br>
amount:&nbsp;The&nbsp;amount&nbsp;in&nbsp;cents&nbsp;that&nbsp;are&nbsp;to&nbsp;be&nbsp;refunded<br>
description:&nbsp;A&nbsp;description&nbsp;of&nbsp;the&nbsp;refund&nbsp;(optional)<br>
&nbsp;<br>
Returns:&nbsp;a&nbsp;dict&nbsp;with&nbsp;a&nbsp;member&nbsp;"data"&nbsp;which&nbsp;is&nbsp;a&nbsp;dict&nbsp;representing&nbsp;a&nbsp;refund,&nbsp;or&nbsp;None&nbsp;if&nbsp;the&nbsp;amount&nbsp;is&nbsp;0</tt></dd></dl>

<dl><dt><a name="Pymill-transact"><strong>transact</strong></a>(self, amount<font color="#909090">=0</font>, currency<font color="#909090">='eur'</font>, description<font color="#909090">=None</font>, token<font color="#909090">=None</font>, client<font color="#909090">=None</font>, card<font color="#909090">=None</font>)</dt><dd><tt>Create&nbsp;a&nbsp;transaction&nbsp;(charge&nbsp;a&nbsp;card).&nbsp;You&nbsp;must&nbsp;provide&nbsp;an&nbsp;amount,&nbsp;and&nbsp;exactly&nbsp;one&nbsp;funding&nbsp;source.<br>
The&nbsp;amount&nbsp;is&nbsp;in&nbsp;Eurocents,&nbsp;and&nbsp;the&nbsp;funding&nbsp;source&nbsp;can&nbsp;be&nbsp;a&nbsp;client,&nbsp;a&nbsp;token,&nbsp;or&nbsp;a&nbsp;card&nbsp;id.<br>
amount:&nbsp;The&nbsp;amount&nbsp;(in&nbsp;Euro&nbsp;CENTS)&nbsp;to&nbsp;be&nbsp;charged.&nbsp;For&nbsp;example,&nbsp;240&nbsp;will&nbsp;charge&nbsp;2&nbsp;euros&nbsp;and&nbsp;40&nbsp;cents,&nbsp;NOT&nbsp;240&nbsp;euros.<br>
currency:&nbsp;Must&nbsp;be&nbsp;"eur"&nbsp;if&nbsp;given&nbsp;(optional)<br>
description:&nbsp;A&nbsp;short&nbsp;description&nbsp;of&nbsp;the&nbsp;transaction&nbsp;(optional)<br>
token:&nbsp;A&nbsp;token&nbsp;generated&nbsp;by&nbsp;the&nbsp;paymill&nbsp;bridge&nbsp;js&nbsp;library<br>
client:&nbsp;A&nbsp;client&nbsp;id&nbsp;number<br>
creditcard:&nbsp;A&nbsp;CC&nbsp;id&nbsp;number.<br>
&nbsp;<br>
Returns:&nbsp;None&nbsp;if&nbsp;one&nbsp;of&nbsp;the&nbsp;required&nbsp;parameters&nbsp;is&nbsp;missing.&nbsp;A&nbsp;dict&nbsp;with&nbsp;a&nbsp;member&nbsp;"data"&nbsp;containing&nbsp;a&nbsp;transaction&nbsp;dict&nbsp;otherwise.</tt></dd></dl>

<dl><dt><a name="Pymill-updateclient"><strong>updateclient</strong></a>(self, cid, email, description<font color="#909090">=None</font>)</dt><dd><tt>Updates&nbsp;the&nbsp;details&nbsp;of&nbsp;a&nbsp;client.<br>
cid:&nbsp;string&nbsp;Unique&nbsp;client&nbsp;id<br>
email:&nbsp;The&nbsp;email&nbsp;of&nbsp;the&nbsp;client<br>
description:&nbsp;A&nbsp;description&nbsp;of&nbsp;the&nbsp;client&nbsp;(optional)<br>
&nbsp;<br>
Returns:&nbsp;a&nbsp;dict&nbsp;with&nbsp;a&nbsp;member&nbsp;"data"&nbsp;which&nbsp;is&nbsp;a&nbsp;dict&nbsp;representing&nbsp;a&nbsp;client</tt></dd></dl>

<dl><dt><a name="Pymill-updateoffer"><strong>updateoffer</strong></a>(self, oid, name)</dt><dd><tt>Updates&nbsp;the&nbsp;details&nbsp;of&nbsp;an&nbsp;offer.&nbsp;Only&nbsp;the&nbsp;name&nbsp;may&nbsp;be&nbsp;changed<br>
oid:&nbsp;string&nbsp;Unique&nbsp;offer&nbsp;id<br>
name:&nbsp;The&nbsp;new&nbsp;name&nbsp;of&nbsp;the&nbsp;offer<br>
&nbsp;<br>
Returns:&nbsp;a&nbsp;dict&nbsp;with&nbsp;a&nbsp;member&nbsp;"data"&nbsp;which&nbsp;is&nbsp;a&nbsp;dict&nbsp;representing&nbsp;an&nbsp;offer</tt></dd></dl>

</td></tr></table></td></tr></table>
