#!/usr/bin/python3
# -*- coding: utf-8 -*-

import binance
from constants import *

def I__FUTURES_ACCOUNT_TRADES(client, symbol):
    """
    Name : I__FUTURES_ACCOUNT_TRADES()
    
    Parameters : 
        client : binance.client
            Client used to connect to Binance server
        symbol : str
            Currency traded
    
    Description : Gets a symbol's trade history of a futures account. 
                  Client contains the API key credentials allowing to connect to Binance server
    """
    err_cpt = 0
    ret = 1

    while (err_cpt < MAX_RETRY) and (ret == 1):
        try:
            ret = client.futures_position_information(symbol=symbol, timestamp=client.futures_time())
        except:
            ret = 1
            err_cpt += 1

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
    err_cpt = 0
    ret = 1

    while (err_cpt < MAX_RETRY) and (ret == 1):
        try:
            ret = client.get_all_orders(symbol=symbol, limit='1')
        except:
            ret = 1
            err_cpt += 1
    
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


def I__CLOSE_LONG_SPOT(client, symbol):
    """
    Name : I__CLOSE_LONG_SPOT()
    
    Parameters : 
        client : binance.client
            Client used to connect to Binance server
        symbol : str
            Currency traded
    
    Description : ...
    """
    err_cpt = 0
    ret = 1

    if (symbol == BTCUSDT):
        curr_asset = BTC
    elif (symbol == ETHUSDT):
        curr_asset = ETH
    else:
        return 1

    while (err_cpt < MAX_RETRY) and (ret == 1):
        try:
            price = client.get_avg_price(symbol=symbol)[PRICE]
            asset = round(float(client.get_asset_balance(asset=curr_asset)[FREE])*float(price) - 0.05,1)
            client.create_order(symbol=symbol, side=SELL, type=MARKET, quoteOrderQty=asset, timestamp=client.get_server_time())
            ret = 0
        except:
            ret = 1
            err_cpt += 1
    
    return ret

def I__CLOSE_LONG_FUTURES(client, symbol):
    """
    Name : I__CLOSE_LONG_FUTURES()
    
    Parameters : 
        client : binance.client
            Client used to connect to Binance server
        symbol : str
            Currency traded
    
    Description : ...
    """
    err_cpt = 1
    ret = 1
    while (err_cpt < MAX_RETRY) and (ret == 1):
        try:
            last_trade = I__FUTURES_ACCOUNT_TRADES(client, symbol)
            client.futures_create_order(symbol=symbol, positionside=LONG, side=SELL, \
                                            closePosition='true', type=MARKET, quantity=last_trade[0][POSITION_AMT], \
                                            timestamp=client.futures_time())
            ret = 0
        except:
            ret = 1
            err_cpt += 1
    
    return ret

def I__CLOSE_LONG(client, master_api):
    """
    Name : I__CLOSE_LONG()
    
    Parameters : 
        client : binance.client
            Client used to connect to Binance server
        master_api : ApiKeyMaster
            ...
    
    Description : ...
    """
    if (master_api.account_type == SPOT):
        ret = I__CLOSE_LONG_SPOT(client, master_api.symbol)
    elif (master_api.account_type == FUTURES):
        ret = I__CLOSE_LONG_FUTURES(client, master_api.symbol, master_api.markPrice)
    else:
        ret = 1
        
    return ret

def I__OPEN_LONG_SPOT(client, symbol):
    """
    Name : I__OPEN_LONG_SPOT()
    
    Parameters : 
        client : binance.client
            Client used to connect to Binance server
        symbol : str
            Currency traded
    
    Description : ...
    """
    err_cpt = 0
    ret = 1

    while (err_cpt < MAX_RETRY) and (ret == 1):
        try:
            usdt_asset = client.get_asset_balance(asset=USDT)[FREE]
            asset_round=round(usdt_asset-0.05,1)

            client.create_order(symbol=symbol, side=BUY, type=MARKET, quoteOrderQty=asset_round, timestamp=client.get_server_time())
            ret = 0
        except:
            ret = 1
            err_cpt += 1
    
    return ret

