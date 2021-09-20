#!/usr/bin/python3
# -*- coding: utf-8 -*-

from constants import *
import os
import sys
import datetime
import traceback
from abc import ABC, abstractmethod
import functools
import hashlib
import hmac
import json
import requests
import urllib3



API_KEY = "api_key"
SIGN = "sign"
GET = "get"
POST = "post"

class Client:
    def __init__(self, api_key, api_secret_key):
        self._api_key = api_key
        self._api_secret_key = api_secret_key
class CryptoExchangePlatform(ABC):
    """
    A class used to represent a cryptocurrency exchange platform. 
    This class is abstract.

    Attributes
    ----------
    name : str
        Name of the cryptocurrency exchange platform
    
    called_function_name : str
        Name of the function called
    
    Methods
    -------
    get_called_function_name()
    CEP__BaseFunction()
    cep__client()
    CEP__CLIENT()
    cep__futures_account_trades()
    CEP__FUTURES_ACCOUNT_TRADES()
    cep__spot_account_trades()
    CEP__SPOT_ACCOUNT_TRADES()
    CEP__GET_ACCOUNT_HISTORY()
    cep__close_long_spot()
    CEP__CLOSE_LONG_SPOT()
    cep__close_long_futures()
    CEP__CLOSE_LONG_FUTURES()
    CEP__CLOSE_LONG()
    cep__open_long_futures()
    CEP__OPEN_LONG_FUTURES()
    cep__open_long_spot()
    CEP__OPEN_LONG_SPOT()
    CEP__OPEN_LONG()
    cep__close_short()
    CEP__CLOSE_SHORT()
    cep__open_short()
    CEP__OPEN_SHORT()
    cep__get_futures_account_balance()
    CEP__GET_FUTURES_ACCOUNT_BALANCE()
    cep__get_asset_balance()
    CEP__GET_ASSET_BALANCE()
    cep__set_stop_loss_long
    CEP__SET_STOP_LOSS_LONG()
    cep__set_stop_loss_short()
    CEP__SET_STOP_LOSS_SHORT()
    cep__clear_stop_loss()
    CEP__CLEAR_STOP_LOSS()
    CEP__MANAGE_STOP_LOSS()
    cep__compute_side_spot_account()
    CEP__COMPUTE_SIDE_SPOT_ACCOUNT()
    cep__compute_side_futures_account()
    CEP__COMPUTE_SIDE_FUTURES_ACCOUNT()
    CEP__COMPUTE_ACCOUNT_SIDE()
    cep__compute_engaged_balance()
    CEP__COMPUTE_ENGAGED_BALANCE()
    """
    def __init__(self):
        self.name = ""
        self.called_function_name = ""
        self.ALL_SYMBOLS_DICT = {BTCUSDT:(BTC,3), ETHUSDT:(ETH,2), BNBUSDT:(BNB,2)}
        self.BASIC_ENDPOINT = ""
        self.BASIC_TESTNET_ENDPOINT = ""
        self.REQUEST_ACK_OK = 0

    def get_called_function_name(self):
        return (self.called_function_name + "_" + self.name)

    def CEP__BaseFunction(self, api_service, retry=MAX_RETRY, retry_period=WAIT_DEFAULT):
        err_cpt = 0
        ret = 1
        api_ret = ""

        while (err_cpt < retry) and (ret == 1):
            try:
                api_ret = api_service()
                ret = 0
            except:
                ret = 1
                err_cpt += 1
                function = self.get_called_function_name()
                print("{} \nDATE : {} \n{} \n{}".format(function, \
                str(datetime.now()), sys.exc_info(), traceback.format_exc()))
                sleep(retry_period)
        
        return api_ret

    @abstractmethod
    def create_request_body(self, request_parameters): pass

    @abstractmethod
    def send_request_body(self, body, sign, request_type, endpoint): pass

    @abstractmethod
    def send_request(self, request_type, endpoint, request_parameters): pass

    @abstractmethod
    def check_response(self, response): pass

    @abstractmethod
    def cep__client(self, api_key, api_secret_key, account_contract_type): pass

    def CEP__CLIENT(self, api_key, api_secret_key, account_contract_type):
        self.called_function_name="CEP__CLIENT"
        return self.CEP__BaseFunction(functools.partial(self.cep__client, \
                            api_key, api_secret_key, account_contract_type), \
                            retry=MAX_RETRY*4)

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
    def cep__close_long_spot(self, client, symbol): pass

    def CEP__CLOSE_LONG_SPOT(self, client, symbol):
        self.called_function_name="CEP__CLOSE_LONG_SPOT"
        return self.CEP__BaseFunction(functools.partial( \
                            self.cep__close_long_spot, \
                            client, symbol), \
                            retry=MAX_RETRY*100, \
                            retry_period=0.1)

    @abstractmethod
    def cep__close_long_futures(self, client, symbol): pass

    def CEP__CLOSE_LONG_FUTURES(self, client, symbol):
        self.called_function_name="CEP__CLOSE_LONG_FUTURES"
        return self.CEP__BaseFunction(functools.partial( \
                                self.cep__close_long_futures, \
                                client, symbol), \
                                retry=MAX_RETRY*100, \
                                retry_period=0.1)

    def CEP__CLOSE_LONG(self, client, account_contract_type, symbol):
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
            ret = self.CEP__CLOSE_LONG_SPOT(client, symbol)
        elif (account_contract_type == FUTURES):
            ret = self.CEP__CLOSE_LONG_FUTURES(client, symbol)
        else:
            ret = 1
            
        return ret


    @abstractmethod
    def cep__open_long_futures(self, client, symbol, leverage, \
                               engaged_balance, entryPrice): pass

    def CEP__OPEN_LONG_FUTURES(self, client, symbol, leverage, \
                               engaged_balance, entryPrice):
        self.called_function_name="CEP__OPEN_LONG_FUTURES"
        return self.CEP__BaseFunction(functools.partial( \
                            self.cep__open_long_futures, client, \
                            symbol, leverage, engaged_balance, \
                            entryPrice), retry_period=0.5)

    @abstractmethod
    def cep__open_long_spot(self, client, symbol): pass

    def CEP__OPEN_LONG_SPOT(self, client, symbol):
        self.called_function_name="CEP__OPEN_LONG_SPOT"
        return self.CEP__BaseFunction(functools.partial( \
                            self.cep__open_long_spot, \
                            client, symbol), retry_period=0.5)

    #def CEP__OPEN_LONG(self, client, account):
    def CEP__OPEN_LONG(self, client, account_contract_type, symbol, \
                        leverage, engaged_balance, entryPrice):
        self.called_function_name="CEP__OPEN_LONG"
        if (account_contract_type == SPOT):
            ret = self.CEP__OPEN_LONG_SPOT(client, symbol)
        elif (account_contract_type == FUTURES):
            ret = self.CEP__OPEN_LONG_FUTURES(client, \
                                symbol, \
                                leverage, \
                                engaged_balance, \
                                entryPrice)
        else:
            ret = 1

        return ret
    

    @abstractmethod
    def cep__close_short(self, client, symbol): pass

    def CEP__CLOSE_SHORT(self, client, symbol):
        self.called_function_name="CEP__CLOSE_SHORT"
        return self.CEP__BaseFunction(functools.partial( \
                            self.cep__close_short, client, \
                            symbol), retry=MAX_RETRY*100, \
                            retry_period=0.1)


    @abstractmethod
    def cep__open_short(self, client, symbol, leverage, \
                        engaged_balance, entryPrice): pass

    def CEP__OPEN_SHORT(self, client, symbol, leverage, \
                        engaged_balance, entryPrice):
        self.called_function_name="CEP__OPEN_SHORT"
        return self.CEP__BaseFunction(functools.partial( \
                            self.cep__open_short, client, \
                            symbol, leverage, engaged_balance, \
                            entryPrice), retry_period=0.5)
    

    @abstractmethod
    #PLATFORM SPECIFIC
    def cep__get_futures_account_balance(self, client): pass

    def CEP__GET_FUTURES_ACCOUNT_BALANCE(self, client):
        self.called_function_name="CEP__GET_FUTURES_ACCOUNT_BALANCE"
        return self.CEP__BaseFunction(functools.partial( \
                            self.cep__get_futures_account_balance, \
                            client), retry=MAX_RETRY*5, retry_period=0.5)


    @abstractmethod
    #PLATFORM SPECIFIC
    def cep__get_asset_balance(self, client): pass

    def CEP__GET_ASSET_BALANCE(self, client):
        self.called_function_name="CEP__GET_ASSET_BALANCE"
        return self.CEP__BaseFunction(functools.partial( \
                            self.cep__get_asset_balance, \
                            client), retry_period=0.5)

    """
    @abstractmethod
    def cep__set_stop_loss_long(self, client, symbol, engaged_balance, \
                                entryPrice, mode, risk=RISK): pass

    def CEP__SET_STOP_LOSS_LONG(self, client, symbol, engaged_balance, \
                                entryPrice, mode, risk=RISK):
        self.called_function_name="CEP__SET_STOP_LOSS_LONG"
        return self.CEP__BaseFunction(functools.partial( \
                            self.cep__set_stop_loss_long, \
                            client, symbol, engaged_balance, \
                            entryPrice, mode, risk=RISK), \
                            retry_period=0.5)
    """
    """
    @abstractmethod
    def cep__set_stop_loss_short(self, client, symbol, engaged_balance, \
                                entryPrice, mode, risk=RISK): pass

    def CEP__SET_STOP_LOSS_SHORT(self, client, symbol, engaged_balance, \
                                 entryPrice, mode, risk=RISK):
        self.called_function_name="CEP__SET_STOP_LOSS_SHORT"
        return self.CEP__BaseFunction(functools.partial( \
                            self.cep__set_stop_loss_short, \
                            client, symbol, engaged_balance, \
                            entryPrice, mode, risk=RISK), retry_period=0.5)
    """
    """
    @abstractmethod
    def cep__clear_stop_loss(self, client, symbol): pass

    def CEP__CLEAR_STOP_LOSS(self, client, symbol):
        self.called_function_name="CEP__CLEAR_STOP_LOSS"
        return self.CEP__BaseFunction(functools.partial( \
                            self.cep__clear_stop_loss, \
                            client, symbol), retry_period=0.5)


    def CEP__MANAGE_STOP_LOSS(self, client, symbol, \
                              engaged_balance, entryPrice, \
                              side, mode, risk=RISK):
        self.called_function_name="CEP__MANAGE_STOP_LOSS"
        if (side == LONG):
            ret = self.CEP__SET_STOP_LOSS_LONG(client, symbol, \
                                engaged_balance, entryPrice, \
                                mode, risk)
        elif (side == SHORT):
            ret = self.CEP__SET_STOP_LOSS_SHORT(client, symbol, \
                                engaged_balance, entryPrice, \
                                mode, risk)
        elif (side == OUT):
            ret = self.CEP__CLEAR_STOP_LOSS(client, symbol)
        else:
            return 1
        
        return ret
    """
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
    
    """
    @abstractmethod
    #PLATFORM SPECIFIC
    def cep__compute_engaged_balance(self, account, cep_response): pass
    
    def CEP__COMPUTE_ENGAGED_BALANCE(self, account, cep_response):
        self.called_function_name="CEP__COMPUTE_ENGAGED_BALANCE"
        return self.cep__compute_engaged_balance(account, cep_response)
    """
    @abstractmethod
    def cep__get_symbol_price(self, client, symbol): pass
    
    
    def CEP__GET_SYMBOL_PRICE(self, client, symbol):
        self.called_function_name="CEP__GET_SYMBOL_PRICE"
        return self.CEP__BaseFunction(functools.partial( \
                            self.cep__get_symbol_price, \
                            client, symbol), retry=5, \
                            retry_period=0.1)
        