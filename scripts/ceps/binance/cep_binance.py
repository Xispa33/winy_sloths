#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
#sys.path.append("/Users/brice/Desktop/winy_sloths/scripts")
from constants import *
from constants_binance import *
#import datetime as datetime
import traceback
from abc import ABC, abstractmethod
from crypto_exchange_platform import *
import time
from urllib.parse import urljoin, urlencode
from binance.client import Client

class CEP__Binance(CryptoExchangePlatform):
    """
    Description :
        This class represents a Binance object. It contains all basic functions
        enabling trading on Binance.
    Attributes
    ----------
    name : str
        Name of the cryptocurrency exchange platform. Here Binance
    
    Methods
    -------
    cep__client()
    cep__futures_account_trades()
    cep__spot_account_trades()
    cep__close_long_spot()
    cep__close_long_futures()
    cep__open_long_futures()
    cep__open_long_spot()
    cep__close_short()
    cep__open_short()
    cep__get_futures_account_balance()
    cep__get_asset_balance()
    cep__set_stop_loss_long
    cep__set_stop_loss_short()
    cep__clear_stop_loss()
    cep__compute_side_spot_account()
    cep__compute_side_futures_account()
    cep__compute_engaged_balance()
    """
    def __init__(self):
        super().__init__()
        self.name = BINANCE
        #self.BASIC_ENDPOINT = FUTURES_BASIC_ENDPOINT
        self.BASIC_ENDPOINT = SPOT_BASIC_ENDPOINT
        self.REQUEST_ACK_OK = 200
        self.api_key = ""
        self.api_secret_key = ""
    
    def cep__client(self, api_key, api_secret_key, account_contract_type): 
        self.called_function_name = "cep__client"
        self.api_key = api_key
        self.api_secret_key = api_secret_key
        return 0
    
    def check_response(self, response):
        json_response = json.loads(response.text)
        if (response.status_code != self.REQUEST_ACK_OK):
            print(type(json_response))
            raise ValueError('Request was not sent successfully. \
            Error code is {}'.format(json_response[CODE]))
        else:
            return json_response

    def create_request_body(self, request_parameters):
        self.called_function_name = "create_request_body"
        params = request_parameters

        sign = ''
        for key in sorted(params.keys()):
            v = params[key]
            if isinstance(params[key], bool):
                if params[key]:
                    v = 'true'
                else :
                    v = 'false'
            sign += key + '=' + v + '&'
        sign = sign[:-1]
        
        params[TIMESTAMP] = int(params[TIMESTAMP])
        query_string = urlencode(params)
        signature = hmac.new(self.api_secret_key.encode(UTF8), sign.encode(UTF8), hashlib.sha256).hexdigest()
        sign_real = {
            SIGNATURE: signature
        }
        
        body = dict(params,**sign_real)
        return (body, sign)

    def send_request_body(self, body, sign, request_type, endpoint):
        self.called_function_name = "send_request_body"
        url = self.BASIC_ENDPOINT + endpoint
        
        url = url + "?" + sign + '&signature='+body[SIGNATURE]
        urllib3.disable_warnings()
        if (request_type == GET):
            response = requests.get(url, headers={X_MBX_APIKEY: self.api_key}, verify=False)
            
        elif (request_type == POST):
            response = requests.post(url, headers={X_MBX_APIKEY: self.api_key}, verify=False)
            
        else:
            raise ValueError('The request type is incorrect')
        
        return self.check_response(response)
        

    def send_request(self, request_type, endpoint, request_parameters):
        self.called_function_name = "send_request"

        body,sign = self.create_request_body(request_parameters)
        binance_response = self.send_request_body(body, sign, request_type, endpoint)
        return binance_response
    
    ################################# FUTURES #########################################
    def futures_time(self, client):
        self.called_function_name = "futures_time"
        
        request_parameters = {}
        binance_response = self.send_request(GET, SERVER_TIME_ENDPOINT, request_parameters)
        timestamp = binance_response[SERVER_TIME]

        if (int(float(timestamp)) == 0):
            raise ValueError('Timestamp was equal to 0')
        else:
            return int(float(timestamp))
    
    def futures_position_information(self, symbol):
        self.called_function_name = "futures_position_information"
        request_parameters = {SYMBOL:symbol, \
                            TIMESTAMP: str(int(time.time()*1000))}
        query_response = self.send_request(GET, FUTURES_POSITION_INFORMATION, request_parameters)
        return query_response

    def cep__futures_account_trades(self, symbol):
        self.called_function_name = "cep__futures_account_trades"
        return self.futures_position_information(symbol=symbol)

    def get_futures_account_balance(self):
        self.called_function_name = "futures_position_information"
        request_parameters = {TIMESTAMP: str(int(time.time()*1000))}
        binance_response = self.send_request(GET, FUTURES_ACCOUNT_BALANCE, request_parameters)
        for dic in binance_response:
            if dic[ASSET] == USDT:
                ret = dic
        return ret 

    def cep__get_futures_account_balance(self):
        self.called_function_name = "cep__get_futures_account_balance"
        return self.get_futures_account_balance()

    def compute_side_futures_account(self, account, cep_response):
        self.called_function_name="cep__compute_side_futures_account"
        if (isinstance(cep_response, int)):
            #print("Binance return was crap ! \n")
            return account.side
        else:
            binance_response = cep_response
            
            # Store needed information for FUTURES account
            account.account_mode = ONE_WAY
            account.markPrice = round(float(binance_response[0][MARK_PRICE]), 0)
            account.entryPrice = round(float(binance_response[0][ENTRY_PRICE]), 0)
            account.leverage = binance_response[0][LEVERAGE]
            account.positionAmt = float(binance_response[0][POSITION_AMT])
            account.markPrice = round(float(binance_response[0][MARK_PRICE]), 0)
            notional = float(binance_response[0][NOTIONAL])
            account_balance = self.CEP__BaseFunction(functools.partial( \
                            self.get_futures_account_balance),retry=5, retry_period=0.5)
            if (account_balance != 1):
                account.balance = float(account_balance[BALANCE])
                account.engaged_balance = float(notional/account.balance)
                if (notional == float(0)):
                    return OUT
                elif (notional < 0):
                    return SHORT
                else: 
                    return LONG
            else:
                return account.side
    
    def cep__compute_side_futures_account(self, account, cep_response):
        self.called_function_name="cep__compute_side_futures_account"
        return self.compute_side_futures_account(account, cep_response)
    
    def futures_change_position_mode(self, dualSidePosition=FALSE):
        self.called_function_name = "futures_change_position_mode"
        request_parameters = {DUAL_SIDE_POSITION:dualSidePosition, TIMESTAMP: str(int(time.time()*1000))}
        binance_response = self.send_request(POST, FUTURES_CHANGE_POSITION_MODE, request_parameters)
        #TODO
        #Checker la valeur de retour

    def futures_change_leverage(self, symbol, leverage):
        self.called_function_name = "futures_change_leverage"
        request_parameters = {symbol:symbol, LEVERAGE:int(leverage), TIMESTAMP: str(int(time.time()*1000))}
        binance_response = self.send_request(POST, FUTURES_CHANGE_LEVERAGE, request_parameters)
        #TODO
        #Checker la valeur de retour

    def futures_create_order(self, symbol, side, positionSide, _type, quantity):
        self.called_function_name = "futures_create_order"
        request_parameters = {symbol:symbol, LEVERAGE:int(leverage), \
                            SIDE:side, POSITION_SIDE:positionSide, \
                            TYPE:_type, QUANTITY:quantity, \
                            TIMESTAMP: str(int(time.time()*1000))}
        binance_response = self.send_request(POST, FUTURES_CHANGE_LEVERAGE, request_parameters)
        #TODO
        #Checker la valeur de retour

    def open_long_futures(self, symbol, leverage, \
                        engaged_balance, entryPrice):
        self.called_function_name="open_long_futures"

        precision = self.ALL_SYMBOLS_DICT[symbol][PRECISION_IDX]
        ret = self.cep__futures_position_information(symbol=symbol)
        if (len(ret) == 1):
            self.futures_change_position_mode(dualSidePosition=TRUE)
        
        self.futures_change_leverage(symbol, leverage)
        
        #Need slave available balance
        bin_ret = self.cep__get_futures_account_balance()
        
        for dic in bin_ret:
            if dic[ASSET] == USDT:
                ret = dic

        balance=ret[WITHDRAW_AVAILABLE]

        quantity=round(((float(balance)*engaged_balance/entryPrice) - \
                                                    (5*10**(-precision-1))),precision)

        if (quantity < (1*10**(-precision))):
            quantity = 1*10**(-precision)
        
        self.futures_create_order(symbol=symbol, side=BUY, positionSide=LONG, \
                                    _type=MARKET, quantity=quantity)
        
        return 0

    def cep__open_long_futures(self, symbol, leverage, \
                               engaged_balance, entryPrice):
        self.called_function_name="cep__open_long_futures"
        return self.open_long_futures(symbol, leverage, \
                               engaged_balance, entryPrice)

    def open_short(self, symbol, leverage, \
                    engaged_balance, entryPrice):
        self.called_function_name="open_short"

        precision = self.ALL_SYMBOLS_DICT[symbol][PRECISION_IDX]
        ret = self.cep__futures_position_information(symbol=symbol)
        if (len(ret) == 1):
            self.futures_change_position_mode(dualSidePosition=TRUE)
        
        self.futures_change_leverage(symbol, leverage)
        
        #Need slave available balance
        bin_ret = self.cep__get_futures_account_balance()
        
        for dic in bin_ret:
            if dic[ASSET] == USDT:
                ret = dic

        balance=ret[WITHDRAW_AVAILABLE]
        
        quantity = round(((float(balance)*abs(engaged_balance)/entryPrice) - \
                                                    (5*10**(-precision - 1))), precision)

        if (quantity < (1*10**(-precision))):
            quantity = 1*10**(-precision)
        
        self.futures_create_order(symbol=symbol, side=BUY, positionSide=SHORT, \
                                    _type=MARKET, quantity=quantity)

        return 0

    def cep__open_short(self, client, symbol, leverage, \
                        engaged_balance, entryPrice):
        self.called_function_name="cep__open_short"
        return self.open_short(client, symbol, leverage, \
                               engaged_balance, entryPrice)
    
    def close_long_futures(self, symbol):
        self.called_function_name="close_long_futures"
        last_trade = []
        precision = self.ALL_SYMBOLS_DICT[symbol][PRECISION_IDX]
        found = False
        ret = {}

        if last_trade == []:
            last_trade = self.cep__futures_account_trades(symbol)
        else:
            pass
        
        for dic in last_trade:
            if dic[POSITION_SIDE] == LONG:
                ret = dic
                found = True

        if (found):
            position_amt = round(float(ret[POSITION_AMT]), precision)
        else:
            position_amt = 0.0

        if (position_amt != 0.0):
            self.futures_create_order(symbol=symbol, side=SELL, positionSide=LONG, \
                                    _type=MARKET, quantity=position_amt)
        else:
            pass
        
        return 0

    def cep__close_long_futures(self, client, symbol):
        self.called_function_name="cep__close_long_futures"
        return self.close_long_futures(symbol)
    
    def close_short(self, symbol):
        self.called_function_name="close_short"
        last_trade = []
        precision = self.ALL_SYMBOLS_DICT[symbol][PRECISION_IDX]

        if last_trade == []:
            last_trade = self.cep__futures_account_trades(symbol)
        else:
            pass
            
        for dic in last_trade:
            if dic[POSITION_SIDE] == SHORT:
                ret = dic
        
        quantity = round(abs(float(ret[POSITION_AMT])), precision)

        if (quantity != 0.0):
            self.futures_create_order(symbol=symbol, side=BUY, positionSide=SHORT, \
                                    _type=MARKET, quantity=quantity)
        else:
            pass
            
        return 0

    def cep__close_short(self, symbol):
        self.called_function_name="cep__close_short"
        return self.close_short(symbol)
    
    ################################# FUTURES #########################################

    #TODO
    def get_all_orders(self, symbol, limit):
        self.called_function_name="get_all_orders"
        request_parameters = {SYMBOL:symbol, \
                              LIMIT: str(limit)}
        binance_response = self.send_request(GET, SPOT_GET_ALL_ORDERS, request_parameters)
        return binance_response
    
    def cep__get_all_orders(self, symbol, limit):
        self.called_function_name="cep__get_all_orders"
        return self.get_all_orders(symbol, limit)
    
    def cep__spot_account_trades(self, symbol, limit='1'):
        self.called_function_name="cep__spot_account_trades"
        return (self.get_all_orders(symbol, limit))
    ####################################################
    #COMPUTE SIDE SPOT
    #####################################################
    def get_avg_price(self, symbol):
        self.called_function_name="get_avg_price"
        request_parameters = {SYMBOL:symbol}
        binance_response = self.send_request(GET, SPOT_GET_AVG_PRICE, request_parameters)
        return binance_response
    
    def cep__get_avg_price(self, symbol):
        self.called_function_name="cep__get_avg_price"
        return self.get_avg_price(symbol)
    
    def get_symbol_price_ticker(self, symbol):
        self.called_function_name="get_symbol_price_ticker"
        request_parameters = {SYMBOL:symbol}
        binance_response = self.send_request(GET, SPOT_SYMBOL_PRICE_TICKER, request_parameters)
        return binance_response

    def cep__get_symbol_price_ticker(self, symbol):
        self.called_function_name="cep__get_symbol_price_ticker"
        return self.get_symbol_price_ticker(symbol)
    
    def get_order_book(self, symbol):
        self.called_function_name="get_order_book"
        request_parameters = {SYMBOL:symbol}
        binance_response = self.send_request(GET, SPOT_SYMBOL_ORDER_BOOK, request_parameters)
        return binance_response

    def cep__get_order_book(self, symbol):
        self.called_function_name="cep__get_order_book"
        return self.get_order_book(symbol)

    def get_aggregate_trades(self, symbol, start_time=0, end_time=0):
        self.called_function_name="get_aggregate_trades"
        if (start_time != 0 and end_time != 0):
            request_parameters = {SYMBOL:symbol, START_TIME:start_time, END_TIME:end_time}
        else:
            request_parameters = {SYMBOL:symbol}
        binance_response = self.send_request(GET, SPOT_AGGREGATES_TRADES, request_parameters)
        return binance_response

    def cep__get_aggregate_trades(self, symbol, start_time=0, end_time=0):
        self.called_function_name="cep__get_aggregate_trades"
        if (start_time != 0 and end_time != 0):
            return self.get_aggregate_trades(symbol, start_time, end_time)
        else:
            return self.get_aggregate_trades(symbol)

    def get_asset_balance(self, asset):
        self.called_function_name="get_asset_balance"
        request_parameters = {ASSET:asset}
        binance_response = self.send_request(GET, SPOT_GET_ASSET_BALANCE, request_parameters)
        return binance_response

    def cep__get_asset_balance(self, asset):
        self.called_function_name="cep__get_asset_balance"
        return self.get_asset_balance(asset)
     
    def spot_create_order(self, symbol, side, _type, quoteOrderQty):
        self.called_function_name="spot_create_order"

        request_parameters = {symbol:symbol, \
                            SIDE:side, \
                            TYPE:_type, QUOTE_ORDER_QTY:quoteOrderQty, \
                            TIMESTAMP: str(int(time.time()*1000))}
        binance_response = self.send_request(POST, SPOT_CREATE_ORDER, request_parameters)
        #TODO
        #Checker la valeur de retour

        
    def cep__close_long_spot(self, symbol):
        self.called_function_name="cep__close_long_spot"
        curr_asset = self.ALL_SYMBOLS_DICT[symbol][ASSET_IDX]
        price = self.get_avg_price(symbol)[PRICE]
        asset = round(float(self.get_asset_balance( \
                        asset=curr_asset)[FREE])*float(price) - 1,1)
        self.spot_create_order(symbol, SELL, MARKET, abs(asset))
        return 0
    """
    def cep__close_long_futures(self, client, symbol):
        self.called_function_name="cep__close_long_futures"
        last_trade = []
        precision = self.ALL_SYMBOLS_DICT[symbol][PRECISION_IDX]
        found = False
        ret = {}

        if last_trade == []:
            last_trade = self.CEP__FUTURES_ACCOUNT_TRADES(client, symbol)
        else:
            pass
        
        for dic in last_trade:
            if dic[POSITION_SIDE] == LONG:
                ret = dic
                found = True

        if (found):
            position_amt = round(float(ret[POSITION_AMT]), precision)
        else:
            position_amt = 0.0

        if (position_amt != 0.0):
            client.futures_create_order(symbol=symbol, positionside=LONG, \
                                        side=SELL, type=MARKET, \
                                        quantity=position_amt, \
                                        timestamp=client.futures_time())
        else:
            pass
        
        return 0
    """
    
    def cep__open_long_spot(self, symbol):
        self.called_function_name="cep__open_long_spot"
        usdt_asset = self.get_asset_balance(asset=USDT)[FREE]
        asset_round=round(float(usdt_asset)-0.05,1)
        self.spot_create_order(symbol, BUY, MARKET, abs(asset_round))
        return 0

    def cep__compute_side_spot_account(self, account, cep_response):
        self.called_function_name="cep__compute_side_spot_account"

        if (isinstance(cep_response, int)):
            #print("Binance return was crap ! \n")
            return account.side
        else:
            if (len(cep_response) == 0):
                return account.side
            else:
                #asset_dict = self.CEP__GET_ASSET_BALANCE( \
                #                self.CEP__CLIENT(account.api_key._api_key, \
                #                account.api_key._api_secret_key, None))
                asset_dict = self.get_asset_balance(asset=USDT)
                if (not isinstance(asset_dict, dict)):
                    return account.side
                else:
                    binance_response = cep_response[0]
                    asset_usdt=float(asset_dict[FREE])

                    if binance_response[SIDE] == BUY and \
                       round(float(asset_usdt),1) < MIN_WALLET_IN_USDT:
                        return LONG
                    elif binance_response[SIDE] == SELL and \
                         round(float(asset_usdt),1) > MIN_WALLET_IN_USDT:
                        return OUT
                    else:
                        return account.side

    """
    def cep__open_long_futures(self, client, symbol, leverage, \
                                engaged_balance, entryPrice):
        self.called_function_name="cep__open_long_futures"

        precision = self.ALL_SYMBOLS_DICT[symbol][PRECISION_IDX]
        ret = client.futures_position_information(symbol=symbol, \
                                                  timestamp=client.futures_time())
        if (len(ret) == 1):
            client.futures_change_position_mode(dualSidePosition=TRUE, \
                                                timestamp=client.futures_time())
        
        client.futures_change_leverage(symbol=symbol, leverage=leverage, \
                                       timestamp=client.futures_time())
        
        bin_ret=client.futures_account_balance(timestamp=client.futures_time())

        for dic in bin_ret:
            if dic[ASSET] == USDT:
                ret = dic

        balance=ret[WITHDRAW_AVAILABLE]

        quantity=round(((float(balance)*engaged_balance/entryPrice) - \
                                                    (5*10**(-precision-1))),precision)

        if (quantity < (1*10**(-precision))):
            quantity = 1*10**(-precision)
        
        client.futures_create_order(symbol=symbol, side=BUY, positionSide=LONG, \
                                    type=MARKET, quantity=quantity, \
                                    timestamp=client.futures_time())
        
        return 0
    """
    """
    def cep__close_short(self, client, symbol):
        self.called_function_name="cep__close_short"
        last_trade = []
        precision = self.ALL_SYMBOLS_DICT[symbol][PRECISION_IDX]

        if last_trade == []:
            last_trade = self.CEP__FUTURES_ACCOUNT_TRADES(client, symbol)
        else:
            pass
            
        for dic in last_trade:
            if dic[POSITION_SIDE] == SHORT:
                ret = dic
        
        quantity = round(abs(float(ret[POSITION_AMT])), precision)

        if (quantity != 0.0):
            client.futures_create_order(symbol=symbol, positionside=SHORT, \
                                        side=BUY, type=MARKET, quantity=quantity, \
                                        timestamp=client.futures_time())
        else:
            pass
            
        return 0
    """
    """
    def cep__open_short(self, client, symbol, leverage, engaged_balance, \
                                            entryPrice):
        self.called_function_name="cep__open_short"
        precision = self.ALL_SYMBOLS_DICT[symbol][PRECISION_IDX]

        ret = client.futures_position_information(symbol=symbol, \
                                                  timestamp=client.futures_time())
        if (len(ret) == 1):
            client.futures_change_position_mode(dualSidePosition=TRUE, \
                                                timestamp=client.futures_time())
        
        client.futures_change_leverage(symbol=symbol, leverage=leverage, \
                                       timestamp=client.futures_time())

        bin_ret=client.futures_account_balance(timestamp=client.futures_time())
        
        for dic in bin_ret:
            if dic[ASSET] == USDT:
                ret = dic
        
        balance=ret[WITHDRAW_AVAILABLE]

        quantity = round(((float(balance)*abs(engaged_balance)/entryPrice) - \
                                                    (5*10**(-precision - 1))), precision)

        if (quantity < (1*10**(-precision))):
            quantity = 1*10**(-precision)
        
        client.futures_create_order(symbol=symbol, side=SELL, positionSide=SHORT, \
                                    type=MARKET, quantity=quantity, \
                                    timestamp=client.futures_time())
            
        return 0

    """
    """
    def cep__get_asset_balance(self, client):
        self.called_function_name="cep__get_asset_balance"
        return client.get_asset_balance(asset=USDT)
    """
    """
    def cep__set_stop_loss_long(self, client, symbol, engaged_balance, \
                                entryPrice, mode, risk=RISK):
        self.called_function_name="cep__set_stop_loss_long"
        ret = 0
        price=(1 - (risk/engaged_balance))*entryPrice
        if (mode == HEDGE):
            client.futures_create_order(symbol=symbol, side=SELL, \
                                        positionSide=LONG, closeposition=TRUE, \
                                        stopPrice=round(float(price),0), \
                                        type=STOP_MARKET, \
                                        timestamp=client.futures_time())
        elif (mode == ONE_WAY):
            client.futures_create_order(symbol=symbol, side=SELL, \
                                        closeposition=TRUE, \
                                        stopPrice=round(float(price),0), \
                                        type=STOP_MARKET, \
                                        timestamp=client.futures_time())
        else:
            ret = 1
        
        return ret

    def cep__set_stop_loss_short(self, client, symbol, engaged_balance, \
                                entryPrice, mode, risk=RISK):
        self.called_function_name="cep__set_stop_loss_short"
        ret = 0
        price=(1 + (RISK/engaged_balance))*entryPrice
        if (mode == HEDGE):
            client.futures_create_order(symbol=symbol, side=BUY, positionSide=SHORT, \
                                        closeposition=TRUE, stopPrice=round(float(price),0), \
                                        type=STOP_MARKET, \
                                        timestamp=client.futures_time())
        elif (mode == ONE_WAY):
            client.futures_create_order(symbol=symbol, side=BUY, closeposition=TRUE, \
                                        stopPrice=round(float(price),0), type=STOP_MARKET, \
                                        timestamp=client.futures_time())
        else:
            ret = 1
        
        return ret
    
    def cep__clear_stop_loss(self, client, symbol):
        self.called_function_name="cep__clear_stop_loss"
        return client.futures_cancel_all_open_orders(symbol=symbol, countdownTime=0, \
                                                     timestamp=client.futures_time())
    
    """
    """
    def cep__compute_side_spot_account(self, account, cep_response):
        self.called_function_name="cep__compute_side_spot_account"

        if (isinstance(cep_response, int)):
            #print("Binance return was crap ! \n")
            return account.side
        else:
            if (len(cep_response) == 0):
                return account.side
            else:
                asset_dict = self.CEP__GET_ASSET_BALANCE( \
                                self.CEP__CLIENT(account.api_key._api_key, \
                                account.api_key._api_secret_key, None))
            
                if (not isinstance(asset_dict, dict)):
                    return account.side
                else:
                    binance_response = cep_response[0]
                    asset_usdt=float(asset_dict[FREE])

                    if binance_response[SIDE] == BUY and \
                       round(float(asset_usdt),1) < MIN_WALLET_IN_USDT:
                        return LONG
                    elif binance_response[SIDE] == SELL and \
                         round(float(asset_usdt),1) > MIN_WALLET_IN_USDT:
                        return OUT
                    else:
                        return account.side
    """
    """
    def compute_engaged_balance(self, account, cep_response):
        self.called_function_name="compute_engaged_balance"
        if (account.balance != 0):
            account.engaged_balance = (account.positionAmt * account.entryPrice/account.balance)
            return 0
        else:
            print("WS should be restarting.\n{} \n {}. \
            ".format(cep_response, \
            account.exchange_platform_obj.CEP__GET_FUTURES_ACCOUNT_BALANCE( \
                                account.api_key.exchange_platform_obj.CEP__CLIENT( \
                                account.api_key._api_key, account.api_key._api_secret_key, None))))
            return 1
    """
    def cep__get_symbol_price(self, client, symbol):
        self.called_function_name="cep__get_symbol_price"
    
        info = client.get_symbol_ticker(symbol=symbol)
        return info[PRICE]

    def get_exchange_info(self):
        self.called_function_name="get_exchange_info"
        #request_parameters = {TIMESTAMP: str(int(time.time()*1000))}
        #binance_response = self.send_request(GET, SPOT_GET_EXCHANGE_INFO, request_parameters)
        binance_response = requests.get(self.BASIC_ENDPOINT + SPOT_GET_EXCHANGE_INFO)

        return binance_response.json()

    def cep__get_exchange_info(self):
        self.called_function_name="cep__get_exchange_info"
        return self.get_exchange_info()