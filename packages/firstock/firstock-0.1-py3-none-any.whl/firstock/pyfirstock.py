# -*- coding: utf-8 -*-
"""
Rest API Documentation
   http://developers.thefirstock.com/api/
"""

import hmac
import hashlib
import base64
import requests
import json
import traceback



class api:
    """
    A class Which has methods to handle all the api calls to firstock

    """
    
    def __init__(self,api_key,api_secret,user_id,api_type="user"):
        """
         Function used to initialize object of class api.
         ...

         Attributes
         ----------
         api_key : str
             User Api key 
         api_secret : str
             User Api secret 
         user_id    : str
            Userid of Firstock account
         account_id :str
            Account id of Firstock account
         api_type : str
            If api cradentials are of user account value is "user"
            If api cradentials are of Partner account value is "partner"
         ----------
         Example:
        firstock=api(api_key="my_api_key",api_secret="my_api_secret",user_id="my_user_id",api_type="user")
         """








        self._api_key=api_key
        self._api_secret=api_secret
        self._session_id=""
        self._access_token="" 
        self._user_id=user_id
        self._account_id=user_id
        self._api_type=api_type
        self._endpoint=""
    
    
    
    
    
    def login_url(self):
        try:
            if self._api_type.lower()=="user" :
                return "http://api.thefirstock.com/v1/login?api_key=" + str(self._api_key)

            elif self._api_type.lower()=="partner" :
                return "http://api.thefirstock.com/v1/applogin?api_key=" + str(self._api_key)
            else :
                return {"stat": "Not_Ok","emsg": "ivalid_api_type"}        
        except Exception as ex:
            #traceback.print_exc()
            return ex
                               
    def generate_accesstoken(self,request_token):
        try:
            if self._api_type.lower()=="user" :
                self._endpoint='http://api.thefirstock.com/v1/login-response'

            elif self._api_type.lower()=="partner" :
                self._endpoint='http://api.thefirstock.com/v1/applogin-response'
            else :
                return {"stat": "Not_Ok","emsg": "ivalid_api_type"}                     
            signature = hmac.new(bytes(request_token, 'utf-8'),msg= bytes(self._api_key+self._api_secret , 'utf-8'),digestmod=hashlib.sha256).hexdigest()
            data2={

            "api_key":self._api_key,
            "request_token":request_token,
            "signature":signature
            }
            headers=headers = {'Content-Type': 'application/json'}
            responsedata=requests.post(self._endpoint,data=json.dumps(data2),headers=headers).json()    

            if 'access_token' in responsedata:
                self._access_token=responsedata['access_token']
                self._session_id=responsedata['session_id']

            return responsedata    
        except Exception as ex:
            #traceback.print_exc()
            return ex    

    def place_order(self,exchange,symbol,quantity,transaction_type,order_type="MKT",product="I",price="0",disc="0",is_amo="NO",ret="DAY",trigprice="",book_profit_price="",book_loss_price="",trail_price="",symbol2="",transaction_type2="",quantity2="",price2="",symbol3="",transaction_type3="",quantity3="",price3="",remarks="",ordersource=""):        

        pardata={"uid":self._user_id,
        "actid":self._account_id,
        "exch":exchange,
        "tsym":symbol,
        "qty":str(quantity),
        "prc":str(price),
        "dscqty":str(disc),
        "prd":str(product),
        "trantype":str(transaction_type),
        "prctyp":str(order_type),
        "ret":str(ret),
        "amo":is_amo
        }

        if trigprice!="":
            pardata["trgprc"]=str(trigprice)
        if ordersource!="":
                pardata["ordersource"]=str(ordersource)
        if remarks!="":
            pardata["remarks"]=str(remarks)
        if book_profit_price!="":
            pardata["bpprc"]=str(book_profit_price)
        if book_loss_price!="":
            pardata["blprc"]=str(book_loss_price)
        if trail_price!="":	
            pardata["trailprc"]=str(trail_price)
        if symbol2!="":
            pardata["tsym2"]=symbol2
        if transaction_type2!="":
            pardata["trantype2"]=str(transaction_type2)
        if quantity2!="":
            pardata["qty2"]=str(quantity2)
        if price2!="":
            pardata["prc2"]=str(price2)
        if symbol3!="":
            pardata["tsym3"]=symbol3
        if transaction_type3!="":
            pardata["trantype3"]=str(transaction_type3)
        if quantity3!="":
            pardata["qty3"]=str(quantity3)
        if price3!="":
            pardata["prc3"]=str(price3)


        data={
        "api_key":self._api_key,
        "session_id":self._session_id,
        "access_token":self._access_token,
        "data":pardata

        }


        headers=headers = {'Content-Type': 'application/json'}
        responsedata=requests.post('http://api.thefirstock.com/v1/PlaceOrder',data=json.dumps(data),headers=headers).json()
        return responsedata 

    def modify_order(self,exchange,order_id,symbol,order_type="",quantity="",price="",trigprice="",book_profit_price="",book_loss_price="",trail_price="",ret=""):
        pardata={
            "uid":self._user_id,
            #"actid":self._account_id,
            "exch":exchange,
            "tsym":symbol,
            "norenordno":order_id
            }

        if 	order_type!="":
            pardata["prctyp"]=order_type
        if quantity!="":
            pardata["qty"]=quantity
        if price!="":
            pardata["prc"]=price

        if ret!="":
            pardata["ret"]=ret
        if trigprice!="":
            pardata["trgprc"]=str(trigprice)	

        if book_profit_price!="":
            pardata["bpprc"]=str(book_profit_price)
        if book_loss_price!="":
            pardata["blprc"]=str(book_loss_price)
        if trail_price!="":	
            pardata["trailprc"]=str(trail_price)

        data={
        "api_key":self._api_key,
        "session_id":self._session_id,
        "access_token":self._access_token,
        "data":pardata

        }


        headers=headers = {'Content-Type': 'application/json'}
        responsedata=requests.post('http://api.thefirstock.com/v1/ModifyOrder',data=json.dumps(data),headers=headers).json()
        return responsedata 




    def cancel_order(self,order_id):
        pardata={
            "uid":self._user_id,
            #"actid":self._account_id,
            "norenordno":order_id
            }

        data={
        "api_key":self._api_key,
        "session_id":self._session_id,
        "access_token":self._access_token,
        "data":pardata

        }


        headers=headers = {'Content-Type': 'application/json'}
        responsedata=requests.post('http://api.thefirstock.com/v1/CancelOrder',data=json.dumps(data),headers=headers).json()
        return responsedata 


    def order_book(self,product =""):
        pardata={
            "uid":self._user_id,
            #"actid":self._account_id
            }
        if product !="":
            pardata["prd"]=product 
        data={
        "api_key":self._api_key,
        "session_id":self._session_id,
        "access_token":self._access_token,
        "data":pardata

        }

        headers=headers = {'Content-Type': 'application/json'}
        responsedata=requests.post('http://api.thefirstock.com/v1/OrderBook',data=json.dumps(data),headers=headers).json()
        return responsedata 

    def single_order_history(self,order_id):
        pardata={
            "uid":self._user_id,
            #"actid":self._account_id,
            "norenordno":order_id
            }

        data={
        "api_key":self._api_key,
        "session_id":self._session_id,
        "access_token":self._access_token,
        "data":pardata

        }


        headers=headers = {'Content-Type': 'application/json'}
        responsedata=requests.post('http://api.thefirstock.com/v1/SingleOrdHist',data=json.dumps(data),headers=headers).json()
        return responsedata 

    def trade_book(self):
        pardata={
            "uid":self._user_id,
            "actid":self._account_id
            }
        data={
        "api_key":self._api_key,
        "session_id":self._session_id,
        "access_token":self._access_token,
        "data":pardata

        }

        headers=headers = {'Content-Type': 'application/json'}
        responsedata=requests.post('http://api.thefirstock.com/v1/TradeBook',data=json.dumps(data),headers=headers).json()
        return responsedata
    
    
    def holdings(self,product="C"):
        pardata={
            "uid":self._user_id,
            "actid":self._account_id,
            "prd":product
            }
        data={
        "api_key":self._api_key,
        "session_id":self._session_id,
        "access_token":self._access_token,
        "data":pardata

        }

        headers=headers = {'Content-Type': 'application/json'}
        responsedata=requests.post('http://api.thefirstock.com/v1/Holdings',data=json.dumps(data),headers=headers).json()
        return responsedata
    
    def position_book(self):
        pardata={
            "uid":self._user_id,
            "actid":self._account_id
            }
        data={
        "api_key":self._api_key,
        "session_id":self._session_id,
        "access_token":self._access_token,
        "data":pardata

        }

        headers=headers = {'Content-Type': 'application/json'}
        responsedata=requests.post('http://api.thefirstock.com/v1/PositionBook',data=json.dumps(data),headers=headers).json()
        return responsedata
    
    def user_limits(self):
        pardata={
            "uid":self._user_id,
            "actid":self._account_id
            }
        data={
        "api_key":self._api_key,
        "session_id":self._session_id,
        "access_token":self._access_token,
        "data":pardata

        }

        headers=headers = {'Content-Type': 'application/json'}
        responsedata=requests.post('http://api.thefirstock.com/v1/Limits',data=json.dumps(data),headers=headers).json()
        return responsedata        

    def user_details(self):
        pardata={
            "uid":self._user_id
                }
        data={
        "api_key":self._api_key,
        "session_id":self._session_id,
        "access_token":self._access_token,
        "data":pardata

        }

        headers=headers = {'Content-Type': 'application/json'}
        responsedata=requests.post('http://api.thefirstock.com/v1/UserDetails',data=json.dumps(data),headers=headers).json()
        return responsedata            

    

    def logout(self):
        pardata={
            "uid":self._user_id
                }
        data={
        "api_key":self._api_key,
        "session_id":self._session_id,
        "access_token":self._access_token,
        "data":pardata

        }

        headers=headers = {'Content-Type': 'application/json'}
        responsedata=requests.post('http://api.thefirstock.com/v1/Logout',data=json.dumps(data),headers=headers).json()
        return responsedata                
    
    
    

    def product_conversion(self,exchange,symbol,quantity,product,previous_product,transaction_type,ret="DAY"):
        pardata={
                "uid":self._user_id,
                "actid":self._account_id,
                "exch":exchange,
                "tsym":symbol,
                "qty":str(quantity),
                "prd":product,
                "prevprd":previous_product,
                "trantype":transaction_type,
                "postype":ret
        }

        data={
        "api_key":self._api_key,
        "session_id":self._session_id,
        "access_token":self._access_token,
        "data":pardata

        }

        headers=headers = {'Content-Type': 'application/json'}
        responsedata=requests.post('http://api.thefirstock.com/v1/ProductConversion',data=json.dumps(data),headers=headers).json()
        return responsedata