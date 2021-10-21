#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.getenv('SCRIPT_DIR'))
from constants import *
from constants_binance import *
import traceback
from abc import ABC, abstractmethod
from crypto_exchange_platform import *
import time
from urllib.parse import urljoin, urlencode

class CEP__Binance(CryptoExchangePlatform):
    """
    Description :
        This class represents a Binance object. It contains all basic functions
        enabling trading on Binance.
    Attributes
    ----------

    """
    def __init__(self, api_key=None, api_secret_key=None, mode=DEBUG):
        super().__init__(mode=mode)
        self.name = BINANCE
        self.SPOT_TESTNET_ENDPOINT = 'https://testnet.binance.vision'
        self.SPOT_REAL_ENDPOINT = 'https://api.binance.com'
        self.FUTURES_TESTNET_ENDPOINT = 'https://testnet.binancefuture.com'
        self.FUTURES_REAL_ENDPOINT = 'https://fapi.binance.com'
        self.CEP__Init_Dicts()
        self.REQUEST_ACK_OK = 200
        self.api_key = ""
        self.api_secret_key = ""
    
    ################################# BASE REQUESTS #########################################
    def check_response(self, response):
        json_response = json.loads(response.text)
        if (response.status_code != self.REQUEST_ACK_OK):
            print(type(json_response))
            raise ValueError('Request was not sent successfully.')
            #Error code is {}'.format(json_response[CODE]))
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
        try:
            params[TIMESTAMP] = int(params[TIMESTAMP])
        except KeyError as key_error:
            pass
        query_string = urlencode(params)
        signature = hmac.new(self.api_secret_key.encode(UTF8), sign.encode(UTF8), hashlib.sha256).hexdigest()
        sign_real = {
            SIGNATURE: signature
        }
        
        body = dict(params,**sign_real)
        return (body, sign)

    def send_request_body(self, body, sign, request_type, endpoint):
        self.called_function_name = "send_request_body"

        url = self.BASIC_ENDPOINT + endpoint[0] + "?" + sign
        
        if (endpoint[1] == SECURITY_TYPE_TRADE or endpoint[1] == SECURITY_TYPE_MARGIN or endpoint[1] == SECURITY_TYPE_USER_DATA):
            url = url + '&signature='+body[SIGNATURE]
        
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
    ################################# END BASE REQUESTS #########################################

    def cep__client(self, api_key, api_secret_key, account_contract_type): 
        self.called_function_name = "cep__client"
        self.api_key = api_key
        self.api_secret_key = api_secret_key
        self.BASIC_ENDPOINT = self.BASIC_ENDPOINT[account_contract_type]
        return 0

    ################################# FUTURES #########################################
    
    def cep__futures_time(self):
        self.called_function_name = "cep__futures_time"
        
        request_parameters = {TIMESTAMP: str(int(time.time()*1000))}
        binance_response = self.send_request(GET, SERVER_TIME_ENDPOINT, request_parameters)
        timestamp = binance_response[SERVER_TIME]

        if (int(float(timestamp)) == 0):
            raise ValueError('Timestamp was equal to 0')
        else:
            return int(float(timestamp))
    
    def cep__futures_account_trades(self, symbol):
        self.called_function_name = "cep__futures_account_trades"
        request_parameters = {SYMBOL:symbol, \
                              TIMESTAMP: str(int(time.time()*1000))}
        query_response = self.send_request(GET, FUTURES_POSITION_INFORMATION, request_parameters)
        return query_response
    
    def cep__get_futures_account_balance(self, asset):
        self.called_function_name = "cep__get_futures_account_balance"
        request_parameters = {TIMESTAMP: str(int(time.time()*1000))}
        binance_response = self.send_request(GET, FUTURES_ACCOUNT_BALANCE, request_parameters)
        for dic in binance_response:
            if dic[ASSET] == asset:
                ret = dic
        return ret 
    
    def cep__compute_side_futures_account(self, account, cep_response):
        self.called_function_name="cep__compute_side_futures_account"
        if (isinstance(cep_response, int) or (len(cep_response) == 0)):
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
                            self.cep__get_futures_account_balance, USDT),retry=5, retry_period=0.5)
            if (account_balance != 1):
                account.balance = float(account_balance[BALANCE])
                account.engaged_balance = float(notional/account.balance)
                
                for idx, elt in enumerate(binance_response):
                    if (float(elt[ENTRY_PRICE])!=0):
                        if (float(elt[NOTIONAL]) > 0):
                            return LONG
                        elif (float(elt[NOTIONAL]) < 0):
                            return SHORT
                        else:
                            pass
                    if (idx == len(binance_response) - 1) and (float(elt[ENTRY_PRICE])==0):
                        return OUT
                
                return account.side
    
    def cep__futures_change_position_mode(self, dualSidePosition=FALSE):
        self.called_function_name = "cep__futures_change_position_mode"
        request_parameters = {DUAL_SIDE_POSITION:dualSidePosition, TIMESTAMP: str(int(time.time()*1000))}
        binance_response = self.send_request(POST, FUTURES_CHANGE_POSITION_MODE, request_parameters)
        return binance_response
    
    def cep__get_futures_open_orders(self, symbol):
        self.called_function_name = "cep__get_futures_open_orders"
        request_parameters = {SYMBOL:symbol, TIMESTAMP: str(int(time.time()*1000))}
        binance_response = self.send_request(GET, FUTURES_OPEN_ORDERS, request_parameters)
        return binance_response
    
    def cep__futures_position_mode(self):
        self.called_function_name = "cep__futures_position_mode"
        request_parameters = {TIMESTAMP: str(int(time.time()*1000))}
        binance_response = self.send_request(GET, FUTURES_POSITION_MODE, request_parameters)
        return binance_response
    
    def cep__futures_change_leverage(self, symbol, leverage):
        self.called_function_name = "cep__futures_change_leverage"
        request_parameters = {SYMBOL:symbol, LEVERAGE:str(leverage), TIMESTAMP: str(int(time.time()*1000))}
        binance_response = self.send_request(POST, FUTURES_CHANGE_LEVERAGE, request_parameters)
        return binance_response
    
    def cep__get_symbol_price_futures(self, symbol):
        self.called_function_name="cep__get_symbol_price_futures"
        
        request_parameters = {SYMBOL:symbol}
        binance_response = self.send_request(GET, FUTURES_TICKER_PRICE, request_parameters)
        return binance_response

    def futures_create_order(self, symbol, side, positionSide, _type, quantity):
        self.called_function_name = "futures_create_order"
        request_parameters = {SYMBOL:symbol, \
                            SIDE:side, POSITION_SIDE:positionSide, \
                            TYPE:_type, QUANTITY:str(quantity), \
                            'newOrderRespType':'RESULT', \
                            TIMESTAMP: str(int(time.time()*1000))}
        binance_response = self.send_request(POST, FUTURES_CREATE_ORDER, request_parameters)
        return binance_response
    
    def cep__open_long_futures(self, symbol, leverage, \
                        engaged_balance, entryPrice, pct):
        self.called_function_name="cep__open_long_futures"

        precision = self.ALL_SYMBOLS_DICT[symbol][PRECISION_IDX]
        ret = self.cep__futures_account_trades(symbol)
        if (len(ret) == 1):
            self.futures_change_position_mode(dualSidePosition=TRUE)
        
        if (leverage >= BINANCE_DEFAULT_LEVERAGE):
            leverage = BINANCE_MAX_LEVERAGE = 18
            #self.cep__futures_change_leverage(symbol, leverage)
        
        #Need slave available balance
        bin_ret = self.cep__get_futures_account_balance(asset=USDT)
        
        if (isinstance(bin_ret, list)):
            for dic in bin_ret:
                if dic[ASSET] == USDT:
                    ret = dic
        elif (isinstance(bin_ret, dict)):
            ret = bin_ret
        else:
            raise ValueError("bin_ret variable is bad.\nType is:{}\nValue is:{}\n".format( \
                type(bin_ret), bin_ret))
        #balance=ret[WITHDRAW_AVAILABLE]
        balance = ret[MAX_WITHDRAW_AMOUNT]

        quantity=round(((float(balance)*engaged_balance/float(entryPrice)) - \
                                                    (5*10**(-precision-1))),precision)
        
        if (pct > 1):
            raise ValueError("Parameter pct has to be less than 1")
        
        quantity = quantity*pct
        
        if (quantity < (1*10**(-precision))):
            quantity = 1*10**(-precision)
        
        binance_response = self.futures_create_order(symbol=symbol, \
                                        side=BUY, positionSide=LONG, \
                                        _type=MARKET, quantity=quantity)
        
        return binance_response

    def cep__open_short(self, symbol, leverage, \
                    engaged_balance, entryPrice, pct):
        self.called_function_name="cep__open_short"

        precision = self.ALL_SYMBOLS_DICT[symbol][PRECISION_IDX]
        ret = self.cep__futures_account_trades(symbol)
        if (len(ret) == 1):
            self.futures_change_position_mode(dualSidePosition=TRUE)
        
        if (abs(leverage) >= BINANCE_DEFAULT_LEVERAGE):
            leverage = BINANCE_MAX_LEVERAGE
            #self.cep__futures_change_leverage(symbol, leverage)
        
        #Need slave available balance
        bin_ret = self.cep__get_futures_account_balance(asset=USDT)
        
        if (isinstance(bin_ret, list)):
            for dic in bin_ret:
                if dic[ASSET] == USDT:
                    ret = dic
        elif (isinstance(bin_ret, dict)):
            ret = bin_ret
        else:
            raise ValueError("bin_ret variable is bad.\nType is:{}\nValue is:{}\n".format( \
                type(bin_ret), bin_ret))
        #balance=ret[WITHDRAW_AVAILABLE]
        balance = ret[MAX_WITHDRAW_AMOUNT]
        
        quantity = round(((float(balance)*abs(engaged_balance)/float(entryPrice)) - \
                                                    (5*10**(-precision - 1))), precision)
        if (pct > 1):
            raise ValueError("Parameter pct has to be less than 1")
        quantity = quantity*pct

        if (quantity < (1*10**(-precision))):
            quantity = 1*10**(-precision)
        
        binance_return = self.futures_create_order(symbol=symbol, \
                                    side=SELL, positionSide=SHORT, \
                                    _type=MARKET, quantity=quantity)

        return binance_return
    
    def cep__close_long_futures(self, symbol):
        self.called_function_name="cep__close_long_futures"
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
            binance_return = self.futures_create_order(symbol=symbol, side=SELL, positionSide=LONG, \
                                    _type=MARKET, quantity=position_amt)
            return binance_return
        else:
            return 0
    
    def cep__close_short(self, symbol):
        self.called_function_name="cep__close_short"
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
            binance_return = self.futures_create_order(symbol=symbol, \
                                    side=BUY, positionSide=SHORT, \
                                    _type=MARKET, quantity=quantity)
            return binance_return
        else:
            return 0

    ################################# END FUTURES #########################################

    ################################# SPOT ################################################
    def cep__spot_account_trades(self, symbol, limit='1'):
        self.called_function_name="cep__spot_account_trades"
        request_parameters = {SYMBOL:symbol, \
                              LIMIT: str(limit), \
                              TIMESTAMP: str(int(time.time()*1000))}
        binance_response = self.send_request(GET, SPOT_GET_ALL_ORDERS, request_parameters)
        return binance_response

    def cep__get_symbol_price(self, symbol):
        self.called_function_name="cep__get_avg_price"
        request_parameters = {SYMBOL:symbol}
        binance_response = self.send_request(GET, SPOT_GET_AVG_PRICE, request_parameters)
        return binance_response
    
    def cep__get_symbol_price_ticker(self, symbol):
        self.called_function_name="cep__get_symbol_price_ticker"
        request_parameters = {SYMBOL:symbol}
        binance_response = self.send_request(GET, SPOT_SYMBOL_PRICE_TICKER, request_parameters)
        return binance_response
    
    def cep__get_order_book(self, symbol):
        self.called_function_name="cep__get_order_book"
        request_parameters = {SYMBOL:symbol}
        binance_response = self.send_request(GET, SPOT_SYMBOL_ORDER_BOOK, request_parameters)
        return binance_response

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

    def cep__get_asset_balance(self, asset):
        self.called_function_name="cep__get_asset_balance"
        request_parameters = {TIMESTAMP: str(int(time.time()*1000))}
        binance_response = self.send_request(GET, SPOT_GET_ASSET_BALANCE, request_parameters)
        for asset_elt in binance_response[BALANCES]:
            if (asset_elt[ASSET] == asset):
                return asset_elt
        return 1
     
    def spot_create_order(self, symbol, side, _type, qty):
        self.called_function_name="spot_create_order"
        request_parameters = {SYMBOL:symbol, \
                              SIDE:side, \
                              TYPE:_type, \
                              TIMESTAMP: str(int(time.time()*1000))}
        if (side == BUY):
            request_parameters[QUOTE_ORDER_QTY] = str(qty)
        else:
            request_parameters[QUANTITY] = str(qty)
        
        binance_response = self.send_request(POST, SPOT_CREATE_ORDER, request_parameters)
        return binance_response
        
    def cep__close_long_spot(self, symbol, compute_avg_price, pct):
        self.called_function_name="cep__close_long_spot"
        curr_asset = self.ALL_SYMBOLS_DICT[symbol][ASSET_IDX]
        binance_return = {'status':'EXPIRED'}
        prices = []
        qty = []
        if (pct > 1):
            raise ValueError("Parameter pct has to be less than 1")

        asset_qty = float(self.cep__get_asset_balance(curr_asset)[FREE])  
        while (binance_return['status'] != 'FILLED'):
            asset_round = float(self.cep__get_asset_balance(curr_asset)[FREE])*pct
            binance_return = self.spot_create_order(symbol, SELL, MARKET, asset_round)
            if (compute_avg_price == True):
                for elt in binance_return['fills']:
                    prices.append(elt['price'])
                    qty.append(float(elt['qty']))
            asset_qty = float(self.cep__get_asset_balance(curr_asset)[FREE])
        
        if (compute_avg_price == True):
            return (prices, qty)
        else:
            return 0

    def cep__open_long_spot(self, symbol, compute_avg_price, pct):
        self.called_function_name="cep__open_long_spot"
        curr_asset = USDT
        binance_return = {'status':'EXPIRED'}
        prices = []
        qty = []
        if (pct > 1):
            raise ValueError("Parameter pct has to be less than 1")

        usdt_asset = float(self.cep__get_asset_balance(curr_asset)[FREE])
        while (binance_return['status'] != 'FILLED'):
            asset_round=round(float(float(usdt_asset))-0.0005,3)*pct
            binance_return = self.spot_create_order(symbol, BUY, MARKET, asset_round)
            if (compute_avg_price == True):
                for elt in binance_return['fills']:
                    prices.append(elt['price'])
                    qty.append(float(elt['qty']))

        if (compute_avg_price == True):
            return (prices, qty)
        else:
            return 0

    def cep__compute_side_spot_account(self, account, cep_response):
        self.called_function_name="cep__compute_side_spot_account"

        if (isinstance(cep_response, int)):
            return account.side
        else:
            if (len(cep_response) == 0):
                return account.side
            else:
                asset_dict = self.cep__get_asset_balance(asset=USDT)
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

    def cep__get_exchange_info(self):
        self.called_function_name="cep__get_exchange_info"
        
        binance_response = requests.get(self.BASIC_ENDPOINT + SPOT_GET_EXCHANGE_INFO[0])
        return binance_response.json()