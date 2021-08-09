#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
from binance.client import Client
from interface_binance import *
from constants import *
from errors import *
from cep_binance import *
#from cep_coinbase import *

class ApiKey:
    """
    A class used to gather all important information about an API key
    
    Attributes
    ----------
    exchange_platform_name : str
        Name of the exchange platform linked to the API key
    
    _api_key : list
        Api key
    
    _api_secret_key : str
        Api key secret code
    
    exchange_platform_obj : CryptoExchangePlatform
        Crypto exchange platform object
    
    Methods
    -------
    find_exchange_platform_class()
    
    """
    def __init__(self, info_strategy_file):
        self.exchange_platform_name = info_strategy_file[ \
                                    OFFSET_EXCHANGE_PLATFORM]
        self._api_key = info_strategy_file[OFFSET_API_KEY]
        self._api_secret_key = info_strategy_file[ \
                                        OFFSET_API_SECRET_KEY]

        self.exchange_platform_obj = self.find_exchange_platform_class()

    def find_exchange_platform_class(self):
        klass = globals()[CEP + self.exchange_platform_name]
        return klass()
        
        
class Account():
    """
    Description :
        A class used to represent an account on a 
        crypto exchange platform. Either a slave or a 
        master, but this is an abstract class.

    Attributes
    ----------
    api_key : ApiKey
        Account API key basic information
    
    account_rtype : str
        Type of the account. Either master or slave
    
    side : str
        Account side. Can be either LONG/SHORT/OUT
    
    Methods
    -------
    close_long()
    close_short()
    open_long()
    open_short()
    open_long_from_short()
    open_short_from_long()
    """
    def __init__(self, info_strategy_file, rtype=None, account_contract_type=None, symbol=None):
        #super().__init__(info_strategy_file)
        self.api_key = ApiKey(info_strategy_file)
        self.account_rtype = rtype if rtype != None else ""
        self.side = info_strategy_file[OFFSET_SIDE]
        
        if (self.account_rtype == MASTER):
            #CASE WHERE MASTER IS INITIALIZING
            self.account_contract_type = info_strategy_file[OFFSET_ACCOUNT_TYPE]
            self.symbol = info_strategy_file[OFFSET_SYMBOL]
        else:
            #CASE WHERE SLAVE IS INITIALIZING
            self.account_contract_type = account_contract_type
            self.symbol = symbol
        
        self.markPrice = 0
        self.entryPrice = 0
        self.leverage = 0
        self.positionAmt = 0
        self.engaged_balance = 0
        self.balance = 0
        self.account_mode = ONE_WAY
    
    def close_long(self):
        """
        Name : close_long(master_api)
    
        Parameters : 
                      master_api : ApiKeyMaster
                        Api key of the slave's master
    
        Description : Function that closes an opened long trade
        """
        client = self.api_key.exchange_platform_obj.CEP__CLIENT( \
                                    self.api_key._api_key, self.api_key._api_secret_key)
        return self.api_key.exchange_platform_obj.CEP__CLOSE_LONG( \
                                    client, self.account_contract_type, self.symbol)

    def close_short(self):
        """
        Name : close_short(master_api)
    
        Parameters : 
                      master_api : ApiKeyMaster
                        Api key of the slave's master
    
        Description : Function that closes an opened short trade
        """
        client = self.api_key.exchange_platform_obj.CEP__CLIENT( \
                                    self.api_key._api_key, self.api_key._api_secret_key)
        return self.api_key.exchange_platform_obj.CEP__CLOSE_SHORT( \
                                    client, self.symbol)

    def open_long(self):
        """
        Name : open_long(master_api)
    
        Parameters : 
                      master_api : ApiKeyMaster
                        Api key of the slave's master
    
        Description : Function that opens a long trade
        """
        client = self.api_key.exchange_platform_obj.CEP__CLIENT(self.api_key._api_key, self.api_key._api_secret_key)
        return self.api_key.exchange_platform_obj.CEP__OPEN_LONG(client, self)

    def open_short(self):
        """
        Name : open_short(master_api)
    
        Parameters : 
                      master_api : ApiKeyMaster
                        Api key of the slave's master
    
        Description : Function that opens a short trade
        """
        client = self.api_key.exchange_platform_obj.CEP__CLIENT( \
                                    self.api_key._api_key, self.api_key._api_secret_key)
        return self.api_key.exchange_platform_obj.CEP__OPEN_SHORT(client, self.symbol, \
                                                        self.leverage, \
                                                        self.engaged_balance, \
                                                        self.entryPrice)
    
    def open_long_from_short(self):
        """
        Name : open_long_from_short(master_api)
    
        Parameters : 
                      master_api : ApiKeyMaster
                        Api key of the slave's master
    
        Description : Function that opens a long trade from a short trade
        """
        if (not self.close_short()):
            return self.open_long()
        else:
            return 1

    def open_short_from_long(self):
        """
        Name : open_short_from_long(master_api)
    
        Parameters : 
                      master_api : ApiKeyMaster
                        Api key of the slave's master
    
        Description : Function that opens a short trade from a long trade
        """
        if (not self.close_long()):
            return self.open_short()
        else:
            return 1
        

class SlaveAccount(Account):
    """
    Description :
        A class used to represent a slave's account. Inherits from Account class
    
    Attributes
    ----------

    Methods
    -------
    
    """
    def __init__(self, info_strategy_file, account_contract_type, symbol):
        super().__init__(info_strategy_file, rtype=SLAVE, \
                    account_contract_type=account_contract_type, \
                    symbol=symbol)

class MasterAccount(Account):
    """
    Description :
        A class used to represent a master's account. Inherits from Account class
    
    Attributes
    ----------

    Methods
    -------
    
    """
    def __init__(self, info_strategy_file):
        super().__init__(info_strategy_file, rtype=MASTER)

class StrategyFile:
    """
    Description : 
        A class gathering all information about a strategy file

    Attributes
    ----------
    strategy_file_path : str
        Path of the strategy file
    
    master_api : MasterAccount
        MasterAccount object representing the master of a strategy
    
    slave_apis : list
        List containing all SlaveAccount of a strategy.
        SlaveAccount represents a slave of a strategy. 

    Methods
    -------
    StrategyFile__InitSlaves()

    """
    def __init__(self, strategy_file_path, info_strategy_file_master, info_strategy_file_slave):
        self.strategy_file_path = strategy_file_path
        self.master_api = MasterAccount(info_strategy_file_master)
        self.slave_apis = self.StrategyFile__InitSlaves(info_strategy_file_slave, \
                            self.master_api.account_contract_type, self.master_api.symbol)

    def StrategyFile__InitSlaves(self, info_strategy_file_slave, account_contract_type, symbol):
        """
        Name : StrategyFile__InitSlaves(info_strategy_file_slave)
    
        Parameters : 
                      info_strategy_file_slave : str
                        Information about all slaves

        Description : Function that retrieves all slaves of a strategy 
                      and gather then into a list

        """
        slaves_list = []

        for slaves in info_strategy_file_slave:
            slaves_list.append(SlaveAccount(slaves.strip('\n').split(" "), \
                                account_contract_type, symbol))

        return slaves_list