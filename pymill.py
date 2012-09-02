#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-
#pymill.py

import pycurl, cStringIO, json


class Pymill():
    
    def __init__(self, privatekey):
        self.c=pycurl.Curl()
        self.c.setopt(pycurl.NOSIGNAL, 1)
        self.c.setopt(pycurl.CONNECTTIMEOUT, 30)
        self.c.setopt(pycurl.USERPWD, '%s:' % (privatekey,))
        
    def post(self,url,params):
        self.c.setopt(self.c.URL, url)
        if params is not ():
            p=str("&".join([i[0]+"="+i[1] for i in params]))
            print p
            self.c.setopt(pycurl.CUSTOMREQUEST, "POST")
            self.c.setopt(self.c.POSTFIELDS,p)
        self.c.perform()
        
    def apicall(self,url,params=(),cr="GET"):
        self.c.setopt(pycurl.CUSTOMREQUEST, cr)
        buf=cStringIO.StringIO()
        self.c.setopt(self.c.WRITEFUNCTION, buf.write)
        self.post(url, params)
        s=buf.getvalue()
        buf.close()
        return json.loads(s)

    def getcard(self,token):
        return self.apicall("https://api.paymill.de/v1/creditcards",(("token", token),))

    def getcards(self):
        return self.apicall("https://api.paymill.de/v1/creditcards/")

    def getcarddetails(self, cardid):
        return self.apicall("https://api.paymill.de/v1/creditcards/"+str(cardid))
        
    def delcard(self, cardid):
        return self.apicall("https://api.paymill.de/v1/creditcards/%s"%(str(cardid),),cr="DELETE")
        
    def transact(self, amount=0, currency="eur", description=None, token=None, client=None, card=None):
        p=[]
        if token is not None:
            p+=[("token",token)]
        elif client is not None:
            p+=[("client",client)]
        elif card is not None:
            p+=[("creditcard",card)]
        if amount==0:
            return
        if description is not None:
            p+=[("description",description)]
        p+=[("amount",str(amount))]
        p+=[("currency",currency)]
        return self.apicall("https://api.paymill.de/v1/transactions/",tuple(p))
                
    
    
if __name__=="__main__":
    p=Pymill("YOURPRIVATEKEYHERE")
    cc=(p.getcards())["data"][0]["id"]
    print p.getcarddetails(cc)
    #print p.transact(amount=300,card=cc,description="pymilltest")
    
