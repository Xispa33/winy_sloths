#!/usr/bin/python3
# -*- coding: utf-8 -*-

import binance

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