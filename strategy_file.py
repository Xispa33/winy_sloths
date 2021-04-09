#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
from binance.client import Client
from interface_binance import *
from constants import *
from errors import *

class ApiKey:
    """
    A class used to gather all important information about an API key
    Attributes
    ----------
    api_key : list
        Api key
    
    api_secret_key : str
        Api key secret code
    
    side : str
        Account side. Can be either LONG/SHORT/OUT
    
    Methods
    -------
    
    """
    def __init__(self, info_strategy_file):
        self.api_key = info_strategy_file[0]
        self.api_secret_key = info_strategy_file[1]
        self.side = info_strategy_file[2]


class ApiKeyMaster(ApiKey):
    """
    A class used to represent a master' account
    Attributes
    ----------
    account_type : str
        Account type. Either SPOT or FUTURES
    
    symbol : str
        Symbol traded
    
    markPrice : int
        Mark price
    
    entryPrice : int
        Entry price
    
    leverage : int
        Leverage
    
    positionAmt : int
        Position amount
    
    engaged_balance : int
        Engaged balance
    
    balance : int
        Balance

    Methods
    -------
    computeEngagedBalance(line_nb, binance_response)
    
    """
    def __init__(self, info_strategy_file):
        super().__init__(info_strategy_file)
        self.account_type = info_strategy_file[3]
        self.symbol = info_strategy_file[4]
        self.markPrice = 0
        self.entryPrice = 0
        self.leverage = 0
        self.positionAmt = 0
        self.engaged_balance = 0
        self.balance = 0
    
    def computeEngagedBalance(self, line_nb, binance_response):
        """
        Name : computeEngagedBalance(line_nb, binance_response)
    
        Parameters : 
                      line_nb : int
                        Line number in winy_sloth.py that called computeEngagedBalance()
                      
                      binance_response : list
                        List provided by Binance about the master' information
        
        Description : Function that returns the amount in % of the wallet
                      in the trade
        """
        if (self.balance != 0):
            self.engaged_balance = (self.positionAmt * self.entryPrice/self.balance)
        else:
            print("Problem at line {}. WS should be restarting".format(line_nb))
            print(binance_response)
            print(I__GET_FUTURES_ACCOUNT_BALANCE(I__CLIENT(self.api_key, self.api_secret_key)))
            self.engaged_balance = (self.positionAmt * self.entryPrice/self.balance)
        

class ApiKeySlave(ApiKey):
    """
    A class used to represent a slave' account
    
    Attributes
    ----------
    api_key : list
        Api key
    
    api_secret_key : str
        Api key secret code
    
    side : str
        Account side. Can be either LONG/SHORT/OUT
    
    Methods
    -------
    
    """
    def __init__(self, info_strategy_file):
        super().__init__(info_strategy_file)

    def close_long(self, master_api):
        """
        Name : close_long(master_api)
    
        Parameters : 
                      master_api : ApiKeyMaster
                        Api key of the slave's master
    
        Description : Function that closes an opened long trade
        """
        client = I__CLIENT(self.api_key, self.api_secret_key)
        return I__CLOSE_LONG(client, master_api)

    def close_short(self, master_api):
        """
        Name : close_short(master_api)
    
        Parameters : 
                      master_api : ApiKeyMaster
                        Api key of the slave's master
    
        Description : Function that closes an opened short trade
        """
        client = I__CLIENT(self.api_key, self.api_secret_key)
        return I__CLOSE_SHORT(client, master_api.symbol, master_api.leverage)

    def open_long(self, master_api):
        """
        Name : open_long(master_api)
    
        Parameters : 
                      master_api : ApiKeyMaster
                        Api key of the slave's master
    
        Description : Function that opens a long trade
        """
        client = I__CLIENT(self.api_key, self.api_secret_key)
        return I__OPEN_LONG(client, master_api)

    def open_short(self, master_api):
        """
        Name : open_short(master_api)
    
        Parameters : 
                      master_api : ApiKeyMaster
                        Api key of the slave's master
    
        Description : Function that opens a short trade
        """
        client = I__CLIENT(self.api_key, self.api_secret_key)
        return I__OPEN_SHORT(client, master_api.symbol, master_api.leverage, master_api.engaged_balance, master_api.entryPrice)
    
    def open_long_from_short(self, master_api):
        """
        Name : open_long_from_short(master_api)
    
        Parameters : 
                      master_api : ApiKeyMaster
                        Api key of the slave's master
    
        Description : Function that opens a long trade from a short trade
        """
        if (not self.close_short(master_api)):
            return self.open_long(master_api)
        else:
            return 1

    def open_short_from_long(self, master_api):
        """
        Name : open_short_from_long(master_api)
    
        Parameters : 
                      master_api : ApiKeyMaster
                        Api key of the slave's master
    
        Description : Function that opens a short trade from a long trade
        """
        if (not self.close_long(master_api)):
            return self.open_short(master_api)
        else:
            return 1
    
class StrategyFile:
    """
    A class used to represent a strategy file
    Attributes
    ----------
    strategy_file_path : str
        Path of the folder containing all strategies
    
    master_api : ApiKeyMaster
        Api key of the master
    
    slave_apis : list
        List of ApiKeySlave, containing all slave for a strategy
    
    Methods
    -------
    StrategyFile__InitSlaves(info_strategy_file_slave)
    """
    def __init__(self, strategy_file_path, info_strategy_file_master, info_strategy_file_slave):
        self.strategy_file_path = strategy_file_path
        self.master_api = ApiKeyMaster(info_strategy_file_master)
        self.slave_apis = self.StrategyFile__InitSlaves(info_strategy_file_slave)
        self.global_slave_status = 0

    def StrategyFile__InitSlaves(self, info_strategy_file_slave):
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
            slaves_list.append(ApiKeySlave(slaves.strip('\n').split(" ")))

        return slaves_list