#!/usr/bin/python3
# -*- coding: utf-8 -*-

import binance
from constants import *

def I__GET_SYSTEM_STATUS(client):
    """
    Name : I__GET_SYSTEM_STATUS()
    
    Parameters : 
        client : binance.client
            Client used to connect to Binance server
    
    Description : Checks the connectivity of an API key pair with Binance server
    """
    try:
        ret = client.get_system_status()['status']
    except:
        ret = 2
    
    return ret

def I__FUTURES_ACCOUNT_TRADES(client, symbol):
    """
    Name : I__FUTURES_ACCOUNT_TRADES()
    
    Parameters : 
        client : binance.client
            Client used to connect to Binance server
        symbol : str
            Currency traded
    
    Description : Gets a symbol's trade history of a futures account. Client contains the API key credentials allowing to connect to Binance server
    """
    try:
        ret = client.futures_account_trades(symbol=symbol, limit='1')
    except:
        ret = 1

    return ret

def I__SPOT_ACCOUNT_TRADES(client, symbol):
    """
    Name : I__SPOT_ACCOUNT_TRADES()
    
    Parameters : 
        client : binance.client
            Client used to connect to Binance server
        symbol : str
            Currency traded 
    
    Description : Gets a symbol's trade history of a SPOT account. Client contains the API key credentials allowing to connect to Binance server
    """
    try:
        ret = client.get_all_orders(symbol=symbol, limit='1')
    except:
        ret = 1
    
    return ret

def I__GET_ACCOUNT_HISTORY(client, account_type, symbol):
    """
    Name : I__GET_ACCOUNT_HISTORY()
    
    Parameters : 
        client : binance.client
            Client used to connect to Binance server
        account_type : str
            Type of account, either 'SPOT' or 'FUTURES'
        symbol : str
            Currency traded
    
    Description : Gets the trade history of a symbol, depending on the account_type. 
                  Client contains the API key credentials allowing to connect to Binance server
    """
    if (account_type == SPOT):
        ret = I__SPOT_ACCOUNT_TRADES(client, symbol)
    elif (account_type == FUTURES):
        ret = I__FUTURES_ACCOUNT_TRADES(client, symbol)
    else:
        ret = 1
    
    return ret

def I__GET_FUTURES_POSITION(client, symbol):
    """
    Name : I__GET_FUTURES_POSITION()
    
    Parameters : 
        client : binance.client
            Client used to connect to Binance server

        symbol : str
            Currency traded
    
    Description : Gets the position side of a futures account (supposing that the account only trades on 1 symbol) 
                  Client contains the API key credentials allowing to connect to Binance server
    """
    try:
        a = client.futures_time()
        ret = client.futures_position_information(symbol=symbol, timestamp=a)
        ret = (ret[0]['positionSide'], float(ret[0]['entryPrice']))
        #ret = ('BOTH', 0.0)
    except:
        ret = 1
    
    return ret