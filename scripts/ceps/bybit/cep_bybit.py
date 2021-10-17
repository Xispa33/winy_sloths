#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.getenv('SCRIPT_DIR'))
from constants import *
from datetime import *
import traceback
from abc import ABC, abstractmethod
from crypto_exchange_platform import *
import time
from constants_bybit import *

class CEP__Bybit(CryptoExchangePlatform):
    def __init__(self):
        super().__init__()
        self.name = BYBIT
        self.SPOT_TESTNET_ENDPOINT = 'https://api-testnet.bybit.com'
        self.SPOT_REAL_ENDPOINT = 'https://api.bybit.com'
        self.FUTURES_TESTNET_ENDPOINT = 'https://api-testnet.bybit.com'
        self.FUTURES_REAL_ENDPOINT = 'https://api.bybit.com'
        self.REQUEST_ACK_OK = 0
        self.CEP__Init_Dicts()
        self.api_key = ""
        self.api_secret_key = ""

    def check_response(self, response):
        json_response = json.loads(response.text)
        if (json_response[RET_CODE] != self.REQUEST_ACK_OK):
            raise ValueError('Request was not sent successfully. \
            Error code is {}'.format(json_response[RET_CODE]))
        else:
            return json_response

    def create_request_body(self, request_parameters):
        self.called_function_name = "create_request_body"
        params = {
            API_KEY: self.api_key,
        }
        params.update(request_parameters)
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

        hash = hmac.new(str.encode(self.api_secret_key), sign.encode(UTF8), hashlib.sha256)
        signature = hash.hexdigest()
        sign_real = {
            SIGN: signature
        }
        body = dict(params,**sign_real)
        return (body, sign)

    def send_request_body(self, body, sign, request_type, endpoint):
        self.called_function_name = "send_request_body"
        url = self.BASIC_ENDPOINT + endpoint
        
        urllib3.disable_warnings()
        url = url + "?" + sign + '&sign='+body[SIGN]
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        #headers = {"Content-Type": "application/json"}
        
        if (request_type == GET):
            response = requests.get(url, headers=headers,verify=False)
            
        elif (request_type == POST):
            response = requests.post(url, headers=headers,verify=False)
        else:
            raise ValueError('The request type is incorrect')
        
        json_response = json.loads(response.text)
        if (json_response[RET_CODE] != self.REQUEST_ACK_OK):
            raise ValueError('Request was not sent successfully. \
            Error code is {}'.format(json_response[RET_CODE]))
        else:
            return json_response

    def send_request(self, request_type, endpoint, request_parameters):
        self.called_function_name = "send_request"

        body,sign = self.create_request_body(request_parameters)
        bybit_response = self.send_request_body(body, sign, request_type, endpoint)
        return bybit_response

    def cep__get_asset_balance(self, asset):
        self.called_function_name="cep__get_asset_balance"
        request_parameters = {TIMESTAMP: str(int(time.time()*1000))}

        bybit_response = self.send_request(GET, BYBIT_SPOT_WALLET_BALANCE, request_parameters)
        
        for coin_dict in bybit_response[RESULT][BALANCES]:
            if coin_dict[COIN] == asset:
                return coin_dict
        
        return 1
    
    def cep__get_avg_price(self, symbol):
        self.called_function_name="cep__get_avg_price"
        request_parameters = {SYMBOL:symbol}
        binance_response = self.send_request(GET, BYBIT_SPOT_SYMBOL_LAST_TRADE_PRICE, request_parameters)
        return binance_response[RESULT]

    def cep__get_symbol_price_ticker(self, symbol):
        self.called_function_name="cep__get_symbol_price_ticker"
        request_parameters = {SYMBOL:symbol}
        binance_response = self.send_request(GET, BYBIT_SPOT_SYMBOL_PRICE_TICKER, request_parameters)
        return binance_response[RESULT]

    def cep__get_order_book(self, symbol):
        self.called_function_name="cep__get_order_book"
        request_parameters = {SYMBOL:symbol}
        binance_response = self.send_request(GET, BYBIT_SPOT_SYMBOL_ORDER_BOOK, request_parameters)
        return binance_response

    def cep__get_exchange_info(self):
        self.called_function_name="cep__get_exchange_info"
        
        binance_response = self.send_request(GET, BYBIT_SPOT_QUERY_SYMBOL, {})
        return binance_response[RESULT]
    

    def create_spot_order(self, symbol, side, _type, qty):
        self.called_function_name = "create_spot_order"
        request_parameters = {SYMBOL:symbol, SIDE:side, \
                              TYPE:_type, QTY:qty,
                              TIMESTAMP: str(int(time.time()*1000))}

        bybit_response = self.send_request(POST, BYBIT_SPOT_CREATE_ORDER, request_parameters)
        
        return bybit_response

    def cep__close_long_spot(self, symbol, compute_avg_price, pct):
        self.called_function_name="cep__close_long_spot"

        precision = self.ALL_SYMBOLS_DICT[symbol][PRECISION_IDX]
        asset = self.ALL_SYMBOLS_DICT[symbol][ASSET_IDX]
        min_asset = 1*10**(-precision)
        available_asset = float(self.cep__get_asset_balance(asset=asset)[FREE])
        if (available_asset < (1*10**(-precision))):
            available_asset = 1*10**(-precision)

        while (available_asset > min_asset):
            available_asset = round(float(available_asset)*pct - 5*10**(-precision-1),precision+1)
        
            bybit_response = self.create_spot_order(symbol=symbol, \
                            side=SELL, _type=MARKET, qty=str(available_asset))
            time.sleep(0.3)
            available_asset = float(self.cep__get_asset_balance(asset=asset)[FREE])
            if (available_asset < (1*10**(-precision))):
                break
        
        return 0

    def cep__spot_account_trades(self, symbol, limit):
        self.called_function_name = "cep__spot_account_trades"
        
        request_parameters = {SYMBOL:symbol, LIMIT:str(limit), \
                              TIMESTAMP: str(int(time.time()*1000))}
        bybit_response = self.send_request(GET, BYBIT_SPOT_ORDER_HISTORY, \
                                            request_parameters)
        return bybit_response[RESULT]
    
    def cep__open_long_spot(self, symbol, compute_avg_price, pct):
        self.called_function_name="cep__open_long_spot"
        available_usdt = self.cep__get_asset_balance(asset=USDT)[FREE]
        available_usdt = round(float(available_usdt) - 0.05,2)
        while (available_usdt > 10):
            bybit_response = self.create_spot_order(symbol=symbol, side=BUY, _type=MARKET, \
                                qty=str(available_usdt))
            time.sleep(0.3)
            available_usdt = self.cep__get_asset_balance(asset=USDT)[FREE]
            available_usdt = round(float(available_usdt)*pct - 0.05,2)
        return 0

    def cep__get_symbol_price(self, symbol):
        self.called_function_name = "cep__get_symbol_price"
        request_parameters = {SYMBOL:symbol, TIMESTAMP: str(int(time.time()*1000))}

        bybit_response = self.send_request(GET, BYBIT_SPOT_SYMBOL_PRICE, request_parameters)
        
        return bybit_response[RESULT]
    
    def cep__compute_side_spot_account(self, account, cep_response):
        self.called_function_name="cep__compute_side_spot_account"
        if (not isinstance(cep_response, list)):
            return account.side
        else:
            bybit_response = cep_response
            if (len(bybit_response) != 0):
                if (bybit_response[0][SIDE] == SELL.upper()):
                    return OUT
                elif (bybit_response[0][SIDE] == BUY.upper()):
                    return LONG
                else:
                    return account.side
            else:
                return account.side

    ######################################### FUTURES #########################################

    def cep__futures_time(self):
        self.called_function_name = "cep__futures_time"
        
        bybit_response = self.send_request(GET, BYBIT_SERVER_TIME_ENDPOINT, {})
        timestamp = bybit_response[TIME_NOW]

        if (int(float(timestamp)) == 0):
            raise ValueError('Timestamp was equal to 0')
        else:
            return int(float(timestamp))

    def cep__get_futures_account_balance(self, asset):
        self.called_function_name = "cep__get_futures_account_balance"
        request_parameters = {TIMESTAMP: str(int(time.time()*1000))}
        binance_response = self.send_request(GET, BYBIT_FUTURES_WALLET_BALANCE, request_parameters)
        return binance_response[RESULT][asset]
    
    def cep__futures_account_trades(self, symbol):
        self.called_function_name = "cep__futures_account_trades"
        
        request_parameters = {SYMBOL:symbol, \
                            TIMESTAMP: str(int(time.time()*1000))}
        bybit_response = self.send_request(GET, BYBIT_FUTURES_POSITION, \
                                            request_parameters)
        return bybit_response[RESULT]

    def cep__get_symbol_price_futures(self, symbol):
        self.called_function_name="cep__get_symbol_price_futures"
        
        request_parameters = {SYMBOL:symbol}
        binance_response = self.send_request(GET, \
                                BYBIT_FUTURES_SYMBOL_LATEST_INFO, \
                                request_parameters)
        return binance_response[RESULT]
    
    def futures_create_order(self, symbol, side, positionSide, _type, quantity):
        self.called_function_name = "futures_create_order"
        request_parameters = {SYMBOL:symbol, \
                              SIDE:side, 
                              ORDER_TYPE:MARKET, \
                              QTY:quantity, \
                              TIME_IN_FORCE:GOODTILLCANCEL, 
                              CLOSE_ON_TRIGGER:False, \
                              TIMESTAMP: str(int(time.time()*1000))}
        if ((side == SELL and positionSide == LONG) or (side == BUY and positionSide == SHORT)):
            request_parameters[REDUCE_ONLY] = TRUE
        else:
            request_parameters[REDUCE_ONLY] = FALSE
        binance_response = self.send_request(POST, BYBIT_FUTURES_PLACE_ORDER, request_parameters)
        
        return binance_response
    
    def cep__get_my_futures_positions(self, symbol):
        self.called_function_name="cep__get_my_futures_positions"

        request_parameters = {SYMBOL:symbol, \
                            TIMESTAMP: str(int(time.time()*1000))}
        bybit_response = self.send_request(GET, \
                                BYBIT_FUTURES_MY_POSITIONS, \
                                request_parameters)
        return bybit_response[RESULT]

    def cep__futures_change_leverage(self, symbol, leverage):
        self.called_function_name="cep__futures_change_leverage"
        request_parameters = {SYMBOL:symbol, 
                            BUY_LEVERAGE:str(leverage), \
                            SELL_LEVERAGE:str(leverage), \
                            TIMESTAMP: str(int(time.time()*1000))}
        
        bybit_response = self.send_request(POST, \
                                BYBIT_FUTURES_SET_LEVERAGE, \
                                request_parameters)
        return bybit_response

    def cep__close_long_futures(self, symbol):
        self.called_function_name="cep__close_long_futures"
        bybit_positions = self.cep__get_my_futures_positions(symbol)

        if (isinstance(bybit_positions, list)):
            for elt in bybit_positions:
                if (elt[SIZE] > 0):
                    size = elt[SIZE]
                    leverage = elt[LEVERAGE]
                    break

            bybit_response = self.futures_create_order(symbol, SELL, LONG, MARKET, str(size))[RESULT]
        
            if (leverage > BYBIT_DEFAULT_LEVERAGE):
                self.CEP__BaseFunction(functools.partial( \
                    self.cep__futures_change_leverage, \
                    symbol, BYBIT_DEFAULT_LEVERAGE), \
                    retry=MAX_RETRY, \
                    retry_period=1)

            return bybit_response
        else: 
            return 1

    def cep__open_long_futures(self, symbol, leverage, \
                                engaged_balance, entryPrice, pct):
        self.called_function_name="cep__open_long_futures"
        balance = self.cep__get_futures_account_balance(USDT)['available_balance']
        if (leverage > BYBIT_DEFAULT_LEVERAGE):
            leverage = BYBIT_MAX_LEVERAGE
        
        self.CEP__BaseFunction(functools.partial( \
                self.cep__futures_change_leverage, \
                symbol, leverage), \
                retry=MAX_RETRY, \
                retry_period=1)
        
        precision = self.ALL_SYMBOLS_DICT[symbol][PRECISION_IDX]
        quantity=round(((float(balance)*engaged_balance/entryPrice) - \
                                                (5*10**(-precision - 1))), precision)
        if (quantity < (1*10**(-precision))):
            quantity = 1*10**(-precision)
        
        if (pct > 1):
            raise ValueError("Parameter pct has to be less than 1")
        quantity = quantity*pct

        while (balance > 30):
            bybit_response = self.futures_create_order(symbol, BUY, LONG, MARKET, str(quantity))[RESULT]
            
            balance = self.cep__get_futures_account_balance(USDT)['available_balance']
            precision = self.ALL_SYMBOLS_DICT[symbol][PRECISION_IDX]
            quantity=round(((float(balance)*engaged_balance/entryPrice) - \
                                                    (5*10**(-precision - 1))), precision)
            if (quantity < (1*10**(-precision))):
                quantity = 1*10**(-precision)
            quantity = quantity*pct
            time.sleep(0.5)
        return bybit_response

    def cep__close_short(self, symbol):
        self.called_function_name="cep__close_short"
        
        bybit_positions = self.cep__get_my_futures_positions(symbol)

        if (isinstance(bybit_positions, list)):
            for elt in bybit_positions:
                if (elt[SIZE] > 0):
                    size = elt[SIZE]
                    leverage = elt[LEVERAGE]
                    break

            bybit_response = self.futures_create_order(symbol, BUY, SHORT, MARKET, str(size))[RESULT]
        
            if (leverage > BYBIT_DEFAULT_LEVERAGE):
                self.CEP__BaseFunction(functools.partial( \
                    self.cep__futures_change_leverage, \
                    symbol, BYBIT_DEFAULT_LEVERAGE), \
                    retry=MAX_RETRY, \
                    retry_period=1)

            return bybit_response
        else: 
            return 1

    def cep__open_short(self, symbol, leverage, engaged_balance, \
                                            entryPrice, pct):
        self.called_function_name="cep__open_short"

        balance = self.cep__get_futures_account_balance(USDT)['available_balance']
        if (leverage > BYBIT_DEFAULT_LEVERAGE):
            leverage = BYBIT_MAX_LEVERAGE
        self.CEP__BaseFunction(functools.partial( \
            self.cep__futures_change_leverage, \
            symbol, leverage), \
            retry=MAX_RETRY, \
            retry_period=1)
        
        precision = self.ALL_SYMBOLS_DICT[symbol][PRECISION_IDX]
        quantity=round(((float(balance)*abs(engaged_balance)/entryPrice) - \
                                                (5*10**(-precision - 1))), precision)
        if (quantity < (1*10**(-precision))):
            quantity = 1*10**(-precision)
        
        if (pct > 1):
            raise ValueError("Parameter pct has to be less than 1")
        quantity = quantity*pct

        while (balance > 30):
            bybit_response = self.futures_create_order(symbol, SELL, SHORT, MARKET, str(quantity))[RESULT]
            
            balance = self.cep__get_futures_account_balance(USDT)['available_balance']
            precision = self.ALL_SYMBOLS_DICT[symbol][PRECISION_IDX]
            quantity=round(((float(balance)*engaged_balance/entryPrice) - \
                                                    (5*10**(-precision - 1))), precision)
            if (quantity < (1*10**(-precision))):
                quantity = 1*10**(-precision)
            quantity = quantity*pct
            time.sleep(0.5)
        return bybit_response

    def cep__compute_side_futures_account(self, account, cep_response):
        self.called_function_name="cep__compute_side_futures_account"
        if (not isinstance(cep_response, list)):
            return account.side
        else:
            if (len(cep_response) == 0):
                return account.side
            else:
                bybit_response = cep_response
                for elt in bybit_response:
                    if (elt[SIZE] > 0):
                        account.markPrice = 0
                        account.entryPrice = round(float(elt[ENTRY_PRICE]), 0)
                        account.leverage = elt[LEVERAGE]
                        account.positionAmt = elt[SIZE]
                        account.engaged_balance = abs(float(elt[POSITION_VALUE]/elt[POSITION_MARGIN]))
                        account.balance = float(elt[POSITION_MARGIN])
                        if (elt[SIDE]) == BUY:
                            return LONG 
                        elif (elt[SIDE]) == SELL:
                            return SHORT
                return account.side