#!/usr/bin/python3
# -*- coding: utf-8 -*-

import binance
from constants import *

def I__GET_SYSTEM_STATUS(client):
    try:
        ret = client.get_system_status()['status']
    except:
        ret = 2
    
    return ret

def I__FUTURES_ACCOUNT_TRADES(client, symbol):
    try:
        #return client.futures_account_trades(symbol=symbol, limit='1')
        #return client.futures_account_trades()
        return client.futures_account_trades(symbol=symbol, limit='1')
    except:
        return 1

def I__SPOT_ACCOUNT_TRADES(client, symbol):
    try:
        ret = client.get_all_orders(symbol=symbol, limit='1')
    except:
        ret = 1
    
    return ret

def I__GET_ACCOUNT_HISTORY(client, account_type, symbol):
    if (account_type == SPOT):
        return I__SPOT_ACCOUNT_TRADES(client, symbol)
    elif (account_type == FUTURES):
        return I__FUTURES_ACCOUNT_TRADES(client, symbol)
    else:
        return 1

def I__GET_FUTURES_POSITION(client, symbol):
    try:
        #ret = client.futures_position_information(symbol=symbol, timestamp=client.futures_time())
        #return (ret['positionSide'], float(ret['positionSide']))
        return ('BOTH', 0.0)
    except:
        return 1