def I__OPEN_LONG_FUTURES(client, symbol, leverage, engaged_balance, entryPrice):
    """
    Name : I__OPEN_LONG_SPOT()
    
    Parameters : 
        client : binance.client
            Client used to connect to Binance server
        master_api : ApiKeyMaster
            ...
    
    Description : ...
    """
    err_cpt = 0
    ret = 1

    while (err_cpt < MAX_RETRY) and (ret == 1):
        try:
            client.futures_change_position_mode(dualSidePosition='true',timestamp=client.futures_time())
            
            client.futures_change_leverage(symbol=symbol,leverage=leverage,timestamp=client.futures_time())

            ret=client.futures_account_balance(timestamp=client.futures_time())
            balance=ret[0][WITHDRAW_AVAILABLE]

            quantity=round(((float(balance)*engaged_balance/entryPrice)-0.0005),3)

            client.futures_create_order(symbol=BTCUSDT, side=BUY, positionSide=LONG, type=MARKET, quantity=quantity ,timestamp=client.futures_time())

            ret = 0
        except:
            ret = 1
            err_cpt += 1
    
    return ret

def I__OPEN_LONG(client, master_api):
    """
    Name : I__OPEN_LONG()
    
    Parameters : 
        client : binance.client
            Client used to connect to Binance server
        master_api : ApiKeyMaster
            ...
    
    Description : ...
    """
    if (master_api.account_type == SPOT):
        ret = I__OPEN_LONG_SPOT(client, master_api.symbol)
    elif (master_api.account_type == FUTURES):
        ret = I__OPEN_LONG_FUTURES(client, master_api)
    else:
        ret = 1

    return ret




def I__GET_FUTURES_ACCOUNT_BALANCE(client):
    """
    Name : I__GET_FUTURES_ACCOUNT()
    
    Parameters : 
        client : binance.client
            Client used to connect to Binance server
    
    Description : ...
    """
    err_cpt = 0
    ret = 1

    while (err_cpt < MAX_RETRY) and (ret == 1):
        try:
            ret = client.futures_account_balance(timestamp=client.futures_time())
        except:
            ret = 1
            err_cpt += 1
    
    return ret

def I__CLOSE_SHORT(client, symbol):
    """
    Name : I__CLOSE_SHORT()
    
    Parameters : 
        client : binance.client
            Client used to connect to Binance server
        master_api : ApiKeyMaster
            ...
    
    Description : ...
    """
    err_cpt = 0
    ret = 1

    while (err_cpt < MAX_RETRY) and (ret == 1):
        try:
            last_trade = I__FUTURES_ACCOUNT_TRADES(client, symbol)
            client.futures_create_order(symbol=symbol, positionside=SHORT, side=BUY, \
                                            closePosition='true', type=MARKET, quantity=last_trade[0][POSITION_AMT], \
                                            timestamp=client.futures_time())
            ret = 0
        except:
            ret = 1
            err_cpt += 1
    
    return ret
    
def I__OPEN_SHORT(client, master_api, leverage, engaged_balance, entryPrice):
    """
    Name : I__OPEN_SHORT()
    
    Parameters : 
        client : binance.client
            Client used to connect to Binance server
        master_api : ApiKeyMaster
            ...
    
    Description : ...
    """
    err_cpt = 0
    ret = 1

    while (err_cpt < MAX_RETRY) and (ret == 1):
        try:
            client.futures_change_position_mode(dualSidePosition='true',timestamp=client.futures_time())
            client.futures_change_leverage(symbol=BTCUSDT,leverage=leverage,timestamp=client.futures_time())

            client.futures_change_leverage(symbol=BTCUSDT,leverage=leverage,timestamp=client.futures_time())

            ret=client.futures_account_balance(timestamp=client.futures_time())
            balance=ret[0][WITHDRAW_AVAILABLE]

            quantity=round(((float(balance)*engaged_balance/entryPrice)-0.0005),3)

            client.futures_create_order(symbol=BTCUSDT, side=SELL, positionSide=SHORT, type=MARKET, quantity=quantity ,timestamp=client.futures_time())

            ret = 0
        except:
            ret = 1
            err_cpt += 1
    
    return ret