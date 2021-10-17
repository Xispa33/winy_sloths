#!/usr/bin/python3
# -*- coding: utf-8 -*-

from constants import *
import os
import sys
import time
import datetime
import traceback
from abc import ABC, abstractmethod
import functools
import hashlib
import hmac
import json
import requests
import urllib3

class CryptoExchangePlatform(ABC):
    """
    A class used to represent a cryptocurrency exchange platform. 
    This class is abstract.

    Attributes
    ----------
    name : str
        Name of the cryptocurrency exchange platform

    """
    def __init__(self, mode=DEBUG):
        self.name = ""
        self.called_function_name = ""
        self.ALL_SYMBOLS_DICT = {BTCUSDT:(BTC,3), ETHUSDT:(ETH,2), BNBUSDT:(BNB,2)}
        self.SPOT_TESTNET_ENDPOINT = ""
        self.SPOT_REAL_ENDPOINT = ""
        self.FUTURES_TESTNET_ENDPOINT = ""
        self.FUTURES_REAL_ENDPOINT = ""
        self.TESTNET_ENDPOINTS = ""
        self.REAL_ENDPOINTS = ""
        self.ENDPOINTS = ""
        self.BASIC_ENDPOINT = ""
        self.REQUEST_ACK_OK = 0
        self.mode = mode

    def CEP__Init_Dicts(self):
        self.TESTNET_ENDPOINTS = {SPOT:self.SPOT_TESTNET_ENDPOINT, FUTURES:self.FUTURES_TESTNET_ENDPOINT}
        self.REAL_ENDPOINTS = {SPOT:self.SPOT_REAL_ENDPOINT, FUTURES:self.FUTURES_REAL_ENDPOINT}
        self.ENDPOINTS = {DEBUG:self.TESTNET_ENDPOINTS, RUN:self.REAL_ENDPOINTS}
        self.BASIC_ENDPOINT = self.ENDPOINTS[self.mode]

    def get_called_function_name(self):
        return (self.called_function_name + "_" + self.name)

    def CEP__BaseFunction(self, api_service, retry=MAX_RETRY, retry_period=WAIT_DEFAULT):
        err_cpt = 0
        ret = 1
        api_ret = 1

        while (err_cpt < retry) and (ret == 1):
            try:
                api_ret = api_service()
                ret = 0
            except:
                ret = 1
                err_cpt += 1
                function = self.get_called_function_name()
                print("{} \nDATE : {} \n{} \n{}".format(function, \
                str(datetime.datetime.now()), sys.exc_info(), traceback.format_exc()))
                time.sleep(retry_period)
        
        return api_ret

    @abstractmethod
    def create_request_body(self, request_parameters): pass

    @abstractmethod
    def send_request_body(self, body, sign, request_type, endpoint): pass

    @abstractmethod
    def send_request(self, request_type, endpoint, request_parameters): pass

    @abstractmethod
    def check_response(self, response): pass

    def cep__client(self, api_key, api_secret_key, account_contract_type):
        self.called_function_name = "cep__client"
        self.api_key = api_key
        self.api_secret_key = api_secret_key
        self.BASIC_ENDPOINT = self.BASIC_ENDPOINT[account_contract_type]

    def CEP__CLIENT(self, api_key, api_secret_key, account_contract_type):
        self.called_function_name="CEP__CLIENT"
        return self.cep__client(api_key, api_secret_key, \
                                account_contract_type)

    @abstractmethod
    def cep__futures_account_trades(self, symbol): pass

    def CEP__FUTURES_ACCOUNT_TRADES(self, symbol):
        self.called_function_name="CEP__FUTURES_ACCOUNT_TRADES"
        return self.CEP__BaseFunction(functools.partial( \
                            self.cep__futures_account_trades, \
                            symbol))

    @abstractmethod
    def cep__spot_account_trades(self, symbol, limit='1'): pass

    def CEP__SPOT_ACCOUNT_TRADES(self, symbol, limit='1'):
        self.called_function_name="CEP__SPOT_ACCOUNT_TRADES"
        return self.CEP__BaseFunction(functools.partial( \
                            self.cep__spot_account_trades, \
                            symbol, limit))

    def CEP__GET_ACCOUNT_HISTORY(self, account_type, symbol):
        """
        Name : I__GET_ACCOUNT_HISTORY()
        
        Parameters : 
                    client : binance.client
                        Client used to connect to Binance server

                    account_type : str
                        Type of account, either 'SPOT' or 'FUTURES'

                    symbol : str
                        Currency traded
        
        Description : Gets a symbol's trade history, depending on the 
                    account_type. 
                    Client contains the API key credentials allowing 
                    to connect to Binance server
        """
        self.called_function_name="CEP__GET_ACCOUNT_HISTORY"
        if (account_type == SPOT):
            ret = self.CEP__SPOT_ACCOUNT_TRADES(symbol)
        elif (account_type == FUTURES):
            ret = self.CEP__FUTURES_ACCOUNT_TRADES(symbol)
        else:
            ret = 1
        
        return ret

    @abstractmethod
    def cep__close_long_spot(self, symbol, compute_avg_price, pct): pass

    def CEP__CLOSE_LONG_SPOT(self, symbol, compute_avg_price, pct):
        self.called_function_name="CEP__CLOSE_LONG_SPOT"
        return self.CEP__BaseFunction(functools.partial( \
                            self.cep__close_long_spot, \
                            symbol, compute_avg_price, pct), \
                            retry=100, \
                            retry_period=0.1)
    #TODO: ADD PCT AS PARAMETER HERE
    @abstractmethod
    def cep__close_long_futures(self, symbol): pass

    def CEP__CLOSE_LONG_FUTURES(self, symbol):
        self.called_function_name="CEP__CLOSE_LONG_FUTURES"
        return self.CEP__BaseFunction(functools.partial( \
                                self.cep__close_long_futures, \
                                symbol), \
                                retry=MAX_RETRY*100, \
                                retry_period=0.1)

    def CEP__CLOSE_LONG(self, account_contract_type, symbol, compute_avg_price=FALSE, pct=1):
        """
        Name : I__CLOSE_LONG()
        
        Parameters : 
                    client : binance.client
                        Client used to connect to Binance server

                    master_api : ApiKeyMaster
                        Binance account handled by EC
        
        Description : Function closing an open trade depending on 
                    the accounts type (SPOT/FUTURES).
                    Client contains the API key credentials allowing
                    to connect to Binance server.
        """
        self.called_function_name="CEP__CLOSE_LONG"
        if (account_contract_type == SPOT):
            ret = self.CEP__CLOSE_LONG_SPOT(symbol, compute_avg_price, pct)
        elif (account_contract_type == FUTURES):
            ret = self.CEP__CLOSE_LONG_FUTURES(symbol)
        else:
            ret = 1
            
        return ret

    @abstractmethod
    def cep__open_long_futures(self, symbol, leverage, \
                               engaged_balance, entryPrice, pct): pass

    def CEP__OPEN_LONG_FUTURES(self, symbol, leverage, \
                               engaged_balance, entryPrice, pct):
        self.called_function_name="CEP__OPEN_LONG_FUTURES"
        return self.CEP__BaseFunction(functools.partial( \
                            self.cep__open_long_futures, symbol, leverage, \
                            engaged_balance, entryPrice, pct), retry_period=0.5)

    @abstractmethod
    def cep__open_long_spot(self, symbol, compute_avg_price, pct): pass

    def CEP__OPEN_LONG_SPOT(self, symbol, compute_avg_price, pct):
        self.called_function_name="CEP__OPEN_LONG_SPOT"
        return self.CEP__BaseFunction(functools.partial( \
                            self.cep__open_long_spot, \
                            symbol, compute_avg_price, pct), retry_period=0.5)

    def CEP__OPEN_LONG(self, account_contract_type, symbol, \
                        leverage, engaged_balance, entryPrice, \
                        compute_avg_price=FALSE, pct = 1):
        self.called_function_name="CEP__OPEN_LONG"
        if (account_contract_type == SPOT):
            ret = self.CEP__OPEN_LONG_SPOT(symbol, compute_avg_price, pct)
        elif (account_contract_type == FUTURES):
            ret = self.CEP__OPEN_LONG_FUTURES( symbol, \
                                leverage, \
                                engaged_balance, \
                                entryPrice, pct)
        else:
            ret = 1

        return ret
    # TODO:ADD PCT AS PARAMETER HERE
    @abstractmethod
    def cep__close_short(self, symbol): pass

    def CEP__CLOSE_SHORT(self, symbol):
        self.called_function_name="CEP__CLOSE_SHORT"
        return self.CEP__BaseFunction(functools.partial( \
                            self.cep__close_short, \
                            symbol), retry=MAX_RETRY*100, \
                            retry_period=0.1)

    @abstractmethod
    def cep__open_short(self, symbol, leverage, \
                        engaged_balance, entryPrice, pct): pass

    def CEP__OPEN_SHORT(self, symbol, leverage, \
                        engaged_balance, entryPrice, pct=1):
        self.called_function_name="CEP__OPEN_SHORT"
        return self.CEP__BaseFunction(functools.partial( \
                            self.cep__open_short, \
                            symbol, leverage, engaged_balance, \
                            entryPrice, pct), retry_period=0.5)
    
    @abstractmethod
    def cep__get_futures_account_balance(self, asset): pass

    def CEP__GET_FUTURES_ACCOUNT_BALANCE(self, asset):
        self.called_function_name="CEP__GET_FUTURES_ACCOUNT_BALANCE"
        return self.CEP__BaseFunction(functools.partial( \
                            self.cep__get_futures_account_balance, \
                            asset), retry=MAX_RETRY*5, retry_period=0.5)

    @abstractmethod
    def cep__get_asset_balance(self, asset): pass

    def CEP__GET_ASSET_BALANCE(self, asset):
        self.called_function_name="CEP__GET_ASSET_BALANCE"
        return self.CEP__BaseFunction(functools.partial( \
                            self.cep__get_asset_balance, \
                            asset), retry_period=0.5)

    @abstractmethod
    def cep__compute_side_spot_account(self, account, cep_response): pass

    def CEP__COMPUTE_SIDE_SPOT_ACCOUNT(self, account, cep_response):
        self.called_function_name="CEP__COMPUTE_SIDE_SPOT_ACCOUNT"
        return self.cep__compute_side_spot_account(account, cep_response)

    @abstractmethod
    def cep__compute_side_futures_account(self, account, cep_response): pass

    def CEP__COMPUTE_SIDE_FUTURES_ACCOUNT(self, account, cep_response):
        self.called_function_name="CEP__COMPUTE_SIDE_FUTURES_ACCOUNT"
        return self.cep__compute_side_futures_account(account, cep_response)

    def CEP__COMPUTE_ACCOUNT_SIDE(self, account, cep_response):
        self.called_function_name="CEP__COMPUTE_ACCOUNT_SIDE"
        if (account.account_contract_type == SPOT):
            return self.CEP__COMPUTE_SIDE_SPOT_ACCOUNT(account, cep_response)
        elif (account.account_contract_type == FUTURES):
            return self.CEP__COMPUTE_SIDE_FUTURES_ACCOUNT(account, cep_response)
        else:
            return account.side
    
    @abstractmethod
    def cep__get_symbol_price(self, symbol): pass

    def CEP__GET_SYMBOL_PRICE_SPOT(self, symbol):
        self.called_function_name="CEP__GET_SYMBOL_PRICE_SPOT"
        return self.cep__get_symbol_price(symbol)
    
    @abstractmethod
    def cep__get_symbol_price_futures(self, symbol): pass

    def CEP__GET_SYMBOL_PRICE_FUTURES(self, symbol):
        self.called_function_name="CEP__GET_SYMBOL_PRICE_FUTURES"
        return self.cep__get_symbol_price_futures(symbol)

    def CEP__GET_SYMBOL_PRICE(self, account_contract_type, symbol):
        self.called_function_name="CEP__GET_SYMBOL_PRICE"
        if (account_contract_type == SPOT): 
            return self.CEP__GET_SYMBOL_PRICE_SPOT(symbol)[PRICE]
        elif (account_contract_type == FUTURES):
            return self.CEP__GET_SYMBOL_PRICE_FUTURES(symbol)[PRICE]
        else:
            return 1

    def CEP__COMPUTE_AVG_PRICE(self, prices_list, qty_list):
        self.called_function_name="CEP__COMPUTE_AVG_PRICE"
        tot_qty = 0
        nb_elt_price = len(prices_list)
        nb_elt_qty_list = len(qty_list)
        tot_qty = sum(float(elt) for elt in qty_list)
        if (nb_elt_price == nb_elt_qty_list):
            return sum(float(prices_list[i])*float(qty_list[i]) \
                        for i in range(nb_elt_price))/tot_qty