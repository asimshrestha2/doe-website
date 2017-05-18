from flask import request, session
import stripe

class StripeManager:

    def __init__(self):
        stripe.api_key = "" #insert API key here, two types, test and live

    def charge(self):
        amount = 500
        token = request.form['stripeToken']
        #save customer token
        if token is not None and session.get('CID'):
            customer = stripe.Customer.create(
                email='customer@example.com',
                source=token 
            )
            session['CID'] = customer.id
        else:
            return -1 #some error

        try:   
            charge = stripe.Charge.create(
                customer = session['CID'],
                amount=amount,
                currency='usd',
                metadata={"event_id": session['eid'], "event_name": session['ename'], "state":session['state']}, #add extra metadata here
                description='Flask Charge'
            )
            
            session.pop('eid', None)
            session.pop('ename', None)
            session.pop('state', None)
            
        except stripe.error.CardError as e: #card decline
            body = e.json_body
            err  = body['error']
            print ("Status is: %s" % e.http_status)
            print ("Type is: %s" % err['type'])
            print ("Code is: %s" % err['code'])
            print ("Param is: %s" % err['param'])
            print ("Message is: %s" % err['message'])
            return -1 #let this be default error parameter
        except Exception as e:
            return -1

    #get all purchase history
    def balance(self):
        #grab list of transactions contributing to stripe account balance
        transactionInfo = stripe.BalanceTransaction.all()
        #get the charge id
        for transaction in transactionInfo.data:
            cID = transaction.source
            charge = stripe.Charge.retrieve(cID)
            md = charge.metadata
            if 'event_name' in md: #check if key exists
                print(md['event_name'])

    #wrap a function in this to error check it
    def errhandlingwrapper(self, methodToCheck):
        try:
           methodToCheck() #pass in some stripe operation from this class
        #handle stripe request
        except stripe.error.CardError as e:
          # Since it's a decline, stripe.error.CardError will be caught
          body = e.json_body
          err  = body['error']
          print ("Status is: %s" % e.http_status)
          print ("Type is: %s" % err['type'])
          print ("Code is: %s" % err['code'])
          # param is '' in this case
          print ("Param is: %s" % err['param'])
          print ("Message is: %s" % err['message'])
        except stripe.error.RateLimitError as e:
          # Too many requests made to the API too quickly
          pass
        except stripe.error.InvalidRequestError as e:
          # Invalid parameters were supplied to Stripe's API
          pass
        except stripe.error.AuthenticationError as e:
          # Authentication with Stripe's API failed
          # (maybe you changed API keys recently)
          pass
        except stripe.error.APIConnectionError as e:
          # Network communication with Stripe failed
          pass
        except stripe.error.StripeError as e:
          # Display a very generic error to the user, and maybe send
          # yourself an email
          pass
        except Exception as e:
          # Something else happened, completely unrelated to Stripe
          pass
                
