#!/usr/bin/python3
# -*- coding: utf-8 -*-

import bybit
import sys
sys.path.append(sys.path[0] + "/../..")
from constants import *
import os
from datetime import *
import traceback
from abc import ABC, abstractmethod
from crypto_exchange_platform import *
import time

BALANCES = "balances"
BUY = "Buy"
COIN = 'coin'
MARKET = "Market"
SELL = "Sell"
ENTRY_PRICE = "entry_price"
POSITION_VALUE = "position_value"
POSITION_MARGIN = "position_margin"
BYBIT_BASIC_ENDPOINT="https://api.bybit.com"
BYBIT_SERVER_TIME_ENDPOINT = "/v2/public/time"
BYBIT_SPOT_ORDER_HISTORY = "/spot/v1/history-orders"
BYBIT_SPOT_WALLET_BALANCE = "/spot/v1/account"
BYBIT_SPOT_CREATE_ORDER = "/spot/v1/order"
BYBIT_SPOT_SYMBOL_PRICE = "/spot/quote/v1/ticker/price"
TIME_NOW = 'time_now'
RET_CODE = "ret_code"
GET = "get"
POST = "post"
API_KEY = "api_key"
SIGN = "sign"
LIMIT = "limit"
QTY = "qty"

class CEP__Bybit(CryptoExchangePlatform):
    def __init__(self):
        super().__init__()
        self.name = BYBIT
        self.api_key = ""
        self.api_secret_key = ""
        self.REQUEST_ACK_OK = 0
        self.BASIC_TESTNET_ENDPOINT = ""
        self.BASIC_ENDPOINT = BYBIT_BASIC_ENDPOINT

    def cep__client(self, api_key, api_secret_key, account_contract_type): 
        self.called_function_name = "cep__client"
        if (account_contract_type != SPOT):
            self.api_key = ""
            self.api_secret_key = ""
            return (bybit.bybit(test=False, api_key=api_key, api_secret=api_secret_key))
        else:
            self.api_key = api_key
            self.api_secret_key = api_secret_key
            return 0

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
        url = BYBIT_BASIC_ENDPOINT + endpoint
        
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

    def get_timestamp(self):
        self.called_function_name = "get_timestamp"
        
        request_parameters = {}
        bybit_response = self.send_request(GET, BYBIT_SERVER_TIME_ENDPOINT, request_parameters)
        timestamp = bybit_response[TIME_NOW]

        if (int(float(timestamp)) == 0):
            raise ValueError('Timestamp was equal to 0')
        else:
            return int(float(timestamp))
    
    def get_spot_last_trade(self, symbol):
        self.called_function_name = "get_spot_last_trade"
        request_parameters = {SYMBOL:symbol, LIMIT:"1", TIMESTAMP: str(int(time.time()*1000))}

        bybit_response = self.send_request(GET, BYBIT_SPOT_ORDER_HISTORY, request_parameters)
        
        return bybit_response

    def create_spot_order(self, symbol, side, _type, qty):
        self.called_function_name = "create_spot_order"
        request_parameters = {SYMBOL:symbol, SIDE:side, \
                              TYPE:_type, QTY:qty,
                              TIMESTAMP: str(int(time.time()*1000))}

        bybit_response = self.send_request(POST, BYBIT_SPOT_CREATE_ORDER, request_parameters)
        
        return bybit_response

    def get_asset_balance(self):
        self.called_function_name = "get_asset_balance"
        request_parameters = {TIMESTAMP: str(int(time.time()*1000))}

        bybit_response = self.send_request(GET, BYBIT_SPOT_WALLET_BALANCE, request_parameters)
        
        return bybit_response

    def cep__futures_account_trades(self, client, symbol):
        self.called_function_name = "cep__futures_account_trades"
        return client.LinearPositions.LinearPositions_myPosition(symbol=symbol).result()
    
    def cep__spot_account_trades(self, client, symbol):
        self.called_function_name="cep__spot_account_trades"
        bybit_spot_history = self.get_spot_last_trade(symbol)
        return bybit_spot_history


    def cep__close_long_spot(self, client, symbol):
        self.called_function_name="cep__close_long_spot"

        precision = self.ALL_SYMBOLS_DICT[symbol][PRECISION_IDX]
        assets_list = self.get_asset_balance()[RESULT][BALANCES]
        available_asset = 0
        
        for elt in assets_list:
            if (elt[COIN] == self.ALL_SYMBOLS_DICT[symbol][ASSET_IDX]):
                available_asset = round(float(elt[FREE]) - (5*10**(-precision-1)), precision)
                break

        if (available_asset < (1*10**(-precision))):
            available_asset = 1*10**(-precision)
        
        self.create_spot_order(symbol=symbol, side=SELL, _type=MARKET, \
                            qty=str(available_asset))
        
        return 0

    def cep__close_long_futures(self, client, symbol):
        self.called_function_name="cep__close_long_futures"
        bybit_positions=client.LinearPositions.LinearPositions_myPosition( \
                            symbol=symbol).result()

        if (isinstance(bybit_positions, tuple)):
            bybit_positions = bybit_positions[0][RESULT]
            for elt in bybit_positions:
                if (elt[SIZE] > 0):
                    size = elt[SIZE]
                    break
            
            client.LinearOrder.LinearOrder_new(side=SELL, symbol=symbol, \
                            order_type=MARKET, qty=size, \
                            time_in_force=GOODTILLCANCEL, reduce_only=True, \
                            close_on_trigger=False).result()
            return 0
        else: 
            return 1

    
    def cep__open_long_spot(self, client, symbol):
        self.called_function_name="cep__open_long_spot"
        assets_list = self.get_asset_balance()[RESULT][BALANCES]
        available_usdt = 0
        for elt in assets_list:
            if (elt[COIN] == USDT):
                available_usdt = round(float(elt[FREE]) - 0.05, 1)
        
        self.create_spot_order(symbol=symbol, side=BUY, _type=MARKET, \
                            qty=str(available_usdt))
        
        return 0

    def cep__open_long_futures(self, client, symbol, leverage, \
                                engaged_balance, entryPrice):
        self.called_function_name="cep__open_long_futures"
        client.Positions.Positions_saveLeverage(symbol=symbol, \
                                            leverage=str(leverage)).result()

        bybit_balance_response = client.Wallet.Wallet_getBalance(coin=USDT).result()
        balance=bybit_balance_response[0][RESULT][USDT][WALLET_BALANCE]
        precision = self.ALL_SYMBOLS_DICT[symbol][PRECISION_IDX]
        quantity=round(((float(balance)*engaged_balance/entryPrice) - \
                                                (5*10**(-precision - 1))), precision)
        if (quantity < (1*10**(-precision))):
            quantity = 1*10**(-precision)

        client.LinearOrder.LinearOrder_new(side=BUY, symbol=symbol, order_type=MARKET, \
                    qty=quantity, time_in_force=GOODTILLCANCEL, reduce_only=False, \
                    close_on_trigger=False).result()

        return 0

    def cep__close_short(self, client, symbol):
        self.called_function_name="cep__close_short"

        bybit_positions=client.LinearPositions.LinearPositions_myPosition( \
                            symbol=symbol).result()

        if (isinstance(bybit_positions, tuple)):
            bybit_positions = bybit_positions[0][RESULT]
            for elt in bybit_positions:
                if (elt[SIZE] > 0):
                    size = elt[SIZE]
                    break
            client.LinearOrder.LinearOrder_new(side=BUY, symbol=symbol, \
                            order_type=MARKET, qty=size, \
                            time_in_force=GOODTILLCANCEL, reduce_only=True, \
                            close_on_trigger=False).result()
            return 0
        else: 
            return 1
    
    def cep__open_short(self, client, symbol, leverage, engaged_balance, \
                                            entryPrice):
        self.called_function_name="cep__open_short"
        
        client.Positions.Positions_saveLeverage(symbol=symbol, leverage=str(leverage)).result()

        bybit_balance_response = client.Wallet.Wallet_getBalance(coin=USDT).result()
        balance=bybit_balance_response[0][RESULT][USDT][WALLET_BALANCE]
        precision = self.ALL_SYMBOLS_DICT[symbol][PRECISION_IDX]
        quantity = round(((float(balance)*abs(engaged_balance)/entryPrice) - \
                                                    (5*10**(-precision - 1))), precision)

        if (quantity < (1*10**(-precision))):
            quantity = 1*10**(-precision)

        client.LinearOrder.LinearOrder_new(side=SELL, symbol=symbol, order_type=MARKET, \
                    qty=quantity, time_in_force=GOODTILLCANCEL, reduce_only=False, \
                    close_on_trigger=False).result()

        return 0

    def cep__get_futures_account_balance(self, client):
        self.called_function_name="cep__get_futures_account_balance"
        #USELESS
        return 0


    def cep__get_asset_balance(self, client):
        self.called_function_name="cep__get_asset_balance"
        #USELESS
        return 0
    

    def cep__set_stop_loss_long(self, client, symbol, engaged_balance, \
                                entryPrice, mode, risk=RISK):
        self.called_function_name="cep__set_stop_loss_long"
        
        return 0

    def cep__set_stop_loss_short(self, client, symbol, engaged_balance, \
                                entryPrice, mode, risk=RISK):
        self.called_function_name="cep__set_stop_loss_short"
        
        return 0
    
    def cep__clear_stop_loss(self, client, symbol):
        self.called_function_name="cep__clear_stop_loss"
        return 0
    
    
    def cep__compute_side_spot_account(self, account, cep_response):
        self.called_function_name="cep__compute_side_spot_account"
        if (not isinstance(cep_response, dict)):
            #print("Bybit return was crap ! \n")
            return account.side
        else:
            bybit_response = cep_response[RESULT]
            if (len(bybit_response) != 0):
                if (bybit_response[0][SIDE] == SELL.upper()):
                    return OUT
                elif (bybit_response[0][SIDE] == BUY.upper()):
                    return LONG
                else:
                    return account.side
            else:
                return account.side
        
    
    def cep__compute_side_futures_account(self, account, cep_response):
        self.called_function_name="cep__compute_side_futures_account"
        if (not isinstance(cep_response, tuple)):
            #print("Bybit return was crap ! \n")
            return account.side
        else:
            bybit_response = cep_response[0][RESULT]
            if (not isinstance(bybit_response, list)):
                return account.side
            else:
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

    
    def cep__compute_engaged_balance(self, account, cep_response):
        self.called_function_name="cep__compute_engaged_balance"
        #USELESS
        return 0
    
    def get_symbol_price(self, symbol):
        self.called_function_name = "get_symbol_price"
        request_parameters = {SYMBOL:symbol, TIMESTAMP: str(int(time.time()*1000))}

        bybit_response = self.send_request(GET, BYBIT_SPOT_SYMBOL_PRICE, request_parameters)
        
        return bybit_response

    def cep__get_symbol_price(self, symbol):
        self.called_function_name="cep__get_symbol_price"
        price = self.get_symbol_price(symbol)
        return price[RESULT][PRICE]