#!/usr/bin/python3
# -*- coding: utf-8 -*-

import binance

SPOT = 'SPOT'
FUTURE = 'FUTURE'

def I__GET_SYSTEM_STATUS(client):
    try:
        ret = client.get_system_status()['status']
    except:
        ret = 2
    
    return ret

def I__FUTURES_ACCOUNT_TRADES(client):
    try:
        ret = client.futures_account_trades()
    except:
        ret = 1
    
    return ret

def I__SPOT_ACCOUNT_TRADES(client):
    try:
        #TODO: Modifier fonction
        ret = client.futures_account_trades()
    except:
        ret = 1
    
    return ret

def I__GET_ACCOUNT_HISTORY(client, account_type):
    if (account_type == SPOT):
        return I__SPOT_ACCOUNT_TRADES(client)
    elif (account_type == FUTURE):
        return I__FUTURES_ACCOUNT_TRADES(client)
    else:
        return 1